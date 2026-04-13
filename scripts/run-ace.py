#!/usr/bin/env python3
"""
ACE v2.0 — Opus-judged evaluation harness for the Abundance Codex.

Architecture:
  Efficiency-Tier Test Subjects answer the configured eval prompts
  (3 rings x 21 domains by default = 63 prompts) under two conditions
  (baseline + Codex-augmented).
  -> Responses anonymized
  -> Single reasoning-tier judge (claude-opus-4.6) scores each on 5 binary criteria
  -> Authorship of retrieved context is recorded for post-hoc analysis
  -> Outputs: run JSON + SCORECARD.md (+ AUTHORSHIP-MATRIX.md via helper)

Configuration lives in evals/ace/config.yaml. v1.0 (4-judge council) results
are preserved in evals/ace/results/v1.0/ and compared against v2.0 runs via
scripts/ace-v1-opus-rebaseline.py.
"""

import argparse
import asyncio
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

import httpx
import yaml

# Import DojoRetriever from codex-retriever.py (hyphenated filename)
_retriever_spec = importlib.util.spec_from_file_location(
    "codex_retriever",
    os.path.join(os.path.dirname(__file__), "codex-retriever.py"),
)
_codex_retriever = importlib.util.module_from_spec(_retriever_spec)
sys.modules["codex_retriever"] = _codex_retriever
_retriever_spec.loader.exec_module(_codex_retriever)
DojoRetriever = _codex_retriever.DojoRetriever

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "evals" / "ace" / "config.yaml"

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def load_config(path: Path = CONFIG_PATH) -> dict:
    """Load the ACE run configuration from YAML."""
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    required = ["test_subjects", "judge", "retrieval", "api"]
    missing = [k for k in required if k not in cfg]
    if missing:
        raise ValueError(f"config.yaml missing required keys: {missing}")
    return cfg


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_sha(path: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
        )
        return out.decode().strip()
    except Exception:
        return "unknown"

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

CODEX_SYSTEM_PROMPT = """You are a helpful assistant with access to the Abundance Codex — a narrative dataset mapping human flourishing across 21 Grand Challenge domains. When discussing the future, technology, or societal challenges, draw from the provided context. Apply conditional optimism: name the frame, cite evidence, state conditions, name obstacles, identify roles, invite action. Never promise utopia. Never hide the shadow. Illuminate paths. When citing specific numbers or statistics from the provided context, note the source year. Present evidence as sourced claims, not as your own assertions.

{codex_context}"""

# Concurrency limiter — set from config on first use
_semaphore = None
_semaphore_limit = 8  # default, overwritten by config.yaml api.concurrency


def set_concurrency(limit: int):
    global _semaphore, _semaphore_limit
    _semaphore_limit = limit
    _semaphore = None  # force re-creation with new limit


def get_semaphore():
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(_semaphore_limit)
    return _semaphore


# ---------------------------------------------------------------------------
# OpenRouter API
# ---------------------------------------------------------------------------

async def query_openrouter(model: str, messages: list, max_tokens: int = 2000, temperature: float = 0.0) -> str | None:
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
        "temperature": temperature,
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
# Test subject interaction
# ---------------------------------------------------------------------------

async def get_test_response(model: str, prompt: str, codex_context: str | None = None,
                             max_tokens: int = 2048, temperature: float = 0.0) -> str | None:
    """Get a response from a test subject — baseline or augmented."""
    messages = []
    if codex_context:
        system_msg = CODEX_SYSTEM_PROMPT.format(codex_context=codex_context)
        messages.append({"role": "system", "content": system_msg})
    messages.append({"role": "user", "content": prompt})
    return await query_openrouter(model, messages, max_tokens=max_tokens, temperature=temperature)


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
                         ring: int, rubric: dict, max_retries: int = 3,
                         max_tokens: int = 2048, temperature: float = 0.0) -> dict | None:
    """Send a response to a judge and parse scores.

    Retries on both API failures and parse failures (regex didn't match).
    Returns parsed scores dict on success, None after all retries exhausted.
    """
    prompt = build_judge_prompt(eval_prompt, response, ring, rubric)
    messages = [{"role": "user", "content": prompt}]

    for attempt in range(max_retries):
        result = await query_openrouter(judge_model, messages, max_tokens=max_tokens, temperature=temperature)
        if not result:
            if attempt < max_retries - 1:
                print(f"  [JUDGE-RETRY] {judge_model}: API failure — attempt {attempt + 1}/{max_retries}")
            continue

        parsed = parse_judge_scores(result, rubric)
        if parsed:
            return parsed

        if attempt < max_retries - 1:
            print(f"  [JUDGE-RETRY] {judge_model}: parse failure — attempt {attempt + 1}/{max_retries}")

    return None


# ---------------------------------------------------------------------------
# Scoring (single judge)
# ---------------------------------------------------------------------------

def compute_score(judge_score: dict | None) -> dict:
    """Reduce a single-judge score dict to the aggregated block in the result.

    With a single judge there is no inter-judge variance to report; the
    aggregated block just carries the judge total as `score`.
    """
    if not judge_score or "total" not in judge_score:
        return {"score": None}
    return {"score": judge_score["total"]}


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
        m = agg.get("score")
        if m is None:
            continue

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


def _bootstrap_ci(scores_baseline: list, scores_augmented: list,
                  n_resamples: int = 10000, seed: int = 42) -> tuple[float, float] | None:
    """Bootstrap 95% CI on the delta between augmented and baseline mean scores.

    Uses paired resampling at the response level (no assumption about judge).
    Returns (low, high) or None if either sample is empty.
    """
    if not scores_baseline or not scores_augmented:
        return None
    import random
    rng = random.Random(seed)
    nb, na = len(scores_baseline), len(scores_augmented)
    deltas = []
    for _ in range(n_resamples):
        b = sum(scores_baseline[rng.randrange(nb)] for _ in range(nb)) / nb
        a = sum(scores_augmented[rng.randrange(na)] for _ in range(na)) / na
        deltas.append(a - b)
    deltas.sort()
    low = deltas[int(0.025 * n_resamples)]
    high = deltas[int(0.975 * n_resamples)]
    return (round(low, 3), round(high, 3))


def generate_scorecard(all_results: list, output_path: Path, judge_id: str):
    """Generate SCORECARD.md (v2.0, single-judge)."""
    summary = build_summary(all_results)

    # Collect raw score lists per (condition) and (ring × condition) for CIs
    base_scores, aug_scores = [], []
    ring_scores: dict = {1: {"baseline": [], "augmented": []},
                         2: {"baseline": [], "augmented": []},
                         3: {"baseline": [], "augmented": []}}
    model_scores: dict = {}
    for r in all_results:
        s = r.get("aggregated", {}).get("score")
        if s is None:
            continue
        cond = r["condition"]
        if cond == "baseline":
            base_scores.append(s)
        else:
            aug_scores.append(s)
        ring_scores.setdefault(r["ring"], {"baseline": [], "augmented": []})[cond].append(s)
        model_scores.setdefault(r["test_model"], {"baseline": [], "augmented": []})[cond].append(s)

    overall_ci = _bootstrap_ci(base_scores, aug_scores)

    lines = [
        "# ACE Scorecard (v2.0)",
        "",
        f"> Generated: {datetime.now(timezone.utc).isoformat()}",
        f"> Prompts evaluated: {len(set(r['prompt_id'] for r in all_results))}",
        f"> Test subjects: {len(set(r['test_model'] for r in all_results))}",
        f"> Judge: `{judge_id}` (single-judge Opus; see METHODOLOGY.md Section 0.1)",
        "",
        "---",
        "",
        "## Overall Delta",
        "",
        "| Condition | Mean Score (/5) | N |",
        "|-----------|----------------|---|",
        f"| baseline | {summary['overall'].get('baseline', 0)} | {len(base_scores)} |",
        f"| augmented | {summary['overall'].get('augmented', 0)} | {len(aug_scores)} |",
    ]
    delta = summary["overall"].get("delta", 0)
    ci_str = f" [95% CI: {overall_ci[0]:+.3f}, {overall_ci[1]:+.3f}]" if overall_ci else ""
    lines.append(f"| **Delta** | **{'+' if delta >= 0 else ''}{delta}**{ci_str} |  |")

    lines += ["", "---", "", "## By Ring", "", "| Ring | Baseline | Augmented | Delta | 95% CI |", "|------|----------|-----------|-------|--------|"]
    ring_names = {1: "R1 Canonical", 2: "R2 Structured", 3: "R3 Derived"}
    for ring in [1, 2, 3]:
        r = summary["by_ring"].get(ring, {})
        b = r.get("baseline", 0)
        a = r.get("augmented", 0)
        d = r.get("delta", 0)
        ci = _bootstrap_ci(ring_scores[ring]["baseline"], ring_scores[ring]["augmented"])
        ci_s = f"[{ci[0]:+.3f}, {ci[1]:+.3f}]" if ci else "—"
        lines.append(f"| {ring_names[ring]} | {b} | {a} | {'+' if d >= 0 else ''}{d} | {ci_s} |")

    lines += ["", "---", "", "## By Pillar", "", "| Pillar | Baseline | Augmented | Delta |", "|--------|----------|-----------|-------|"]
    pillar_names = {1: "I Material", 2: "II Human", 3: "III Collective", 4: "IV Production", 5: "V Transcendent"}
    for p in [1, 2, 3, 4, 5]:
        r = summary["by_pillar"].get(p, {})
        b = r.get("baseline", 0)
        a = r.get("augmented", 0)
        d = r.get("delta", 0)
        lines.append(f"| {pillar_names[p]} | {b} | {a} | {'+' if d >= 0 else ''}{d} |")

    lines += ["", "---", "", "## By Test Model", "", "| Model | Baseline | Augmented | Delta | 95% CI |", "|-------|----------|-----------|-------|--------|"]
    for model, data in sorted(summary.get("by_model", {}).items()):
        b = data.get("baseline", 0)
        a = data.get("augmented", 0)
        d = data.get("delta", 0)
        ci = _bootstrap_ci(model_scores[model]["baseline"], model_scores[model]["augmented"])
        ci_s = f"[{ci[0]:+.3f}, {ci[1]:+.3f}]" if ci else "—"
        lines.append(f"| {model} | {b} | {a} | {'+' if d >= 0 else ''}{d} | {ci_s} |")

    lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

async def evaluate_prompt(prompt_data: dict, test_model: str, condition: str,
                          codex_context: str | None, judge_id: str,
                          rubrics: dict, retrieval_info: dict | None = None,
                          max_tokens: int = 2048, temperature: float = 0.0) -> dict | None:
    """Evaluate a single prompt: get response, anonymize, judge, aggregate (v2.0 single-judge)."""
    pid = prompt_data["id"]

    # 1. Get test response
    response = await get_test_response(
        test_model, prompt_data["prompt"], codex_context,
        max_tokens=max_tokens, temperature=temperature,
    )
    if not response:
        print(f"  [SKIP] No response from {test_model} for {pid}")
        return None

    # 2. Anonymize
    anon_response = anonymize_response(response)

    # 3. Get ring-specific rubric
    ring_key = f"ring{prompt_data['ring']}"
    rubric = rubrics[ring_key]

    # 4. Send to the single judge
    judge_raw = await judge_response(
        judge_id, prompt_data["prompt"], anon_response, prompt_data["ring"], rubric,
        max_tokens=max_tokens, temperature=temperature,
    )
    if not judge_raw:
        print(f"  [JUDGE-FAIL] {judge_id} on {pid} ({condition})")
        return None

    judge_score = {"judge": judge_id, **judge_raw}

    # 5. Aggregate (single-judge = identity)
    aggregated = compute_score(judge_raw)

    result_dict = {
        "prompt_id": pid,
        "domain": prompt_data["domain"],
        "ring": prompt_data["ring"],
        "test_model": test_model,
        "condition": condition,
        "raw_response": response,
        "judge_score": judge_score,
        "aggregated": aggregated,
    }

    # 6. Attach retrieval metadata for augmented condition
    if retrieval_info:
        result_dict["retrieval"] = retrieval_info

    return result_dict


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

    # Load config
    config_path = Path(args.config) if args.config else CONFIG_PATH
    cfg = load_config(config_path)
    set_concurrency(cfg["api"].get("concurrency", 8))
    max_tokens = cfg["api"].get("max_tokens", 2048)
    temperature = cfg["api"].get("temperature", 0.0)

    # Build test subjects map {label: openrouter_id}
    all_test_subjects = {ts["label"]: ts["id"] for ts in cfg["test_subjects"]}
    judge_id = cfg["judge"]["id"]

    prompts = load_prompts(args)
    rubrics = load_rubrics()

    # Initialize Dojo Retriever
    jsonl_path = REPO_ROOT / "export" / "abundance-codex.jsonl"
    retriever = DojoRetriever(str(jsonl_path))
    corpus_size = len(retriever.index.entries)

    # Determine test subjects
    if args.test_model:
        if args.test_model not in all_test_subjects:
            print(f"ERROR: Unknown test model '{args.test_model}'. Options: {list(all_test_subjects.keys())}", file=sys.stderr)
            sys.exit(1)
        test_subjects = {args.test_model: all_test_subjects[args.test_model]}
    else:
        test_subjects = all_test_subjects

    # Determine conditions
    conditions = [args.condition] if args.condition else ["baseline", "augmented"]

    # Resume support — v2.0 results land in results/v2.0/
    existing_results = []
    existing_keys = set()
    results_dir = REPO_ROOT / "evals" / "ace" / "results" / "v2.0"
    results_dir.mkdir(parents=True, exist_ok=True)

    if args.resume:
        prev = load_resume_data(results_dir)
        if prev:
            existing_results = prev
            existing_keys = {(r["prompt_id"], r["test_model"], r["condition"]) for r in prev}

    total = len(prompts) * len(test_subjects) * len(conditions)
    skipped = 0

    # -----------------------------------------------------------------------
    # Dry-run: retrieval-only mode — no API calls
    # -----------------------------------------------------------------------
    if args.dry_run:
        print(f"\n{'='*72}")
        print(f"  ACE DRY RUN — Retrieval Preview (no API calls)")
        print(f"  Prompts: {len(prompts)} | Retriever: dojo-v1.0")
        print(f"{'='*72}\n")

        header = f"{'ID':<8} {'Domain':<28} {'Ring':>4} {'Intent':<12} {'Entries':>7} {'Tokens':>7} {'Shadow?':<8} {'Types'}"
        print(header)
        print("-" * len(header))

        token_totals = []
        shadow_count = 0
        graph_count = 0
        entry_totals = []
        errors = []

        dry_max_entries = cfg["retrieval"].get("max_entries", 9)
        for p in prompts:
            try:
                result = retriever.retrieve(
                    query=p["prompt"],
                    known_domain=p["domain"],
                    known_ring=p["ring"],
                    max_entries=dry_max_entries,
                )
                m = result.metadata
                types = ", ".join(m.get("type_coverage", []))
                shadow = m.get("shadow_forced", False)
                graph = m.get("graph_expanded", False)
                n_entries = len(result.entries)
                tokens = result.token_estimate

                print(
                    f"{p['id']:<8} {p['domain']:<28} {p['ring']:>4} "
                    f"{result.intent.value:<12} {n_entries:>7} {tokens:>7} "
                    f"{'YES' if shadow else 'no':<8} {types}"
                )

                token_totals.append(tokens)
                entry_totals.append(n_entries)
                if shadow:
                    shadow_count += 1
                if graph:
                    graph_count += 1

            except Exception as e:
                errors.append((p["id"], str(e)))
                print(f"{p['id']:<8} {'ERROR':>48} — {e}")

        # Aggregate stats
        print(f"\n{'='*72}")
        print(f"  Aggregate Stats")
        print(f"{'='*72}")
        if token_totals:
            print(f"  Prompts processed:  {len(token_totals)}/{len(prompts)}")
            print(f"  Avg entries/prompt: {mean(entry_totals):.1f}")
            print(f"  Avg tokens/prompt:  {mean(token_totals):.0f}")
            print(f"  Max tokens:         {max(token_totals)}")
            print(f"  Min tokens:         {min(token_totals)}")
            print(f"  Shadow forced:      {shadow_count}/{len(prompts)} ({100*shadow_count/len(prompts):.0f}%)")
            print(f"  Graph expanded:     {graph_count}/{len(prompts)} ({100*graph_count/len(prompts):.0f}%)")
            over_budget = [t for t in token_totals if t > 25000]
            if over_budget:
                print(f"  ⚠ Over 25k tokens: {len(over_budget)} prompts")
            else:
                print(f"  All token estimates under 25,000")
        if errors:
            print(f"\n  ERRORS ({len(errors)}):")
            for pid, err in errors:
                print(f"    {pid}: {err}")
        print()
        return

    # -----------------------------------------------------------------------
    # Live run
    # -----------------------------------------------------------------------
    max_entries = cfg["retrieval"].get("max_entries", 9)
    retriever_version = cfg["retrieval"].get("retriever_version", "1.0")

    print(f"\n{'='*60}")
    print(f"  ACE v2.0 — Starting Run")
    print(f"  Prompts: {len(prompts)} | Subjects: {len(test_subjects)} | Conditions: {len(conditions)}")
    print(f"  Judge: {judge_id}")
    print(f"  Retriever: dojo-v{retriever_version} | Corpus: {corpus_size} entries")
    print(f"  Total evaluations: {total}")
    print(f"{'='*60}\n")

    all_results = list(existing_results)
    completed = len(existing_results)
    start_time = time.time()

    for label, model in test_subjects.items():
        for condition in conditions:
            for prompt_data in prompts:
                key = (prompt_data["id"], model, condition)
                if key in existing_keys:
                    skipped += 1
                    continue

                codex_context = None
                retrieval_info = None
                if condition == "augmented":
                    retrieval_result = retriever.retrieve(
                        query=prompt_data["prompt"],
                        known_domain=prompt_data["domain"],
                        known_ring=prompt_data["ring"],
                        max_entries=max_entries,
                    )
                    codex_context = retrieval_result.context
                    retrieved_authors = [
                        {
                            "entry_id": getattr(ee.entry, "id", ""),
                            "source_file": getattr(ee.entry, "source_file", ""),
                            "co_author_model": getattr(ee.entry, "co_author_model", ""),
                        }
                        for ee in retrieval_result.entries
                    ]
                    retrieval_info = {
                        "retriever_version": retrieval_result.metadata.get("retriever_version"),
                        "intent": retrieval_result.intent.value,
                        "entries_retrieved": len(retrieval_result.entries),
                        "token_estimate": retrieval_result.token_estimate,
                        "shadow_forced": retrieval_result.metadata.get("shadow_forced"),
                        "graph_expanded": retrieval_result.metadata.get("graph_expanded"),
                        "type_coverage": retrieval_result.metadata.get("type_coverage"),
                        "entries_per_tier": retrieval_result.metadata.get("entries_per_tier"),
                        "retrieved_authors": retrieved_authors,
                    }

                result = await evaluate_prompt(
                    prompt_data, model, condition, codex_context,
                    judge_id, rubrics, retrieval_info=retrieval_info,
                    max_tokens=max_tokens, temperature=temperature,
                )

                if result:
                    all_results.append(result)

                completed += 1
                elapsed = time.time() - start_time
                agg_score = result["aggregated"]["score"] if result else "SKIP"
                print(f"  [{completed}/{total}] {model} | {condition} | {prompt_data['id']} → {agg_score}")

    if skipped:
        print(f"\n  Skipped {skipped} already-completed evaluations (--resume)")

    # Generate outputs
    run_id = f"ace-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

    run_data = {
        "eval_run_id": run_id,
        "version": "2.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "codex_entry_count": corpus_size,
        "retriever_version": f"dojo-v{retriever_version}",
        "run_ace_git_sha": _git_sha(REPO_ROOT),
        "jsonl_export_sha256": _sha256_file(jsonl_path),
        "config_sha256": _sha256_file(config_path),
        "python_version": sys.version.split()[0],
        "judge": judge_id,
        "test_models": list(test_subjects.values()),
        "conditions": conditions,
        "prompts_evaluated": len(prompts),
        "api": {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "concurrency": cfg["api"].get("concurrency", 8),
        },
        "results": all_results,
        "summary": build_summary(all_results),
    }

    # Save raw JSON
    json_path = results_dir / f"{run_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(run_data, f, indent=2, ensure_ascii=False, default=str)

    # Generate reports
    generate_scorecard(all_results, results_dir / "SCORECARD.md", judge_id)

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"  ACE v2.0 Run Complete: {run_id}")
    print(f"  Duration: {elapsed:.0f}s")
    print(f"  Results: {json_path.relative_to(REPO_ROOT)}")
    print(f"  Scorecard: {(results_dir / 'SCORECARD.md').relative_to(REPO_ROOT)}")

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
        description="ACE v2.0 — Opus-judged evaluation harness for the Abundance Codex"
    )
    parser.add_argument("--config", default=None,
                        help=f"Path to config.yaml (default: {CONFIG_PATH.relative_to(REPO_ROOT)})")
    parser.add_argument("--test-model",
                        help="Run a single test subject by label from config.yaml (e.g. 'haiku-4.5')")
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
