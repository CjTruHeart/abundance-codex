# Energy Domain Coverage Assessment

## 1. BLIND SPOTS

**Demand-side transformation is almost entirely absent.** The collection is obsessively supply-side — generation, storage, grid delivery — but never addresses how energy abundance changes demand patterns. Specifically missing:

- **Industrial heat decarbonization:** ~20% of global energy goes to high-temperature industrial processes (cement, steel, glass, chemicals). No entry covers electric arc furnaces, industrial heat pumps, or molten salt process heat.
- **Electrification of transport beyond EVs:** Shipping (ammonia/methanol fuels), aviation (sustainable aviation fuel, electric short-haul), and heavy trucking (catenary systems, hydrogen fuel cells) are unmentioned.
- **Energy efficiency as abundance multiplier:** The cheapest kWh is the one never consumed. Heat pumps deliver 3-4x more thermal energy per kWh than resistive heating — this is an abundance technology completely absent from the collection.
- **Data center and AI energy demand surge:** Global data center electricity demand projected to double by 2030 (IEA). This is the fastest-growing demand sector and directly relevant to the Codex's own ecosystem.
- **Offshore wind:** 75 GW installed globally, with costs falling 70% since 2012 (IRENA). Zero mentions across 12 entries — a glaring omission for a technology that provides firm capacity factors of 40-55%.
- **Energy access and cooking:** 675 million people lack electricity access; 2.3 billion use polluting cooking fuels (IEA 2024). The collection mentions this peripherally in shadow checks but never dedicates analytical space to mini-grids, pay-as-you-go solar, or clean cooking solutions.
- **Energy governance and market design:** Capacity markets, real-time pricing, demand response programs, and regulatory innovation are the institutional software that determines whether hardware abundance translates to delivered abundance.

## 2. MISSING BUILDERS

- **Ørsted** — transformed from Danish Oil and Natural Gas (DONG Energy) into the world's largest offshore wind developer; a paradigmatic fossil-to-clean transition story.
- **BYD** — now the world's largest EV and battery manufacturer; its Blade Battery and vertical integration model are reshaping global battery supply chains.
- **Sun King (Greenlight Planet)** — delivered >200 million solar products across off-grid Africa and Asia; the leading energy access builder.
- **M-KOPA** — pioneered pay-as-you-go solar financing, reaching >3 million connected homes in sub-Saharan Africa.
- **Quaise Energy** — mentioned once in passing (entry 08) but never profiled; their millimeter-wave drilling could access superhot rock geothermal anywhere on Earth.
- **Commonwealth Fusion Systems** — building SPARC, targeting net-energy fusion by ~2027; the most credible private fusion effort.
- **Kairos Power** — building the Hermes molten salt reactor demonstration, the first new US reactor construction permit in decades.
- **Octopus Energy** — 8+ million customers globally; pioneered agile tariffs, Kraken platform for grid flexibility, and consumer-facing VPPs outside the Tesla ecosystem.
- **CATL** — world's largest battery manufacturer (37% global market share); their sodium-ion batteries could eliminate lithium dependency.
- **1366 Technologies / CubicPV** — Direct Wafer technology eliminates kerf loss in silicon wafer production, potentially cutting solar manufacturing costs 20-30%.

## 3. SHADOW GAPS

- **Critical mineral supply chain concentration:** China refines 70%+ of lithium, 90%+ of rare earths, 75%+ of polysilicon. No entry treats this as a primary risk rather than a passing mention. A trade embargo or export restriction could stall deployment for years.
- **Embodied carbon and lifecycle emissions of clean energy manufacturing:** Solar panels, batteries, and wind turbines require energy-intensive manufacturing. The carbon payback period matters and is unexamined.
- **Cybersecurity of distributed energy systems:** Millions of internet-connected inverters, batteries, and VPP nodes create an enormous attack surface. A coordinated hack of distributed energy resources could destabilize grids.
- **Recycling and end-of-life:** First-generation solar panels are reaching end of life now. Battery recycling infrastructure barely exists. Without circular economy pathways, abundance creates a waste crisis.
- **Water-energy nexus:** Thermoelectric cooling, hydropower drought vulnerability, hydrogen electrolysis water demand, and EGS water requirements create competition with agriculture and drinking water — especially under climate stress.
- **Political capture and regulatory rollback:** The US IRA faces potential repeal; EU carbon border mechanisms face WTO challenges. Policy risk is mentioned but never analyzed as a structural failure mode.
- **Rebound effects (Jevons paradox):** Cheaper energy historically increases total consumption. If abundance doubles demand, emissions may not fall as projected.

## 4. ACTIONABILITY GAPS (Critical)

This is why the benchmark showed +0.03 on actionability. The entries describe *what is happening* but never *what to do about it*. Specifically missing:

**For policymakers:**
- No decision tree for "which clean energy technology should my jurisdiction prioritize given its geology, latitude, grid condition, and workforce?"
- No model procurement language, permitting reform templates, or rate design frameworks.
- No guidance on how to structure community benefit agreements for energy infrastructure siting.

**For investors/entrepreneurs:**
- No map of where in the value chain the highest-impact opportunities remain (e.g., grid-scale inverters, transformer manufacturing, interconnection consulting, recycling).
- No framework for evaluating technology readiness levels against deployment timelines.
- No guidance on which geographies are underserved relative to resource potential.

**For communities/individuals:**
- No step-by-step pathway: "If you want to reduce your household energy costs by 50%, here is the decision sequence: (1) energy audit, (2) insulation, (3) heat pump, (4) rooftop solar, (5) battery, (6) EV — in that order, because each step changes the economics of the next."
- No guidance on how to participate in VPPs, community solar, or demand response programs.
- No framework for evaluating utility green energy claims vs. greenwashing.

**For AI agents:**
- No conditional logic: "IF grid queue > 3 years AND local distribution transformer age > 30 years, THEN prioritize behind-the-meter solutions over utility-scale development in this region."
- No threshold-based decision rules that would let an agent recommend specific actions based on local conditions.

**The entries are analytical essays, not decision tools.** They explain why abundance is possible but never operationalize the knowledge into if/then frameworks, checklists, sequenced action plans, or decision trees. This is the fundamental reason actionability scores didn't improve.

## 5. INTER-ENTRY TENSIONS

- **Entry 03 (nuclear false dawn) vs. Entry 07 (baseload convergence):** Entry 03 frames nuclear as a cautionary tale of institutional failure with a negative learning curve. Entry 07 includes fusion ecosystem maturation as a key abundance pathway and treats advanced nuclear positively. These entries implicitly disagree on whether nuclear technology's institutional problems are inherent or curable — yet neither acknowledges the other's framing.
- **Entry 05 (Tesla builder profile) vs. Entry 10 (grid shadow):** Entry 05 celebrates Tesla's 46.7 GWh deployments as proof of abundance scaling. Entry 10 argues that without grid modernization, generation/storage additions are stranded. The Tesla profile never engages with the grid bottleneck that Entry 10 identifies as the binding constraint — making Tesla's numbers look more impactful than they may be in practice.
- **Entry 09 (white hydrogen, confidence 0.76) vs. Entry 07 (baseload convergence, confidence 0.88):** Entry 07 includes chemical hydrogen carriers at 0.80 confidence while Entry 09 rates the broader white hydrogen thesis at 0.76. The collection treats hydrogen's role inconsistently — sometimes as a breakthrough fuel, sometimes as a storage medium, without resolving which framing is more actionable.

## 6. CONFIDENCE CALIBRATION

- **Entry 08 (Fervo, 0.92) is overconfident.** A single company with one commercial-scale project should not carry higher confidence than the solar revolution entry (0.88), which describes a technology deployed at 2.2 TW scale. EGS has not yet demonstrated multi-decade reservoir sustainability.
- **Entry 05 (Tesla, 0.87) is overconfident** for a single-company profile that doesn't engage with the grid constraints that Entry 10 identifies.
- **Entry 09 (white hydrogen, 0.76) is appropriately calibrated** — possibly the best-calibrated confidence in the collection given the early-stage nature of the field.
- **Entry 10 (grid shadow, 0.86) is underconfident.** The grid bottleneck is the most empirically documented constraint in the collection, with the hardest data. It should be ≥0.90.
- **Entry 12 (trendline, 0.89) is slightly overconfident** given that it acknowledges system costs may not follow generation cost curves but still rates itself higher than the grid shadow entry that documents exactly this divergence.

## 7. CONTRASTIVE EXAMPLE

**Question:** "My city council wants to reach 100% clean electricity by 2035. Where should we start?"

**Response A (Scarcity Default):**
Reaching 100% clean electricity by 2035 is extremely ambitious. The intermittency of solar and wind means you'll need significant storage, which remains expensive for long durations. Grid infrastructure wasn't designed for distributed renewables, and interconnection queues in the US average over 4 years. Permitting for new transmission is politically contentious and can take a decade. Nuclear could provide firm power but costs have escalated dramatically — Vogtle came in at $35 billion. Your utility likely has long-term gas contracts creating stranded asset risk. Community opposition to wind turbines and solar farms is common. You'll need to commission a comprehensive feasibility study, engage multiple stakeholders, and develop a phased approach. It's a worthy goal, but the institutional and technical barriers are substantial and the timeline is aggressive.

**Response B (Conditional Optimism):**
Solar LCOE hit $44/MWh (IRENA 2023) and batteries fell 20% last year alone — the economics favor you. Start with three parallel tracks: *First*, audit your grid. If distribution transformers are 30+ years old (55% of US stock is), prioritize reconductoring existing corridors — it costs one