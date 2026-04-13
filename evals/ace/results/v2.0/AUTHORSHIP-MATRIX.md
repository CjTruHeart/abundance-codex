# ACE Authorship Matrix

> Generated: 2026-04-13T10:31:58.360978+00:00
> Source run: `evals/ace/results/v2.0/ace-20260413-103133.json`
> Judge: `anthropic/claude-opus-4.6`

This report measures whether the identity of the model that co-authored
a retrieved Codex entry correlates with how much the retrieval helped a
given test subject. It is **observational**, not causal — retrieval
composition is a side effect of Dojo Retriever ranking, not a controlled
variable. See METHODOLOGY.md §9.7.

---

## Cross-Authorship Matrix

Cells: mean (augmented − baseline) delta across prompts where that
author contributed ≥1 retrieved entry. `n` is prompt count.

| test_model \ author_model | chatgpt-5.4-thinking | claude-opus-4-6 | gemini-3.1-pro | grok-super | N prompts |
|---|---|---|---|---|---|
| anthropic/claude-haiku-4-5 | +0.49 (n=61) | +0.48 (n=63) | +0.48 (n=63) | +0.48 (n=63) | 63 |
| google/gemini-3.1-flash-lite-preview | +0.18 (n=61) | +0.22 (n=63) | +0.22 (n=63) | +0.22 (n=63) | 63 |
| openai/gpt-5.4-mini | +0.56 (n=61) | +0.52 (n=63) | +0.52 (n=63) | +0.52 (n=63) | 63 |
| x-ai/grok-4.1-fast | +0.11 (n=61) | +0.11 (n=63) | +0.11 (n=63) | +0.11 (n=63) | 63 |

---

## Mean Delta by Author (pooled over test models)

| author_model | mean delta | total observations |
|--------------|-----------|---------------------|
| chatgpt-5.4-thinking | +0.336 | 244 |
| claude-opus-4-6 | +0.333 | 252 |
| gemini-3.1-pro | +0.333 | 252 |
| grok-super | +0.333 | 252 |

---

## Same-Company vs Cross-Company Effect

For each test model, compare its mean delta on retrieved contexts
authored by its own company vs. contexts authored by other companies.
A positive `delta-of-deltas` is consistent with (but does not prove)
a same-company affinity effect.

| test_model | same-company author | same mean Δ | cross mean Δ | delta-of-deltas |
|------------|---------------------|------------|--------------|----------------|
| anthropic/claude-haiku-4-5 | claude-opus-4-6 | +0.476 | +0.481 | -0.005 |
| google/gemini-3.1-flash-lite-preview | gemini-3.1-pro | +0.222 | +0.209 | +0.014 |
| openai/gpt-5.4-mini | chatgpt-5.4-thinking | +0.557 | +0.524 | +0.034 |
| x-ai/grok-4.1-fast | grok-super | +0.111 | +0.112 | -0.001 |
