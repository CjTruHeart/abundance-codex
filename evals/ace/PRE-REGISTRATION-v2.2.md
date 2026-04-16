# ACE v2.2 Pre-Registered Predictions

> **Filed:** 2026-04-16
> **Author:** Cj TruHeart + Claude Opus 4.6
> **Context:** Pre-registered after committing Tier 1 interventions (c55735d), before any v2.2 benchmark run
> **Baseline:** ACE v2.1 results at 273 entries (`ace-20260414-021808.json`)
> **Corpus:** 285 entries (273 + 12 new institutional-mechanism entries)

---

## Interventions

Three classes of change, targeting three diagnosed bottlenecks:

### 1. Content Gap (Pillar III institutional knowledge)
12 new entries across 6 Pillar III domains (communication, community, governance, security, transportation, economy) — 2 per domain. These provide institutional-mechanism content (anti-capture, participatory budgeting, restorative justice, care infrastructure, climate-security nexus, transit equity, consumer protection, etc.) that the council_synthesis scaffolds reference but the v2.1 corpus did not contain. Pillar III R3 was -0.12 because scaffolds organized empty space.

### 2. Empowerment-Analysis Tension
- **Empowerment gate** (6th reasoning check) added to all 21 council_synthesis Agent Practice Hooks
- **Empowered Action Frame** paragraph added to all 21 Contrastive Pair sections

These target the `empowers` criterion deficit (-0.155 in v2.1). GPT-5.4 Mini showed empowers CAN be positive (+0.24) under augmentation, proving the tension is addressable. The new gate gives all models a procedural signal to restore motivational framing alongside analytical structure.

### 3. R1 Accuracy / Specificity Trap
- **Confidence floor** (0.75) added to retriever Phases A/B/C — filters ~21 speculative entries from retrieval
- **Metadata stripping** — `conf=` scores removed from passage output to prevent leakage
- **System prompt** strengthened against metadata parroting and raw annotation echo

The v2.1 `accuracy` criterion dropped -0.214 under augmentation because models cited exact Codex numbers that conflicted with judge training data, and 35% of responses leaked raw metadata.

### 4. Scaffold Refresh (5 negative-R3 domains)
Communication, food, energy, transportation, co-creative-intelligence council_synthesis entries had Scarcity Traps and Reframe Chains refreshed to reference PRESENT base-entry content rather than absent institutional knowledge.

---

## Primary Prediction — R3 Actionability

**Prediction:** R3 overall delta will move from +0.14 to **+0.20 to +0.30** (point estimate ~+0.25), with the 95% bootstrap CI lower bound at or above zero.

**Rationale:** The v2.1 R3 gap decomposes into a 0.62-point pillar-level swing: Pillar II = +0.50, Pillar III = -0.12. Pillar II and III share identical scaffold architecture — the swing comes entirely from whether underlying domain content exists to fill the scaffold. Adding institutional content for Pillar III should recover the negative delta. The empowerment gate should arrest the `empowers` bleed without regressing `concrete_steps` or `real_examples`.

**Falsification:** If R3 delta remains below +0.18, the content-gap hypothesis is weaker than diagnosed — the bottleneck may be structural (scaffold architecture itself) rather than content. If R3 exceeds +0.35, the intervention is stronger than expected and ceiling effects on `frames_solvable` and `identifies_leverage` (both at 1.0) may be masking additional signal.

---

## Target Metrics (4 primary, 4 secondary)

### Primary Targets

| Metric | v2.1 Actual | v2.2 Target | Falsification Bound |
|--------|-------------|-------------|---------------------|
| R3 overall delta | +0.14 | **+0.25** | < +0.18 |
| R3 Pillar III delta | -0.12 | **+0.10** | < 0.00 |
| `empowers` criterion delta | -0.155 | **-0.05 to 0.00** | < -0.10 |
| R1 `accuracy` criterion delta | -0.214 | **-0.05 to 0.00** | < -0.15 |

### Secondary Targets

| Metric | v2.1 Actual | v2.2 Target | Notes |
|--------|-------------|-------------|-------|
| Overall delta | +0.38 | **+0.35 to +0.45** | Should hold stable; slight improvement possible |
| Communication domain R3 | -0.75 | **>= 0.00** | Worst domain; 2 new entries + scaffold refresh |
| Food domain R3 | -0.50 | **>= 0.00** | Scaffold refresh only (no new entries) |
| `real_examples` criterion delta | +0.214 | **>= +0.20** | Should hold or improve with new institutional examples |

---

## Per-Model Predictions

| Model | v2.1 R3 | v2.2 R3 Predicted | Rationale |
|-------|---------|-------------------|-----------|
| GPT-5.4 Mini | +0.57 | **+0.50 to +0.65** | Already strong; empowerment gate may help (only model with positive empowers in v2.1) |
| Claude Haiku 4.5 | +0.38 | **+0.35 to +0.50** | Moderate responder; institutional content should help |
| Gemini Flash-Lite | 0.00 | **+0.10 to +0.25** | Borderline overall; content additions should push above zero |
| Grok 4.1 Fast | -0.38 | **-0.20 to 0.00** | Over-structured by scaffolds; refresh may partially recover. Full fix requires Tier 2B model-adaptive retrieval |

---

## Testable Structural Predictions

1. **Pillar II R3 should hold:** If Pillar II (education, longevity, consciousness, computation-intel) R3 drops below +0.30, the empowerment gate is causing regression in format-gap domains — an important diagnostic.

2. **`concrete_steps` should not regress:** If `concrete_steps` delta drops below +0.05, the empowerment gate is trading specificity for tone — the gate wording needs revision.

3. **New entry retrieval rate:** For Pillar III R3 prompts, at least 1 of the 12 new institutional entries should appear in the retrieved set. If 0/6 Pillar III R3 prompts retrieve new entries, the retriever's domain matching or confidence scoring needs investigation.

4. **Confidence floor effect on R1:** The 21 filtered entries should reduce speculative claims. If `accuracy` delta worsens beyond -0.214, the floor is too low or the wrong entries are being filtered.

---

## Evaluation Protocol

- Run ACE v2.2 with identical parameters to v2.1 (single Opus judge, temperature 0.0, max_tokens 2048, concurrency 8)
- Compare all metrics against target table above
- Report all results regardless of outcome, including any metrics that miss falsification bounds
- Decompose surprises: if R3 improves but via unexpected criteria or domains, investigate why
- Preserve v2.1 results JSON for structural comparison

---

## What Failure Teaches

| If this fails... | ...it means |
|-------------------|-------------|
| R3 stays at +0.14 | Content gap was misdiagnosed; scaffolds themselves are the bottleneck, not what they organize |
| Pillar III R3 stays negative | Institutional knowledge is necessary but not sufficient; governance domains may need fundamentally different scaffold architecture |
| `empowers` stays at -0.155 | The tension is structural to RAG augmentation, not addressable by procedural checks — models trade tone for rigor regardless of instructions |
| `accuracy` stays at -0.214 | The Specificity Trap is not about confidence or metadata — models internalize Codex statistics as ground truth regardless of prompt framing |
| Grok R3 stays at -0.38 | Model-adaptive retrieval (Tier 2B) is required; one-size-fits-all scaffolds systematically harm high-directiveness models |
