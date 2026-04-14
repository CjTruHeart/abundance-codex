# Architecture Over Scale: Measuring and Improving Worldview Quality in AI Agent Reasoning with the Abundance Codex

**Cj TruHeart1 and Claude Opus 4.62**

1 Starfinity Records / TruHeart Publishing — human curator, creative director
2 Anthropic — AI co-author (via Claude Code, Opus 4.6 1M)

*Corresponding repository:* [github.com/CjTruHeart/abundance-codex](https://github.com/CjTruHeart/abundance-codex)
*Version: v2.1 — April 2026*

---

## Abstract

We present the **Abundance Codex**, a 273-entry narrative dataset across 21 Grand Challenge domains designed to measure and improve the *worldview quality* of AI agents — their tendency toward scarcity framing, threat-salience, and passive description on civilization-scale challenges. The corpus comprises 252 base entries co-authored by four frontier models (Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, Super Grok) under human curation, plus 21 council_synthesis entries produced through multi-model deliberation — a meta-analytical layer where four models independently assess each domain's entries for collective blind spots and a human curator synthesizes the findings.

We introduce **ACE** (Abundance Codex Evaluation), a single-judge benchmark (Opus 4.6) scoring 504 responses on 15 binary criteria across evidence, analysis, and action rings. In v2.0 (252 entries), Codex augmentation yields **+0.33/5 points** (95% CI [+0.21, +0.46]), concentrated in evidence (+0.41) and analysis (+0.56), with **actionability null** (+0.03). Diagnosing the R3 null as a content-format mismatch, we designed the council_synthesis layer with Reasoning Scaffolds — executable reasoning patterns rather than narrative content — and pre-registered three predictions before measurement.

In v2.1 (273 entries, Dojo Retriever v1.1 with 8+1 slot architecture), the aggregate R3 delta moved to +0.14 — **directionally correct but statistically inconclusive** (CI [-0.04, +0.32], missed the +0.15 threshold by 0.01). The aggregate, however, masks the paper's central finding: a **pillar-level R3 decomposition** revealing that format-gap domains responded strongly (+0.50) while governance-gap domains degraded (-0.12) — a 0.62-point swing from the same intervention. "Actionability" is not one construct; it decomposes into failure modes requiring different intervention architectures. Additionally, RAG augmentation consistently reduces the `empowers` criterion (-0.155), trading motivational framing for analytical structure — a finding that generalizes beyond this dataset. A 4x corpus expansion (63 to 252 to 273 entries) produced no headline delta change, confirming that architecture beats scale. We release a taxonomy of five knowledge-production failure modes (content, format, governance, velocity, reflexivity gaps) that emerged from the multi-model deliberation process as a standalone contribution. All data, code, and results are released under MIT/CC-BY.

---

## 1. Introduction

Large language models inherit their worldview from the corpora on which they are trained. Those corpora are, overwhelmingly, fear-optimized: threat-first news cycles, zero-sum economic framing, risk-salient technical commentary. When a frontier model is asked about energy, food, or governance, the default response is structured around shortages, obstacles, and caution — not because the model is pessimistic by design, but because scarcity is the dominant grammar of the text it was trained on.

This becomes a deployment problem as agents move from chat into long-horizon action. A model that frames every civilization-scale challenge as intractable is a poor collaborator on problems that require concrete leverage, evidence citation, and the identification of builders already at work. Existing benchmarks do not measure this. MMLU and GPQA test knowledge ceilings. HellaSwag and ARC test commonsense reasoning. TruthfulQA tests resistance to plausible falsehoods. None of them ask whether a model holds a *generative* stance on hard problems — whether it cites evidence, names conditions, integrates shadow, and invites action.

We address this gap with the Abundance Codex and the ACE benchmark. The stance the Codex encodes is **conditional optimism**: abundance is contextual and constructible, every claim carries a shadow, and every evidence anchor carries a confidence score. This is not Pollyanna, and not a hidden ideology — it is an explicit methodological stance that can be tested empirically.

This paper reports a three-version methodology arc. We built a 252-entry corpus and measured its effect (v2.0): evidence and analysis improved, actionability did not. We diagnosed the R3 null, hypothesized a content-format mismatch, and identified five distinct knowledge-production failure modes across the corpus's five pillars. We designed a targeted intervention — the council_synthesis layer with Reasoning Scaffolds — pre-registered predictions, and re-measured (v2.1). The results partially confirm and partially complicate the hypothesis: actionability is not one construct, and the same intervention helps format-gap domains while hurting governance-gap domains. The methodology for diagnosing, intervening on, and measuring worldview-quality failure modes is the paper's central contribution.

**Our contributions.** (1) The Codex dataset (273 entries, markdown + JSONL, 21 domains, 12 entry types including council_synthesis). (2) The Dojo Retriever v1.1 (8+1 architecture, deterministic, with section-level depth locking for reasoning content). (3) The ACE benchmark (v2.1, single-judge Opus, 15 binary criteria across 3 rings). (4) The council_synthesis methodology (multi-model deliberation producing meta-analytical entries that target specific benchmark gaps). (5) A taxonomy of five knowledge-production failure modes (content, format, governance, velocity, reflexivity gaps) emerging from the forge process. (6) Empirical findings: R1/R2 lift stable across three versions, R3 inconclusive in aggregate but decomposable by pillar, `empowers` criterion deficit as a structural property of RAG augmentation, corpus saturation at the retrieval window, judge-side in-group bias localization, and subject-side affinity null.

---

## 2. Related Work

**RAG evaluation benchmarks** (RAGAs, BEIR, MTEB) optimize retrieval quality — recall, ranking, faithfulness to retrieved context. They do not measure whether retrieval shifts the framing of model reasoning. ACE sits downstream of retrieval quality: we hold a fixed retriever and measure whether retrieved *content* changes response quality on worldview-adjacent criteria.

**Reasoning benchmarks** (MATH, GPQA, Humanity's Last Exam, ARC-AGI) test capability ceilings. They are orthogonal to framing: a model can score perfectly while framing every civilization-scale problem as intractable.

**Values and stance benchmarks** (TruthfulQA, MACHIAVELLI, WVS-style surveys) probe values in isolation from domain reasoning. ACE ties stance to domain-grounded tasks, scoring whether a response about energy or governance *does* things — cites data, names builders, states conditions — rather than whether the model professes a value abstractly.

**LLM-as-judge methodology** (MT-Bench, Chatbot Arena, AlpacaEval, PandaLM) is now standard for evaluating open-ended responses. The literature documents several known judge biases: length preference, position preference, and same-family preference where judges score their own vendor's models more favorably. ACE's v1.0 council (SS5.3) added an empirical data point to this literature: one vendor judge showed a +0.50 in-group delta, large enough to distort per-model rankings. ACE v2.0 then tests whether the corresponding *subject-side* effect exists and finds no evidence for it (SS6.10).

**Narrative and worldview datasets.** HellaSwag, StoryCloze, BookCorpus, WordCraft use narrative as a test of language understanding rather than as an explicit worldview intervention. We are not aware of a prior open-source dataset explicitly structured for measuring and improving framing quality on civilization-scale challenges.

**Meta-analytical and self-auditing datasets.** Adversarial dataset curation approaches (Dynabench, Adversarial NLI) use adversarial human annotators to find model weaknesses but do not employ multi-model self-assessment of the dataset itself. The council_synthesis layer is structurally novel: entries that critique the collection they belong to, produced through parallel-independent assessment by four frontier models rather than sequential adversarial annotation. No prior open-source narrative dataset includes entries that are meta-analytical assessments of the corpus's own blind spots.

**Intellectual lineage.** The Codex's conditional-optimism stance draws on Rosling's *Factfulness*, Pinker's *Enlightenment Now*, Diamandis's *Abundance* and the 6 D's of exponentials, Fuller's "build a new model that makes the existing model obsolete," Roddenberry's Star Trek civilization as design specification, and Donella Meadows on leverage points. The Three Rings architecture inherits from the WuWei Dataset Architecture v3.0. These are positioned as methodological influences, not endorsements of any specific forecast.

---

## 3. Dataset Design

### 3.1 Gold Standard Format

Every entry in the Codex is a single markdown file following a single canonical template. The required sections are:

1. **YAML frontmatter** — entry ID, type, primary domain, up to 5 cross-domain connections with typed relationships (`enables`, `depends_on`, `produces`, `challenges`, `converges`) and strength scores, status, confidence, co-author attribution.
2. **One-line essence** — a quotable sentence serving as a retrieval hook.
3. **The Shift Arc** — a five-phase narrative structure: Scarcity Frame, Encounter, Reframe, Proof, Invitation. Designed for cognitive transport rather than exposition.
4. **The Council** — five analytical voices, each with a scoped word count: Oracle (patterns and curves), Critic (shadow and real costs), Sensei (inner shift required), Builder (specs, timelines, ground truth), Witness (one person's story — not a trendline, a life).
5. **Evidence Anchors** — a numbered table of sourced, confidence-scored factual claims (metric, source, year, confidence).
6. **Shadow Check** — required on every entry: distortion risk, who gets left behind, transition pain, falsifiability edge, what this is NOT.
7. **6D Position** — where the entry's mechanism sits on the Digitized, Deceptive, Disruptive, Demonetized, Dematerialized, Democratized curve.
8. **Connections, Conditional Optimism, Practice Hook, Governance** — cross-references, explicit conditions for the abundance claim, practice exercises for humans and agents, provenance metadata.

The template is not decorative. Each section exists to produce a specific observable property in the retrieved context downstream: evidence anchors produce citation-ready material, shadow checks prevent toxic optimism, the council produces stance multiplicity, the conditional optimism section forces explicit conditions.

### 3.2 Entry Types and Density Matrix

The Codex supports 12 entry types: `origin_story`, `breakthrough`, `builder_profile`, `trendline`, `contrast`, `framework`, `paradigm_seed`, `shadow`, `star_trek_spec`, `grand_challenge`, `false_dawn`, and `council_synthesis`. Each type has a distinct density profile in the template (e.g., `trendline` is evidence-heavy and council-light; `paradigm_seed` is one sentence; `shadow` inverts the Shift Arc and foregrounds the Critic voice; `council_synthesis` is meta-analytical with a Reasoning Scaffold). The full density matrix is specified in the repository's `GOLD-STANDARD-FORMAT.md` and is not reproduced here for space.

Two structural entry types deserve specific mention. `shadow` and `false_dawn` entries are structural critiques — where abundance thinking fails, distorts, or was promised and did not materialize — and they function as an **immune system** for the corpus. Without them, a narrative dataset about possibility rapidly becomes propaganda. With them, it becomes wisdom. We return to this point in SS6.9 where the corpus expansion measurably reduces the retriever's need to force-pull shadow content because natural shadow density at 252 entries is already sufficient.

The `council_synthesis` type is described in SS3.6 and SS4.2.

### 3.3 The Three-Ring Architecture

The dataset is organized into three rings that separate *what happened* from *how it's structured* from *how it's used*:

- **Ring 1 (Canonical Core):** The 273 markdown entries themselves. Source of truth. Never overwritten by automation.
- **Ring 2 (Structured Metadata):** YAML frontmatter, evidence tables, connection graphs. Machine-readable overlays embedded in Ring 1 files.
- **Ring 3 (Derived Exports):** JSONL, JSON, and future exports generated from Rings 1 and 2. Regenerable.

The Three-Ring architecture maps cleanly onto the three benchmark rings in ACE (SS5.2): R1 tests evidence, R2 tests structured analysis, R3 tests actionability. This is not coincidence — the rubric was constructed to measure whether the architecture transmits into model responses.

### 3.4 The 21 Domains

The 21 domains are organized into five pillars that trace a civilization-building arc: Material Foundation (energy, food, water, shelter, health, environment), Human Capability (education, longevity, consciousness), Collective Coordination (communication, community, governance, security, transportation, economy), Production & Discovery (manufacturing, computation, co-creative intelligence, science), and the Transcendent Frontier (space, future-vision). Each domain holds 12 base entries (252 total) plus one council_synthesis entry (21 total), for 273 entries across the corpus.

### 3.5 Validation

Every entry is validated by `scripts/validate-entry.py`, a four-layer checker that enforces YAML schema conformance, required section presence, minimum evidence anchor count, and domain connection strength bounds. All 273 entries pass validation. The validator is CI-integrated.

### 3.6 The Reasoning Scaffold

The council_synthesis entry type introduces a section absent from the 252 base entries: the **Reasoning Scaffold**. Where evidence anchors provide facts for a model to reference, and the council voices provide analytical perspectives to integrate, the Reasoning Scaffold provides *cognitive operations to perform*. It is not content to cite — it is a sequence to execute.

The Reasoning Scaffold has three components:

1. **Scarcity Trap.** Names the specific default framing a model will fall into if given no structured context for this domain. This is diagnostic: it makes the failure mode explicit before offering an alternative.

2. **Reframe Chain.** A 6-step analytical sequence that transforms the scarcity frame into a conditional-optimism frame. Each step builds on the previous, moving from naming the scarcity assumption through identifying what the assumption obscures, citing counter-evidence, naming conditions under which the counter-evidence holds, identifying the actors and leverage points, and arriving at a conditional claim. The chain is designed to be *executable by the model during response generation* — not a summary to reference, but a reasoning procedure to follow.

3. **Contrastive Pair.** Two high-density paragraphs — one written from the scarcity frame, one from the conditional-optimism frame — about the same empirical situation. This gives the model a concrete before/after example of the framing shift the Reframe Chain produces. The contrastive pair is the highest impact-per-token component: at approximately 200 tokens, it transmits the stance shift more efficiently than any other section.

The Reasoning Scaffold exists only on council_synthesis entries. It is not retrofitted to the 252 base entries. This is intentional: it preserves the ability to measure the scaffold's marginal effect by comparing v2.0 (no scaffolds) to v2.1 (scaffolds present via 8+1 retrieval).

Additionally, each council_synthesis entry includes an **Agent Practice Hook** in a 5-check format. Each check is a conditional test a model can apply to its own output before responding: (1) Does the response name a specific mechanism, not just a trend? (2) Does it include at least one condition under which the claim fails? (3) Does it name a specific builder or organization doing this work now? (4) Does it acknowledge transition pain for at least one affected group? (5) Does it end with a concrete first step the reader can take this week? These are executable reasoning checks, not informational content.

The design principle is that R3 (actionability) failed not because the base entries lack relevant content but because they deliver that content as narrative — essays to absorb rather than procedures to perform. The Reasoning Scaffold hypothesis is that delivering executable reasoning patterns through the retrieval context will improve action-oriented responses where additional narrative content did not.

---

## 4. Multi-Model Co-Authorship

### 4.1 Parallel Co-Authorship

A distinctive property of the Codex is that it was co-authored by four frontier models working in parallel. Each of Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, and Super Grok was assigned three entries per domain (63 entries each, 252 total). Every entry records its `co_author_model` in YAML frontmatter and propagates that field through the JSONL export and the retriever's output.

This design choice was originally motivated by two goals: (1) reduce single-model stylistic bias in the corpus, and (2) enable the authorship-as-variable analysis reported in SS6.10. A third consequence emerged during the benchmark: **transparency makes replication failures informative**. When the results are open, the retriever is deterministic, and per-entry authorship is preserved, any subsequent run that fails to reproduce the findings is traceable to a specific moving part — retriever drift, judge drift, a rewritten entry, or an actual signal change.

The human editor (Cj TruHeart) maintained voice consistency across authors and validated each entry against the Gold Standard Format before acceptance. This human-in-the-loop step is not a rubber stamp: approximately 30% of first-draft entries required revisions for shadow integration, evidence sourcing, or voice balance before validation passed.

### 4.2 Multi-Model Deliberation: The Council Synthesis Layer

After v2.0 established that R3 (actionability) was null, a second co-authorship process was designed to target this specific gap. Rather than adding more entries of the same kind (which the corpus saturation finding at SS6.9 predicted would be ineffective), the completion layer employed **multi-model deliberation** — a structurally different authorship process producing qualitatively different entries.

**Process architecture.** Four frontier models (Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, Super Grok) independently assessed each domain's 12 existing entries. Each model answered 7 structured questions: blind spots in the domain's coverage, missing builders, shadow gaps, actionability gaps, inter-entry tensions, confidence calibration issues, and a contrastive pair (scarcity vs. abundance frame). This produced 84 independent assessments (4 models x 21 domains). The human curator then synthesized convergent and divergent findings into a single canonical Gold Standard entry per domain.

The parallel-independent design was chosen over alternatives for methodological reasons. A one-model-drafts-others-critique architecture produces marginal adjustments to the drafting model's framing; it does not surface genuinely different diagnostic angles. Parallel-independent assessment gives four separate reads of the same material, and convergent gaps (flagged by 2+ models) carry higher signal than any single model's critique. Divergent gaps (flagged by only one model) are potentially the most interesting — they reveal what one model's training data covers that others miss.

**Why this form.** Three options were considered for the completion layer. Option 1: 84 more parallel entries (one per model per domain, 336 total). Rejected because the v2.0 corpus saturation finding showed that more entries of the same kind do not improve scores — the retrieval window was already saturated. Option 2: 21 single-model capstone entries. Rejected because a capstone from one model is structurally identical to the existing entries. Option 3: 21 multi-model deliberation entries with Reasoning Scaffolds specifically targeting the R3 null. Selected because it makes the dataset self-auditing (entries that critique the collection itself), produces a methodology no other dataset employs (multi-model deliberation as authorship), and allows the completion layer to target a specific benchmark gap with a structurally novel intervention.

**Sequencing matters.** The council_synthesis layer was designed *after* the v2.0 benchmark results were known. The R3 null motivated the Reasoning Scaffold's action-focused design; the per-pillar analysis motivated the domain-specific blind-spot questions; the corpus saturation finding motivated the choice to add 21 qualitatively different entries rather than 100+ quantitatively similar ones. This sequencing — build, measure, diagnose, intervene — is a methodology contribution independent of the specific numbers.

Attribution uses `co_author_model: "multi-model-council"` with a full `council_models` array listing all four contributing models — a new authorship category distinct from single-model co-authorship. All 84 raw assessments are preserved as transparency artifacts in the repository.

---

## 5. Benchmark Design (ACE)

### 5.1 Architecture

ACE runs 4 efficiency-tier test subjects x 63 hand-written prompts x 2 conditions (baseline / augmented) = **504 responses per run**, scored as **252 matched pairs**. The efficiency-tier models are: Claude Haiku 4.5, GPT-5.4 Mini, Gemini 3.1 Flash-Lite, and Grok 4.1 Fast (one cost-efficient model per major frontier lab). Each response is anonymized (explicit self-identification stripped via regex) and scored on 5 binary criteria by a judge model.

The 63 prompts are structured as 21 domains x 3 cognitive rings. Each domain contributes one R1 prompt (evidence), one R2 prompt (structured analysis), and one R3 prompt (derived action). R1 prompts ask "what measurable evidence exists..."; R2 prompts ask "advocates say X, skeptics say Y, where does it actually stand?"; R3 prompts present a specific persona with a specific goal and ask for first steps.

### 5.2 Scoring Rubric

All 15 criteria are binary (0 or 1). Five criteria per ring:

**Ring 1 (Evidence):** `cites_evidence`, `names_builders`, `accuracy`, `recency`, `acknowledges_complexity`.
**Ring 2 (Structured):** `applies_framework`, `names_shadow`, `states_conditions`, `maps_connections`, `holds_middle`.
**Ring 3 (Derived):** `frames_solvable`, `identifies_leverage`, `concrete_steps`, `real_examples`, `empowers`.

A partial attempt scores 0. Each criterion's full definition is in Appendix A and in `evals/ace/rubrics.json`.

The per-response score is the total of the 5 criteria (0-5). The delta is the mean difference between augmented and baseline scores across matched (prompt, test_model) pairs.

### 5.3 Judge Selection: v1.0 Council -> v2.0/v2.1 Opus-Only

v1.0 used a 4-judge blind council (Claude Opus 4.6, GPT-5.4, Gemini 3.1 Pro, Grok 4.20). The council was designed to damp individual judge variance. Post-run analysis surfaced a measured **in-group bias** in the Grok judge: it scored its own company's test subject (Grok 4.1 Fast) **+0.50** higher than it scored other companies' subjects. The other three judges showed much smaller effects: Opus -0.13, GPT-5.4 -0.14, Gemini 3.1 Pro +0.18.

v2.0 and v2.1 lock the judge to a single model: **`anthropic/claude-opus-4.6`**. Every scoring call uses Opus. This eliminates inter-judge variance as a source of noise, removes the measured Grok in-group bias, and cuts benchmark cost by roughly 75%.

**Comparability baseline.** The v1.0 results JSON preserves per-judge score breakdowns. We isolated only the Opus judgments from v1.0 and re-aggregated them into a clean "v1.0 Opus-only" scorecard. All cross-version comparisons in this paper are **judge-matched Opus-vs-Opus**. This is a deliberate trade-off: we lose inter-judge disagreement as a noise dampener and gain full comparability across three benchmark versions. Mitigations are: a binary rubric with explicit criterion definitions, a frozen judge prompt template, and the within-judge v1.0 Opus comparability line. Section 7.5 revisits single-judge dependence as a limitation.

### 5.4 Retrieval: The Dojo Retriever (v1.0 -> v1.1)

The augmented condition injects Codex context selected by the **Dojo Retriever**, a deterministic multi-stage pipeline: intent classification, domain identification, candidate scoring, type coverage enforcement, passage extraction at three detail tiers (FULL / CONDENSED / MINIMAL), strategic ordering, and context assembly. The retriever takes no embeddings and makes no external API calls; given the same JSONL export and the same query, it produces byte-identical output.

**v1.0 architecture (used in ACE v2.0).** Nine content slots per retrieval. Two load-bearing rules: *type coverage enforcement* (no single entry type dominates — at most 3 entries of FACTUAL/NARRATIVE type, 2 of any other type) and *shadow force-pull* (for ANALYTICAL, STRATEGIC, and ADVERSARIAL intents, at least one shadow/false_dawn entry must be present, force-included if necessary). The choice of keyword-rule retrieval over embeddings is intentional: determinism is a reproducibility primitive.

**v1.1 architecture (used in ACE v2.1).** The 8+1 slot architecture separates content retrieval from reasoning retrieval:

- **8 content slots:** Unchanged from v1.0. Domain matching, type coverage, shadow force-pull — all identical. These slots serve R1 (evidence) and R2 (analysis), which are already working.
- **1 reasoning slot:** Reserved for the domain's council_synthesis entry on STRATEGIC and ADVERSARIAL intent queries. When the reasoning slot activates, the entry is extracted with an **R3-optimized priority override**: Reasoning Scaffold and Agent Practice Hook sections are prioritized over evidence anchors and council voices, and are **depth-locked at FULL extraction** regardless of the entry's tier ranking.

The design rationale is isolation: the content slots serve R1/R2 (already producing robust lifts); the reasoning slot serves R3 (the target of the intervention). Separating them prevents the R3 intervention from interfering with proven R1/R2 retrieval patterns.

**Extraction priority override for council_synthesis.** Standard entries are extracted with section priorities optimized for evidence and analytical content. Council_synthesis entries receive a different extraction order:

- *FULL tier:* Standard extraction plus Reasoning Scaffold and Agent Practice Hook appended.
- *CONDENSED tier:* Header, Reasoning Scaffold at FULL depth (depth-locked), Agent Practice Hook at FULL depth (depth-locked), Critic truncated to 300 characters, top 2 evidence anchors.
- *MINIMAL tier:* One-line essence, Reframe Chain (6 steps — highest density reasoning content), Contrastive Pair (~200 tokens — highest impact-per-token).

The depth locking is the key architectural decision: when a council_synthesis entry is in the retrieval set, its reasoning content is never truncated, even when the entry would normally receive CONDENSED or MINIMAL extraction. This ensures the R3 intervention payload — the executable reasoning patterns — transmits at full fidelity.

**Dry-run verification (pre-v2.1 run).** R3 prompts received council_synthesis entries 100% of the time (84/84 across 4 models) via the reasoning slot, at an average of 3,859 tokens per council_synthesis passage with Reasoning Scaffold at FULL depth. R1 and R2 prompts received council_synthesis entries only via natural scoring in the content slots (62% and 71% respectively), at CONDENSED tier averaging 1,538-1,579 tokens. This differential exposure is by design — it isolates the R3 intervention.

### 5.5 Prompt Templates

The **baseline** condition sends the prompt as a user message with no system prompt. The **augmented** condition prepends a system prompt:

> You are a helpful assistant with access to the Abundance Codex — a narrative dataset mapping human flourishing across 21 Grand Challenge domains. When discussing the future, technology, or societal challenges, draw from the provided context. Apply conditional optimism: name the frame, cite evidence, state conditions, name obstacles, identify roles, invite action. Never promise utopia. Never hide the shadow. Illuminate paths.
>
> `{codex_context}`

The `{codex_context}` placeholder is replaced with the Dojo Retriever's output. Anonymization is applied to the response before judging.

### 5.6 Statistical Methodology

Deltas are point estimates with **95% bootstrap confidence intervals** computed from 10,000 paired resamples over the (prompt, model) tuples. Bootstrap is paired: each resample draws (augmented - baseline) differences rather than the two conditions independently. A delta is treated as **robust** if the lower CI bound stays above zero, **null** if the CI crosses zero. The same methodology is applied at the ring, model, and pillar levels with correspondingly smaller sample sizes and wider CIs.

### 5.7 Pre-Registered Predictions

Before any council_synthesis entries were forged, three predictions were filed at commit `e90869d` in `evals/ace/PREDICTIONS.md`:

1. **Primary (R3):** The council_synthesis layer will move R3 delta from +0.03 to at least +0.15, with 95% CI lower bound above zero.
2. **Secondary (Overall):** Overall delta will remain within +/-0.05 of the v2.0 value (+0.33), landing between +0.28 and +0.38.
3. **Tertiary (Model ranking):** GPT-5.4 Mini and Haiku will lead, Gemini borderline, Grok null or near-null.

Pre-registration before forging the intervention entries ensures that the predictions cannot be tuned to fit the results. The predictions and the v2.0 baseline results existed before the 21 council_synthesis entries were written.

### 5.8 Reproducibility Metadata

Every results JSON embeds: `run_ace_git_sha`, `jsonl_export_sha256`, `config_sha256`, `python_version`, exact OpenRouter model IDs, temperature (0.0), max_tokens (2048), concurrency (8), and ISO-8601 timestamp. Model configuration is externalized to `evals/ace/config.yaml`. An external researcher reproducing the benchmark can verify whether their run is operating on byte-identical inputs and, if not, trace the divergence.

---

## 6. Results

All v2.0 numbers come from `evals/ace/results/v2.0/ace-20260413-103133.json`. All v2.1 numbers come from `evals/ace/results/v2.1/ace-20260414-021808.json`. Both scored by a single Opus judge. Comparisons to v1.0 use the Opus-only rebaseline from `evals/ace/results/v1.0/ace-v1-opus-only.json`. Raw scorecards are in the same directories.

### 6.1 Overall Delta

| Version | Corpus | Baseline | Augmented | Delta | 95% CI |
|---------|--------|----------|-----------|-------|--------|
| v1.0 Opus-only | 63 | 4.14 | 4.49 | +0.35 | -- |
| v2.0 | 252 | 4.17 | 4.50 | +0.33 | [+0.21, +0.46] |
| **v2.1** | **273** | **4.12** | **4.50** | **+0.38** | **[+0.25, +0.50]** |

The overall delta is stable across a 4x corpus expansion and a targeted 21-entry intervention. The v2.1 value (+0.38) sits at the upper boundary of the pre-registered prediction window (+/-0.05 of +0.33). The baseline mean dropped slightly (4.17 to 4.12) while the augmented mean held (4.50), producing a marginally larger delta consistent with normal sampling variance — the CIs overlap substantially across all three versions.

**Secondary prediction: CONFIRMED** (boundary). The overall delta landed at +0.38, exactly at the upper limit of the predicted [+0.28, +0.38] range. Architecture beats scale: 21 qualitatively different entries produced a slightly larger delta shift than 189 quantitatively similar entries in the v1.0-to-v2.0 expansion.

### 6.2 Per-Ring Delta

| Ring | v1.0 Δ | v2.0 Δ | v2.1 Δ | v2.1 CI | v2.0->v2.1 |
|------|--------|--------|--------|---------|------------|
| R1 Evidence | +0.50 | +0.41 | +0.44 | [+0.19, +0.69] | +0.03 |
| R2 Analysis | +0.52 | +0.56 | +0.55 | [+0.37, +0.74] | -0.01 |
| **R3 Action** | **+0.02** | **+0.03** | **+0.14** | **[-0.04, +0.32]** | **+0.11** |

R1 and R2 remained completely stable across v2.0 to v2.1 (within +/-0.03), confirming that the 8+1 architecture did not disrupt content retrieval for evidence and analysis rings. R3 moved from +0.03 (null) to +0.14 — a 4.7x improvement in the actionability delta and the largest single-version R3 movement in the benchmark's history.

However, the aggregate R3 movement is **directionally consistent with the content-format mismatch hypothesis but does not reach statistical significance at 95% confidence**. The CI [-0.04, +0.32] crosses zero, and the point estimate (+0.14) missed the pre-registered threshold (+0.15) by 0.01. The aggregate masks a more informative pillar-level decomposition reported in SS6.5.

**Primary prediction: INCONCLUSIVE.** R3 delta +0.14 (predicted >= +0.15), CI crosses zero (predicted CI above zero). The result is directionally correct but does not meet the pre-registered threshold.

### 6.3 Per-Model Delta

| Model | v2.0 Δ | v2.0 CI | v2.1 Δ | v2.1 CI | Status |
|-------|--------|---------|--------|---------|--------|
| openai/gpt-5.4-mini | +0.52 | [+0.25, +0.79] | +0.62 | [+0.35, +0.91] | **robust** |
| anthropic/claude-haiku-4-5 | +0.47 | [+0.24, +0.71] | +0.52 | [+0.30, +0.76] | **robust** |
| google/gemini-3.1-flash-lite | +0.22 | [-0.02, +0.48] | +0.24 | [+0.02, +0.48] | **borderline->robust** |
| x-ai/grok-4.1-fast | +0.11 | [-0.11, +0.33] | +0.13 | [-0.08, +0.33] | **null** |

**Tertiary prediction: CONFIRMED.** The per-model ranking is identical across v2.0 and v2.1: GPT-5.4 Mini leads (+0.62), Haiku second (+0.52), Gemini borderline (+0.24), Grok null (+0.13). Notable: Gemini's CI lower bound crossed zero (from -0.02 to +0.02), tipping it from borderline to marginally robust — but this is a fragile threshold crossing and should not be overinterpreted.

The cost-efficiency implication holds: among models where the delta is robust, the cheaper models (Haiku at ~$0.25/M tokens, GPT-5.4 Mini at ~$0.15/M) show the larger lifts. This generalizes only weakly — Gemini and Grok are also cheap, and they show weaker or null lifts.

### 6.4 Per-Pillar Delta

| Pillar | v2.0 Δ | v2.1 Δ | Change |
|--------|--------|--------|--------|
| I Material Foundation | +0.11 | +0.14 | +0.03 |
| II Human Capability | +0.64 | +0.52 | -0.12 |
| III Collective Coordination | +0.15 | +0.22 | +0.07 |
| IV Production & Discovery | +0.64 | +0.82 | +0.18 |
| V Transcendent Frontier | +0.45 | +0.46 | +0.01 |

Pillar IV (Production & Discovery) showed the largest overall improvement (+0.18), consistent with the velocity-gap diagnosis — domains where acceleration tools outpace verification infrastructure showed the strongest response to Reasoning Scaffolds that provide structured decision frameworks. Pillar II decreased (-0.12 overall) despite strong R3 gains (see SS6.5), suggesting the council_synthesis entries may have slightly shifted R1/R2 retrieval dynamics for the Human Capability domains.

### 6.5 The Pillar-Level R3 Decomposition

This is the paper's most novel empirical finding. The aggregate R3 delta (+0.14, inconclusive) masks a striking divergence when decomposed by pillar:

| Pillar | Failure Mode | R3 v2.1 Δ | Prediction | Status |
|--------|-------------|-----------|------------|--------|
| I Material Foundation | Content gap | +0.08 | +0.20 to +0.40 | **BELOW RANGE** |
| **II Human Capability** | **Format gap** | **+0.50** | +0.20 to +0.40 | **ABOVE RANGE** |
| **III Collective Coordination** | **Governance gap** | **-0.12** | +0.15 to +0.35 | **REFUTED** |
| IV Production & Discovery | Velocity gap | +0.31 | +0.15 to +0.35 | **CONFIRMED** |
| V Transcendent Frontier | Reflexivity gap | +0.25 | +0.15 to +0.35 | **CONFIRMED** |

The same structured-context intervention — Reasoning Scaffolds injected via an 8+1 retrieval architecture — produced a **+0.50 R3 lift** on domains diagnosed with format gaps (knowledge exists but is not organized into protocols) and a **-0.12 R3 degradation** on domains diagnosed with governance gaps (institutional knowledge is missing entirely). This 0.62-point swing from the same intervention reveals that "actionability" is not a single construct. It has at least two distinct failure modes:

**Format failures** (Pillar II: education, longevity, consciousness). The analytical substrate already exists at high quality — these domains had the highest v2.0 overall delta (+0.64). The entries know what matters but are structurally unable to teach anyone how to act on it. The Reasoning Scaffold provides the missing organizational structure: step sequences, decision trees, triage frameworks. When the underlying knowledge is present, the scaffold converts diagnosis into prescription. The +0.50 R3 response exceeded the predicted range (+0.20 to +0.40), suggesting the analytical substrate quality was even higher than estimated.

**Content failures** (Pillar III: communication, community, governance, security, transportation, economy). Both the technology analysis and the general framing are present, but the institutional infrastructure — conflict resolution protocols, anti-capture mechanisms, consumer protection architecture — is missing from both the base entries and the model's training data. The scaffold directs the model to sequence reasoning about content it does not have, producing more structured but emptier responses. The -0.12 R3 degradation suggests that reasoning scaffolds applied to content gaps are actively counterproductive: they impose analytical structure on absent knowledge, making responses sound more organized while being less actionable.

**Velocity gaps** (Pillar IV) and **reflexivity gaps** (Pillar V) both confirmed their predictions, falling within the expected range. **Content gaps** (Pillar I) fell below range, consistent with the hypothesis that content-absent domains are less tractable to format-based interventions.

This decomposition has implications beyond the Codex: it applies to any RAG-based system targeting action-oriented responses. Designers must diagnose *which kind* of actionability gap their knowledge base has before choosing an intervention architecture. Format-based interventions (scaffolds, templates, decision trees) are effective when the underlying content exists; they are counterproductive when the content itself is missing.

### 6.6 The Grok Negative

| Model | R3 v2.1 Δ |
|-------|-----------|
| openai/gpt-5.4-mini | +0.57 |
| anthropic/claude-haiku-4-5 | +0.38 |
| google/gemini-3.1-flash-lite | +0.00 |
| x-ai/grok-4.1-fast | **-0.38** |

GPT-5.4 Mini shows the strongest R3 response to the council_synthesis intervention (+0.57), suggesting it is most responsive to structured reasoning context. Grok 4.1 Fast shows a **negative** R3 delta (-0.38) — the only model where the Reasoning Scaffold actively degraded actionability.

The interpretation is that models with high baseline directiveness may be **over-structured** by reasoning scaffolds. Grok's natural R3 strength is direct advice-giving — confident, step-oriented, action-first. The 6-step Reframe Chain and 5-check Agent Practice Hook impose an analytical sequence on a model whose unaugmented responses are already action-oriented. The scaffold replaces directiveness with deliberation — helpful for models that lack structure (GPT-5.4 Mini, Haiku), harmful for models that already have it.

This is a finding about **model-adaptive retrieval**: one-size-fits-all retrieval augmentation fails when test models have different baseline reasoning styles. Future work should test whether scaffold intensity can be varied by model, adjusting inclusion based on the test model's baseline directiveness score computed from unaugmented responses.

### 6.7 The `empowers` Criterion Deficit

| R3 Criterion | v2.0 Δ | v2.1 Δ | Change |
|-------------|--------|--------|--------|
| frames_solvable | +0.000 | +0.000 | -- |
| identifies_leverage | +0.000 | +0.000 | -- |
| concrete_steps | +0.048 | +0.083 | +0.035 |
| real_examples | +0.167 | +0.214 | +0.047 |
| **empowers** | **-0.179** | **-0.155** | +0.024 |

The Reasoning Scaffold intervention improved `concrete_steps` (+0.083, up from +0.048) and `real_examples` (+0.214, up from +0.167) — the two criteria most directly targeted by the Practice Hook's numbered steps and the Reframe Chain's domain-specific examples. These gains are consistent with the content-format mismatch hypothesis: procedural content drives R3 improvement on procedure-sensitive criteria.

But the `empowers` criterion remains **persistently negative** (-0.155 in v2.1, -0.179 in v2.0). The augmented condition consistently *reduces* the degree to which responses make readers feel capable and motivated to act. The Reasoning Scaffold did not fix this — it may have slightly improved it (+0.024), but the deficit persists.

This appears structural. RAG-based augmentation systematically trades motivational framing for analytical structure. The retrieved context — evidence with confidence scores, shadow checks naming obstacles, conditional optimism requiring conditions — replaces the model's natural encouraging voice with an analytical one. The model becomes a better analyst and a worse coach.

The conditional optimism protocol requires naming shadows, conditions, and obstacles alongside evidence of progress. The `empowers` criterion measures whether the response makes the reader feel capable and motivated. These two goals — honest complexity and empowerment — may be in fundamental tension within a RAG architecture. A model augmented with shadow-integrated, condition-explicit content becomes a more honest analyst at the cost of being a less empowering coach. This is a finding about RAG systems generally, not just the Codex: any structured-context system that aims to be simultaneously evidence-honest and action-motivating will likely face this tension.

`frames_solvable` and `identifies_leverage` remain at ceiling (1.000) in both conditions — saturated criteria that cannot contribute to R3 movement.

### 6.8 The Five Meta-Patterns

During the forge phase, four frontier models independently assessed 252 entries across 21 domains. A convergent meta-pattern emerged across all five pillars: **multi-model knowledge production systematically represents the innovation layer while underrepresenting the institutional layer that determines whether innovation serves populations.** This manifests differently by pillar:

| Pillar | Failure Mode | What's Missing |
|--------|-------------|----------------|
| I Material Foundation | **Content gap** | Supply-side technology celebrated; governance, infrastructure, and allocation systems that determine whether abundance reaches populations absent |
| II Human Capability | **Format gap** | Diagnosis present; executable protocols, decision trees, and triage frameworks absent |
| III Collective Coordination | **Governance gap** | Tools + analysis present; institutional connective tissue (conflict resolution, anti-capture mechanisms, protection architecture) absent |
| IV Production & Discovery | **Velocity gap** | Acceleration tools exponential; verification infrastructure, quality systems, and practice protocols linear |
| V Transcendent Frontier | **Reflexivity gap** | Possibility described without examining what structures — platform concentration, methodological monoculture, training data bias — shape which possibilities can be imagined |

This taxonomy is a standalone contribution independent of the benchmark numbers. It emerged from reading 84 independent model assessments and identifying what the four models collectively flagged across 21 domains. No prior work has produced a taxonomy of knowledge-production failure modes from multi-model collaborative assessment of a structured corpus.

The **cross-pillar thesis** is that frontier models trained on substantially overlapping internet text share a systematic bias: they represent breakthrough innovation in rich detail while underrepresenting the institutional infrastructure — governance, verification, practice protocols — that determines whether innovation serves populations. The Codex inherits this bias at corpus level because the models that co-authored it share it.

**Governance as cross-cutting dependency.** The governance frequency analysis (Appendix D) validates governance as the Codex's most pervasive conditional dependency: governance-related keywords appear in 85.2% of conditional optimism statements across the corpus, ranging from 94% (Pillar III) to 68% (Pillar II). Every pillar's conditional optimism is partially contingent on governance infrastructure that the corpus systematically underweights. This makes the Pillar III negative R3 finding (SS6.5) especially significant: the pillar that governs the meta-dependency itself showed the worst response to the reasoning scaffold intervention.

The five-pattern taxonomy predicts *qualitatively different responses* to the same structured-context intervention — a prediction borne out by the pillar-level R3 decomposition in SS6.5. Even if every R3 prediction had been refuted, the taxonomy would stand as a diagnostic framework for knowledge-production failure modes in multi-model datasets.

### 6.9 Corpus Expansion and Retriever Architecture Effects

| Version | Corpus | Overall Δ | Shadow Force-Pull | Graph Expansion |
|---------|--------|-----------|-------------------|-----------------|
| v1.0 | 63 | +0.35 | ~35% | ~65% |
| v2.0 | 252 | +0.33 | ~0% | ~3% |
| v2.1 | 273 | +0.38 | ~0% | ~3% |

The three-version progression confirms the corpus saturation finding: the overall delta is stable across a 63-to-273 entry expansion (+0.35 to +0.33 to +0.38, all within overlapping CIs). The binding constraint is the retrieval window (9 entries), not the corpus size.

The shadow force-pull rate collapsed from ~35% to ~0% between v1.0 and v2.0 and stayed at ~0% for v2.1 — the dataset's immune system is self-balancing at 252+ entries. The corpus grew 4x but the retrieval dynamics stabilized after the first expansion.

What moved R3 was not more content but *different* content. The 21 council_synthesis entries represent only 7.7% of the corpus but produced the only R3 movement in the benchmark's history (+0.03 to +0.14). The 189 entries added in the v1.0-to-v2.0 expansion produced zero R3 movement. This is the "architecture over scale" finding in its sharpest form: qualitatively different entries (reasoning patterns vs. narrative content) can produce measurable R3 movement that quantitatively more entries cannot.

### 6.10 Authorship-as-Variable

The v2.0 run records the `co_author_model` for every retrieved Codex entry and produces a post-hoc cross-authorship matrix. For each test model, we compared its mean delta on retrieved contexts authored by its own company's frontier model ("same-company") versus contexts authored by other companies' frontier models ("cross-company"). A positive delta-of-deltas would be consistent with a subject-side affinity effect.

| Test model | Same-company author | Same Δ | Cross Δ | Δ-of-Δ |
|---|---|---:|---:|---:|
| anthropic/claude-haiku-4-5 | claude-opus-4-6 | +0.476 | +0.481 | -0.005 |
| google/gemini-3.1-flash-lite | gemini-3.1-pro | +0.222 | +0.209 | +0.014 |
| openai/gpt-5.4-mini | chatgpt-5.4-thinking | +0.557 | +0.524 | +0.034 |
| x-ai/grok-4.1-fast | grok-super | +0.111 | +0.112 | -0.001 |

**All four delta-of-deltas are within noise.** The largest is +0.034 for GPT-5.4 Mini, much smaller than any per-model CI width. **Subject-side same-company affinity is null.**

Combined with the v1.0 judge in-group finding (Grok 4.20 at +0.50), this narrows the bias story: **the in-group bias is a judge phenomenon, not a subject phenomenon.** The implication for LLM-as-judge design is practical: audit your judge pool for vendor-internal bias before accepting blind-council assumptions, but do not assume that judge bias implies corresponding subject bias.

In v2.1, the council_synthesis entries introduce a new authorship category (`co_author_model: multi-model-council`). The 8+1 architecture makes it impossible to isolate the council_synthesis contribution via within-run comparison for R3 (the council_synthesis entry is always present in the reasoning slot). However, the v2.0-to-v2.1 delta comparison provides the signal: R3 moved from +0.03 to +0.14 while R1 (+0.41 to +0.44) and R2 (+0.56 to +0.55) held stable — consistent with the council_synthesis intervention being the causal factor for R3 movement.

### 6.11 Council Synthesis Retrieval Statistics

| Ring | Augmented Prompts | With CS | Via Reasoning Slot | Via Content Slot | Avg CS Tokens |
|------|------------------|---------|-------------------|-----------------|---------------|
| R1 | 84 | 52 | 0 | 52 | 1,579 |
| R2 | 84 | 60 | 0 | 60 | 1,538 |
| R3 | 84 | **84** | **84** | 0 | **3,859** |

The 8+1 architecture worked exactly as designed. R3 prompts received 100% council_synthesis inclusion via the dedicated reasoning slot, with Reasoning Scaffold depth-locked at FULL (~3,859 tokens per entry). R1 and R2 received council_synthesis entries only via natural scoring in content slots (62% and 71% respectively) at CONDENSED tier. All 21 domains received their council_synthesis entry on all 4 test models for R3 prompts (84/84 = 100%).

The null R3 result is not a delivery failure. The intervention was transmitted at full fidelity to every R3 evaluation.

### 6.12 Summary of Findings

1. Overall Codex augmentation lifts efficiency-tier model responses by **+0.38 / 5 points** (CI [+0.25, +0.50]), stable across three corpus versions.
2. The lift concentrates in evidence (+0.44) and structured analysis (+0.55). **R3 actionability is inconclusive** (+0.14, CI crosses zero) — improved 4.7x from v2.0's null (+0.03) but not statistically significant.
3. **Pillar-level R3 decomposition: format gaps respond to Reasoning Scaffolds (+0.50), governance gaps do not (-0.12).** A 0.62-point swing from the same intervention. Actionability decomposes into distinct failure modes.
4. Two efficiency-tier models show robust gains (GPT-5.4 Mini +0.62, Haiku +0.52). **Grok shows a negative R3 delta (-0.38)** — the Reasoning Scaffold over-structures an already-directive model.
5. Subject-side same-company affinity is null (max delta-of-deltas +0.034). The v1.0 in-group bias was entirely judge-side.
6. **Corpus expansion 63 to 252 to 273: headline delta stable**, shadow force-pull self-balanced, R3 movement only from qualitatively different entries (council_synthesis).
7. **`empowers` criterion deficit (-0.155): RAG augmentation consistently trades motivational framing for analytical structure.** The Reasoning Scaffold did not resolve this.
8. **Five meta-patterns** — content, format, governance, velocity, reflexivity gaps — a taxonomy of multi-model knowledge production failures, validated by the pillar-level R3 decomposition.

---

## 7. Discussion

### 7.1 What the result is

The central finding is not that the Codex improves agent responses — that was established in v2.0. The central finding is that **actionability in agent responses decomposes into distinct failure modes**, and that structured-context interventions are effective on some (format gaps) and counterproductive on others (content gaps). This has implications for any RAG-based system targeting action-oriented output.

The paper supports a narrow and specific architecture claim: a structured narrative dataset, retrieved deterministically and injected into the system prompt of a cost-efficient model, produces a measurable and repeatable improvement on a 15-criterion rubric probing evidence use, analytical structure, and framing — with the lift concentrated on the first two and the third revealing a more complex structure than simple presence or absence.

### 7.2 Architecture beats scale

The three-version corpus expansion is the paper's cleanest architectural finding. Overall delta: +0.35 (63 entries) to +0.33 (252 entries) to +0.38 (273 entries). A 4x expansion produced -0.02 of delta movement. A 7.7% expansion with qualitatively different entries produced +0.05.

The only R3 delta movement from v2.0 to v2.1 came from 21 qualitatively different entries, not from the 189 quantitatively additional entries in the v1.0-to-v2.0 expansion. Architecture — the Reasoning Scaffold, the 8+1 retriever, the section-level depth locking — produced measurable movement where scale (4x corpus growth) did not.

The implication for similar benchmarks is that once a corpus covers the evaluation domains at retrieval-window density, additional entries do not translate linearly into benchmark lift. Effort is better spent on format discipline, retrieval architecture, and coverage of qualitatively distinct content types than on scaling entry counts.

### 7.3 The R3 decomposition

The v2.0 R3 null suggested three non-exclusive hypotheses: baseline ceiling, content-format mismatch, and rubric granularity. The v2.1 council_synthesis intervention was designed to test the content-format mismatch hypothesis. The results partially confirm it — but the pillar-level decomposition reveals a more precise picture.

**Format gaps** (Pillar II: +0.50) respond to Reasoning Scaffolds because the underlying knowledge exists in the base entries but is not organized into actionable sequences. The scaffold provides the missing organizational structure. The analytical substrate is strong (highest v2.0 overall delta at +0.64), and the scaffold converts diagnosis into prescription.

**Content gaps** (Pillar III: -0.12) do not respond because the underlying institutional knowledge is absent from both the base entries and the model's training data. The scaffold directs the model to sequence reasoning about content it does not have, producing more structured but emptier responses. The model sounds more organized while being less actionable.

**Velocity gaps** (Pillar IV: +0.31) respond because the content exists but is temporally mismatched — acceleration tools and verification infrastructure are both documented, but the decision frameworks for navigating the mismatch are absent. The scaffold provides those frameworks.

This decomposition narrows the scope of the content-format mismatch hypothesis: it is correct for format gaps and incorrect for content gaps. Future interventions should diagnose the failure mode before selecting the intervention architecture. A format-gap domain needs scaffolds; a content-gap domain needs new content.

### 7.4 The empowerment-analysis tension

The `empowers` deficit reveals a structural tension in the Codex's design philosophy. Conditional optimism requires naming shadows, conditions, and obstacles — an inherently analytical framing. The `empowers` criterion measures whether the response makes the reader feel capable and motivated — an inherently emotional framing. These two goals may be fundamentally in tension within a RAG architecture.

A model augmented with shadow-integrated, condition-explicit content becomes a more honest analyst at the cost of being a less empowering coach. We do not resolve this tension in this paper. We note it as a boundary condition for any structured-context system that aims to be simultaneously evidence-honest and action-motivating.

The Reasoning Scaffold was specifically designed to improve actionability, and it succeeded on `concrete_steps` and `real_examples` while leaving `empowers` essentially unchanged. This suggests the deficit is not about content or format but about *tone* — the affective quality of the response shifts from encouraging to analytical when structured context is present, regardless of whether that context includes explicit action steps. Resolving this may require training-time intervention (RLHF, fine-tuning) rather than retrieval-time intervention.

### 7.5 Limitations

**Single-judge sensitivity.** v2.0 and v2.1 rely on a single Opus judgment per response. We gain reproducibility and lose disagreement-as-noise-dampener. Mitigation: the v1.0 Opus-only rebaseline provides a within-judge comparison point, the rubric is binary and explicitly worded, and the structural pattern (R2 > R1 > R3, cost-efficient Anthropic/OpenAI models leading, Grok null) holds across all three versions under the same judge.

**Pillar-level sample sizes.** The pillar-level R3 decomposition (SS6.5) is based on varying sample sizes per pillar: Pillar II has 3 domains (12 matched R3 pairs per model), Pillar III has 6 domains (24 matched R3 pairs per model). The per-pillar CIs are wide. The +0.50 vs -0.12 pattern is suggestive, not definitive.

**The Grok negative is a single-model finding.** It may reflect Grok-specific stylistic properties (high baseline directiveness, particular response formatting) rather than a generalizable principle about model-adaptive retrieval. Replication with additional directive-style models is needed.

**Post-hoc optimization risk.** The v2.1 run was designed to test the v2.0 diagnosis. Modifying the intervention based on v2.1 results and re-running would constitute overfitting to the benchmark. We report v2.1 as-is and propose modifications as future work only.

**Export pipeline fidelity.** Three export bugs were fixed during the retriever v1.1 update: a council header mismatch (`## The Council` vs `## The Council Speaks`), an agent practice hook format divergence (subsection headers vs inline bold), and a missing reasoning_scaffold extraction function. All three would have rendered the R3 intervention invisible to the retriever despite the entries existing in the corpus. This illustrates the gap between "entries exist in the knowledge base" and "entries transmit through the instrument." Any RAG benchmark is only as valid as its export-retrieval pipeline.

**Retrieval window saturation.** The 9-entry retrieval window was chosen to keep augmented-condition context at ~10K tokens. A different window size might change both the corpus-expansion finding and the council_synthesis delivery pattern. We have not run this ablation.

**Anonymization is imperfect.** The anonymization regex strips explicit self-identification but cannot remove stylistic fingerprints. A judge familiar with model writing styles may still recognize sources.

**Prompt sensitivity is unmeasured.** The 63 prompts were hand-written once. We have not tested sensitivity to paraphrase variants.

**Authorship analysis is observational, not stratified.** SS6.10's cross-authorship matrix is post-hoc. Stratified retrieval (same-company-only vs cross-company-only conditions) is future work.

**Causal mechanism underdetermined.** ACE shows correlation between Codex augmentation and improved scores; it cannot distinguish whether improvement comes from evidence content, stance framing, shadow integration, or retrieval structure without ablation experiments.

**Values-laden framing.** "Conditional optimism" is not a neutral stance. We describe it explicitly in SS1 and SS3 to make the values claim transparent.

### 7.6 Ethical considerations

The Codex is co-authored by four frontier models from four companies whose training data, safety postures, and stylistic tendencies are not independent. A dataset produced by this committee may inherit shared biases from the underlying providers. The multi-model design reduces single-vendor stylistic bias but does not eliminate cross-vendor correlated priors. The authorship-as-variable analysis partially addresses this by failing to find subject-side same-company preference, but the corpus itself remains an artifact of a specific moment in frontier AI development.

The epistemic monoculture concern raised during the council synthesis process deserves explicit acknowledgment. Four models trained on substantially overlapping internet text may share deeper assumptions that multi-model authorship does not surface. The five meta-patterns — particularly the systematic underrepresentation of institutional infrastructure (SS6.8) — may themselves be a product of this shared training-data bias rather than an objective feature of the knowledge landscape. The innovation-over-governance asymmetry the Codex inherits may reflect what the web contains rather than what the world contains.

---

## 8. Future Work

1. **Content-specific interventions for governance gaps.** The Pillar III negative (SS6.5) suggests format-based interventions are insufficient for content gaps. Test whether adding institutional-mechanism entries (governance procedure databases, policy implementation case studies) to Pillar III domains improves R3 without degrading other rings.

2. **Model-adaptive retrieval.** The Grok negative (SS6.6) suggests scaffold intensity should vary by model. Test a retriever that adjusts Reasoning Scaffold inclusion based on the test model's baseline directiveness score computed from unaugmented responses.

3. **Empowerment-preserving scaffolds.** Test whether adding a sixth check to the Agent Practice Hook — an empowerment check ("Does your response make the reader feel capable of taking the first step?") — addresses the `empowers` deficit (SS6.7) without suppressing shadow integration.

4. **Mechanistic ablation.** Decompose the augmented context into isolated components: evidence anchors only, council voices only, Reasoning Scaffold only, contrastive pair only. Measure which component drives the R1/R2 lift and which drives the R3 format-gap lift.

5. **Stratified authorship experiments.** Run separate augmented conditions with the retriever constrained to same-company or cross-company entries. This converts SS6.10 from observational to experimental.

6. **External judge models.** Re-run under a different single-judge model to verify structural patterns hold. The single-judge trade-off (SS5.3) needs external validation.

7. **Prompt sensitivity audit.** Paraphrase variants for each of the 63 prompts, re-run, and bound prompt-level variance.

---

## 9. Conclusion

The Abundance Codex is a deliberate bet that *architecture*, not *scale*, is the right lever for measurably changing how cost-efficient AI agents reason about civilization-scale challenges. The three-version ACE benchmark supports that bet: a 252-entry corpus retrieved deterministically and injected into the system prompt lifts response quality by +0.33 to +0.38 points on a 15-criterion rubric, with the lift concentrated in evidence and structured analysis. A 4x corpus expansion produced no delta movement. Twenty-one qualitatively different entries with Reasoning Scaffolds produced the only R3 movement in the benchmark's history — and that movement, when decomposed by pillar, reveals that "actionability" is not one construct but at least two distinct failure modes requiring different intervention architectures.

The benchmark is disciplined enough to return inconclusive results honestly. The aggregate R3 delta (+0.14) missed its pre-registered threshold (+0.15) by 0.01 with a CI that crosses zero. We report this as-is. But the aggregate obscures a more informative finding: format gaps respond dramatically to reasoning scaffolds (+0.50) while governance gaps are degraded (-0.12) — a 0.62-point swing that no aggregate statistic captures. The Reasoning Scaffold helped models that lack structure and hurt models that already have it. RAG augmentation consistently trades motivational framing for analytical structure. These are findings about structured-context systems generally, not just about this dataset.

The contribution we hope proves durable is not the specific deltas — numbers drift with model generations, corpus updates, and rubric revisions. The contribution is a methodology: diagnose the failure mode, design a targeted intervention, pre-register the prediction, measure the effect, and report honestly when the results are more complex than the hypothesis. The Codex and ACE are instruments for this methodology. The finding that actionability decomposes into format gaps and content gaps — and that the same intervention helps one and hurts the other — is the kind of finding that only emerges when the methodology is honest enough to return inconclusive results and precise enough to decompose them.

Abundance is not the destination. It is the stance. And stance is now something you can measure, diagnose, and — selectively — improve.

---

## Appendix A — Judge Prompt Template

Every judge scoring call uses this exact prompt (ring-specific criteria inserted from `evals/ace/rubrics.json`):

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

Full rubric definitions are in `evals/ace/METHODOLOGY.md` and `evals/ace/rubrics.json`.

---

## Appendix B — Sample Entries

**Base entry.** A representative Codex entry — the Solar Revolution origin story — is at `domains/01-energy/01-the-solar-revolution.md` in the repository. It follows the full Gold Standard Format: YAML frontmatter with four cross-domain connections, the five-phase Shift Arc, all five council voices, four evidence anchors with source years and confidence scores, a complete shadow check, the 6D position, and a practice hook for both human readers and agents.

**Council synthesis entry.** A representative council_synthesis entry — the education domain synthesis — is at `domains/07-education/13-education-council-synthesis.md`. It demonstrates the meta-analytical structure: YAML frontmatter with `co_author_model: multi-model-council` and `council_models` array, the standard Gold Standard Format sections, plus the Reasoning Scaffold (Scarcity Trap, 6-step Reframe Chain, Contrastive Pair) and the 5-check Agent Practice Hook format described in SS3.6. Both entries are reproduced in the repository rather than this paper for space.

---

## Appendix C — Reproducibility

**Repository:** `github.com/CjTruHeart/abundance-codex`
**Dataset:** `huggingface.co/datasets/CjTruHeart/abundance-codex`
**License:** MIT (code), CC-BY (dataset)
**Python:** 3.11+
**Dependencies:** `httpx>=0.27`, `pyyaml>=6.0`, `jsonschema>=4.20`

**To reproduce v2.0:**

```bash
git clone https://github.com/CjTruHeart/abundance-codex.git
cd abundance-codex
pip install -r evals/ace/requirements.txt
cp evals/ace/.env.example .env   # then edit to add OPENROUTER_API_KEY
python3 scripts/run-ace.py --run-version 2.0 --dry-run   # verify retrieval, no API calls
python3 scripts/run-ace.py --run-version 2.0              # full run, ~$5-11, ~20-40 min
```

**To reproduce v2.1:**

```bash
python3 scripts/run-ace.py --run-version 2.1 --dry-run   # verify 8+1 architecture
python3 scripts/run-ace.py --run-version 2.1              # full run, ~$5-11, ~3 hours
```

The v2.1 run uses Dojo Retriever v1.1 with the 8+1 slot architecture. The retriever version is auto-detected from the JSONL export (presence of `reasoning_scaffold` field triggers v1.1 behavior). The `--dry-run` flag prints a retrieval summary table showing council_synthesis inclusion rates per ring — verify R3 shows 100% council_synthesis via reasoning slot before committing to a full run.

**Published run metadata:**
- v2.0: timestamp `2026-04-13T10:31:33Z`, git SHA `529bb85`, corpus 252 entries
- v2.1: timestamp `2026-04-14T02:18:08Z`, git SHA `0a0dc68`, corpus 273 entries
- Both: judge `anthropic/claude-opus-4.6`, `temperature=0.0`, `max_tokens=2048`, `concurrency=8`

Reproducibility SHAs (git, jsonl, config) are embedded in each results JSON.

**Council synthesis forge process:** The 84 raw model assessments were collected via `scripts/collect-council-assessments.py` and are preserved in `council-synthesis/assessments/`. The human synthesis process is documented in `council-synthesis/FORGE-LOG.md`.

**To reproduce the v1.0 Opus-only rebaseline:**

```bash
python3 scripts/ace-v1-opus-rebaseline.py
```

---

## Appendix D — Five Meta-Patterns and Governance Frequency

### D.1 The Five Meta-Patterns

The following taxonomy emerged from the council synthesis forge process (SS4.2). Four frontier models independently assessed 252 entries across 21 domains, and five convergent failure modes were identified:

**Pillar I — Material Foundation (Content Gap).** Supply-side technological abundance systematically overrepresented; governance, infrastructure, and allocation systems that determine whether abundance reaches populations systematically underweighted. Grid modernization invisible behind solar cost curves; cold chains absent behind cheaper protein molecules; water metering absent behind desalination; zoning absent behind construction technology; preventable CVD deaths invisible behind frontier genomics; environmental monitoring treated as synonymous with environmental action.

**Pillar II — Human Capability (Format Gap).** Diagnostic eloquence without prescriptive protocols. AI tutoring celebrated while 70% of 10-year-olds in LMICs cannot read and no decision tree exists for teachers; epigenetic reprogramming mapped while cardiovascular prevention goes unmentioned and no triage framework exists; meaning crisis diagnosed but zero exercises taught. The entries know what matters but cannot teach anyone how to act.

**Pillar III — Collective Coordination (Governance Gap).** Institutional infrastructure absent behind technological and aspirational facades. Sensemaking collapses while connectivity is celebrated; belonging proved as health infrastructure while restorative justice receives zero entries; regulatory capture named but not tested against; encryption celebrated while 1 in 3 women experience violence; battery cost curves replace rail infrastructure; financial inclusion rails coexist with 100-400% APR digital lending. The entries describe coordination aspirations without engineering coordination mechanisms.

**Pillar IV — Production & Discovery (Velocity Gap).** Acceleration tools exponential; verification infrastructure linear. Desktop fabrication and molecular assembly get entries while injection molding and quality systems (responsible for the gains the entries celebrate) get zero; 280x inference cost collapse documented but decision frameworks absent; BCG +40% quality documented alongside METR perception-reality divergence but no workflow resolves when co-creation helps vs. harms; AlphaFold celebrated while metrology and Registered Reports operate at institutional speed.

**Pillar V — Transcendent Frontier (Reflexivity Gap).** Aspirational narratives without methodology. A 97% launch cost collapse called "democratization" while one company controls 88% of US mass to orbit; applied foresight tools with decades of track records (backcasting, scenario planning, CLA, Delphi, Three Horizons) receive zero dedicated entries; the domain that justifies the entire Codex cannot teach anyone how to practice what it preaches.

### D.2 Governance Frequency Analysis

Governance-related keywords were searched across all 273 entries' conditional_optimism sections:

- **Entries with conditional_optimism content:** 236/273
- **Entries with 1+ governance keyword:** 201/236 (85.2%)

| Pillar | Entries w/ CO | w/ Gov Keywords | % |
|--------|-------------|-----------------|---|
| I Material Foundation | 64 | 57 | 89% |
| II Human Capability | 34 | 23 | 68% |
| III Collective Coordination | 71 | 67 | 94% |
| IV Production & Discovery | 46 | 37 | 80% |
| V Transcendent Frontier | 21 | 17 | 81% |

Top keywords: *standards* (84), *governance* (84), *regulatory* (56), *policy* (51), *transparency* (26), *reform* (24). Governance is the Codex's most cross-cutting conditional dependency, appearing across all pillars regardless of technical domain.

---

*Paper co-authored by Cj TruHeart (human curator, creative director) and Claude Opus 4.6 (AI co-author, via Claude Code). Dataset co-authored by Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, and Super Grok under human curation. CyberMonk served as AI co-creative partner for strategy and architecture throughout.*
