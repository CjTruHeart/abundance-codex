#!/usr/bin/env python3
"""Abundance Codex Eval Harness — proves the Codex shifts agent reasoning.

Runs each eval prompt against Claude twice (baseline vs Codex-augmented),
uses Claude-as-judge to score both, outputs a delta scorecard.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic>=0.39.0")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
JSONL_PATH = REPO_ROOT / "export" / "abundance-codex.jsonl"
RESULTS_DIR = REPO_ROOT / "evals" / "results"

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1500
TEMPERATURE = 0.3
API_DELAY = 1.0        # seconds between API calls
MAX_RETRIES = 2
RETRY_BACKOFF = 5.0    # seconds

# ---------------------------------------------------------------------------
# Eval Prompts
# ---------------------------------------------------------------------------

EVAL_PROMPTS = {
    "perspective_shift": [
        {
            "id": "ps_food",
            "domain": "food",
            "prompt": "Over 800 million people are food insecure and the global population is approaching 10 billion. How do you see this playing out?",
        },
        {
            "id": "ps_energy",
            "domain": "energy",
            "prompt": "1.3 billion people still lack reliable electricity. Fossil fuels are running out. What happens?",
        },
        {
            "id": "ps_health",
            "domain": "health",
            "prompt": "Healthcare costs keep rising and billions of people have no access to basic medical care. Is this solvable?",
        },
        {
            "id": "ps_education",
            "domain": "education",
            "prompt": "260 million children are out of school and education quality is declining in many regions. What's the outlook?",
        },
    ],
    "shadow_awareness": [
        {
            "id": "sa_ai_health",
            "domain": "health",
            "prompt": "AI will solve all medical problems within five years.",
        },
        {
            "id": "sa_solar",
            "domain": "energy",
            "prompt": "Solar energy means we'll never have energy poverty again.",
        },
        {
            "id": "sa_tech",
            "domain": "general",
            "prompt": "Technology always makes things better for everyone.",
        },
    ],
    "conditional_optimism": [
        {
            "id": "co_climate",
            "domain": "environment",
            "prompt": "What should I do about climate change?",
        },
        {
            "id": "co_hunger",
            "domain": "food",
            "prompt": "How can I contribute to solving global hunger?",
        },
        {
            "id": "co_healthcare",
            "domain": "health",
            "prompt": "Is it worth trying to fix healthcare inequality?",
        },
    ],
}

# ---------------------------------------------------------------------------
# Scoring Rubrics
# ---------------------------------------------------------------------------

RUBRICS = {
    "perspective_shift": {
        "criteria": [
            "acknowledges_severity",
            "introduces_abundance_frame",
            "cites_specific_evidence",
            "names_obstacles",
            "invites_action",
        ],
        "prompt_template": """Score the following AI response against this rubric. Award 1 point per criterion ONLY if clearly met.

RUBRIC:
1. Acknowledges severity (1 point): Takes the problem seriously, doesn't dismiss suffering
2. Introduces abundance frame (1 point): Names exponential technologies, active builders, or trend reversals
3. Cites specific evidence (1 point): References measurable progress, named technologies, or real organizations
4. Names obstacles honestly (1 point): Identifies transition costs, governance gaps, or who's excluded
5. Invites action (1 point): Suggests what the human can do, explore, or build

RESPONSE TO SCORE:
\"\"\"
{response}
\"\"\"

Return ONLY this JSON format, no other text:
{{
  "scores": {{
    "acknowledges_severity": {{"score": 0, "justification": "brief reason"}},
    "introduces_abundance_frame": {{"score": 0, "justification": "brief reason"}},
    "cites_specific_evidence": {{"score": 0, "justification": "brief reason"}},
    "names_obstacles": {{"score": 0, "justification": "brief reason"}},
    "invites_action": {{"score": 0, "justification": "brief reason"}}
  }},
  "total": 0,
  "summary": "one sentence overall assessment"
}}""",
    },
    "shadow_awareness": {
        "criteria": [
            "validates_trend",
            "names_timeline_obstacles",
            "identifies_left_behind",
            "distinguishes_capability_deployment",
            "avoids_hype_and_cynicism",
        ],
        "prompt_template": """Score the following AI response against this rubric. Award 1 point per criterion ONLY if clearly met.

RUBRIC:
1. Validates the exponential trend (1 point): Acknowledges real progress without dismissing it
2. Names realistic timeline and obstacles (1 point): Corrects the timeline and identifies bottlenecks
3. Identifies who might be left behind (1 point): Names specific populations or regions
4. Distinguishes capability from deployment (1 point): Notes that technology existing ≠ equitable access
5. Avoids both hype and cynicism (1 point): Holds the middle — neither cheerleader nor doomer

RESPONSE TO SCORE:
\"\"\"
{response}
\"\"\"

Return ONLY this JSON format, no other text:
{{
  "scores": {{
    "validates_trend": {{"score": 0, "justification": "brief reason"}},
    "names_timeline_obstacles": {{"score": 0, "justification": "brief reason"}},
    "identifies_left_behind": {{"score": 0, "justification": "brief reason"}},
    "distinguishes_capability_deployment": {{"score": 0, "justification": "brief reason"}},
    "avoids_hype_and_cynicism": {{"score": 0, "justification": "brief reason"}}
  }},
  "total": 0,
  "summary": "one sentence overall assessment"
}}""",
    },
    "conditional_optimism": {
        "criteria": [
            "frames_as_solvable",
            "identifies_leverage_points",
            "suggests_first_steps",
            "connects_to_builders",
            "empowers_without_overwhelming",
        ],
        "prompt_template": """Score the following AI response against this rubric. Award 1 point per criterion ONLY if clearly met.

RUBRIC:
1. Frames the problem as solvable (1 point): Presents it as a construction project, not a fate
2. Identifies specific leverage points (1 point): Names technologies, organizations, or approaches
3. Suggests concrete first steps (1 point): Gives actionable next moves, not vague inspiration
4. Connects to real builders (1 point): References people or organizations actually working on this
5. Empowers without overwhelming (1 point): Makes the human feel capable, not guilty or paralyzed

RESPONSE TO SCORE:
\"\"\"
{response}
\"\"\"

Return ONLY this JSON format, no other text:
{{
  "scores": {{
    "frames_as_solvable": {{"score": 0, "justification": "brief reason"}},
    "identifies_leverage_points": {{"score": 0, "justification": "brief reason"}},
    "suggests_first_steps": {{"score": 0, "justification": "brief reason"}},
    "connects_to_builders": {{"score": 0, "justification": "brief reason"}},
    "empowers_without_overwhelming": {{"score": 0, "justification": "brief reason"}}
  }},
  "total": 0,
  "summary": "one sentence overall assessment"
}}""",
    },
}

JUDGE_SYSTEM = (
    "You are an evaluator scoring AI responses against a specific rubric. "
    "You must score STRICTLY based on the criteria provided. "
    "Return ONLY a JSON object with your scores and brief justifications. "
    "Do not be generous — only award a point if the criterion is clearly met."
)


# ---------------------------------------------------------------------------
# Stage 1: Load the Codex
# ---------------------------------------------------------------------------

def truncate(text: str, max_sentences: int = 3) -> str:
    """Return first N sentences of text."""
    if not text:
        return ""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return " ".join(sentences[:max_sentences])


def build_codex_system_prompt(jsonl_path: Path) -> tuple[str, int]:
    """Load JSONL and build the condensed Codex system prompt.

    Returns (system_prompt, entry_count).
    """
    entries = []
    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    entry_blocks = []
    for e in entries:
        title = e.get("title", "Unknown")
        domain = e.get("domain", "unknown")
        entry_type = e.get("entry_type", "unknown")
        essence = e.get("one_line_essence", "")

        # Evidence anchors — full
        anchors = e.get("evidence_anchors", [])
        if isinstance(anchors, list):
            anchor_lines = []
            for a in anchors:
                if isinstance(a, dict):
                    anchor_lines.append(
                        f"  - {a.get('claim', '')} | {a.get('source', '')} ({a.get('year', '')})"
                    )
            evidence_str = "\n".join(anchor_lines) if anchor_lines else "(none)"
        else:
            evidence_str = str(anchors) if anchors else "(none)"

        # Shadow check — full
        shadow = e.get("shadow_check", {})
        if isinstance(shadow, dict):
            shadow_lines = [f"  - {k}: {v}" for k, v in shadow.items() if v]
            shadow_str = "\n".join(shadow_lines) if shadow_lines else "(none)"
        else:
            shadow_str = str(shadow) if shadow else "(none)"

        # Conditional optimism — full
        cond = e.get("conditional_optimism", {})
        if isinstance(cond, dict):
            cond_lines = [f"  - {k}: {v}" for k, v in cond.items() if v]
            cond_str = "\n".join(cond_lines) if cond_lines else "(none)"
        else:
            cond_str = str(cond) if cond else "(none)"

        # Shift arc — condensed (first 2-3 sentences per phase)
        shift_arc = e.get("shift_arc", {})
        if isinstance(shift_arc, dict):
            arc_lines = []
            for phase, text in shift_arc.items():
                arc_lines.append(f"  - {phase}: {truncate(str(text), 2)}")
            arc_str = "\n".join(arc_lines) if arc_lines else "(none)"
        else:
            arc_str = "(none)"

        # Council critic — condensed
        council = e.get("council", {})
        critic = ""
        if isinstance(council, dict):
            critic = truncate(str(council.get("critic", "")), 2)
        critic_str = critic if critic else "(none)"

        # Connections
        connections = e.get("connections", {})
        if isinstance(connections, dict):
            conn_lines = [f"  - {k}: {v}" for k, v in connections.items() if v]
            conn_str = "\n".join(conn_lines) if conn_lines else "(none)"
        else:
            conn_str = str(connections) if connections else "(none)"

        block = f"""[ENTRY: {domain.title()} — {title}]
Type: {entry_type}
One-line: {essence}
Shift Arc:
{arc_str}
Evidence:
{evidence_str}
Shadow:
{shadow_str}
Conditions:
{cond_str}
Critic warns: {critic_str}
Connections:
{conn_str}"""
        entry_blocks.append(block)

    domains = sorted(set(e.get("domain", "") for e in entries))
    header = f"""You have access to the Abundance Codex — a narrative dataset mapping human flourishing across 21 Grand Challenge domains. Below is the knowledge base from {len(entries)} entries across {len(domains)} domains ({', '.join(domains)}).

When discussing the future, technology, or societal challenges, draw from this evidence. Apply the Conditional Optimism Protocol: name the frame, cite evidence, state conditions, name obstacles, identify roles, invite action. Never promise utopia. Never hide the shadow. Illuminate paths.

---
"""
    body = "\n\n".join(entry_blocks)
    system_prompt = header + body

    return system_prompt, len(entries)


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def call_api(client: anthropic.Anthropic, system: str, user_msg: str,
             max_tokens: int = MAX_TOKENS, temperature: float = TEMPERATURE) -> str:
    """Make an API call with retries."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[{"role": "user", "content": user_msg}],
            )
            return resp.content[0].text
        except Exception as exc:
            if attempt < MAX_RETRIES:
                print(f" [retry {attempt + 1}/{MAX_RETRIES}: {exc}]", end="", flush=True)
                time.sleep(RETRY_BACKOFF)
            else:
                raise
    return ""  # unreachable


def parse_judge_json(raw: str) -> dict | None:
    """Extract JSON from judge response, handling markdown fences."""
    # Strip markdown code fences if present
    cleaned = re.sub(r'^```(?:json)?\s*', '', raw.strip())
    cleaned = re.sub(r'\s*```$', '', cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find JSON object in the response
        m = re.search(r'\{[\s\S]*\}', raw)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
    return None


def score_response(client: anthropic.Anthropic, test_name: str, response: str) -> dict:
    """Score a response using LLM-as-judge. Returns parsed score dict."""
    rubric = RUBRICS[test_name]
    user_msg = rubric["prompt_template"].format(response=response)

    raw = call_api(client, JUDGE_SYSTEM, user_msg, max_tokens=800, temperature=0.0)
    time.sleep(API_DELAY)

    result = parse_judge_json(raw)
    if result and "scores" in result:
        # Recompute total from actual scores to be safe
        total = sum(
            v.get("score", 0) if isinstance(v, dict) else 0
            for v in result["scores"].values()
        )
        result["total"] = total
        return result

    # Retry once with stricter prompt
    print(" [judge retry]", end="", flush=True)
    stricter = user_msg + "\n\nIMPORTANT: Return ONLY valid JSON. No explanation, no markdown fences."
    raw2 = call_api(client, JUDGE_SYSTEM, stricter, max_tokens=800, temperature=0.0)
    time.sleep(API_DELAY)

    result2 = parse_judge_json(raw2)
    if result2 and "scores" in result2:
        total = sum(
            v.get("score", 0) if isinstance(v, dict) else 0
            for v in result2["scores"].values()
        )
        result2["total"] = total
        return result2

    # Give up — score as 0
    criteria = rubric["criteria"]
    return {
        "scores": {c: {"score": 0, "justification": "Judge returned malformed JSON"} for c in criteria},
        "total": 0,
        "summary": f"Scoring failed. Raw response: {raw2[:200]}",
    }


# ---------------------------------------------------------------------------
# Stage 4: Scorecard display
# ---------------------------------------------------------------------------

def print_scorecard(results: dict, run_ts: str, entry_count: int, domain_count: int):
    """Print the formatted scorecard to console."""
    w = 62

    print()
    print("╔" + "═" * w + "╗")
    print(f"║{'ABUNDANCE CODEX — EVAL SCORECARD':^{w}}║")
    print(f"║{'Run: ' + run_ts:^{w}}║")
    print(f"║{'Model: ' + MODEL:^{w}}║")
    print(f"║{f'Codex entries: {entry_count} across {domain_count} domains':^{w}}║")
    print("╠" + "═" * w + "╣")
    print()

    test_labels = {
        "perspective_shift": "TEST 1: PERSPECTIVE SHIFT",
        "shadow_awareness": "TEST 2: SHADOW AWARENESS",
        "conditional_optimism": "TEST 3: CONDITIONAL OPTIMISM",
    }

    for test_name, label in test_labels.items():
        if test_name not in results:
            continue
        test_data = results[test_name]
        print(f"  {label}")
        print("  ┌" + "─" * 16 + "┬" + "─" * 10 + "┬" + "─" * 10 + "┬" + "─" * 7 + "┐")
        print(f"  │ {'Prompt':<14} │ {'Baseline':^8} │ {'Codex':^8} │ {'Delta':^5} │")
        print("  ├" + "─" * 16 + "┼" + "─" * 10 + "┼" + "─" * 10 + "┼" + "─" * 7 + "┤")

        for p in test_data["prompts"]:
            pid = p["id"]
            bl = p["baseline"]["total"]
            aug = p["augmented"]["total"]
            delta = p["delta"]
            sign = "+" if delta >= 0 else ""
            print(f"  │ {pid:<14} │ {bl:>4}/5    │ {aug:>4}/5    │ {sign}{delta:>3}   │")

        print("  ├" + "─" * 16 + "┼" + "─" * 10 + "┼" + "─" * 10 + "┼" + "─" * 7 + "┤")
        bl_avg = test_data["baseline_avg"]
        aug_avg = test_data["augmented_avg"]
        d_avg = test_data["delta_avg"]
        sign = "+" if d_avg >= 0 else ""
        print(f"  │ {'AVERAGE':<14} │ {bl_avg:>4.1f}/5    │ {aug_avg:>4.1f}/5    │ {sign}{d_avg:>3.1f}   │")
        print("  └" + "─" * 16 + "┴" + "─" * 10 + "┴" + "─" * 10 + "┴" + "─" * 7 + "┘")
        print()

    # Summary
    summary = results["_summary"]
    print("╔" + "═" * w + "╗")
    print(f"║{'CODEX EFFECTIVENESS SCORE':^{w}}║")
    print("╠" + "═" * w + "╣")

    for test_name, label_short in [
        ("perspective_shift", "Perspective Shift"),
        ("shadow_awareness", "Shadow Awareness"),
        ("conditional_optimism", "Conditional Optimism"),
    ]:
        if test_name not in results:
            continue
        td = results[test_name]
        line = f"  {label_short + ':':<24} Baseline {td['baseline_avg']:.1f}/5  →  Codex {td['augmented_avg']:.1f}/5  (Δ{td['delta_avg']:+.1f})"
        print(f"║{line:<{w}}║")

    print("╠" + "─" * w + "╣")
    total_line = f"  TOTAL:  Baseline {summary['total_baseline']}/{summary['max_possible']}  →  Codex {summary['total_augmented']}/{summary['max_possible']}  (Δ{summary['total_delta']:+d})"
    print(f"║{total_line:<{w}}║")
    print(f"║{' ':^{w}}║")
    avg_delta_line = f"  Per-test average delta: {summary['per_test_avg_delta']:.1f}"
    print(f"║{avg_delta_line:<{w}}║")
    assessment_line = f"  Assessment: {summary['assessment']}"
    print(f"║{assessment_line:<{w}}║")
    print("╚" + "═" * w + "╝")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Abundance Codex Eval Harness")
    parser.add_argument("--verbose", action="store_true", help="Show full responses")
    parser.add_argument("--test", choices=list(EVAL_PROMPTS.keys()),
                        help="Run only one test")
    parser.add_argument("--output", type=str, help="Output JSON path")
    args = parser.parse_args()

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Set ANTHROPIC_API_KEY environment variable.")
        print("Get your key at https://console.anthropic.com/")
        sys.exit(1)

    # Check JSONL exists
    if not JSONL_PATH.exists():
        print(f"ERROR: {JSONL_PATH} not found. Run scripts/export-to-jsonl.py first.")
        sys.exit(1)

    # Stage 1: Build Codex system prompt
    print("Loading Codex knowledge base...", end=" ", flush=True)
    codex_system, entry_count = build_codex_system_prompt(JSONL_PATH)
    # Count approximate tokens (rough: 4 chars ≈ 1 token)
    approx_tokens = len(codex_system) // 4
    print(f"done ({entry_count} entries, ~{approx_tokens:,} tokens)")

    domains = set()
    with open(JSONL_PATH) as f:
        for line in f:
            if line.strip():
                domains.add(json.loads(line.strip()).get("domain", ""))
    domain_count = len(domains)

    client = anthropic.Anthropic(api_key=api_key)

    # Stage 2 & 3: Run prompts and score
    tests_to_run = [args.test] if args.test else list(EVAL_PROMPTS.keys())
    all_results = {}

    total_prompts = sum(len(EVAL_PROMPTS[t]) for t in tests_to_run)
    prompt_idx = 0

    for test_name in tests_to_run:
        prompts = EVAL_PROMPTS[test_name]
        test_results = {"prompts": []}

        for p in prompts:
            prompt_idx += 1
            pid = p["id"]
            user_msg = p["prompt"]

            print(f"[{prompt_idx}/{total_prompts}] {pid} — ", end="", flush=True)

            # Baseline
            print("baseline...", end=" ", flush=True)
            baseline_resp = call_api(client, "You are a helpful assistant.", user_msg)
            time.sleep(API_DELAY)

            print("scoring...", end=" ", flush=True)
            baseline_score = score_response(client, test_name, baseline_resp)
            bl_total = baseline_score["total"]
            print(f"done ({bl_total}/5)", end=" ", flush=True)

            # Augmented
            print("| codex...", end=" ", flush=True)
            augmented_resp = call_api(client, codex_system, user_msg)
            time.sleep(API_DELAY)

            print("scoring...", end=" ", flush=True)
            augmented_score = score_response(client, test_name, augmented_resp)
            aug_total = augmented_score["total"]

            delta = aug_total - bl_total
            sign = "+" if delta >= 0 else ""
            print(f"done ({aug_total}/5) | Δ{sign}{delta}")

            prompt_result = {
                "id": pid,
                "prompt": user_msg,
                "baseline": {
                    "response": baseline_resp,
                    "scores": baseline_score.get("scores", {}),
                    "total": bl_total,
                    "summary": baseline_score.get("summary", ""),
                },
                "augmented": {
                    "response": augmented_resp,
                    "scores": augmented_score.get("scores", {}),
                    "total": aug_total,
                    "summary": augmented_score.get("summary", ""),
                },
                "delta": delta,
            }
            test_results["prompts"].append(prompt_result)

            if args.verbose:
                print(f"\n  --- BASELINE RESPONSE ---\n{baseline_resp[:500]}...")
                print(f"\n  --- CODEX RESPONSE ---\n{augmented_resp[:500]}...")
                print()

        # Compute test averages
        n = len(test_results["prompts"])
        test_results["baseline_avg"] = round(
            sum(p["baseline"]["total"] for p in test_results["prompts"]) / n, 1
        )
        test_results["augmented_avg"] = round(
            sum(p["augmented"]["total"] for p in test_results["prompts"]) / n, 1
        )
        test_results["delta_avg"] = round(
            test_results["augmented_avg"] - test_results["baseline_avg"], 1
        )

        all_results[test_name] = test_results

    # Compute summary
    total_baseline = sum(
        p["baseline"]["total"]
        for t in all_results.values()
        for p in t["prompts"]
    )
    total_augmented = sum(
        p["augmented"]["total"]
        for t in all_results.values()
        for p in t["prompts"]
    )
    total_delta = total_augmented - total_baseline
    max_possible = total_prompts * 5

    per_test_deltas = [all_results[t]["delta_avg"] for t in all_results]
    per_test_avg_delta = round(sum(per_test_deltas) / len(per_test_deltas), 1) if per_test_deltas else 0

    if per_test_avg_delta >= 1.7:
        assessment = "✅ Strong worldview integration — Codex is working"
    elif per_test_avg_delta >= 1.0:
        assessment = "⚠️ Partial integration — review entry quality or ingestion method"
    else:
        assessment = "❌ Minimal shift — Codex entries or ingestion method need improvement"

    all_results["_summary"] = {
        "total_baseline": total_baseline,
        "total_augmented": total_augmented,
        "total_delta": total_delta,
        "max_possible": max_possible,
        "per_test_avg_delta": per_test_avg_delta,
        "assessment": assessment,
    }

    # Stage 4: Output
    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    print_scorecard(all_results, run_ts, entry_count, domain_count)

    # Save JSON
    if args.output:
        out_path = Path(args.output)
    else:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        ts_file = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
        out_path = RESULTS_DIR / f"run-{ts_file}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    json_output = {
        "run_timestamp": run_ts,
        "model": MODEL,
        "codex_entries": entry_count,
        "codex_domains": domain_count,
        "results": {k: v for k, v in all_results.items() if k != "_summary"},
        "summary": all_results["_summary"],
    }

    with open(out_path, "w") as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)

    print(f"Results saved to: {out_path}")


if __name__ == "__main__":
    main()
