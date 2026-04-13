#!/usr/bin/env python3
"""
ace-authorship-report.py — Post-run cross-authorship matrix generator.

Consumes a v2.0 ACE results JSON and emits AUTHORSHIP-MATRIX.md: for each
(test_model, author_model) pair, the mean augmented-minus-baseline delta
across prompts where that author contributed at least one retrieved entry.

This is observational, not causal — retrieval composition is a side effect
of the Dojo Retriever's ranking, not a controlled variable. See
METHODOLOGY.md §9.7.

Usage:
  python3 scripts/ace-authorship-report.py               # latest v2.0 run
  python3 scripts/ace-authorship-report.py --input <path-to-json>
  python3 scripts/ace-authorship-report.py --input <path> --compare-v1
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

REPO_ROOT = Path(__file__).resolve().parent.parent
V2_DIR = REPO_ROOT / "evals" / "ace" / "results" / "v2.0"
V1_OPUS_PATH = REPO_ROOT / "evals" / "ace" / "results" / "v1.0" / "ace-v1-opus-only.json"


def find_latest_v2_run() -> Path:
    runs = sorted(V2_DIR.glob("ace-*.json"), reverse=True)
    if not runs:
        sys.exit(f"ERROR: no v2.0 run JSON found in {V2_DIR}")
    return runs[0]


def index_by_baseline(results: list) -> dict:
    """Build a {(prompt_id, test_model): baseline_score} index."""
    idx = {}
    for r in results:
        if r["condition"] != "baseline":
            continue
        score = r.get("aggregated", {}).get("score")
        if score is None:
            continue
        idx[(r["prompt_id"], r["test_model"])] = score
    return idx


def build_matrix(results: list) -> tuple[dict, list, list]:
    """Return ({test_model: {author_model: {"deltas": [...], "n": int}}}, sorted test models, sorted authors)."""
    baselines = index_by_baseline(results)
    matrix: dict = {}
    authors_seen: set = set()
    models_seen: set = set()

    for r in results:
        if r["condition"] != "augmented":
            continue
        aug = r.get("aggregated", {}).get("score")
        if aug is None:
            continue
        key = (r["prompt_id"], r["test_model"])
        if key not in baselines:
            continue
        delta = aug - baselines[key]
        models_seen.add(r["test_model"])

        authors = {
            ra.get("co_author_model", "")
            for ra in r.get("retrieval", {}).get("retrieved_authors", [])
            if ra.get("co_author_model")
        }
        for author in authors:
            authors_seen.add(author)
            cell = matrix.setdefault(r["test_model"], {}).setdefault(author, {"deltas": [], "n": 0})
            cell["deltas"].append(delta)
            cell["n"] += 1

    return matrix, sorted(models_seen), sorted(authors_seen)


def render_matrix(matrix: dict, models: list, authors: list) -> list[str]:
    header = "| test_model \\ author_model | " + " | ".join(authors) + " | N prompts |"
    sep = "|" + "---|" * (len(authors) + 2)
    lines = [header, sep]
    for m in models:
        total_n = 0
        row_cells = []
        for a in authors:
            cell = matrix.get(m, {}).get(a, {"deltas": [], "n": 0})
            if cell["deltas"]:
                avg = mean(cell["deltas"])
                row_cells.append(f"{'+' if avg >= 0 else ''}{avg:.2f} (n={cell['n']})")
                total_n = max(total_n, cell["n"])
            else:
                row_cells.append("—")
        lines.append(f"| {m} | " + " | ".join(row_cells) + f" | {total_n} |")
    return lines


def overall_by_author(matrix: dict, authors: list) -> list[str]:
    lines = ["| author_model | mean delta | total observations |",
             "|--------------|-----------|---------------------|"]
    for a in authors:
        deltas = []
        for m, row in matrix.items():
            cell = row.get(a)
            if cell:
                deltas.extend(cell["deltas"])
        if deltas:
            lines.append(f"| {a} | {'+' if mean(deltas) >= 0 else ''}{mean(deltas):.3f} | {len(deltas)} |")
        else:
            lines.append(f"| {a} | — | 0 |")
    return lines


def same_company_analysis(matrix: dict, models: list, authors: list) -> list[str]:
    """Does each test model score higher on its own company's authored context?"""
    company_map = {
        "anthropic/claude-haiku-4-5": "claude-opus-4-6",
        "openai/gpt-5.4-mini": "chatgpt-5.4-thinking",
        "google/gemini-3.1-flash-lite-preview": "gemini-3.1-pro",
        "x-ai/grok-4.1-fast": "grok-super",
    }
    lines = ["| test_model | same-company author | same mean Δ | cross mean Δ | delta-of-deltas |",
             "|------------|---------------------|------------|--------------|----------------|"]
    for m in models:
        own = company_map.get(m)
        if not own:
            continue
        same_deltas = []
        cross_deltas = []
        for a, cell in matrix.get(m, {}).items():
            if a == own:
                same_deltas.extend(cell["deltas"])
            else:
                cross_deltas.extend(cell["deltas"])
        if not same_deltas and not cross_deltas:
            continue
        s = mean(same_deltas) if same_deltas else 0.0
        c = mean(cross_deltas) if cross_deltas else 0.0
        diff = s - c
        lines.append(
            f"| {m} | {own} | {'+' if s >= 0 else ''}{s:.3f} | {'+' if c >= 0 else ''}{c:.3f} | "
            f"{'+' if diff >= 0 else ''}{diff:.3f} |"
        )
    return lines


def generate_report(run_json: dict, out_path: Path, source: str):
    results = run_json.get("results", [])
    matrix, models, authors = build_matrix(results)

    lines = [
        "# ACE Authorship Matrix",
        "",
        f"> Generated: {datetime.now(timezone.utc).isoformat()}",
        f"> Source run: `{source}`",
        f"> Judge: `{run_json.get('judge', 'unknown')}`",
        "",
        "This report measures whether the identity of the model that co-authored",
        "a retrieved Codex entry correlates with how much the retrieval helped a",
        "given test subject. It is **observational**, not causal — retrieval",
        "composition is a side effect of Dojo Retriever ranking, not a controlled",
        "variable. See METHODOLOGY.md §9.7.",
        "",
        "---",
        "",
        "## Cross-Authorship Matrix",
        "",
        "Cells: mean (augmented − baseline) delta across prompts where that",
        "author contributed ≥1 retrieved entry. `n` is prompt count.",
        "",
    ]
    if not matrix:
        lines += ["_No augmented results with authorship metadata found._", ""]
    else:
        lines += render_matrix(matrix, models, authors)
        lines += ["", "---", "", "## Mean Delta by Author (pooled over test models)", ""]
        lines += overall_by_author(matrix, authors)
        lines += ["", "---", "", "## Same-Company vs Cross-Company Effect", "",
                  "For each test model, compare its mean delta on retrieved contexts",
                  "authored by its own company vs. contexts authored by other companies.",
                  "A positive `delta-of-deltas` is consistent with (but does not prove)",
                  "a same-company affinity effect.",
                  ""]
        lines += same_company_analysis(matrix, models, authors)

    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def generate_comparison(v2_json: dict, v2_source: str, out_path: Path):
    """Produce v1-vs-v2-comparison.md if v1.0 Opus-only rebaseline exists."""
    if not V1_OPUS_PATH.exists():
        return False
    with open(V1_OPUS_PATH, encoding="utf-8") as f:
        v1 = json.load(f)

    v1s = v1.get("summary", {})
    v2s = v2_json.get("summary", {})

    lines = [
        "# ACE v1.0 vs v2.0 — Judge-Matched Comparison",
        "",
        f"> Generated: {datetime.now(timezone.utc).isoformat()}",
        f"> v1.0 source: `{v1.get('source_run')}` (Opus-only rebaseline)",
        f"> v2.0 source: `{v2_source}`",
        f"> Both versions judged by: `anthropic/claude-opus-4.6`",
        "",
        "---",
        "",
        "## Overall Delta",
        "",
        "| Version | Baseline | Augmented | Delta |",
        "|---------|----------|-----------|-------|",
    ]
    for label, s in [("v1.0 Opus", v1s), ("v2.0", v2s)]:
        o = s.get("overall", {})
        d = o.get("delta", 0)
        lines.append(f"| {label} | {o.get('baseline', 0)} | {o.get('augmented', 0)} | {'+' if d >= 0 else ''}{d} |")

    def delta_diff(v1d, v2d):
        return round((v2d or 0) - (v1d or 0), 2)

    lines += ["", "---", "", "## By Ring", "",
              "| Ring | v1.0 Δ | v2.0 Δ | diff |",
              "|------|--------|--------|------|"]
    ring_names = {1: "R1", 2: "R2", 3: "R3"}
    for ring in [1, 2, 3]:
        v1d = v1s.get("by_ring", {}).get(str(ring), v1s.get("by_ring", {}).get(ring, {})).get("delta", 0)
        v2d = v2s.get("by_ring", {}).get(str(ring), v2s.get("by_ring", {}).get(ring, {})).get("delta", 0)
        diff = delta_diff(v1d, v2d)
        lines.append(f"| {ring_names[ring]} | {'+' if v1d >= 0 else ''}{v1d} | {'+' if v2d >= 0 else ''}{v2d} | {'+' if diff >= 0 else ''}{diff} |")

    lines += ["", "---", "", "## By Test Model", "",
              "| Model | v1.0 Δ | v2.0 Δ | diff |",
              "|-------|--------|--------|------|"]
    all_models = sorted(set(v1s.get("by_model", {}).keys()) | set(v2s.get("by_model", {}).keys()))
    for m in all_models:
        v1d = v1s.get("by_model", {}).get(m, {}).get("delta", 0)
        v2d = v2s.get("by_model", {}).get(m, {}).get("delta", 0)
        diff = delta_diff(v1d, v2d)
        lines.append(f"| {m} | {'+' if v1d >= 0 else ''}{v1d} | {'+' if v2d >= 0 else ''}{v2d} | {'+' if diff >= 0 else ''}{diff} |")

    lines += ["", "---", "",
              "A materially different v2.0 delta from v1.0 Opus-only indicates that",
              "expanding the corpus to 252 entries changed the retrieval quality",
              "(the only other variable held constant). The Grok judge artifact is",
              "eliminated in both rows so it cannot explain a difference.",
              ""]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=None,
                    help="v2.0 run JSON (default: latest in results/v2.0/)")
    ap.add_argument("--compare-v1", action="store_true",
                    help="Also write v1-vs-v2-comparison.md")
    args = ap.parse_args()

    src = args.input or find_latest_v2_run()
    with open(src, encoding="utf-8") as f:
        run_json = json.load(f)

    out_dir = src.parent
    out_path = out_dir / "AUTHORSHIP-MATRIX.md"
    generate_report(run_json, out_path, str(src.relative_to(REPO_ROOT)))
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")

    if args.compare_v1:
        cmp_path = out_dir / "v1-vs-v2-comparison.md"
        if generate_comparison(run_json, str(src.relative_to(REPO_ROOT)), cmp_path):
            print(f"Wrote {cmp_path.relative_to(REPO_ROOT)}")
        else:
            print(f"[skip] {V1_OPUS_PATH.relative_to(REPO_ROOT)} not found — run scripts/ace-v1-opus-rebaseline.py first")


if __name__ == "__main__":
    main()
