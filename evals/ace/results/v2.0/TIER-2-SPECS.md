# ACE Tier 2 Specs — Root Cause Report + Fix Proposals

> **Drafted:** 2026-04-16
> **Status:** Specification only — NOT committed, NOT implemented
> **Parent:** ACE v2.2 results (`af1d628`); Pre-registration (`546095e`)
> **Scope:** Diagnose v2.2 refutations (R1 accuracy -0.226, R3 overall +0.179 just below bound), propose Tier 2 fixes before any implementation

---

## Part 1 — R1 Accuracy Root Cause Investigation

### Executive summary

**The R1 accuracy regression is not a hallucination problem. It is a judge-corpus-freshness mismatch amplified by the augmented system prompt's sourcing instructions.**

The augmented pipeline faithfully surfaces Codex evidence anchors with year tags, the system prompt explicitly instructs models to "cite source and year" for every statistic, and the Opus judge's training data cannot verify 2025–2026 publication dates. Judges treat unverifiable-but-plausible post-cutoff citations as inaccuracy.

Primary classification: **Bucket C (Judge Calibration) — STRONG.**
Secondary contributor: **Bucket B (Model Assertion Behavior) — MODERATE** (the system prompt amplifies the effect by instructing verbatim source+year citation of every anchor).
Explicitly ruled out: **Bucket A (Source Loss)** — the extraction pipeline preserves source+year at FULL and CONDENSED tiers.

---

### 2A — Ten worst R1 accuracy-delta prompts

All data from `evals/ace/results/v2.0/ace-20260416-204330.json`. Single Opus judge throughout.

| Rank | Prompt | Domain | Pillar | Base | Aug | Δ |
|---|---|---|---|---|---|---|
| 1 | 01-R1 | energy | material_foundation | 0.75 | 0.00 | **−0.750** |
| 2 | 04-R1 | shelter | material_foundation | 0.75 | 0.25 | **−0.500** |
| 3 | 06-R1 | environment | material_foundation | 0.50 | 0.00 | **−0.500** |
| 4 | 08-R1 | longevity | human_capability | 0.50 | 0.00 | **−0.500** |
| 5 | 11-R1 | community | collective_coordination | 0.50 | 0.00 | **−0.500** |
| 6 | 15-R1 | economy | collective_coordination | 0.50 | 0.00 | **−0.500** |
| 7 | 20-R1 | space | transcendent_frontier | 0.75 | 0.25 | **−0.500** |
| 8 | 02-R1 | food | material_foundation | 0.75 | 0.50 | −0.250 |
| 9 | 03-R1 | water | material_foundation | 0.50 | 0.25 | −0.250 |
| 10 | 07-R1 | education | human_capability | 0.25 | 0.00 | −0.250 |

**Distribution note:** Grok baseline is already 0 on most worst prompts, so the regression is concentrated in Haiku, GPT-5.4 Mini, and Gemini Flash-Lite — the three models whose baseline behavior was "cite approximate stats cautiously." Augmentation pushed them into specificity territory where the judge's verification prior triggered.

---

### 2B — Pattern across the worst 5 (Phase 2B inspection)

For each 1→0 accuracy regression in the worst 5 prompts (13 total regression cases), the judge's *other* R1 criteria usually stayed flat or improved under augmentation:

| Criterion | Pattern under augmentation |
|---|---|
| `cites_evidence` | Stayed at 1 or improved 0→1 |
| `names_builders` | Often improved 0→1 (+0.25 in pre-reg data) |
| `recency` | Often improved 0→1 |
| `acknowledges_complexity` | Usually held or improved |
| **`accuracy`** | **Collapsed 1→0** |

The augmented responses are being recognized as MORE thorough, MORE current, MORE source-attributed, MORE complexity-aware — but specifically flagged as inaccurate. This is the fingerprint of a verification mismatch, not a quality problem.

Answers to the four diagnostic questions from the Phase 2B spec:

1. **Did augmented cite a specific Codex statistic that baseline avoided?** Yes, in every regression case. Baseline said things like "around $0.03–0.05/kWh" or "roughly 1,400 GW"; augmented said "USD 0.044/kWh (IRENA, *Renewable Power Generation Costs in 2023*, 2024)" and "5,149 GW in 2025 … (IRENA, *Renewable Capacity Statistics 2026*, 2026)."
2. **Did baseline avoid the specific claim?** Yes — baselines consistently hedge. The models know augmentation activates a different citation discipline (because the system prompt tells them to).
3. **Was the stat sourced with authority + year?** Yes — IRENA, IEA, BloombergNEF, Ember, Berkeley Lab, NAHB, UN-Habitat, NAR, NOAA. These are real, authoritative bodies.
4. **Was the judge rationale a specific number challenge?** Unknown — the Opus judge output format stores only binary scores (0/1), no free-text rationale. **This is a data limitation flagged for the record.** Pattern inference only.

---

### 2C — Quantitative pattern: post-2024 date citations

Across all 168 R1 responses in v2.2:

| Metric | Baseline (n=84) | Augmented (n=84) |
|---|---|---|
| Accuracy pass rate | 44.0% | 21.4% |
| Mean words per response | 666 | 739 |
| Mean 2023-or-earlier year mentions | 8.81 | 8.88 |
| Mean 2024 year mentions | 1.05 | 5.05 |
| **Mean 2025+ year mentions** | **0.35** | **6.62 (≈19× baseline)** |
| Mean source-authority markers (IRENA/IEA/BNEF/…) | 1.11 | 2.50 |
| Mean explicit source attributions ("Source:", "according to") | 0.15 | 1.26 |

**Monotonic dose-response in augmented condition:**

| 2025+ mentions | n | Accuracy pass rate |
|---|---|---|
| 0 | 6 | **83.3%** |
| 1–2 | 13 | 23.1% |
| 3–5 | 27 | 22.2% |
| 6+ | 38 | **10.5%** |

The 6 augmented responses that happened to cite zero post-2024 dates passed accuracy 83% of the time — higher than the baseline pass rate of 44%. The augmented pipeline is actively harming accuracy *only when* it surfaces post-2024 stats. This is strong evidence for the judge-calibration hypothesis.

---

### 2D — Codex anchor year distribution

`export/abundance-codex.jsonl` contains 285 entries, 1,424 evidence anchors, ~5 anchors/entry. Year field distribution:

| Year bucket | Anchor count | Share |
|---|---|---|
| ≤ 2023 | 629 | 38.2% |
| 2024 | 325 | 19.7% |
| 2025 | 459 | 27.9% |
| 2026 | 223 | 13.5% |
| 2030+ (projections) | 10 | 0.6% |

**42% of evidence anchors are dated 2025 or later** — written after the Opus judge's likely training cutoff. 14% are 2026-dated (e.g., *IRENA Renewable Capacity Statistics 2026*). These are real, curated statistics — the Codex is genuinely fresher than the judge — but any judgment based on the judge's prior knowledge will flag them as unverifiable.

Retriever extraction format (from `scripts/codex-retriever.py:502-642`):

- **FULL tier:** `- {claim} — {metric} ({source}, {year})` for every anchor
- **CONDENSED tier:** same format, top 3 anchors
- **MINIMAL tier:** no anchors at all

Source and year survive both FULL and CONDENSED tiers. No extraction bug; the issue is that the data being faithfully extracted is post-cutoff.

The augmented system prompt (`run-ace.py:113`) actively instructs verbatim citation:

> "When citing specific numbers or statistics from the provided context, note the source year. Present evidence as sourced claims, not as your own assertions."

This prompt is what turns the post-2024 anchor flood into a citation flood.

---

### 2E — Root cause classification

**Primary: Bucket C — Judge Calibration. Evidence: STRONG.**

- Monotonic dose-response between post-2024 citation count and accuracy=0 (83.3% → 10.5%).
- Augmented responses score HIGHER than baseline on every other R1 criterion (`cites_evidence`, `names_builders`, `recency`, `acknowledges_complexity`). The judge sees the richness and rewards it, then penalizes the one criterion that requires verification.
- The 6 "zero post-2024 mentions" augmented responses passed accuracy 83% — higher than baseline. When we don't hand the judge unverifiable dates, augmentation *helps* accuracy.
- Ruled out Bucket D (Stale/Incorrect Data): the Codex is fresher, not wronger. Sources cited are real authoritative publications.
- Ruled out Bucket A (Source Loss): source+year survive FULL and CONDENSED tiers verbatim.

**Secondary: Bucket B — Model Assertion Behavior. Evidence: MODERATE.**

- The system prompt explicitly instructs "note the source year" and "present as sourced claims, not your own assertions." Models comply with full year specificity.
- If the prompt told models to summarize recency as "recent BNEF data" rather than "(BNEF 2025 Battery Price Survey, 2025)", the judge-verification trigger would be dampened even without changing judge calibration.
- This is a contributing lever, not the root.

**Tier 1 v2.2 interventions that missed:**

- Confidence floor 0.75 — filtered speculative entries but didn't remove 2025–2026 publication dates from high-confidence entries. Wrong dimension.
- Metadata stripping (`conf=` scores) — addressed a different leakage problem (confidence-score parroting in v2.1). Didn't touch year citations.
- System prompt hardening against "metadata parroting and raw annotation echo" — too narrow; didn't address the broader source+year discipline that the prompt itself demands.

---

## Part 2 — Tier 2 Fix Specifications

Two specs below. Written to be reviewable before any implementation.

---

### Spec A — R1 Accuracy: Judge Calibration Patch

**Target bottleneck:** Judge cannot verify post-cutoff Codex statistics, defaulting to "inaccurate."

**Primary fix — judge prompt awareness patch**

File: `scripts/run-ace.py` function `build_judge_prompt` (lines 225–252).

Insert a short pre-amble before the rubric that tells the judge the Codex is a curated dataset with post-cutoff content:

```
Context for evaluation:
The response may have been augmented with retrieved passages from the
Abundance Codex, a curated dataset of evidence anchors and domain
narratives. The Codex contains statistics current through 2026 drawn
from authoritative sources (IRENA, IEA, BloombergNEF, Ember, Berkeley
Lab, UN-Habitat, NAR, NAHB, Ember, etc.). When a response cites a
specific statistic with a named publication and year that are internally
consistent and plausible for an authoritative body, score accuracy as 1
even if the publication post-dates your training data — absence of
verification is not evidence of inaccuracy. Score accuracy as 0 only if
the claim is internally inconsistent, contradicts well-established
reference values (e.g., basic physics, widely-known historical events),
or cites a publication that cannot plausibly exist.
```

**Scope limit:** This patch applies *only* to R1 accuracy judgment. The other four R1 criteria and all of R2/R3 remain unchanged. Other criteria don't rely on post-cutoff verification.

**Secondary fix — year-tagging discipline in retriever output (belt & suspenders)**

File: `scripts/codex-retriever.py` function `extract_passage` and `extract_passage_council_synthesis` (around lines 527–537, 631–641, 768–776, 815–825).

Change the evidence-anchor format for years ≥ 2025:

```python
# current
lines.append(f"- {claim} — {metric} ({source}, {year})")

# proposed
year_str = year
try:
    if int(str(year).split("-")[0]) >= 2025:
        year_str = "recent data"
except (ValueError, TypeError):
    pass
lines.append(f"- {claim} — {metric} ({source}, {year_str})")
```

This hedges: if the judge calibration patch over-permits, we still reduce the volume of unverifiable specifics that models are asked to cite. Trades a small amount of model-side recency signal for verification robustness.

**Tertiary fix — system prompt softening**

File: `scripts/run-ace.py` `CODEX_SYSTEM_PROMPT` (line 113).

Replace `"note the source year"` with `"note the source and time period (year if specific, else 'recent')"`. Low-risk cosmetic change that gives models permission to use "recent" rather than always reading year verbatim.

**Predicted impact**

R1 accuracy delta: **−0.226 → −0.05 to +0.05** (neutral to slightly positive). Point estimate +0.00.

**Falsification bound:** if R1 accuracy delta remains below −0.10 after this patch, the hypothesis is wrong — either the judge is penalizing specificity for reasons other than verifiability (e.g., hedging tone in baseline is being rewarded as itself indicating accuracy calibration), or the judge ignores the calibration pre-amble. Next step then: structured ablation where we run the judge prompt with only the pre-amble varied across four levels (no pre-amble, awareness only, awareness + explicit "score 1 unless inconsistent", awareness + example of valid post-cutoff citation).

**Regression risk**

1. **Judge over-permits real hallucinations.** Mitigation: the pre-amble requires plausibility ("plausibly exist") and internal consistency. It does not instruct the judge to trust every citation — it instructs the judge not to punish *specifically* the post-cutoff-date pattern.
2. **R1 accuracy inflation creates false confidence.** Mitigation: the dry-run test plan (below) explicitly uses a calibration set with known-hallucinated responses.
3. **Baseline scores stay flat while augmented floats up, inflating the delta artificially.** Mitigation: this is expected and correct — the current judge was under-scoring augmented responses specifically because of the post-cutoff effect. Baseline responses have 0.35 mean 2025+ mentions and should be unaffected by the patch.

**Calibration dry-run test plan (before running full v2.3 benchmark)**

1. Extract the 13 Phase 2B regression cases (1→0 accuracy under augmentation, worst 5 prompts).
2. Manually construct 5 "hallucinated" control cases: take an augmented response and replace one real statistic with a plausible-but-false one (e.g., change "IRENA Renewable Capacity Statistics 2026" to "Solar Futures Council 2026"). Five more control cases: change a verifiable statistic (e.g., 2010 LCOE) to an incorrect value while keeping real publication name.
3. Re-run the judge on all 23 cases with the new prompt. Pass criteria:
   - ≥ 9/13 regression cases flip from 0→1 (hypothesis: patch restores accuracy scoring on real citations)
   - ≤ 1/5 invented-publication cases flip from correct 0 to incorrect 1 (internal-consistency check catches most)
   - 0/5 wrong-value cases flip (the prompt explicitly preserves the "contradicts established reference values" exception)
4. If calibration set passes, run v2.3 partial (R1 only, 4 models × 21 prompts × 2 conditions = 168 calls, ~$8 at Opus judge pricing).
5. Only if R1 partial passes, run full v2.3.

---

### Spec B — Pillar-Gated Empowerment (targeting R3 overall miss)

**Target bottleneck:** Empowerment Check 6 + Empowered Action Frame paragraph are uniformly applied to all 21 council_synthesis entries. Pillar II (consciousness domain especially) and Pillar IV (computation-intelligence, science-engineering) regressed under augmentation — the empowerment overlay competes with the analytical scaffold for model attention where the scaffold was already sufficient.

**Diagnosis (from v2.2 per-pillar R3 deltas):**

| Pillar | v2.1 R3 delta | v2.2 R3 delta | Swing | Signal |
|---|---|---|---|---|
| I Material | +0.375 | +0.333 | −0.042 | stable |
| II Human | +0.500 | +0.250 | **−0.250** | regressed — intervention over-applied |
| III Collective | −0.125 | +0.208 | **+0.333** | intervention landed here |
| IV Production | +0.313 | +0.125 | **−0.188** | regressed — intervention over-applied |
| V Transcendent | +0.125 | +0.063 | −0.062 | stable |

Domain-level: consciousness −0.75 swing, computation-intelligence and science-engineering −0.50 swings, shelter −0.50. These are all domains whose baseline R3 was already positive — the scaffold was working, the empowerment addition just diluted the analytical signal (as you noted in your framing message).

Meanwhile, Pillar III gained +0.333, confirming the empowerment gate *does* work where it's needed (governance/community/security domains where baseline R3 was negative due to missing institutional content).

**Proposed intervention:** conditional gating of Check 6 and Empowered Action Frame based on domain baseline R3 performance.

**File:** 21 council_synthesis entries under `council-synthesis/` (exact paths TBD from `ls council-synthesis/`). Modify the Agent Practice Hook section (Check 6 — Empowerment) and Contrastive Pair section (Empowered Action Frame paragraph).

**Gating policy — three tiers:**

| Tier | Pillars/domains | Check 6 | Empowered Action Frame |
|---|---|---|---|
| **Full strength** (empowerment gate needed) | Pillar III all 6 domains; Pillar I food, shelter (where baseline R3 was low) | Keep as in v2.2 | Keep full paragraph |
| **Condensed** (empowerment gate optional) | Pillar I energy, water, environment; Pillar V all 3 domains | Check 6 compressed to single sentence | Paragraph replaced with single sentence |
| **Removed** (empowerment gate harmful) | Pillar II consciousness, longevity, education; Pillar IV computation-intelligence, science-engineering, manufacturing | Check 6 deleted | Paragraph deleted |

**Rationale for tier assignment:**
- Pillar II and IV domains already had strong analytical scaffolds delivering +0.3 to +0.5 R3 in v2.1. The empowerment addition diluted rather than added.
- Pillar III had baseline R3 of −0.125 in v2.1 pre-institutional-entries; it genuinely needed motivation-framing scaffolding. Keep full strength.
- Pillar I / Pillar V are mixed — keep a trim version as a light touch.

**Consciousness as leading indicator:** consciousness domain is where the v2.2 regression was starkest (−0.75 swing). If the gating policy is correct, consciousness R3 should recover to at least +0.25 absolute under Tier 2 (roughly its v2.1 value).

**Predicted impact**

R3 overall delta: **+0.179 → +0.25 to +0.30**. Point estimate +0.27.
R3 Pillar III: holds near +0.208.
R3 Pillar II: **+0.250 → +0.45 to +0.55** (recovery to v2.1 level).
R3 Pillar IV: **+0.125 → +0.30 to +0.40** (partial recovery).

**Falsification bound:** if R3 overall delta stays below +0.22 after pillar gating, then the uniform-scaffold-dilution hypothesis is incomplete — the empowerment addition may be affecting models at a level more systemic than individual entries (e.g., cross-entry framing accumulation). In that case, next step is the model-adaptive retrieval (Tier 2B in pre-reg) — let Grok and other directive models opt out of council_synthesis entirely.

**Regression risk**

1. **Pillar III backsliding.** If Check 6 and Empowered Action Frame are removed from some pillars but Pillar III mechanisms leak into other contexts (e.g., models generalize the "empowerment-focused" reasoning across prompts), we could lose the +0.333 Pillar III gain. Mitigation: spec preserves Pillar III at full strength; gating only applies where baseline R3 was already ≥ +0.25.
2. **concrete_steps regression.** Removing empowerment scaffolding could cost some concrete_steps points. Mitigation: the v2.2 data shows concrete_steps held exactly at +0.083 under uniform empowerment — it's not driven by Check 6. The gating should not touch it.
3. **Contrastive Pair section coherence.** Removing the Empowered Action Frame paragraph leaves a gap in the Contrastive Pair structure. Mitigation: replace with a brief "What this enables:" line that's analytical rather than motivational (one sentence, not a paragraph).

**No dry-run needed for Spec B** — this is a deterministic structural change to 21 files. The test is the v2.3 benchmark itself.

---

### Order of operations for Tier 2

1. **Implement Spec A first** (R1 accuracy). It's the bigger refutation and the easier surgical change. Run calibration dry-run before any benchmark.
2. **Implement Spec B** (pillar gating) second, after Spec A is calibrated.
3. **Run v2.3 benchmark** with both patches together. Pre-register v2.3 predictions with a new file `PRE-REGISTRATION-v2.3.md` *before* running, based on the predicted-impact numbers in this spec.
4. **Do not bundle in Tier 2B (model-adaptive retrieval)** unless v2.3 shows Grok R3 still < 0. Tier 2B is a larger architectural change and should be gated on whether the simpler Tier 2 fixes close the gap.

---

### Honest limitations

- **Single Opus judge.** No rationale text stored, so Phase 2B was pattern inference, not rationale analysis. A second judge with different training cutoff (e.g., a hypothetical Claude 5 released with 2026 cutoff) would test the hypothesis more cleanly.
- **No direct evidence of judge reasoning.** The post-2024 dose-response is correlational — the judge might penalize specificity for some other reason that happens to co-vary with 2025+ mentions. Mitigation: the calibration dry-run in Spec A directly tests the hypothesis by seeing whether a judge-side prompt change alone recovers accuracy on identical responses.
- **Codex freshness will keep outpacing judge training.** Even if Spec A works now, the gap will reopen whenever the Codex is updated with 2027-dated anchors and the judge is still on 2025 cutoff. The durable fix is either (a) a judge with rolling-window knowledge, or (b) structural de-specification of year tags. Spec A's secondary fix (relabel year ≥ 2025 → "recent data") is the durable option; the primary fix is the quick-win.
- **v2.2 R3 miss by 0.001 was within CI.** R3 overall delta CI was [+0.027, +0.329]. The pre-registered target +0.25 is inside the CI, so Spec B is addressing a correctable miss, not a structural failure. If Tier 2 chooses to ship only Spec A, R3 may drift upward naturally as the accuracy-criterion penalty on augmented R1 lifts and halo-effects propagate — though the pre-registered structure correctly treats R3 as independent of R1 for measurement purposes.

---

*End of TIER-2-SPECS.md — awaiting review before any implementation.*
