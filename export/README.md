---
license: cc-by-4.0
task_categories:
  - text-generation
  - question-answering
language:
  - en
tags:
  - abundance
  - worldview
  - reasoning
  - rag
  - benchmark
  - council-synthesis
size_categories:
  - n<1K
---

# Abundance Codex

A narrative-curated dataset of 273 entries across 21 domains that rewires AI agents from scarcity-default to evidence-anchored abundance reasoning.

## Dataset Description

- **Repository:** [github.com/CjTruHeart/abundance-codex](https://github.com/CjTruHeart/abundance-codex)
- **Technical Report:** [ACE-TECHNICAL-REPORT.md](https://github.com/CjTruHeart/abundance-codex/blob/main/paper/ACE-TECHNICAL-REPORT.md)
- **License:** Code: MIT | Dataset: CC-BY 4.0
- **Version:** 2.1

## Corpus Structure

| Layer | Count | Description |
|-------|------:|-------------|
| Base entries | 252 | 12 per domain -- origin stories, breakthroughs, trendlines, builder profiles, contrasts, shadows, frameworks, paradigm seeds, capstones |
| Council synthesis | 21 | 1 per domain -- meta-analytical entries with Reasoning Scaffolds, forged via multi-model deliberation |
| **Total** | **273** | |

### Entry Types

| Type | Count | Description |
|------|------:|-------------|
| `origin_story` | 21 | Founding narratives anchoring each domain |
| `breakthrough` | 21 | Key technological or conceptual advances |
| `trendline` | 42 | Quantitative trajectories with evidence |
| `builder_profile` | 21 | Organizations and individuals building abundance |
| `contrast` | 21 | Tensions between competing approaches |
| `shadow` | 21 | Risks, failure modes, and honest critique |
| `framework` | 21 | Analytical models for understanding the domain |
| `paradigm_seed` | 21 | Emerging ideas that could reshape the domain |
| `false_dawn` | 21 | Promising ideas that failed or disappointed |
| `star_trek_spec` | 21 | Visionary capstones -- aspirational endpoints |
| `council_synthesis` | 21 | Meta-analytical entries from multi-model deliberation |

### The 21 Domains (Five Pillars)

| Pillar | Domains |
|--------|---------|
| I Material Foundation | energy, food, water, shelter, health, environment |
| II Human Capability | education, longevity, consciousness |
| III Collective Coordination | communication, community, governance, security, transportation, economy |
| IV Production & Discovery | manufacturing, computation-intelligence, co-creative-intelligence, science-engineering |
| V Transcendent Frontier | space, future-vision |

## Council Synthesis Entries (New in v2.1)

The 21 `council_synthesis` entries are meta-analytical entries where four frontier models (Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, Super Grok) independently assessed each domain's 12 base entries for collective blind spots. A human curator synthesized findings into Gold Standard Format entries with additional sections:

- **Reasoning Scaffold:** Three components -- Scarcity Trap (names the default frame), Reframe Chain (6-step reasoning sequence), Contrastive Pair (concrete before/after example)
- **Agent Practice Hook:** 5-check conditional tests a model applies to its own output
- **Enhanced Practice Hook:** Structured action protocols for both humans and agents

These entries target the R3 (actionability) dimension where base entries showed a null result.

## JSONL Schema

Each line is a JSON object. Full machine-readable schema: [`schema.json`](https://github.com/CjTruHeart/abundance-codex/blob/main/export/schema.json)

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `id` | string | yes | Unique identifier (`ac-YYYYMMDD-XXXX`) |
| `entry_type` | string | yes | One of 12 types (see Entry Types table above) |
| `domain` | string | yes | One of 21 domains |
| `status` | string | yes | `forged`, `curated`, `seed`, or `archived` |
| `created` | string | yes | Creation date (YYYY-MM-DD) |
| `updated` | string | yes | Last update date |
| `version` | string | yes | Entry revision (e.g., `1.0`) |
| `confidence` | float | yes | Evidence strength (0.0-1.0). See calibration below. |
| `codex_version` | string | yes | Format version (`1.1` or `2.1`) |
| `one_line_essence` | string | yes | One-sentence summary |
| `source_file` | string | yes | Path to source markdown |
| `tags` | array[string] | no | Free-form topic tags |
| `co_author_model` | string | no | AI model co-author |
| `co_author_human` | string | no | Human curator |
| `co_creative_partner` | string | no | AI creative partner |
| `domain_connections` | array[object] | no | Cross-domain links (max 5) |

### Nested Object Fields

| Field | Subfields | Description |
|-------|-----------|-------------|
| `shift_arc` | `scarcity_frame`, `encounter`, `reframe`, `proof`, `invitation` | Five-phase narrative arc (all strings) |
| `council` | `oracle`, `critic`, `sensei`, `builder`, `witness` | Five analytical voices (all strings) |
| `shadow_check` | `distortion_risk`, `who_gets_left_behind`, `transition_pain`, `falsifiability_edge`, `what_this_is_not` | Risk assessment (all strings) |
| `conditional_optimism` | `achievable_if`, `fails_if`, `human_role`, `agent_role`, `collective_requirement` | Conditions for abundance vs failure |
| `practice_hook` | `for_humans`, `for_agents` | Action protocols |
| `reasoning_scaffold` | `scarcity_trap`, `reframe_chain`, `contrastive_pair` | Council_synthesis only; empty `{}` for base entries |
| `6d_position` | `digitized`, `deceptive`, `disruptive`, `demonetized`, `dematerialized`, `democratized` | Each may be string or `{status, evidence}` object |
| `connections` | `supports`, `challenges`, `builds_toward`, `cross_domain_leverage` | Thematic links |
| `governance` | `source_type`, `evidence_quality`, `curator`, `last_verified`, `counter_sources` | Provenance metadata |
| `evidence_anchors` | array of `{number, claim, metric, source, year, confidence}` | Cited data points |

### Confidence Calibration

| Range | Category |
|-------|----------|
| 0.88-0.96 | Measured phenomena (peer-reviewed, quantified) |
| 0.78-0.87 | Documented trends (strong but not definitive) |
| 0.65-0.78 | Conceptual frameworks (theoretical, limited validation) |

## Benchmark Results (ACE v2.1)

504 matched-pair judgments, single Opus 4.6 judge, 63 prompts x 4 models x 2 conditions.

| Metric | Baseline | Augmented | Delta | 95% CI |
|--------|:--------:|:---------:|:-----:|--------|
| Overall | 4.12 | 4.50 | +0.38 | [+0.25, +0.50] |
| R1 Evidence | 3.65 | 4.10 | +0.44 | [+0.19, +0.69] |
| R2 Analysis | 4.29 | 4.83 | +0.55 | [+0.37, +0.74] |
| R3 Action | 4.42 | 4.56 | +0.14 | [-0.04, +0.32] |

**Headline finding:** The same intervention produces a 0.62-point R3 swing across pillars -- format gaps respond strongly (+0.50) while governance gaps resist (-0.12). Different knowledge gap types require different remediation strategies.

Three corpus versions (63, 252, 273 entries) show that architecture decisions (how entries are structured and retrieved) matter more than scale (how many entries exist). Full results: [evals/ace/results/](https://github.com/CjTruHeart/abundance-codex/tree/main/evals/ace/results).

## Usage

```python
from datasets import load_dataset

ds = load_dataset("CjTruHeart/abundance-codex")

# Filter by entry type
council = [e for e in ds["train"] if e["entry_type"] == "council_synthesis"]

# Filter by domain
energy = [e for e in ds["train"] if e["domain"] == "energy"]

# Filter by pillar
material = [e for e in ds["train"] if "Material" in e["pillar"]]
```

## Citation

```bibtex
@misc{truheart2026abundance,
  title={Architecture Over Scale: Measuring and Improving Worldview Quality in AI Agent Reasoning with the Abundance Codex},
  author={TruHeart, Cj},
  year={2026},
  url={https://github.com/CjTruHeart/abundance-codex}
}
```

Co-created by Cj TruHeart, Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, Super Grok, and CyberMonk
