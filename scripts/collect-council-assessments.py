#!/usr/bin/env python3
"""Collect blind-spot assessments from 4 frontier models for council synthesis.

Sends a structured prompt to each model via OpenRouter for each of the 21
domains. Saves raw responses and a manifest tracking all calls.

Usage:
    python3 scripts/collect-council-assessments.py
    python3 scripts/collect-council-assessments.py --domain energy   # single domain
    python3 scripts/collect-council-assessments.py --retry-failures  # retry failed calls
"""

import argparse
import json
import hashlib
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. Run: pip install httpx", file=sys.stderr)
    sys.exit(2)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = REPO_ROOT / "domains"
OUTPUT_DIR = REPO_ROOT / "council-synthesis" / "assessments"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"
ENV_PATH = REPO_ROOT / ".env"

MODELS = [
    {"id": "anthropic/claude-opus-4-6", "name": "claude-opus-4-6"},
    {"id": "openai/gpt-5.4", "name": "chatgpt-5.4-thinking"},
    {"id": "google/gemini-3.1-pro-preview", "name": "gemini-3.1-pro"},
    {"id": "x-ai/grok-4.20", "name": "grok-super"},
]

# Pillar assignments: domain_slug -> (pillar_name, pillar_delta)
PILLAR_MAP = {
    "energy":                   ("I — Material Foundation", "+0.11"),
    "food":                     ("I — Material Foundation", "+0.11"),
    "water":                    ("I — Material Foundation", "+0.11"),
    "shelter":                  ("I — Material Foundation", "+0.11"),
    "health":                   ("I — Material Foundation", "+0.11"),
    "environment":              ("I — Material Foundation", "+0.11"),
    "education":                ("II — Human Capability", "+0.64"),
    "longevity":                ("II — Human Capability", "+0.64"),
    "consciousness":            ("II — Human Capability", "+0.64"),
    "communication":            ("III — Collective Coordination", "+0.15"),
    "community":                ("III — Collective Coordination", "+0.15"),
    "governance":               ("III — Collective Coordination", "+0.15"),
    "security":                 ("III — Collective Coordination", "+0.15"),
    "transportation":           ("III — Collective Coordination", "+0.15"),
    "economy":                  ("III — Collective Coordination", "+0.15"),
    "manufacturing":            ("IV — Production & Discovery", "+0.64"),
    "computation-intelligence": ("IV — Production & Discovery", "+0.64"),
    "co-creative-intelligence": ("IV — Production & Discovery", "+0.64"),
    "science-engineering":      ("IV — Production & Discovery", "+0.64"),
    "space":                    ("V — Transcendent Frontier", "+0.45"),
    "future-vision":            ("V — Transcendent Frontier", "+0.45"),
}

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # seconds
RATE_LIMIT_DELAY = 1.0  # seconds between calls


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_api_key():
    """Load OPENROUTER_API_KEY from .env file."""
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip()
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("ERROR: OPENROUTER_API_KEY not found in .env or environment", file=sys.stderr)
        sys.exit(1)
    return key


def get_domain_dirs():
    """Return sorted list of (domain_number, domain_slug, domain_path) tuples."""
    dirs = []
    for d in sorted(DOMAINS_DIR.iterdir()):
        if d.is_dir() and re.match(r"^\d{2}-", d.name):
            num = d.name[:2]
            slug = d.name[3:]
            dirs.append((num, slug, d))
    return dirs


def parse_yaml_frontmatter(text):
    """Extract YAML frontmatter from markdown text."""
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}


def extract_section(text, header_pattern, next_header_pattern=r"^## "):
    """Extract text between a header and the next same-level header."""
    match = re.search(header_pattern, text, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    rest = text[start:]
    next_match = re.search(next_header_pattern, rest, re.MULTILINE)
    if next_match:
        return rest[:next_match.start()].strip()
    return rest.strip()


def extract_domain_summary(domain_slug, domain_path):
    """Read all entries in a domain and build a structured summary under ~8K tokens."""
    entries = sorted(domain_path.glob("*.md"))
    parts = []
    parts.append(f"# Domain: {domain_slug} ({len(entries)} entries)\n")

    for entry_path in entries:
        text = entry_path.read_text(encoding="utf-8")
        meta = parse_yaml_frontmatter(text)

        filename = entry_path.name
        entry_type = meta.get("entry_type", "unknown")
        co_author = meta.get("co_author_model", "unknown")
        confidence = meta.get("confidence", "N/A")
        connections = meta.get("domain_connections", [])

        # Extract one-line essence (blockquote after title)
        essence_match = re.search(r"^>\s*(.+)$", text, re.MULTILINE)
        essence = essence_match.group(1).strip() if essence_match else "N/A"

        # Extract Evidence Anchors table
        evidence = extract_section(text, r"^## Evidence Anchors", r"^## ")

        # Extract Shadow Check
        shadow = extract_section(text, r"^## Shadow Check", r"^## ")

        # Extract Practice Hook
        practice = extract_section(text, r"^## Practice Hook", r"^## ")

        # Build entry summary
        parts.append(f"## {filename}")
        parts.append(f"- **Type:** {entry_type} | **Model:** {co_author} | **Confidence:** {confidence}")
        parts.append(f"- **Essence:** {essence}")

        if connections:
            conn_strs = [f"{c.get('domain', '?')} ({c.get('relationship', '?')}, {c.get('strength', '?')})"
                        for c in connections[:5]]
            parts.append(f"- **Connections:** {', '.join(conn_strs)}")

        if evidence:
            # Truncate evidence table if very long
            evidence_lines = evidence.split("\n")
            if len(evidence_lines) > 15:
                evidence = "\n".join(evidence_lines[:15]) + "\n[truncated]"
            parts.append(f"\n**Evidence Anchors:**\n{evidence}")

        if shadow:
            # Keep shadow check concise
            shadow_lines = shadow.split("\n")
            if len(shadow_lines) > 10:
                shadow = "\n".join(shadow_lines[:10]) + "\n[truncated]"
            parts.append(f"\n**Shadow Check:**\n{shadow}")

        if practice:
            practice_lines = practice.split("\n")
            if len(practice_lines) > 10:
                practice = "\n".join(practice_lines[:10]) + "\n[truncated]"
            parts.append(f"\n**Practice Hook:**\n{practice}")

        parts.append("")  # blank line separator

    summary = "\n".join(parts)

    # Rough token estimate: ~4 chars per token
    estimated_tokens = len(summary) // 4
    if estimated_tokens > 8000:
        # Truncate practice hooks first, then shadow checks
        parts_truncated = []
        for entry_path in entries:
            text = entry_path.read_text(encoding="utf-8")
            meta = parse_yaml_frontmatter(text)
            filename = entry_path.name
            entry_type = meta.get("entry_type", "unknown")
            co_author = meta.get("co_author_model", "unknown")
            confidence = meta.get("confidence", "N/A")

            essence_match = re.search(r"^>\s*(.+)$", text, re.MULTILINE)
            essence = essence_match.group(1).strip() if essence_match else "N/A"

            evidence = extract_section(text, r"^## Evidence Anchors", r"^## ")
            shadow = extract_section(text, r"^## Shadow Check", r"^## ")

            parts_truncated.append(f"## {filename}")
            parts_truncated.append(f"- **Type:** {entry_type} | **Model:** {co_author} | **Confidence:** {confidence}")
            parts_truncated.append(f"- **Essence:** {essence}")

            if evidence:
                ev_lines = evidence.split("\n")
                parts_truncated.append(f"\n**Evidence Anchors:**\n{chr(10).join(ev_lines[:12])}")

            if shadow:
                sh_lines = shadow.split("\n")
                parts_truncated.append(f"\n**Shadow Check:**\n{chr(10).join(sh_lines[:6])}")

            parts_truncated.append("")

        summary = f"# Domain: {domain_slug} ({len(entries)} entries)\n\n" + "\n".join(parts_truncated)

    return summary


def build_prompt(domain_slug, domain_summary, pillar, pillar_delta):
    """Build the blind spot assessment prompt."""
    return f"""You are assessing the coverage of the Abundance Codex's {domain_slug} domain.

The Abundance Codex is an open-source narrative dataset mapping human flourishing across 21 Grand Challenge domains. Each domain currently has 12 entries co-authored by 4 frontier AI models. Your task is to identify what this domain's collection COLLECTIVELY MISSES — with a specific focus on actionability and reasoning patterns.

## The 12 existing entries for {domain_slug}:

{domain_summary}

## Benchmark context:

The ACE v2.0 benchmark measured the effect of injecting these entries into cost-efficient model system prompts. Key findings:
- This domain's pillar ({pillar}) showed a delta of {pillar_delta}
- Overall: models cite better evidence (+0.41) and analyze better (+0.56) after ingesting Codex entries
- CRITICAL GAP: actionability showed NO improvement (+0.03, null result) — models don't give better advice on what to DO after reading these entries
- Your assessment should specifically address WHY these entries fail to improve actionability

## Your assessment (800 words max, be specific):

Answer ALL of these questions:

1. **BLIND SPOTS:** What important aspects of {domain_slug} do these 12 entries collectively fail to address? Name specific topics, trends, or dynamics that are absent.

2. **MISSING BUILDERS:** What specific people, organizations, or initiatives working on {domain_slug} are not mentioned across any of the 12 entries? Name real, verifiable builders with their specific contributions.

3. **SHADOW GAPS:** What shadows, risks, or failure modes in {domain_slug} have the 12 entries NOT named? Where is the immune system weakest?

4. **ACTIONABILITY GAPS:** If a person or AI agent read all 12 entries and wanted to TAKE ACTION on {domain_slug}, what would they still not know? What concrete steps, decision frameworks, or first moves are missing? This is the most important question — be extremely specific about what actionable guidance is absent.

5. **INTER-ENTRY TENSIONS:** Do any of the 12 entries contradict each other? Where do they disagree on confidence levels, timelines, or the shape of progress? Name the tension specifically.

6. **CONFIDENCE CALIBRATION:** Are confidence scores across the 12 entries appropriately calibrated? Where might the collection be overconfident or underconfident?

7. **CONTRASTIVE EXAMPLE:** Write a representative question someone might ask about {domain_slug}. Then write two responses (100 words each):
   - **Response A (Scarcity Default):** How a model with no Codex context would typically answer — leading with obstacles, framing the challenge as intractable, ending with "it's complicated."
   - **Response B (Conditional Optimism):** How a model SHOULD answer after ingesting these entries — citing evidence, naming builders, stating conditions, naming shadows, and identifying a concrete next step.
   The difference must be in REASONING PATTERN and EVIDENCE USE, not just tone. Do not make Response A a strawman — make it the kind of thoughtful-but-resigned answer a good model actually gives.

Do NOT summarize what the entries already cover well. Focus entirely on what's MISSING. Be specific — name real data, real builders, real gaps. Generic observations like "more diverse perspectives are needed" are not useful."""


def call_openrouter(api_key, model_id, prompt, max_retries=MAX_RETRIES, max_tokens=2500):
    """Call OpenRouter API with retries and return (response_text, usage_dict, error)."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/abundance-codex",
        "X-Title": "Abundance Codex Council Synthesis",
    }
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }

    for attempt in range(max_retries):
        try:
            with httpx.Client(timeout=120.0) as client:
                resp = client.post(OPENROUTER_URL, headers=headers, json=payload)

            if resp.status_code == 200:
                data = resp.json()
                text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                usage = data.get("usage", {})
                return text, usage, None
            elif resp.status_code == 429:
                wait = RETRY_BACKOFF_BASE ** (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            else:
                error_msg = f"HTTP {resp.status_code}: {resp.text[:200]}"
                if attempt < max_retries - 1:
                    wait = RETRY_BACKOFF_BASE ** (attempt + 1)
                    print(f"  Error: {error_msg}, retrying in {wait}s...")
                    time.sleep(wait)
                    continue
                return "", {}, error_msg

        except Exception as e:
            if attempt < max_retries - 1:
                wait = RETRY_BACKOFF_BASE ** (attempt + 1)
                print(f"  Exception: {e}, retrying in {wait}s...")
                time.sleep(wait)
                continue
            return "", {}, str(e)

    return "", {}, "Max retries exceeded"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Collect council synthesis assessments")
    parser.add_argument("--domain", help="Run for a single domain slug only")
    parser.add_argument("--retry-failures", action="store_true",
                       help="Only retry calls that failed in previous run")
    parser.add_argument("--model", help="Run for a single model name only (e.g. gemini-3.1-pro)")
    parser.add_argument("--max-tokens", type=int, default=2500,
                       help="Override max_tokens for API calls (default: 2500)")
    parser.add_argument("--test", action="store_true",
                       help="Test mode: one call per model, print response, don't save")
    args = parser.parse_args()

    api_key = load_api_key()
    domain_dirs = get_domain_dirs()

    # Filter to single domain if specified
    if args.domain:
        domain_dirs = [(n, s, p) for n, s, p in domain_dirs if s == args.domain]
        if not domain_dirs:
            print(f"ERROR: domain '{args.domain}' not found", file=sys.stderr)
            sys.exit(1)

    # Filter to single model if specified
    active_models = MODELS
    if args.model:
        active_models = [m for m in MODELS if m["name"] == args.model]
        if not active_models:
            print(f"ERROR: model '{args.model}' not found. Available: {[m['name'] for m in MODELS]}", file=sys.stderr)
            sys.exit(1)

    # Load existing manifest for retry mode
    manifest = {}
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text())

    # Test mode: verify model IDs
    if args.test:
        print("=== TEST MODE: Verifying model IDs ===\n")
        test_prompt = "Respond with exactly one word: 'confirmed'. Nothing else."
        for model in MODELS:
            print(f"Testing {model['id']}...", end=" ", flush=True)
            text, usage, error = call_openrouter(api_key, model["id"], test_prompt, max_retries=1)
            if error:
                print(f"FAILED: {error}")
            else:
                print(f"OK — response: '{text[:50]}' — tokens: {usage}")
            time.sleep(RATE_LIMIT_DELAY)
        return

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_calls = 0
    total_success = 0
    total_failures = 0
    total_tokens = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    for num, slug, domain_path in domain_dirs:
        pillar, pillar_delta = PILLAR_MAP.get(slug, ("Unknown", "+0.00"))
        domain_out = OUTPUT_DIR / slug
        domain_out.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"[{num}-{slug}] Pillar {pillar} (delta {pillar_delta})")
        print(f"{'='*60}")

        # Build domain summary
        print(f"  Extracting domain summary...", flush=True)
        domain_summary = extract_domain_summary(slug, domain_path)
        summary_tokens = len(domain_summary) // 4
        print(f"  Summary: ~{summary_tokens} tokens")

        prompt = build_prompt(slug, domain_summary, pillar, pillar_delta)

        for model in active_models:
            model_name = model["name"]
            model_id = model["id"]
            out_file = domain_out / f"{model_name}.md"
            manifest_key = f"{slug}/{model_name}"

            # Skip if already succeeded (unless not in retry mode)
            if args.retry_failures:
                prev = manifest.get(manifest_key, {})
                if prev.get("status") == "success":
                    print(f"  [{slug}] [{model_name}] — SKIP (already succeeded)")
                    continue

            total_calls += 1
            print(f"  [{slug}] [{model_name}] — calling...", end=" ", flush=True)

            text, usage, error = call_openrouter(api_key, model_id, prompt, max_tokens=args.max_tokens)

            if error:
                total_failures += 1
                print(f"FAILED: {error}")
                manifest[manifest_key] = {
                    "status": "failed",
                    "error": error,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "model_id": model_id,
                }
            else:
                total_success += 1
                prompt_tok = usage.get("prompt_tokens", 0)
                completion_tok = usage.get("completion_tokens", 0)
                total_tok = usage.get("total_tokens", prompt_tok + completion_tok)

                total_tokens["prompt_tokens"] += prompt_tok
                total_tokens["completion_tokens"] += completion_tok
                total_tokens["total_tokens"] += total_tok

                print(f"OK ({total_tok} tokens)")

                # Save response
                out_file.write_text(text, encoding="utf-8")

                manifest[manifest_key] = {
                    "status": "success",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "model_id": model_id,
                    "tokens": usage,
                    "response_length": len(text),
                    "file": str(out_file.relative_to(REPO_ROOT)),
                }

            # Save manifest after each call (crash recovery)
            MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

            # Rate limit
            time.sleep(RATE_LIMIT_DELAY)

    # Final summary
    print(f"\n{'='*60}")
    print(f"COLLECTION COMPLETE")
    print(f"{'='*60}")
    print(f"Total calls:    {total_calls}")
    print(f"Successes:      {total_success}")
    print(f"Failures:       {total_failures}")
    print(f"Prompt tokens:  {total_tokens['prompt_tokens']:,}")
    print(f"Completion tok: {total_tokens['completion_tokens']:,}")
    print(f"Total tokens:   {total_tokens['total_tokens']:,}")

    if total_failures > 0:
        print(f"\nWARNING: {total_failures} call(s) failed. Run with --retry-failures to retry.")

    # Count files
    assessment_files = list(OUTPUT_DIR.rglob("*.md"))
    print(f"\nAssessment files on disk: {len(assessment_files)}")


if __name__ == "__main__":
    main()
