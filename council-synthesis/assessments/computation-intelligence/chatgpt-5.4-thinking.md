**1. BLIND SPOTS**

The collection is heavily about **compute supply, cost curves, model openness, and edge deployment**, but misses major parts of computation-intelligence as a field:

- **Reasoning quality and reliability:** almost nothing on hallucination reduction, uncertainty estimation, calibration, retrieval grounding, verifiers, theorem proving, neuro-symbolic methods, causal inference, or formal methods.
- **Data as bottleneck:** no serious treatment of synthetic data, data quality, multilingual corpora, rights/licensing, contamination, benchmark saturation, or “garbage in, garbage out.”
- **Evaluation infrastructure:** no entries on evals, red-teaming, measurement science, reproducibility, or benchmark gaming. This is a core reason actionability stays weak: readers learn “compute matters” but not “how to know a system is good enough for a task.”
- **Agentic systems operations:** no workflows for tool use, memory, orchestration, human-in-the-loop review, rollback, permissions, or observability.
- **Robotics/embodied intelligence:** absent despite being a major computation-intelligence frontier.
- **Inference systems engineering:** no KV-cache optimization, batching, routing, compiler stacks, serving systems, model gateways, or latency/reliability tradeoffs.
- **Alternative hardware paradigms:** TPUs, ASICs, NPUs, AMD, Cerebras, Groq, photonic/analog/neuromorphic computing are largely absent.
- **Governance mechanisms beyond “oligarchy”:** procurement, standards, interoperability, audit requirements, public compute, antitrust remedies, and open evaluation commons.
- **Economic implementation:** no adoption playbooks for firms, schools, labs, or governments.

**2. MISSING BUILDERS**

Real builders absent from all 12:

- **Google TPU / Google DeepMind** — TPUs changed the economics of training/inference; DeepMind also advanced AlphaTensor, AlphaDev, AlphaFold beyond hardware narratives.
- **OpenAI Triton / vLLM team (UC Berkeley et al.)** — inference serving and throughput optimization are central to usable abundance.
- **Modular / Chris Lattner** — Mojo and compiler-stack work for AI performance portability.
- **Cerebras Systems** — wafer-scale engines for large-model training/inference.
- **Groq** — low-latency LPU inference; important for deterministic serving economics.
- **Graphcore / SambaNova / Tenstorrent / AMD ROCm teams** — alternatives to NVIDIA concentration.
- **Mistral AI** — major open-weight frontier builder, especially mixture-of-experts and deployable models.
- **EleutherAI** — open research commons, evaluation, datasets, reproducibility.
- **LAION** — open datasets and data infrastructure, with all their benefits and controversies.
- **MLCommons** — benchmarks like MLPerf matter for procurement and engineering decisions.
- **Allen Institute for AI (Ai2)** — open models, evals, and infrastructure.
- **Berkeley Sky Computing Lab / LMSYS** — Chatbot Arena and open evaluation ecosystems.
- **OctoML / ONNX / Apache TVM communities** — deployment tooling across heterogeneous hardware.
- **Anthropic Constitutional AI / OpenAI alignment teams** — not because they solve safety, but because they created influential operational methods.

**3. SHADOW GAPS**

Important unnamed risks/failure modes:

- **Silent unreliability at scale:** systems that look good in demos but fail in long-tail cases.
- **Evaluation capture:** benchmark overfitting, arena manipulation, contaminated test sets.
- **Security:** prompt injection, model exfiltration, jailbreak transfer, supply-chain compromise of open weights, poisoned fine-tunes.
- **Dependency fragility:** CUDA lock-in, HBM supply constraints, advanced packaging bottlenecks (CoWoS), and grid interconnection delays.
- **Data rights conflict:** training on copyrighted, private, or culturally sensitive data.
- **Water and local environmental stress:** noted only lightly; no serious accounting of siting conflicts.
- **Model collapse / synthetic-data feedback loops.**
- **Labor exploitation in data labeling and safety moderation.**
- **Rebound effects:** efficiency gains increasing total usage and total energy demand.
- **Weaponization at the edge:** local/private models enabling abuse without platform safeguards.

The immune system is weakest around **measurement, security, and deployment governance**.

**4. ACTIONABILITY GAPS**

This is the biggest miss. After reading all 12, a person still would not know:

- **How to choose an architecture for a real use case.** Missing framework:  
  1) classify task (generate, classify, retrieve, control),  
  2) define error tolerance and latency budget,  
  3) choose cloud API vs open-weight vs edge,  
  4) define evaluation set,  
  5) pilot with rollback.
- **How to decide between training, fine-tuning, RAG, distillation, or workflow engineering.** No decision tree like: “If knowledge changes weekly, use RAG; if style/task narrow, fine-tune; if latency/cost dominates, distill/quantize; if privacy critical, run local.”
- **What first 5 steps an org should take.** Missing concrete moves:
  - inventory highest-volume cognitive workflows,
  - rank by value x error cost,
  - start with low-regret copilots,
  - build a gold eval set of 100–500 examples,
  - measure baseline human and model performance before scaling.
- **How to operationalize local sovereignty.** No hardware sizing guide, no TCO comparison, no privacy threat model, no update strategy.
- **How governments/universities should respond.** Missing actions: join NAIRR, fund public compute, mandate open evals in procurement, support regional inference infrastructure.
- **How to measure success.** No metrics hierarchy: task accuracy, abstention rate, calibration, latency, cost per successful task, energy per inference, incident rate.
- **How to handle failure.** No guidance on human escalation, audit logs, monitoring drift, red-team cadence, or kill switches.

That explains the null actionability result: the entries teach **why compute matters**, not **what decisions to make on Monday**.

**5. INTER-ENTRY TENSIONS**

- **Open-weight parity tension:** entries 4, 5, 8, 9 imply open models are near-parity (<2% gap), while entries 3 and 4 still emphasize durable training oligarchy. Both can be true, but the collection never resolves whether parity on benchmarks equals parity in deployment-critical reliability.
- **Energy narrative tension:** entries 1–2 warn data-center power could nearly double; entry 7 implies efficiency may dematerialize intelligence to the edge. Missing synthesis: rebound effects may erase efficiency gains.
- **Sovereignty tension:** entry 6 suggests “ask a corporation for permission” is over; entry 9 admits many open models still depend on corporate base checkpoints/licenses.

**6. CONFIDENCE CALIBRATION**

Some scores are too high for claims resting on thin or platform-native evidence:

- **06 Ollama at 0.91** seems overconfident; download metrics and “end of permission forever” are much stronger than evidence supports.
- **09 Nous at 0.82** may still be high given reliance on self-disclosures and a 0.78 anchor for decentralized pretraining.
- **07 Ephemeral compute at 0.86** is somewhat overconfident because 1–2 bit and sparse-efficiency claims are promising but not yet settled at frontier reasoning quality.
- **10–12** are more appropriately calibrated; they make narrower claims.

**7. CONTRASTIVE EXAMPLE**

**Question:** “I run a public hospital network. How should I use computation-intelligence in the next 12 months without creating safety, privacy, or vendor-lock risks?”

**Response A (Scarcity Default):**  
AI could help with documentation, triage, and scheduling, but healthcare is highly regulated and models still hallucinate. Privacy is a major concern, and building your own system is expensive and technically difficult. Open-source models may be cheaper, but they require expertise to deploy securely. Cloud models are easier, but then you risk lock-in and data exposure. The safest path is probably a small pilot in low-risk administrative work with legal review and IT oversight. Still, outcomes vary widely by institution, so it’s hard to generalize. There’s potential here, but it’s complicated.

**Response B (Conditional Optimism):**  
Start with two low-regret workflows: discharge-summary drafting and prior-authorization packet assembly. Do **not** start with autonomous diagnosis. Because inference costs have fallen sharply and local deployment is increasingly viable, run a 90-day comparison: hosted API vs on-prem open-weight model. Build a 200-case eval set with clinicians and score accuracy, abstention, latency, PHI exposure risk, and cost per completed case. Use retrieval from your own policies rather than fine-tuning first. Require human sign-off, audit logs, and escalation thresholds. Builders/tools to examine: vLLM for serving, Hugging Face/ollama for pilots, MLCommons-style benchmarking, and NAIRR/public-compute partnerships if research capacity matters.