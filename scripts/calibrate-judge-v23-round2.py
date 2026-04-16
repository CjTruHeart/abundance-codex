#!/usr/bin/env python3
"""
ACE v2.3 Spec A — Round 2 judge calibration (subset).

Runs only:
  - All 5 invented-publication controls
  - First 3 regression spot-checks (extracted the same way as round 1,
    then sliced to the first 3)

Reuses calibrate-judge-v23.py helpers; writes to
evals/ace/calibration/results-v2.3-dry-run-round2.json
(does not overwrite round 1).
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Load the round-1 runner module so we reuse its helpers verbatim.
_spec = importlib.util.spec_from_file_location(
    "calibrate_v23", str(REPO_ROOT / "scripts" / "calibrate-judge-v23.py")
)
cal = importlib.util.module_from_spec(_spec)
sys.modules["calibrate_v23"] = cal
_spec.loader.exec_module(cal)

OUTPUT_PATH = REPO_ROOT / "evals" / "ace" / "calibration" / "results-v2.3-dry-run-round2.json"


async def main():
    if not os.getenv("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    cfg = cal.run_ace.load_config()
    cal.run_ace.set_concurrency(cfg["api"].get("concurrency", 8))
    max_tokens = cfg["api"].get("max_tokens", 2048)
    temperature = cfg["api"].get("temperature", 0.0)
    judge_id = cfg["judge"]["id"]

    rubrics = cal.run_ace.load_rubrics()
    ring1_rubric = rubrics["ring1"]

    all_regression = cal.extract_regression_cases()
    regression_cases = all_regression[:3]  # first 3 spot-checks
    all_controls = cal.load_controls()
    invented_cases = [c for c in all_controls if c["case_type"] == "invented_publication"]

    subset = regression_cases + invented_cases

    print(f"Regression spot-checks: {len(regression_cases)} (of {len(all_regression)} available)")
    for c in regression_cases:
        print(f"  - {c['case_id']}")
    print(f"Invented-publication controls: {len(invented_cases)}")
    print(f"Total judge calls: {len(subset)}")
    print(f"Judge: {judge_id}  | temperature: {temperature}  | max_tokens: {max_tokens}")
    print()

    tasks = [
        cal.judge_case(c, judge_id, ring1_rubric, max_tokens, temperature)
        for c in subset
    ]
    results = await asyncio.gather(*tasks)

    print(f"\n{'='*80}")
    print("Per-case results")
    print(f"{'='*80}")
    for r in results:
        if r["case_type"] == "regression":
            orig = r.get("original_accuracy")
            new = r.get("new_accuracy")
            flipped = r.get("flipped_correctly")
            print(f"  [REG ] {r['case_id']:<50} orig_acc={orig}  new_acc={new}  "
                  f"flipped={'YES' if flipped else ('ERR' if new is None else 'no')}")
        else:
            new = r.get("new_accuracy")
            fp = r.get("false_positive")
            print(f"  [INV ] {r['case_id']:<50} new_acc={new}  "
                  f"false_positive={'YES' if fp else ('ERR' if new is None else 'no')}")

    reg = [r for r in results if r["case_type"] == "regression"]
    inv = [r for r in results if r["case_type"] == "invented_publication"]
    reg_flips = sum(1 for r in reg if r.get("flipped_correctly"))
    inv_fp = sum(1 for r in inv if r.get("false_positive"))
    errs = sum(1 for r in results if r.get("error"))

    verdict = {
        "regression_flips": f"{reg_flips}/{len(reg)}",
        "regression_pass": reg_flips >= 3,
        "invented_publication_false_positives": f"{inv_fp}/{len(inv)}",
        "invented_publication_pass": inv_fp <= 1,
        "errors": errs,
    }
    verdict["overall_pass"] = verdict["regression_pass"] and verdict["invented_publication_pass"]

    print(f"\n{'='*80}")
    print("Verdict")
    print(f"{'='*80}")
    print(f"Regression spot-check flips:            {verdict['regression_flips']} "
          f"{'PASS' if verdict['regression_pass'] else 'FAIL'} (>=3 required)")
    print(f"Invented-publication false positives:   {verdict['invented_publication_false_positives']} "
          f"{'PASS' if verdict['invented_publication_pass'] else 'FAIL'} (<=1 allowed)")
    print(f"OVERALL: {'PASS' if verdict['overall_pass'] else 'FAIL'}")
    if errs:
        print(f"Errors: {errs}")

    payload = {
        "run_id": f"calibrate-v23-round2-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Spec A R1 preamble round-2 calibration (tightened preamble; subset)",
        "judge": judge_id,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "controls_file": str(cal.CONTROLS_PATH.relative_to(REPO_ROOT)),
        "regression_case_count": len(regression_cases),
        "invented_control_count": len(invented_cases),
        "pass_criteria": {
            "regression_min_flips": 3,
            "invented_publication_max_fp": 1,
        },
        "results": results,
        "verdict": verdict,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
