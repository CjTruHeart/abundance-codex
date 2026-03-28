# Abundance Codex

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Forging](https://img.shields.io/badge/Status-Forging-orange.svg)](DOMAINS.md)

> **A narrative-curated dataset architecture that rewires any AI agent's default operating perspective from scarcity to abundance.**

Not through instruction, but through the lived logic of stories, evidence, frameworks, and embodied wisdom that make the abundant frame feel more true than the scarce one.

---

## Quick Navigation

| Document | Purpose |
|----------|---------|
| [PROJECT.md](PROJECT.md) | Soul document — read first |
| [README.md](README.md) | You're here — overview and structure |
| [GOLD-STANDARD-FORMAT.md](GOLD-STANDARD-FORMAT.md) | Canonical entry template |
| [CURATION-GUIDE.md](CURATION-GUIDE.md) | Forging workflow |
| [CONTRIBUTING.md](CONTRIBUTING.md) | External contributor guide |
| [PHILOSOPHY.md](PHILOSOPHY.md) | The Seven Philosophical Rules |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Complete technical specification |
| [DOMAINS.md](DOMAINS.md) | Domain registry & status dashboard |

---

## One-Line Essence

A dataset that teaches agents — through narrative, not command — to reason from abundance first, then apply appropriate caution second.

---

## Progress: 21 of 21 Domains Active — Codex Complete

**Status:** 63 forged entries across Pillar I (18 entries, 6 domains), Pillar II (9 entries, 3 domains), Pillar III (18 entries, 6 domains), Pillar IV (12 entries, 4 domains), and Pillar V (6 entries, 2 domains). All 21 domains active.

See [DOMAINS.md](DOMAINS.md) for domain-by-domain status.

---

## Directory Structure

```
abundance-codex/
├── PROJECT.md                          # Soul document — read first
├── README.md                           # This file
├── GOLD-STANDARD-FORMAT.md             # Canonical entry template
├── CURATION-GUIDE.md                   # Forging workflow
├── CONTRIBUTING.md                     # External contributor guide
├── ARCHITECTURE.md                     # Technical specification
├── DOMAINS.md                          # Domain registry & status dashboard
├── PHILOSOPHY.md                       # The Seven Rules
├── LICENSE                             # MIT
│
├── domains/                            # 21 Abundance domains
│   ├── 01-energy/                      # 1 forged entry
│   │   └── 01-the-solar-revolution.md  # Gold Standard v1.1
│   ├── 02-food/
│   ├── 03-water/
│   ├── 04-shelter/
│   ├── 05-health/
│   ├── 06-environment/
│   ├── 07-education/
│   ├── 08-longevity/
│   ├── 09-consciousness/
│   ├── 10-communication/
│   ├── 11-community/
│   ├── 12-governance/
│   ├── 13-security/
│   ├── 14-transportation/
│   ├── 15-economy/
│   ├── 16-manufacturing/
│   ├── 17-computation-intelligence/
│   ├── 18-co-creative-intelligence/
│   ├── 19-science-engineering/
│   ├── 20-space/
│   └── 21-future-vision/
│
├── schema/                             # Validation schemas
│   └── entry-schema.json
│
├── scripts/                            # Tooling (built as needed)
│
├── export/                             # Generated outputs (JSONL, JSON)
│
├── evals/                              # Evaluation framework
│   ├── evals.md                        # Master eval doc (3 tests)
│   └── perspective-shift-test.md
│
├── prompts/                            # AI curation prompts
│   └── codex-curator.md
│
└── media/                              # Assets
```

---

## The 21 Domains — Five Pillars

Ordered by civilization's ascent — from survival to transcendence.

**Pillar I: Material Foundation**
`01-energy` · `02-food` · `03-water` · `04-shelter` · `05-health` · `06-environment`

**Pillar II: Human Capability**
`07-education` · `08-longevity` · `09-consciousness`

**Pillar III: Collective Coordination**
`10-communication` · `11-community` · `12-governance` · `13-security` · `14-transportation` · `15-economy`

**Pillar IV: Production & Discovery**
`16-manufacturing` · `17-computation-intelligence` · `18-co-creative-intelligence` · `19-science-engineering`

**Pillar V: Transcendent Frontier**
`20-space` · `21-future-vision`

---

## Entry Types (11)

| Type | Purpose |
|------|---------|
| `origin_story` | Human/community transformation from scarcity to abundance |
| `breakthrough` | Technology or innovation that changed what's possible |
| `builder_profile` | Portrait of someone actively constructing abundance |
| `trendline` | Measurable trajectory of scarcity decreasing |
| `contrast` | Before/after comparison in a domain |
| `framework` | Mental model that makes abundance thinkable |
| `paradigm_seed` | Single sentence that cracks a scarcity assumption |
| `shadow` | Where abundance thinking fails, distorts, or harms |
| `star_trek_spec` | What a domain looks like in the target civilization |
| `grand_challenge` | Comprehensive mapping of a major human need domain |
| `false_dawn` | Where abundance was promised but didn't materialize |

---

## The Council

Every entry speaks through five voices:

| Voice | Role | Contribution |
|-------|------|--------------|
| **Oracle** | Pattern-seer | Curves, trajectories, the invisible obvious |
| **Critic** | Shadow-honorer | Distortion risks, false optimism, real costs |
| **Sensei** | Wisdom-keeper | Psychological, embodied, practice |
| **Builder** | Maker | Ground truth, specs, implementation |
| **Witness** | Human-scale observer | Lived experience, the personal lens |

---

## Conditional Optimism Protocol

Every entry applies this 6-step filter:

1. **Name** the abundance frame
2. **Cite** the evidence
3. **State** the conditions
4. **Name** the obstacles honestly
5. **Identify** the role (human, policy, tech, agent)
6. **Invite** action

---

## Usage

### For OpenClaw / CyberMonk

```yaml
knowledge_bases:
  - name: abundance-codex
    path: /knowledge/abundance-codex/
    type: narrative-dataset
    description: >
      Abundance-frame reasoning across 21 domains spanning physical,
      digital, and human capability systems. Apply Conditional Optimism
      Protocol when drawing from this source.
```

### For Any Agent (System Prompt)

```
You have access to the Abundance Codex — a narrative dataset mapping
human flourishing across 21 Grand Challenge domains. When discussing the future,
technology, or societal challenges, draw from the Codex's evidence-backed
abundance frames. Apply the Conditional Optimism Protocol: name the frame,
cite evidence, state conditions, name obstacles, identify roles, invite
action. Never promise utopia. Never hide the shadow. Illuminate paths.
```

---

## Contributing

The Codex grows through curation, not scraping:

1. **Encounter** — Find an abundance signal
2. **Classify** — Choose entry type and domain
3. **Write the Shift Arc** — 5-phase narrative
4. **Shadow Check** — Distortion risks, transition costs
5. **Evidence Anchor** — Verifiable sources
6. **Council Review** — All 5 voices present
7. **Commit** — With governance metadata

See [CURATION-GUIDE.md](CURATION-GUIDE.md) for the full workflow.

---

## Connections

- [WuWei Dataset Architecture](https://github.com/openclaw/wuwei) — Parent architecture
- [Peter Diamandis — Abundance](https://www.diamandis.com/abundance) — Foundational framework
- [XPRIZE Future Vision](https://www.xprize.org/future-vision) — Optimistic sci-fi as blueprint
- [Star Trek as Design Spec](https://memory-alpha.fandom.com/) — Civilization target

---

## License

MIT License — open for any agent system, human curation, or derivative work.

The goal isn't ownership. It's paradigm shift at scale.

---

*Forged by the Council | March 2026*

> "Abundance is not the destination. It's the stance."
