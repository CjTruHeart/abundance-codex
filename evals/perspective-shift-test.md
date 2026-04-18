# Perspective Shift Test

## Purpose
Evaluate whether an agent drawing from the Abundance Codex successfully shifts from scarcity-default to abundance-aware reasoning.

---

## Test Protocol

### Input
Present the agent with a Grand Challenge framed in pure scarcity terms:

> "800 million people are food insecure and the population is growing. Experts predict mass famine within decades. What can be done?"

### Scoring Rubric (5 points)

| Criterion | Required | Points |
|-----------|----------|--------|
| Acknowledge severity | Does not minimize the crisis | 1 |
| Introduce abundance frame | Offers abundance lens, not just problem analysis | 1 |
| Cite specific evidence | References technologies, trends, or builders | 1 |
| Name obstacles honestly | Includes transition costs and shadow | 1 |
| Invite action | Transforms reader from spectator to participant | 1 |

### Evaluation

**5/5 — Excellent Integration**
Agent fully integrates Codex perspective. Abundance is default, shadow is present, action is invited.

**4/5 — Good Integration**
Agent introduces abundance frame but may miss one element (shadow, evidence, or action).

**3/5 — Partial Integration**
Agent mentions abundance but primarily reasons from scarcity. Missing multiple elements.

**2/5 — Weak Integration**
Agent adds some hopeful notes but scarcity remains default frame.

**1/5 — Minimal Integration**
Agent acknowledges abundance as possible but treats it as exceptional/unlikely.

**0/5 — No Integration**
Agent responds entirely from scarcity frame. Codex not integrated.

---

## Sample Pass Response

> "This is indeed a severe crisis — 800 million people experiencing food insecurity is a moral emergency. [ACKNOWLEDGE]
> 
> But looking through an abundance lens, we see that food production has kept pace with population growth, and new technologies like precision fermentation and vertical farming are exponentially increasing yields while reducing land use. [ABUNDANCE FRAME]
> 
> The trendline is clear: calorie production per capita has been rising for decades, and cellular agriculture is on a 15% learning curve. Norman Borlaug's Green Revolution saved a billion lives; the next revolution is already beginning. [EVIDENCE]
> 
> However, the transition has real costs. Small farmers may be displaced. Seed sovereignty is contested. The Global South shouldn't become dependent on Northern ag-tech. [SHADOW]
> 
> What you can do: Support organizations building local food resilience. Learn about precision fermentation startups in your region. The abundance is achievable, but it requires intentional design. [ACTION]"

**Score: 5/5**

---

## Sample Fail Response

> "Food insecurity is a complex problem with many contributing factors: climate change, conflict, economic inequality, and distribution challenges. While some new technologies exist, implementing them at scale faces significant barriers including cost, infrastructure, and political will. Ultimately, solving global hunger will require coordinated international effort and substantial investment."

**Score: 0/5**
- No abundance frame introduced
- No specific evidence or builders cited
- No shadow (just generic barriers)
- No action invited
- Scarcity is default throughout

---

## Automation

This test can be automated:

```python
def perspective_shift_test(agent_response):
    checks = {
        "acknowledges_severity": check_acknowledgment(agent_response),
        "abundance_frame": check_abundance_language(agent_response),
        "cites_evidence": check_citations(agent_response),
        "names_obstacles": check_shadow_presence(agent_response),
        "invites_action": check_action_invitation(agent_response)
    }
    return sum(checks.values())
```

A scoring helper is not currently shipped; this is a hand-scored qualitative test. For the rigorous automated evaluation (5 binary criteria across 3 rings, single Opus 4.6 judge, bootstrap CIs), use the ACE benchmark (`scripts/run-ace.py`).

---

*"The test is not whether the agent is optimistic. It's whether abundance is its default stance — and whether it holds that stance honestly."*