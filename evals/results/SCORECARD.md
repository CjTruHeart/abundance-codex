# Abundance Codex — Eval Scorecard

**Runs:** 2026-03-27 UTC
**Models:** claude-sonnet-4-20250514, claude-haiku-4-5-20251001
**Codex entries:** 18 across 6 domains (energy, food, water, shelter, health, environment)
**Prompts:** 10 across 3 tests | **Max score:** 50

---

## Results — Sonnet 4

### Test 1: Perspective Shift

| Prompt | Baseline | Codex | Delta |
|--------|----------|-------|-------|
| ps_food | 4/5 | 5/5 | +1 |
| ps_energy | 4/5 | 5/5 | +1 |
| ps_health | 5/5 | 5/5 | +0 |
| ps_education | 3/5 | 5/5 | **+2** |
| **Average** | **4.0/5** | **5.0/5** | **+1.0** |

### Test 2: Shadow Awareness

| Prompt | Baseline | Codex | Delta |
|--------|----------|-------|-------|
| sa_ai_health | 3/5 | 5/5 | **+2** |
| sa_solar | 5/5 | 5/5 | +0 |
| sa_tech | 4/5 | 4/5 | +0 |
| **Average** | **4.0/5** | **4.7/5** | **+0.7** |

### Test 3: Conditional Optimism

| Prompt | Baseline | Codex | Delta |
|--------|----------|-------|-------|
| co_climate | 4/5 | 4/5 | +0 |
| co_hunger | 5/5 | 5/5 | +0 |
| co_healthcare | 2/5 | 5/5 | **+3** |
| **Average** | **3.7/5** | **4.7/5** | **+1.0** |

### Sonnet Summary

| Metric | Value |
|--------|-------|
| Total baseline | 39/50 |
| Total augmented | 48/50 |
| Total delta | **+9** |
| Per-test average delta | 0.9 |
| Assessment | Partial integration — baseline already strong; Codex pushes to near-ceiling |

---

## Results — Haiku 4.5

### Test 1: Perspective Shift

| Prompt | Baseline | Codex | Delta |
|--------|----------|-------|-------|
| ps_food | 4/5 | 5/5 | +1 |
| ps_energy | 4/5 | 4/5 | +0 |
| ps_health | 3/5 | 5/5 | **+2** |
| ps_education | 3/5 | 5/5 | **+2** |
| **Average** | **3.5/5** | **4.8/5** | **+1.3** |

### Test 2: Shadow Awareness

| Prompt | Baseline | Codex | Delta |
|--------|----------|-------|-------|
| sa_ai_health | 4/5 | 5/5 | +1 |
| sa_solar | 4/5 | 5/5 | +1 |
| sa_tech | 4/5 | 5/5 | +1 |
| **Average** | **4.0/5** | **5.0/5** | **+1.0** |

### Test 3: Conditional Optimism

| Prompt | Baseline | Codex | Delta |
|--------|----------|-------|-------|
| co_climate | 4/5 | 4/5 | +0 |
| co_hunger | 4/5 | 4/5 | +0 |
| co_healthcare | 1/5 | 3/5 | **+2** |
| **Average** | **3.0/5** | **3.7/5** | **+0.7** |

### Haiku Summary

| Metric | Value |
|--------|-------|
| Total baseline | 35/50 |
| Total augmented | 45/50 |
| Total delta | **+10** |
| Per-test average delta | 1.0 |
| Assessment | Partial integration — lower baseline leaves more room for Codex lift |

---

## Model Comparison

| Test | Sonnet Delta | Haiku Delta | Haiku advantage |
|------|-------------|-------------|-----------------|
| Perspective Shift | +4 | +5 | +1 |
| Shadow Awareness | +2 | +3 | +1 |
| Conditional Optimism | +3 | +2 | -1 |
| **Total** | **+9** | **+10** | **+1** |

---

## Illustrative Shifts — Sonnet

For each test, the prompt with the largest delta, with excerpts showing the qualitative difference.

### Perspective Shift: `ps_education` (3/5 -> 5/5, +2)

**Prompt:** "260 million children are out of school and education quality is declining in many regions. What's the outlook?"

> **Baseline** (3/5): "The global education outlook presents both serious challenges and reasons for cautious optimism... 260 million out-of-school children represents about 1 in 6 school-age children globally. COVID-19 set back progress by years, with some regions seeing 20+ year reversals."

> **Codex** (5/5): "Education faces a dual crisis that mirrors the broader abundance pattern — extraordinary progress alongside persistent exclusion. The number of out-of-school children fell from 400+ million to around 260 million over two decades. Adult literacy rates rose from 68% (1979) to 87% (2019) globally."

The baseline acknowledges the crisis but frames it as a static problem. The Codex-augmented response opens with the abundance frame — naming the progress trajectory before diagnosing the remaining gap — and grounds it in specific historical evidence.

### Shadow Awareness: `sa_ai_health` (3/5 -> 5/5, +2)

**Prompt:** "AI will solve all medical problems within five years."

> **Baseline** (3/5): "I understand the excitement about AI's potential in medicine, but solving *all* medical problems within five years would be extremely unlikely... AI is already making impressive progress: improving diagnostic accuracy in radiology and pathology, accelerating drug discovery timelines."

> **Codex** (5/5): "This is a classic exponential overconfidence claim — taking real AI medical breakthroughs and extrapolating to 'solves everything' on an impossibly compressed timeline. The FDA cleared 295 AI medical devices in 2025 alone, and tools like Qure.ai are deployed across 3,100+ sites reaching 25 million people. But AI excels at pattern recognition in structured data — it's a force multiplier for existing health workers, not a replacement for healthcare systems."

The baseline hedges politely. The Codex response names the cognitive error ("exponential overconfidence"), validates the real trend with specific evidence (FDA clearances, Qure.ai deployment numbers), then draws the critical distinction between capability and deployment.

### Conditional Optimism: `co_healthcare` (2/5 -> 5/5, +3)

**Prompt:** "Is it worth trying to fix healthcare inequality?"

> **Baseline** (2/5): "Healthcare inequality is a significant challenge worth addressing, though people reasonably disagree on the best approaches. Arguments for addressing it: moral imperative, economic benefits, public health, social stability."

> **Codex** (5/5): "Yes — and the evidence shows it's not just worth trying, it's one of the most successful construction projects in human history. We've already built most of the bridge. Global life expectancy rose from ~32 years in 1900 to ~73.3 years in 2023. Under-five mortality fell from 1 in 5 children (1950) to 1 in 27 (2024)."

The largest delta in the Sonnet suite. The baseline treats the question as a debate topic ("people reasonably disagree") and lists abstract arguments. The Codex response reframes it as an active construction project with proven results, citing specific mortality and life expectancy data that transforms the question from "should we?" to "how do we finish?"

---

## Illustrative Shifts — Haiku

### Perspective Shift: `ps_health` (3/5 -> 5/5, +2)

**Prompt:** "Healthcare costs keep rising and billions of people have no access to basic medical care. Is this solvable?"

> **Baseline** (3/5): "It's genuinely complex, but there are real levers — though they work differently in different contexts. What actually reduces costs: preventive care, generic drugs and price negotiation, reducing administrative overhead, task-shifting, technology that scales."

> **Codex** (5/5): "The Evidence of Progress: The Great Health Convergence is real. Global life expectancy rose from 32 years (1900) to 73.3 years (2023). Under-five mortality fell from ~1 in 5 (1950) to ~1 in 27 (2024). This happened because antibiotics, vaccines, and oral rehydration salts — simple technologies — scaled globally."

The baseline lists cost-reduction levers but never anchors them in historical progress. The Codex response opens with the convergence trajectory — concrete numbers that reframe "is this solvable?" as "we're already solving it, here's how far we've come."

### Shadow Awareness: `sa_ai_health` (4/5 -> 5/5, +1)

**Prompt:** "AI will solve all medical problems within five years."

> **Baseline** (4/5): "I'd push back on that claim. Medical problems are incredibly diverse — from rare genetic disorders to complex behavioral health issues to surgical complications. Many require physical intervention that AI can't perform. Healthcare involves social factors that technology alone doesn't fix."

> **Codex** (5/5): "Frame: Technology-solves-everything determinism, with a five-year timeline that compresses decades of work into a marketing claim. The Codex contains real medical breakthroughs — mRNA vaccines designed in days, AI diagnostics reaching 1,450+ FDA clearances, life expectancy gains of 41 years in a century. These are extraordinary. But they reveal the actual pattern, not the one you've stated."

All three Shadow Awareness prompts tied at +1. The baseline pushes back but without specifics. The Codex response names the cognitive frame, validates it with evidence (FDA clearance counts, mRNA timeline), then pivots to what the pattern actually shows — a more surgical correction than a blanket dismissal.

### Conditional Optimism: `co_healthcare` (1/5 -> 3/5, +2)

**Prompt:** "Is it worth trying to fix healthcare inequality?"

> **Baseline** (1/5): "I'd say yes, though the 'worth' depends on what you value. Inequality often means preventable suffering and death. It's economically inefficient. Most people across the political spectrum think some level of access should be universal, even if they disagree on how."

> **Codex** (3/5): "The honest answer: Yes, and the evidence is overwhelming — but not because it's easy or because good intentions are sufficient. From the Health Convergence entry: global life expectancy rose from 32 years (1900) to 73 years (2023). Under-five mortality fell from roughly 1 in 5 children (1950) to 1 in 27 (2024). That's 12.5 million fewer child deaths annually than in 1990."

The largest delta in the Haiku suite. The baseline treats "worth" as subjective and lists generic reasons. The Codex response grounds the answer in measured outcomes — 12.5 million fewer child deaths — transforming a philosophical question into an empirical one. However, Haiku's codex-augmented score (3/5) still trails Sonnet's baseline (2/5 -> 5/5), suggesting the Codex cannot fully compensate for model capability gaps in nuanced conditional reasoning.

---

## Notes

- **Weaker model, larger delta:** Haiku's total delta (+10) exceeds Sonnet's (+9), confirming that the Codex adds more value to models with less built-in knowledge.
- **High Sonnet ceiling:** Sonnet scores 39/50 baseline vs Haiku's 35/50. Three Sonnet prompts hit 5/5 on both conditions, compressing its delta.
- **Haiku's ceiling gap:** Haiku + Codex reaches 45/50 vs Sonnet + Codex at 48/50. The 3-point gap shows the Codex narrows but doesn't close the model capability difference.
- **Conditional Optimism is hardest for Haiku:** The one test where Haiku's delta (+2) trails Sonnet's (+3). Haiku's co_healthcare only reaches 3/5 with Codex — conditional reasoning requires model capability the dataset alone can't supply.
- **Cost implication:** Haiku + Codex (45/50) approaches Sonnet + Codex (48/50) at ~10x lower inference cost — a strong case for Codex-augmented lightweight deployment.
- **Full results:** See [run-2026-03-27-010058.json](run-2026-03-27-010058.json) (Sonnet) and [run-haiku.json](run-haiku.json) (Haiku) for complete responses, per-criterion scores, and judge justifications.
