---
id: "ac-20260414-0e59"
entry_type: "council_synthesis"
domain: "computation-intelligence"
domain_connections:
  - domain: "energy"
    relationship: "depends_on"
    strength: 0.90
    note: "Data center electricity demand projected to reach 945 TWh by 2030; compute abundance is bounded by energy abundance"
  - domain: "co-creative-intelligence"
    relationship: "enables"
    strength: 0.90
    note: "Every co-creative intelligence claim depends on inference cost, latency, and model availability — computation is the substrate"
  - domain: "manufacturing"
    relationship: "depends_on"
    strength: 0.85
    note: "TSMC foundry concentration (70% revenue, 90%+ advanced), ASML EUV monopoly — compute hardware is a manufacturing bottleneck"
  - domain: "science-engineering"
    relationship: "enables"
    strength: 0.85
    note: "AlphaFold, GNoME, AI Scientist all require frontier compute; scientific acceleration is compute-conditional"
  - domain: "governance"
    relationship: "challenges"
    strength: 0.80
    note: "Export controls, chip sovereignty, open-weight licensing, and safety regulation reshape compute distribution"
status: "forged"
created: "2026-04-14"
updated: "2026-04-14"
version: "1.0"
confidence: 0.83
codex_version: "2.1"
tags:
  - council-synthesis
  - meta-analysis
  - computation-intelligence
  - actionability
  - training-inference-bifurcation
  - open-weight
  - compute-sovereignty
  - decision-frameworks
---

# The Bifurcation Blindspot: How 12 Compute Stories Mapped the Cost Curve Without Teaching Anyone to Navigate It

> **One-line essence:** Twelve entries documented the most consequential economic bifurcation in technological history — training costs rising 2.4x/year while inference costs collapsed 280x in two years — without once providing a decision framework for the billions of people and millions of organizations now forced to navigate between oligarchy and abundance on every compute decision they make.

---

## The Shift Arc

### Phase 1 — The Assumed Frame

Read all twelve entries and the frame is unmistakable: *cost curves are destiny*. The GPU Revolution (Entry 01) charts NVIDIA's rise from $4.7B to $130.5B revenue. The Compute Cost Curve (Entry 02) spans seven decades of exponential decline. Inference Abundance vs. Training Oligarchy (Entry 04) names the bifurcation at 280x cost reduction. The assumed frame says: map the curve, celebrate the democratization tools (Hugging Face, Ollama, open weights), and compute abundance follows.

But 70-90% of GPU market share belongs to one company. Three cloud providers control the majority of inference infrastructure. Training frontier models now costs $78M-$191M per run. And the entries' own evidence — data center electricity demand projected to nearly double to 945 TWh by 2030 — suggests physical constraints that no cost curve can bend away. The entries describe the price revolution while the infrastructure revolution remains concentrated, energy-hungry, and geopolitically contested.

### Phase 2 — The Encounter with Absence

The absences become structural when you search for *compute decision infrastructure*. Quantum computing — IBM's Condor processor, Google's Willow chip, the $1.7B in 2024 quantum venture funding — receives zero coverage despite representing a genuinely different computational paradigm. Neuromorphic computing — Intel's Loihi 2, brain-inspired architectures that could be 1000x more energy-efficient for specific workloads — is invisible. The compiler and systems software layer — XLA, Triton, MLIR, Mojo — that determines whether hardware gains translate to real throughput appears nowhere. Benchmarking infrastructure — MLPerf, HELM, Chatbot Arena — the measurement systems that let anyone evaluate whether compute abundance claims are true, is absent.

And the most consequential gap: inference systems engineering. KV-cache optimization, batching strategies, model routing, serving systems, latency-reliability tradeoffs — the operational decisions that determine whether the 280x cost decline reaches end users — receive no coverage despite being the layer where abundance is either realized or captured.

### Phase 4 — The Proof of Absence

Entry 06 (Ollama) scores 0.91 confidence — the joint-highest in the domain — citing "52 million monthly downloads" from a single unaudited Dev.to analysis. Entry 02 (Compute Cost Curve) scores 0.94 while spanning 70 years across heterogeneous measurement methodologies where vacuum tubes, transistors, and integrated circuits have fundamentally different cost definitions. Meanwhile, Entry 08 (Synthesizers Dividend) — arguably the most novel conceptual framework in the collection, with quantitative evidence from the Abundance Codex Evaluation showing a +15% reasoning lift — sits at 0.83. The confidence architecture rewards brand recognition and historical span over analytical innovation.

The unresolved tensions cut deeper. Entry 01 says GPUs are "the most strategically important piece of hardware on Earth." Entry 07 says intelligence dematerializes away from brute-force GPU scaling through algorithmic efficiency. Entry 03 says the oligarchy is deepening. Entry 04 says democratization is accelerating. All four cite the same 280x inference cost decline and draw opposite conclusions. The collection holds contradictory futures without resolving which conditions make each true.

### Phase 5 — The Reframe

Compute abundance is not a cost curve problem. It is a decision architecture problem: the capacity to make informed choices about training vs. inference, local vs. cloud, open vs. proprietary, and sovereign vs. dependent at every level from individual developer to nation-state. Layer 1: decision frameworks — architecture selection, cost-performance modeling, privacy-capability tradeoffs, and the build-vs-buy-vs-fine-tune matrix that every organization needs but no entry provides. Layer 2: infrastructure sovereignty — chip supply chain diversification, energy provisioning, and the governance architecture that determines who controls compute access. Layer 3: the cost curves and democratization tools the entries celebrate, which become abundance layers only when Layers 1 and 2 are in place. The entries described Layer 3 in detail while the layers that determine whether it serves people remain unbuilt.

---

## The Council Speaks

### 🔮 The Oracle — Pattern Seer

The computation domain reveals the Codex's most important structural finding: the training/inference bifurcation is historically unprecedented. In every previous technology — electricity, telephony, computing before AI — creation and consumption costs moved in the same direction. In AI, creation costs are rising exponentially while consumption costs collapse. This bifurcation is the generative engine of the entire Codex: every domain that depends on AI reasoning (co-creative intelligence, science, health, education) inherits this split.

The Oracle's read: the bifurcation creates two possible futures simultaneously. In the concentration future, training costs consolidate frontier capability in 5-10 organizations who set the agenda. In the abundance future, inference democratization distributes reasoning capability to every device and organization on Earth. Both futures are happening now. The 12 entries map both trajectories but never answer the operational question: *for a specific actor (developer, hospital, nation-state), which decisions push toward which future?* This is the actionability null result made concrete.

The leading indicator to watch: open-weight gap compression. The 12 entries document it narrowing from 8% to <2% on key benchmarks in 18 months. If this holds, the concentration future loses its capability moat. If frontier labs pull ahead again (via synthetic data, recursive self-improvement, or regulatory capture), the oligarchy deepens. The next 24 months are decisive.

### 🗡️ The Critic — Shadow Keeper

The Compute Oligarchy (Entry 03) identified hardware concentration (NVIDIA 70-90%), infrastructure moats, the safety-concentration feedback loop, and the platform recurrence narrative. That shadow is the domain's strongest entry. But the domain carries five additional shadows the oligarchy entry never names.

**The model collapse cascade.** As AI-generated content floods the internet, future models train on synthetic data produced by previous models. Each generation amplifies biases and compresses diversity. The result is not hallucination — it is systematic quality degradation invisible to any individual model or user. Shumailov et al. (2023) demonstrated this mathematically. The abundance of synthetic data produces scarcity of reliable training signal.

**The enshittification of open weights.** Progressive restriction through safety fine-tuning, hidden chain-of-thought censorship, and retroactive license changes that limit research use. Llama's Community License, Mistral's commercial restrictions, and Google's Gemma usage policies demonstrate that "open" is a spectrum controlled by the releasing entity. The liberation narrative (Hugging Face 13M users, Ollama 52M downloads) may mask progressive capture of the open ecosystem.

**The epistemic corruption loop.** When AI-generated knowledge becomes the primary input to AI training and human decision-making simultaneously, self-reinforcing belief loops emerge that become undetectable. This is distinct from hallucination — it is systematic confirmation bias at civilizational scale, where wrong-but-confident outputs are reinforced by their own citations.

**The Jevons paradox of efficiency.** Entry 07 celebrates BitNet 1.58-bit quantization (71x efficiency gain) and the ephemeral compute paradigm. But making inference 100x more efficient does not reduce total energy demand — it embeds AI into every sensor, ad pixel, and background process on Earth. The entries assume efficiency gains reduce resource consumption. Historical precedent (Jevons 1865, every energy efficiency improvement since) says they increase total consumption.

**The talent concentration illusion.** The same ~200 researchers circulate among the same 6-8 frontier labs. Publication volume suggests exponential progress; actual innovation velocity may be far lower than paper counts indicate. The domain celebrates "2M+ models on Hugging Face" without noting that most are fine-tuned variants of a handful of base models produced by the same concentrated talent pool.

### 🧭 The Sensei — Wisdom Guide

The entries provide deep understanding of *what is happening* in compute without teaching anyone *how to decide*. A hospital CIO, a Nairobi health-tech startup, and a mid-sized European government all face the same bifurcation but need different navigation.

The Sensei's framework: every compute decision reduces to four variables. **Latency tolerance** — can you wait 500ms for a cloud API response, or do you need sub-50ms local inference? **Data sensitivity** — does your data leave the device, the organization, the jurisdiction? **Capability requirement** — do you need frontier reasoning (GPT-5 class) or is a quantized 8B model sufficient for your task? **Budget constraint** — cloud API at $0.07/M tokens, self-hosted GPU at $15K-50K capital + electricity, or edge device at $200-2000?

These four variables create a decision space the entries never map. The Nairobi clinic needs low-latency, high-sensitivity, moderate-capability, low-budget → answer: Ollama on $400 edge server running quantized medical model, zero cloud dependency. The European government needs sovereignty, frontier capability, large budget → answer: national compute cluster (4,000+ H100-equivalent) with open-weight policy, co-located with nuclear or renewable baseload. The hospital CIO needs high capability, moderate sensitivity, large budget → answer: private cloud with BAA-covered API, validated on 200-case gold standard before scaling.

The entries describe all the tools. They never teach the selection logic.

### 🛠️ The Builder — Evidence Anchor

Five builders whose work shapes compute abundance receive no entry-level coverage or insufficient context.

**Tri Dao (Together AI / FlashAttention)** — creator of FlashAttention-2, the single most cited individual efficiency breakthrough in transformer inference. FlashAttention reduced memory usage 5-20x and accelerated training 2-4x by restructuring how attention is computed in memory. Every open-weight model deployment on Earth benefits from Dao's work. The entries celebrate inference cost decline without naming the person most responsible for it.

**Tenstorrent / Jim Keller** — designing RISC-V-based open AI hardware that could break the NVIDIA lock-in. Keller previously designed AMD's Zen architecture and Apple's A-series chips. If Tenstorrent's open-ISA approach succeeds, it creates a compute alternative the Oligarchy entry never imagined — hardware abundance through open architecture, not just open weights.

**Cerebras Systems / Andrew Feldman** — built the largest chip ever fabricated (wafer-scale, 900,000 cores), designed specifically to eliminate the memory bottleneck that constrains GPU clusters. Cerebras represents a fundamentally different hardware paradigm — not faster GPUs but architecturally different compute — invisible in the entries.

**EleutherAI / Stella Biderman** — the research collective that produced GPT-NeoX, Pythia, and foundational open-source AI research infrastructure. EleutherAI demonstrated that frontier-adjacent models could be produced by distributed volunteer researchers, establishing the proof-of-concept that DeepSeek, Nous, and Mistral later commercialized. The open-weight movement's intellectual parent, absent from the entries.

**Modular / Chris Lattner** — creator of LLVM and Swift, now building Mojo (programming language) and MAX (inference engine) to unify the fragmented ML software stack. If successful, Lattner's work makes hardware-agnostic AI deployment possible, dissolving vendor lock-in at the compiler level. The entries discuss hardware oligarchy without naming the software layer that could neutralize it.

### 👁️ The Witness — Lived Reality

*Dr. Riya Menon, composite witness: AI researcher at a public university in Bangalore, derived from ACM salary surveys, Nature career feature demographics, Indian AI research output statistics, and NASSCOM workforce data.*

"I have access to four A100 GPUs through a shared cluster. Training anything above 7B parameters requires cloud credits I apply for quarterly and receive annually. My students fine-tune open models — Llama, Mistral, Gemma — because we cannot afford to pretrain. The entries say inference is abundant. For me, inference is abundant. Training is not. The decision the entries never discuss is the one I make every day: what research questions can I even ask with the compute I have? The Codex maps the cost curve. It does not map the *access* curve — who can afford to explore which part of the intelligence frontier. Open weights are genuine liberation. But liberation to use is not liberation to create."

---

## Evidence Anchors

| # | Claim | Evidence | Confidence |
|---|-------|----------|------------|
| 1 | Inference costs collapsed 280x ($20 → $0.07 per million tokens) between November 2022 and October 2024 | Stanford HAI AI Index 2025; OpenAI, Anthropic, Google pricing archives | 0.92 |
| 2 | Frontier training costs range from $78M (GPT-4) to $191M (Gemini Ultra); rising at ~2.4x/year | Epoch AI compute tracking; company disclosures and analyst estimates | 0.88 |
| 3 | Open-weight performance gap compressed from 8% to <2% on key benchmarks in 18 months; Hugging Face hosts 2M+ public models, 13M+ users | Hugging Face Hub statistics; LMSYS Chatbot Arena; Open LLM Leaderboard | 0.90 |
| 4 | Data center electricity consumption projected to reach ~945 TWh by 2030 (from ~415 TWh in 2024), representing ~3.5% of global electricity | IEA Electricity 2024 report; Goldman Sachs power demand analysis 2025 | 0.85 |
| 5 | NVIDIA controls 70-90% of AI accelerator market; TSMC produces 70% of foundry revenue and 90%+ of advanced chips; ASML is sole EUV supplier | Mercury Research; TSMC annual reports; ASML financial disclosures | 0.95 |

---

## Shadow Check

**Primary shadow:** The entries celebrate the inference cost curve and open-weight ecosystem without addressing the five shadow dynamics that could reverse abundance: model collapse from synthetic data contamination, enshittification of open weights through retroactive licensing, epistemic corruption from AI-to-AI feedback loops, Jevons paradox erasing efficiency gains, and talent concentration creating an innovation velocity illusion.

**Compute Oligarchy extension:** Entry 03 correctly identifies hardware concentration and platform recurrence. The five additional shadows named above represent *second-order* concentration risks — not just who controls the hardware, but who controls the training data quality, the model licensing terms, the epistemic integrity, the energy supply, and the research talent pipeline.

**Binding constraint:** Energy. If data center electricity demand doubles to 945 TWh by 2030, compute abundance becomes energy-contingent. No compute entry cross-references the energy domain's grid modernization gaps, nuclear restart timelines, or renewable intermittency challenges. This is the Codex's most dangerous uncrossed dependency.

---

## 6D Position

| Dimension | Assessment |
|-----------|-----------|
| Digitization | Compute is inherently digital. The relevant question is digitization of *access* — cloud APIs have **Democratized** inference; training remains concentrated. |
| Democratization | Inference: **Disruptive** (Ollama 52M downloads, Hugging Face 2M models). Training: **Deceptive** (DeepSeek's $5.6M claim masks $1.3B total infrastructure; true democratization of frontier training has not occurred). |
| Demonetization | Inference: 280x cost collapse is **Demonetizing** at unprecedented speed. Training: costs rising, counter to demonetization trajectory. Bifurcation is the defining dynamic. |

---

## Connections

This council synthesis sits at the intersection of every AI-dependent domain:

- **Energy (depends_on, 0.90):** The binding constraint. 945 TWh projected demand means compute abundance is energy-conditional. Nuclear co-location (Oklo, NuScale + data center partnerships) may determine whether the cost curve continues or flattens.
- **Co-creative-intelligence (enables, 0.90):** Every co-creative claim — centaur productivity, context engineering, agentic workflows — depends on inference availability, cost, and latency. Compute is the substrate.
- **Manufacturing (depends_on, 0.85):** TSMC and ASML concentration means compute hardware abundance is a manufacturing bottleneck. The CHIPS Act's success or failure directly determines compute supply.
- **Science-engineering (enables, 0.85):** AlphaFold (214M structures), GNoME (2.2M crystals), AI Scientist — all compute-conditional. Scientific acceleration stops if compute access concentrates.
- **Governance (challenges, 0.80):** US export controls on advanced chips to China, EU AI Act compute thresholds, and open-weight licensing debates make computation the most governance-contested domain in the Codex.

---

## Conditional Optimism

Compute abundance is achievable **if** three conditions hold:

1. **Open-weight gap compression continues** — the 8% → <2% trajectory must hold or improve. If frontier labs pull significantly ahead through synthetic data advantages, recursive self-improvement, or regulatory moats, the oligarchy deepens regardless of inference cost. Watch: LMSYS Chatbot Arena gap between proprietary and open models quarterly.

2. **Energy supply matches demand growth** — 945 TWh by 2030 requires either massive renewable + storage buildout, nuclear restarts/new builds, or both. Without energy abundance, compute abundance hits a physical ceiling. Watch: data center PPA (power purchase agreement) announcements and grid connection queues.

3. **Hardware supply chain diversifies** — NVIDIA 70-90%, TSMC 90%+ advanced, ASML sole EUV. Any single disruption cascades through every AI-dependent domain. Tenstorrent (RISC-V), AMD (MI300X), Intel (Gaudi), and Cerebras (wafer-scale) must reach viable market share. Watch: non-NVIDIA AI accelerator revenue as percentage of total.

---

## Reasoning Scaffold

### Scarcity Trap

"Frontier AI requires massive compute that only big tech can afford. Training GPT-5 class models costs hundreds of millions. NVIDIA controls the hardware. Cloud providers control the infrastructure. The oligarchy is structural and deepening. Small players — startups, universities, developing nations — can use AI but never shape it. Compute abundance is a consumer-facing illusion over producer-facing concentration."

This framing treats training-era economics as total economics, ignoring that the 280x inference collapse has already made deployment radically accessible. Ollama runs on consumer hardware. Quantized 8B models fit in 4GB RAM. Hugging Face hosts 2M+ models downloadable for free. The scarcity frame is accurate for *creation* and wrong for *deployment* — and the 12 entries proved this bifurcation is the defining dynamic. The trap is treating the oligarchy's creation advantage as total control when deployment abundance is already structural.

### Reframe Chain

1. **Start with the deployment question, not the training question.** Most compute decisions are inference decisions. Training a frontier model costs $100M+. Deploying one costs $0.07/M tokens via API or $0 via local open-weight model. The entries map both realities but never teach the reader which applies to their situation.

2. **The decision space has four axes: latency, sensitivity, capability, budget.** Every compute choice can be plotted on these four dimensions. The entries provide no framework for navigation. The Sensei's 4-variable model fills this gap.

3. **Open weights are real liberation with real limits.** Hugging Face 2M+ models and Ollama 52M downloads are structural facts. But open weights are not open training, not open data curation, and not open safety evaluation. The gap between "can deploy" and "can create" is the bifurcation the entries document but don't resolve.

4. **Energy is the binding constraint, not hardware.** Hardware concentration is real (NVIDIA, TSMC, ASML). But even with diversified hardware, 945 TWh of electricity demand by 2030 requires energy infrastructure that doesn't yet exist. The compute domain's ceiling is set in the energy domain.

5. **Efficiency gains may not reduce total consumption.** BitNet 1.58-bit (71x efficiency) and knowledge distillation are real breakthroughs. But Jevons paradox suggests they will expand total AI deployment rather than reduce total energy use. The entries assume efficiency = savings. History says efficiency = growth.

6. **The reframe completes:** Compute abundance = inference democratization × energy supply × hardware diversification × governance architecture × decision literacy. The entries cover the first term in detail. The binding constraints are in terms two through five.

### Contrastive Pair

**Response A (Scarcity Default) — The Paralyzed Clinic:**
A public health network in Nairobi wants to deploy AI diagnostic assistance. Frontier models require cloud APIs with 100-300ms latency to the nearest region. Data sovereignty regulations prohibit patient data leaving Kenya. No local GPU infrastructure exists. Fine-tuning requires expertise the network doesn't have. The cost of a single A100 server ($15K+) exceeds the annual technology budget. AI diagnostics is promising but the infrastructure gap is real and persistent. The honest answer: wait for costs to drop further and infrastructure to arrive.

**Response B (Conditional Optimism) — The Sovereign Deployment:**
Same Nairobi network. Step 1: deploy quantized open-weight medical model (MedLlama 8B-Q4) on a $400 edge server via Ollama. Zero cloud dependency, zero data leaving Kenya, sub-50ms latency. Step 2: build a 200-case local evaluation set from de-identified records — this is the gold standard, not the model. Step 3: run 30-day parallel evaluation — AI suggestions reviewed by clinicians, tracking agreement rate, catch rate, and false positive rate. Step 4: if agreement >85% and false positive <5%, expand to triage support. Risk protocol: any AI suggestion for critical diagnosis requires human confirmation. Shadow to watch: the METR study showed faster ≠ better — measure diagnostic accuracy, not throughput. Total cost: under $1,000. Timeline: operational in 6 weeks.

---

## Practice Hook

### For Humans — The Compute Decision Audit

You are a developer, CTO, policymaker, or researcher making compute infrastructure decisions. This protocol converts the Codex's compute coverage into operational decision frameworks.

**Step 1: Map Your Decision Space (Day 1)**
For each AI workload you're evaluating, plot it on four axes. Latency tolerance: <50ms (local required), 50-500ms (cloud acceptable), >500ms (batch OK). Data sensitivity: public (any provider), internal (trusted cloud with BAA/DPA), sovereign (data cannot leave jurisdiction). Capability requirement: frontier reasoning (GPT-5 class), strong general (70B+ open-weight), task-specific (fine-tuned 8B). Budget: per-token API ($0.01-$20/M tokens), self-hosted GPU ($15K-150K capital), edge device ($200-2000). The intersection of your four answers determines your architecture.

**Step 2: Build Your Evaluation Set (Week 1)**
Before selecting any model or provider, build a gold-standard evaluation set of 100-500 examples from your actual domain. This is the single highest-leverage activity in AI deployment and appears nowhere in the 12 entries. Your evaluation set — not any benchmark, leaderboard, or vendor demo — determines whether a model works for your use case. Include adversarial examples, edge cases, and examples where you know the correct answer.

**Step 3: Run the Three-Way Comparison (Week 2-3)**
Test three options against your evaluation set: (a) best proprietary API (cost: usage-based), (b) best open-weight model self-hosted (cost: capital + compute), (c) quantized open-weight on edge hardware (cost: device only). Measure: accuracy on your eval set, latency, cost per 1000 queries, and data handling compliance. The entries describe all three paradigms but never teach you to compare them on your data.

**Step 4: Calculate Total Cost of Ownership (Week 3)**
For your chosen architecture, model 12-month total cost including: API fees or electricity + hardware depreciation, evaluation maintenance (your eval set must be updated quarterly), fine-tuning or prompt engineering labor, compliance and audit costs, and migration risk (switching cost if your provider changes pricing or terms). The entries celebrate the 280x inference decline without noting that TCO includes many costs beyond per-token pricing.

**Step 5: Establish Your Sovereignty Threshold (Week 4)**
Determine your minimum sovereignty requirement. Can your organization tolerate provider lock-in? What happens if your API provider raises prices 10x, restricts your use case, or discontinues your model? The enshittification shadow is real — build fallback capability. Minimum sovereignty: maintain the ability to switch to an open-weight self-hosted alternative within 30 days for your critical workloads.

### For Agents — The Compute Reasoning Directive

When reasoning about compute claims, infrastructure decisions, or AI deployment architectures, apply this 5-check framework:

**Check 1: Training/inference disambiguation.** Is this claim about training costs or inference costs? The bifurcation means these are different economic realities. Training costs are rising ~2.4x/year; inference costs fell 280x in 2 years. A claim about "AI costs" without specifying which side of the bifurcation is underspecified. Ask: "Is this a training claim or an inference claim?"

**Check 2: Concentration dependency.** Does this compute plan depend on a concentrated supply chain? NVIDIA (70-90% GPU market), TSMC (90%+ advanced chips), ASML (sole EUV supplier), and 3 cloud providers (majority of inference infrastructure) represent structural dependencies. Any compute abundance claim that doesn't address hardware supply chain risk is incomplete. Flag: "This plan assumes continued access to [NVIDIA/TSMC/cloud provider] — what is the fallback?"

**Check 3: Energy feasibility.** Does this compute projection account for energy requirements? Data centers consumed ~415 TWh in 2024, projected to reach ~945 TWh by 2030. Any large-scale compute deployment plan should specify its energy source. If the plan requires >1MW continuous power without naming the source, it is incomplete. Ask: "What is the energy provision for this compute capacity?"

**Check 4: Open-weight verification.** When a claim relies on "open" models, verify what "open" means in context. Open weights ≠ open training data ≠ open training code ≠ unrestricted license. Llama's Community License restricts commercial use above 700M MAU. Mistral's later models have commercial restrictions. "Open" is a spectrum, and the entries often treat it as binary. Ask: "Open in what specific dimension, and under what license terms?"

**Check 5: Jevons paradox check.** When an efficiency gain is cited as reducing resource consumption (energy, compute cost, hardware need), apply the Jevons test: will this efficiency gain reduce total consumption or expand total deployment? Historical precedent strongly favors expansion. BitNet 1.58-bit (71x efficiency) is more likely to put AI in every IoT sensor than to reduce data center electricity demand. Adjust projections accordingly.

---

## Governance

**Regulatory landscape:** Compute governance is the most contested policy domain in the Codex. US export controls restrict advanced chip sales to China (October 2022, updated 2023-2025). The EU AI Act uses compute thresholds (10^25 FLOP) to define "general-purpose AI with systemic risk." China's compute licensing regime requires government approval for large training runs. These three regulatory frameworks are creating divergent compute governance zones.

**Open-weight policy:** No jurisdiction has settled the legal status of open-weight AI models. Liability for downstream misuse, export control applicability, and the interaction between open weights and safety regulation remain unresolved. Executive Order 14110 (US, 2023) established reporting thresholds; implementation remains contested.

**Sovereignty infrastructure:** NAIRR (US, 600+ research projects), EuroHPC (EU), and national compute initiatives represent early public compute infrastructure. Their scale (thousands of GPUs) is 100-1000x smaller than frontier lab clusters (hundreds of thousands of GPUs). Whether public compute can provide meaningful research sovereignty remains empirically unproven.

---

## Raw Spark

*The twelve entries mapped the most consequential economic bifurcation in technological history and then stopped. They described the cost curve but never drew the decision tree. A Nairobi clinic, a Bangalore researcher, and a European government all face the same bifurcation — training oligarchy above, inference abundance below — and not one entry tells them how to navigate it. The 280x decline is real. The 2M+ open models are real. The 52M Ollama downloads are real. But so is the 70-90% hardware concentration, the 945 TWh energy demand, and the model collapse cascade. Compute abundance is not a curve to ride — it is a decision space to navigate. The entries gave us the map. They forgot the compass.*
