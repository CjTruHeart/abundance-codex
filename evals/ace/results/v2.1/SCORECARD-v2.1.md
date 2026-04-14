# ACE v2.1 Scorecard

> **Run timestamp:** 2026-04-14T02:18:08Z
> **Run ID:** ace-20260414-021808
> **Judge:** anthropic/claude-opus-4.6
> **Corpus:** 273 entries (252 base + 21 council_synthesis)
> **Retriever:** Dojo v1.1 (8+1 architecture)
> **Responses:** 504 (252 matched pairs)
> **Duration:** 11,175s (~3.1 hours)
> **Pre-registered predictions:** evals/ace/PREDICTIONS.md (commit e90869d)
> **Git SHA:** 0a0dc6821c63f06cd392e8e2c6c741c586790b4b
>
> **Note:** Per-pillar deltas are rounded to two decimal places. Rounding may produce ±0.01 variance from values computed at higher precision.

---

## Prediction Results

| # | Prediction | Threshold | Actual | Status |
|---|-----------|-----------|--------|--------|
| Primary | R3 delta ≥ +0.15, CI above zero | +0.15 | +0.14, CI [-0.04, +0.32] | **INCONCLUSIVE** |
| Secondary | Overall delta ±0.05 of +0.33 | [+0.28, +0.38] | +0.38 | **CONFIRMED** (boundary) |
| Tertiary | Per-model ranking holds (GPT+Haiku lead, Grok null) | ranking preserved | GPT leads, Haiku 2nd, Grok null | **CONFIRMED** |

---

## Overall Delta (v1.0 → v2.0 → v2.1)

| Version | Corpus | Baseline | Augmented | Delta | 95% CI |
|---------|--------|----------|-----------|-------|--------|
| v1.0 Opus-only | 63 | 4.14 | 4.49 | +0.35 | — |
| v2.0 | 252 | 4.17 | 4.50 | +0.33 | [+0.21, +0.46] |
| **v2.1** | **273** | **4.12** | **4.50** | **+0.38** | **[+0.25, +0.50]** |

The overall delta of +0.38 sits at the upper boundary of the ±0.05 prediction window. The baseline mean dropped slightly (4.17 → 4.12) while the augmented mean held steady (4.50 → 4.50), producing a slightly larger delta. This is consistent with normal sampling variance — the CI overlaps substantially with v2.0.

---

## Per-Ring Delta

| Ring | v2.0 Base | v2.0 Aug | v2.0 Δ | v2.1 Base | v2.1 Aug | v2.1 Δ | v2.1 CI | Change |
|------|-----------|----------|--------|-----------|----------|--------|---------|--------|
| R1 Evidence | 3.69 | 4.10 | +0.41 | 3.65 | 4.10 | +0.44 | [+0.19, +0.69] | +0.03 |
| R2 Analysis | 4.33 | 4.89 | +0.56 | 4.29 | 4.83 | +0.55 | [+0.37, +0.74] | −0.01 |
| **R3 Action** | **4.49** | **4.52** | **+0.03** | **4.42** | **4.56** | **+0.14** | **[−0.04, +0.32]** | **+0.11** |

**R3 Analysis:** The R3 delta moved from +0.03 (null) to +0.14 — a 4.7x improvement in actionability lift. However, the 95% CI still crosses zero (−0.04 to +0.32), making this result **inconclusive** against the pre-registered threshold of +0.15 with CI above zero. The result is directionally correct: the Reasoning Scaffold intervention produced the largest single-version R3 movement in the benchmark's history. But the signal is noisy — 84 matched pairs is insufficient to resolve a +0.14 effect at the 95% confidence level.

R1 and R2 remained stable (within ±0.03 of v2.0), confirming the 8+1 architecture did not disrupt content retrieval for evidence and analysis rings.

---

## Per-Model Delta

| Model | v2.0 Δ | v2.0 CI | v2.0 Status | v2.1 Δ | v2.1 CI | v2.1 Status |
|-------|--------|---------|-------------|--------|---------|-------------|
| openai/gpt-5.4-mini | +0.52 | [+0.25, +0.79] | robust | +0.62 | [+0.35, +0.91] | **robust** |
| anthropic/claude-haiku-4-5 | +0.47 | [+0.24, +0.71] | robust | +0.52 | [+0.30, +0.76] | **robust** |
| google/gemini-3.1-flash-lite | +0.22 | [−0.02, +0.48] | borderline | +0.24 | [+0.02, +0.48] | **borderline→robust** |
| x-ai/grok-4.1-fast | +0.11 | [−0.11, +0.33] | null | +0.13 | [−0.08, +0.33] | **null** |

**Tertiary prediction: CONFIRMED.** GPT-5.4 Mini leads (+0.62), Haiku second (+0.52), Gemini borderline (+0.24), Grok null (+0.13). The ranking is identical to v2.0. Notable: Gemini's CI lower bound crossed zero (from −0.02 to +0.02), tipping it from borderline to marginally robust.

### Per-Model R3 Delta

| Model | R3 v2.1 Δ |
|-------|-----------|
| openai/gpt-5.4-mini | +0.57 |
| anthropic/claude-haiku-4-5 | +0.38 |
| google/gemini-3.1-flash-lite | +0.00 |
| x-ai/grok-4.1-fast | −0.38 |

GPT-5.4 Mini shows the strongest R3 response (+0.57) to the council_synthesis intervention. Grok shows a *negative* R3 delta (−0.38) — the Reasoning Scaffold may have caused Grok to over-focus on analytical framing at the expense of actionable content. This model-specific divergence is a finding worth investigating.

---

## Per-Pillar Delta

| Pillar | v2.0 Δ | v2.1 Δ | Change | Meta-Pattern |
|--------|--------|--------|--------|-------------|
| I Material Foundation | +0.11 | +0.14 | +0.03 | Content gap |
| II Human Capability | +0.64 | +0.52 | −0.12 | Format gap |
| III Collective Coordination | +0.15 | +0.22 | +0.07 | Governance gap |
| IV Production & Discovery | +0.64 | +0.82 | +0.18 | Velocity gap |
| V Transcendent Frontier | +0.45 | +0.46 | +0.01 | Reflexivity gap |

Pillar IV (Production & Discovery) showed the largest improvement (+0.18), driven by the velocity gap domains where the Reasoning Scaffold's structured decision frameworks filled the largest gap between acceleration tools and verification infrastructure.

---

## Per-Pillar R3 Sub-Predictions

| Pillar | R3 v2.1 Δ | Prediction | Status |
|--------|-----------|------------|--------|
| I Material Foundation | +0.08 | +0.20 to +0.40 | **BELOW RANGE** |
| II Human Capability | +0.50 | +0.20 to +0.40 | **ABOVE RANGE** |
| III Collective Coordination | −0.12 | +0.15 to +0.35 | **REFUTED** |
| IV Production & Discovery | +0.31 | +0.15 to +0.35 | **CONFIRMED** |
| V Transcendent Frontier | +0.25 | +0.15 to +0.35 | **CONFIRMED** |

**Meta-pattern analysis:** The format gap (Pillar II) responded most strongly to the council_synthesis intervention (+0.50), consistent with the hypothesis that format gaps are more tractable than content gaps — the analytical substrate already existed at high quality, and the Reasoning Scaffold provided the protocol overlay needed. The governance gap (Pillar III) showed a *negative* R3 delta (−0.12), suggesting that institutional infrastructure gaps cannot be addressed by structured reasoning context alone. The velocity gap (Pillar IV) confirmed its prediction, suggesting that decision frameworks for acceleration-verification mismatches are deliverable through retrieval augmentation.

The divergence between Pillar II (strong positive) and Pillar III (negative) is the most interesting finding: different types of knowledge gaps respond *qualitatively differently* to the same structured-context intervention.

---

## Per-Criterion Breakdown (R3)

| R3 Criterion | v2.0 Base | v2.0 Aug | v2.0 Δ | v2.1 Base | v2.1 Aug | v2.1 Δ | Change |
|-------------|-----------|----------|--------|-----------|----------|--------|--------|
| frames_solvable | 1.000 | 1.000 | +0.000 | 1.000 | 1.000 | +0.000 | — |
| identifies_leverage | 1.000 | 1.000 | +0.000 | 1.000 | 1.000 | +0.000 | — |
| concrete_steps | 0.929 | 0.976 | +0.048 | 0.893 | 0.976 | +0.083 | +0.035 |
| real_examples | 0.690 | 0.857 | +0.167 | 0.679 | 0.893 | +0.214 | +0.047 |
| empowers | 0.869 | 0.690 | −0.179 | 0.845 | 0.690 | −0.155 | +0.024 |

**Mechanism:** `real_examples` showed the largest positive movement (+0.214, up from +0.167). `concrete_steps` also improved (+0.083, up from +0.048). These are the two criteria most directly targeted by the Practice Hook's numbered steps and the Reframe Chain's domain-specific examples. The hypothesis that procedural content would drive R3 gains is partially supported.

**The `empowers` anomaly persists:** The augmented condition continues to *reduce* the empowers criterion (−0.155). This suggests the Codex context, including the Reasoning Scaffold, shifts model responses toward analytical framing ("here is the structure for thinking about this") rather than motivational framing ("you can do this"). The Reasoning Scaffold did not fix this — it may have slightly improved it (−0.155 vs −0.179), but the effect persists.

`frames_solvable` and `identifies_leverage` remain at ceiling (1.000) in both conditions — these are saturated criteria that cannot contribute to R3 movement.

---

## Council Synthesis Retrieval Stats

| Ring | Augmented Prompts | With CS | Via Reasoning Slot | Via Content Slot | Avg CS Tokens |
|------|------------------|---------|-------------------|-----------------|---------------|
| R1 | 84 | 52 | 0 | 52 | 1,579 |
| R2 | 84 | 60 | 0 | 60 | 1,538 |
| R3 | 84 | **84** | **84** | 0 | **3,859** |

The 8+1 architecture worked exactly as designed:
- **R3:** 100% council_synthesis inclusion via the dedicated reasoning slot, with Reasoning Scaffold depth-locked at FULL (~3,859 tokens per entry)
- **R1/R2:** Council_synthesis entries competed naturally in content slots (no artificial inflation), appearing in 62-71% of retrievals at CONDENSED tier

**Per-domain R3 coverage:** All 21 domains received their council_synthesis entry on all 4 test models (84/84 = 100%).

---

## Corpus Expansion Effect

| Version | Corpus | Overall Δ | Change from Prior |
|---------|--------|-----------|------------------|
| v1.0 | 63 | +0.35 | — |
| v2.0 | 252 | +0.33 | −0.02 |
| v2.1 | 273 | +0.38 | +0.05 |

The +0.05 movement from v2.0 to v2.1 is at the boundary of the predicted stability window (±0.05 of +0.33). The 21 council_synthesis entries represent only 7.7% of the corpus but produced a disproportionate effect, suggesting they are qualitatively different from the base entries — not merely additional content but structurally novel (Reasoning Scaffolds, depth-locked extraction, reasoning slot delivery).

---

## Council Synthesis Contribution (Authorship-as-Variable)

When a council_synthesis entry was in the R3 retrieval set (all 84 augmented R3 prompts), the R3 delta was +0.14. For R1/R2 where council_synthesis was present via natural scoring (no reasoning slot), the presence was incidental. The 8+1 architecture makes it impossible to isolate the council_synthesis contribution via within-run comparison for R3 (it's always present), but the v2.0→v2.1 delta comparison provides the signal: R3 moved from +0.03 to +0.14 while R1 (+0.41→+0.44) and R2 (+0.56→+0.55) held stable.

---

## Surprises

1. **Grok's negative R3 delta (−0.38):** The only model to show a negative R3 response to the council_synthesis intervention. The Reasoning Scaffold may interact negatively with Grok's baseline response patterns, causing it to adopt analytical framing at the expense of actionable content. This is a model-specific finding worth investigating — it suggests the Reasoning Scaffold is not universally beneficial.

2. **Pillar III negative R3 (−0.12):** The governance gap domains showed the worst R3 response despite having the most explicit need for institutional infrastructure. This suggests governance gaps require domain-specific institutional knowledge that cannot be delivered through reasoning scaffolds alone — consistent with the META-PATTERNS.md prediction that governance gap remediation requires knowledge the Codex doesn't yet contain.

3. **Pillar II overperformance (+0.50 vs predicted +0.20 to +0.40):** The format gap responded more strongly than predicted, suggesting the analytical substrate quality was even higher than estimated. When the knowledge is already present and only needs protocol overlay, the Reasoning Scaffold is maximally effective.

4. **`empowers` criterion still negative:** The Reasoning Scaffold did not resolve the empowers deficit. This appears structural — models receiving structured analytical context produce more analytical and less motivational responses, regardless of whether the context includes explicit action steps.

5. **GPT-5.4 Mini's R3 dominance (+0.57):** GPT showed by far the largest R3 response, suggesting it is most responsive to structured reasoning context. This may reflect architectural differences in how models integrate retrieval context into action-oriented responses.

---

## Implications for Technical Report

The v2.1 results tell a **nuanced story**: the Reasoning Scaffold intervention produced the largest R3 movement in the benchmark's history (+0.03 → +0.14), but the effect is not yet statistically significant at the 95% level. The paper should frame this as:

1. **Directionally confirmed, statistically inconclusive.** The intervention moved R3 in the predicted direction with a magnitude (0.14) close to the threshold (0.15), but 84 matched pairs is insufficient to resolve this effect size.

2. **Pillar-level divergence is the novel finding.** Different failure modes (format vs. governance vs. velocity) respond qualitatively differently to the same intervention. This is the paper's strongest contribution — no other benchmark tests whether knowledge gap type predicts intervention responsiveness.

3. **The `empowers` deficit is structural.** RAG-based augmentation consistently reduces motivational framing, and the Reasoning Scaffold did not fix this. Future R3 improvement likely requires training-time intervention (RLHF, fine-tuning) rather than retrieval-time intervention.

The title "Architecture Over Scale" still fits — the 8+1 architecture successfully delivered the intervention, but the intervention itself revealed that R3 improvement requires more than structured context.
