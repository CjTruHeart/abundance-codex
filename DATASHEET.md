# Datasheet for the Abundance Codex

Following the framework from Gebru et al. (2021), "Datasheets for Datasets."

---

## 1. Motivation

**For what purpose was the dataset created?**
To provide AI agents and humans with a structured, evidence-anchored counterweight to the scarcity-coded defaults in most AI training data. The dataset shifts reasoning from threat-focused pessimism toward conditional optimism grounded in evidence, while preserving honest critique of risks, transition costs, and exclusions.

**Who created the dataset and on behalf of which entity?**
Cj TruHeart (human curator and creative director), with Claude Opus 4.6 (Anthropic) as AI model co-author for research and drafting, and CyberMonk as AI co-creative partner for strategy and architecture. Created as an independent open-source project, not on behalf of any company or institution.

**Who funded the creation of the dataset?**
Self-funded by Cj TruHeart. API costs for model inference (OpenRouter) and benchmark evaluation are the primary expenses.

---

## 2. Composition

**What do the instances that comprise the dataset represent?**
Each instance is a narrative-analytical entry about a civilization-scale challenge domain. Entries combine storytelling (the Shift Arc), multi-perspective analysis (five Council voices), quantitative evidence (Evidence Anchors), honest critique (Shadow Check), and actionable guidance (Practice Hook).

**How many instances are there?**
273 entries: 252 base entries (12 per domain) and 21 council_synthesis meta-entries (1 per domain).

**What data does each instance consist of?**
26 structured fields per entry. See `export/schema.json` for the full machine-readable schema. Key fields: narrative arc (5 phases), council voices (5 perspectives), evidence anchors (cited data points with sources, years, and confidence scores), shadow check (5 risk dimensions), practice hook (human and agent protocols), and for council_synthesis entries, a reasoning scaffold (3 components).

**Is there a label or target associated with each instance?**
No supervised labels. Entries carry metadata: entry_type (12 types), domain (21 domains), pillar (5 pillars), confidence score (0.0-1.0), and status (forged, curated, seed, archived).

**Is any information missing from individual instances?**
By design. The density matrix (see GOLD-STANDARD-FORMAT.md) specifies which sections are required, minimal, or skipped for each entry type. Lightweight types (paradigm_seed, false_dawn) intentionally omit some sections. The `reasoning_scaffold` field is populated only for council_synthesis entries (empty object for base entries).

**Are there any errors, sources of noise, or redundancies?**
Known limitations:
- Evidence anchors cite source years but are not automatically refreshed. A 2019 citation in a 2026 dataset may be outdated.
- The `empowers` criterion in ACE benchmark evaluation shows a consistent negative delta (-0.155) — RAG augmentation with the Codex trades motivational framing for analytical structure. This is a measured property, not an error.
- Four co-author models share training corpora biased toward technological optimism and supply-side narratives. The council_synthesis layer partially mitigates this but does not eliminate it.

**Entry type distribution:**

| Type | Count | % |
|------|------:|--:|
| builder_profile | 41 | 15.0 |
| contrast | 37 | 13.6 |
| trendline | 36 | 13.2 |
| breakthrough | 35 | 12.8 |
| framework | 30 | 11.0 |
| origin_story | 22 | 8.1 |
| shadow | 21 | 7.7 |
| council_synthesis | 21 | 7.7 |
| paradigm_seed | 15 | 5.5 |
| false_dawn | 6 | 2.2 |
| star_trek_spec | 6 | 2.2 |
| grand_challenge | 3 | 1.1 |

The uneven distribution is intentional. Builder profiles and trendlines carry the most evidence; grand_challenge entries require exhaustive domain mapping and are used sparingly.

**Does the dataset contain data that might be considered confidential?**
No. All evidence anchors cite publicly available sources. No personal data, user data, or proprietary information is included.

---

## 3. Collection Process

**How was the data associated with each instance acquired?**
Entries are co-authored through a human-AI collaboration workflow:
1. Human curator (Cj TruHeart) selects domain and entry type, provides direction
2. AI model (Claude Opus 4.6 via OpenRouter) drafts entry following Gold Standard Format
3. Human reviews, edits, and curates — adding lived experience, correcting claims, strengthening shadows
4. Validation script checks structural compliance (4-layer validation)
5. Entry is committed to the repository

Council_synthesis entries follow a different process:
1. Four frontier models (GPT-5.4 Mini, Claude Haiku 4.5, Gemini Flash-Lite, Grok 4.1 Fast) independently assess each domain's 12 base entries for collective blind spots
2. Human curator synthesizes 84 parallel-independent assessments into 21 meta-entries
3. Reasoning Scaffolds and Practice Hooks are designed to target measured weaknesses (R3 actionability null result)

**Who was involved in the data collection process?**
- Cj TruHeart: human curator, creative director, final editorial authority
- Claude Opus 4.6 (Anthropic): primary AI co-author for base entries
- CyberMonk: AI co-creative partner for strategy and architecture
- GPT-5.4 Mini, Claude Haiku 4.5, Gemini Flash-Lite, Grok 4.1 Fast: council deliberation models for council_synthesis entries

**Over what timeframe was the data collected?**
April 2026 (v1.0 through v2.1). Entries reference evidence spanning 1954-2026.

**Were any ethical review processes conducted?**
No formal IRB or ethics board review. The dataset contains no human subjects data. Ethical considerations are documented in the technical report (Section 7.6), including concerns about epistemic monoculture (4 Western-trained models), the tension between analytical rigor and motivational framing, and the risk that conditional optimism becomes unconditional optimism through retrieval compression.

---

## 4. Preprocessing

**Was any preprocessing/cleaning/labeling of the data done?**
- Structural audit of all 252 base entries to ensure section completeness
- Evidence anchor verification (sources checked, years confirmed)
- Composite witness disclosures added to 30 entries where the Witness voice synthesized rather than quoted direct experience
- Normalization pass across all domains (emoji consistency, header formatting, date alignment)
- JSONL export extracts structured fields from markdown via regex parsing (see `scripts/export-to-jsonl.py`)

**Is the software used to preprocess the data available?**
Yes. All scripts are in `scripts/`: `validate-entry.py` (4-layer validation), `export-to-jsonl.py` (structured extraction), `generate-schema.py` (schema generation), `validate-jsonl.py` (schema validation).

---

## 5. Uses

**Has the dataset been used for any tasks already?**
Yes. The ACE benchmark (v1.0, v2.0, v2.1) uses the dataset as retrieval context for evaluating reasoning quality improvement. Results are published in the technical report (`paper/ACE-TECHNICAL-REPORT.md`).

**What (other) tasks could the dataset be used for?**
- RAG context for AI agents reasoning about civilization-scale challenges
- Training data for worldview-aware language models
- Benchmark for measuring knowledge gap types (content, format, governance, velocity, reflexivity)
- Educational resource for understanding abundance economics, exponential technology, and conditional optimism
- Research into multi-model deliberation and meta-analytical entry design

**Is there anything about the composition of the dataset or the way it was collected that might impact future uses?**
- The dataset reflects the worldview of its creators and co-author models. It is intentionally optimistic-conditional, not neutral.
- Co-author models (primarily Claude Opus 4.6) share training data biases toward Western, English-language, technology-optimistic sources. The council_synthesis layer identifies but does not fully correct these biases.
- The governance gap (Pillar III) showed negative R3 delta (-0.12) under structured-context intervention, suggesting institutional knowledge gaps that retrieval augmentation alone cannot address.

**Are there tasks for which the dataset should not be used?**
- Should not be used as authoritative investment or policy guidance. The dataset provides reasoning frameworks, not recommendations.
- Should not be used to train models that present conditional optimism as unconditional certainty. The shadow checks and falsifiability edges are integral, not optional.
- Should not be used without the Shadow Check and Critic voice. Stripping these creates toxic positivity.

---

## 6. Distribution

**How will the dataset be distributed?**
- GitHub repository: [github.com/CjTruHeart/abundance-codex](https://github.com/CjTruHeart/abundance-codex)
- HuggingFace: [huggingface.co/datasets/CjTruHeart/abundance-codex](https://huggingface.co/datasets/CjTruHeart/abundance-codex)
- JSONL export: `export/abundance-codex.jsonl`

**When will the dataset be distributed?**
Available now. Updated with each version release.

**Will the dataset be distributed under a copyright or other intellectual property (IP) license?**
MIT License. Open for any agent system, human curation, or derivative work.

**Have any third parties imposed IP-based or other restrictions on the data associated with the instances?**
No. All evidence anchors cite publicly available sources.

---

## 7. Maintenance

**Who is supporting/hosting/maintaining the dataset?**
Cj TruHeart (primary maintainer). Repository hosted on GitHub with CI/CD via GitHub Actions.

**How can the owner/curator/manager of the dataset be contacted?**
Via GitHub issues on the repository.

**Will the dataset be updated?**
Yes. The dataset follows a milestone-based versioning scheme (v1.0, v2.0, v2.1). Future versions may add entries, domains, or entry types. All changes are tracked in CHANGELOG.md.

**How will updates be communicated?**
Via CHANGELOG.md, GitHub releases, and HuggingFace dataset card updates.

**If the dataset relates to people, are there applicable limits on the retention of the data?**
The dataset does not contain personal data about identifiable individuals. Builder profiles reference public figures and organizations based on publicly available information.

**Confidence calibration methodology:**
Confidence scores (0.0-1.0) are assigned based on evidence strength:
- **0.88-0.96**: Measured phenomena with peer-reviewed sources, quantified metrics, and multiple independent confirmations
- **0.78-0.87**: Well-documented trends with strong but not definitive evidence
- **0.65-0.78**: Conceptual frameworks, theoretical models, or emerging trends with limited empirical validation
- **Below 0.65**: Speculative or contested claims (rare in the dataset; most are flagged via shadow checks)

Scores are assigned by the human curator during the curation process and are not the product of automated scoring or inter-rater agreement.
