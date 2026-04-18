<!-- Last verified: 2026-04-18, commit ec0515c -->

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

See [`GOLD-STANDARD-FORMAT.md`](GOLD-STANDARD-FORMAT.md) for the complete entry template and [`CURATION-GUIDE.md`](CURATION-GUIDE.md) for the step-by-step forging workflow. `ARCHITECTURE.md` covers the broader technical architecture.

### 3. Use the Curation Prompt

The `prompts/codex-curator.md` file contains the full curation workflow prompt used to co-author entries with AI models.

### 4. Run the Validators Before Submitting

```bash
python3 scripts/validate-entry.py path/to/your-entry.md
python3 scripts/validate-jsonl.py        # after re-running export-to-jsonl.py
```

Both validators run in CI on every push (`.github/workflows/validate.yml`).

### 5. Submit via Pull Request

**Format:**
- Branch name: `domain/entry-type-brief-description`
- PR description: Link to issue, summary of entry, sources checked
- Review criteria: All 5 voices present? Shadow honest? Evidence solid?

---

## Entry Quality Gates

Before a PR is merged:

- [ ] `scripts/validate-entry.py` passes (YAML, schema, content, cross-refs)
- [ ] All 5 Council voices present and distinct
- [ ] Shift Arc follows 5-phase structure
- [ ] Evidence cited with verifiable sources (source name + year + confidence score)
- [ ] Shadow check includes distortion risks, excluded populations, transition pain, falsifiability edge
- [ ] Star Trek spec written (for applicable entries)
- [ ] Conditional Optimism Protocol applicable
- [ ] No proprietary/copyrighted material without permission
- [ ] Entry passes qualitative sanity tests (see [`evals/evals.md`](evals/evals.md))

---

## Pillar-Specific Guidelines

The 21 domains are organized into five pillars. Contribution priorities differ per pillar.

### Pillar I — Material Foundation (01-06: energy, food, water, shelter, health, environment)
Ground every claim in measurable physical reality. Confidence scores in the 0.85–0.95 range; frontier research anchored in peer-reviewed sources. Builder voice dominant.

### Pillar II — Human Capability (07-09: education, longevity, consciousness)
Balance empirical trendlines with honest epistemic humility about what we don't yet measure well. Paradigm seeds welcome here.

### Pillar III — Collective Coordination (10-15: communication, community, governance, security, transportation, economy)
**Institutional focus.** This pillar's entries are +2 heavier than others (15 each) because governance-gap remediation required more institutional exemplars. New entries should surface working coordination mechanisms, not just the tech substrate.

### Pillar IV — Production & Discovery (16-19: manufacturing, computation-intelligence, co-creative-intelligence, science-engineering)
**Velocity-gap aware.** Entries should name the mismatch between acceleration tools and verification infrastructure. Shadow checks must engage the velocity dimension.

### Pillar V — Transcendent Frontier (20-21: space, future-vision)
**Reflexivity required.** These domains invite grand vision — the correction is structural critique of the vision. Every star_trek_spec needs a matching shadow or false_dawn in the same domain.

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