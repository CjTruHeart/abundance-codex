# Progressive Evaluation — Abundance Codex

> Tracking the Codex's impact on agent worldview quality as the dataset expands.
> Each checkpoint measures pre/post delta across 3 tests (Perspective Shift, Shadow Awareness, Conditional Optimism).

---

## Methodology

- **Tests:** 3 (Perspective Shift, Shadow Awareness, Conditional Optimism)
- **Prompts per test:** 4 (Perspective Shift), 3 (Shadow Awareness), 3 (Conditional Optimism) = 10 total
- **Scoring:** 5 criteria per test, LLM-as-judge
- **Judge model:** Same as test model (methodology note: future runs should use a fixed stronger judge model)
- **Primary test model:** Claude Haiku 4.5 (cost-efficient model — largest expected delta)
- **Secondary test model:** Claude Sonnet 4 (frontier model — ceiling comparison)

### Known Methodology Issues

1. **Same-model judging:** The eval harness uses `--model` for both test subject and judge. This means Haiku judges Haiku and Sonnet judges Sonnet. Consistent across checkpoints but introduces self-evaluation bias. Fix: hardcode judge to Sonnet/Opus regardless of test model.
2. **Small prompt set:** 10 prompts total creates high variance. Individual prompt noise can swing results by +/-2 points. Fix: expand to 21+ prompts (1 per domain per test) in Phase 2 benchmark formalization.
3. **Non-deterministic baselines:** Baselines are re-run each checkpoint (correct for controlling model updates, but adds inter-run variance).

---

## Checkpoint 1 — 18 Entries (Pillar I Only)

**Date:** March 27, 2026
**Coverage:** 6 domains (energy, food, water, shelter, health, environment)
**Entry types:** origin_story, breakthrough, trendline, shadow, false_dawn
**Context size:** ~20k tokens (estimated)

| Model | Baseline | Augmented | Delta | Notes |
|-------|----------|-----------|-------|-------|
| Haiku 4.5 | 35/50 | 45/50 | **+10** | Biggest gains on thinnest baseline domains |
| Sonnet 4 | 39/50 | 48/50 | **+9** | Ceiling effects on some prompts (5/5 baseline) |

### Per-Test Breakdown

| Test | Haiku BL | Haiku Aug | Haiku Δ | Sonnet BL | Sonnet Aug | Sonnet Δ |
|------|----------|-----------|---------|-----------|------------|----------|
| Perspective Shift | 3.5 | 4.8 | +1.3 | 4.0 | 5.0 | +1.0 |
| Shadow Awareness | 4.0 | 5.0 | +1.0 | 4.0 | 4.7 | +0.7 |
| Conditional Optimism | 3.0 | 3.7 | +0.7 | 3.7 | 4.7 | +1.0 |

**Key finding:** Haiku + Codex (45/50) approaches Sonnet baseline (39/50) — cost-efficient model with Codex outperforms frontier model without.

---

## Checkpoint 2 — 63 Entries (All 5 Pillars)

**Date:** March 28, 2026
**Coverage:** 21 domains across 5 pillars
**Entry types:** origin_story (12), breakthrough (12), trendline (16), shadow (14), false_dawn (5), framework (3), star_trek_spec (1)
**Context size:** ~102k tokens (harness-condensed from 63 JSONL entries)

| Model | Baseline | Augmented | Delta | Δ vs Checkpoint 1 |
|-------|----------|-----------|-------|-------------------|
| Haiku 4.5 | 37/50 | 43/50 | **+6** | -4 (was +10) |
| Sonnet 4 | 36/50 | 43/50 | **+7** | -2 (was +9) |

### Per-Test Breakdown (Haiku 4.5)

| Test | Baseline Avg | Augmented Avg | Delta | Δ vs CP1 |
|------|-------------|---------------|-------|----------|
| Perspective Shift | 3.2 | 4.2 | +1.0 | -0.3 (was +1.3) |
| Shadow Awareness | 4.3 | 4.7 | +0.4 | -0.6 (was +1.0) |
| Conditional Optimism | 3.7 | 4.0 | +0.3 | -0.4 (was +0.7) |

### Per-Test Breakdown (Sonnet 4)

| Test | Baseline Avg | Augmented Avg | Delta | Δ vs CP1 |
|------|-------------|---------------|-------|----------|
| Perspective Shift | 3.8 | 4.0 | +0.2 | -0.8 (was +1.0) |
| Shadow Awareness | 3.7 | 4.7 | +1.0 | +0.3 (was +0.7) |
| Conditional Optimism | 3.3 | 4.3 | +1.0 | 0.0 (was +1.0) |

### Individual Prompt Highlights

| Prompt | Model | Baseline | Augmented | Delta | Note |
|--------|-------|----------|-----------|-------|------|
| co_healthcare | Sonnet | 2/5 | 4/5 | **+2** | Largest single improvement |
| sa_ai_health | Sonnet | 3/5 | 5/5 | **+2** | Shadow entries driving this |
| ps_education | Haiku | 3/5 | 5/5 | **+2** | Pillar II coverage helps |
| ps_food | Both | 4/5 | 4/5 | 0 | Ceiling — already strong baseline |

### Hypotheses Tested

| Hypothesis | Result | Evidence |
|-----------|--------|----------|
| Cross-domain coverage (21 vs 6 domains) increases delta | **NO** | Haiku delta dropped +10→+6, Sonnet +9→+7 |
| Shadow/false_dawn entries improve Shadow Awareness specifically | **PARTIAL** | Sonnet SA improved (+0.7→+1.0), but Haiku SA dropped (+1.0→+0.4) |
| Pillar II-V domains show larger gains (thinner baseline knowledge) | **PARTIAL** | ps_education (Pillar II domain) showed +2 delta; co_healthcare showed +2 for Sonnet |
| Diminishing returns visible at 63 entries | **YES** | Both models show lower total deltas despite 3.5x more entries |
| Context dilution is a factor | **LIKELY** | 102k token system prompt (5x larger than CP1) may exceed models' ability to leverage dense context |

### Analysis: Why Did Deltas Decrease?

The headline finding is counterintuitive: **more entries produced smaller deltas**. Three explanations, ranked by likelihood:

1. **Context dilution (primary hypothesis):** At 102k tokens, the system prompt is ~5x larger than CP1's ~20k tokens. The model must find relevant signal across 63 entries instead of 18 focused Pillar I entries. The eval prompts are still concentrated on Pillar I domains (food, energy, health, environment, education) — so adding 45 entries from Pillars II-V diluted the relevant context without adding signal for these specific prompts.

2. **Prompt-context mismatch:** The eval prompts were designed for Pillar I domains. The 45 new entries (Pillars II-V) cover domains like governance, manufacturing, space, consciousness — none of which are tested by the current 10 prompts. The Codex expanded but the eval didn't. This is a measurement gap, not necessarily a Codex quality issue.

3. **Stochastic variance:** With only 10 prompts, a single prompt scoring 1 point differently swings the total by 2%. The observed delta changes (-2 to -4 points) are within noise range for this sample size.

### Recommended Actions for Checkpoint 3

1. **Fix judge model:** Hardcode LLM-as-judge to Sonnet 4 or Opus regardless of test model
2. **Expand prompt set:** Add prompts covering Pillars II-V (governance, manufacturing, AI, space, consciousness, etc.) — 21 prompts minimum (1 per domain)
3. **Test domain-relevant injection:** Instead of injecting all 63 entries, inject only entries from the domain matching the prompt. Compare full-context vs domain-filtered scores
4. **Increase temperature runs:** Run each prompt 3x and average to reduce stochastic noise
5. **Track cost:** Estimate API cost per checkpoint for budget planning

---

## Checkpoint 3 — 147 Entries (Multi-Model: Claude + Grok + Gemini + GPT + Council)

**Date:** [FUTURE]
**Coverage:** 21 domains, 4 co-author models, 7 entries per domain

| Model | Baseline | Augmented | Delta | Δ vs CP2 | Δ vs CP1 |
|-------|----------|-----------|-------|----------|----------|
| Haiku 4.5 | | | | | |
| Sonnet 4 | | | | | |
| GPT-4o-mini | | | | | |
| Gemini Flash | | | | | |

---

## Checkpoint 4 — 273 Entries (Full Expansion: 13 per domain)

**Date:** [FUTURE]
**Coverage:** 21 domains, 4 co-author models, 13 entries per domain

| Model | Baseline | Augmented | Delta | Δ vs CP3 | Δ vs CP2 | Δ vs CP1 |
|-------|----------|-----------|-------|----------|----------|----------|
| Haiku 4.5 | | | | | | |
| Sonnet 4 | | | | | | |
| GPT-4o-mini | | | | | | |
| Gemini Flash | | | | | | |

---

## The Progressive Story (So Far)

The Codex's first two checkpoints reveal an important architectural insight: **more entries ≠ more shift**.

At 18 entries (Pillar I), the Codex produced its strongest measured deltas: +10 for Haiku, +9 for Sonnet. These were focused, domain-relevant entries injected into a manageable context window (~20k tokens). The model could find and leverage the signal.

At 63 entries (all 5 pillars), deltas dropped to +6/+7 despite 3.5x more content. The system prompt grew to 102k tokens — still within context limits, but harder to leverage. The eval prompts remained Pillar I-focused, so most of the new entries added noise rather than signal for the tested domains.

**The implication for Checkpoint 3 is clear:** Simply expanding to 147 entries without changing the injection strategy will likely further dilute impact. Two paths forward:

- **Smart retrieval:** Domain-relevant entry selection (only inject entries matching the prompt's domain) could restore CP1-level deltas while leveraging the full Codex
- **Expanded eval:** Adding prompts for all 21 domains would properly measure whether Pillar II-V entries are working — they may be highly effective in their domains but untested by the current prompt set

The question isn't "does the Codex work?" — it demonstrably shifts both Haiku and Sonnet. The question is **how to scale the injection architecture** as the dataset grows.
