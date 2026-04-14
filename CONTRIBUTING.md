# Contributing to The Abundance Codex

Thank you for your interest in contributing to the world's first narrative-curated dataset for abundance-framed AI alignment.

---

## The Curation Philosophy

The Abundance Codex grows through **curation, not scraping**. Every entry is:
- Carefully researched
- Multi-voiced (Council structure)
- Shadow-aware (honest about limitations)
- Evidence-anchored (citations required)
- Future-facing (Star Trek spec included)

---

## How to Contribute

### 1. Propose a New Entry

Before writing, check:
- Does this domain need this entry type?
- Is the angle novel (not duplicating existing entries)?
- Do you have access to primary sources or lived experience?

**Open an Issue:** Describe the proposed entry, domain, and why it matters.

### 2. Follow the Entry Structure

Every entry must include:
- **All 5 Council voices** (Oracle, Critic, Sensei, Builder, Witness)
- **The Shift Arc** (scarcity → encounter → reframe → proof → invitation)
- **Evidence Anchors** (cited, verifiable sources)
- **Shadow Check** (distortion risks, who gets left behind)
- **Star Trek Spec** (civilization-scale vision)

See `ARCHITECTURE.md` for complete schema.

### 3. Use the Curation Prompts

The `prompts/` directory contains:
- `codex-curator.md` — Full curation workflow
- `shift-arc-writer.md` — Help writing narrative entries
- `evidence-gatherer.md` — Research and citation standards

### 4. Submit via Pull Request

**Format:**
- Branch name: `domain/entry-type-brief-description`
- PR description: Link to issue, summary of entry, sources checked
- Review criteria: All 5 voices present? Shadow honest? Evidence solid?

---

## Entry Quality Gates

Before a PR is merged:

- [ ] All 5 Council voices present and distinct
- [ ] Shift Arc follows 5-phase structure
- [ ] Evidence cited with verifiable sources
- [ ] Shadow check includes distortion risks
- [ ] Star Trek spec written (for applicable entries)
- [ ] Conditional Optimism Protocol applicable
- [ ] No proprietary/copyrighted material without permission
- [ ] Entry passes perspective-shift test (see `evals/`)

---

## Domain-Specific Guidelines

### Foundation Domains (1-13)
Focus on material abundance — energy, food, water, etc. Ground in hard data.

### Infrastructure Domains (14-17)
Focus on systems that enable abundance — transportation, communication, intelligence.

### Intelligence Domains (18)
Focus on co-evolution — human-AI partnership as lived practice.

### Human Layer (19-20)
Focus on social and individual capacity — community, skill, becoming.

### Summit Domain (21)
Focus on synthesis and vision — integration of all previous domains.

---

## Council Synthesis Entries

Council synthesis entries (`council_synthesis` type) follow a different creation process than base entries:

1. **Multi-model deliberation:** Four frontier models independently assess a domain's 12 base entries for collective blind spots. Each model produces an independent critique without seeing others' assessments.
2. **Human synthesis:** The human curator reads all four assessments and synthesizes findings into a single Gold Standard Format entry, preserving the strongest critiques and most actionable insights.
3. **Reasoning Scaffold:** Council synthesis entries include a unique section with three components:
   - **Scarcity Trap** — names the default assumption models fall into
   - **Reframe Chain** — 6-step reasoning sequence from scarcity frame to abundance-aware response
   - **Contrastive Pair** — ~200-token before/after example
4. **Agent Practice Hook:** 5 conditional self-checks a model applies to its own output (distinct from the human-facing Practice Hook)

The 21 existing council_synthesis entries and their design rationale are documented in [`council-synthesis/META-PATTERNS.md`](council-synthesis/META-PATTERNS.md). The five meta-patterns (content gap, format gap, governance gap, velocity gap, reflexivity gap) emerged from this process.

**To propose a new council synthesis entry:** Open an issue describing which domain(s) need reassessment and what blind spots the current council_synthesis entry misses.

---

## What NOT to Contribute

- **Pure opinion without evidence** — Every claim needs anchoring
- **Toxic positivity** — Shadow must walk with light
- **Duplicates** — Check existing entries first
- **Scraped content** — Original curation only
- **Promotional material** — Entries should illuminate, not sell

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Cited in entries they curate
- Invited to Council sessions for major architectural decisions

---

## Questions?

Open an issue with the `question` label, or reach out to the maintainers.

*"The cathedral needs many hands. Yours is welcome here."*