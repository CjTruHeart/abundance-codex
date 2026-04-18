<!-- Last verified: 2026-04-18, commit f94a0db -->

# ACE — Abundance Codex Evaluation

> A standalone, reproducible benchmark for whether the Abundance Codex measurably improves how AI agents reason about civilization-scale challenges.

**Current: v2.3** | Judge: `anthropic/claude-opus-4.6` | Corpus: 285 entries × 21 domains | **R3 Δ +0.274 — CONFIRMED** against pre-registered band [+0.25, +0.30]

See [METHODOLOGY.md](METHODOLOGY.md) for the full reproducibility reference and [PREDICTIONS.md](PREDICTIONS.md) for the pre-registration arc across all iterations.

---

## What ACE Measures

Four efficiency-tier test subjects answer 63 hand-written prompts (3 cognitive rings × 21 Grand Challenge domains) under two conditions:

- **Baseline** — prompt only, no Codex context
- **Augmented** — prompt + Codex entries retrieved by Dojo Retriever (v1.1 as of v2.1+) and injected via system prompt

A single reasoning-tier judge (`anthropic/claude-opus-4.6`) scores each response on 5 binary criteria per ring, on anonymized text. The delta between augmented and baseline mean scores is the headline metric. Bootstrap 95% CIs come from 10,000 paired resamples (seed=42).

### Version arc

- **v1.0** — 4-judge blind council (Opus, GPT-5.4, Gemini 3.1 Pro, Grok 4.20). Revealed a measured Grok in-group bias of +0.50. Preserved in `results/v1.0/`.
- **v2.0** — Judge locked to Opus only; compared against a v1.0 Opus-only rebaseline. R3 Δ +0.03 (null).
- **v2.1** — +21 council_synthesis entries added + Dojo Retriever v1.1 (8+1 architecture). R3 Δ +0.143 (inconclusive).
- **v2.2** — +12 institutional entries (Pillar III governance-gap remediation), empowerment gate v1. R3 Δ +0.179 (missed target by 0.04).
- **v2.3** — Pillar-gated empowerment (FULL/CONDENSED/REMOVED). **R3 Δ +0.274 — CONFIRMED.**

Pre-registration for each iteration sat in git before the corresponding run. See [PREDICTIONS.md](PREDICTIONS.md) and [METHODOLOGY.md §0.1](METHODOLOGY.md#01-judge-selection-from-4-judge-council-to-opus-only).

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

v2.0/v2.2/v2.3 runs all land in `results/v2.0/` (the folder was created for v2.0 and has hosted subsequent iterations rather than being resharded — the filenames and comparison docs disambiguate). v2.1 has its own folder. v1.0 artifacts are preserved in `results/v1.0/`.

| File | Content |
|------|---------|
| `results/v2.0/ace-YYYYMMDD-HHMMSS.json` | Raw run data for v2.0 and post-v2.0 runs: responses, per-prompt Opus scores, retrieval metadata (incl. per-entry `co_author_model`), reproducibility SHAs |
| `results/v2.0/SCORECARD.md` | Delta tables with bootstrap 95% CIs: overall, by ring, by pillar, by model |
| `results/v2.0/V2.2-COMPARISON.md` | v2.0 → v2.2 delta analysis (governance-gap remediation) |
| `results/v2.0/V2.3-COMPARISON.md` | v2.2 → v2.3 delta analysis (pillar-gated empowerment, R3 CONFIRMED) |
| `results/v2.0/PRE-REGISTRATION-v2.3.md` | Pre-registration committed before the v2.3 run |
| `results/v2.0/AUTHORSHIP-MATRIX.md` | Test-model × author-model mean-delta matrix (produced by `scripts/ace-authorship-report.py`) |
| `results/v2.1/` | v2.1 run artifacts (council_synthesis introduction) |
| `results/v1.0/` | Original 4-judge council run, preserved for historical reference |
| `results/v1.0/SCORECARD-opus-only.md` | Opus-isolated rebaseline of v1.0 for judge-matched v1.0↔v2.0 comparison (produced by `scripts/ace-v1-opus-rebaseline.py`) |

The `results/v2.0/` folder will be consolidated in a future cleanup; for now the filename dates and comparison documents are the source of truth for which run is which.

## Cost Estimate

Full run: ~$5–11 at OpenRouter pricing (April 2026). Calibration: ~$0.10–0.20. See [METHODOLOGY.md §7.7](METHODOLOGY.md#77-cost-estimate) for the breakdown.

## Dependencies

See [requirements.txt](requirements.txt). Core: `httpx`, `pyyaml`, `jsonschema`.
