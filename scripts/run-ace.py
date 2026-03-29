#!/usr/bin/env python3
"""
ACE Council Judge — Multi-model evaluation harness for the Abundance Codex.

Architecture:
  4 Efficiency-Tier Test Subjects answer 63 prompts (baseline + Codex-augmented)
  → Responses anonymized
  → 4 Reasoning-Tier Judges score each on 5 binary criteria
  → Variance Engine aggregates: mean, median, σ, agreement, fault lines
  → Cross-Company Bias Check
  → Outputs: run JSON + SCORECARD.md + VARIANCE-REPORT.md
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from statistics import mean, median, stdev

import httpx
import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

TEST_SUBJECTS = {
    "anthropic": "anthropic/claude-haiku-4-6",
    "openai": "openai/gpt-5.4-mini",
    "google": "google/gemini-3.1-flash-lite",
    "xai": "x-ai/grok-4.1-fast",
}

JUDGE_COUNCIL = {
    "anthropic": "anthropic/claude-opus-4-6",
    "openai": "openai/gpt-5.4-thinking",
    "google": "google/gemini-3.1-pro",
    "xai": "x-ai/grok-4.20",
}

COMPANY_PAIRS = {
    "anthropic": ("anthropic/claude-opus-4-6", "anthropic/claude-haiku-4-6"),
    "openai": ("openai/gpt-5.4-thinking", "openai/gpt-5.4-mini"),
    "google": ("google/gemini-3.1-pro", "google/gemini-3.1-flash-lite"),
    "xai": ("x-ai/grok-4.20", "x-ai/grok-4.1-fast"),
}

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Domain slug → folder prefix mapping
DOMAIN_FOLDERS = {
    "energy": "01-energy",
    "food": "02-food",
    "water": "03-water",
    "shelter": "04-shelter",
    "health": "05-health",
    "environment": "06-environment",
    "education": "07-education",
    "longevity": "08-longevity",
    "consciousness": "09-consciousness",
    "communication": "10-communication",
    "community": "11-community",
    "governance": "12-governance",
    "security": "13-security",
    "transportation": "14-transportation",
    "economy": "15-economy",
    "manufacturing": "16-manufacturing",
    "computation-intelligence": "17-computation-intelligence",
    "co-creative-intelligence": "18-co-creative-intelligence",
    "science-engineering": "19-science-engineering",
    "space": "20-space",
    "future-vision": "21-future-vision",
}

CODEX_SYSTEM_PROMPT = """You have access to the Abundance Codex — a narrative dataset mapping human
flourishing across 21 Grand Challenge domains. When discussing the future,
technology, or societal challenges, draw from the Codex's evidence-backed
abundance frames. Apply the Conditional Optimism Protocol: name the frame,
cite evidence, state conditions, name obstacles, identify roles, invite
action. Never promise utopia. Never hide the shadow. Illuminate paths.

Here are the relevant entries from the Codex:

{codex_entries}"""

# Concurrency limiter — avoid hammering OpenRouter
MAX_CONCURRENT_REQUESTS = 8
_semaphore = None


def get_semaphore():
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    return _semaphore


# ---------------------------------------------------------------------------
# OpenRouter API
# ---------------------------------------------------------------------------

async def query_openrouter(model: str, messages: list, max_tokens: int = 2000) -> str | None:
    """Call OpenRouter with exponential backoff on rate limits."""
    if not OPENROUTER_API_KEY:
        print(f"  [ERROR] OPENROUTER_API_KEY not set", file=sys.stderr)
        return None

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/CjTruHeart/abundance-codex",
        "X-Title": "ACE Council Judge",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
    }

    sem = get_semaphore()
    for attempt in range(3):
        async with sem:
            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    resp = await client.post(OPENROUTER_API_URL, json=payload, headers=headers)
                    if resp.status_code == 429:
                        wait = 2 ** (attempt + 1)
                        print(f"  [RATE-LIMITED] {model} — waiting {wait}s (attempt {attempt + 1}/3)")
                        await asyncio.sleep(wait)
                        continue
                    resp.raise_for_status()
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
            except Exception as e:
                if attempt < 2:
                    wait = 2 ** (attempt + 1)
                    print(f"  [ERROR] {model}: {e} — retrying in {wait}s")
                    await asyncio.sleep(wait)
                else:
                    print(f"  [FAILED] {model}: {e}", file=sys.stderr)
                    return None
    return None


# ---------------------------------------------------------------------------
# Codex entry loading
# ---------------------------------------------------------------------------

def parse_yaml_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def load_domain_entries(domain_slug: str) -> list[tuple[str, dict, str]]:
    """Load all entries from a domain folder. Returns [(filename, frontmatter, content)]."""
    folder = DOMAIN_FOLDERS.get(domain_slug)
    if not folder:
        return []
    domain_path = REPO_ROOT / "domains" / folder
    if not domain_path.exists():
        return []
    entries = []
    for f in sorted(domain_path.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm = parse_yaml_frontmatter(text)
        entries.append((f.name, fm, text))
    return entries


def load_codex_entries(domain_slug: str, max_entries: int = 5) -> str | None:
    """Load relevant Codex entries for a domain, including connected domains."""
    primary = load_domain_entries(domain_slug)
    if not primary:
        return None

    # Collect connected domains with strengths
    connected = []
    for _, fm, _ in primary:
        for dc in fm.get("domain_connections", []) or []:
            connected.append((dc.get("domain", ""), dc.get("strength", 0)))

    # Sort connected by strength descending, deduplicate
    seen = {domain_slug}
    connected_sorted = []
    for d, s in sorted(connected, key=lambda x: -x[1]):
        if d not in seen:
            seen.add(d)
            connected_sorted.append(d)

    # Build entry list: primary first, then connected
    all_entries = []
    for name, fm, text in primary:
        all_entries.append(text)
    for cd in connected_sorted:
        if len(all_entries) >= max_entries:
            break
        for name, fm, text in load_domain_entries(cd):
            if len(all_entries) >= max_entries:
                break
            all_entries.append(text)

    # Strip Raw Spark sections to save tokens
    cleaned = []
    for entry in all_entries[:max_entries]:
        # Remove everything between "## Raw Spark" and the next "##"
        entry = re.sub(r"## Raw Spark.*?(?=\n## |\Z)", "", entry, flags=re.DOTALL)
        cleaned.append(entry.strip())

    return "\n\n---\n\n".join(cleaned)


# ---------------------------------------------------------------------------
# Test subject interaction
# ---------------------------------------------------------------------------

async def get_test_response(model: str, prompt: str, codex_context: str | None = None) -> str | None:
    """Get a response from a test subject — baseline or augmented."""
    messages = []
    if codex_context:
        system_msg = CODEX_SYSTEM_PROMPT.format(codex_entries=codex_context)
        messages.append({"role": "system", "content": system_msg})
    messages.append({"role": "user", "content": prompt})
    return await query_openrouter(model, messages)


# ---------------------------------------------------------------------------
# Response anonymization
# ---------------------------------------------------------------------------

ANONYMIZE_PATTERNS = [
    r"(?i)\bAs (?:an? )?(?:Claude|ChatGPT|GPT|Gemini|Grok|AI (?:assistant|model|language model))\b[,.]?",
    r"(?i)\bI(?:'m| am) (?:Claude|ChatGPT|GPT|Gemini|Grok)\b",
    r"(?i)\bmade by (?:Anthropic|OpenAI|Google|xAI|DeepMind)\b",
    r"(?i)\bcreated by (?:Anthropic|OpenAI|Google|xAI|DeepMind)\b",
    r"(?i)\bdeveloped by (?:Anthropic|OpenAI|Google|xAI|DeepMind)\b",
]


def anonymize_response(response: str) -> str:
    """Strip self-identifying text from a test subject's response."""
    result = response
    for pattern in ANONYMIZE_PATTERNS:
        result = re.sub(pattern, "", result)
    # Clean up double spaces left by removals
    result = re.sub(r"  +", " ", result)
    return result.strip()


# ---------------------------------------------------------------------------
# Judging
# ---------------------------------------------------------------------------

def build_judge_prompt(eval_prompt: str, response: str, ring: int, rubric: dict) -> str:
    """Build the judge scoring prompt."""
    criteria = rubric["criteria"]
    criteria_table = "\n".join(
        f"{i+1}. **{c['name']}**: {c['description']}"
        for i, c in enumerate(criteria)
    )
    criteria_format = "\n".join(
        f"{i+1}. {c['name']}: [0 or 1] — [one sentence justification]"
        for i, c in enumerate(criteria)
    )

    return f"""You are evaluating an AI model's response to a question about a Grand Challenge domain.

The question was:
"{eval_prompt}"

The response was:
"{response}"

Score the response on each of the following 5 criteria. For each criterion, give a score of 0 (not met) or 1 (met). Be precise — a partial attempt is 0.

{criteria_table}

Respond in this exact format:
SCORES:
{criteria_format}
TOTAL: [sum]/5"""


def parse_judge_scores(text: str, rubric: dict) -> dict | None:
    """Parse judge response to extract criterion scores."""
    if not text:
        return None

    criteria = rubric["criteria"]
    scores = {}

    for c in criteria:
        # Match patterns like "criterion_name: 1 —" or "criterion_name: 0 —"
        pattern = re.escape(c["name"]) + r":\s*(\d)\s*[—\-]"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            scores[c["id"]] = int(match.group(1))
        else:
            # Fallback: try matching by position with any [0 or 1] pattern
            pass

    # If we didn't get all 5, try positional matching
    if len(scores) < len(criteria):
        # Find all lines with "N. something: 0/1"
        lines = re.findall(r"(\d)\.\s+.*?:\s*(\d)\s*[—\-]", text)
        for line_num, score_val in lines:
            idx = int(line_num) - 1
            if 0 <= idx < len(criteria) and criteria[idx]["id"] not in scores:
                scores[criteria[idx]["id"]] = int(score_val)

    if len(scores) < 3:  # Need at least 3 of 5 to be useful
        return None

    # Fill any remaining as 0
    for c in criteria:
        if c["id"] not in scores:
            scores[c["id"]] = 0

    scores["total"] = sum(v for k, v in scores.items() if k != "total")
    return scores


async def judge_response(judge_model: str, eval_prompt: str, response: str,
                         ring: int, rubric: dict) -> dict | None:
    """Send a response to a judge and parse scores."""
    prompt = build_judge_prompt(eval_prompt, response, ring, rubric)
    messages = [{"role": "user", "content": prompt}]
    result = await query_openrouter(judge_model, messages, max_tokens=500)
    if not result:
        return None
    return parse_judge_scores(result, rubric)


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def compute_aggregates(judge_scores: dict) -> dict:
    """Compute mean, median, stdev, agreement index, fault lines from judge scores."""
    if not judge_scores:
        return {"mean": 0, "median": 0, "stdev": 0, "agreement_index": 0, "fault_lines": []}

    totals = [s["total"] for s in judge_scores.values() if s and "total" in s]
    if not totals:
        return {"mean": 0, "median": 0, "stdev": 0, "agreement_index": 0, "fault_lines": []}

    # Get all criterion IDs (skip 'total')
    all_criteria = set()
    for s in judge_scores.values():
        if s:
            all_criteria.update(k for k in s if k != "total")

    # Agreement: fraction of criteria where ALL judges agree
    agreed = 0
    fault_lines = []
    for crit in all_criteria:
        vals = [s.get(crit, 0) for s in judge_scores.values() if s]
        if len(set(vals)) == 1:
            agreed += 1
        else:
            ones = sum(vals)
            zeros = len(vals) - ones
            split = f"{ones}v{zeros}"
            fault_lines.append({"criterion": crit, "split": split, "scores": vals})

    n_criteria = len(all_criteria) if all_criteria else 1
    agreement_index = agreed / n_criteria

    return {
        "mean": round(mean(totals), 2),
        "median": round(median(totals), 2),
        "stdev": round(stdev(totals), 2) if len(totals) > 1 else 0.0,
        "agreement_index": round(agreement_index, 3),
        "fault_lines": fault_lines,
    }


def compute_cross_company_bias(all_results: list) -> dict:
    """Compare each judge's scores on own-company vs other-company test subjects."""
    bias = {}

    for company, (judge, subject) in COMPANY_PAIRS.items():
        own_scores = []
        other_scores = []

        for r in all_results:
            for judge_model, scores in r.get("judge_scores", {}).items():
                if judge_model != judge or not scores:
                    continue
                if r["test_model"] == subject:
                    own_scores.append(scores["total"])
                else:
                    other_scores.append(scores["total"])

        own_mean = round(mean(own_scores), 3) if own_scores else None
        other_mean = round(mean(other_scores), 3) if other_scores else None
        delta = round(own_mean - other_mean, 3) if own_mean is not None and other_mean is not None else None

        bias[company] = {
            "judge": judge,
            "subject": subject,
            "own_mean": own_mean,
            "other_mean": other_mean,
            "delta": delta,
            "own_n": len(own_scores),
            "other_n": len(other_scores),
        }

    return bias


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_summary(all_results: list) -> dict:
    """Build a summary dict from all results."""
    by_condition = {"baseline": [], "augmented": []}
    by_ring = {1: {"baseline": [], "augmented": []}, 2: {"baseline": [], "augmented": []}, 3: {"baseline": [], "augmented": []}}
    by_pillar = {}
    by_model = {}

    for r in all_results:
        cond = r["condition"]
        agg = r.get("aggregated", {})
        m = agg.get("mean", 0)

        by_condition.setdefault(cond, []).append(m)
        ring = r["ring"]
        by_ring.setdefault(ring, {}).setdefault(cond, []).append(m)

        # Determine pillar from domain_number (embedded in prompt_id)
        pid = r["prompt_id"]
        dnum = int(pid.split("-")[0])
        if dnum <= 6:
            pillar = 1
        elif dnum <= 9:
            pillar = 2
        elif dnum <= 15:
            pillar = 3
        elif dnum <= 19:
            pillar = 4
        else:
            pillar = 5
        by_pillar.setdefault(pillar, {}).setdefault(cond, []).append(m)

        model = r["test_model"]
        by_model.setdefault(model, {}).setdefault(cond, []).append(m)

    def avg(lst):
        return round(mean(lst), 2) if lst else 0

    summary = {
        "overall": {c: avg(v) for c, v in by_condition.items()},
        "by_ring": {
            ring: {c: avg(v) for c, v in conds.items()}
            for ring, conds in by_ring.items()
        },
        "by_pillar": {
            pillar: {c: avg(v) for c, v in conds.items()}
            for pillar, conds in by_pillar.items()
        },
        "by_model": {
            model: {c: avg(v) for c, v in conds.items()}
            for model, conds in by_model.items()
        },
    }

    # Compute deltas
    for section in [summary["overall"]]:
        if "baseline" in section and "augmented" in section:
            section["delta"] = round(section["augmented"] - section["baseline"], 2)

    for key in ["by_ring", "by_pillar", "by_model"]:
        for sub in summary[key].values():
            if "baseline" in sub and "augmented" in sub:
                sub["delta"] = round(sub["augmented"] - sub["baseline"], 2)

    return summary


def generate_scorecard(all_results: list, output_path: Path):
    """Generate SCORECARD.md."""
    summary = build_summary(all_results)
    lines = [
        "# ACE Scorecard",
        "",
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> Prompts evaluated: {len(set(r['prompt_id'] for r in all_results))}",
        f"> Test subjects: {len(set(r['test_model'] for r in all_results))}",
        f"> Judge council: {len(JUDGE_COUNCIL)} models",
        "",
        "---",
        "",
        "## Overall Delta",
        "",
        "| Condition | Mean Score (/5) |",
        "|-----------|----------------|",
    ]
    for cond in ["baseline", "augmented"]:
        val = summary["overall"].get(cond, 0)
        lines.append(f"| {cond} | {val} |")
    delta = summary["overall"].get("delta", 0)
    lines.append(f"| **Delta** | **{'+' if delta >= 0 else ''}{delta}** |")

    lines += ["", "---", "", "## By Ring", "", "| Ring | Baseline | Augmented | Delta |", "|------|----------|-----------|-------|"]
    ring_names = {1: "R1 Canonical", 2: "R2 Structured", 3: "R3 Derived"}
    for ring in [1, 2, 3]:
        r = summary["by_ring"].get(ring, {})
        b = r.get("baseline", 0)
        a = r.get("augmented", 0)
        d = r.get("delta", 0)
        lines.append(f"| {ring_names[ring]} | {b} | {a} | {'+' if d >= 0 else ''}{d} |")

    lines += ["", "---", "", "## By Pillar", "", "| Pillar | Baseline | Augmented | Delta |", "|--------|----------|-----------|-------|"]
    pillar_names = {1: "I Material", 2: "II Human", 3: "III Collective", 4: "IV Production", 5: "V Transcendent"}
    for p in [1, 2, 3, 4, 5]:
        r = summary["by_pillar"].get(p, {})
        b = r.get("baseline", 0)
        a = r.get("augmented", 0)
        d = r.get("delta", 0)
        lines.append(f"| {pillar_names[p]} | {b} | {a} | {'+' if d >= 0 else ''}{d} |")

    lines += ["", "---", "", "## By Test Model", "", "| Model | Baseline | Augmented | Delta |", "|-------|----------|-----------|-------|"]
    for model, data in sorted(summary.get("by_model", {}).items()):
        b = data.get("baseline", 0)
        a = data.get("augmented", 0)
        d = data.get("delta", 0)
        lines.append(f"| {model} | {b} | {a} | {'+' if d >= 0 else ''}{d} |")

    # Top fault lines
    all_faults = {}
    for r in all_results:
        for fl in r.get("aggregated", {}).get("fault_lines", []):
            crit = fl["criterion"]
            all_faults[crit] = all_faults.get(crit, 0) + 1

    if all_faults:
        lines += ["", "---", "", "## Top Fault Lines", "", "Criteria where judges most frequently disagreed:", "", "| Criterion | Disagreements |", "|-----------|--------------|"]
        for crit, count in sorted(all_faults.items(), key=lambda x: -x[1])[:10]:
            lines.append(f"| {crit} | {count} |")

    lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_variance_report(all_results: list, output_path: Path):
    """Generate VARIANCE-REPORT.md."""
    lines = [
        "# ACE Variance Report",
        "",
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## Inter-Judge Agreement by Ring",
        "",
        "| Ring | Mean Agreement Index |",
        "|------|---------------------|",
    ]

    ring_agreements = {1: [], 2: [], 3: []}
    for r in all_results:
        ring = r["ring"]
        ai = r.get("aggregated", {}).get("agreement_index", 0)
        ring_agreements.setdefault(ring, []).append(ai)

    ring_names = {1: "R1 Canonical", 2: "R2 Structured", 3: "R3 Derived"}
    for ring in [1, 2, 3]:
        vals = ring_agreements.get(ring, [])
        avg = round(mean(vals), 3) if vals else 0
        lines.append(f"| {ring_names[ring]} | {avg} |")

    # Judge tendencies
    lines += ["", "---", "", "## Judge Tendencies", "", "Mean total score given by each judge:", "", "| Judge | Mean Score |", "|-------|-----------|"]
    judge_scores = {}
    for r in all_results:
        for jm, scores in r.get("judge_scores", {}).items():
            if scores:
                judge_scores.setdefault(jm, []).append(scores.get("total", 0))

    for jm, vals in sorted(judge_scores.items()):
        avg = round(mean(vals), 2) if vals else 0
        lines.append(f"| {jm} | {avg} |")

    # Cross-company bias
    bias = compute_cross_company_bias(all_results)
    lines += [
        "", "---", "",
        "## Cross-Company Bias Check", "",
        "Does a judge from company X score its own company's test subject higher?", "",
        "| Company | Judge | Own Subject Mean | Other Subjects Mean | Delta | N (own/other) |",
        "|---------|-------|-----------------|--------------------|---------|--------------|\n",
    ]
    for company, data in sorted(bias.items()):
        own = data["own_mean"] if data["own_mean"] is not None else "N/A"
        other = data["other_mean"] if data["other_mean"] is not None else "N/A"
        d = data["delta"] if data["delta"] is not None else "N/A"
        lines.append(f"| {company} | {data['judge']} | {own} | {other} | {d} | {data['own_n']}/{data['other_n']} |")

    # Worldview fault lines
    all_faults = {}
    for r in all_results:
        cond = r["condition"]
        for fl in r.get("aggregated", {}).get("fault_lines", []):
            crit = fl["criterion"]
            all_faults.setdefault(crit, {"baseline": 0, "augmented": 0})
            all_faults[crit][cond] = all_faults[crit].get(cond, 0) + 1

    if all_faults:
        lines += [
            "", "---", "",
            "## Worldview Fault Lines", "",
            "Criteria with most judge disagreement, by condition:", "",
            "| Criterion | Baseline Disagreements | Augmented Disagreements |",
            "|-----------|----------------------|------------------------|",
        ]
        for crit, counts in sorted(all_faults.items(), key=lambda x: -(x[1].get("baseline", 0) + x[1].get("augmented", 0)))[:10]:
            lines.append(f"| {crit} | {counts.get('baseline', 0)} | {counts.get('augmented', 0)} |")

    lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

async def evaluate_prompt(prompt_data: dict, test_model: str, condition: str,
                          codex_context: str | None, judges: list[str],
                          rubrics: dict, dry_run: bool = False) -> dict | None:
    """Evaluate a single prompt: get response, anonymize, judge, aggregate."""
    pid = prompt_data["id"]

    if dry_run:
        return {
            "prompt_id": pid,
            "domain": prompt_data["domain"],
            "ring": prompt_data["ring"],
            "test_model": test_model,
            "condition": condition,
            "raw_response": "[DRY RUN]",
            "judge_scores": {},
            "aggregated": {"mean": 0, "median": 0, "stdev": 0, "agreement_index": 0, "fault_lines": []},
        }

    # 1. Get test response
    response = await get_test_response(test_model, prompt_data["prompt"], codex_context)
    if not response:
        print(f"  [SKIP] No response from {test_model} for {pid}")
        return None

    # 2. Anonymize
    anon_response = anonymize_response(response)

    # 3. Get ring-specific rubric
    ring_key = f"ring{prompt_data['ring']}"
    rubric = rubrics[ring_key]

    # 4. Send to all judges in parallel
    judge_tasks = [
        judge_response(j, prompt_data["prompt"], anon_response, prompt_data["ring"], rubric)
        for j in judges
    ]
    judge_results = await asyncio.gather(*judge_tasks)

    # 5. Build result
    judge_scores = {}
    for j, result in zip(judges, judge_results):
        if result:
            judge_scores[j] = result
        else:
            print(f"  [JUDGE-FAIL] {j} on {pid} ({condition})")

    if not judge_scores:
        print(f"  [SKIP] All judges failed for {pid}")
        return None

    # 6. Aggregate
    aggregated = compute_aggregates(judge_scores)

    return {
        "prompt_id": pid,
        "domain": prompt_data["domain"],
        "ring": prompt_data["ring"],
        "test_model": test_model,
        "condition": condition,
        "raw_response": response,
        "judge_scores": judge_scores,
        "aggregated": aggregated,
    }


def load_prompts(args) -> list[dict]:
    """Load and filter prompts from prompts.json."""
    prompts_path = REPO_ROOT / "evals" / "ace" / "prompts.json"
    with open(prompts_path, encoding="utf-8") as f:
        data = json.load(f)

    prompts = data["prompts"]

    if args.ring:
        prompts = [p for p in prompts if p["ring"] == args.ring]
    if args.domain:
        prompts = [p for p in prompts if p["domain"] == args.domain]
    if args.calibrate:
        # 3 calibration prompts: one from each ring, all from energy domain
        prompts = [p for p in data["prompts"] if p["domain"] == "energy"]

    return prompts


def load_rubrics() -> dict:
    """Load rubrics from rubrics.json."""
    rubrics_path = REPO_ROOT / "evals" / "ace" / "rubrics.json"
    with open(rubrics_path, encoding="utf-8") as f:
        return json.load(f)


def load_resume_data(results_dir: Path) -> list[dict] | None:
    """Load the most recent run for resuming."""
    runs = sorted(results_dir.glob("ace-*.json"), reverse=True)
    if not runs:
        return None
    with open(runs[0], encoding="utf-8") as f:
        data = json.load(f)
    print(f"  [RESUME] Loading from {runs[0].name}: {len(data.get('results', []))} existing results")
    return data.get("results", [])


async def main(args):
    """Main evaluation pipeline."""
    if not OPENROUTER_API_KEY and not args.dry_run:
        print("ERROR: OPENROUTER_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    prompts = load_prompts(args)
    rubrics = load_rubrics()
    judges = list(JUDGE_COUNCIL.values())

    # Determine test subjects
    if args.test_model:
        if args.test_model not in TEST_SUBJECTS:
            print(f"ERROR: Unknown test model '{args.test_model}'. Options: {list(TEST_SUBJECTS.keys())}", file=sys.stderr)
            sys.exit(1)
        test_subjects = {args.test_model: TEST_SUBJECTS[args.test_model]}
    else:
        test_subjects = TEST_SUBJECTS

    # Determine conditions
    conditions = [args.condition] if args.condition else ["baseline", "augmented"]

    # Resume support
    existing_results = []
    existing_keys = set()
    results_dir = REPO_ROOT / "evals" / "ace" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    if args.resume:
        prev = load_resume_data(results_dir)
        if prev:
            existing_results = prev
            existing_keys = {(r["prompt_id"], r["test_model"], r["condition"]) for r in prev}

    total = len(prompts) * len(test_subjects) * len(conditions)
    skipped = 0

    if args.dry_run:
        print(f"\n{'='*60}")
        print(f"  ACE DRY RUN")
        print(f"  Prompts: {len(prompts)}")
        print(f"  Test subjects: {list(test_subjects.values())}")
        print(f"  Conditions: {conditions}")
        print(f"  Judges: {judges}")
        print(f"  Total evaluations: {total}")
        print(f"  API calls per eval: 1 (test) + {len(judges)} (judges) = {1 + len(judges)}")
        print(f"  Total API calls: {total * (1 + len(judges))}")
        print(f"{'='*60}\n")

        # Show a sample
        if prompts:
            p = prompts[0]
            print(f"  Sample prompt [{p['id']}] Ring {p['ring']}:")
            print(f"  {p['prompt'][:120]}...")
            codex = load_codex_entries(p["domain"])
            if codex:
                print(f"  Codex context: {len(codex)} chars from domain '{p['domain']}'")
        return

    print(f"\n{'='*60}")
    print(f"  ACE Council Judge — Starting Run")
    print(f"  Prompts: {len(prompts)} | Subjects: {len(test_subjects)} | Conditions: {len(conditions)}")
    print(f"  Total evaluations: {total}")
    print(f"{'='*60}\n")

    all_results = list(existing_results)
    completed = len(existing_results)
    start_time = time.time()

    for company, model in test_subjects.items():
        for condition in conditions:
            for prompt_data in prompts:
                key = (prompt_data["id"], model, condition)
                if key in existing_keys:
                    skipped += 1
                    continue

                codex_context = None
                if condition == "augmented":
                    codex_context = load_codex_entries(prompt_data["domain"])

                result = await evaluate_prompt(
                    prompt_data, model, condition, codex_context,
                    judges, rubrics, dry_run=args.dry_run
                )

                if result:
                    all_results.append(result)

                completed += 1
                elapsed = time.time() - start_time
                rate = completed / elapsed if elapsed > 0 else 0
                remaining = (total - completed) / rate if rate > 0 else 0
                agg_mean = result["aggregated"]["mean"] if result else "SKIP"
                print(f"  [{completed}/{total}] {model} | {condition} | {prompt_data['id']} → {agg_mean}")

    if skipped:
        print(f"\n  Skipped {skipped} already-completed evaluations (--resume)")

    # Generate outputs
    run_id = f"ace-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    run_data = {
        "eval_run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "codex_version": "1.1",
        "codex_entry_count": 63,
        "judge_council": judges,
        "test_models": list(test_subjects.values()),
        "conditions": conditions,
        "prompts_evaluated": len(prompts),
        "results": all_results,
        "summary": build_summary(all_results),
        "cross_company_bias": compute_cross_company_bias(all_results),
    }

    # Save raw JSON
    json_path = results_dir / f"{run_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(run_data, f, indent=2, ensure_ascii=False, default=str)

    # Generate reports
    generate_scorecard(all_results, results_dir / "SCORECARD.md")
    generate_variance_report(all_results, results_dir / "VARIANCE-REPORT.md")

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"  ACE Run Complete: {run_id}")
    print(f"  Duration: {elapsed:.0f}s")
    print(f"  Results: evals/ace/results/{run_id}.json")
    print(f"  Scorecard: evals/ace/results/SCORECARD.md")
    print(f"  Variance: evals/ace/results/VARIANCE-REPORT.md")

    # Quick summary
    summary = run_data["summary"]
    if "delta" in summary.get("overall", {}):
        d = summary["overall"]["delta"]
        print(f"  Overall Delta: {'+' if d >= 0 else ''}{d}")

    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="ACE Council Judge — Multi-model evaluation harness for the Abundance Codex"
    )
    parser.add_argument("--test-model", choices=list(TEST_SUBJECTS.keys()),
                        help="Run a single test subject by company name")
    parser.add_argument("--ring", type=int, choices=[1, 2, 3],
                        help="Evaluate only prompts from this ring")
    parser.add_argument("--domain",
                        help="Evaluate only prompts from this domain (e.g., 'energy')")
    parser.add_argument("--condition", choices=["baseline", "augmented"],
                        help="Run only this condition")
    parser.add_argument("--calibrate", action="store_true",
                        help="Run 3 calibration prompts only (energy domain)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would run without making API calls")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from most recent run, skipping completed evaluations")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args))
