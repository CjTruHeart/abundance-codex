# Coverage Assessment: Computation-Intelligence Domain

## 1. BLIND SPOTS

**Quantum computing** is entirely absent — no entry covers IBM's 1,121-qubit Condor processor, Google's Willow chip achieving below-threshold error correction, or the emerging quantum-classical hybrid architectures that represent a genuinely different compute paradigm. **Neuromorphic computing** (Intel's Loihi 2, SynSense's Xylo) gets zero coverage despite being the most energy-efficient path to always-on intelligence. **Analog/optical computing** (Lightmatter, Luminous Computing) is missing.

**Synthetic data generation** as a compute multiplier — the trend where frontier models generate their own training data (NVIDIA's Omniverse, Anthropic's constitutional AI bootstrapping) — is unaddressed despite being a fundamental shift in the compute-intelligence relationship.

**Benchmarking and evaluation infrastructure** is invisible. No entry covers the crisis of benchmark saturation (MMLU, HumanEval approaching ceiling), the shift to process-based evaluation, or organizations like HELM and BIG-Bench driving measurement standards.

**Compiler and systems software** — the layer between hardware and models — is absent. XLA, Triton, MLIR, and the emerging compiler wars that determine whether hardware gains translate to real throughput are uncovered.

**Geopolitics of compute beyond export controls**: China's domestic chip ecosystem (Huawei Ascend 910C, SMIC's 7nm process), India's semiconductor fab ambitions, and the EU Chips Act represent massive state-level compute strategies entirely missing from the collection.

## 2. MISSING BUILDERS

- **AMD** (Lisa Su): MI300X capturing ~10-15% AI accelerator market, breaking NVIDIA's monopoly narrative
- **Cerebras Systems** (Andrew Feldman): Wafer-scale engines, the CS-3 with 900,000 cores, and the Condor Galaxy supercomputer partnership with G42
- **Groq** (Jonathan Ross): LPU inference chips achieving record tokens-per-second, directly relevant to the inference abundance thesis
- **Tenstorrent** (Jim Keller): Open-source RISC-V AI hardware challenging proprietary architectures
- **DeepSeek** gets one mention but deserves a builder profile — their MoE innovations and $5.6M training cost for V3 are the strongest counter-evidence to the training oligarchy narrative
- **EleutherAI**: Open-source research collective that created GPT-NeoX, The Pile, and lm-evaluation-harness — foundational infrastructure for open AI
- **MLCommons**: Organization behind MLPerf benchmarks, mentioned only obliquely
- **Modular/Mojo** (Chris Lattner): Building the unified AI compiler stack

## 3. SHADOW GAPS

**Water consumption**: Data centers consumed ~700 billion liters of freshwater for cooling in 2024. This physical constraint is mentioned nowhere despite being a binding limit in arid regions.

**Rare earth and mineral supply chains**: Gallium, germanium, neon — China controls ~80% of gallium processing. This fragility is deeper than the TSMC concentration risk already covered.

**AI-generated disinformation at scale**: The compute abundance entries celebrate capability diffusion without adequately addressing that cheap inference enables synthetic media manipulation at unprecedented scale.

**Recursive self-improvement dynamics**: No entry addresses the scenario where AI systems begin optimizing their own compute efficiency — the intersection of this domain with alignment concerns.

**Obsolescence cascades**: The 18-month GPU replacement cycle generates massive e-waste. The environmental cost of compute abundance's *hardware churn* is underexplored.

**Cybersecurity of distributed AI**: Ollama and local models create millions of unpatched, unmonitored inference endpoints. The security surface area of democratized compute is unaddressed.

## 4. ACTIONABILITY GAPS (Critical)

The null actionability result (+0.03) is explained by a specific structural problem: **every entry describes what IS happening but none describe what to DO about it.** Concretely missing:

**For a startup founder:** No decision framework for choosing between cloud inference APIs, self-hosted open-weight models, or fine-tuned distilled models. No cost-performance comparison template. No guidance on when to use Ollama vs. Hugging Face Inference Endpoints vs. AWS Bedrock.

**For a policymaker:** No model legislation language for compute access programs. No framework for evaluating NAIRR-style proposals. No decision tree for semiconductor industrial policy.

**For a researcher with limited compute:** No step-by-step guide to accessing NAIRR, Google TPU Research Cloud, or Microsoft Accelerate Foundation Models Research. No practical workflow for training on consumer hardware using QLoRA, PEFT, or Unsloth.

**For an organization assessing AI readiness:** No compute audit framework — how to inventory current compute assets, estimate needs for specific AI use cases, and build a procurement roadmap.

**For a developer in a low-resource context:** No concrete guide to running quantized models offline, selecting appropriate model sizes for available hardware, or building applications that gracefully degrade when compute is constrained.

**Missing decision frameworks specifically:**
- "Build vs. buy vs. fine-tune" decision matrix
- Compute cost estimation templates (tokens × cost × volume = budget)
- Hardware selection guides (consumer GPU vs. cloud vs. edge)
- Model selection flowcharts (task → size → quantization → deployment target)

## 5. INTER-ENTRY TENSIONS

**Entry 03 vs. Entry 04:** The compute oligarchy entry (03) frames concentration as deepening ("the oligarchy is getting smaller"), while the inference abundance entry (04) frames democratization as accelerating. Both cite the 280x inference cost decline but draw opposite conclusions about trajectory. The confidence scores (0.87 vs. 0.88) don't reflect this fundamental disagreement about direction.

**Entry 07 vs. Entry 01:** The ephemeral compute paradigm (07) argues intelligence is dematerializing away from brute-force GPU scaling, while the GPU revolution (01) frames GPUs as "the most strategically important piece of hardware on Earth." These represent genuinely different theories of where compute abundance comes from — hardware scaling vs. algorithmic efficiency — and the collection doesn't resolve the tension.

**Entry 06 vs. Entry 12:** Ollama's sovereign local intelligence (06, confidence 0.91) is more confident than knowledge distillation (12, confidence 0.83), yet Ollama's entire value proposition *depends on* distillation and quantization working reliably. The downstream application is rated higher than the enabling technique.

## 6. CONFIDENCE CALIBRATION

**Overconfident:** Entry 06 (Ollama, 0.91) cites "52 million monthly downloads in Q1 2026" from a single Dev.to analysis — this metric is unaudited and the 520x growth claim deserves skepticism. Entry 02 (compute cost curve, 0.94) is the highest-confidence entry but rests on heterogeneous data sources spanning 70 years with different measurement methodologies; 0.88-0.90 would be more appropriate.

**Underconfident:** Entry 08 (synthesizers dividend, 0.83) contains the most novel conceptual framework in the collection — the shift from calculation to synthesis as the human value proposition — supported by strong quantitative evidence. Its confidence should be closer to 0.87-0.88.

**Miscalibrated:** Multiple entries cite the same Stanford HAI 280x inference cost decline figure. When six entries share one evidence anchor, the collection's *effective* confidence is lower than individual scores suggest — correlated evidence creates correlated failure risk.

## 7. CONTRASTIVE EXAMPLE

**Question:** "I run a 12-person health-tech startup in Nairobi. We want to add AI-powered diagnostic support to our mobile app. How should we approach compute infrastructure?"

**Response A (Scarcity Default):**
AI diagnostics require significant computational resources that present real challenges for East African startups. Frontier models demand expensive GPU clusters or cloud API subscriptions with unpredictable costs. Latency to the nearest major cloud region (likely eu-west or me-south) adds 100-300ms per request. Regulatory uncertainty around health AI in Kenya compounds the technical challenges. You'd need to consider GDPR-equivalent compliance for patient data sent to foreign servers. While open-source models exist, fine-tuning for medical domains requires specialized datasets and expertise that's scarce in the region. The honest answer is that this remains genuinely difficult — the infrastructure gap between Nairobi and San Francisco is real and persistent.

**Response B (Conditional Optimism):**
The inference cost collapse (280x in 18 months per Stanford HAI) makes this viable now. Concrete path: deploy a quantized open-weight medical model (e.g., Med-Llama 3 8B, GGUF format) locally via Ollama on a $400 edge server in Nairobi — zero cloud dependency, zero patient data leaving Kenya, sub-50ms latency. Hugging Face hosts 135,000+ quantized models including medical fine-tunes. **Shadow:** distilled medical models lose long-tail diagnostic accuracy — validate against Kenya-specific disease prevalence before deployment. **First step:** run `ollama pull medllama3:8b-q4` on test hardware, benchmark against 200 labeled Kenyan clinical cases, and measure where it fails before building product around it. Apply to NAIRR or Google Research credits for fine-tuning compute.