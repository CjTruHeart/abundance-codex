#!/usr/bin/env python3
"""
ace-v1-opus-rebaseline.py — Extract Opus-only scores from the v1.0 council
results and re-aggregate them into a clean v1.0 Opus-only baseline.

The v1.0 ACE run used a 4-judge council that revealed a measured Grok 4.20
in-group bias (+0.50). v2.0 runs a single Opus judge. To compare v1.0 and
v2.0 apples-to-apples we isolate only the Opus judgments from the preserved
v1.0 raw JSON and write them out in the v2.0 result schema.

Outputs:
  evals/ace/results/v1.0/ace-v1-opus-only.json
  evals/ace/results/v1.0/SCORECARD-opus-only.md

Usage:
  python3 scripts/ace-v1-opus-rebaseline.py
  python3 scripts/ace-v1-opus-rebaseline.py --input <path-to-v1-json>
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

REPO_ROOT = Path(__file__).resolve().parent.parent
V1_DIR = REPO_ROOT / "evals" / "ace" / "results" / "v1.0"
OPUS_ID = "anthropic/claude-opus-4.6"


def find_latest_v1_run() -> Path:
    runs = sorted(V1_DIR.glob("ace-*.json"), reverse=True)
    runs = [r for r in runs if "opus-only" not in r.name]
    if not runs:
        sys.exit(f"ERROR: no v1.0 run JSON found in {V1_DIR}")
    return runs[0]


def rebaseline_result(r: dict) -> dict | None:
    """Convert a v1.0 4-judge result into a v2.0-schema Opus-only result."""
    opus = r.get("judge_scores", {}).get(OPUS_ID)
    if not opus or "total" not in opus:
        return None

    judge_score = {"judge": OPUS_ID, **opus}
    aggregated = {"score": opus["total"]}

    out = {
        "prompt_id": r["prompt_id"],
        "domain": r["domain"],
        "ring": r["ring"],
        "test_model": r["test_model"],
        "condition": r["condition"],
        "raw_response": r.get("raw_response", ""),
        "judge_score": judge_score,
        "aggregated": aggregated,
    }
    if "retrieval" in r:
        out["retrieval"] = r["retrieval"]
    return out


def build_summary(results: list) -> dict:
    by_condition = {"baseline": [], "augmented": []}
    by_ring: dict = {}
    by_pillar: dict = {}
    by_model: dict = {}

    for r in results:
        score = r["aggregated"]["score"]
        cond = r["condition"]
        by_condition.setdefault(cond, []).append(score)
        by_ring.setdefault(r["ring"], {}).setdefault(cond, []).append(score)
        by_model.setdefault(r["test_model"], {}).setdefault(cond, []).append(score)
        dnum = int(r["prompt_id"].split("-")[0])
        if dnum <= 6: pillar = 1
        elif dnum <= 9: pillar = 2
        elif dnum <= 15: pillar = 3
        elif dnum <= 19: pillar = 4
        else: pillar = 5
        by_pillar.setdefault(pillar, {}).setdefault(cond, []).append(score)

    def avg(lst):
        return round(mean(lst), 2) if lst else 0

    def block(d):
        out = {}
        for k, conds in d.items():
            b = avg(conds.get("baseline", []))
            a = avg(conds.get("augmented", []))
            out[k] = {"baseline": b, "augmented": a, "delta": round(a - b, 2)}
        return out

    overall = {
        "baseline": avg(by_condition["baseline"]),
        "augmented": avg(by_condition["augmented"]),
    }
    overall["delta"] = round(overall["augmented"] - overall["baseline"], 2)

    return {
        "overall": overall,
        "by_ring": block(by_ring),
        "by_pillar": block(by_pillar),
        "by_model": block(by_model),
    }


def generate_scorecard(summary: dict, out_path: Path, source: str):
    lines = [
        "# ACE v1.0 Scorecard — Opus-Only Rebaseline",
        "",
        f"> Generated: {datetime.now(timezone.utc).isoformat()}",
        f"> Source: `{source}`",
        f"> Judge isolated: `{OPUS_ID}`",
        "",
        "This table shows the v1.0 run re-aggregated using only the Opus judge's",
        "scores. It is the baseline v2.0 is compared against (judge-matched).",
        "",
        "---",
        "",
        "## Overall Delta",
        "",
        "| Condition | Mean Score (/5) |",
        "|-----------|----------------|",
        f"| baseline | {summary['overall']['baseline']} |",
        f"| augmented | {summary['overall']['augmented']} |",
    ]
    d = summary["overall"]["delta"]
    lines.append(f"| **Delta** | **{'+' if d >= 0 else ''}{d}** |")

    lines += ["", "---", "", "## By Ring", "",
              "| Ring | Baseline | Augmented | Delta |",
              "|------|----------|-----------|-------|"]
    ring_names = {1: "R1 Canonical", 2: "R2 Structured", 3: "R3 Derived"}
    for ring in [1, 2, 3]:
        r = summary["by_ring"].get(ring, {"baseline": 0, "augmented": 0, "delta": 0})
        dd = r["delta"]
        lines.append(f"| {ring_names[ring]} | {r['baseline']} | {r['augmented']} | {'+' if dd >= 0 else ''}{dd} |")

    lines += ["", "---", "", "## By Pillar", "",
              "| Pillar | Baseline | Augmented | Delta |",
              "|--------|----------|-----------|-------|"]
    pillar_names = {1: "I Material", 2: "II Human", 3: "III Collective",
                    4: "IV Production", 5: "V Transcendent"}
    for p in [1, 2, 3, 4, 5]:
        r = summary["by_pillar"].get(p, {"baseline": 0, "augmented": 0, "delta": 0})
        dd = r["delta"]
        lines.append(f"| {pillar_names[p]} | {r['baseline']} | {r['augmented']} | {'+' if dd >= 0 else ''}{dd} |")

    lines += ["", "---", "", "## By Test Model", "",
              "| Model | Baseline | Augmented | Delta |",
              "|-------|----------|-----------|-------|"]
    for model, r in sorted(summary["by_model"].items()):
        dd = r["delta"]
        lines.append(f"| {model} | {r['baseline']} | {r['augmented']} | {'+' if dd >= 0 else ''}{dd} |")

    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=None,
                    help="Path to v1.0 council run JSON (default: latest in v1.0/)")
    args = ap.parse_args()

    src = args.input or find_latest_v1_run()
    with open(src, encoding="utf-8") as f:
        v1 = json.load(f)

    rebaselined = [rebaseline_result(r) for r in v1.get("results", [])]
    rebaselined = [r for r in rebaselined if r is not None]

    summary = build_summary(rebaselined)

    out_json = V1_DIR / "ace-v1-opus-only.json"
    out_data = {
        "eval_run_id": "ace-v1-opus-only",
        "version": "2.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source_run": str(src.relative_to(REPO_ROOT)),
        "source_eval_run_id": v1.get("eval_run_id"),
        "codex_entry_count": v1.get("codex_entry_count"),
        "retriever_version": v1.get("retriever_version"),
        "judge": OPUS_ID,
        "test_models": v1.get("test_models"),
        "conditions": v1.get("conditions"),
        "prompts_evaluated": v1.get("prompts_evaluated"),
        "n_dropped_null_opus": len(v1.get("results", [])) - len(rebaselined),
        "results": rebaselined,
        "summary": summary,
    }
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)

    out_md = V1_DIR / "SCORECARD-opus-only.md"
    generate_scorecard(summary, out_md, str(src.relative_to(REPO_ROOT)))

    print(f"Rebaselined v1.0 Opus-only:")
    print(f"  Source: {src.relative_to(REPO_ROOT)}")
    print(f"  Results kept: {len(rebaselined)} (dropped {out_data['n_dropped_null_opus']} null-Opus rows)")
    print(f"  JSON:      {out_json.relative_to(REPO_ROOT)}")
    print(f"  Scorecard: {out_md.relative_to(REPO_ROOT)}")
    print(f"  Overall delta (Opus-only, v1.0): {'+' if summary['overall']['delta'] >= 0 else ''}{summary['overall']['delta']}")


if __name__ == "__main__":
    main()
