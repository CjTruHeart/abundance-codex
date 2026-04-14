# Changelog

All notable changes to the Abundance Codex are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning tracks corpus milestones, not semver.

---

## [v2.1] — 2026-04-14

**Corpus:** 273 entries (252 base + 21 council_synthesis)

### Added
- 21 `council_synthesis` entries (one per domain) — meta-analytical entries forged via multi-model deliberation (GPT-5.4 Mini, Claude Haiku 4.5, Gemini Flash-Lite, Grok 4.1 Fast) with human synthesis
- Reasoning Scaffold section for council_synthesis entries: Scarcity Trap, Reframe Chain (6-step), Contrastive Pair
- Agent Practice Hook: 5-check conditional tests for model self-evaluation
- Dojo Retriever v1.1: 8+1 slot architecture (8 content + 1 reasoning slot for council_synthesis on STRATEGIC/ADVERSARIAL queries)
- Extraction priority override: council_synthesis entries depth-locked at FULL for Reasoning Scaffold and Practice Hook
- ACE benchmark v2.1 results (504 matched-pair judgments, single Opus 4.6 judge)
- Pre-registered predictions filed at commit `e90869d` before intervention
- Five meta-patterns taxonomy: content gap, format gap, governance gap, velocity gap, reflexivity gap
- Technical report: "Architecture Over Scale" (`paper/ACE-TECHNICAL-REPORT.md`)

### Changed
- `reasoning_scaffold` field added to JSONL export schema
- `council` extraction now supports both `## The Council Speaks` and `## The Council` headers
- `practice_hook` extraction supports subsection format (`### For Humans` / `### For Agents`)

---

## [v2.0] — 2026-04-13

**Corpus:** 252 entries (12 per domain x 21 domains)

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

**Corpus:** 63 entries

### Changed
- Gold Standard Format updated to v1.1
- Density matrix formalized for all entry types
- Domain connection schema tightened (max 5, typed relationships, 0-1 strength)

---

## [v1.0] — 2026-04-11

**Corpus:** 63 entries (3 per domain x 21 domains)

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
