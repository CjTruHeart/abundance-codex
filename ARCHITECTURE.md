# ARCHITECTURE.md — Complete Technical Specification

## The Three Layers

Inspired by WuWei v3 "Three Rings": separate what happened from how it's interpreted from how it's used.

| Layer | Purpose | Contents |
|-------|---------|----------|
| **Layer 1: Narrative Core** | Stories that shift perspective | Origin stories, breakthroughs, builder profiles, shadows, Star Trek specs |
| **Layer 2: Evidence Lattice** | Data that grounds narrative | Trendlines, contrasts, measurable progress |
| **Layer 3: Framework Mesh** | Mental models for reasoning | Frameworks, paradigm seeds, Grand Challenge mappings |

---

## The Shift Arc — Five-Phase Narrative Structure

Every narrative entry follows this emotional engine:

### Phase 1: The Scarcity Frame
- What does the world look like assuming this problem is permanent?
- What's the emotional weight? Who suffers?
- **Goal:** Establish the starting mental model

### Phase 2: The Encounter
- What evidence disrupts the scarcity frame?
- What's the pivotal moment where "impossible" cracks?
- **Goal:** Create narrative transport — the "wait, what?" moment

### Phase 3: The Reframe
- What becomes visible through the abundance lens?
- What's the exponential lever, design insight, overlooked resource?
- **Goal:** Install the new mental model

### Phase 4: The Proof
- What measurable evidence supports the new frame?
- Who's already building? How far along?
- **Goal:** Anchor to reality, not fantasy

### Phase 5: The Invitation
- What becomes possible at scale?
- What's the first move? The practice hook?
- **Goal:** Transform reader from spectator to participant

---

## Entry Types and Schemas

### Type A: Narrative Core Entry

**Applies to:** `origin_story`, `breakthrough`, `builder_profile`, `shadow`, `star_trek_spec`

```json
{
  "id": "ac-[timestamp]-[hash]",
  "entry_type": "origin_story | breakthrough | builder_profile | shadow | star_trek_spec",
  "domain": "energy | food | water | health | education | shelter | environment | security | governance | economy | resources | space | consciousness | longevity | transportation | communication | computation-intelligence | co-evolutionary-intelligence | community | human-capability | future-vision",
  
  "shift_arc": {
    "scarcity_frame": {
      "assumption": "string",
      "emotional_weight": "string",
      "who_suffers": "string",
      "felt_sense": "string"
    },
    "encounter": {
      "disrupting_evidence": "string",
      "pivotal_moment": "string",
      "sensory_detail": "string"
    },
    "reframe": {
      "abundance_lens": "string",
      "what_was_always_there": "string",
      "exponential_lever": "string"
    },
    "proof": {
      "measurable_evidence": "string",
      "builders_active": ["string"],
      "trendline_links": ["string"],
      "current_progress": "string"
    },
    "invitation": {
      "what_becomes_possible": "string",
      "first_move": "string",
      "practice_hook": "string",
      "next_question": "string"
    }
  },

  "council_voices": {
    "oracle": {
      "role": "Pattern-seer, trajectory-tracker",
      "contribution": "Curves, the invisible obvious, 6D analysis"
    },
    "critic": {
      "role": "Shadow-honorer, complexity-holder",
      "contribution": "Distortion risks, false optimism, real costs"
    },
    "sensei": {
      "role": "Wisdom-keeper, embodiment-guide",
      "contribution": "Psychological transition, practice, non-resistance"
    },
    "builder": {
      "role": "Maker, implementer",
      "contribution": "Ground truth, specs, iterative reality"
    },
    "witness": {
      "role": "Human-scale observer",
      "contribution": "Lived experience, personal lens, felt impact"
    }
  },

  "shadow_check": {
    "distortion_risks": ["string"],
    "who_gets_left_behind": "string",
    "transition_pain": "string",
    "what_this_is_not": "string | array",
    "falsifiability_edge": "string"
  },

  "6d_position": {
    "digitized": { "status": "boolean", "evidence": "string" },
    "deceptive": { "status": "boolean", "evidence": "string" },
    "disruptive": { "status": "boolean", "evidence": "string" },
    "demonetized": { "status": "boolean", "evidence": "string" },
    "dematerialized": { "status": "boolean", "evidence": "string" },
    "democratized": { "status": "boolean", "evidence": "string" },
    "current_phase": "string",
    "estimated_timeline_to_next": "string"
  },

  "regenerative_frame": {
    "classification": "extractive | regenerative | transitional",
    "circular_design": "string",
    "net_impact": "string"
  },

  "connections": {
    "related_entries": ["string (entry IDs)"],
    "supports": ["string (entry IDs)"],
    "challenges": ["string (entry IDs)"],
    "builds_toward": "string (entry ID or domain)"
  },

  "governance": {
    "source_type": "lived-experience | journalism | research | conversation | synthesis",
    "evidence_quality": "anecdotal | sourced | peer-reviewed | meta-analysis",
    "confidence": "number (0.0-1.0)",
    "last_verified": "ISO-8601 date",
    "counter_sources": ["string"]
  }
}
```

---

### Type B: Evidence Lattice Entry

**Applies to:** `trendline`, `contrast`

```json
{
  "id": "ac-ev-[timestamp]-[hash]",
  "entry_type": "trendline | contrast",
  "domain": "string",

  "proof_pattern": {
    "claim": "string",
    "metric": "string",
    "unit": "string",
    "data_points": [
      { "year": "number", "value": "number", "source": "string" }
    ],
    "trendline_direction": "improving | stable | declining | exponential_improving",
    "rate_of_change": "string",
    "counter_argument": "string",
    "response_to_counter": "string"
  },

  "scarcity_vs_abundance": {
    "scarcity_state": {
      "year": "number",
      "description": "string",
      "metric_value": "number"
    },
    "abundance_state": {
      "year": "number",
      "description": "string",
      "metric_value": "number",
      "projected": "boolean"
    },
    "transition_mechanism": "string",
    "acceleration_factor": "string"
  },

  "context": {
    "why_this_matters": "string",
    "who_benefits": "string",
    "scale_of_impact": "string",
    "geographic_scope": "local | regional | national | global"
  },

  "governance": {
    "primary_source": "string",
    "secondary_sources": ["string"],
    "last_verified": "ISO-8601 date",
    "data_freshness": "real-time | monthly | annual | historical",
    "confidence": "number (0.0-1.0)"
  }
}
```

---

### Type C: Framework Mesh Entry

**Applies to:** `framework`, `paradigm_seed`, `grand_challenge`

```json
{
  "id": "ac-fw-[timestamp]-[hash]",
  "entry_type": "framework | paradigm_seed | grand_challenge",
  "domain": "string",

  "framework": {
    "name": "string",
    "one_line": "string",
    "description": "string",
    "origin": "string",
    "key_principles": ["string"],
    "application_domains": ["string"],
    "practice_hook": {
      "instruction": "string",
      "frequency": "once | daily | situational | continuous",
      "success_indicator": "string"
    }
  },

  "scarcity_to_abundance_mapping": {
    "scarcity_default": "string",
    "abundance_reframe": "string",
    "cognitive_mechanism": "string",
    "emotional_shift": "string"
  },

  "conditional_optimism": {
    "abundance_is_achievable_if": ["string"],
    "abundance_fails_if": ["string"],
    "agent_role": "string",
    "human_role": "string",
    "collective_requirement": "string"
  },

  "falsifiability": {
    "what_would_disprove_this": "string",
    "known_limitations": ["string"],
    "domains_where_this_breaks": ["string"]
  },

  "connections": {
    "related_frameworks": ["string (entry IDs)"],
    "supporting_evidence": ["string (entry IDs)"],
    "narrative_anchors": ["string (entry IDs)"]
  }
}
```

---

## The 21 Abundance Domains

### Physical Systems (1-8)
| # | Domain | Scarcity Frame | Abundance Lever | Star Trek Spec |
|---|--------|---------------|-----------------|----------------|
| 1 | **Energy** | 1.3B without electricity; fossil dependence | Solar, fusion, storage, geothermal | Clean, limitless energy for all |
| 2 | **Food** | 800M+ food insecure; agricultural limits | Precision fermentation, vertical farming, cellular ag | Nutritious food abundant everywhere |
| 3 | **Water** | 2B lack safe drinking water | Desalination, atmospheric generation, recycling | Clean water as a given, not privilege |
| 4 | **Health** | Preventable disease; unequal access | AI diagnostics, gene therapy, longevity science | Personalized preventive care for all |
| 5 | **Education** | 260M children out of school | AI tutors, open content, immersive learning | World-class personalized learning for all |
| 6 | **Shelter** | 1.6B in inadequate housing | 3D printing, modular design, new materials | Dignified, sustainable housing for all |
| 7 | **Environment** | Climate disruption, biodiversity loss | Carbon capture, regenerative ag, circular economy | Regenerative systems that heal while producing |
| 8 | **Security** | Conflict, violence, cyber threats | Predictive systems, transparent governance, resilience | Prevention-first protection without surveillance |

### Governance & Economy (9-11)
| # | Domain | Scarcity Frame | Abundance Lever | Star Trek Spec |
|---|--------|---------------|-----------------|----------------|
| 9 | **Governance** | Corruption, inefficiency, distrust | Transparent ledgers, participatory platforms, AI policy | Responsive, trustworthy institutions |
| 10 | **Economy** | Winner-take-all, structural inequality | UBI, cooperative models, demonetization | Prosperity disconnected from extraction |
| 11 | **Resources** | Depletion, extraction, conflict | Circular economy, asteroid mining, material science | Regenerative resource abundance |

### Exploration & Consciousness (12-13)
| # | Domain | Scarcity Frame | Abundance Lever | Star Trek Spec |
|---|--------|---------------|-----------------|----------------|
| 12 | **Space** | Single-planet vulnerability | Reusable rockets, asteroid mining, habitats | Multi-planetary civilization |
| 13 | **Consciousness** | Fragmented attention, meaning crisis | Contemplative tech, embodied AI, wisdom+science | Humanity awake, connected, evolving |

### Longevity & Infrastructure (14-17)
| # | Domain | Scarcity Frame | Abundance Lever | Star Trek Spec |
|---|--------|---------------|-----------------|----------------|
| 14 | **Longevity** | Aging as inevitable decline | Senolytics, gene editing, organ regeneration | Healthy lifespan extended; death as choice |
| 15 | **Transportation** | Friction, pollution, inefficiency | EVs, autonomy, hyperloop, EVTOL | Frictionless, clean mobility globally |
| 16 | **Communication** | Information asymmetry, isolation | Ubiquitous connectivity, translation, presence | Global mind, no one left out of conversation |
| 17 | **Computation-Intelligence** | Cognitive limits, slow analysis | AI, quantum, edge, distributed | Intelligence as infrastructure, like electricity |

### Human Systems (18-21)
| # | Domain | Scarcity Frame | Abundance Lever | Star Trek Spec |
|---|--------|---------------|-----------------|----------------|
| 18 | **Co-Evolutionary-Intelligence** | Human vs machine anxiety | Human-AI partnership, collective intelligence | Intelligence multiplied through partnership |
| 19 | **Community** | Isolation, division, belonging crisis | Digital villages, shared purpose, connection tech | Global local communities of meaning |
| 20 | **Human-Capability** | Fixed human limits, learned helplessness | Enhancement, skill acquisition, potential realization | Every human operating at full potential |
| 21 | **Future-Vision** | Pessimism, short-term thinking, dystopia | Optimistic sci-fi, moonshots, generational thinking | Culture oriented toward glorious futures |

---

## The 6 D's of Exponentials

Every technology entry maps to the Diamandis 6D framework:

| D | Phase | Description | Signal |
|---|-------|-------------|--------|
| 1 | **Digitized** | Becomes information technology | Can be coded, shared, improved |
| 2 | **Deceptive** | Early growth looks flat | Doubling from 0.01% → 0.02% is invisible |
| 3 | **Disruptive** | Sufficient to destabilize incumbent | Market share shift begins |
| 4 | **Demonetized** | Cost approaches zero | Previous revenue model breaks |
| 5 | **Dematerialized** | Physical product disappears | Service/substitute replaces object |
| 6 | **Democratized** | Available to everyone globally | Access inequality collapses |

---

## Entry Relationship Schema

The Codex is a graph, not a list.

### Connection Types

| Relationship | Meaning | Example |
|--------------|---------|---------|
| `supports` | Entry A provides evidence for Entry B | Solar trendline supports Energy origin story |
| `challenges` | Entry A contradicts or complicates Entry B | Shadow entry challenges breakthrough narrative |
| `builds_toward` | Entry is a stepping stone to larger vision | All entries in a domain build toward Star Trek spec |
| `related_entries` | Thematic or domain adjacency | Energy and Climate entries |

### Traversal Pattern

When an agent queries a domain, it should:
1. Start with the **Star Trek spec** (the vision)
2. Gather **origin stories** and **breakthroughs** (the narrative proof)
3. Check **trendlines** (the data proof)
4. Review **builder profiles** (the human proof)
5. Read **shadows** (the honest assessment)
6. Synthesize through **Conditional Optimism Protocol**

---

## File Naming Convention

```
domains/[##]-[domain-name]/
├── 01-origin-story.md
├── 02-breakthrough.md
├── 03-builder-profile.md
├── 04-trendline.md
├── 05-star-trek-spec.md
└── 06-false-dawn.md (optional shadow)

entries/[type]/
└── ac-[timestamp]-[hash].json

schema/
├── narrative-core.json
├── evidence-lattice.json
└── framework-mesh.json
```

---

## Confidence Scoring

| Score | Meaning | Example |
|-------|---------|---------|
| 0.9-1.0 | Established fact, multiple sources | Solar cost decline |
| 0.7-0.9 | Strong evidence, some uncertainty | Battery learning curve |
| 0.5-0.7 | Emerging trend, early data | Fusion commercialization |
| 0.3-0.5 | Speculative, hypothesis stage | Brain-computer interfaces |
| <0.3 | Philosophical, unverified | Post-scarcity psychology |

---

## Quality Gates

Before an entry is "Forged" (complete):

- [ ] All 5 Council voices present
- [ ] Shift Arc complete (5 phases)
- [ ] Shadow check completes (distortion risks named)
- [ ] Evidence anchors to verifiable sources
- [ ] 6D position mapped (for applicable entries)
- [ ] Regenerative frame classified
- [ ] Conditional Optimism Protocol applicable
- [ ] Entry passes perspective-shift test

---

## Evolution Path

**Phase 1:** 1 domain complete (Energy) ✓  
**Phase 2:** 5 domains with seed entries (Energy + 4 more)  
**Phase 3:** 13 core domains with seed entries (basic necessities)  
**Phase 4:** All 21 domains with seed entries (complete framework)  
**Phase 5:** 126 entries (6 per domain)  
**Phase 6:** Cross-domain connections mapped  
**Phase 7:** External curation workflow established

We're at Phase 1. Target: Phase 3 for "usable" status, Phase 4 for "complete framework."

---

*"Architecture is frozen intent. What intent do we freeze here? The belief that better is possible, and the honesty to build it."*
