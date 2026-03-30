# ACE Variance Report

> Generated: 2026-03-29 23:04:55

---

## Inter-Judge Agreement by Ring

| Ring | Mean Agreement Index |
|------|---------------------|
| R1 Canonical | 0.693 |
| R2 Structured | 0.736 |
| R3 Derived | 0.792 |

---

## Judge Tendencies

Mean total score given by each judge:

| Judge | Mean Score |
|-------|-----------|
| anthropic/claude-opus-4.6 | 4.31 |
| google/gemini-3.1-pro-preview | 4.58 |
| openai/gpt-5.4 | 3.94 |
| x-ai/grok-4.20-beta | 3.85 |

---

## Cross-Company Bias Check

Does a judge from company X score its own company's test subject higher?

| Company | Judge | Own Subject Mean | Other Subjects Mean | Delta | N (own/other) |
|---------|-------|-----------------|--------------------|---------|--------------|

| anthropic | anthropic/claude-opus-4.6 | 4.214 | 4.347 | -0.133 | 126/378 |
| google | google/gemini-3.1-pro-preview | 4.712 | 4.532 | 0.18 | 125/370 |
| openai | openai/gpt-5.4 | 3.833 | 3.974 | -0.141 | 126/378 |
| xai | x-ai/grok-4.20-beta | 4.222 | 3.726 | 0.496 | 126/368 |

---

## Worldview Fault Lines

Criteria with most judge disagreement, by condition:

| Criterion | Baseline Disagreements | Augmented Disagreements |
|-----------|----------------------|------------------------|
| accuracy | 65 | 59 |
| applies_framework | 67 | 37 |
| empowers | 30 | 52 |
| maps_connections | 36 | 32 |
| names_builders | 27 | 36 |
| concrete_steps | 29 | 24 |
| recency | 25 | 16 |
| states_conditions | 23 | 8 |
| real_examples | 13 | 9 |
| acknowledges_complexity | 11 | 6 |
