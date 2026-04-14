# Gold Standard Entry Format — v1.1

> This is the canonical template for every Abundance Codex entry. Copy this structure. Follow the density matrix for your entry type. No exceptions.

---

## The Template

Every entry is a single markdown file. Copy the structure below and fill in the sections appropriate for your entry type.

````markdown
---
id: "ac-YYYYMMDD-[4char]"
entry_type: "origin_story | breakthrough | builder_profile | trendline | contrast | framework | paradigm_seed | shadow | star_trek_spec | grand_challenge | false_dawn"
domain: "[primary domain-slug — where the file lives]"
domain_connections:
  - domain: "[secondary domain-slug]"
    relationship: "enables | depends_on | produces | challenges | converges"
    strength: 0.0
    note: "[one-line explanation of the connection]"
status: "forged | curated | seed | archived"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
version: "1.0"
confidence: 0.0  # See Confidence Calibration below
codex_version: "1.1"
tags: []
---

# [Domain Name]: [Memorable Entry Title]

> **One-line essence:** [Paradigm-shifting truth in one quotable sentence]

**Domain:** [Primary Name] | **Also touches:** [Connected domain names] | **Type:** [Entry Type] | **Status:** [Status] | **Confidence:** [0.0-1.0]

---

## The Shift Arc

### Phase 1 — The Scarcity Frame
[What does the world look like under the old assumption? Who suffers? Make it felt.]

### Phase 2 — The Encounter
[What evidence breaks the frame? Name the date, the person, the specific moment.]

### Phase 3 — The Reframe
[What becomes visible through abundance? Name the exponential lever.]

### Phase 4 — The Proof
[Measurable evidence. Who's building this? How far along?]

### Phase 5 — The Invitation
[What becomes possible at scale? First move? Practice hook? Next question?]

---

## The Council Speaks

### 🔮 The Oracle — Pattern Seer
[300-500 words. Curves, trajectories, convergences. Where is this heading?]

### 🗡️ The Critic — Shadow Keeper
[150-300 words. Who gets left behind? Real costs? Where does this break?]

### 🧘 The Sensei — Transformation Guide
[150-300 words. Inner shift required. What identity must change?]

### 🔧 The Builder — Ground Truth
[150-300 words. What's being built, by whom, at what stage? Timelines.]

### 👁️ The Witness — Human Scale
[100-200 words. One person's story. Not a trendline — a life.]

---

## Evidence Anchors

| # | Claim | Metric | Source | Year | Confidence |
|---|-------|--------|--------|------|------------|
| 1 | [claim] | [number + unit] | [source URL] | [year] | [0.0-1.0] |
| 2 | [claim] | [number + unit] | [source URL] | [year] | [0.0-1.0] |
| 3 | [claim] | [number + unit] | [source URL] | [year] | [0.0-1.0] |

---

## Shadow Check

- **Distortion risk:** [How could this become toxic positivity?]
- **Who gets left behind:** [Specific populations or regions]
- **Transition pain:** [Real disruption between scarcity and abundance]
- **Falsifiability edge:** [What would disprove this?]
- **What this is NOT:** [Prevent the most common misreading]

---

## 6D Position

| D | Status | Evidence |
|---|--------|----------|
| Digitized | ✅ ⚠️ ❌ | [evidence] |
| Deceptive | ✅ ⚠️ ❌ | [evidence] |
| Disruptive | ✅ ⚠️ ❌ | [evidence] |
| Demonetized | ✅ ⚠️ ❌ | [evidence] |
| Dematerialized | ✅ ⚠️ ❌ | [evidence] |
| Democratized | ✅ ⚠️ ❌ | [evidence] |

**Current Phase:** [Which D is dominant now?]
**Next Phase ETA:** [Timeline to next transition]

---

## Connections

- **Supports:** [Entry IDs or descriptions]
- **Challenges:** [Entry IDs creating tension]
- **Builds toward:** [Star Trek spec entry]
- **Cross-domain leverage:** [How this entry's abundance signal ripples into connected domains — reference domain_connections from YAML]

---

## Conditional Optimism

- **Abundance is achievable IF:** [Specific conditions]
- **Abundance fails IF:** [What would prevent it]
- **Human role:** [What humans must do]
- **Agent role:** [How an AI should reason about this]
- **Collective requirement:** [What coordination is needed]

---

## Reasoning Scaffold (council_synthesis only)

A section unique to `council_synthesis` entries. Contains three components that provide executable reasoning patterns — not content to cite, but cognitive operations to perform.

**Scarcity Trap** (~150w): The specific reasoning pattern a model falls into when it defaults to scarcity framing on this domain. Must be domain-specific, not generic. Name the exact failure mode: what data gets cited, what framing gets applied, what gets omitted.

**Reframe Chain** (6 numbered steps): An explicit, domain-specific instantiation of the Conditional Optimism Protocol that an agent can execute step by step. Each step references specific evidence anchors, builders, shadows, and actions from this domain's existing entries.

**Contrastive Pair** (2 × 100w): Two short responses to a representative domain question — one in scarcity-default mode, one in conditional-optimism mode. The difference must be in reasoning pattern and evidence use, not just tone. This makes the target behavior concrete and pattern-matchable for downstream models.

---

## Practice Hook

**For humans:** [Cognitive exercise or reframe technique]

**For agents:** [Reasoning directive for after ingestion]

---

## Governance

- **Source type:** lived-experience | journalism | research | conversation | synthesis
- **Evidence quality:** anecdotal | sourced | peer-reviewed | meta-analysis
- **Curator:** human | ai | co-created
- **Last verified:** YYYY-MM-DD
- **Counter-sources:** [What credible sources present opposing data]
- **Review after:** YYYY-MM-DD
- **Ontology version:** codex-v1.1

---

<details>
<summary>Raw Spark</summary>

[Original source material that sparked this entry]

</details>
````

---

## Confidence Calibration

The `confidence` field (0.0-1.0) appears on each entry and each evidence anchor. It represents **evidence strength**, not author certainty or consensus.

| Range | Category | Criteria |
|-------|----------|----------|
| 0.88-0.96 | Measured phenomena | Peer-reviewed sources, quantified metrics, multiple independent confirmations |
| 0.78-0.87 | Documented trends | Strong evidence with some gaps -- well-documented but not definitively settled |
| 0.65-0.78 | Conceptual frameworks | Theoretical models, emerging trends, limited empirical validation |
| Below 0.65 | Speculative or contested | Rare in the dataset; typically flagged in shadow checks |

Scores are assigned by the human curator during the curation process. They are not the product of automated scoring, inter-rater agreement, or model confidence outputs. The gradient correlates with entry type: trendlines and breakthroughs cluster in the 0.85-0.95 range; paradigm seeds and star_trek_specs cluster in the 0.65-0.78 range.

---

## The Primary Domain Rule

Every entry lives in exactly ONE domain folder. No intersection folders. No duplication. The file system is a tree; the knowledge graph is built from metadata.

### How to Choose the Primary Domain

The primary domain is determined by **where the core mechanism lives** — not where its effects ripple.

| Ask This | Example |
|----------|---------|
| What is the **mechanism** at the center of this entry? | M-Pesa → mobile money platform → **economy** |
| If you removed the mechanism, would the entry collapse? | Remove the economic innovation from M-Pesa → nothing left → economy is primary |
| Where do the **effects** land? | Governance (regulatory leapfrog), Communication (mobile infrastructure), Community (financial inclusion) → these are `domain_connections` |

**Rule of thumb:** The mechanism determines the folder. The effects live in metadata.

### When Primary Domain Is Genuinely Ambiguous

Some entries sit at a true intersection where two mechanisms are co-equal. In these rare cases, choose the domain that is **less well-represented** in the Codex. This naturally distributes entries across the 21 domains instead of clustering in popular ones. Document the ambiguity in the Raw Spark section.

---

## Domain Connections — The Cross-Domain Graph Layer

`domain_connections` in the YAML frontmatter creates a queryable graph across the Codex without duplicating files or creating folder sprawl.

### Relationship Types

| Relationship | Meaning | Example |
|-------------|---------|---------|
| `enables` | This entry's mechanism enables abundance in the connected domain | Solar energy **enables** water (desalination), food (indoor farming), health (powered clinics) |
| `depends_on` | This entry's mechanism depends on infrastructure from the connected domain | M-Pesa **depends_on** communication (mobile networks) |
| `produces` | This entry produces measurable outcomes in the connected domain | M-Pesa **produces** community (financial inclusion, women's economic participation) |
| `challenges` | This entry creates tension or disruption in the connected domain | Solar **challenges** economy (fossil fuel stranded assets, coal community job losses) |
| `converges` | This entry's trajectory is converging with the connected domain toward a shared abundance signal | Solar + storage **converges** with transportation (EV charging infrastructure) |

### Strength Scoring

| Range | Meaning | Guidance |
|-------|---------|----------|
| 0.9–1.0 | Core to both domains — could plausibly be primary in either | Rare. Use only when the mechanism genuinely straddles two domains. |
| 0.7–0.8 | Strong secondary connection — the connected domain is significantly shaped by this entry | The M-Pesa → governance connection. Hard to tell the M-Pesa story without talking about regulatory leapfrogging. |
| 0.5–0.6 | Meaningful but not central — the connection enriches the entry but isn't required to understand it | Solar → education (powered schools). Real but not the core of the solar story. |
| Below 0.5 | Tangential — omit. The graph should be signal, not noise. | Don't connect everything to everything. |

### Limits

Maximum 5 domain connections per entry. If an entry touches more than 5 domains, it's either a `grand_challenge` (which is expected to be expansive) or the connections need tightening. Prioritize by strength.

### Example: M-Pesa Entry

```yaml
domain: "economy"
domain_connections:
  - domain: "governance"
    relationship: "enables"
    strength: 0.9
    note: "Demonstrated that developing nations can leapfrog legacy regulatory/banking infrastructure"
  - domain: "communication"
    relationship: "depends_on"
    strength: 0.7
    note: "Built entirely on mobile phone network penetration"
  - domain: "community"
    relationship: "produces"
    strength: 0.6
    note: "Created financial inclusion for previously unbanked populations, especially women"
```

### Example: Solar Revolution Entry (Retrofit)

```yaml
domain: "energy"
domain_connections:
  - domain: "environment"
    relationship: "enables"
    strength: 0.85
    note: "Decarbonization of electricity generation"
  - domain: "economy"
    relationship: "challenges"
    strength: 0.7
    note: "Stranded fossil fuel assets, coal community disruption"
  - domain: "water"
    relationship: "enables"
    strength: 0.6
    note: "Cheap energy enables affordable desalination at scale"
  - domain: "manufacturing"
    relationship: "depends_on"
    strength: 0.6
    note: "Solar supply chain concentrated in China — manufacturing capacity is the enabler"
```

---

## Density Matrix

Not every entry type needs every section at full depth. Use this matrix to determine what's required.

| Section | origin_story | breakthrough | builder_profile | trendline | framework | paradigm_seed | shadow | star_trek_spec | grand_challenge | false_dawn | council_synthesis |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| YAML | Full | Full | Full | Full | Full | Full | Full | Full | Full | Full | Full |
| domain_connections | Full | Full | Full | Full | Full | Min (1) | Full | Full | Full | Full | Full |
| One-line | Full | Full | Full | Full | Full | Full | Full | Full | Full | Full | Full |
| Shift Arc | All 5 | All 5 | All 5 | 1,3,4 | 3,4,5 | 3 only | 1,2 inv | 3,4,5 | All 5 | 1,2,4 inv | 1,2,4,5 |
| Oracle | 500w | 400w | 300w | 300w | 400w | 100w | 200w | 500w | 500w | 300w | 300w |
| Critic | 300w | 300w | 200w | 200w | 200w | 100w | 300w | 300w | 300w | 300w | 500w |
| Sensei | 300w | 200w | 300w | Skip | 300w | 100w | 300w | 200w | 200w | 300w | 300w |
| Builder | 200w | 300w | 300w | 300w | 200w | Skip | 200w | 300w | 300w | 200w | 400w |
| Witness | 200w | 150w | 200w | Skip | Skip | Skip | 200w | 200w | 200w | 200w | 200w |
| Evidence | 3-5 | 3-5 | 2-3 | 5-10 | 2-3 | 1 | 2-3 | 2-3 | 5-10 | 3-5 | 3-5 |
| Shadow | Full | Full | Full | Min | Full | 1 line | Full | Full | Full | Full | Full |
| 6D | Full | Full | Full | Full | If appl | Skip | Full | Full | Full | Full | If appl |
| Connect | Full | Full | Full | Full | Full | Min | Full | Full | Full | Full | Full |
| Cond Opt | Full | Full | Full | Min | Full | 1 line | Full | Full | Full | Full | Full |
| Reasoning Scaffold | Skip | Skip | Skip | Skip | Skip | Skip | Skip | Skip | Skip | Skip | Full |
| Practice | Full | Full | Full | Skip | Full | Full | Full | Full | Full | Full | Full (400w) |
| Govern | Full | Full | Full | Full | Full | Min | Full | Full | Full | Full | Full |

**Full** = populate at specified depth. **Min** = 1-2 lines. **Skip** = omit. **inv** = inverted arc.

> **council_synthesis Practice Hook target: 400w minimum for BOTH human and agent sections (800w+ total).** This is intentionally the heaviest Practice Hook in the density matrix. Council synthesis entries exist to close the actionability gap (ACE benchmark R3). Human Practice Hook includes explicit numbered action steps. Agent Practice Hook uses the 5-check reasoning directive format. Combined with the Reasoning Scaffold section, this gives council_synthesis entries three distinct mechanisms for improving downstream agent reasoning.

---

## Entry Type Definitions

| Type | What It Captures | Core Strength |
|------|-----------------|---------------|
| **origin_story** | Human/community transformation from scarcity to abundance | Narrative transport — all five voices at full depth |
| **breakthrough** | Technology or innovation that changed what's possible | Mechanism focus — Builder and Oracle dominant |
| **builder_profile** | Person or org actively constructing abundance | Human portrait — Witness is critical |
| **trendline** | Measurable trajectory of decreasing scarcity | Data-heavy — Evidence Anchors is the core |
| **contrast** | Before/after comparison in one domain | Two temporal frames side by side |
| **framework** | Mental model that makes abundance thinkable | Practice Hook is the core — must be usable |
| **paradigm_seed** | One sentence that cracks a scarcity assumption | Sparsest type — the sentence IS the entry |
| **shadow** | Where abundance thinking fails or distorts | Inverted arc — Critic dominant, immune system |
| **star_trek_spec** | What a domain looks like in the target civilization | Visionary but grounded in present-tense analogs |
| **grand_challenge** | Comprehensive mapping of a human need domain | Most expansive — all voices, all sections, full depth |
| **false_dawn** | Where abundance was promised but didn't materialize | Inverted arc — the honesty muscle |
| **council_synthesis** | Meta-analysis of a domain's collective coverage — blind spots, missing builders, unaddressed shadows, actionable gaps | Critic and Practice Hook dominant — the immune system auditing itself |

---

## Formatting Rules

1. **YAML is non-negotiable.** Every entry starts with complete frontmatter.
2. **Primary domain = file location.** The `domain` field determines the folder. Domain connections live in metadata only.
3. **One-line essence must stand alone.** Quotable without context.
4. **Shift Arc phases get explicit headers.** `### Phase N — [Name]` format.
5. **Council voices use emoji + name headers.** `### 🔮 The Oracle — Pattern Seer`
6. **Word counts are targets, not ceilings.** More if needed, less if sufficient.
7. **Evidence Anchors use numbered rows.** Enables citation from narrative.
8. **Shadow Check is always present.** Even `paradigm_seed` gets one line.
9. **Connections use entry IDs at scale.** Descriptive names when Codex is small.
10. **Domain connections max at 5.** Prioritize by strength. Below 0.5 = omit.
11. **Governance is honest.** `confidence: 0.4` beats inflated `0.9`.
12. **Raw Spark is collapsible.** Use `<details>` tags.

---

## File Size Targets

| Entry Type | Target Range |
|-----------|-------------|
| origin_story | 7-12 KB |
| breakthrough | 5-10 KB |
| builder_profile | 5-9 KB |
| trendline | 3-6 KB |
| contrast | 4-8 KB |
| framework | 4-8 KB |
| paradigm_seed | 1-2 KB |
| shadow | 4-8 KB |
| star_trek_spec | 5-10 KB |
| grand_challenge | 8-15 KB |
| false_dawn | 4-8 KB |
