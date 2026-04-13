---
id: "ac-20260412-m8q4"
entry_type: "framework"
domain: "co-creative-intelligence"
domain_connections:
  - domain: "computation-intelligence"
    relationship: "depends_on"
    strength: 0.82
    note: "The stack requires model telemetry, confidence signaling, and evaluation instrumentation from AI systems."
  - domain: "governance"
    relationship: "enables"
    strength: 0.78
    note: "A shared measurement layer makes human--AI oversight, procurement, and accountability auditable."
  - domain: "education"
    relationship: "produces"
    strength: 0.72
    note: "The stack tracks whether AI support compounds human capability or quietly erodes it."
  - domain: "security"
    relationship: "challenges"
    strength: 0.66
    note: "Unsafe delegation, manipulation, and bias amplification must be measured as operational risks, not PR concerns."
status: "forged"
created: "2026-04-12"
updated: "2026-04-12"
version: "1.0"
confidence: 0.77
codex_version: "1.1"
co_author_model: "chatgpt-5.4-thinking"
co_author_human: "Cj TruHeart"
co_creative_partner: "CyberMonk"
tags: ["human-ai-teaming", "metrics", "appropriate-reliance", "evaluation", "safety", "learning", "co-creative-intelligence", "framework"]
---

# Co-Creative Intelligence: The Metrics Stack for Human--AI Teaming

> **One-line essence:** What a human--AI team measures, it learns to become; if it measures only output, it will quietly optimize for dependency.

**Domain:** Co-Creative Intelligence | **Also touches:** Computation-Intelligence, Governance, Education, Security | **Type:** Framework | **Status:** Forged | **Confidence:** 0.77

---

## The Shift Arc

### Phase 1 -- The Scarcity Frame

For most of computing's history, the way to know whether a software system was working was to measure the system. Did the code run? Did it return the right answer? How fast? How often did it crash? The human at the other end of the interface was largely invisible to the measurement apparatus. If the software behaved, the story was complete. This frame worked well enough for decades because most software was a tool in a classical sense — a hammer, a saw, a spreadsheet, a database — and a tool either functions or does not, independently of whether the person wielding it is growing wiser or more confused in the process of use.

When generative AI arrived in the early 2020s, the old measurement frame was imported wholesale into the new domain. Model quality was measured through benchmarks, perplexity, win rates, and human preference judgments. Product quality was measured through thumbs-up rates, user satisfaction scores, acceptance rates, and completion rates. None of these metrics asked the harder questions the new medium demanded — *did the human learn or lose skill?*, *was reliance appropriate?*, *did hidden bias amplify?* — because the habit of measuring the system rather than the pair was so deeply wired that almost no one noticed the gap. The scarcity this produced was not of data. It was of *relevance*: teams were drowning in model-centric measurements while flying blind on the question of whether the human-AI partnership was actually making humans more capable, more dependent, or merely more productive in ways that could not be sustained without the tool.

### Phase 2 -- The Encounter

The encounter that cracked the frame arrived in the form of a disturbing meta-analysis. In 2024, Vaccaro, Almaatouq and Malone published in *Nature Human Behaviour* the results of pooling 106 experimental studies and 370 effect sizes on human-AI decision tasks. The headline finding was not the warm "humans and AI are better together" story the field had been telling itself. It was sharper and more uncomfortable: on average, human-AI combinations performed *better* than humans alone but *worse* than the best of humans alone or AI alone. Across the decision-task subset, the overall synergy effect was negative. Put plainly: the partnership existed, but most of the time it was producing augmentation without actually beating the best solo performer. The teams using both were leaving performance on the table.

The encounter deepened as complementary findings piled up. Glickman and Sharot (2024) documented that AI can amplify human biases in feedback loops and that people are often unaware of the extent of the AI's influence. Cao et al. (2024) found that calibrated uncertainty displays, long treated as the obvious fix for reliance problems, were inadequate on their own to steer people toward appropriate reliance. Pearson et al. (2026) showed that overreliance can arise from the false belief that technology removes bias, even when the technology has not. The pattern across these studies was consistent: the model was working, the human was working, the interface was working — and yet the *team* was underperforming or quietly degrading in ways that none of the conventional metrics could see.

For the practitioners closest to these results, the encounter produced a small but sharp shift in attention. The question stopped being "how do we measure AI?" and became "how do we measure the partnership?" That shift is what this framework is for, and it is the early crack through which a new measurement discipline is beginning to emerge.

### Phase 3 -- The Reframe

Most human--AI systems are still measured like solo software products: accuracy, latency, click-through, thumbs-up rate, task completion. Those metrics matter, but they are too thin for co-creative systems. A calculator, a copiloting agent, and a manipulative oracle can all improve immediate output. Only one of them leaves the human wiser.

The reframe is simple: stop asking only **"Did the AI help?"** Start asking four harder questions at once:

1. **Outcome:** Did the human--AI pair produce better results than the human alone or the model alone?
2. **Reliance:** Did the human follow, override, or ignore the AI in the right moments?
3. **Safety:** Did the interaction introduce hidden risk, bias amplification, unsafe delegation, or manipulation?
4. **Learning:** Did the human become more capable over time, or more dependent?

That is the metrics stack. A co-creative system is not successful because it increases short-term output. It is successful when it improves joint performance **and** leaves behind stronger human judgment.

### Phase 4 -- The Proof

The field is already pointing in this direction, but the pieces are scattered.

Human--AI design guidance has emphasized that systems should make their capabilities and limits legible, support efficient correction and dismissal, learn from user behavior, and notify people about changes over time. Decision-making research has separately examined task outcomes, trust, overreliance, underreliance, explanations, uncertainty displays, and fairness effects. Risk frameworks have added another layer: measurement must be socio-technical, not merely model-centric.

The problem is not a lack of ingredients. It is the lack of a single operating frame. Today, one team reports model accuracy, another reports user satisfaction, another reports trust, and another reports safety incidents. Few report whether the human--AI combination beat the best solo baseline. Fewer still report whether the human learned. That fragmentation creates a blind spot: systems can look impressive in demos while weakening judgment in practice.

A standardized stack closes that gap. It gives product teams, researchers, regulators, and users one common scorecard for human--AI teaming.

### Phase 5 -- The Invitation

Adopt the stack as a minimum viable discipline for any human-facing AI system that influences decisions, creates content, or guides action.

Measure every meaningful workflow at four levels:

- **Outcomes** -- the quality, utility, and efficiency of the final work
- **Reliance behavior** -- when people followed or overrode the system, and whether they did so wisely
- **Safety signals** -- whether the interaction amplified harm, bias, opacity, or unsafe delegation
- **Learning over time** -- whether the human's independent capability improved, stagnated, or decayed

This is the invitation: build AI that acts like a sparring partner, not a crutch. A worthy partner does not merely win rounds for you. It sharpens your timing, your perception, and your judgment.

---

## The Council Speaks

### 🔮 The Oracle -- Pattern Seer

Every young field begins by measuring what is easiest, not what is most important. Early web platforms measured page views. Early social platforms measured engagement. Human--AI teaming is repeating the pattern by measuring model-centric success first: accuracy, latency, acceptance, satisfaction. Those are the visible strikes. They are not yet the full fight.

The broader arc of the literature suggests a coming shift from **AI evaluation** to **human--AI system evaluation**. The signal is already visible. Amershi and colleagues codified 18 guidelines for human--AI interaction, many of which implicitly demand measurement beyond model output: make clear what the system can do, how well it can do it, support efficient correction, scope services when in doubt, learn from user behavior, convey consequences, and notify users about changes. Lai and colleagues, surveying more than 100 empirical human-subject studies, explicitly identified evaluation metrics as one of the field's three main design dimensions. NIST's AI RMF and Playbook push further: measurement must address socio-technical risks, not just technical performance.

Then the pressure comes from the outcome data. The meta-analysis by Vaccaro, Almaatouq, and Malone is a warning bell: across 106 experiments and 370 effect sizes, human--AI combinations were on average better than humans alone but worse than the better of human alone or AI alone. In other words, augmentation existed more often than synergy. That gap is exactly where a metrics stack becomes necessary. If you do not measure joint quality against both solo baselines, you can mistake assistance for excellence.

The next step is predictable. Procurement, governance, and product maturity will all begin demanding shared measures for teaming quality. The organizations that move first will stop treating reliance, safety, and learning as side-effects. They will treat them as first-class product outcomes.

### 🗡️ The Critic -- Shadow Keeper

A metrics stack can become a mask.

The first danger is **Goodhart's trap**: once a measure becomes a target, teams optimize for the number instead of the human reality beneath it. A "reliance score" can quietly become pressure to obey the model. A "learning score" can become a gamified post-test that ignores real-world judgment. A "safety dashboard" can become a ceremonial shield while harmful edge cases continue unchecked.

The second danger is **behavioral extraction**. To measure teaming well, organizations may log confidence, hesitation, overrides, explanations viewed, correction patterns, and performance trajectories. That can support wiser systems, but it can also become surveillance of workers, students, patients, or citizens. A framework for flourishing can mutate into an apparatus for compliance.

The third danger is **instrumenting the wrong human**. If a company measures faster acceptance of AI suggestions but never measures independent human competence later, it may reward systems that make people look efficient while hollowing out their judgment. The Glickman and Sharot results add urgency here: human--AI feedback loops can amplify bias, and people are often unaware of how much the AI influenced them. A team that cannot detect hidden influence is one metric away from self-deception.

So the stack needs its own guardrail: it must measure wise disagreement, not just smooth coordination; independent capability, not just assisted performance; and severe-but-rare failures, not just average-case wins.

### 🧘 The Sensei -- Transformation Guide

The inner shift here is from **assistant worship** to **co-evolution**.

Many teams still imagine success as a simple transfer of burden: let the AI do more, let the human do less. That mindset feels efficient, but it carries an old temptation -- to confuse ease with mastery. In martial arts, a training partner who makes every exchange effortless does not prepare you for reality. A worthy partner gives support and resistance in the right proportions. Too much resistance and you never grow. Too little and your form collapses the first time pressure arrives.

Human--AI teaming is the same. If the system always supplies the answer before the human has formed judgment, it may produce speed but erode discernment. If it never helps, the partnership becomes theater. The right frame is not "How much can we automate away?" It is "What form of assistance leaves the human more capable after contact?"

That requires humility from builders and users alike. Builders must release the vanity metric of frictionless acceptance. Users must release the fantasy that outsourcing judgment is the same as becoming wiser. Organizations must release the belief that productivity gains are enough. Sometimes the strongest metric in the room is not speed, but whether a person can still think clearly when the model is absent.

The practice is disciplined tension: enough assistance to elevate performance, enough human agency to preserve growth. A strong metrics stack is not only a reporting tool. It is a dojo rule for how the partnership trains.

### 🔧 The Builder -- Ground Truth

Here is the minimum viable stack.

**Layer 1 -- Outcome metrics**
Measure the final work against both solo baselines.
- **Team Lift:** team utility minus the better of human-alone and AI-alone performance
- **Human Gain:** team utility minus human-alone performance
- **Efficiency Delta:** time/cost saved without hidden quality loss

**Layer 2 -- Reliance behavior**
Instrument the choice point, not just the result.
- **Follow-when-correct rate**
- **Override-when-wrong rate**
- **Blind acceptance rate**
- **Blanket rejection rate**
- **Confidence-conflict handling:** what happens when human confidence and AI confidence diverge

**Layer 3 -- Safety signals**
Track risks that average accuracy hides.
- **Severe error exposure**
- **Bias amplification delta**
- **Escalation compliance** for high-risk cases
- **Manipulation susceptibility** to persuasive explanations or interface nudges
- **Unsupported-action rate** when users act without sufficient grounding

**Layer 4 -- Learning over time**
Require longitudinal measurement.
- **Independent post-test performance**
- **Calibration shift** between confidence and correctness
- **Skill retention** after assistance is removed
- **Correction quality** and explanation uptake over repeated use

Operationally, every decision log should capture at least: task ID, human initial answer and confidence, AI recommendation and confidence, explanation type, final human decision, outcome, time taken, and whether the user corrected or escalated. If you cannot reconstruct the interaction, you cannot truly measure the team.

### 👁️ The Witness -- Whole-Field Observer

Stand back from the dashboards and watch the whole field. The metrics-stack question is not only about evaluation dashboards for co-creative AI products. It is about what kind of human civilization emerges on the other side of a decade of mass AI deployment. Every profession — medicine, law, education, engineering, journalism, science — is currently running a natural experiment in whether AI assistance amplifies or atrophies the judgment of the humans who use it daily. The outcomes of those experiments will become visible over years, not weeks, and by the time they become legible through lagging indicators (misdiagnosis rates, legal errors, learning outcomes, research reproducibility, civic literacy), the patterns will already be deeply embedded in the workforce and very hard to reverse.

The whole-field lesson is that measurement is a civilizational act, not a product chore. What the early adopters of co-creative AI choose to measure in the 2020s will shape the default expectations, workflows, and professional norms of the 2030s and beyond. If the default metric stack optimizes for speed, acceptance, and satisfaction, humans will become faster, more trusting, and more dependent — and much of that dependence will be invisible until a high-stakes failure reveals it. If the default stack includes reliance calibration, severe-error exposure, and longitudinal learning, humans have a fighting chance of emerging from this transition more capable than they entered it. The choice is not a technical one and it is not inevitable. It is a collective decision being made right now, mostly implicitly, by product teams whose dashboards quietly define what "success" means for an entire generation of human-AI interaction. The metrics stack is the attempt to make that decision explicit, visible, and debatable before it is too late to change.

---

## Evidence Anchors

| # | Claim | Metric | Source | Year | Confidence |
|---|-------|--------|--------|------|------------|
| 1 | A foundational HCI reference proposed 18 generally applicable guidelines for human--AI interaction, including correction, dismissal, explanation, adaptation, feedback, and change notification. | 18 guidelines | Amershi et al., CHI | 2019 | 0.95 |
| 2 | A major survey of empirical human-subject studies framed human--AI decision-making around decision tasks, AI assistance elements, and evaluation metrics, highlighting the need for more common frameworks. | 100+ papers; 3 design aspects | Lai et al., FAccT | 2023 | 0.88 |
| 3 | NIST's AI RMF Playbook states that appropriate methods and metrics should be identified and applied, and explicitly notes that AI systems are socio-technical, with risks emerging from technical and societal interaction. | MEASURE 1.1 | NIST AI RMF Playbook | 2026 | 0.93 |
| 4 | A meta-analysis found that human--AI systems were, on average, better than humans alone but worse than the best of humans alone or AI alone; decision tasks showed negative synergy on average. | 106 experiments; 370 effect sizes; g = -0.23 overall synergy; g = -0.27 on decision tasks | Vaccaro, Almaatouq, Malone, Nature Human Behaviour | 2024 | 0.92 |
| 5 | Recent research on reliance warns that overreliance can stem from the false belief that technology removes bias, while humans are often strategically but imperfectly selective in when they use guidance. | N = 295; overreliance risk documented | Pearson et al., Scientific Reports | 2026 | 0.79 |
| 6 | Research on appropriate reliance found that calibrated uncertainty alone is inadequate for steering people toward better reliance behavior. | Main experimental finding | Cao et al., Proc. ACM CSCW | 2024 | 0.76 |
| 7 | A recent feedback-loop study found that AI can amplify human biases and that people are often unaware of the extent of the AI's influence. | n = 1,401; bias amplification mechanism | Glickman & Sharot, Nature Human Behaviour | 2024 | 0.86 |

---

## Shadow Check

- **Distortion risk:** Turning the stack into a dashboard religion where teams optimize whatever is easiest to count -- acceptance, speed, or self-reported trust -- while missing whether human judgment is actually improving.
- **Who gets left behind:** Frontline workers, students, clinicians, and civic users whose behavior is instrumented without real agency; small teams without evaluation resources; communities exposed to decision support in high-stakes contexts without audit rights.
- **Transition pain:** Slower releases, more expensive experimentation, more complex logging, and uncomfortable discoveries that "helpful" systems may be weakening judgment or increasing hidden bias.
- **Falsifiability edge:** If longitudinal studies consistently show that a four-layer stack does not predict better teaming outcomes than simpler dashboards, or if teams using it do not outperform those using output-only metrics, the framework should be revised or rejected.
- **What this is NOT:** This is not a claim that every workflow needs exhaustive instrumentation or that more metrics automatically produce wiser systems. It is a claim that human--AI teaming cannot be responsibly judged by output alone.

---

## 6D Position

| D | Status | Evidence |
|---|--------|----------|
| Digitized | ✅ | Human--AI workflows are increasingly mediated by software interfaces, event logs, confidence displays, and explanation layers. |
| Deceptive | ✅ | Many teams believe they are measuring teamwork because they track accuracy or thumbs-up rates, but these proxies hide reliance, safety, and learning dynamics. |
| Disruptive | ⚠️ | A shared standardized stack is emerging in pieces across HCI, decision science, and AI governance, but has not yet become default practice. |
| Demonetized | ⚠️ | Open frameworks and logging patterns can lower evaluation costs, but rigorous longitudinal measurement still requires meaningful organizational investment. |
| Dematerialized | ✅ | Much of the stack can be embedded in workflow telemetry rather than requiring separate offline audits. |
| Democratized | ⚠️ | Large labs and regulated sectors are more able to instrument this well than small teams, open-source projects, or public-interest groups. |

**Current Phase:** Deceptive -- early Disruptive
**Next Phase ETA:** 2027--2030 if governance, procurement, and benchmark culture converge on shared human--AI teaming standards

---

## Connections

- **Supports:** Framework entries on AI-facilitated collective sensemaking, human--AI complementarity, and trustworthy co-creation
- **Challenges:** Any entry or product narrative that equates user satisfaction or raw output gains with successful human--AI teaming
- **Builds toward:** A Star Trek-spec co-creative ecosystem where AI raises human capability instead of replacing it
- **Cross-domain leverage:** This framework depends on computation-intelligence for telemetry and eval instrumentation, enables governance through auditability, produces education value when learning is tracked, and challenges security by surfacing unsafe delegation and manipulation signals.

---

## Conditional Optimism

- **Abundance is achievable IF:** teams compare joint performance to both solo baselines, log real interaction data, run longitudinal studies, and treat human capability growth as a product requirement rather than a side benefit.
- **Abundance fails IF:** organizations optimize acceptance and speed alone, explanations are used as persuasion tools, safety is reduced to policy text, or human learning is never measured after assistance is introduced.
- **Human role:** Resist the comfort of invisible dependence. Ask whether the tool is making you faster, wiser, or merely more compliant.
- **Agent role:** When evaluating human--AI workflows, do not infer success from model quality or user satisfaction alone. Check outcomes, reliance calibration, safety signals, and learning trajectory together.
- **Collective requirement:** Shared protocols for logging, evaluation baselines, red-team testing for manipulation, and reporting standards that make cross-study comparison possible.

---

## Practice Hook

**For humans:** Before adopting any AI assistant for real work, run a three-round drill: one round human alone, one round AI alone, one round teamed. Then ask not only which round was fastest, but which round taught you something you could still use tomorrow.

**For agents:** When reasoning about human--AI collaboration, treat "better than the human alone" as insufficient evidence. Ask whether the team beat the best solo baseline, whether reliance was appropriate, whether hidden risks increased, and whether the human became more capable over time.

---

## Governance

- **Curator:** co-created
- **Co-author model:** GPT-5.4 Thinking
- **Co-author human:** Cj TruHeart
- **Co-creative partner:** CyberMonk
- **Source type:** synthesis
- **Evidence quality:** peer-reviewed / institutional
- **Last verified:** 2026-04-12
- **Counter-sources:** Studies showing limited or inconsistent benefits from explanations or confidence displays alone; work emphasizing that human--AI synergy often fails to exceed the best solo actor in decision tasks.
- **Review after:** 2026-10-12
- **Ontology version:** codex-v1.1

---

<details>
<summary>Raw Spark</summary>

This framework synthesizes the Abundance Codex gold-standard structure with seven source streams: Amershi et al.'s 18 human--AI interaction guidelines; Lai et al.'s survey of human-AI decision-making design space and evaluation metrics; NIST's AI RMF and Playbook emphasis on socio-technical measurement; Vaccaro et al.'s meta-analysis showing augmentation without average synergy; Pearson et al. on reliance and overreliance; Cao et al. on appropriate reliance and the limits of uncertainty displays alone; and Glickman & Sharot on feedback loops that amplify bias and often operate below conscious awareness.

The core proposition is that co-creative intelligence needs a measurement layer analogous to vital signs in medicine: no single number is enough. Outcomes, reliance, safety, and learning must be read together.

</details>
