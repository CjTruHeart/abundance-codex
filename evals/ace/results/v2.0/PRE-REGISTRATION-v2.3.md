# ACE v2.3 Pre-Registration

**Filed:** 2026-04-16
**Parent spec:** `evals/ace/results/v2.0/TIER-2-SPECS.md` (commit 53b16a9)
**Baseline:** v2.2 results (`ace-20260416-204330.json`, commit af1d628)
**v2.2 pre-registration:** commit 546095e

---

## Interventions

### Spec A — R1 Accuracy (Judge Calibration + Retriever Year-Relabeling)

Execution order (refined from TIER-2-SPECS.md based on review):

1. **PRIMARY:** Retriever relabels evidence anchor years ≥ 2025 → `"recent data"` in passage output (output-layer only, source markdown and JSONL untouched). Applies at FULL and CONDENSED tiers (MINIMAL has no anchors).
2. **SECONDARY:** R1 judge prompt preamble instructing `accuracy=1` for plausible sourced claims even if post-cutoff; `accuracy=0` only for internal inconsistency, contradiction of established values, or unsourced fabrication. Ring-gated to R1 only.
3. **TERTIARY:** `CODEX_SYSTEM_PROMPT` softens "note the source year" → "note the source and time period (year if specific, else 'recent')".

Rationale for re-ordering: retriever-layer relabeling is the durable structural fix; judge preamble is a quick-win that will decay as judge training cutoffs advance past Codex vintages. Leading with retriever is robust; judge preamble is the secondary hedge.

### Spec B — Pillar-Gated Empowerment

Conditional gating of Check 6 (Empowerment) and Empowered Action Frame paragraph across the 21 `council_synthesis` entries, based on v2.1 baseline R3 performance:

- **FULL strength** (Check 6 + Empowered Action Frame both kept): Pillar III all 6 domains + Pillar I food, shelter
- **CONDENSED** (Check 6 kept, Empowered Action Frame removed): Pillar I energy/water/health/environment + Pillar V space/future-vision + Pillar IV co-creative-intelligence
- **REMOVED** (both Check 6 and Empowered Action Frame removed): Pillar II consciousness/longevity/education + Pillar IV computation-intelligence/science-engineering/manufacturing

---

## Predictions

| Metric | v2.2 Actual | Predicted v2.3 | Falsification Bound |
|---|---|---|---|
| R1 accuracy delta | −0.226 | −0.05 to +0.05 | < −0.10 |
| R3 overall delta | +0.179 | +0.25 to +0.30 | < +0.22 |
| R3 Pillar II delta | +0.250 | +0.40 to +0.50 | < +0.30 |
| R3 Pillar III delta | +0.208 | ≥ +0.15 (hold gains) | < +0.10 |
| R3 consciousness domain | −0.250 | +0.25 to +0.50 | < 0.00 |
| `empowers` criterion | −0.036 | ≥ −0.05 (hold gains) | < −0.10 |
| `real_examples` criterion | +0.131 | +0.15 to +0.20 | < +0.10 |
| Overall delta | +0.420 | +0.43 to +0.48 | < +0.40 |

---

## What Failure Teaches

- **If R1 accuracy stays < −0.10:** judge calibration is not the root cause; escalate to rubric redesign (redefine `accuracy` criterion to separate "verifiable" from "plausible")
- **If R3 overall stays < +0.22:** pillar-gating insufficient; escalate to Tier 2B model-adaptive scaffold intensity
- **If Pillar III R3 drops below +0.10:** empowerment removal in adjacent pillars has cross-pillar spillover; revert to uniform application
- **If consciousness doesn't recover to ≥ 0.00:** domain-specific content issue, not empowerment gate — re-open consciousness-domain investigation
- **If Grok R3 still < 0 after both specs:** model-side limitation, not data-side; document as finding, defer to Tier 2B

---

## Controls

Spec A calibration dry-run (must pass before full v2.3 benchmark):

| Test Set | Count | Pass Criterion |
|---|---|---|
| Worst R1 accuracy regressions (1→0 under v2.2 augmented) | 13 | ≥ 9 flip 0→1 under patched judge |
| Invented-publication controls (plausible-sounding fabricated sources) | 5 | ≤ 1 false positive (flip incorrect 0→1) |
| Wrong-value controls (real sources, wrong numbers) | 5 | 0 false positives |

Failure modes:
- Regression flips < 9 → judge preamble too weak; strengthen or keep year-relabeling as sole fix
- Invented controls > 1 false positive → judge preamble too permissive; tighten language or drop preamble, rely on year-relabeling alone
- Wrong-value controls > 0 false positive → critical; revert judge preamble entirely

Spec B has no dry-run (deterministic structural change to 21 files); the v2.3 benchmark itself is the test.

---

## Scientific Integrity Notes

- Pre-registration committed BEFORE any Spec A or Spec B implementation.
- Falsification bounds written to be visibly narrow enough to be genuinely refutable (point-estimate predictions, not wide-band "improvement" claims).
- R3 overall v2.2 CI was [+0.027, +0.329], so pre-reg target +0.25 was inside CI. Spec B is addressing a correctable miss within CI, not a structural failure — framed as such.
- Single-judge limitation acknowledged: no rationale text stored, Phase 2 findings are pattern inference. A second judge with different training cutoff would test the hypothesis more cleanly. Not available for v2.3.
- Codex freshness outpacing judge training is a durable tension. Retriever-layer relabeling is the structural hedge; judge preamble is the quick-win.

---

## Post-Hoc Calibration Addendum (2026-04-16, pre-benchmark)

Added after implementation but before v2.3 benchmark run — records the calibration outcome that triggered a pre-registered decision branch.

**Spec A judge preamble dropped after two calibration rounds.**

| Round | Preamble posture | Regression flips (criterion ≥ 9/13 or ≥ 3/3) | Invented FPs (≤ 1/5) | Wrong-value FPs (0/5) |
|---|---|---|---|---|
| 1 | Permissive, `"and similar institutional publishers"` halo | **11/11 PASS** | **2/5 FAIL** | 0/5 PASS |
| 2 | Tightened, "confirm publisher from training knowledge" | **1/3 FAIL** | 0/5 PASS | (not retested) |

The two failure modes are on opposite sides of the same axis: Round 1 grandfathered fabricated institutional-sounding names via halo phrasing; Round 2 over-corrected and rejected legitimate citations to bodies the judge couldn't independently recognize. Per the pre-registered rule ("two rounds is rigorous; three is overfitting to the control set"), the preamble was dropped rather than tuned a third time.

**Final Spec A composition for v2.3 benchmark:**
1. Retriever year-relabeling (years ≥ 2025 → `"recent data"` in passage output, FULL + CONDENSED tiers) — **KEPT**
2. R1 judge preamble — **DROPPED** (both rounds failed orthogonal control sets)
3. `CODEX_SYSTEM_PROMPT` softening ("source and time period, year if specific, else 'recent'") — **KEPT**

**Revised predictions** (R1 accuracy delta target loosens slightly without the judge-side calibration):

| Metric | Pre-reg original | Revised for benchmark |
|---|---|---|
| R1 accuracy delta | −0.05 to +0.05 | −0.08 to +0.05 |
| R1 accuracy falsification bound | < −0.10 | < −0.12 |

All other predictions unchanged. The retriever relabel is the durable structural fix and should carry most of the R1 recovery; the lost judge-side compensation is bounded (~0.03) based on Round-1 regression-flip magnitude.

**What the calibration proves (orthogonally to v2.3):** the accuracy criterion as written is epistemologically under-specified — it conflates "verifiable" and "plausible," and no single preamble can reliably separate them without either halo error or over-rejection. Escalation path (if R1 still < −0.12 in v2.3): rubric redesign, not more preamble tuning.

---

*End of PRE-REGISTRATION-v2.3.md — filed before implementation begins; calibration addendum added after judge dry-run but before benchmark.*
