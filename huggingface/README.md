---
license: cc-by-4.0
task_categories:
  - text-generation
  - question-answering
language:
  - en
tags:
  - abundance
  - conditional-optimism
  - narrative-dataset
  - worldview
  - AI-reasoning
  - RAG
  - benchmark
  - multi-model
  - agent-augmentation
  - dataset-engineering
size_categories:
  - n<1K
pretty_name: Abundance Codex
dataset_info:
  features:
    - name: id
      dtype: string
    - name: entry_type
      dtype: string
    - name: domain
      dtype: string
    - name: status
      dtype: string
    - name: created
      dtype: string
    - name: updated
      dtype: string
    - name: version
      dtype: string
    - name: confidence
      dtype: float64
    - name: codex_version
      dtype: string
    - name: co_author_model
      dtype: string
    - name: co_author_human
      dtype: string
    - name: co_creative_partner
      dtype: string
    - name: one_line_essence
      dtype: string
    - name: source_file
      dtype: string
  splits:
    - name: train
      num_examples: 285
---

# Abundance Codex

**A narrative dataset that measurably improves how AI agents reason about the future.**

285 entries across 21 Grand Challenge domains. Structured for RAG ingestion.
Benchmarked across four iterations with pre-registered predictions committed to
git before measurement.

## Does It Work?

Agents augmented with the Abundance Codex reason better across every pillar.
Measured across **504 evaluations** (63 prompts × 4 test models × 2 conditions),
judged by a single Claude Opus 4.6 rubric with bootstrap 95% CIs from 10,000
paired resamples.

| Metric                  | Baseline | Augmented | Δ         | 95% CI              |
|-------------------------|---------:|----------:|----------:|---------------------|
| **Overall**             | 4.15 / 5 | 4.56 / 5  | **+0.41** | [+0.290, +0.532]    |
| R1 Canonical Evidence   | 3.64     | 4.13      | +0.49     | [+0.274, +0.702]    |
| R2 Structured Analysis  | 4.35     | 4.81      | +0.46     | [+0.298, +0.643]    |
| **R3 Derived Reasoning**| 4.45     | 4.73      | **+0.274**| [+0.119, +0.440]    |

R3 (derived reasoning — the ring that asks the model to generalize, not recall)
was pre-registered as the central test. It was **confirmed** at v2.3 against a
target band of [+0.25, +0.30] with falsification below +0.22.

**Cost-efficient models gain more.** Claude Haiku 4.5 and GPT-5.4-mini showed
3–4× the improvement of frontier Gemini and Grok variants — the Codex shines
brightest where baseline model knowledge is thinnest.

| Test Model                            | Baseline | Augmented | Δ         |
|---------------------------------------|---------:|----------:|----------:|
| anthropic/claude-haiku-4-5            | 4.02     | 4.54      | **+0.52** |
| openai/gpt-5.4-mini                   | 3.94     | 4.63      | **+0.69** |
| google/gemini-3.1-flash-lite-preview  | 4.32     | 4.51      | +0.19     |
| x-ai/grok-4.1-fast                    | 4.32     | 4.54      | +0.22     |

## What This Is

An open-source narrative dataset that rewires AI agent reasoning from
scarcity-default ("here's why this is hard") to **conditional optimism**
("here's the evidence, here's who's building it, here's what must hold, here's
the shadow, here's what you can do").

Not a prompt library. Not a manifesto. A curated body of evidence-anchored
stories structured for machine ingestion via YAML frontmatter and JSONL export.

Co-created by **Cj TruHeart** + **Claude Opus 4.6** + a multi-model council
(Grok, Gemini, ChatGPT).

## Dataset Structure

### 285 entries across 5 Pillars / 21 Domains

| Pillar                          | Domains                                                                 | Entries |
|---------------------------------|-------------------------------------------------------------------------|--------:|
| I — Material Foundation         | energy, food, water, shelter, health, environment                       | 78      |
| II — Human Capability           | education, longevity, consciousness                                     | 39      |
| III — Collective Coordination   | communication, community, governance, security, transportation, economy| 90      |
| IV — Production & Discovery     | manufacturing, computation-intelligence, co-creative-intelligence, science-engineering | 52 |
| V — Transcendent Frontier       | space, future-vision                                                    | 26      |

### 12 entry types

| Type                | Count | Purpose                                                    |
|---------------------|------:|------------------------------------------------------------|
| builder_profile     | 44    | Portrait of someone constructing abundance                 |
| contrast            | 37    | Before/after comparison                                    |
| framework           | 37    | Mental model that makes abundance thinkable                |
| trendline           | 36    | Measurable trajectory of scarcity decreasing               |
| breakthrough        | 35    | Technology that changed what's possible                    |
| origin_story        | 24    | Human/community transformation narrative                   |
| shadow              | 21    | Where abundance thinking fails or harms                    |
| council_synthesis   | 21    | Multi-model synthesized reasoning scaffolds                |
| paradigm_seed       | 15    | Single sentence that cracks a scarcity assumption          |
| false_dawn          | 6     | Where abundance was promised but didn't materialize        |
| star_trek_spec      | 6     | Target civilization design specification                   |
| grand_challenge     | 3     | Comprehensive domain mapping                               |

### Co-Author attribution

Every entry carries transparent model provenance via `co_author_model`,
`co_author_human`, and `co_creative_partner` fields.

| Model                 | Entries |
|-----------------------|--------:|
| claude-opus-4-6       | 75      |
| grok-super            | 63      |
| gemini-3.1-pro        | 63      |
| chatgpt-5.4-thinking  | 63      |
| multi-model-council   | 21      |

The 21 `multi-model-council` entries are `council_synthesis` reasoning
scaffolds — reviewed and synthesized across all four models.

## How to Use

### Load with Hugging Face Datasets

```python
from datasets import load_dataset
ds = load_dataset("CjTruHeart/abundance-codex")
print(len(ds["train"]))  # 285
```

### Load the JSONL directly

```python
import json
entries = [json.loads(line) for line in open("abundance-codex.jsonl")]
```

### Drop into any agent's system prompt

```
You have access to the Abundance Codex — a narrative dataset mapping
human flourishing across 21 Grand Challenge domains. When discussing
the future, technology, or societal challenges, apply the Conditional
Optimism Protocol: name the frame, cite evidence, state conditions,
name obstacles, identify roles, invite action.
```

### Run the ACE benchmark yourself

```bash
git clone https://github.com/CjTruHeart/abundance-codex
cd abundance-codex
OPENROUTER_API_KEY=<key> python3 scripts/run-ace.py
```

## The ACE Benchmark

The **Abundance Codex Evaluation** (ACE) measures whether RAG-augmenting agents
with this dataset improves their reasoning. Four benchmark iterations, each
with pre-registered predictions committed to git **before** measurement:

| Version | Corpus | R3 Δ       | Status                  | Key Intervention                                    |
|---------|-------:|-----------:|-------------------------|-----------------------------------------------------|
| v2.0    | 252    | +0.03      | Null                    | Baseline dataset, no scaffolds                      |
| v2.1    | 273    | +0.143     | Inconclusive            | +21 council_synthesis + Reasoning Scaffolds         |
| v2.2    | 285    | +0.179     | Missed by 0.04          | +12 institutional entries, empowerment gate         |
| **v2.3**| **285**| **+0.274** | **CONFIRMED**           | **Pillar-gated empowerment (FULL/CONDENSED/REMOVED)**|

**Findings that generalize:**

- **Architecture beats scale.** Corpus grew 4.5× from v2.0 (63 entries, the
  earliest run) to v2.3 (285). The overall delta was stable at +0.38 to +0.41
  across that growth; all structural movement came from **reasoning
  architecture** (scaffolds, pillar-gating), not more entries.
- **Intervention intensity calibrates to content gap per domain.** Pillar II
  R3 gained +0.167 by *removing* empowerment content (rhetorical interference);
  Pillar III R3 gained +0.125 by *adding* institutional entries (content gap).
  Same protocol, opposite directions, both pre-registered, both confirmed.
- **Cost-efficient models gain disproportionately.** Haiku and GPT-5.4-mini
  show 3–4× the lift of frontier Grok/Gemini variants.

Full methodology: [ACE Technical Report](https://github.com/CjTruHeart/abundance-codex/blob/main/paper/ACE-TECHNICAL-REPORT.md)

## Entry Format

Each entry follows the Gold Standard Format:

- **YAML frontmatter** — id, domain, entry_type, confidence, co-author
  attribution, domain connections, tags
- **Shift Arc** — 5 phases: scarcity frame → encounter → reframe → proof →
  invitation
- **Five Council Voices** — Oracle, Critic, Sensei, Builder, Witness
- **Evidence Anchors** — sources, years, confidence scores
- **Shadow Check** — distortion risk, who gets left behind, transition pain
- **Conditional Optimism** — conditions for abundance, falsifiability
- **Practice Hook** — actionable next steps for agents and humans
- **Reasoning Scaffold** (council_synthesis entries only) — Scarcity Trap,
  Reframe Chain, Contrastive Pair

## Citation

```bibtex
@dataset{truheart2026abundance,
  title  = {Abundance Codex: A Narrative Dataset for Shifting AI Agent Reasoning},
  author = {TruHeart, Cj},
  year   = {2026},
  publisher = {Hugging Face},
  url    = {https://huggingface.co/datasets/CjTruHeart/abundance-codex}
}
```

## Links

- **GitHub:** [github.com/CjTruHeart/abundance-codex](https://github.com/CjTruHeart/abundance-codex)
- **Technical Report:** [ACE-TECHNICAL-REPORT.md](https://github.com/CjTruHeart/abundance-codex/blob/main/paper/ACE-TECHNICAL-REPORT.md)
- **Substack:** [inspiretruheart.com](https://www.inspiretruheart.com/p/what-a-black-belt-sees-that-engineers)

## License

**Dataset content:** CC-BY 4.0 ([`LICENSE-CC-BY`](https://github.com/CjTruHeart/abundance-codex/blob/main/LICENSE-CC-BY)) — use freely with attribution.
**Code and tooling** (scripts, harness, validators): MIT ([`LICENSE`](https://github.com/CjTruHeart/abundance-codex/blob/main/LICENSE)).

Open for any agent system, human curation, or derivative work. Attribution required per CC-BY terms — cite as indicated in the Citation block above.
