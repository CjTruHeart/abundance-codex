1. **BLIND SPOTS**

The set is strong on productivity narratives, weak on operating models. Missing topics:

- **Workflow protocols:** no concrete patterns for when to use AI for draft, critique, decomposition, verification, retrieval, simulation, or abstention.
- **Role redesign:** no treatment of how managers, teachers, clinicians, lawyers, researchers, or product teams should rebundle work when AI enters the loop.
- **Training science:** almost nothing on how to teach co-creative skill systematically. Missing “AI literacy” curricula, deliberate-practice loops, prompt/debug/review routines, and progression ladders from novice to expert.
- **Memory and knowledge management:** no coverage of personal/team knowledge systems, retrieval pipelines, or how shared context compounds over time.
- **Interface design:** no treatment of multimodal collaboration, versioning, critique UIs, provenance, sandboxing, branch/merge for ideas, or interruptibility.
- **Reliability infrastructure:** little on eval-driven deployment, human escalation thresholds, red-teaming, sandbox-to-production gates, or task routing.
- **Domain-specific teaming:** no serious treatment of medicine, education, science, law, design, customer support, government operations.
- **Economic allocation:** heavy “centaur” optimism, little on procurement, ROI measurement, incentive design, labor bargaining, or who captures gains.
- **Cross-cultural/language inclusion:** low-resource languages and localization are mentioned only abstractly, not operationally.
- **Long-horizon collaboration:** no coverage of persistent agents, memory drift, delegation chains, or how to supervise agent swarms over weeks.

2. **MISSING BUILDERS**

Notable absent builders with concrete contributions:

- **Andrej Karpathy** — articulated the practical “LLM OS / partial autonomy” mental model and common coding-with-AI workflows; influential in developer co-creation practice.
- **OpenAI / ChatGPT + Advanced Data Analysis** — mainstreamed iterative human-AI analysis, code execution, and document collaboration at scale.
- **Anthropic / Artifacts + Constitutional AI team** — important for structured co-writing/co-building interfaces and reliance/safety research beyond the single deskilling citation.
- **Microsoft Research + Copilot Studio team** — major work on human-AI interaction guidelines, copilots in work, and orchestration tooling.
- **Stanford HAI / Fei-Fei Li, Erik Brynjolfsson, Percy Liang** — rigorous work on augmentation, foundation model transparency, and economic impacts.
- **All Hands AI / OpenHands (formerly OpenDevin)** — open-source agentic software collaboration environments.
- **Hugging Face** — open collaboration infrastructure for models, datasets, and community evaluation.
- **Label Studio / Humanloop / Arize / LangSmith (LangChain)** — builders of human-in-the-loop eval and observability infrastructure, crucial for actionable teaming.
- **Khan Academy / Sal Khan with Khanmigo** — one of the clearest applied experiments in AI as tutor/co-teacher.
- **Abridge, Nuance DAX, Nabla** — real clinical co-intelligence systems where human-AI workflow design matters more than raw model capability.
- **Pol.is founder Colin Megill / Taiwan’s Audrey Tang** are indirectly present via tools/cases, but not as builders shaping civic co-intelligence practice.

3. **SHADOW GAPS**

Missing failure modes:

- **Pseudo-collaboration:** humans become approvers of machine-made work without real understanding.
- **Context poisoning:** bad files, outdated docs, malicious retrieval, or organizational lore corrupting outputs.
- **Coordination collapse:** multiple AI agents create inconsistent assumptions, duplicate work, or hidden contradictions.
- **Accountability diffusion:** nobody owns mistakes because “the model suggested it” and “the human reviewed it.”
- **Style monoculture:** organizations converge on bland, over-optimized language/design/strategy.
- **Privacy leakage through collaboration traces:** prompts, documents, and feedback become latent surveillance data.
- **Evaluation gaming:** teams optimize acceptance rate or speed while quietly increasing latent risk.
- **Motivational atrophy:** not just deskilling, but reduced willingness to struggle, explore, and originate.
The immune system is weakest around **governance of everyday use**: review rights, escalation rules, auditability, provenance, and incentive design.

4. **ACTIONABILITY GAPS**

This is why actionability stayed flat: the entries diagnose and inspire, but rarely convert insight into executable decisions.

A reader still would not know:

- **Which tasks should be augmented vs automated vs kept human-only.**
  Missing tool: a task-routing matrix using two axes: error cost and verifiability.  
  - High verifiability/low error cost → automate  
  - High verifiability/high error cost → AI draft + mandatory human review  
  - Low verifiability/high error cost → human-led, AI only for options/critique  
  - Low verifiability/low error cost → experimentation zone

- **How to start in an organization.**
  Missing first 30 days:
  1. Pick 3 recurring workflows.
  2. Baseline time, quality, error rate.
  3. Insert AI at one step only.
  4. Define review protocol.
  5. Track output + understanding retention.
  6. Expand only if both improve.

- **How to prompt for co-creation.**
  Missing templates:
  - “Generate 3 options, state assumptions, ask 2 clarifying questions before finalizing.”
  - “Critique this draft against rubric X; do not rewrite until failure modes are identified.”
  - “Show uncertainty and what would change your answer.”

- **How to preserve human capability.**
  Missing rules like:
  - Draft with AI, finalize from memory.
  - One no-AI repetition per week for core skills.
  - Require explanation-before-acceptance for high-stakes outputs.
  - Alternate “delegate mode” and “coach mode.”

- **How to supervise agents.**
  Missing checklists for permissions, sandboxing, rollback, logging, and kill-switches.

- **How to evaluate success.**
  Missing practical KPI bundle: cycle time, defect rate, independent skill retention, override quality, trust calibration, and downstream rework.

5. **INTER-ENTRY TENSIONS**

- **Centaur optimism vs negative-synergy evidence:** entries 4/6 imply centaur is the new baseline; entry 12 cites meta-analysis showing human-AI systems often underperform the better of human alone or AI alone, especially in decision tasks.
- **Context engineering centrality vs possible obsolescence:** entry 2 says context engineering is the century’s key skill; entries 7/8 imply interfaces may abstract prompting away into conversational agentic tooling.
- **Commodity reasoning vs deskilling:** entry 9 celebrates cheap reasoning abundance; entry 3 implies cheap reasoning may increase dependence and reduce mastery.
- **Builder examples skew coding-heavy while domain claims are universal.** The software examples may not transfer cleanly to medicine, law, or education.

6. **CONFIDENCE CALIBRATION**

Some entries are overconfident relative to evidence quality:

- **07 and 08** lean heavily on vendor reports and case studies; confidence in the low 0.8s is too high.
- **06** generalizes from heterogeneous productivity studies to “new baseline unit of cognitive output”; that’s too strong.
- **09** is conceptually interesting but empirically thin; 0.78 feels high.
Underconfident:
- **12** could be slightly higher; it is one of the most evidence-grounded entries.
- **10** may also be slightly underconfident because civic deliberation evidence is stronger than many speculative productivity claims.

7. **CONTRASTIVE EXAMPLE**

**Question:** “How should a 200-person company adopt AI so teams become genuinely better, not just faster?”

**Response A (Scarcity Default):**  
Adopting AI well is difficult because outcomes vary a lot by role, tool quality, data access, and company culture. Some teams see productivity gains, but others create rework, security problems, or overreliance. You’d need training, governance, change management, and careful tool selection, especially for high-stakes work. There’s also a risk of deskilling and employee resistance. A prudent approach is to pilot a few tools, collect feedback, and iterate slowly. But there’s no universal playbook yet, and whether AI makes teams better rather than merely faster depends on many contextual factors. It’s promising, but complicated.

**Response B (Conditional Optimism):**  
Start with a **task-routing audit**, not a company-wide rollout. Evidence from BCG and Copilot studies suggests gains are real, but Vaccaro et al. shows decision tasks often have negative synergy. So classify workflows by **error cost x verifiability**. Pick 3 high-volume, verifiable workflows first. For each, baseline time, defect rate, and human understanding. Use AI in one role only at first: draft, critique, or retrieval. Require human sign-off plus explanation for high-stakes outputs. Track not just speed, but rework, override quality, and skill retention. Builders like Microsoft, Anthropic, and LangSmith provide HAI and evaluation patterns. Next step: run a 30-day pilot with explicit review rules and a rollback threshold.