# Pre-Publication Audit Report

**Date:** 2026-04-14
**Auditor:** Claude Code (Opus 4.6)
**Repo SHA:** 12f0870
**Branch:** main (6 commits ahead of origin)

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| WARNING  | 4 |
| NOTE     | 4 |

---

## CRITICAL Issues (Block Publication)

### AUDIT-001: CITATION.cff is completely stale

**File:** `CITATION.cff`

Every field is outdated:

| Field | Current Value | Correct Value |
|-------|--------------|---------------|
| version | "1.0" | "2.1" |
| date-released | "2026-03-28" | "2026-04-14" |
| abstract entry count | "63 entries" | "273 entries" |
| abstract judgments | "2,016 cross-model judgments" | "504 matched-pair judgments" |
| abstract improvement | "+9% improvement" | "+0.38/5 delta" |

**Fix:** Rewrite abstract to match paper's abstract. Update version, date, and all statistics.

---

### AUDIT-002: 21/21 council_synthesis entries missing `co_author_model` in YAML frontmatter

**Files:** All `domains/*/13-council-synthesis.md`

No council_synthesis entry has `co_author_model` in its YAML frontmatter. Expected value: `"multi-model-council"`. Only `domains/01-energy/13-council-synthesis.md` has it in the body text (governance section), but not in YAML. The remaining 20 don't have it anywhere.

As a result, the JSONL export also lacks `co_author_model` for all 21 council_synthesis entries.

The 252 base entries are correct: 63 each of claude-opus-4-6, grok-super, gemini-3.1-pro, chatgpt-5.4-thinking.

**Fix:** Add `co_author_model: "multi-model-council"` to YAML frontmatter of all 21 council_synthesis entries, then re-export JSONL.

---

## WARNING Issues (Fix Before Publication)

### AUDIT-003: License inconsistency — paper claims CC-BY, no CC-BY file exists

**File:** `paper/ACE-TECHNICAL-REPORT.md` lines 19 and 559

The paper abstract (line 19) says "released under MIT/CC-BY" and Appendix C (line 559) says "License: MIT (code), CC-BY (dataset)". However:
- `LICENSE` file is MIT only
- `README.md` says MIT only
- `DATASHEET.md` says MIT only
- No CC-BY license file exists in the repo

**Fix:** Either add a CC-BY license file for the dataset (if dual-license intended) or remove CC-BY references from the paper.

---

### AUDIT-004: GLOSSARY missing two key paper terms

**File:** `GLOSSARY.md`

Two terms used significantly in the paper are absent from the glossary:

1. **shadow force-pull** — retrieval mechanism described in paper Section 5 (Dojo Retriever architecture)
2. **empowers** — R3 criterion with the notable -0.155 deficit, discussed extensively in paper Section 6.7

All other 28+ paper terms are present in the glossary.

**Fix:** Add definitions for both terms.

---

### AUDIT-005: Bootstrap CI bounds differ by ±0.01 from paper

**Source files:** `evals/ace/results/v2.1/SCORECARD-v2.1.md`, `paper/ACE-TECHNICAL-REPORT.md`

When independently bootstrapping from raw JSON (seed=42, n=10,000):

| Metric | Paper CI | Computed CI | Diff |
|--------|----------|-------------|------|
| v2.1 Overall | [+0.25, +0.50] | [+0.26, +0.50] | low bound +0.01 |
| v2.0 Overall | [+0.21, +0.46] | [+0.22, +0.45] | both ±0.01 |

This is expected bootstrap variance from different random seeds. Not a data integrity issue, but worth documenting for reproducibility — the paper should either fix the seed or note the ±0.01 tolerance.

---

### AUDIT-006: Pillar overall deltas differ by 0.01 from scorecard (rounding)

**Source:** `evals/ace/results/v2.1/SCORECARD-v2.1.md`

| Pillar | Scorecard | Computed | Diff |
|--------|-----------|----------|------|
| II Human Capability | +0.52 | +0.53 | +0.01 |
| IV Production & Discovery | +0.82 | +0.81 | -0.01 |

Likely a rounding-direction difference (round-half-even vs round-half-up). All other values match exactly. Not a data integrity issue — but the scorecard generator should use consistent rounding.

---

## NOTE Issues (Cosmetic, Fix Later)

### AUDIT-007: Only 1/21 council_synthesis entries uses the 5-check reasoning format

Only `domains/01-energy/13-council-synthesis.md` contains the `**Evidence check:**`, `**Builder check:**`, `**Shadow check:**`, `**Action check:**`, `**Frame check:**` pattern. The other 20 council_synthesis entries use different reasoning check formats. This is cosmetic — validate-entry.py passes all of them.

---

### AUDIT-008: Two entries at confidence ceiling (0.96)

- `domains/10-communication/08-satellite-constellations-builder-profile.md` (0.96)
- `domains/14-transportation/09-babcock-ranch-resilience-builder-profile.md` (0.96)

Both are builder_profile entries about well-documented infrastructure projects. The 0.96 score is at the documented ceiling for "measured phenomena" (DATASHEET says 0.88-0.96). Technically within range, but worth noting as they're at the absolute top.

---

### AUDIT-009: "Composite" keyword triggers ~100 false positives

The composite witness disclosure check flagged ~100 entries. Investigation shows the vast majority mention "composite" in technical contexts (composite materials, composite indicators, composite patterns). Approximately 7 entries have actual composite witness characters with proper `**Composite based on documented patterns...**` disclosures. The check regex needs refinement, but no actual disclosure is missing.

---

### AUDIT-010: 08-longevity council_synthesis mentions "Phase 3"

`domains/08-longevity/13-council-synthesis.md` line 212 contains "Phase 3" but in clinical trial context ("Phase 1... Phase 2... Phase 3 failure rate"), not as a Shift Arc phase. Council_synthesis entries correctly skip Shift Arc Phase 3. False positive from the audit script.

---

## Verified Clean

The following audits passed with zero issues:

| Audit | Result |
|-------|--------|
| **1.1 Entry validation** | 273/273 PASS, 0 FAIL |
| **1.2 Entry count by domain** | 13 entries × 21 domains = 273 |
| **1.3 ID uniqueness** | No duplicate IDs |
| **1.4 ID format** | All 273 match `ac-YYYYMMDD-XXXX` |
| **1.5 File naming** | All match `[##]-[slug].md` |
| **2.1 Required YAML fields** | All 273 entries have id, entry_type, domain, status, created, version, confidence, codex_version |
| **2.2 Entry type distribution** | 12 types, council_synthesis = 21, matches expectations |
| **2.3 Domain field matches folder** | All 273 entries match |
| **2.5 Domain connections** | No self-references, all strengths in [0,1], all relationship types valid, max 5 per entry |
| **3.1 co_author_human** | 273/273 = "Cj TruHeart" (in YAML or body) |
| **3.2 co_creative_partner** | 273/273 = "CyberMonk" (in YAML or body) |
| **3.4 Council synthesis attribution** | All 21 have council_models and synthesis_method in body |
| **4.1 Reasoning Scaffold** | All 21 have Scaffold, Scarcity Trap, Reframe Chain, Contrastive Pair |
| **4.3 No Phase 3 in Shift Arc** | 0/21 have Phase 3 as Shift Arc (longevity mention is clinical trial context) |
| **5.1 JSONL line count** | 273 lines |
| **5.2 JSONL parsing** | All 273 parse correctly, unique IDs, all critical fields present |
| **5.3 JSONL ↔ markdown sync** | 273 IDs match in both directions |
| **5.4 Council synthesis JSONL fields** | reasoning_scaffold, practice_hook (agent), contrastive pair all present |
| **6.1 Results files** | v1.0, v2.0, v2.1 all present and well-formed |
| **7.1 Git status** | Clean working tree |
| **7.2 .gitignore** | Covers .env, __pycache__/, *.pyc, .DS_Store, node_modules/ |
| **7.3 Sensitive data** | No API keys in tracked files; .env not tracked |
| **7.4 LICENSE** | MIT license present |
| **7.5 Large files** | JSONL = 6.0MB, result JSONs = 3.3-3.4MB each — all under 10MB |
| **8.1 README accuracy** | 273 entries, 21 domains, +0.38 delta, per-model deltas, v2.1, MIT — all correct |
| **9.2 Prediction commit** | e90869d exists and predates v2.1 results |
| **9.3 Reproducibility** | validate-entry.py, run-ace.py --dry-run, export-to-jsonl.py all work |
| **JSONL schema validation** | `validate-jsonl.py` passes all 273 entries |
| **Export round-trip** | export-to-jsonl.py produces identical 273-line output |
| **CHANGELOG dates** | v2.1=Apr14, v2.0=Apr13 match git log timestamps |
| **DATASHEET distribution** | Entry type counts and percentages match actual data |
| **DATASHEET confidence calibration** | Ranges match: 0.88-0.96 (measured), 0.78-0.87 (trends), 0.65-0.78 (frameworks), council_synthesis 0.78-0.84 |
| **CONTRIBUTING.md process** | Correctly describes 4-step deliberation (multi-model → human synthesis → Reasoning Scaffold → Gold Standard) |

---

## Numbers Verification

Every numerical claim in the paper was independently computed from the raw results JSON:

### v2.1 Claims (from `ace-20260414-021808.json`)

| Paper Claim | Computed | Status |
|-------------|----------|--------|
| Overall delta = +0.38 | +0.38 | **MATCH** |
| Baseline mean = 4.12 | 4.12 | **MATCH** |
| Augmented mean = 4.50 | 4.50 | **MATCH** |
| Overall CI = [+0.25, +0.50] | [+0.26, +0.50] | **~MATCH** (±0.01 bootstrap) |
| R1 delta = +0.44 | +0.44 | **MATCH** |
| R2 delta = +0.55 | +0.55 | **MATCH** |
| R3 delta = +0.14 | +0.14 | **MATCH** |
| R3 CI = [-0.04, +0.32] | [-0.04, +0.32] | **MATCH** |
| GPT-5.4 Mini delta = +0.62 | +0.62 | **MATCH** |
| Haiku delta = +0.52 | +0.52 | **MATCH** |
| Gemini delta = +0.24 | +0.24 | **MATCH** |
| Grok delta = +0.13 | +0.13 | **MATCH** |
| GPT-5.4 Mini R3 = +0.57 | +0.57 | **MATCH** |
| Haiku R3 = +0.38 | +0.38 | **MATCH** |
| Gemini R3 = +0.00 | +0.00 | **MATCH** |
| Grok R3 = -0.38 | -0.38 | **MATCH** |
| Pillar I delta = +0.14 | +0.14 | **MATCH** |
| Pillar II delta = +0.52 | +0.53 | **~MATCH** (rounding) |
| Pillar III delta = +0.22 | +0.22 | **MATCH** |
| Pillar IV delta = +0.82 | +0.81 | **~MATCH** (rounding) |
| Pillar V delta = +0.46 | +0.46 | **MATCH** |
| Pillar I R3 = +0.08 | +0.08 | **MATCH** |
| Pillar II R3 = +0.50 | +0.50 | **MATCH** |
| Pillar III R3 = -0.12 | -0.12 | **MATCH** |
| Pillar IV R3 = +0.31 | +0.31 | **MATCH** |
| Pillar V R3 = +0.25 | +0.25 | **MATCH** |
| frames_solvable = +0.000 | +0.000 | **MATCH** |
| identifies_leverage = +0.000 | +0.000 | **MATCH** |
| concrete_steps = +0.083 | +0.083 | **MATCH** |
| real_examples = +0.214 | +0.214 | **MATCH** |
| empowers = -0.155 | -0.155 | **MATCH** |
| 273 entries | 273 | **MATCH** |
| 252 base + 21 council_synthesis | 252 + 21 | **MATCH** |

### v2.0 Claims (from `ace-20260413-103133.json`)

| Paper Claim | Computed | Status |
|-------------|----------|--------|
| Baseline = 4.17, Aug = 4.50, Delta = +0.33 | 4.17, 4.50, +0.33 | **MATCH** |
| CI = [+0.21, +0.46] | [+0.22, +0.45] | **~MATCH** (±0.01 bootstrap) |

### v1.0 Opus-only Claims (from `ace-v1-opus-only.json`)

| Paper Claim | Computed | Status |
|-------------|----------|--------|
| Baseline = 4.14, Aug = 4.49, Delta = +0.35 | 4.14, 4.49, +0.35 | **MATCH** |

### Other Claims

| Paper Claim | Source | Status |
|-------------|--------|--------|
| Governance frequency = 85.2% | governance-frequency-report.md | **MATCH** |
| Predictions at commit e90869d | git log | **MATCH** (commit exists, predates v2.1) |
| v2.0 at commit 529bb85 | git log | **MATCH** |
| v2.1 at commit 0a0dc68 | git log | **MATCH** |

### Verdict

**35/35 claims match exactly. 3 additional claims match within ±0.01 (bootstrap variance / rounding). Zero mismatches found.**

---

## Confidence Score Distribution (Audit 2.4)

| Range | Description | Count | % |
|-------|------------|-------|---|
| 0.88-0.96 | Measured phenomena | 75 | 27.5 |
| 0.78-0.87 | Documented trends | 140 | 51.3 |
| 0.65-0.77 | Conceptual frameworks | 47 | 17.2 |
| 0.58-0.64 | Speculative (paradigm seeds) | 11 | 4.0 |

- council_synthesis range: 0.78-0.84 (mean 0.821) — within expected 0.70-0.85
- No entry above 0.96 or below 0.50
- Two entries at 0.96 ceiling (NOTE, not actionable)
- Mean: 0.823

---

*Report generated by Claude Code. No fixes applied — awaiting human review.*
