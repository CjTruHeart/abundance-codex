# ACE v1.0 vs v2.0 — Judge-Matched Comparison

> Generated: 2026-04-13T10:31:58.378474+00:00
> v1.0 source: `evals/ace/results/v1.0/ace-20260329-230455.json` (Opus-only rebaseline)
> v2.0 source: `evals/ace/results/v2.0/ace-20260413-103133.json`
> Both versions judged by: `anthropic/claude-opus-4.6`

---

## Overall Delta

| Version | Baseline | Augmented | Delta |
|---------|----------|-----------|-------|
| v1.0 Opus | 4.14 | 4.49 | +0.35 |
| v2.0 | 4.17 | 4.5 | +0.33 |

---

## By Ring

| Ring | v1.0 Δ | v2.0 Δ | diff |
|------|--------|--------|------|
| R1 | +0.5 | +0.41 | -0.09 |
| R2 | +0.52 | +0.56 | +0.04 |
| R3 | +0.02 | +0.03 | +0.01 |

---

## By Test Model

| Model | v1.0 Δ | v2.0 Δ | diff |
|-------|--------|--------|------|
| anthropic/claude-haiku-4-5 | +0.49 | +0.47 | -0.02 |
| google/gemini-3.1-flash-lite-preview | +0.2 | +0.22 | +0.02 |
| openai/gpt-5.4-mini | +0.59 | +0.52 | -0.07 |
| x-ai/grok-4.1-fast | +0.11 | +0.11 | +0.0 |

---

A materially different v2.0 delta from v1.0 Opus-only indicates that
expanding the corpus to 252 entries changed the retrieval quality
(the only other variable held constant). The Grok judge artifact is
eliminated in both rows so it cannot explain a difference.
