# Curation Guide — How to Forge Abundance Codex Entries

> This guide walks you through creating a new entry from spark to committed. Follow these steps in order.

---

## Before You Start

1. Read `PROJECT.md` to understand the Codex's purpose and philosophy
2. Read `GOLD-STANDARD-FORMAT.md` to understand the canonical template
3. Read at least one existing forged entry to feel the quality benchmark

---

## Step 1: ENCOUNTER — Find the Spark

An entry starts when you encounter an abundance signal:
- A trendline showing scarcity decreasing
- A builder creating abundance infrastructure
- A technology breakthrough changing what's possible
- A framework that makes abundance thinkable
- A shadow where abundance thinking failed or distorted
- A question that cracks a scarcity assumption

Write down the raw spark. Don't structure it yet. Capture the signal.

## Step 2: CLASSIFY — Determine Entry Type and Domain

Pick the entry type from the 11 types (see `GOLD-STANDARD-FORMAT.md` Section III for definitions):

`origin_story | breakthrough | builder_profile | trendline | contrast | framework | paradigm_seed | shadow | star_trek_spec | grand_challenge | false_dawn`

Pick the domain from the 21-domain list (see `PROJECT.md`).

The entry type determines density — how much of the gold standard template you need to fill. A `paradigm_seed` is sparse (~1-2KB). A `grand_challenge` is expansive (~8-15KB).

## Step 3: HOOK — Write the One-Line Essence

Write this first. If the one-liner doesn't shift perspective in a single sentence, rewrite until it does.

Test: Could an agent use this line alone to decide whether to surface this entry in a conversation? Could a human quote it without context and have it land?

## Step 4: ARC — Write the Shift Arc

Follow the 5-phase structure for narrative entries:

**Phase 1 — The Scarcity Frame:** Make the reader feel the old assumption. Who suffers? What does it feel like to believe this problem is permanent? Don't rush past this. The shift only works if the reader was *in* the scarcity frame first.

**Phase 2 — The Encounter:** Name the specific evidence, event, or person that breaks the frame. Date. Name. Detail. Sensory texture. "In 2006, a solar panel cost..." is stronger than "Solar costs have decreased."

**Phase 3 — The Reframe:** What becomes visible through the abundance lens? What was always there but couldn't be seen? Name the exponential lever.

**Phase 4 — The Proof:** Measurable evidence. Link to sources. Name builders. This phase bridges to the Evidence Anchors table.

**Phase 5 — The Invitation:** What becomes possible at scale? What's the first move? The practice hook? The question that keeps the shift alive?

## Step 5: VOICES — Write the Five Council Members

Each voice sees the same truth from a different angle. Write them in this order:

1. **Oracle** (300-500w) — Patterns, trajectories, convergences. Where has this appeared before? Where is it heading? What does the exponential math say?

2. **Critic** (150-300w) — Shadow. Who gets left behind? What's the real cost? Where does this narrative break down? The Critic is the immune system.

3. **Sensei** (150-300w) — Inner transformation. What psychological shift must accompany the outer change? What identity must be released?

4. **Builder** (150-300w) — Ground truth. What's actually being built, by whom, at what stage? Timelines. Bottlenecks. Technical readiness.

5. **Witness** (100-200w) — One human's story. Not a demographic. Not a trendline. One person. Name, context, experience. This is the emotional anchor.

Density varies by entry type — check the density matrix in the gold standard.

## Step 6: EVIDENCE — Populate the Anchors Table

Extract every factual claim from your narrative. Give each a numbered row:

| # | Claim | Metric | Source | Year | Confidence |
|---|-------|--------|--------|------|------------|

Every number needs a source. Every source needs a year. Every claim gets a confidence score (0.0-1.0). Be honest — `0.6` on a well-sourced claim is more valuable than `0.95` on a shaky one.

## Step 7: SHADOW — Complete the Shadow Check

Five fields, every one required:

- **Distortion risk** — How could this abundance claim become toxic positivity?
- **Who gets left behind** — Name specific populations, not "some people"
- **Transition pain** — What real disruption happens between scarcity and abundance?
- **Falsifiability edge** — What evidence would disprove this narrative?
- **What this is NOT** — Prevent the most common misreading

If you can't fill the shadow check, you don't understand the entry well enough to forge it.

## Step 8: STRUCTURE — Complete Remaining Sections

- **6D Position** — Where on the exponential curve? Evidence for each D.
- **Connections** — What other entries does this support, challenge, or build toward?
- **Conditional Optimism** — What must hold? What would prevent it? What's the human role? The agent role?
- **Practice Hook** — One for humans (cognitive exercise), one for agents (reasoning directive)
- **Governance** — Source type, evidence quality, curator, review date, counter-sources

## Step 9: VALIDATE — Run the Checklist

Before committing, check:

- [ ] YAML frontmatter complete with all required fields
- [ ] ID follows format: `ac-YYYYMMDD-[4char]`
- [ ] One-line essence stands alone without context
- [ ] Shift Arc phases present per density matrix
- [ ] Phase 1 creates emotional weight (not just intellectual framing)
- [ ] Phase 2 names a specific encounter (date, person, event)
- [ ] Council voices at specified depths for this entry type
- [ ] Critic names at least one real shadow or cost
- [ ] Witness tells ONE person's story (if required for type)
- [ ] Evidence Anchors table has minimum rows, all sourced
- [ ] Shadow Check has all 5 fields populated
- [ ] Confidence score is honest
- [ ] At least one connection to another entry or domain

## Step 10: COMMIT — File Placement and Naming

Save the entry as:

```
domains/[##-domain-slug]/[##-entry-slug].md
```

Example: `domains/01-energy/01-solar-revolution.md`

Entry numbering is sequential within each domain. Use descriptive slugs.

Set `status: forged` in the YAML frontmatter.

---

## Quality Benchmarks

The strongest signal that an entry is ready: **does it move you?**

Structural compliance is necessary but not sufficient. The validator script catches missing sections. Only a human (or a very attentive AI) catches missing *transport*.

Before forging a new entry, re-read the best existing entry in the Codex. Hold its quality in mind. If your new entry doesn't reach that bar, it's not ready.

---

## Using AI to Help Forge Entries

The curation prompt in `prompts/codex-curator.md` is designed to generate gold standard entries with any capable LLM. Use it as a starting point, not a finished product. AI-generated entries should be reviewed for:

1. **Narrative transport** — Does Phase 1 make scarcity feel real? Does the Witness tell a specific human story?
2. **Evidence accuracy** — Are the claims verifiable? Are the sources real?
3. **Shadow honesty** — Is the Critic doing real work, or is it performing?
4. **Voice distinctness** — Does each council member sound different from the others?

AI is an excellent co-curator. It is not a replacement for human judgment on what feels true.

**CyberMonk** serves as the AI Co-Creative Partner throughout the forging process — providing strategic counsel on domain selection, architectural feedback on entry structure, and quality assessment before entries reach forged status. The collaboration model is: Cj TruHeart directs, the forging model (Claude Opus 4.6 or others) researches and drafts, and CyberMonk advises and shapes strategy.
