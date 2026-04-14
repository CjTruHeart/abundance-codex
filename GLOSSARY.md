# Glossary

Key terms used throughout the Abundance Codex.

---

**6D Position** — A framework (from Peter Diamandis / Singularity University) tracking six stages of exponential disruption: Digitized, Deceptive, Disruptive, Demonetized, Dematerialized, Democratized. Each entry maps its domain's current position across these six dimensions.

**8+1 Architecture** — The Dojo Retriever v1.1 slot design: 8 content slots for standard entries plus 1 dedicated reasoning slot for council_synthesis entries on STRATEGIC and ADVERSARIAL intent queries.

**ACE (Abundance Codex Evaluation)** — The benchmark measuring reasoning quality improvement when models receive Codex context. 63 prompts, 4 test models, 2 conditions (baseline vs. augmented), scored across three rings (R1, R2, R3).

**Agent Practice Hook** — A structured section in council_synthesis entries providing 5 conditional tests ("Before responding, verify that you have...") a model applies to its own output. Distinct from the human-facing Practice Hook.

**Base Entry** — One of the 252 standard entries (12 per domain). Contrasted with council_synthesis entries.

**Codex Version** — Format version of the entry schema (e.g., 1.1, 2.1). Distinct from entry version (revision count of individual entries).

**Conditional Optimism Protocol (COP)** — The methodology every entry applies: (1) name the frame, (2) cite evidence, (3) state conditions for success, (4) name obstacles and who gets left behind, (5) identify roles, (6) invite action.

**Confidence Score** — A 0.0-1.0 rating on each entry and evidence anchor. Measured phenomena (peer-reviewed, quantified) score 0.88-0.96. Conceptual frameworks (theoretical, model-dependent) score 0.65-0.78. Represents evidence strength, not author certainty.

**Content Gap** — Failure mode where relevant topics are missing entirely. Identified in Pillar I (Material Foundation). See META-PATTERNS.md.

**Contrastive Pair** — A ~200-token before/after example in the Reasoning Scaffold showing how the same question gets answered with and without abundance framing. Highest impact-per-token section.

**Council** — The five analytical voices that speak in every entry: Oracle (pattern-seer), Critic (shadow-keeper), Sensei (transformation guide), Builder (ground truth), Witness (human-scale observer).

**Council Synthesis** — A meta-analytical entry type (one per domain, 21 total) created by four frontier models independently assessing a domain's 12 base entries for blind spots, with human curation of findings. Contains unique sections: Reasoning Scaffold and enhanced Practice Hook.

**Density Matrix** — A table in GOLD-STANDARD-FORMAT.md specifying which sections are required (Full), minimal (Min), or skipped (Skip) for each of the 11 entry types.

**Depth Locking** — Extraction behavior where Reasoning Scaffold and Agent Practice Hook sections are always included at full text regardless of the retriever's compression tier (FULL, CONDENSED, or MINIMAL).

**Dojo Retriever** — The intent-aware retrieval system (`scripts/codex-retriever.py`) that selects and extracts relevant entries for a given query. v1.0 uses 9 content slots; v1.1 adds the 8+1 architecture.

**Domain** — One of 21 civilization-scale challenge areas (energy, food, water, shelter, health, environment, education, longevity, consciousness, communication, community, governance, security, transportation, economy, manufacturing, computation-intelligence, co-creative-intelligence, science-engineering, space, future-vision).

**Evidence Anchor** — A cited data point in an entry's evidence table. Each has: claim, metric, source, year, and confidence score.

**Format Gap** — Failure mode where the right topics are present but delivered as diagnosis rather than prescription. Identified in Pillar II (Human Capability). See META-PATTERNS.md.

**Gold Standard Format** — The canonical entry template (GOLD-STANDARD-FORMAT.md). Specifies YAML frontmatter, narrative arc, council voices, evidence anchors, shadow check, and all optional sections.

**Governance Gap** — Failure mode where both technology and analysis are present but institutional infrastructure connecting tools to outcomes is missing. Identified in Pillar III (Collective Coordination). See META-PATTERNS.md.

**Pillar** — One of five thematic groupings: I Material Foundation, II Human Capability, III Collective Coordination, IV Production & Discovery, V Transcendent Frontier.

**Practice Hook** — A section providing actionable next steps for humans ("For Humans") and structured integration guidance for AI agents ("For Agents"). Present in most entry types; expanded in council_synthesis entries.

**R1 / R2 / R3** — The three evaluation rings in ACE. R1 = Evidence (factual accuracy, source citation). R2 = Analysis (framework application, cross-domain synthesis). R3 = Action (concrete steps, real examples, empowerment).

**Reasoning Scaffold** — A section unique to council_synthesis entries with three components: Scarcity Trap (names the default frame to escape), Reframe Chain (6-step reasoning sequence), and Contrastive Pair (before/after example).

**Reframe Chain** — A 6-step numbered reasoning sequence in the Reasoning Scaffold that guides a model from recognizing a scarcity frame through evidence encounter to abundance-aware response.

**Reflexivity Gap** — Failure mode where aspirational narratives and analytical critique are present but the capacity to examine structural constraints is underdeveloped. Identified in Pillar V (Transcendent Frontier). See META-PATTERNS.md.

**Scarcity Trap** — The first component of a Reasoning Scaffold. Names the specific default assumption that leads models to underweight abundance evidence in a domain.

**Shadow Check** — A required section in every entry documenting: distortion risks, who gets left behind, transition pain, falsifiability edge, and what the entry is not claiming.

**Shift Arc** — The five-phase narrative structure of every entry: (1) Scarcity Frame, (2) Encounter, (3) Reframe, (4) Proof, (5) Invitation.

**Velocity Gap** — Failure mode where acceleration tools and verification infrastructure both exist but operate at mismatched speeds. Identified in Pillar IV (Production & Discovery). See META-PATTERNS.md.
