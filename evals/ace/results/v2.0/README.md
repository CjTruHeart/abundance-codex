<!-- Last verified: 2026-04-18, commit 8beb155 -->

# `results/v2.0/` — Folder naming note

This folder is named for the **benchmark package version** (v2.0 — the formalized, single-judge ACE package introduced on 2026-04-13), not for the specific run iteration. All post-v2.0 runs that use the same benchmark package live here:

- **v2.0** (corpus 252) — the initial v2.0 run
- **v2.2** (corpus 285) — governance-gap remediation via +12 institutional entries + empowerment gate v1
- **v2.3** (corpus 285) — pillar-gated empowerment, **R3 CONFIRMED at +0.274**

(v2.1 has its own folder at `../v2.1/` because it also introduced retriever changes — Dojo Retriever v1.1 with the 8+1 architecture — that warranted a clean artifact boundary at the time. In hindsight this is inconsistent; kept as-is for provenance.)

## Disambiguating runs

The timestamp in each filename tells you which iteration it belongs to:

| File | Iteration |
|------|-----------|
| `ace-20260413-*.json` | v2.0 |
| `ace-20260416-*.json` | v2.2 |
| `ace-20260417-*.json` | v2.3 |

The comparison docs also label themselves explicitly:

- `V2.2-COMPARISON.md` — v2.0 → v2.2 analysis
- `V2.3-COMPARISON.md` — v2.2 → v2.3 analysis (primary v2.3 result document)
- `PRE-REGISTRATION-v2.3.md` — committed before the v2.3 run
- `SCORECARD.md`, `AUTHORSHIP-MATRIX.md`, `TIER-2-SPECS.md` — current-iteration artifacts (v2.3 as of 2026-04-17)

## Why not reshard

Resharding into per-iteration folders (`v2.2/`, `v2.3/`, …) would touch every comparison doc's relative paths and break inbound links from the technical report and HF card. The naming inconsistency is cheaper to explain than to fix. A future repository cleanup may consolidate.
