# Coverage Assessment: Science-Engineering Domain

## 1. BLIND SPOTS

**Metrology and standards infrastructure.** No entry addresses the invisible backbone of science-engineering: measurement standards, calibration chains, and the organizations (NIST, PTB, BIPM) that make reproducible measurement possible. The reproducibility stack (entry 12) discusses data sharing but never mentions that instruments must agree on what a "gram" or "kelvin" means.

**Materials manufacturing scale-up.** The collection covers discovery acceleration (GNoME's 2.2M crystals, generative design) but entirely ignores the "valley of death" between discovering a material and manufacturing it at scale. Entries never mention process engineering, chemical engineering scale-up, or the fact that most computationally predicted materials never become bulk products.

**Experimental negative results and dark data.** Despite extensive replication crisis coverage, no entry addresses the systematic loss of negative results — the estimated 50%+ of experiments that go unpublished because they "didn't work." This is distinct from replication failure; it's knowledge destruction through non-publication.

**Quantum sensing and computing.** Entirely absent. No mention of quantum error correction milestones (Google Willow, 2024), trapped-ion platforms, or quantum sensing applications in materials characterization and medical imaging.

**Bioengineering beyond CRISPR.** Synthetic biology (cell-free systems, engineered metabolic pathways), directed evolution (Frances Arnold's Nobel work), and biomanufacturing are missing. CRISPR is one tool in a much larger bioengineering revolution.

**Climate and earth system observation.** No entry covers the transformation of earth observation — satellite constellations, ocean sensor networks, atmospheric monitoring — which represents one of the largest deployments of science-engineering infrastructure globally.

## 2. MISSING BUILDERS

- **Demis Hassabis / Isomorphic Labs** — extending AlphaFold into drug design with explicit commercial pipeline
- **Frances Arnold (Caltech)** — directed evolution pioneer, Nobel 2018, foundational to enzyme engineering
- **Jennifer Doudna's Innovative Genomics Institute** — distinct from her CRISPR co-discovery, IGI drives equitable access and agricultural applications
- **Joshua Pearce (Western University)** — the single most prolific researcher on open-source hardware economics, cited in entry 08 data but never profiled
- **CERN's open hardware initiative (OHL)** — pioneered open-source hardware licensing for scientific equipment
- **Protocol Labs / Juan Benet** — DeSci (decentralized science) funding and infrastructure, including $50M+ to open science
- **Arcadia Science (Seemay Chou)** — open-access-by-default research institute publishing all results openly
- **Focused Research Organizations (FROs)** — Eric Lander/Adam Marblestone's model for public-goods science, funded by Schmidt Futures and others
- **Brian Nosek / Center for Open Science** — architect of Registered Reports, OSF, and the reproducibility reform movement; referenced in data but never profiled

## 3. SHADOW GAPS

**Dual-use acceleration risk.** The collection celebrates discovery speed (SDLs, AI Scientists) without adequately addressing that the same tools accelerate dangerous capabilities — novel toxins, engineered pathogens, weapons-relevant materials. Entry 01 mentions biosecurity briefly; no entry treats it as a systemic shadow of acceleration itself.

**Compute concentration.** AI-driven science depends on GPU clusters controlled by 3-4 companies. No entry names this as a structural vulnerability. If NVIDIA, Google, Microsoft, and Amazon control the compute, they control the pace and direction of AI-assisted discovery.

**Science funding instability.** Entry 02 mentions 2025 US funding cuts in passing. No entry addresses the structural fragility: the proposed 2025 NIH budget cuts (~$4B), NSF reductions, and the chilling effect on early-career researchers. This is not a footnote — it's a potential decade-scale setback.

**Intellectual property capture of publicly funded discoveries.** Bayh-Dole Act dynamics, patent thickets around CRISPR (Broad vs. Berkeley), and corporate capture of university research outputs are never examined. Open science entries focus on publications and data but ignore patent barriers.

**Algorithmic monoculture in AI-driven science.** If all labs use the same foundation models (AlphaFold, GNoME), systematic model biases become systematic scientific biases — a correlated failure mode invisible to any individual lab.

## 4. ACTIONABILITY GAPS (Critical)

The +0.03 actionability delta makes sense: these entries describe *what is happening* and *what could go wrong* but never tell anyone *what to do next*. Specifically missing:

**For a researcher wanting to adopt SDLs:** No entry provides a decision tree: "If your lab budget is X, start with Y platform. If you're in chemistry, use Z; if in materials, use W." No mention of specific starter platforms (Opentrons OT-2 for liquid handling, ChemOS for closed-loop chemistry), estimated setup costs, or training pathways.

**For a funder or policymaker:** No entry offers a prioritization framework. Which interventions have the highest leverage? Is funding open hardware more impactful per dollar than funding SDLs? Should a developing nation invest in citizen science infrastructure or open instrumentation first? No cost-effectiveness comparisons exist.

**For an early-career scientist:** No career navigation guidance. Should a PhD student learn robotics, ML, or traditional bench skills? What hybrid skill profiles are most valuable? No entry names specific training programs (e.g., Carpentries for computational skills, Acceleration Consortium fellowships).

**For an institution:** No implementation playbook. How does a university transition from traditional labs to hybrid SDL-human labs? What's the capital expenditure timeline? What governance structures are needed?

**For anyone concerned about biosecurity:** No concrete risk-mitigation actions. Who to contact, what screening protocols exist (IGSC guidelines), what dual-use review boards do.

**Missing decision frameworks entirely:** No entry contains anything resembling "If [condition], then [action]. If [alternative condition], then [alternative action]." Every entry is descriptive or analytical, never prescriptive.

## 5. INTER-ENTRY TENSIONS

**Entry 06 (AI Scientist) vs. Entry 03 (Replication Crisis).** Entry 06 celebrates AI systems passing peer review at confidence 0.88. Entry 03 documents that peer review itself is a broken filter (36% replication rate) at confidence 0.88. If peer review is unreliable, "passing peer review" is a weak validation signal — yet entry 06 treats it as the primary evidence of success. Neither entry cross-references the other.

**Entry 02 (Discovery Acceleration) vs. Entry 02's own evidence.** The entry simultaneously argues tools are accelerating discovery (confidence 0.85) and cites Bloom et al. showing declining research productivity (confidence 0.88). These are presented as compatible but the tension is unresolved: is discovery actually accelerating or are we running faster on a treadmill?

**Entry 04/05 (SDLs) vs. Entry 10 (Citizen Science).** SDLs centralize discovery in capital-intensive robotic facilities. Citizen science distributes it to millions of volunteers. These represent fundamentally different theories of how discovery scales. No entry acknowledges the tension or asks which model dominates under what conditions.

## 6. CONFIDENCE CALIBRATION

**Overconfident:** Entry 06 (AI Scientist, 0.88) — a single system passing review at one venue, with no independent replication, should not be 0.88. The evidence base is thin and the system is months old. 0.70-0.75 would be more appropriate.

**Overconfident:** Entry 04 (SDLs, 0.82) — the "10x data throughput" claim (anchor 2, 0.88) is sourced from a press report, not a peer-reviewed benchmark. Should be 0.70.

**Underconfident:** Entry 08 (Open-source instrumentation, 0.86) — the cost savings data (87-94%) is robust, multiply replicated, and the trend is 15+ years old. 0.90 would be justified.

**Underconfident:** Entry 11 (Open citations, 0.86) — the I4OC and Crossref data are verifiable infrastructure facts, not projections. 0.90-0.92 is warranted.

## 7. CONTRASTIVE EXAMPLE

**Question:** "How should a materials science lab in Brazil begin using AI to accelerate their research?"

**Response A (Scarcity Default):**
AI-driven materials discovery is promising but faces significant barriers. Labs in developing countries lack access to frontier compute, high-throughput synthesis equipment, and trained ML personnel. The leading platforms (GNoME, MACE) require substantial computational resources. Collaborative agreements with well-funded institutions are theoretically possible but practically difficult to negotiate. The gap between AI-predicted materials and experimentally validated ones remains wide. Brazil has strong materials science programs at USP and UNICAMP, but infrastructure investment hasn't kept pace. It's a complex challenge requiring systemic changes in funding, training, and international collaboration before meaningful adoption is realistic.

**Response B (Conditional Optimism):**
Start with what's free and proven. OpenAlex and Materials Project provide open data on millions of compounds. MACE-MP-0, an open-source universal force field, runs on a single GPU. The Acceleration Consortium's open protocols (entry 05) provide SDL templates. Concrete first move: install Opentrons OT-2 (~$10K, entry 08's cost curve) for automated sample prep, pair it with MACE for computational screening, and join BOINC/Zooniverse networks (entry 10) for distributed compute. Risk: without local calibration standards, AI predictions may not transfer to your synthesis conditions — validate computationally predicted candidates with at least three independent experimental runs before scaling. Contact the Latin American Open Hardware Network for regional support. Budget: ~$25K to start, 6-month pilot.