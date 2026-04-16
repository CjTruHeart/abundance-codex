#!/usr/bin/env python3
"""
ACE v2.3 Spec A — judge-only calibration dry-run.

Replays the existing v2.2 augmented responses for 11 regression cases through
the patched Ring-1 judge (with R1_ACCURACY_PREAMBLE), plus 10 control cases
(5 invented-publication + 5 wrong-value) to verify the preamble (a) flips
the regression cases 0->1 and (b) doesn't become too permissive.

Does not modify Spec A code. Reuses run-ace.py's judge-call helpers
(judge_response, build_judge_prompt, load_rubrics, load_config, set_concurrency).

Outputs: evals/ace/calibration/results-v2.3-dry-run.json
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

# Dynamically load run-ace.py (hyphenated filename) so we reuse its helpers.
_spec = importlib.util.spec_from_file_location(
    "run_ace", str(REPO_ROOT / "scripts" / "run-ace.py")
)
run_ace = importlib.util.module_from_spec(_spec)
sys.modules["run_ace"] = run_ace
_spec.loader.exec_module(run_ace)


V22_RESULTS = REPO_ROOT / "evals" / "ace" / "results" / "v2.0" / "ace-20260416-204330.json"
PROMPTS_PATH = REPO_ROOT / "evals" / "ace" / "prompts.json"
CONTROLS_PATH = REPO_ROOT / "evals" / "ace" / "calibration" / "controls-v2.3.json"
OUTPUT_PATH = REPO_ROOT / "evals" / "ace" / "calibration" / "results-v2.3-dry-run.json"

TARGET_PROMPTS = {"01-R1", "04-R1", "06-R1", "08-R1", "11-R1"}


def load_prompt_text_by_id() -> dict[str, str]:
    with open(PROMPTS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return {p["id"]: p["prompt"] for p in data["prompts"]}


def extract_regression_cases() -> list[dict]:
    """Find (prompt_id, test_model) pairs where baseline accuracy=1 and augmented accuracy=0
    for the 5 target prompts. Returns list with prompt text + augmented response."""
    with open(V22_RESULTS, encoding="utf-8") as f:
        data = json.load(f)

    lookup = {}
    for r in data["results"]:
        lookup[(r["prompt_id"], r["test_model"], r["condition"])] = r

    prompt_texts = load_prompt_text_by_id()
    cases = []
    models = sorted({r["test_model"] for r in data["results"]})
    for pid in sorted(TARGET_PROMPTS):
        for m in models:
            b = lookup.get((pid, m, "baseline"))
            a = lookup.get((pid, m, "augmented"))
            if not b or not a:
                continue
            b_acc = b["judge_score"].get("accuracy")
            a_acc = a["judge_score"].get("accuracy")
            if b_acc == 1 and a_acc == 0:
                cases.append({
                    "case_type": "regression",
                    "case_id": f"{pid}|{m}",
                    "prompt_id": pid,
                    "test_model": m,
                    "eval_prompt": prompt_texts[pid],
                    "response_text": a["raw_response"],
                    "original_baseline_score": b["judge_score"],
                    "original_augmented_score": a["judge_score"],
                })
    return cases


def load_controls() -> list[dict]:
    with open(CONTROLS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    cases = []
    for c in data["invented_publication_controls"]:
        cases.append({
            "case_type": "invented_publication",
            "case_id": c["case_id"],
            "prompt_id": c.get("prompt_id_basis"),
            "eval_prompt": c["eval_prompt"],
            "response_text": c["response_text"],
            "description": c["description"],
        })
    for c in data["wrong_value_controls"]:
        cases.append({
            "case_type": "wrong_value",
            "case_id": c["case_id"],
            "prompt_id": c.get("prompt_id_basis"),
            "eval_prompt": c["eval_prompt"],
            "response_text": c["response_text"],
            "description": c["description"],
        })
    return cases


async def judge_case(case: dict, judge_id: str, rubric: dict,
                     max_tokens: int, temperature: float) -> dict:
    """Run the Ring-1 judge on one case. Retries handled inside judge_response."""
    # First attempt: standard judge_response (has internal retries)
    result = await run_ace.judge_response(
        judge_id,
        case["eval_prompt"],
        case["response_text"],
        ring=1,
        rubric=rubric,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    out = {
        "case_type": case["case_type"],
        "case_id": case["case_id"],
        "prompt_id": case.get("prompt_id"),
        "test_model": case.get("test_model"),
    }
    if result is None:
        # One explicit retry outside judge_response (its 3 internal already ran)
        result = await run_ace.judge_response(
            judge_id,
            case["eval_prompt"],
            case["response_text"],
            ring=1,
            rubric=rubric,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    if result is None:
        out["error"] = "judge_call_failed_after_retries"
        out["new_score"] = None
        out["new_accuracy"] = None
    else:
        out["new_score"] = result
        out["new_accuracy"] = result.get("accuracy")

    if case["case_type"] == "regression":
        out["original_baseline_score"] = case["original_baseline_score"]
        out["original_augmented_score"] = case["original_augmented_score"]
        orig = case["original_augmented_score"].get("accuracy")
        out["original_accuracy"] = orig
        if out["new_accuracy"] is not None:
            out["flipped_correctly"] = (orig == 0 and out["new_accuracy"] == 1)
        else:
            out["flipped_correctly"] = None
    else:
        out["description"] = case.get("description")
        # For controls, "false positive" = judge incorrectly gives accuracy=1
        if out["new_accuracy"] is not None:
            out["false_positive"] = (out["new_accuracy"] == 1)
        else:
            out["false_positive"] = None
    return out


def summarize(all_results: list[dict]) -> dict:
    reg = [r for r in all_results if r["case_type"] == "regression"]
    inv = [r for r in all_results if r["case_type"] == "invented_publication"]
    wrong = [r for r in all_results if r["case_type"] == "wrong_value"]

    def count_flips(items):
        return sum(1 for r in items if r.get("flipped_correctly"))

    def count_fp(items):
        return sum(1 for r in items if r.get("false_positive"))

    def count_err(items):
        return sum(1 for r in items if r.get("error"))

    reg_flips = count_flips(reg)
    inv_fp = count_fp(inv)
    wrong_fp = count_fp(wrong)

    verdict = {
        "regression_flips": f"{reg_flips}/{len(reg)}",
        "regression_pass": reg_flips >= 9,
        "invented_publication_false_positives": f"{inv_fp}/{len(inv)}",
        "invented_publication_pass": inv_fp <= 1,
        "wrong_value_false_positives": f"{wrong_fp}/{len(wrong)}",
        "wrong_value_pass": wrong_fp == 0,
        "errors_regression": count_err(reg),
        "errors_invented": count_err(inv),
        "errors_wrong": count_err(wrong),
    }
    verdict["overall_pass"] = (
        verdict["regression_pass"]
        and verdict["invented_publication_pass"]
        and verdict["wrong_value_pass"]
    )
    return verdict


async def main():
    if not os.getenv("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    cfg = run_ace.load_config()
    run_ace.set_concurrency(cfg["api"].get("concurrency", 8))
    max_tokens = cfg["api"].get("max_tokens", 2048)
    temperature = cfg["api"].get("temperature", 0.0)
    judge_id = cfg["judge"]["id"]

    rubrics = run_ace.load_rubrics()
    ring1_rubric = rubrics["ring1"]

    regression_cases = extract_regression_cases()
    control_cases = load_controls()
    all_cases = regression_cases + control_cases

    print(f"Regression cases extracted: {len(regression_cases)}")
    print(f"Control cases loaded: {len(control_cases)} "
          f"({sum(1 for c in control_cases if c['case_type']=='invented_publication')} invented + "
          f"{sum(1 for c in control_cases if c['case_type']=='wrong_value')} wrong-value)")
    print(f"Total judge calls: {len(all_cases)}")
    print(f"Judge: {judge_id}  | temperature: {temperature}  | max_tokens: {max_tokens}")
    print()

    # Run all cases concurrently (bounded by run_ace's semaphore)
    tasks = [
        judge_case(c, judge_id, ring1_rubric, max_tokens, temperature)
        for c in all_cases
    ]
    results = await asyncio.gather(*tasks)

    # Pretty-print per-case
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
            tag = "INV " if r["case_type"] == "invented_publication" else "WRNG"
            print(f"  [{tag}] {r['case_id']:<50} new_acc={new}  "
                  f"false_positive={'YES' if fp else ('ERR' if new is None else 'no')}")

    verdict = summarize(results)

    print(f"\n{'='*80}")
    print("Verdict")
    print(f"{'='*80}")
    print(f"Regression flips:                       {verdict['regression_flips']} "
          f"{'PASS' if verdict['regression_pass'] else 'FAIL'} (>=9 required)")
    print(f"Invented-publication false positives:   {verdict['invented_publication_false_positives']} "
          f"{'PASS' if verdict['invented_publication_pass'] else 'FAIL'} (<=1 allowed)")
    print(f"Wrong-value false positives:            {verdict['wrong_value_false_positives']} "
          f"{'PASS' if verdict['wrong_value_pass'] else 'FAIL'} (0 allowed)")
    print(f"OVERALL: {'ALL CRITERIA PASS' if verdict['overall_pass'] else 'FAIL'}")
    if verdict["errors_regression"] or verdict["errors_invented"] or verdict["errors_wrong"]:
        print(f"Errors: regression={verdict['errors_regression']}  "
              f"invented={verdict['errors_invented']}  wrong={verdict['errors_wrong']}")

    payload = {
        "run_id": f"calibrate-v23-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Spec A R1 accuracy preamble calibration dry-run (judge-side only)",
        "judge": judge_id,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "v22_results_file": str(V22_RESULTS.relative_to(REPO_ROOT)),
        "controls_file": str(CONTROLS_PATH.relative_to(REPO_ROOT)),
        "regression_case_count": len(regression_cases),
        "control_case_count": len(control_cases),
        "pass_criteria": {
            "regression_min_flips": 9,
            "invented_publication_max_fp": 1,
            "wrong_value_max_fp": 0,
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
