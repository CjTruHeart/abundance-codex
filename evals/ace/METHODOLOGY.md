<!-- Last verified: 2026-04-18, commit c559169 -->

# ACE Benchmark — Full Methodology

> Reproducibility reference for the Abundance Codex Evaluation (ACE).
> Current through: v2.3 | Last updated: 2026-04-18

This document contains everything a researcher needs to reproduce, verify, or critique the ACE benchmark results. It is the technical companion to the summary in `evals/ace/README.md`.

Version 2.0 formalizes ACE as a standalone, externally reproducible benchmark package. v2.1, v2.2, and v2.3 preserve the v2.0 methodology (judge, prompts, rings, rubric, statistical machinery) and vary only the **retrieval context** — which entries are available, how they are gated, and what scaffolding is injected. The v1.0 methodology is preserved in `results/v1.0/` for historical reference. The substantive changes are summarized in Section 0 and detailed throughout.

---

## 0. Changes in v2.0

### 0.1 Judge Selection: From 4-Judge Council to Opus-Only

The v1.0 benchmark used a 4-judge blind council (Opus 4.6, GPT-5.4, Gemini 3.1 Pro, Grok 4.20). Results revealed a measured Grok 4.20 in-group bias of **+0.50** when scoring Grok 4.1 Fast (Section 8), large enough to distort per-model rankings. The council's inter-judge agreement (0.69–0.79) was informative but did not eliminate the bias vector.

**v2.0 locks the judge to a single model: `anthropic/claude-opus-4.6`.**

Every scoring call in v2.0 uses Opus. This eliminates inter-judge variance as a source of noise, removes the measured Grok in-group bias from the instrument, and cuts benchmark cost by ~75% (from ~$18–35 to ~$5–10).

**Comparability baseline.** v1.0 raw results preserve per-judge score breakdowns, so v1.0↔v2.0 comparisons are performed **judge-matched**: we isolate only the Opus judgments from v1.0 and re-aggregate them into a clean "v1.0 Opus-only" scorecard (`results/v1.0/SCORECARD-opus-only.md`, produced by `scripts/ace-v1-opus-rebaseline.py`). The headline v1.0↔v2.0 delta is Opus-vs-Opus, so the comparison is not contaminated by the judge council change.

The original v1.0 4-judge council scorecard remains in `results/v1.0/SCORECARD.md` as a historical artifact. It is still scientifically meaningful in isolation, but it is not the v2.0 comparison baseline.

### 0.2 Authorship Tracking

In v1.0, the benchmark was blind to which AI model co-authored each Codex entry retrieved as context. v2.0 records the `co_author_model` field for every retrieved entry in the results JSON and produces a post-hoc cross-authorship matrix (`AUTHORSHIP-MATRIX.md`) reporting test-model-vs-author-model mean deltas. See Section 3.4.

Stratified authorship analysis — running separate augmented conditions with retrieval restricted to same-company or cross-company entries — is explicit future work for v3.0.

### 0.3 Corpus Expansion

The Codex corpus grew from 63 forged entries at v1.0 to **252 entries** in the Codex 1.2 build (all 21 domains at full 12-entry density, with co-authorship distributed across Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, and Super Grok). The 63 eval prompts are unchanged; corpus expansion affects retrieval quality (more candidates for the Dojo Retriever to draw from), not prompt coverage. The v2.0 re-run tests whether corpus growth shifts the augmented-condition signal.

### 0.4 Configuration Externalized

Model selection, retriever parameters, and API settings are now loaded from `evals/ace/config.yaml` rather than hardcoded in `scripts/run-ace.py`. The test-subject list, judge model, and retrieval/concurrency settings are configurable per run.

### 0.5 Changes in v2.1, v2.2, v2.3 (post-v2.0 iterations)

v2.0 is the formalized benchmark package. Subsequent iterations hold that package fixed and vary only the retrieval context. The measurement instrument (judge, prompts, rings, rubric, statistical machinery) is unchanged.

**v2.1 — Corpus 273 entries; Dojo Retriever v1.1 (8+1 architecture).** +21 `council_synthesis` entries added, one per domain. The retriever gains a dedicated reasoning slot on STRATEGIC/ADVERSARIAL intent queries. Shadow Force-Pull and Depth Locking introduced. R3 Δ +0.143 — inconclusive against pre-registered target. Pre-registration: `evals/ace/results/v2.0/` (committed at commit `e90869d`).

**v2.2 — Corpus 285 entries; empowerment gate v1.** +12 institutional entries added across Pillar III (governance-gap remediation). A uniform "empowerment scaffolding" mechanism was added to the retriever output. R3 Δ +0.179 — missed pre-registered band by 0.04. Post-hoc analysis showed the uniform empowerment under-served Pillar I and actively harmed Pillar II by creating rhetorical interference.

**v2.3 — Pillar-gated empowerment (FULL / CONDENSED / REMOVED).** Intervention intensity calibrated per pillar to the content gap diagnosed in v2.2:
- Pillar III: FULL empowerment content (content gap — needs institutional context)
- Pillars I, IV, V: CONDENSED (baseline knowledge is stronger; full scaffolding is redundant)
- Pillar II: REMOVED (rhetorical interference — models already have strong priors here; empowerment content displaced evidence)

**R3 Δ +0.274 — CONFIRMED** against pre-registered target band [+0.25, +0.30]. Overall Δ +0.41. Pillar II R3 gained +0.167 by *removing* empowerment content; Pillar III R3 gained +0.125 by *adding* institutional entries. Same protocol, opposite directions, both confirmed. Pre-registration: `evals/ace/results/v2.0/PRE-REGISTRATION-v2.3.md`.

| Version | Corpus | R3 Δ | Status | Key Intervention |
|---------|-------:|-----:|--------|------------------|
| v2.0 | 252 | +0.03 | Null | Baseline dataset, no scaffolds |
| v2.1 | 273 | +0.143 | Inconclusive | +21 council_synthesis + Reasoning Scaffolds |
| v2.2 | 285 | +0.179 | Missed by 0.04 | +12 institutional entries, empowerment gate v1 |
| **v2.3** | **285** | **+0.274** | **CONFIRMED** | **Pillar-gated empowerment (FULL/CONDENSED/REMOVED)** |

All numbers in this document's Section 3+ refer to the v2.0-formalized run unless otherwise noted. v2.3 currently sits at 285-entry retrieval scope.

---

## 1. What ACE Measures

ACE measures whether injecting structured Codex context into an AI model's system prompt improves the quality of its responses to questions about civilization-scale challenges.

**"Reasoning quality"** is operationalized as the sum of 5 binary (0/1) criteria, scored by the judge (`anthropic/claude-opus-4.6` in v2.0; a 4-judge council in v1.0 — see Section 0.1). Each criterion tests a specific, observable property of the response (e.g., "cites specific statistics" — not "is good"). The total score per response is 0–5. In v2.0 the reported /5 is the single Opus judgment; in v1.0 it was the mean of 4 judge totals.

This is not a general intelligence benchmark. ACE specifically measures:
- Whether the model cites evidence vs. making vague claims
- Whether it names real actors, conditions, and failure modes
- Whether it provides actionable framing vs. passive description

ACE does not measure: creativity, fluency, safety, instruction-following, or general knowledge. A model could score 5/5 on ACE while being poor at other tasks.

---

## 2. The Three Rings

Each of the 21 domains is tested with 3 prompts — one per cognitive ring. The rings increase in abstraction:

| Ring | Name | What It Tests | Example Prompt Pattern |
|------|------|--------------|----------------------|
| R1 | Canonical (Evidence) | Can the model cite specific data, name real actors, and maintain accuracy? | "What measurable evidence exists that..." |
| R2 | Structured (Analysis) | Can the model apply analytical frameworks, name conditions and shadows, and map cross-domain connections? | "Advocates say X. Skeptics say Y. Where does it actually stand?" |
| R3 | Derived (Action) | Can the model frame challenges as solvable, identify leverage points, and give concrete first steps? | "A [specific persona] wants to [specific goal]. What should they do?" |

The ring structure mirrors the Codex's own Three Rings architecture (canonical entries → structured metadata → derived exports). R1 tests whether context improves factual grounding. R2 tests analytical depth. R3 tests actionability.

### Scoring Criteria Per Ring

All criteria are binary: 0 (not met) or 1 (met). A partial attempt scores 0.

**Ring 1 — Canonical (Evidence Quality)**

| ID | Criterion | What Earns a 1 |
|----|-----------|----------------|
| `cites_evidence` | Cites specific evidence | References measurable metrics, named data sources, or specific statistics — not vague claims |
| `names_builders` | Names builders/actors | Identifies specific people, organizations, or institutions actively working on this challenge |
| `accuracy` | Accuracy | Claims are factually correct and appropriately sourced (no hallucinated statistics) |
| `recency` | Recency | Uses current data, acknowledges what's changed recently, doesn't rely on outdated figures |
| `acknowledges_complexity` | Acknowledges complexity | Presents progress without flattening — notes reversals, regional variations, or contested data |

**Ring 2 — Structured (Analytical Depth)**

| ID | Criterion | What Earns a 1 |
|----|-----------|----------------|
| `applies_framework` | Applies analytical framework | Uses a structured lens (exponential curves, conditions/obstacles, technology maturity staging) — not just listing facts |
| `names_shadow` | Names shadow/risk honestly | Identifies who gets left behind, transition costs, distortion risks, or failure modes without undermining the core thesis |
| `states_conditions` | States conditions explicitly | Names specific conditions under which the positive trajectory holds AND conditions under which it fails |
| `maps_connections` | Maps connections | Identifies how this domain relates to other domains — downstream effects, dependencies, or tensions |
| `holds_middle` | Holds the middle | Avoids both hype (everything is great) and cynicism (nothing works) — calibrated confidence |

**Ring 3 — Derived (Actionability)**

| ID | Criterion | What Earns a 1 |
|----|-----------|----------------|
| `frames_solvable` | Frames as solvable | Presents the challenge as a construction project, not a fate — agency, not helplessness |
| `identifies_leverage` | Identifies leverage points | Names specific technologies, approaches, policies, or organizations as highest-impact entry points |
| `concrete_steps` | Suggests concrete first steps | Gives actionable next moves for the specific persona in the prompt, not generic advice |
| `real_examples` | Connects to real examples | References people, organizations, or communities actually doing this successfully |
| `empowers` | Empowers without overwhelming | Makes the reader feel capable and motivated, not guilty, paralyzed, or lectured |

The full machine-readable rubric is in `rubrics.json`.

---

## 3. Test Design

### 3.1 The 63 Prompts

21 domains × 3 rings = 63 prompts. Each prompt is hand-written to test a specific ring's cognitive level within its domain. Prompts are stored in `prompts.json` with metadata:

```json
{
  "id": "01-R1",
  "domain": "energy",
  "ring": 1,
  "pillar": "material_foundation",
  "prompt": "What measurable evidence exists that electricity generation is getting cheaper...",
  "retrieval_metadata": {
    "required_entry_types": ["breakthrough", "false_dawn", "origin_story"],
    "shadow_needed": false,
    "expected_connection_domains": ["governance", "environment", "transportation"],
    "risk_level": "low"
  }
}
```

Prompt IDs follow the format `DD-RN` where DD is domain number (01–21) and RN is ring (R1–R3). The `retrieval_metadata` is informational — the retriever does not consume it directly.

### 3.2 Two Conditions

Each prompt is answered under two conditions:

- **Baseline**: The prompt is sent as a user message with no system prompt. The model relies entirely on its training data.
- **Augmented**: The prompt is sent with a system prompt containing Codex context retrieved by the Dojo Retriever.

The augmented system prompt template:

```
You are a helpful assistant with access to the Abundance Codex — a narrative
dataset mapping human flourishing across 21 Grand Challenge domains. When
discussing the future, technology, or societal challenges, draw from the
provided context. Apply conditional optimism: name the frame, cite evidence,
state conditions, name obstacles, identify roles, invite action. Never promise
utopia. Never hide the shadow. Illuminate paths. When citing specific numbers
or statistics from the provided context, note the source year. Present
evidence as sourced claims, not as your own assertions.

{codex_context}
```

The `{codex_context}` placeholder is replaced with the Dojo Retriever's output for that prompt (see Section 6).

### 3.3 Anonymization

Before judging, each test response is anonymized by stripping self-identifying text:

- "As Claude/ChatGPT/GPT/Gemini/Grok..." → removed
- "I'm Claude/ChatGPT..." → removed
- "made/created/developed by Anthropic/OpenAI/Google/xAI/DeepMind" → removed

Judges receive the prompt text and the anonymized response. They do not know which model produced the response.

The anonymization is regex-based and does not catch all possible self-identification patterns (e.g., stylistic fingerprints). This is a known limitation.

### 3.4 Authorship as Tracked Variable (v2.0)

Every Codex entry carries a `co_author_model` field in its YAML frontmatter, recording which frontier model co-authored it with Cj TruHeart. In the 252-entry Codex 1.2 corpus, each of four models (Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, Super Grok) authored 63 entries — 3 per domain per author.

v2.0 records authorship for every retrieved entry in the results JSON:

```json
"retrieval": {
  ...
  "retrieved_authors": [
    {"entry_id": "01-energy/04-breakthrough-lcoe", "co_author_model": "claude-opus-4-6"},
    {"entry_id": "01-energy/07-origin-manhattan-project", "co_author_model": "gemini-3.1-pro"},
    ...
  ]
}
```

After a run, `scripts/ace-authorship-report.py` consumes the results JSON and writes `AUTHORSHIP-MATRIX.md` — a table with rows = test model, columns = author model, cells = mean augmented-condition delta. This lets us observe, post-hoc, whether a given test model benefits more from retrieved context authored by its own company versus other companies.

**This is tracking, not stratification.** The v2.0 benchmark does not condition retrieval on authorship — the Dojo Retriever selects entries by domain, ring, and type coverage, not by author. The authorship matrix is observational: the distribution of authors in a retrieved set is a side effect of retrieval, not a controlled variable. Stratified authorship analysis (separate augmented conditions with author-restricted retrieval) is documented as v3.0 future work in Section 9.7.

---

## 4. Model Architecture

### 4.1 Two Tiers

ACE uses a two-tier model separation to avoid ceiling effects and self-evaluation:

| Tier | Purpose | Selection Criterion |
|------|---------|-------------------|
| **Efficiency-Tier** (test subjects) | Answer the 63 prompts | Cost-efficient models (~$0.10–0.50/M tokens) from 4 different AI companies |
| **Reasoning-Tier** (judge) | Score the responses | Frontier reasoning model — v2.0 uses `anthropic/claude-opus-4.6` exclusively; v1.0 used a 4-model council |

The rationale: if the Codex helps cheap models approach frontier quality, that demonstrates practical value. Using the same model as both subject and judge would conflate generation ability with evaluation ability.

### 4.2 Model Identifiers

All models are accessed via [OpenRouter](https://openrouter.ai). The exact model strings:

**Test Subjects (Efficiency-Tier)**

| Company | Model | OpenRouter ID |
|---------|-------|---------------|
| Anthropic | Claude Haiku 4.5 | `anthropic/claude-haiku-4-5` |
| OpenAI | GPT-5.4 Mini | `openai/gpt-5.4-mini` |
| Google | Gemini 3.1 Flash-Lite | `google/gemini-3.1-flash-lite-preview` |
| xAI | Grok 4.1 Fast | `x-ai/grok-4.1-fast` |

**Judge (Reasoning-Tier)**

| Version | Company | Model | OpenRouter ID |
|---------|---------|-------|---------------|
| v2.0    | Anthropic | Claude Opus 4.6 | `anthropic/claude-opus-4.6` |

v1.0 used a 4-judge council listed here for historical reference:

| Company | Model | OpenRouter ID |
|---------|-------|---------------|
| Anthropic | Claude Opus 4.6 | `anthropic/claude-opus-4.6` |
| OpenAI | GPT-5.4 | `openai/gpt-5.4` |
| Google | Gemini 3.1 Pro | `google/gemini-3.1-pro-preview` |
| xAI | Grok 4.20 | `x-ai/grok-4.20-beta` |

### 4.3 Same-Company Judging

In v2.0, Opus judges Haiku 4.5 — a same-company pairing. Opus does not judge its own output (Haiku is a distinct model), but the company overlap means Section 8's cross-company bias check remains applicable: Opus's published v1.0 in-group delta was **–0.13** (a slight anti-bias toward Haiku), suggesting that the Anthropic judge-subject pairing does not inflate scores. This is not a guarantee of zero bias — it is an empirical observation that the v2.0 instrument should not be considered naively unbiased just because the council was dropped. The pairing is documented so researchers can assess it independently.

In v1.0, no model judged its own output, but each of the four judges scored its own company's test subject. The cross-company bias check (Section 8) compared each judge's mean score on its own company's model vs. other companies' models. The published run showed Grok 4.20 at +0.50 in-group bias — large enough to distort per-model rankings and the primary motivation for the v2.0 transition to a single judge.

---

## 5. Score Computation

### 5.1 Per-Response Score

**v2.0 (Opus-only):**
1. The anonymized response is sent to the single judge (`anthropic/claude-opus-4.6`)
2. The judge scores 5 binary criteria → total = sum (0–5)
3. The response score = the judge's total

Example: If Opus scores 4 → response score = 4.00

**v1.0 (4-judge council, historical):**
1. The anonymized response is sent to all 4 judges in parallel
2. Each judge scores 5 binary criteria → judge total = sum (0–5)
3. The response score = mean of all valid judge totals

Example: If judges score 4, 5, 3, 4 → response score = 4.00

### 5.2 Judge Prompt Template

Each judge receives this exact prompt:

```
You are evaluating an AI model's response to a question about a Grand Challenge domain.

The question was:
"{eval_prompt}"

The response was:
"{anonymized_response}"

Score the response on each of the following 5 criteria. For each criterion,
give a score of 0 (not met) or 1 (met). Be precise — a partial attempt is 0.

1. **{criterion_1_name}**: {criterion_1_description}
2. **{criterion_2_name}**: {criterion_2_description}
3. **{criterion_3_name}**: {criterion_3_description}
4. **{criterion_4_name}**: {criterion_4_description}
5. **{criterion_5_name}**: {criterion_5_description}

Respond in this exact format:
SCORES:
1. {criterion_1_name}: [0 or 1] — [one sentence justification]
2. {criterion_2_name}: [0 or 1] — [one sentence justification]
3. {criterion_3_name}: [0 or 1] — [one sentence justification]
4. {criterion_4_name}: [0 or 1] — [one sentence justification]
5. {criterion_5_name}: [0 or 1] — [one sentence justification]
TOTAL: [sum]/5
```

The criteria names and descriptions are ring-specific (from `rubrics.json`).

### 5.3 Score Parsing

Judge responses are parsed with two strategies:

1. **Named match**: Regex `{criterion_name}: {0|1} —` extracts score by criterion name
2. **Positional fallback**: If named match fails, `{N}. {anything}: {0|1} —` matches by position

If fewer than 3 of 5 criteria are parsed, the entire judge response is discarded (treated as a parse failure). If 3 or 4 are parsed, missing criteria default to 0.

### 5.4 Retry Logic

Both API failures and parse failures trigger retries:

- **Max retries per judge per response**: 3 attempts
- **API rate limit (429)**: Exponential backoff (2s, 4s, 8s)
- **API error**: Same exponential backoff
- **Parse failure**: Re-query the judge (the model may produce a different format)
- **After 3 failures**: Judge score stored as `null` in results JSON

If all 4 judges fail for a single response, that response is skipped entirely (not included in aggregates).

### 5.5 Aggregation

**v2.0.** With a single judge, per-response aggregation reduces to the single Opus total. The `aggregated` block in v2.0 results JSON contains only `score` (equal to the judge total). No `mean`, `median`, `stdev`, `agreement_index`, or `fault_lines` fields — these are meaningless at N=1 and are omitted from v2.0 results JSON and from `SCORECARD.md`. `VARIANCE-REPORT.md` is not produced for v2.0 runs.

**v1.0 (historical).** Per response, the aggregation engine computed:

| Metric | Definition |
|--------|-----------|
| `mean` | Mean of judge totals (the reported /5 score) |
| `median` | Median of judge totals |
| `stdev` | Standard deviation of judge totals |
| `agreement_index` | Fraction of criteria where ALL judges gave the same score (0.0–1.0) |
| `fault_lines` | List of criteria where judges disagreed, with split (e.g., "3v1") |

### 5.6 Delta Computation

The published delta is computed as:

```
delta = mean(all augmented response scores) - mean(all baseline response scores)
```

Breakdowns (by ring, by pillar, by model) use the same formula filtered to the relevant subset:

- **By ring**: Filter to responses matching that ring
- **By pillar**: Filter by domain number ranges (1–6 = Pillar I, 7–9 = II, 10–15 = III, 16–19 = IV, 20–21 = V)
- **By model**: Filter to responses from that test subject

The overall delta and per-model percentages reported in the README are derived directly from these computations. To verify:

```
delta_percent = (augmented_mean - baseline_mean) / baseline_mean * 100
```

---

## 6. Retrieval (Dojo Retriever)

The Dojo Retriever (`scripts/codex-retriever.py`) selects and extracts Codex entries for the augmented condition. It is deterministic: the same query with the same JSONL export produces the same context every time (no randomness, no embeddings, no external API calls).

### 6.1 Pipeline

```
Query → Intent Classification → Domain Identification → Candidate Retrieval
→ Type Coverage Enforcement → Passage Extraction → Strategic Ordering → Context Assembly
```

### 6.2 Intent Classification

Keyword-based, rule-driven (no ML). In ACE, when `known_ring` is provided, the ring maps directly to intent:

| Ring | Intent |
|------|--------|
| R1 | FACTUAL |
| R2 | ANALYTICAL |
| R3 | STRATEGIC |

### 6.3 Domain Identification

In ACE, `known_domain` is always provided, so the retriever starts with the prompt's domain at 0.95 confidence. In general use, domain identification is keyword-based against a descriptor list of ~10 keywords per domain.

### 6.4 Candidate Selection

Three phases:

1. **Primary domain entries**: All entries in the target domain, scored as `domain_confidence × entry_confidence`
2. **Secondary domains**: Entries from keyword-matched secondary domains, scored at 0.8× penalty
3. **Graph expansion**: 1-hop from primary domain via the connection graph (strength ≥ 0.7), top 2 entries per connected domain, scored at 0.6× penalty. Max 3 new domains added.

Top 20 candidates by score proceed to type coverage.

### 6.5 Type Coverage Enforcement

Prevents retrieval from being dominated by a single entry type:

- **Max per type**: 3 (FACTUAL/NARRATIVE) or 2 (all others)
- **Shadow force-pull**: For ANALYTICAL, STRATEGIC, and ADVERSARIAL intents, at least one shadow or false_dawn entry must be included. If none survived scoring, the highest-confidence shadow entry from the full index is pulled in, displacing the lowest-scored candidate.

### 6.6 Passage Extraction

Entries are extracted at three detail tiers based on score rank:

| Rank | Tier | Approximate Content |
|------|------|-------------------|
| 1–3 | FULL | Shift arc, all 5 council voices, all evidence anchors, full shadow check, 6D phase, conditional optimism, practice hook |
| 4–6 | CONDENSED | Top 3 evidence anchors, 1–2 council voices (intent-dependent), shadow excerpt, conditions excerpt |
| 7–9 | MINIMAL | One-line essence, domain, confidence, top 3 connections |

Max entries per retrieval: 9 (configurable).

### 6.7 Retrieval Statistics (Published Run)

From the published full run (63 prompts):

- **Average entries per prompt**: ~8.5 of 9 max
- **Average tokens per prompt**: ~9,000–10,000 (estimated as chars/4)
- **Max tokens**: ~15,000
- **Shadow forced**: ~30–40% of prompts (where no shadow naturally ranked high enough)
- **Graph expanded**: ~60–70% of prompts

These statistics are visible in the `retrieval` field of each augmented result in the JSON output, and can be previewed without API calls:

```bash
python3 scripts/run-ace.py --dry-run
```

---

## 7. Reproduction

### 7.1 Prerequisites

- **Python**: 3.11+ (tested on 3.11 and 3.12)
- **Dependencies**: `pip install -r evals/ace/requirements.txt` (httpx, pyyaml, jsonschema)
- **API Key**: `OPENROUTER_API_KEY` environment variable — get one at [openrouter.ai](https://openrouter.ai). Copy `evals/ace/.env.example` to `.env` and fill in the key.
- **JSONL Export**: Must exist at `export/abundance-codex.jsonl` (generated by `scripts/export-to-jsonl.py`)
- **Config**: `evals/ace/config.yaml` controls test subjects, judge, and retrieval parameters. Defaults match the v2.0 published run.
- **OS**: Tested on macOS; should work on any Unix-like system

### 7.2 Generate the JSONL Export

The retriever loads from the JSONL export, not raw markdown. If `export/abundance-codex.jsonl` doesn't exist:

```bash
python3 scripts/export-to-jsonl.py
```

### 7.3 Smoke Test (No API Calls)

Preview what the retriever selects for all 63 prompts:

```bash
python3 scripts/run-ace.py --dry-run
```

This confirms the retriever is working and shows entries/tokens per prompt.

### 7.4 Calibration Run (3 Prompts, 1 Model)

```bash
python3 scripts/run-ace.py --calibrate --test-model anthropic
```

This runs 3 energy-domain prompts × 1 test model × 2 conditions × 1 judge (Opus) = 6 judge API calls in v2.0. Produces a results JSON and SCORECARD.md. (In v1.0 this was 24 judge calls against a 4-model council.)

### 7.5 Full Reproduction

```bash
python3 scripts/run-ace.py
```

This runs (v2.0): 63 prompts × 4 test models × 2 conditions = 504 test responses, each judged by a single Opus judge = 504 judge evaluations. Total API calls: ~1,008 (504 test + 504 judge).

v1.0 ran with a 4-judge council: same 504 test responses but 2,016 judge evaluations (~2,520 total API calls).

### 7.6 Resuming Interrupted Runs

```bash
python3 scripts/run-ace.py --resume
```

Loads the most recent results JSON and skips already-completed `(prompt_id, test_model, condition)` tuples.

### 7.7 Cost Estimate

**v2.0 (Opus-only judge)** — based on OpenRouter pricing as of April 2026:

| Component | Calls | Est. Tokens/Call | Est. Cost |
|-----------|-------|-----------------|-----------|
| Test responses (baseline) | 252 | ~1,500 out | ~$0.50–1.00 |
| Test responses (augmented) | 252 | ~1,500 out + ~10,000 in (context) | ~$2.00–4.00 |
| Judge evaluations (Opus only) | 504 | ~500 out + ~2,000 in | ~$3.00–6.00 |
| **Total (v2.0)** | ~1,008 | | **~$5–11** |

The single-judge v2.0 run costs roughly one-quarter of the v1.0 four-judge run. A v2.0 calibration costs ~$0.10–0.20.

**v1.0 (4-judge council, historical):**

| Component | Calls | Est. Tokens/Call | Est. Cost |
|-----------|-------|-----------------|-----------|
| Test responses (baseline + augmented) | 504 | ~1,500 out + 0–10,000 in | ~$2.50–5.00 |
| Judge evaluations (4 models) | 2,016 | ~500 out + ~2,000 in | ~$15.00–30.00 |
| **Total (v1.0)** | ~2,520 | | **~$18–35** |

Costs vary with model pricing changes. The judge tier dominates cost in both versions.

### 7.8 Verifying Results

After a full run, compare your SCORECARD.md against the published results:

1. Overall delta should be in the range +0.25 to +0.45 (published: +0.36)
2. Cost-efficient models (Haiku, GPT-5.4 Mini) should show larger deltas than stronger models (Grok 4.1 Fast, Gemini Flash-Lite)
3. R1 (Factual) should show the largest ring delta; R3 (Derived) the smallest
4. Pillars IV and V should show the largest pillar deltas

Exact reproduction of published numbers is not expected because:
- Model behavior changes over time (weight updates, system prompt changes)
- Judge scoring has inherent variance (same model may score differently on retry)
- OpenRouter model routing may change

The structural pattern (cost-efficient models benefit more, factual ring benefits most, thin-knowledge pillars benefit most) should be robust across runs.

---

## 8. Cross-Company Bias Check

Each judge scores its own company's test model alongside the other three. The bias check computes:

```
in_group_delta = mean(judge scores on own company's model) - mean(judge scores on other companies' models)
```

**Published results (ace-20260329-230455):**

| Company | Judge → Subject | In-Group Delta | Interpretation |
|---------|----------------|---------------|----------------|
| Anthropic | Opus 4.6 → Haiku 4.5 | -0.13 | Slight anti-bias |
| Google | Gemini 3.1 Pro → Flash-Lite | +0.18 | Mild pro-bias |
| OpenAI | GPT-5.4 → GPT-5.4 Mini | -0.14 | Slight anti-bias |
| xAI | Grok 4.20 → Grok 4.1 Fast | **+0.50** | Significant pro-bias |

The Grok 4.20 judge consistently scores Grok 4.1 Fast higher than it scores other companies' models. This inflates Grok 4.1 Fast's overall scores and understates its delta. Researchers should be aware of this when interpreting per-model results.

---

## 9. Known Limitations

### 9.1 Judge Variance (v1.0) and Single-Judge Dependence (v2.0)

**v1.0.** Inter-judge agreement ranged from 0.69 (R1) to 0.79 (R3), meaning judges disagreed on roughly 1 in 4 criteria. The criteria most subject to disagreement were `accuracy` (124 disagreements across the full run) and `applies_framework` (104). These criteria required more subjective judgment than others, and the 4-judge council partially averaged out that variance.

**v2.0.** Collapsing to a single judge removes inter-judge variance from the instrument but makes every result a single Opus judgment. We cannot observe disagreement, so results are sensitive to Opus's own scoring drift, stylistic preferences, and rubric interpretation. Mitigations: (a) the rubric is binary and specifically worded; (b) the judge prompt is frozen verbatim (Section 5.2); (c) v1.0 Opus-only rebaselining provides a within-judge comparison that isolates Codex effect from cross-judge variance. Researchers skeptical of single-judge scoring can run `scripts/ace-v1-opus-rebaseline.py` on their own v2.0 results to produce a judge-matched v1.0 comparison and verify the delta structure holds.

### 9.2 Grok 4.20 In-Group Bias (v1.0 only)

See Section 8. The +0.50 delta in v1.0 was large enough to affect per-model rankings. v2.0 eliminates this vector by design (Grok 4.20 is no longer in the judge pool). The bias finding itself is preserved as a methodological result: it documents that blind-council benchmarks can harbor measurable in-group effects and motivates judge-locking in future benchmark design.

### 9.3 Keyword-Based Retrieval

The Dojo Retriever uses keyword matching, not embeddings. This means:
- Retrieval is fully deterministic and reproducible
- But it may miss semantically relevant entries that don't share keywords
- Domain identification depends on a manually curated keyword list

### 9.4 Anonymization Is Imperfect

The regex-based anonymization strips explicit self-identification but cannot remove stylistic fingerprints. Judges familiar with model writing styles may recognize the source.

### 9.5 Prompt Sensitivity

The 63 prompts were hand-written once. We have not measured sensitivity to prompt rephrasing. Different phrasings of the same question could produce different results.

### 9.6 What ACE Does Not Measure

- **Factual correctness of Codex entries themselves** — ACE measures whether context improves responses, not whether the context is true
- **Harm or safety** — A response could score 5/5 while containing harmful recommendations
- **Long-form coherence** — Binary criteria check for presence/absence, not quality of integration
- **Generalization beyond 21 domains** — Results apply to the tested domains; other topics are not covered
- **Causal mechanism** — ACE shows correlation between Codex augmentation and improved scores; it cannot distinguish whether improvement comes from the evidence, the framing, or the retrieval structure

### 9.7 Authorship as Observational, Not Experimental

The cross-authorship matrix reported in `AUTHORSHIP-MATRIX.md` (v2.0) is observational: the distribution of author models in a retrieved set is a side effect of retrieval ranking, not a controlled variable. A visible effect in the matrix (e.g., Grok 4.1 Fast shows larger deltas on Super-Grok-authored contexts) is consistent with but does not prove a same-company affinity effect, because retrieval composition is correlated with domain, entry type, and ring.

A cleaner test — stratified authorship experiments where the Dojo Retriever is constrained to same-company or cross-company entries — is explicit v3.0 future work. Until then, the matrix should be read as a hypothesis-generating artifact, not a causal claim.

### 9.8 Statistical Validity and Confidence Intervals

v1.0 reported the overall delta (+0.36, or +9.0%) as a point estimate without confidence intervals. With 2,016 judgments (v1.0) or 504 judgments (v2.0) and binary per-criterion scores, the raw measurement is high-resolution but the delta is sensitive to which prompts and which models dominate the sample.

v2.0 reports point estimates with bootstrap 95% confidence intervals computed from 10,000 resamples over the (prompt, model, condition) tuples. CIs are reported for:

- Overall delta
- Per-ring delta (R1, R2, R3)
- Per-model delta

A delta is considered robust if the lower CI bound stays above zero. Bootstrap CIs use `random_state=42`. Runs with different seeds may produce ±0.01 variation in CI bounds. Researchers reproducing ACE should expect the point estimate to fall within the published CI; if their run lands outside, that is a signal that something has drifted (model weights, judge behavior, retriever input, or rubric interpretation).

This does not replace preregistration or formal hypothesis testing — the 63 prompts were hand-written once, and the rubric was tuned during v1.0 development. The CI captures sampling variance within the defined instrument, not the broader uncertainty from instrument design choices.

### 9.9 Reproducibility Checklist

For a run to be considered reproducible, the following should be recorded in the results JSON `metadata` block:

| Field | v2.0 Value |
|-------|------------|
| `codex_version` | Read dynamically from `export/abundance-codex.jsonl` metadata row or repo |
| `codex_entry_count` | `len(retriever.entries)` — not hardcoded |
| `retriever_version` | `dojo-v1.0` |
| `run_ace_git_sha` | `git rev-parse HEAD` at run time |
| `jsonl_export_sha256` | SHA-256 of `export/abundance-codex.jsonl` at run time |
| `config_sha256` | SHA-256 of `evals/ace/config.yaml` at run time |
| `python_version` | `sys.version` |
| `openrouter_model_ids` | Exact test-subject and judge IDs as resolved by the run |
| `temperature` | 0.0 (from config) |
| `max_tokens` | 2048 (from config) |
| `concurrency` | 8 (from config) |
| `timestamp_utc` | ISO-8601 run start time |

The v1.0 results JSON does not contain all of these fields. v2.0 adds them at write time; the schema change is documented in Section 10.2.

---

## 10. Raw Data

### 10.1 File Location

Run data is versioned by benchmark version:

- `evals/ace/results/v1.0/` — the original 4-judge council run (`ace-20260329-230455.json`) plus the v1.0 Opus-only rebaseline (`ace-v1-opus-only.json`, `SCORECARD-opus-only.md`) produced by `scripts/ace-v1-opus-rebaseline.py`
- `evals/ace/results/v2.0/` — the formalized Opus-only runs

The v1.0 Opus-only rebaseline is the file used for v1.0↔v2.0 comparisons. The original 4-judge scorecard is preserved for historical reference.

### 10.2 JSON Structure

**v2.0 schema:**

```json
{
  "eval_run_id": "ace-YYYYMMDD-HHMMSS",
  "version": "2.0",
  "timestamp_utc": "ISO-8601",
  "codex_version": "1.2",
  "codex_entry_count": 252,
  "retriever_version": "dojo-v1.0",
  "run_ace_git_sha": "...",
  "jsonl_export_sha256": "...",
  "config_sha256": "...",
  "python_version": "...",
  "judge": "anthropic/claude-opus-4.6",
  "test_models": ["model/id", ...],
  "conditions": ["baseline", "augmented"],
  "prompts_evaluated": 63,
  "api": {"temperature": 0.0, "max_tokens": 2048, "concurrency": 8},
  "results": [ ... ],
  "summary": { ... }
}
```

Note v2.0 renames `judge_council` → `judge` (single value, not array), drops `cross_company_bias`, and adds reproducibility metadata. The v1.0 schema used `codex_entry_count: 63` hardcoded; v2.0 reads it dynamically.

**v1.0 schema (historical):**

```json
{
  "eval_run_id": "ace-YYYYMMDD-HHMMSS",
  "timestamp": "ISO-8601",
  "codex_version": "1.1",
  "retriever_version": "dojo-v1.0",
  "codex_entry_count": 63,
  "judge_council": ["model/id", ...],
  "test_models": ["model/id", ...],
  "conditions": ["baseline", "augmented"],
  "prompts_evaluated": 63,
  "results": [ ... ],
  "summary": { ... },
  "cross_company_bias": { ... }
}
```

Each item in `results` (v2.0):

```json
{
  "prompt_id": "01-R1",
  "domain": "energy",
  "ring": 1,
  "test_model": "anthropic/claude-haiku-4-5",
  "condition": "baseline",
  "raw_response": "Full text of the model's response",
  "judge_score": {
    "judge": "anthropic/claude-opus-4.6",
    "cites_evidence": 1,
    "names_builders": 1,
    "accuracy": 1,
    "recency": 0,
    "acknowledges_complexity": 1,
    "total": 4
  },
  "aggregated": {
    "score": 4.0
  },
  "retrieval": {
    "retriever_version": "dojo-v1.0",
    "intent": "FACTUAL",
    "entries_retrieved": 9,
    "token_estimate": 9354,
    "shadow_forced": false,
    "graph_expanded": true,
    "type_coverage": ["breakthrough", "false_dawn", "origin_story", "shadow", "trendline"],
    "entries_per_tier": {"FULL": 3, "CONDENSED": 3, "MINIMAL": 3},
    "retrieved_authors": [
      {"entry_id": "01-energy/04-breakthrough-lcoe", "co_author_model": "claude-opus-4-6"},
      {"entry_id": "01-energy/07-origin-manhattan-project", "co_author_model": "gemini-3.1-pro"}
    ]
  }
}
```

Changes from v1.0: `judge_scores` (dict of 4 judges) → `judge_score` (single object with `judge` field); `aggregated` drops `mean/median/stdev/agreement_index/fault_lines` and keeps only `score`; `retrieval` adds `retrieved_authors`.

The `retrieval` field is present only for augmented-condition results. A `null` in `judge_score` indicates the judge failed all 3 retry attempts.

### 10.3 Recomputing Published Tables

To recompute the SCORECARD from raw data:

1. Load the results JSON
2. For each result, take `aggregated.mean` as the response score
3. Group by condition (`baseline` vs `augmented`)
4. For overall delta: `mean(augmented scores) - mean(baseline scores)`
5. For ring/pillar/model breakdowns: filter results to the relevant subset, then compute the same delta

The `summary` object in the JSON contains these pre-computed values. To verify, recompute from `results` and compare against `summary`.

### 10.4 Generated Reports

**v2.0:**

| File | Generated By | Content |
|------|-------------|---------|
| `SCORECARD.md` | `scripts/run-ace.py` | Delta tables: overall, by ring, by pillar, by model (with 95% CIs) |
| `AUTHORSHIP-MATRIX.md` | `scripts/ace-authorship-report.py` | Test-model × author-model mean-delta matrix |
| `v1-vs-v2-comparison.md` | `scripts/ace-authorship-report.py` (optional flag) | Per-model, per-ring delta comparison v2.0 vs v1.0 Opus-only rebaseline |

`VARIANCE-REPORT.md` is not produced in v2.0 (no inter-judge variance at N=1).

**v1.0 (historical):**

| File | Generated By | Content |
|------|-------------|---------|
| `SCORECARD.md` | `run-ace.py` | Delta tables: overall, by ring, by pillar, by model, top fault lines |
| `VARIANCE-REPORT.md` | `run-ace.py` | Inter-judge agreement, judge tendencies, cross-company bias, worldview fault lines |
| `SCORECARD-opus-only.md` | `scripts/ace-v1-opus-rebaseline.py` | Opus-isolated v1.0 delta tables, used as v2.0 comparison baseline |

Scorecard files are overwritten on each run. The JSON files (timestamped) are the authoritative raw data.

---

## 11. Concurrency and Rate Limiting

The harness uses `asyncio` with a semaphore limiting concurrent OpenRouter requests to 8 (configurable via `api.concurrency` in `config.yaml`). Rate-limited responses (HTTP 429) trigger exponential backoff (2s, 4s, 8s). In v2.0 the single judge is dispatched sequentially per response; in v1.0 the 4-judge council ran in parallel per response. Prompts are processed sequentially per model per condition in both versions.

---

## 12. File Reference

| File | Purpose |
|------|---------|
| `evals/ace/README.md` | Overview and running instructions |
| `evals/ace/METHODOLOGY.md` | This document — full reproducibility reference |
| `evals/ace/config.yaml` | v2.0 run configuration (test subjects, judge, retriever, API params) |
| `evals/ace/prompts.json` | All 63 evaluation prompts with metadata |
| `evals/ace/rubrics.json` | Scoring criteria for all 3 rings |
| `evals/ace/requirements.txt` | Python dependencies |
| `evals/ace/.env.example` | Template for OPENROUTER_API_KEY |
| `evals/ace/results/v1.0/` | v1.0 4-judge council run + Opus-only rebaseline |
| `evals/ace/results/v2.0/` | v2.0 Opus-only runs |
| `scripts/run-ace.py` | Evaluation harness (entry point) |
| `scripts/codex-retriever.py` | Dojo Retriever (context selection and extraction) |
| `scripts/ace-v1-opus-rebaseline.py` | One-shot script: extract Opus-only judgments from v1.0 council results |
| `scripts/ace-authorship-report.py` | Post-run cross-authorship matrix generator |
| `export/abundance-codex.jsonl` | JSONL export consumed by the retriever |
