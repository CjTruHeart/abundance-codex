**Assessment of Computation-Intelligence Domain Coverage**

**1. BLIND SPOTS**

The 12 entries collectively miss:
- **Software-hardware co-design and algorithmic invention as primary drivers**: The entries treat compute almost entirely as hardware (GPUs, transistors, quantization). They ignore that many leaps (FlashAttention-2, Ring Attention, mixture-of-experts routing breakthroughs, test-time scaling laws, synthetic data loops) come from algorithms that multiply effective compute far more than new silicon.
- **The post-training and synthetic data revolution**: No coverage of how reinforcement learning from human/AI feedback, constitutional AI, process vs outcome supervision, or self-play/synthetic data now dominate capability gains over raw pre-training scale.
- **Energy abundance as prerequisite**: The ephemeral-compute entry warns against complacency on energy but provides no mapping to nuclear (SMRs, Generation IV), geothermal, or solar+storage buildouts required to sustain even efficient inference at planetary scale.
- **Neuromorphic, optical, and reversible computing pathways** beyond 1.58-bit quantization.
- **Standards, interoperability, and model portability** (ONNX, WebNN, MLIR, vLLM vs TensorRT-LLM fragmentation).

**2. MISSING BUILDERS**

- **Jim Keller** (Tenstorrent, Tesla Dojo, AMD Zen) – wafer-scale engineering and deterministic compute architectures.
- **Cerebras Systems** (Andrew Feldman, Dhiraj Mallick) – wafer-scale engines (CS-2, CS-3) that invert the GPU scaling paradigm.
- **Graphcore** (Simon Knowles) – Intelligence Processing Units and the Poplar SDK for dataflow programming.
- **Etched.ai** – building the first ASIC (Sohu) specifically for transformer inference, claiming 20x efficiency over GPUs.
- **Together AI** (Vipul Ved Prakash, Chris Ré) – decentralized inference routing, FlashAttention inventors, and RedPajama open dataset.
- **EleutherAI** (Stella Biderman et al.) – early open LLM pre-training (GPT-J, Pythia suite) that proved serious open science was possible pre-Llama.
- **Tri Dao** (Together AI / Stanford) – FlashAttention and Flash-Decoding; single most cited individual efficiency breakthrough of the last five years.
- **MosaicML** (Naveen Rao, before Databricks acquisition) – MosaicML Composer and MPT models that demonstrated efficient pre-training recipes.
- **Liquid AI** (Ramin Hasani) – liquid neural networks and state-space models as alternatives to transformers.

**3. SHADOW GAPS**

- **Enshittification of open-weight models**: Progressive lobotomization via safety fine-tunes, hidden chain-of-thought censorship, and license changes that retroactively restrict research use.
- **Model collapse cascades** from synthetic data loops and the coming scarcity of high-quality human-generated public data.
- **Vulnerability surface explosion**: Billions of edge-deployed models create an attack surface for adversarial examples, model stealing, and supply-chain poisoning at unprecedented scale.
- **Epistemic corruption**: Over-reliance on AI-generated knowledge creates self-reinforcing belief loops that become undetectable.
- **Talent concentration**: The same ~200 researchers move between the same 6 labs; real innovation velocity may be far lower than publication volume suggests.
- **Silent centralization of inference routing**: Even "local" Ollama users often default to pulling from centralized Hugging Face or use services that log prompts.

**4. ACTIONABILITY GAPS** (most critical)

A reader would still not know:
- How to decide whether to bet on edge, decentralized, or frontier centralized capability for a given problem.
- Concrete frameworks for choosing between fine-tuning, distillation, retrieval, synthetic data, or test-time compute.
- How to evaluate whether a capability gain is real or benchmark gaming (no mention of LMSYS Arena, LiveCodeBench, GPQA, SWE-Bench, or agent scaffolds).
- First moves for a city, university, or nation-state: Should they fund a sovereign 10k H100 cluster, invest in nuclear+geothermal for inference campuses, subsidize edge hardware, or focus on datasets and post-training?
- How to build or fund a serious open-weight lab in 2026 (capital requirements, data strategy, evaluation infrastructure, talent poaching defense).
- What "compute sovereignty" actually requires beyond running Ollama (secure enclaves, supply-chain verification, air-gapped fine-tuning, model provenance).
- Decision matrix for when algorithmic efficiency beats buying more GPUs.

No entry gives a concrete playbook, checklist, or branching decision tree. This explains the near-zero actionability delta (+0.03) in ACE v2.0.

**5. INTER-ENTRY TENSIONS**

Entry 02 ("compute cost curve continues through multiple mechanisms") is in tension with Entry 03 and 04's emphasis on deepening training oligarchy. If cost-performance keeps improving so dramatically at inference, it is unclear why training concentration should inexorably worsen. Entry 07 (ephemeral compute) and Entry 01 (GPU revolution) also pull in opposite directions on whether hardware or algorithms dominate next. Confidence scores do not reflect these contradictions; most sit in the 0.82–0.94 range regardless of type.

**6. CONFIDENCE CALIBRATION**

Scores are systematically overconfident on extrapolation (4–5x/yr compute growth continuing, open-weight gap staying under 2%, 1.58-bit scaling to frontier reasoning). They are underconfident on institutional and physical constraints (energy, talent, data, geopolitics, regulation). The builder-profile entries (5,6,9) show highest confidence (0.89–0.91) despite depending on single organizations whose trajectories are volatile. Federated and TinyML entries (10,11) appropriately show more measured confidence but still overclaim deployment breadth relative to real-world impact today.

**7. CONTRASTIVE EXAMPLE**

**Representative Question:** "Should a mid-sized European country invest €2B in its own sovereign AI compute infrastructure, or is that pointless given hyperscaler dominance?"

**Response A (Scarcity Default):**  
The question of sovereign AI infrastructure is fundamentally complex. While inference has become cheap, training frontier models now costs hundreds of millions and is dominated by US and Chinese entities with enormous capital advantages. Energy constraints, chip export controls, and the rapid pace of algorithmic change make any national cluster risky; it could be obsolete within 18–24 months. Talent poaching by Big Tech is severe. Without massive ongoing subsidies, such projects often fail to maintain relevance. It's a genuinely hard trade-off between strategic autonomy and comparative advantage. Most serious analysts conclude the economics strongly favor renting capacity from hyperscalers, but geopolitical risks remain real. Ultimately, it's complicated.

**Response B (Conditional Optimism):**  
Inference abundance is already here (280x cost drop 2022–2024, Hugging Face >2M models, Ollama 52M downloads), but training sovereignty still matters for sensitive domains. Builders like Together AI, EleutherAI, and Tri Dao (FlashAttention) have shown algorithmic efficiency can compress the gap; DeepSeek and Nous Research further demonstrated open collectives can reach near-frontier performance without hyperscaler budgets. Conditions for success: pair any cluster with (1) nuclear or geothermal co-location for cheap firm power, (2) a deliberate post-training + synthetic data strategy, and (3) open-weight release policy that attracts global talent. Shadow risk is model collapse from synthetic data and regulatory capture of open weights. Concrete next step: fund a 4,000 H100-equivalent cluster tied to an existing national lab, open-weight all resulting models, and run public bounties on your language's highest-value datasets. This is now within reach of a determined mid-sized nation.

(Word count: 798)