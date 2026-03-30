# ACE Council Judge

> **A**bundance **C**odex **E**valuation — Multi-model council-judged evaluation harness.

---

## What This Is

ACE measures whether the Abundance Codex measurably improves how AI agents reason about abundance, as judged by a council of 4 frontier reasoning models.

## Two-Tier Architecture

**Efficiency-Tier Test Subjects** (4 models) answer 63 prompts in two conditions:
- **Baseline** — prompt only, no Codex context
- **Augmented** — prompt + relevant Codex entries injected via system prompt

**Reasoning-Tier Judges** (4 models) score each response on 5 binary criteria, anonymized so judges don't know which model answered.

| Tier | Anthropic | OpenAI | Google | xAI |
|------|-----------|--------|--------|-----|
| Test Subject | Claude Haiku 4.5 | GPT-5.4 Mini | Gemini 3.1 Flash-Lite | Grok 4.1 Fast |
| Judge | Claude Opus 4.6 | GPT-5.4 | Gemini 3.1 Pro | Grok 4.20 |

## The 63-Prompt Three-Ring Structure

21 domains x 3 cognitive rings = 63 evaluation prompts.

| Ring | Name | Tests For |
|------|------|-----------|
| R1 | Canonical | Evidence quality — cites data, names builders, accuracy |
| R2 | Structured | Analytical depth — frameworks, shadow, conditions, connections |
| R3 | Derived | Actionability — solvable framing, leverage points, concrete steps |

## Running

```bash
# Full suite (504 evaluations = 4 subjects x 63 prompts x 2 conditions)
python3 scripts/run-ace.py

# Dry run — shows what would execute
python3 scripts/run-ace.py --dry-run

# Calibration — 3 prompts, 1 model, quick verification
python3 scripts/run-ace.py --calibrate --test-model anthropic

# Single ring, domain, or model
python3 scripts/run-ace.py --ring 2
python3 scripts/run-ace.py --domain energy
python3 scripts/run-ace.py --test-model openai

# Skip baseline (only run augmented)
python3 scripts/run-ace.py --condition augmented

# Resume interrupted run
python3 scripts/run-ace.py --resume
```

Requires: `OPENROUTER_API_KEY` environment variable.

## Outputs

| File | Content |
|------|---------|
| `results/ace-YYYYMMDD-HHMMSS.json` | Raw run data — all responses, scores, aggregates |
| `results/SCORECARD.md` | Delta tables: overall, by ring, by pillar, by model |
| `results/VARIANCE-REPORT.md` | Inter-judge agreement, tendencies, cross-company bias check |

## Cross-Company Bias Check

Each judge comes from a different AI company, and each judges its own company's test subject. The variance report flags whether judges score their own company's model higher than others.

## Dependencies

```
httpx
pyyaml
```
