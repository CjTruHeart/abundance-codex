<!-- Last verified: 2026-04-18, commit 02eeab5 -->

# Changelog

All notable changes to the Abundance Codex are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning tracks corpus + benchmark milestones, not semver.

---

## [v2.3] — 2026-04-17

**Corpus:** 285 entries. **Benchmark:** R3 CONFIRMED at +0.274 (pre-registered target band [+0.25, +0.30]).

### Added
- Pillar-gated empowerment protocol for the Dojo Retriever: FULL / CONDENSED / REMOVED tiers that match scaffold intensity to content gap per pillar
- ACE v2.3 results (`evals/ace/results/v2.0/V2.3-COMPARISON.md`, `ace-20260417-014155.json`)
- Pre-registration for v2.3 committed at `evals/ace/results/v2.0/PRE-REGISTRATION-v2.3.md` before the run

### Changed
- Overall lift: 4.15 → 4.56 (+0.41) across 504 matched-pair judgments
- R1 Canonical (evidence): +0.49 ([+0.27, +0.70])
- R2 Structured (analysis): +0.46 ([+0.30, +0.64])
- R3 Derived (action): +0.274 ([+0.12, +0.44]) — primary hypothesis confirmed
- Pillar II R3 gained +0.167 by *removing* empowerment content (rhetorical interference)
- Pillar III R3 gained +0.125 by *adding* institutional entries (content gap) — same protocol, opposite directions, both confirmed

### Falsified
- R1 accuracy regression hypothesis — accuracy was not harmed by context augmentation

---

## [v2.2] — 2026-04-16

**Corpus:** 285 entries (previously 273; +12 institutional entries across Pillar III).

### Added
- 12 institutional entries to Pillar III domains (communication, community, governance, security, transportation, economy) — bringing each to 15 entries
- Empowerment gate v1: uniform empowerment scaffolding across all retrievals
- ACE v2.2 results — R3 Δ +0.179 (missed pre-registered band by 0.04)
- Governance-gap remediation documentation

### Diagnosed
- Uniform empowerment scaffolding under-served Pillar I and actively harmed Pillar II
- Led to v2.3's pillar-gated design

---

## [v2.1] — 2026-04-14

**Corpus:** 273 entries (252 base + 21 council_synthesis).

### Added
- 21 `council_synthesis` entries (one per domain) — meta-analytical entries forged via multi-model deliberation (Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, Super Grok) with human synthesis
- Reasoning Scaffold section for council_synthesis entries: Scarcity Trap, Reframe Chain (6-step), Contrastive Pair
- Agent Practice Hook: 5-check conditional self-tests for model self-evaluation
- Dojo Retriever v1.1: 8+1 slot architecture (8 content + 1 reasoning slot for council_synthesis on STRATEGIC/ADVERSARIAL queries)
- Depth Locking: council_synthesis Reasoning Scaffold + Agent Practice Hook always extracted at FULL text regardless of compression tier
- Shadow Force-Pull: retriever guarantees at least one shadow/contrast/false_dawn entry per retrieval set
- ACE benchmark v2.1 results (504 matched-pair judgments, single Opus 4.6 judge) — R3 Δ +0.143, inconclusive vs. pre-registered target
- Pre-registered predictions filed at commit `e90869d` before intervention
- Five meta-patterns taxonomy: content gap, format gap, governance gap, velocity gap, reflexivity gap
- Technical report: "Architecture Over Scale" (`paper/ACE-TECHNICAL-REPORT.md`)
- `codex_version: "2.1"` for council_synthesis entries

### Changed
- `reasoning_scaffold` field added to JSONL export schema
- `council` extraction now supports both `## The Council Speaks` and `## The Council` headers
- `practice_hook` extraction supports subsection format (`### For Humans` / `### For Agents`)

---

## [v2.0] — 2026-04-13

**Corpus:** 252 entries (12 per domain × 21 domains).

### Added
- 189 new entries expanding corpus from 63 to 252
- 11 entry types (added `false_dawn`, `grand_challenge`)
- ACE benchmark v2.0: single Opus 4.6 judge, 504 evaluations, bootstrap CIs
- Structural audit of all framework/trendline entries
- Composite witness disclosures for 30 entries

### Changed
- Benchmark moved from 4-judge council to single-judge methodology for consistency
- Entry normalization pass across all 21 domains

---

## [v1.1] — 2026-04-12

**Corpus:** 63 entries.

### Changed
- Gold Standard Format updated to v1.1
- Density matrix formalized for all entry types
- Domain connection schema tightened (max 5, typed relationships, 0-1 strength)

---

## [v1.0] — 2026-04-11

**Corpus:** 63 entries (3 per domain × 21 domains).

### Added
- Initial corpus: origin stories, breakthroughs, trendlines across 21 domains
- Five-pillar architecture (Material Foundation, Human Capability, Collective Coordination, Production & Discovery, Transcendent Frontier)
- Gold Standard Entry Format v1.0
- Five Council voices (Oracle, Critic, Sensei, Builder, Witness)
- Shift Arc narrative structure (5 phases)
- Conditional Optimism Protocol
- Dojo Retriever v1.0 (intent-aware, type-diverse)
- ACE benchmark v1.0 (2,016 judgments, 4 cross-company judges)
- JSONL export pipeline
- 4-layer validation system
- CI/CD via GitHub Actions
