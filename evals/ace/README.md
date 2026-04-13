# ACE — Abundance Codex Evaluation

> A standalone, reproducible benchmark for whether the Abundance Codex measurably improves how AI agents reason about civilization-scale challenges.

v2.0 | Judge: `anthropic/claude-opus-4.6` | Corpus: 252 entries × 21 domains

See [METHODOLOGY.md](METHODOLOGY.md) for the full reproducibility reference.

---

## What ACE Measures

Four efficiency-tier test subjects answer 63 hand-written prompts (3 cognitive rings × 21 Grand Challenge domains) under two conditions:

- **Baseline** — prompt only, no Codex context
- **Augmented** — prompt + Codex entries retrieved by Dojo Retriever v1.0 and injected via system prompt

A single reasoning-tier judge (`anthropic/claude-opus-4.6`) scores each response on 5 binary criteria per ring, on anonymized text. The delta between augmented and baseline mean scores is the headline metric.

### v2.0 vs v1.0

v1.0 used a 4-judge blind council (Opus, GPT-5.4, Gemini 3.1 Pro, Grok 4.20) and revealed a measured Grok in-group bias of +0.50. v2.0 locks the judge to Opus only and compares against a v1.0 Opus-only rebaseline produced from the preserved v1.0 per-judge data. See [METHODOLOGY.md §0.1](METHODOLOGY.md#01-judge-selection-from-4-judge-council-to-opus-only).

## The Three Rings

| Ring | Name | Tests For |
|------|------|-----------|
| R1 | Canonical | Evidence quality — cites data, names builders, accuracy |
| R2 | Structured | Analytical depth — frameworks, shadow, conditions, connections |
| R3 | Derived | Actionability — solvable framing, leverage points, concrete steps |

## Running

```bash
# 1. Install dependencies
pip install -r evals/ace/requirements.txt

# 2. Set your OpenRouter API key
cp evals/ace/.env.example .env
# then edit .env and fill in OPENROUTER_API_KEY
export $(grep -v '^#' .env | xargs)

# 3. Dry run — preview retrieval for all 63 prompts, no API calls
python3 scripts/run-ace.py --dry-run

# 4. Calibration — 3 prompts, 1 model, ~$0.10–0.20
python3 scripts/run-ace.py --calibrate --test-model haiku-4.5

# 5. Full reproduction — 504 test responses + 504 judge calls, ~$5–11
python3 scripts/run-ace.py
```

### Useful flags

```bash
python3 scripts/run-ace.py --ring 2            # only R2 prompts
python3 scripts/run-ace.py --domain energy     # only energy-domain prompts
python3 scripts/run-ace.py --test-model gpt-5.4-mini
python3 scripts/run-ace.py --condition augmented   # skip baseline
python3 scripts/run-ace.py --resume            # resume from most recent run
python3 scripts/run-ace.py --config path/to/custom-config.yaml
```

Test-subject labels are defined in [config.yaml](config.yaml) and are how you select a single model via `--test-model`.

## Outputs

v2.0 runs land in `results/v2.0/`. v1.0 artifacts are preserved in `results/v1.0/`.

| File | Content |
|------|---------|
| `results/v2.0/ace-YYYYMMDD-HHMMSS.json` | Raw run data: responses, per-prompt Opus scores, retrieval metadata (incl. per-entry `co_author_model`), reproducibility SHAs |
| `results/v2.0/SCORECARD.md` | Delta tables with bootstrap 95% CIs: overall, by ring, by pillar, by model |
| `results/v2.0/AUTHORSHIP-MATRIX.md` | Test-model × author-model mean-delta matrix (produced by `scripts/ace-authorship-report.py`) |
| `results/v1.0/` | Original 4-judge council run, preserved for historical reference |
| `results/v1.0/SCORECARD-opus-only.md` | Opus-isolated rebaseline of v1.0 for judge-matched v1.0↔v2.0 comparison (produced by `scripts/ace-v1-opus-rebaseline.py`) |

## Cost Estimate

v2.0 full run: ~$5–11 at OpenRouter pricing (April 2026). Calibration: ~$0.10–0.20. See [METHODOLOGY.md §7.7](METHODOLOGY.md#77-cost-estimate) for the breakdown.

## Dependencies

See [requirements.txt](requirements.txt). Core: `httpx`, `pyyaml`, `jsonschema`.
