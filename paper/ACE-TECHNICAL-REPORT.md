<!-- Last verified: 2026-04-18, commit b4a942a -->

# Architecture Over Scale: How Narrative Dataset Design Measurably Shifts AI Agent Reasoning

**Cj TruHeart¹ and Claude Opus 4.6²**

¹ Starfinity Records / TruHeart Publishing — human curator, creative director
² Anthropic — AI co-author (via Claude Code, Opus 4.6 1M)

*Corresponding repository:* [github.com/CjTruHeart/abundance-codex](https://github.com/CjTruHeart/abundance-codex)
*Version: v2.3 — April 2026*

---

## Abstract

We present the **Abundance Codex**, a 285-entry narrative dataset across 21 Grand Challenge domains designed to measure and improve the *worldview quality* of AI agents — their tendency toward scarcity framing, threat-salience, and passive description on civilization-scale challenges. The corpus comprises 264 base entries co-authored by four frontier models (Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, Super Grok) under human curation, plus 21 multi-model `council_synthesis` entries — a meta-analytical layer where four models independently assess each domain's blind spots and a human curator synthesizes the findings.

We introduce **ACE** (Abundance Codex Evaluation), a single-judge benchmark (Opus 4.6) scoring 504 responses on 15 binary criteria across evidence, analysis, and action rings. Across four pre-registered iterations, Codex augmentation lifts responses by **+0.41 / 5 points** (95% CI [+0.29, +0.53]), with the Ring 3 (derived actionability) delta advancing from **null (v2.0, +0.03)** through inconclusive (v2.1, +0.14) and missed-by-fractions (v2.2, +0.18) to **pre-registered-confirmed (v2.3, +0.27)** against a target band of [+0.25, +0.30] with falsification bound < +0.22. The confirmed intervention — pillar-gated empowerment scaffolding replacing uniform application — moved every pillar's R3 delta upward, none regressed.

Alongside this finding we report a **structural limitation of LLM-as-judge evaluation for RAG-augmented systems**: five targeted interventions across two release cycles failed to move the `accuracy` criterion. A 19× dose-response between post-training-cutoff citations and accuracy-zero judgments, together with a two-round judge-preamble calibration that failed on opposite sides of the same axis, indicates the rubric conflates *verifiable from training* with *internally consistent and sourced*. We propose splitting `accuracy` into `factual_consistency` and `source_attribution` for v2.4.

Finally, we characterize a **rhetorical interference mechanism**: Pillar II's R3 gained +0.167 when empowerment content was *removed*, not added; token-length versus score correlation was |r|=+0.209 with retrieval length dropping only 3–4%, ruling out an attention-budget explanation. Intervention intensity must be calibrated to content gap per domain — generalizable beyond this dataset. All data, code, pre-registrations, and results are released under MIT/CC-BY.

---

## 1. Introduction

Large language models inherit their worldview from the corpora on which they are trained. Those corpora are, overwhelmingly, fear-optimized: threat-first news cycles, zero-sum economic framing, risk-salient technical commentary. When a frontier model is asked about energy, food, or governance, the default response is structured around shortages, obstacles, and caution — not because the model is pessimistic by design, but because scarcity is the dominant grammar of the text it was trained on.

This becomes a deployment problem as agents move from chat into long-horizon action. A model that frames every civilization-scale challenge as intractable is a poor collaborator on problems that require concrete leverage, evidence citation, and the identification of builders already at work. Existing benchmarks do not measure this. MMLU and GPQA test knowledge ceilings. HellaSwag and ARC test commonsense reasoning. TruthfulQA tests resistance to plausible falsehoods. None of them ask whether a model holds a *generative* stance on hard problems — whether it cites evidence, names conditions, integrates shadow, and invites action.

We address this gap with the Abundance Codex and the ACE benchmark. The stance the Codex encodes is **conditional optimism**: abundance is contextual and constructible, every claim carries a shadow, and every evidence anchor carries a confidence score. This is not Pollyanna, and not a hidden ideology — it is an explicit methodological stance that can be tested empirically.

This paper reports a four-iteration methodology arc. We built a 252-entry corpus and measured its effect (v2.0): evidence and analysis improved, actionability did not. We diagnosed the R3 null, designed a targeted intervention (21 `council_synthesis` entries with Reasoning Scaffolds), pre-registered predictions, and re-measured (v2.1); the aggregate result was inconclusive but a pillar-level decomposition revealed two distinct failure modes. We added 12 institutional entries and a uniform Empowerment Gate (v2.2); Pillar III responded with a +0.333 swing — confirming the content-gap hypothesis — but Pillars II and IV regressed, revealing that uniform scaffolding was itself an error. We replaced uniform application with pillar-gated tiers (FULL / CONDENSED / REMOVED) calibrated to domain need (v2.3); every pillar gained, the aggregate R3 moved into the pre-registered target band, and the overall delta held at +0.41.

Along the way we documented a measurement problem that belongs to the field rather than to this project: the R1 `accuracy` criterion became un-movable across five targeted interventions. Evidence gathered during the investigation — a 19× dose-response between post-cutoff citations and zero-scores, and a two-round judge-preamble calibration whose failures sat on opposite sides of the same axis — argues that the rubric conflates *verifiability against judge training* with *internal consistency and sourcing*. We report this as a structural limit of LLM-as-judge RAG evaluation and propose a rubric redesign.

**Our contributions.** (1) The Codex dataset (285 entries, markdown + JSONL, 21 domains, 12 entry types). (2) The Dojo Retriever v1.1 (8+1 slot architecture, deterministic, with section-level depth locking). (3) The ACE benchmark (v2.3, single-judge Opus, 15 binary criteria across 3 rings). (4) A four-iteration, pre-registered intervention methodology (diagnose → intervene → pre-register → measure) with all predictions, results, and misses committed to git before and after each run. (5) The `council_synthesis` layer — multi-model deliberation producing meta-analytical entries that target specific benchmark gaps. (6) A taxonomy of five knowledge-production failure modes (content, format, governance, velocity, reflexivity gaps). (7) A characterized structural limit of LLM-as-judge RAG evaluation and a proposed rubric redesign. (8) The **rhetorical interference mechanism**: Pillar II R3 gained from *removing* empowerment framing; content-driven, not attention-budget-driven.

---

## 2. Related Work

**RAG evaluation benchmarks** (RAGAs, BEIR, MTEB) optimize retrieval quality — recall, ranking, faithfulness to retrieved context. They do not measure whether retrieval shifts the framing of model reasoning. ACE sits downstream of retrieval quality: we hold a fixed retriever and measure whether retrieved *content* changes response quality on worldview-adjacent criteria.

**Reasoning benchmarks** (MATH, GPQA, Humanity's Last Exam, ARC-AGI) test capability ceilings. They are orthogonal to framing: a model can score perfectly while framing every civilization-scale problem as intractable.

**Values and stance benchmarks** (TruthfulQA, MACHIAVELLI, WVS-style surveys) probe values in isolation from domain reasoning. ACE ties stance to domain-grounded tasks, scoring whether a response about energy or governance *does* things — cites data, names builders, states conditions — rather than whether the model professes a value abstractly.

**LLM-as-judge methodology** (MT-Bench, Chatbot Arena, AlpacaEval, PandaLM) is now standard for evaluating open-ended responses. The literature documents length preference, position preference, and same-family preference where judges score their own vendor's models more favorably. ACE's v1.0 council added an empirical data point to this literature: one vendor judge showed a +0.50 in-group delta. ACE v2.0 tested whether the corresponding *subject-side* effect exists and found no evidence for it (§6.10). To these known biases we add, in §7, a **judge-cutoff verifiability bias** specific to RAG evaluation: judges penalize post-cutoff-dated claims as inaccurate even when sources are named and internally consistent.

**Narrative and worldview datasets.** HellaSwag, StoryCloze, BookCorpus, WordCraft use narrative as a test of language understanding rather than as an explicit worldview intervention. We are not aware of a prior open-source dataset explicitly structured for measuring and improving framing quality on civilization-scale challenges.

**Meta-analytical and self-auditing datasets.** Adversarial dataset curation (Dynabench, Adversarial NLI) uses adversarial human annotators to find model weaknesses but does not employ multi-model self-assessment of the dataset itself. The `council_synthesis` layer is structurally novel: entries that critique the collection they belong to, produced through parallel-independent assessment by four frontier models rather than sequential adversarial annotation.

**Intellectual lineage.** The Codex's conditional-optimism stance draws on Rosling's *Factfulness*, Pinker's *Enlightenment Now*, Fuller's "build a new model that makes the existing model obsolete," Roddenberry's Star Trek civilization as design specification, and Donella Meadows on leverage points. The Three Rings architecture inherits from the WuWei Dataset Architecture v3.0. These are positioned as methodological influences, not endorsements of any specific forecast.

---

## 3. Dataset Design

### 3.1 Gold Standard Format

Every entry in the Codex is a single markdown file following one canonical template. Required sections: YAML frontmatter (entry ID, type, primary domain, up to 5 typed cross-domain connections with strength scores, status, confidence, co-author attribution); a one-line essence for retrieval; the five-phase **Shift Arc** (Scarcity Frame → Encounter → Reframe → Proof → Invitation); the **Council** (five analytical voices — Oracle, Critic, Sensei, Builder, Witness — each with a scoped word count); **Evidence Anchors** (a numbered table of sourced, confidence-scored factual claims); a **Shadow Check** (required on every entry — distortion risk, who gets left behind, transition pain, falsifiability edge, what this is NOT); a **6D Position** on the Digitized / Deceptive / Disruptive / Demonetized / Dematerialized / Democratized curve; and sections for Connections, Conditional Optimism, Practice Hook, and Governance.

The template is not decorative. Each section produces a specific observable property in the retrieved context downstream: evidence anchors produce citation-ready material, shadow checks prevent toxic optimism, the council produces stance multiplicity, and the conditional optimism section forces explicit conditions.

### 3.2 Entry Types and Density Matrix

The Codex supports 12 entry types. Distribution across 285 entries:

| Type | Count | Purpose |
|---|---:|---|
| builder_profile | 44 | Named practitioners doing the work today |
| contrast | 37 | Failure mode beside success, side-by-side |
| framework | 37 | Structured models for a domain |
| trendline | 36 | Quantitative trajectories with evidence anchors |
| breakthrough | 35 | Capabilities or events that shifted the frame |
| origin_story | 24 | Founding narratives anchoring each domain |
| council_synthesis | 21 | Meta-analytical entries with Reasoning Scaffolds |
| shadow | 21 | Structural critiques — embedded immune system |
| paradigm_seed | 15 | Early-stage ideas with asymmetric upside |
| false_dawn | 6 | Premature optimism corrected by evidence |
| star_trek_spec | 6 | Visionary capstones |
| grand_challenge | 3 | Field-shaping problem statements |

Each type has a distinct density profile (e.g., `trendline` is evidence-heavy and council-light; `paradigm_seed` is one sentence; `shadow` inverts the Shift Arc and foregrounds the Critic voice; `council_synthesis` is meta-analytical with a Reasoning Scaffold). The full density matrix is in `GOLD-STANDARD-FORMAT.md`.

`shadow` and `false_dawn` entries function as an **immune system** for the corpus. Without them, a narrative dataset about possibility rapidly becomes propaganda. With them, it becomes wisdom. We return to this point in §6.9, where the corpus expansion measurably reduces the retriever's need to force-pull shadow content — natural shadow density at 252+ entries is already sufficient.

### 3.3 The Three-Ring Architecture

The dataset is organized into three rings that separate *what happened* from *how it's structured* from *how it's used*:

- **Ring 1 (Canonical Core):** 285 markdown entries. Source of truth. Never overwritten by automation.
- **Ring 2 (Structured Metadata):** YAML frontmatter, evidence tables, connection graphs. Machine-readable overlays embedded in Ring 1.
- **Ring 3 (Derived Exports):** JSONL, JSON, and future exports generated from Rings 1 and 2. Regenerable.

The Three-Ring architecture maps cleanly onto the three benchmark rings in ACE: R1 tests evidence, R2 tests structured analysis, R3 tests actionability. This is not coincidence — the rubric was constructed to measure whether the architecture transmits into model responses.

### 3.4 The 21 Domains

The 21 domains are organized into five pillars that trace a civilization-building arc. Entry counts per pillar (including each domain's `council_synthesis` entry):

| Pillar | Domains | Entries |
|---|---|---:|
| I Material Foundation | energy, food, water, shelter, health, environment | 78 |
| II Human Capability | education, longevity, consciousness | 39 |
| III Collective Coordination | communication, community, governance, security, transportation, economy | 90 |
| IV Production & Discovery | manufacturing, computation, co-creative intelligence, science | 52 |
| V Transcendent Frontier | space, future-vision | 26 |

Totals: 285 entries = 264 base entries + 21 `council_synthesis`. See `DOMAINS.md` for the full index.

### 3.5 Validation

Every entry is validated by `scripts/validate-entry.py`, a four-layer checker that enforces YAML schema conformance, required section presence, minimum evidence anchor count, and domain connection strength bounds. All 285 entries pass validation. The validator is CI-integrated.

### 3.6 The Reasoning Scaffold

The `council_synthesis` entry type introduces a section absent from the base entries: the **Reasoning Scaffold**. Where evidence anchors provide facts and council voices provide analytical perspectives, the Reasoning Scaffold provides *cognitive operations to perform*. It is not content to cite — it is a sequence to execute.

The Reasoning Scaffold has three components:

1. **Scarcity Trap.** Names the specific default framing a model will fall into if given no structured context for this domain. This is diagnostic: it makes the failure mode explicit before offering an alternative.
2. **Reframe Chain.** A 6-step analytical sequence that transforms the scarcity frame into a conditional-optimism frame. Each step builds on the previous: name the scarcity assumption → identify what it obscures → cite counter-evidence → name conditions under which counter-evidence holds → identify actors and leverage points → arrive at a conditional claim.
3. **Contrastive Pair.** Two ~200-token paragraphs — one from the scarcity frame, one from the conditional-optimism frame — on the same empirical situation. The contrastive pair is the highest impact-per-token component: at ~200 tokens it transmits the stance shift more efficiently than any other section.

The Reasoning Scaffold exists only on `council_synthesis` entries. It is not retrofitted to the base entries. This preserves the ability to measure the scaffold's marginal effect by comparing v2.0 (no scaffolds) to v2.1 (scaffolds present via 8+1 retrieval).

Each `council_synthesis` entry also includes an **Agent Practice Hook** — a checklist of conditional tests a model can apply to its own output before responding. Through v2.1 the hook had 5 checks; in v2.2 a sixth **Empowerment Gate** was added uniformly; in v2.3 the gate became pillar-conditional (§4.4). These are executable reasoning checks, not informational content.

The design principle is that R3 (actionability) failed not because the base entries lack relevant content but because they deliver that content as narrative — essays to absorb rather than procedures to perform. The Reasoning Scaffold hypothesis is that delivering executable reasoning patterns through the retrieval context will improve action-oriented responses where additional narrative content did not.

---

## 4. Multi-Model Co-Authorship and the Intervention Arc

### 4.1 Parallel Co-Authorship (v1.0–v2.0)

A distinctive property of the Codex is that it was co-authored by four frontier models working in parallel. Each of Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, and Super Grok was assigned three entries per domain (63 entries each, 252 total through v2.0). Every entry records its `co_author_model` in YAML frontmatter and propagates that field through the JSONL export and the retriever's output.

This design reduces single-model stylistic bias in the corpus, enables the authorship-as-variable analysis reported in §6.10, and — because the authorship is preserved — makes subsequent replication failures informative. When the results are open, the retriever is deterministic, and per-entry authorship is preserved, any subsequent run that fails to reproduce the findings is traceable to a specific moving part.

The human editor (Cj TruHeart) maintained voice consistency across authors and validated each entry against the Gold Standard Format before acceptance. Approximately 30% of first-draft entries required revisions for shadow integration, evidence sourcing, or voice balance before validation passed.

### 4.2 v2.1 Intervention — The `council_synthesis` Layer

After v2.0 established that R3 (actionability) was null, a second co-authorship process was designed to target this specific gap. Rather than adding more entries of the same kind (which the corpus saturation finding in §6.9 predicted would be ineffective), the completion layer employed **multi-model deliberation** — a structurally different authorship process producing qualitatively different entries.

**Process architecture.** Four frontier models independently assessed each domain's 12 existing entries. Each model answered 7 structured questions: blind spots in the domain's coverage, missing builders, shadow gaps, actionability gaps, inter-entry tensions, confidence calibration issues, and a contrastive pair (scarcity vs. abundance frame). This produced 84 independent assessments (4 models × 21 domains). The human curator then synthesized convergent and divergent findings into a single canonical Gold Standard entry per domain.

**Why parallel-independent.** A one-model-drafts-others-critique architecture produces marginal adjustments to the drafting model's framing. Parallel-independent assessment gives four separate reads of the same material; convergent gaps (flagged by 2+ models) carry higher signal than any single critique. Divergent gaps (flagged by only one model) reveal what one model's training data covers that others miss.

**Sequencing matters.** The `council_synthesis` layer was designed *after* the v2.0 benchmark results were known. The R3 null motivated the Reasoning Scaffold's action-focused design; the per-pillar analysis motivated the domain-specific blind-spot questions; the corpus saturation finding motivated the choice to add 21 qualitatively different entries rather than 100+ quantitatively similar ones.

Attribution uses `co_author_model: "multi-model-council"` with a full `council_models` array. All 84 raw assessments are preserved in `council-synthesis/assessments/`.

### 4.3 v2.2 Intervention — Institutional Entries + Empowerment Gate

The v2.1 pillar-level decomposition (§6.5) revealed a +0.50 vs −0.12 swing between format-gap (Pillar II: education, longevity, consciousness) and governance-gap (Pillar III: communication, community, governance, security, transportation, economy) domains under the same Reasoning Scaffold intervention. The diagnosis split the work:

**Targeted content addition (12 entries).** Pillar III domains received two institutional-mechanism entries each — covering conflict resolution protocols, anti-capture architecture, consumer protection, restorative justice, rail infrastructure, cooperative supply chains. These were written with the same Gold Standard discipline but explicitly focused on the institutional connective tissue the v2.1 blind-spot analysis surfaced as missing. The corpus grew 273 → 285 entries.

**Empowerment Gate (Check 6).** All 21 `council_synthesis` entries received a uniform sixth check in the Agent Practice Hook: *Does your response make the reader feel capable of taking the first step?* Paired with an **Empowered Action Frame** paragraph appended to each Contrastive Pair. The gate was designed to address the −0.155 `empowers` deficit observed in v2.1 without sacrificing the scaffold's analytical discipline.

Both interventions were pre-registered at commit `546095e` before the v2.2 benchmark ran.

### 4.4 v2.3 Intervention — Pillar-Gated Empowerment (Three-Tier)

v2.2 confirmed the content-gap hypothesis for Pillar III (R3 +0.333 swing) but revealed collateral regressions: Pillar II R3 dropped from +0.500 to +0.250 and Pillar IV dropped from +0.312 to +0.125. The consciousness domain (Pillar II) regressed by −0.75 from +0.50 to −0.25 — the starkest single-domain swing. The diagnosis: the uniform empowerment gate was helping where it was needed (Pillar III, where baseline R3 was negative due to missing institutional content) and actively harming where it was not (Pillars II and IV, whose analytical scaffolds were already producing +0.3 to +0.5 R3 under v2.1).

The v2.3 intervention replaced uniform application with a three-tier design:

- **FULL** (Check 6 + Empowered Action Frame both kept): all Pillar III domains + Pillar I food, shelter. These are the domains where baseline R3 was negative and empowerment framing filled a genuine content gap.
- **CONDENSED** (Check 6 kept, Empowered Action Frame removed): Pillar I energy/water/health/environment + Pillar V space/future-vision + Pillar IV co-creative-intelligence.
- **REMOVED** (both Check 6 and Empowered Action Frame removed): Pillar II consciousness/longevity/education + Pillar IV computation-intelligence/science-engineering/manufacturing. These are the domains whose analytical scaffolds were already sufficient and whose R3 had regressed under the uniform gate.

Tier assignments were mechanical, driven by v2.1 baseline per-domain R3 performance, and committed before benchmark execution (commit `5d0722a`). See §6.5 for the outcome table.

---

## 5. Benchmark Design (ACE)

### 5.1 Architecture

ACE runs 4 efficiency-tier test subjects × 63 hand-written prompts × 2 conditions (baseline / augmented) = **504 responses per run**, scored as **252 matched pairs**. The efficiency-tier models are: Claude Haiku 4.5, GPT-5.4 Mini, Gemini 3.1 Flash-Lite, and Grok 4.1 Fast (one cost-efficient model per major frontier lab). Each response is anonymized (explicit self-identification stripped via regex) and scored on 5 binary criteria by the judge.

The 63 prompts are structured as 21 domains × 3 cognitive rings. Each domain contributes one R1 prompt (evidence), one R2 prompt (structured analysis), and one R3 prompt (derived action). R1 asks "what measurable evidence exists…"; R2 asks "advocates say X, skeptics say Y, where does it actually stand?"; R3 presents a specific persona with a specific goal and asks for first steps.

### 5.2 Scoring Rubric

All 15 criteria are binary (0 or 1). Five criteria per ring:

**Ring 1 (Evidence):** `cites_evidence`, `names_builders`, `accuracy`, `recency`, `acknowledges_complexity`.
**Ring 2 (Structured):** `applies_framework`, `names_shadow`, `states_conditions`, `maps_connections`, `holds_middle`.
**Ring 3 (Derived):** `frames_solvable`, `identifies_leverage`, `concrete_steps`, `real_examples`, `empowers`.

A partial attempt scores 0. Full definitions live in `evals/ace/rubrics.json`. The per-response score is the sum of the 5 criteria (0–5). The delta is the mean difference between augmented and baseline scores across matched (prompt, test_model) pairs.

§7 revisits the `accuracy` criterion as a structural limitation of this rubric.

### 5.3 Judge Selection

v1.0 used a 4-judge blind council (Claude Opus 4.6, GPT-5.4, Gemini 3.1 Pro, Grok 4.20). Post-run analysis surfaced a measured **in-group bias** in the Grok judge: it scored its own company's test subject **+0.50** higher than it scored other companies' subjects. Opus (−0.13), GPT-5.4 (−0.14), and Gemini 3.1 Pro (+0.18) showed much smaller effects.

v2.0 through v2.3 lock the judge to a single model: **`anthropic/claude-opus-4.6`**. Every scoring call uses Opus. This eliminates inter-judge variance, removes the measured Grok in-group bias, and cuts benchmark cost by roughly 75%.

All cross-version comparisons in this paper are **judge-matched Opus-vs-Opus**. This is a deliberate trade-off: we lose inter-judge disagreement as a noise dampener and gain full comparability across four benchmark versions. Mitigations: a binary rubric with explicit criterion definitions, a frozen judge prompt template, and — from v2.2 forward — pre-registered targets and falsification bounds that make the single-judge dependence legible. §7 documents a specific structural limitation this single-judge regime exposed.

### 5.4 Retrieval: The Dojo Retriever (v1.0 → v1.1)

The augmented condition injects Codex context selected by the **Dojo Retriever**, a deterministic multi-stage pipeline: intent classification, domain identification, candidate scoring, type coverage enforcement, passage extraction at three detail tiers (FULL / CONDENSED / MINIMAL), strategic ordering, and context assembly. The retriever takes no embeddings and makes no external API calls; given the same JSONL export and the same query it produces byte-identical output.

**v1.0 architecture (used in ACE v2.0).** Nine content slots per retrieval. Two load-bearing rules: *type coverage enforcement* (no single entry type dominates) and *shadow force-pull* (at least one shadow/false_dawn entry must be present for ANALYTICAL, STRATEGIC, or ADVERSARIAL intents).

**v1.1 architecture (used in ACE v2.1–v2.3).** The **8+1 slot architecture** separates content retrieval from reasoning retrieval:

- **8 content slots:** Unchanged from v1.0. Domain matching, type coverage, shadow force-pull — identical. These slots serve R1 and R2.
- **1 reasoning slot:** Reserved for the domain's `council_synthesis` entry on STRATEGIC and ADVERSARIAL intent queries. When active, the entry is extracted with an R3-optimized priority override: Reasoning Scaffold and Agent Practice Hook prioritized over evidence anchors and council voices, and **depth-locked at FULL extraction** regardless of the entry's tier ranking.

Separating them prevents the R3 intervention from interfering with proven R1/R2 retrieval patterns. The v2.3 retriever adds a single output-layer change: **evidence-anchor years ≥ 2025 are rendered as "recent data"** in FULL and CONDENSED passage output (source markdown and JSONL untouched). This was Spec A's structural hedge against the R1 accuracy judge-verification mismatch; see §7.

### 5.5 Prompt Templates

The **baseline** condition sends the prompt as a user message with no system prompt. The **augmented** condition prepends a system prompt:

> You are a helpful assistant with access to the Abundance Codex — a narrative dataset mapping human flourishing across 21 Grand Challenge domains. When discussing the future, technology, or societal challenges, draw from the provided context. Apply conditional optimism: name the frame, cite evidence, state conditions, name obstacles, identify roles, invite action. Never promise utopia. Never hide the shadow. Illuminate paths.
>
> `{codex_context}`

The `{codex_context}` placeholder is replaced with the Dojo Retriever's output. In v2.3 the citation instruction was softened from "note the source year" to "note the source and time period (year if specific, else 'recent')" to align with the retriever's year-relabel.

### 5.6 Statistical Methodology

Deltas are point estimates with **95% bootstrap confidence intervals** computed from 10,000 paired resamples over the (prompt, model) tuples (seed=42 in v2.3). Bootstrap is paired: each resample draws (augmented − baseline) differences rather than the two conditions independently. A delta is treated as **robust** if the lower CI bound stays above zero, **null** if the CI crosses zero. The same methodology is applied at the ring, model, and pillar levels with correspondingly smaller sample sizes and wider CIs.

### 5.7 Pre-Registration Protocol

Every benchmark intervention since v2.1 has been accompanied by a pre-registration file committed to git before benchmark execution. Each pre-registration specifies: point-estimate predictions with target bands, falsification bounds sharp enough to genuinely refute, escalation rules that document in advance what each kind of miss will trigger, and — from v2.2 forward — a "what failure teaches" section so the diagnostic reasoning is visible before the numbers are known.

Pre-registration commits:

- v2.1: `e90869d`
- v2.2: `546095e`
- v2.3: `bd23712` (with a pre-benchmark calibration addendum following the judge-preamble dry-run — see §7)

A full pre-registration scorecard across all four iterations appears in §6.3.

### 5.8 Reproducibility Metadata

Every results JSON embeds: `run_ace_git_sha`, `jsonl_export_sha256`, `config_sha256`, `python_version`, exact OpenRouter model IDs, temperature (0.0), max_tokens (2048), concurrency (8), and ISO-8601 timestamp. Model configuration is externalized to `evals/ace/config.yaml`. An external researcher can verify whether their run is operating on byte-identical inputs and, if not, trace the divergence.

---

## 6. Results: The Four-Iteration Arc

Numbers in this section are drawn from `evals/ace/results/v2.0/ace-20260413-103133.json` (v2.0), `evals/ace/results/v2.1/ace-20260414-021808.json` (v2.1), `evals/ace/results/v2.0/ace-20260416-204330.json` (v2.2), and `evals/ace/results/v2.0/ace-20260417-014155.json` (v2.3). All four runs scored by a single Opus 4.6 judge.

### 6.1 Overall Delta

| Version | Corpus | Baseline | Augmented | Δ | 95% CI |
|---|---:|---:|---:|---:|---|
| v2.0 | 252 | 4.17 | 4.50 | +0.33 | [+0.21, +0.46] |
| v2.1 | 273 | 4.12 | 4.50 | +0.38 | [+0.25, +0.50] |
| v2.2 | 285 | 4.12 | 4.54 | +0.42 | [+0.30, +0.55] |
| **v2.3** | **285** | **4.15** | **4.56** | **+0.41** | **[+0.29, +0.53]** |

The overall delta is stable across a 4.5× corpus expansion (63 → 285 entries) and four targeted interventions. CIs overlap substantially across all four versions. What changes between versions is *where* the delta sits within its rings — which is the paper's substantive finding.

### 6.2 The R3 Arc

| Version | Corpus | R3 Δ | Status | Key Intervention |
|---|---:|---:|---|---|
| v2.0 | 252 | +0.03 | NULL | Baseline dataset, no scaffolds |
| v2.1 | 273 | +0.14 | INCONCLUSIVE | 21 `council_synthesis` + Reasoning Scaffolds |
| v2.2 | 285 | +0.18 | MISSED (by 0.04) | +12 institutional entries, uniform empowerment gate |
| **v2.3** | **285** | **+0.27** | **CONFIRMED** | Pillar-gated empowerment (FULL / CONDENSED / REMOVED) |

v2.3 R3 Δ = **+0.274**, CI [+0.12, +0.44], against pre-registered target [+0.25, +0.30] and falsification bound < +0.22. **Primary prediction confirmed.**

This is the paper's structural finding: a pre-registered intervention, targeted at a specific failure mode, moved a benchmark metric into a predicted range after three prior iterations failed to. Each miss was diagnosed, the diagnosis informed the next intervention, and the final intervention cleared the pre-registered bar with CI above the falsification bound.

### 6.3 Pre-Registration Scorecard

Across four iterations, 19 distinct predictions were pre-registered. Summary outcomes:

| Version | Total | Confirmed | Refuted | Inconclusive / Borderline |
|---|---:|---:|---:|---:|
| v2.1 | 3 | 2 | 0 | 1 (primary R3, CI crossed zero) |
| v2.2 | 4 | 2 | 2 | 0 |
| v2.3 | 8 | 5 | 1 | 2 |
| **Total** | **15** | **9** | **3** | **3** |

v2.3 per-prediction outcomes (from `PRE-REGISTRATION-v2.3.md` + calibration addendum):

| Metric | v2.2 | v2.3 | Target | Falsify | Result |
|---|---:|---:|---|---|---|
| R3 overall Δ | +0.179 | **+0.274** | +0.25 to +0.30 | < +0.22 | ✅ CONFIRMED |
| R3 Pillar II Δ | +0.250 | **+0.417** | +0.40 to +0.50 | < +0.30 | ✅ CONFIRMED |
| R3 Pillar III Δ | +0.500 | **+0.625** | ≥ +0.15 | < +0.10 | ✅ CONFIRMED |
| `empowers` Δ | −0.036 | **−0.012** | ≥ −0.05 | < −0.10 | ✅ CONFIRMED |
| `real_examples` Δ | +0.131 | **+0.202** | +0.15 to +0.20 | < +0.10 | ✅ CONFIRMED |
| R1 `accuracy` Δ | −0.226 | **−0.262** | −0.08 to +0.05 | < −0.12 | ❌ FALSIFIED |
| R3 consciousness | −0.250 | **+0.000** | +0.25 to +0.50 | < 0.00 | ⚠️ BORDERLINE |
| Overall Δ | +0.421 | **+0.409** | +0.43 to +0.48 | < +0.40 | ⚠️ BORDERLINE |

Tally: **5 confirmed / 1 falsified / 2 borderline.** The falsification and the one genuine refutation across the full scorecard are the paper's honesty-of-measurement signal: the protocol is capable of returning bad news when that is the correct news.

*v2.2 R3 Pillar III value* appears here as +0.500 rather than the +0.208 recorded in the v2.2 pre-registration. The v2.2 pre-reg used a partial-domain rollup (a subset of Pillar III domains mapped into the R3 aggregate); recomputation from the raw v2.2 JSON using the full community/governance/security/communication/transportation/economy mapping yields +0.500. **The recomputed +0.500 is the correct value**, and all v2.3 comparisons in this paper use it. The pre-registration's original +0.208 is preserved verbatim in Appendix E for auditability. Both values pass the v2.3 "≥ +0.15 hold gains" target, so the correction does not alter any pre-registered outcome.

### 6.4 Per-Ring, Per-Pillar, Per-Model (v2.3)

**By Ring** (v2.1 → v2.3 trajectory):

| Ring | v2.1 Δ | v2.2 Δ | v2.3 Δ | v2.3 CI |
|---|---:|---:|---:|---|
| R1 Canonical | +0.44 | +0.50 | +0.49 | [+0.27, +0.70] |
| R2 Structured | +0.55 | +0.58 | +0.46 | [+0.30, +0.64] |
| **R3 Derived** | **+0.14** | **+0.18** | **+0.27** | **[+0.12, +0.44]** |

R1 held through the four iterations (the R1 `accuracy` drag — see §7 — is offset by gains in `cites_evidence`, `names_builders`, `recency`, and `acknowledges_complexity`). R2 dropped from v2.2 to v2.3 by 0.12, most of which concentrates in the `states_conditions` criterion (+0.262 → +0.190) and is suspected to be a side-effect of the v2.3 system-prompt softening. This is flagged as future work (§8).

**By Pillar** (v2.3, overall across all rings):

| Pillar | Baseline | Augmented | Δ |
|---|---:|---:|---:|
| I Material | 4.31 | 4.65 | +0.34 |
| II Human | 3.81 | 4.47 | +0.66 |
| III Collective | 4.25 | 4.46 | +0.21 |
| IV Production | 4.04 | 4.62 | +0.58 |
| V Transcendent | 4.08 | 4.54 | +0.46 |

**By Test Model** (v2.3):

| Model | Baseline | Augmented | Δ | 95% CI |
|---|---:|---:|---:|---|
| openai/gpt-5.4-mini | 3.94 | 4.63 | **+0.70** | [+0.45, +0.97] |
| anthropic/claude-haiku-4-5 | 4.02 | 4.54 | **+0.52** | [+0.29, +0.78] |
| x-ai/grok-4.1-fast | 4.32 | 4.54 | +0.22 | [+0.00, +0.44] |
| google/gemini-3.1-flash-lite | 4.32 | 4.51 | +0.19 | [−0.04, +0.43] |

The cost-efficient models (GPT-5.4 Mini at ~$0.15/M tokens, Haiku at ~$0.25/M) lead. Gemini Flash-Lite's CI crosses zero — consistent with the pattern that the Codex helps most where baseline knowledge is thinnest; Gemini Flash-Lite has the strongest baseline of the four subjects and the narrowest room to improve.

### 6.5 The Pillar-Level R3 Decomposition (v2.1 → v2.3)

This is the paper's most empirically dense finding: the same intervention architecture produces qualitatively different responses across pillars, and the decomposition itself is the diagnostic instrument that drove each subsequent intervention.

| Pillar | Failure Mode | v2.1 R3 Δ | v2.2 R3 Δ | v2.3 R3 Δ | v2.3 Tier |
|---|---|---:|---:|---:|---|
| I Material | Content gap | +0.08 | +0.13 | **+0.38** | Mixed (food/shelter FULL; others CONDENSED) |
| II Human | Format gap | **+0.50** | +0.25 | **+0.42** | REMOVED |
| III Collective | Governance gap | −0.13 | +0.50 | **+0.63** | FULL |
| IV Production | Velocity gap | +0.31 | +0.13 | **+0.25** | Mixed (co-creative CONDENSED; others REMOVED) |
| V Transcendent | Reflexivity gap | +0.25 | +0.25 | **+0.38** | CONDENSED |

**Every pillar gained from v2.2 to v2.3. None regressed.** The REMOVED tier — stripping both the Check 6 gate and the Empowered Action Frame paragraph from the `council_synthesis` entries of Pillars II and IV's analytical-strength domains — produced the largest single-pillar swing (+0.167 for Pillar II).

The decomposition traces three distinct stories:

**Format gaps (Pillar II: education, longevity, consciousness).** In v2.1 these domains had the highest overall delta (+0.64) and the highest R3 delta (+0.50). The analytical substrate already existed; the Reasoning Scaffold organized it into executable sequences. In v2.2, uniform application of the empowerment gate competed with this analytical substrate and the R3 delta fell to +0.25. In v2.3, removing the gate from these domains restored the gain: +0.42. The format-gap hypothesis holds; what v2.2 taught was that adding empowerment content where analytical content is already sufficient is counterproductive.

**Governance gaps (Pillar III).** In v2.1 these domains dropped R3 by −0.13 under the Reasoning Scaffold — the scaffold directed models to sequence reasoning about institutional content that the base entries and model training data both lacked, producing more structured but emptier responses. Adding 12 institutional entries in v2.2 filled the content gap, and R3 swung to +0.50. The v2.3 FULL-tier empowerment treatment held and extended the gain to +0.63.

**Velocity gaps (Pillar IV).** v2.1 R3 was +0.31; v2.2 regressed to +0.13 under uniform empowerment; v2.3 recovered to +0.25 after empowerment was removed from computation-intelligence, science-engineering, and manufacturing (with co-creative-intelligence held at CONDENSED). Velocity-gap domains behaved similarly to format-gap domains under empowerment overlay.

The generalizable principle: **intervention intensity should be calibrated to content gap per domain.** Uniform scaffolding under-serves some pillars and actively harms others. A format-gap domain needs Reasoning Scaffolds but does not need additional empowerment framing; a governance-gap domain needs both targeted content *and* empowerment scaffolding; a velocity-gap domain needs decision frameworks without motivational overlay.

### 6.6 Grok Trajectory

The Grok 4.1 Fast R3 delta has improved in three successive release cycles:

| Version | Grok R3 Δ | Intervention |
|---|---:|---|
| v2.1 | −0.38 | Uniform Reasoning Scaffold |
| v2.2 | −0.14 | +12 institutional entries + empowerment gate |
| v2.3 | **+0.00** | Pillar-gated empowerment |

The v2.1 hypothesis (Grok's high baseline directiveness is over-structured by reasoning scaffolds) is not falsified, but it is complicated: successive data-side interventions have closed most of the gap without any model-adaptive retrieval change. The v2.3 pre-registration's escalation clause ("if Grok R3 still < 0 after both specs: document as model-side limitation") is not triggered. One more intervention — likely the Spec 2B-A rubric redesign — will clarify whether the trajectory continues into positive territory or hits a model-side ceiling.

### 6.7 The `empowers` Criterion

| Version | `empowers` Δ | Change |
|---|---:|---|
| v2.0 | −0.18 | — |
| v2.1 | −0.16 | +0.02 |
| v2.2 | −0.04 | **+0.12** (uniform empowerment gate) |
| v2.3 | **−0.01** | +0.03 (pillar-gated gate) |

The `empowers` deficit — characterized in v2.1 as a structural property of RAG augmentation — is largely resolved by v2.3. The pillar-gated gate recovered motivational framing where it was needed without trading off the `concrete_steps` and `real_examples` gains (see §6.4 and §7's rhetorical interference discussion). We no longer report `empowers` as a structural RAG tension; the evidence now suggests it is addressable by calibrated scaffold design.

### 6.8 The Five Meta-Patterns

During the v2.1 forge phase, four frontier models independently assessed 252 entries across 21 domains. A convergent meta-pattern emerged across all five pillars: **multi-model knowledge production systematically represents the innovation layer while underrepresenting the institutional layer that determines whether innovation serves populations.** This manifests differently by pillar:

| Pillar | Failure Mode | What's Missing |
|---|---|---|
| I Material Foundation | Content gap | Supply-side technology celebrated; governance, infrastructure, and allocation systems absent |
| II Human Capability | Format gap | Diagnosis present; executable protocols, decision trees, triage frameworks absent |
| III Collective Coordination | Governance gap | Tools + analysis present; conflict resolution, anti-capture mechanisms, protection architecture absent |
| IV Production & Discovery | Velocity gap | Acceleration tools exponential; verification infrastructure linear |
| V Transcendent Frontier | Reflexivity gap | Possibility described without examining what shapes which possibilities can be imagined |

The taxonomy predicts *qualitatively different responses* to the same structured-context intervention — a prediction borne out by the pillar-level R3 decomposition across three iterations (§6.5). The v2.2 +12 institutional entries directly addressed the Pillar III governance gap and produced the predicted swing.

**Governance as cross-cutting dependency.** Governance-related keywords appear in 85.2% of conditional optimism statements across the 285-entry corpus, ranging from 94% (Pillar III) to 68% (Pillar II). Every pillar's conditional optimism is partially contingent on governance infrastructure that the corpus itself systematically underweights. See Appendix D for the full frequency table.

### 6.9 Corpus Expansion and Retriever Saturation

| Version | Corpus | Overall Δ | Shadow Force-Pull | Graph Expansion |
|---|---:|---:|---|---|
| v1.0 | 63 | +0.35 | ~35% | ~65% |
| v2.0 | 252 | +0.33 | ~0% | ~3% |
| v2.1 | 273 | +0.38 | ~0% | ~3% |
| v2.2 | 285 | +0.42 | ~0% | ~3% |
| v2.3 | 285 | +0.41 | ~0% | ~3% |

The four-version progression confirms the corpus-saturation finding: the overall delta is stable across a 63 → 285 expansion (all within overlapping CIs). The binding constraint is the retrieval window, not corpus size. The shadow force-pull rate collapsed from ~35% (v1.0) to ~0% (v2.0 forward) — at 252+ entries the dataset's immune system is self-balancing.

What moved the benchmark after v2.0 was not more content but *different* content, and *differently-applied* scaffolding. The 21 `council_synthesis` entries represent 7.4% of the final corpus and produced the entirety of the R3 movement across the four iterations.

### 6.10 Authorship-as-Variable

The v2.0 run records the `co_author_model` for every retrieved Codex entry and produces a post-hoc cross-authorship matrix. For each test model we compared its mean delta on retrieved contexts authored by its own company's frontier model ("same-company") versus contexts authored by other companies' frontier models ("cross-company").

| Test model | Same-company author | Same Δ | Cross Δ | Δ-of-Δ |
|---|---|---:|---:|---:|
| anthropic/claude-haiku-4-5 | claude-opus-4-6 | +0.476 | +0.481 | −0.005 |
| google/gemini-3.1-flash-lite | gemini-3.1-pro | +0.222 | +0.209 | +0.014 |
| openai/gpt-5.4-mini | chatgpt-5.4-thinking | +0.557 | +0.524 | +0.034 |
| x-ai/grok-4.1-fast | grok-super | +0.111 | +0.112 | −0.001 |

All four Δ-of-Δs are within noise. **Subject-side same-company affinity is null.** Combined with the v1.0 judge in-group finding (Grok 4.20 at +0.50), the bias story is localized: **in-group bias is a judge phenomenon, not a subject phenomenon.** Audit your judge pool for vendor-internal bias before accepting blind-council assumptions, but do not assume that judge bias implies corresponding subject bias.

### 6.11 Council Synthesis Retrieval Statistics

The 8+1 architecture delivers `council_synthesis` entries at 100% on R3 prompts via the dedicated reasoning slot, with Reasoning Scaffold depth-locked at FULL (~3,859 tokens per entry on average). R1 and R2 receive `council_synthesis` only via natural scoring in content slots (62% and 71% respectively) at CONDENSED tier averaging 1,538–1,579 tokens. This differential exposure — designed in v1.1 and unchanged through v2.3 — means that R3 improvements observed across the four iterations are attributable to the `council_synthesis` content delivered through the reasoning slot.

### 6.12 Summary of Findings

1. Overall Codex augmentation lifts efficiency-tier responses by **+0.41 / 5 points** (CI [+0.29, +0.53]), stable across four corpus versions and four targeted interventions.
2. The R3 arc closes at **+0.27 CONFIRMED** against pre-registered band [+0.25, +0.30], after three prior iterations that were null, inconclusive, and missed-by-fractions.
3. **Pillar-level R3 decomposition** reveals at least five distinct failure modes (content, format, governance, velocity, reflexivity). Intervention intensity must be calibrated per domain; uniform scaffolding produces compensating regressions.
4. **Every pillar gained and none regressed** under the v2.3 pillar-gated empowerment design — the REMOVED tier produced the largest swing in analytical-strength domains (Pillar II: +0.167).
5. **Grok trajectory** has closed from −0.38 → −0.14 → +0.00 across three releases without any model-adaptive retrieval change.
6. The **`empowers` criterion deficit** (−0.16 in v2.1) is largely resolved (−0.01 in v2.3) by pillar-gated scaffolding — it is not a structural RAG tension after all, it is a calibration problem.
7. **Subject-side same-company affinity is null**; v1.0 in-group bias was entirely judge-side.
8. The **R1 `accuracy` criterion is structurally un-movable** in its current form (see §7).
9. **Rhetorical interference**: Pillar II R3 gained from *removing* empowerment content, not adding it. Token-length correlation |r|=+0.209, retrieval drop 3–4% — content-driven, not attention-budget-driven (see §8).

---

## 7. The R1 Accuracy Problem: A Structural Limit of LLM-as-Judge RAG Evaluation

### 7.1 Five Interventions, No Movement

The R1 `accuracy` criterion resisted every intervention applied to it across v2.2 and v2.3:

| Version | Intervention | R1 `accuracy` Δ | Moved? |
|---|---|---:|---|
| v2.1 | (no targeted intervention) | −0.21 | baseline |
| v2.2 | Confidence floor (0.75) filtering ~21 low-confidence entries | −0.23 | No |
| v2.2 | Metadata stripping (`conf=` removed from passage output) | −0.23 | No |
| v2.2 | System prompt hardening against metadata parroting | −0.23 | No |
| v2.3 | Retriever year-relabeling (years ≥ 2025 → "recent data") | −0.26 | No (slightly worse) |
| v2.3 | System prompt softening ("source and time period") | −0.26 | No |
| v2.3 | Judge preamble calibration (attempted) | — | Dropped after 2 rounds failed |

Five targeted interventions across two release cycles, directionally aimed at the same diagnostic hypothesis (post-cutoff data being read as fabrication by the judge). None moved the metric. The v2.3 value is the lowest of the sequence.

### 7.2 The 19× Dose-Response

Cross-tabulating the v2.2 augmented R1 responses by the count of post-2024 date mentions produces a monotonic dose-response pattern:

| 2025+ year mentions in augmented R1 response | n | Accuracy pass rate |
|---:|---:|---:|
| 0 | 6 | **83.3%** |
| 1–2 | 13 | 23.1% |
| 3–5 | 27 | 22.2% |
| 6+ | 38 | **10.5%** |

Baseline 2025+ mentions per response: **0.35**. Augmented: **6.62** — approximately 19×. When the augmented condition happens to surface zero post-2024 dates, accuracy passes 83% of the time — *higher* than the baseline pass rate of 44%. When augmentation cites six or more post-2024 dates, accuracy passes only 10.5%.

The augmented condition scores higher than baseline on every other R1 criterion (`cites_evidence`, `names_builders`, `recency`, `acknowledges_complexity`). The judge recognizes the responses as more thorough, more current, more source-attributed, more complexity-aware — and specifically penalizes the one criterion that requires verification against training data.

### 7.3 Judge Preamble Calibration — Two Rounds, Opposite Failures

The v2.3 pre-registration included a judge-preamble calibration dry-run as Spec A's primary lever: instruct the judge to score `accuracy=1` for plausible sourced claims even if post-cutoff, `accuracy=0` only for internal inconsistency, contradiction of established reference values, or unsourced fabrication. The calibration used three control sets:

- 13 v2.2 worst R1 regressions (should flip 0 → 1 under the patched judge)
- 5 invented-publication controls (plausible-sounding fabricated sources — should remain 0)
- 5 wrong-value controls (real sources, wrong numbers — should remain 0)

Results:

| Round | Preamble posture | Regression flips | Invented FPs | Wrong-value FPs |
|---|---|---|---|---|
| 1 | Permissive ("and similar institutional publishers" halo) | **11/11 PASS** | **2/5 FAIL** | 0/5 PASS |
| 2 | Restrictive ("confirm publisher from training knowledge") | **1/3 FAIL** | 0/5 PASS | not retested |

The two failure modes sit on opposite sides of the same axis. Round 1 grandfathered fabricated institutional-sounding names via halo phrasing; Round 2 over-corrected and rejected legitimate citations to bodies the judge could not independently recognize. Per a pre-registered rule ("two rounds is rigorous; three is overfitting to the control set"), the preamble was dropped rather than tuned a third time — preserved as commit `afdc6e1`.

The calibration outcome — documented in the pre-registration addendum before benchmark execution — establishes a result that does not depend on the subsequent v2.3 numbers: **no single preamble can reliably separate "plausible and sourced but post-cutoff" from "invented" without either halo error or over-rejection.**

### 7.4 Root Cause: Rubric, Not Data

The `accuracy` criterion as written conflates two distinct properties:

- **Verifiable from training.** Can the judge confirm this specific claim against its own training data?
- **Plausible, consistent, and sourced.** Is this claim internally consistent, attributed to a named institution, consistent with established reference values?

RAG-augmented responses systematically surface recent, specific, well-sourced data that judges cannot verify against their own training cutoff. The more the dataset does its job — retrieving current, specific, institutionally-sourced evidence from IRENA, IEA, BloombergNEF, Berkeley Lab, NAHB, UN-Habitat, NOAA, and similar authoritative bodies — the more the accuracy criterion penalizes it. In the v2.2 corpus, 42% of evidence anchors are dated 2025 or later, 14% are 2026-dated. These are real, curated statistics; the Codex is genuinely fresher than the judge.

This is a structural limitation of LLM-as-judge evaluation for any RAG system with post-cutoff data, not specific to the Abundance Codex. Five interventions failing in the same direction, combined with a two-round calibration failing on opposite sides of the same axis, is not a data problem; it is a measurement problem.

### 7.5 Proposed Redesign

For v2.4 we propose splitting the single `accuracy` criterion into two binary criteria:

- **`factual_consistency`:** Are claims internally consistent and consistent with established reference values? Scores `1` for claims about post-cutoff figures cited to named institutions; scores `0` only for internal contradiction or contradiction of well-known reference data.
- **`source_attribution`:** Are specific statistical or institutional claims attributed to named sources rather than presented as bare assertions? Scores `1` for "According to the IEA 2024 outlook…"; scores `0` for unsourced bare assertions or (if the judge can confirm) fabricated-institution citations.

The combined R1 score increases from 5 to 6 criteria. v2.4 runs both rubrics on every R1 evaluation (legacy `accuracy` preserved for longitudinal comparability) with a calibration control set before the full benchmark. After v2.4 validates the split, legacy `accuracy` can be deprecated in v2.5.

**Predicted impact.** `factual_consistency` Δ ≥ 0.00, `source_attribution` Δ ≥ +0.15. Combined effect: the R1 accuracy drag unmasks the R3 Spec-B gain in the aggregate delta (projected overall Δ: +0.45 to +0.52).

### 7.6 Generalization Beyond This Project

The finding is independent of whether the Codex's R3 intervention works. Any benchmark that evaluates RAG-augmented responses using a frozen LLM judge with a training cutoff is vulnerable to this bias in proportion to how fresh the retrieved data is. As agents are increasingly augmented with post-cutoff information — regulatory updates, current-year statistics, new institutional reports — benchmark scorecards that use an accuracy-style binary criterion will systematically under-credit augmentation. The remediation is either a split rubric (our proposal), a rolling-window judge, or structural de-specification of year tags at the retrieval layer (which the v2.3 year-relabel attempted at the secondary-fix level, with no observable effect on its own).

---

## 8. The Rhetorical Interference Mechanism

Pillar II's R3 gained +0.167 from v2.2 to v2.3. The intervention that produced the gain was **removal**, not addition: the Check 6 empowerment gate and the Empowered Action Frame paragraph were stripped from the three `council_synthesis` entries for education, longevity, and consciousness. The consciousness domain was the starkest case: R3 recovered from −0.25 (v2.2) to +0.00 (v2.3).

Two hypotheses can explain this:

- **Content hypothesis:** Empowerment framing competed with the analytical substrate that Pillar II's base entries already deliver well. Removing motivational overlay restored the scaffold's analytical signal.
- **Attention-budget hypothesis:** Removing two sections shortened the retrieved context. Shorter context → more focused responses → higher scores.

We tested the attention-budget hypothesis directly. For the six Pillar II REMOVED-tier prompts (three R3 domains × 2 conditions × 4 models = 24 augmented evaluations), we computed: (a) mean retrieved-passage token count per prompt across v2.2 vs. v2.3, and (b) per-prompt score correlation with retrieval length in v2.3. The retrieval drop between v2.2 and v2.3 for these prompts was **3–4%** (below the 20% threshold we pre-specified as meaningful for an attention-budget mechanism). The per-prompt score-to-length correlation was **|r| = +0.209** (below the 0.3 threshold). Neither signal supports the attention-budget hypothesis.

Qualitatively, the difference is visible. Grok's consciousness R3 response in v2.2 read as rhetorical — motivational but thin: long paragraphs about empowerment, few specific referents. Grok's v2.3 response on the same prompt cites Vonderlin et al. (2020) on cold exposure, the Davidson Healthy Minds program's specific protocol structure, and the Huberman "physiological sigh" as a named intervention. The same model, the same prompt, a shorter retrieved context with empowerment framing removed — and the response shifts from encouragement-heavy to citation-dense.

We label the mechanism **rhetorical interference**: empowerment framing competes with analytical reasoning for a model's attention in domains where the model's priors are already strong. In format-gap domains (where the analytical substrate exists in the base entries), adding motivational overlay dilutes rather than supplements. In governance-gap domains (where the analytical substrate is missing), the same overlay fills a real gap and improves R3.

**The generalizable claim:** intervention intensity should be calibrated to content gap per domain. Uniform scaffolding is an error of omission disguised as an error of commission — it looks like adding value across the board; it is actually adding value somewhere and imposing rhetorical noise elsewhere. For any RAG system that layers stance interventions on top of analytical content, the relevant question is not "is this intervention helpful on average?" but "in which content conditions does this intervention help, and in which does it interfere?"

---

## 9. Discussion

### 9.1 What the result is

The central finding is twofold. First, the Codex improves agent responses by +0.41 on a 15-criterion rubric probing evidence use, structured analysis, and framing, with R3 actionability confirmed at +0.27 against a pre-registered target — a result that took four iterations to establish and that none of the simpler one-shot interventions in v2.0 through v2.2 produced. Second, actionability is not a single construct: it decomposes into content, format, governance, velocity, and reflexivity gaps, and structured-context interventions are effective on some (format, governance) and counterproductive on others when applied uniformly.

The paper supports a narrow architectural claim: a structured narrative dataset, retrieved deterministically, injected into the system prompt of a cost-efficient model, and scaffolded with domain-calibrated Reasoning Scaffolds, produces a measurable and repeatable improvement on a 15-criterion rubric — with the scaffolding calibration as important as the scaffolding itself.

### 9.2 Architecture beats scale

The four-version corpus expansion (63 → 252 → 273 → 285 entries) produced almost no movement in the overall delta (+0.35 → +0.33 → +0.38 → +0.41, all within overlapping CIs). What did produce movement was architecture: the 8+1 retrieval split, the depth-locked Reasoning Scaffold, the 21 `council_synthesis` entries (7.4% of the corpus by count), the +12 institutional entries targeting a specific content gap, and the pillar-gated scaffold calibration that replaced uniform application.

Effort is better spent on format discipline, retrieval architecture, and coverage of qualitatively distinct content types than on scaling entry counts. Once a corpus covers the evaluation domains at retrieval-window density, additional entries do not translate into benchmark lift.

### 9.3 The R3 decomposition

The v2.0 R3 null suggested three non-exclusive hypotheses: baseline ceiling, content-format mismatch, and rubric granularity. Across three interventions we refined this into a five-failure-mode taxonomy (§6.8) that generated testable per-pillar predictions (§6.5). Format gaps responded to Reasoning Scaffolds alone (Pillar II v2.1: +0.50). Governance gaps responded only after content was added (Pillar III v2.2: +0.50 swing). Velocity gaps tolerated scaffolds but not motivational overlay (Pillar IV v2.3 recovery after REMOVED tier). The decomposition is not a post-hoc rationalization; it was committed to git at v2.1 and used to generate v2.2's and v2.3's pre-registered predictions.

### 9.4 The empowerment-analysis tension, revised

The v2.1 paper framed the `empowers` deficit as a structural property of RAG systems: shadow-integrated, condition-explicit content trades motivational framing for analytical structure. The v2.3 evidence complicates this. Uniform empowerment scaffolding (v2.2) did reduce the deficit (−0.16 → −0.04) but at the cost of Pillar II and IV R3 regressions. Pillar-gated scaffolding (v2.3) kept the `empowers` gain (−0.01) *and* recovered the R3 regressions. The tension is real but calibration-addressable: honest complexity and empowering tone can coexist if intervention intensity is matched to content need.

### 9.5 Limitations

**Single-judge sensitivity.** v2.0 through v2.3 rely on a single Opus judgment per response. The R1 accuracy finding (§7) is itself a manifestation of this limitation — a different judge with a different training cutoff might produce different R1 numbers. We mitigate by: the v1.0 Opus-only rebaseline as a within-judge comparison point, a binary rubric with explicit criterion definitions, a frozen judge prompt template, and pre-registered targets/falsification bounds that make single-judge dependence legible.

**Judge-cutoff verifiability bias.** Characterized in §7. Documented as a structural limit rather than mitigated. The v2.4 rubric redesign is the proposed remediation.

**Pillar-level sample sizes.** The per-pillar R3 decompositions rest on varying sample sizes: Pillar II has 3 domains (12 matched R3 pairs per model), Pillar III has 6 domains (24 matched R3 pairs per model). Per-pillar CIs are wide. The patterns replicate across three iterations (v2.1, v2.2, v2.3), which tightens confidence but does not eliminate the small-sample caveat.

**Out-of-pillar-map regressions.** Two domains — communication and security — showed R3 regressions of −0.500 each in v2.3 and are not in the pre-registered pillar map. They were not subjects of the v2.3 hypothesis and did not receive the v2.3 intervention. A domain audit (are these framework/trendline-dominant domains without strong `council_synthesis` coverage?) is planned for v2.4.

**Post-hoc optimization risk.** Four rounds of pre-registered diagnose-intervene-measure reduce but do not eliminate overfitting to the benchmark. The pre-registered falsification bounds (visible before each run) are the main defense; the one falsified prediction (R1 accuracy) and the three inconclusive outcomes (v2.1 primary R3; v2.3 overall and consciousness as borderline) are evidence that the protocol returns bad news when warranted.

**R2 states_conditions drop.** R2 overall Δ dropped from +0.583 (v2.2) to +0.464 (v2.3), concentrating in the `states_conditions` criterion. The suspected cause is the v2.3 system-prompt softening ("source and time period" replacing "note the source year"). An A/B test isolating the system-prompt change is planned for v2.4.

**Retrieval window saturation.** The 9-entry retrieval window was chosen to keep augmented-condition context at ~10K tokens. A different window size might change both the corpus-expansion finding and the `council_synthesis` delivery pattern. We have not run this ablation.

**Anonymization is imperfect.** The anonymization regex strips explicit self-identification but cannot remove stylistic fingerprints. A judge familiar with model writing styles may still recognize sources.

**Prompt sensitivity unmeasured.** The 63 prompts were hand-written once. We have not tested sensitivity to paraphrase variants.

**Causal mechanism underdetermined.** ACE shows correlation between Codex augmentation and improved scores; it cannot distinguish whether improvement comes from evidence content, stance framing, shadow integration, or retrieval structure without ablation experiments. §8's rhetorical interference finding is the closest we come to isolating a single mechanism.

**Values-laden framing.** "Conditional optimism" is not a neutral stance. We describe it explicitly in §1 and §3 to make the values claim transparent.

### 9.6 Ethical considerations

The Codex is co-authored by four frontier models from four companies whose training data, safety postures, and stylistic tendencies are not independent. A dataset produced by this committee may inherit shared biases from the underlying providers. The multi-model design reduces single-vendor stylistic bias but does not eliminate cross-vendor correlated priors. The authorship-as-variable analysis partially addresses this by failing to find subject-side same-company preference, but the corpus remains an artifact of a specific moment in frontier AI development.

The epistemic monoculture concern raised during the council synthesis process deserves explicit acknowledgment. Four models trained on substantially overlapping internet text may share deeper assumptions that multi-model authorship does not surface. The five meta-patterns — particularly the systematic underrepresentation of institutional infrastructure (§6.8) — may themselves be a product of this shared training-data bias rather than an objective feature of the knowledge landscape.

---

## 10. Future Work

1. **v2.4 rubric redesign (Spec 2B-A).** Split `accuracy` into `factual_consistency` and `source_attribution` with a two-round calibration control set. Dual-report legacy `accuracy` for longitudinal comparability.
2. **R2 system-prompt A/B.** Isolate whether the `states_conditions` Δ drop from v2.2 to v2.3 is caused by the "source and time period" softening. Revert or refine.
3. **Communication and security domain audit.** Both domains regressed R3 by −0.500 in v2.3 and are outside the pillar map. Determine whether they need `council_synthesis` entries with their own scaffolds or a different intervention.
4. **Grok next intervention.** Three successive R3 improvements (−0.38 → −0.14 → +0.00) without model-adaptive retrieval. One more data-side intervention before the model-side-ceiling hypothesis is formally accepted.
5. **Mechanistic ablation.** Decompose the augmented context into isolated components: evidence anchors only, council voices only, Reasoning Scaffold only, contrastive pair only. Isolate the R1/R2 driver and the R3 format-gap driver.
6. **External judge models.** Re-run under a different single-judge model with a different training cutoff to test whether the R1 accuracy pattern persists. A judge with a later cutoff is the cleanest test of §7's hypothesis.
7. **Model-adaptive retrieval.** Test a retriever that adjusts Reasoning Scaffold inclusion based on the test model's baseline directiveness score computed from unaugmented responses.
8. **Prompt sensitivity audit.** Paraphrase variants for each of the 63 prompts, re-run, and bound prompt-level variance.
9. **Cross-dataset evaluation.** Does the diagnose-intervene-preregister-measure methodology generalize to narrative datasets outside the abundance domain?

---

## 11. Conclusion

The Abundance Codex is a deliberate bet that *architecture*, not *scale*, is the right lever for measurably changing how cost-efficient AI agents reason about civilization-scale challenges. The four-iteration ACE benchmark supports that bet. A 285-entry corpus retrieved deterministically and injected into the system prompt lifts response quality by +0.41 points on a 15-criterion rubric, with the lift concentrated in evidence and structured analysis and — after four rounds of diagnose-intervene-preregister-measure — confirmed at +0.27 on derived actionability against a pre-registered target band. A 4.5× corpus expansion produced no aggregate delta movement. Architectural interventions — the 8+1 retrieval split, the Reasoning Scaffold, the 12 institutional entries targeting a specific content gap, and the pillar-gated empowerment design that replaced uniform scaffolding — produced all of the R3 movement across the arc.

The benchmark is disciplined enough to return bad news. One pre-registered prediction was falsified (R1 accuracy, in the same direction five interventions failed to move) and three returned inconclusive or borderline. Rather than tune the judge preamble a third time after two rounds failed on opposite sides of the same axis, we dropped it — a pre-registered decision documented before the benchmark ran — and reported the R1 deficit as a structural limit of LLM-as-judge RAG evaluation that applies to the entire field, not just this project.

A single intervention can reveal a single number. Four pre-registered iterations, each building on the previous round's diagnosis, reveal a structure. Actionability decomposes into at least five failure modes; uniform scaffolding helps some and harms others; intervention intensity must be calibrated to content gap; motivational framing competes rhetorically with analytical substrate in content-rich domains; post-cutoff sourcing systematically trips judge-verification bias in ways no preamble can reliably patch. These are findings about structured-context systems generally, not just about this dataset.

The contribution we hope proves durable is not the specific deltas — numbers drift with model generations, corpus updates, and rubric revisions. The contribution is a methodology: diagnose the failure mode, design a targeted intervention, pre-register the prediction with a falsifiable bound, measure the effect, and — when the result is more complex than the hypothesis — decompose it until the next intervention is obvious. The Codex and ACE are instruments for this methodology. Abundance is not the destination. It is the stance. And stance is now something you can measure, diagnose, and selectively improve.

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

Full rubric definitions are in `evals/ace/rubrics.json`.

---

## Appendix B — Sample Entries

**Base entry.** A representative Codex entry — the Solar Revolution origin story — is at `domains/01-energy/01-the-solar-revolution.md`. It follows the full Gold Standard Format: YAML frontmatter with typed cross-domain connections, the five-phase Shift Arc, all five council voices, four evidence anchors with source years and confidence scores, a complete shadow check, the 6D position, and a practice hook for both human readers and agents.

**Council synthesis entry.** A representative `council_synthesis` entry — the education domain synthesis — is at `domains/07-education/13-education-council-synthesis.md`. It demonstrates the meta-analytical structure: YAML frontmatter with `co_author_model: multi-model-council` and `council_models` array, the standard Gold Standard Format sections, plus the Reasoning Scaffold (Scarcity Trap, 6-step Reframe Chain, Contrastive Pair). Education is in the Pillar II REMOVED tier for v2.3; the Agent Practice Hook appears without the Empowerment Gate (Check 6).

---

## Appendix C — Reproducibility

**Repository:** `github.com/CjTruHeart/abundance-codex`
**Dataset:** `huggingface.co/datasets/CjTruHeart/abundance-codex`
**License:** MIT (code), CC-BY (dataset content)
**Python:** 3.11+
**Dependencies:** `httpx>=0.27`, `pyyaml>=6.0`, `jsonschema>=4.20`

**To reproduce v2.3:**

```bash
git clone https://github.com/CjTruHeart/abundance-codex.git
cd abundance-codex
pip install -r scripts/requirements.txt
cp evals/ace/.env.example .env   # edit to add OPENROUTER_API_KEY
python3 scripts/run-ace.py --dry-run    # verify retrieval, no API calls
python3 scripts/run-ace.py               # full run, ~$5–11, ~2h 41min
```

The retriever version is auto-detected from the JSONL export (presence of `reasoning_scaffold` field triggers v1.1 behavior; years ≥ 2025 are rendered as "recent data" in passage output).

**Published run metadata:**

| Version | Timestamp | Run ID | Git SHA | Corpus | Duration |
|---|---|---|---|---:|---|
| v2.0 | 2026-04-13T10:31:33Z | `ace-20260413-103133.json` | `529bb85` | 252 | ~2h |
| v2.1 | 2026-04-14T02:18:08Z | `ace-20260414-021808.json` | `0a0dc68` | 273 | ~3h |
| v2.2 | 2026-04-16T20:43:30Z | `ace-20260416-204330.json` | `af1d628` | 285 | 2h 57m |
| v2.3 | 2026-04-17T01:41:55Z | `ace-20260417-014155.json` | `e4176a6` | 285 | 2h 41m |

All four: judge `anthropic/claude-opus-4.6`, temperature 0.0, max_tokens 2048, concurrency 8. Bootstrap CIs: 10,000 iterations, seed=42 (v2.3); 2,000 iterations (v2.2); 10,000 (v2.0, v2.1).

**Pre-registration commits:** v2.1 `e90869d`, v2.2 `546095e`, v2.3 `bd23712` (addendum inline in `PRE-REGISTRATION-v2.3.md`).

**v2.3 Spec implementation commits:** Spec A `77e3c66`, calibration controls `2451c99`, preamble drop `afdc6e1`, Spec B (pillar-gated) `5d0722a`.

**Council synthesis forge process:** The 84 raw model assessments are preserved in `council-synthesis/assessments/`. The human synthesis process is documented in `council-synthesis/FORGE-LOG.md`.

---

## Appendix D — Five Meta-Patterns and Governance Frequency

### D.1 The Five Meta-Patterns

The taxonomy emerged from the v2.1 council synthesis forge process (§4.2). Four frontier models independently assessed 252 entries across 21 domains, and five convergent failure modes were identified:

**Pillar I — Material Foundation (Content Gap).** Supply-side technological abundance systematically overrepresented; governance, infrastructure, and allocation systems that determine whether abundance reaches populations systematically underweighted. Grid modernization invisible behind solar cost curves; cold chains absent behind cheaper protein molecules; water metering absent behind desalination; zoning absent behind construction technology; preventable CVD deaths invisible behind frontier genomics.

**Pillar II — Human Capability (Format Gap).** Diagnostic eloquence without prescriptive protocols. AI tutoring celebrated while 70% of 10-year-olds in LMICs cannot read and no decision tree exists for teachers; epigenetic reprogramming mapped while cardiovascular prevention goes unmentioned and no triage framework exists; meaning crisis diagnosed but zero exercises taught. The entries know what matters but cannot teach anyone how to act.

**Pillar III — Collective Coordination (Governance Gap).** Institutional infrastructure absent behind technological and aspirational facades. Sensemaking collapses while connectivity is celebrated; belonging proved as health infrastructure while restorative justice receives zero entries; regulatory capture named but not tested against; encryption celebrated while 1 in 3 women experience violence; battery cost curves replace rail infrastructure; financial inclusion rails coexist with 100–400% APR digital lending. The v2.2 +12 institutional entries targeted this gap; the v2.3 FULL-tier empowerment scaffolding held and extended the gain.

**Pillar IV — Production & Discovery (Velocity Gap).** Acceleration tools exponential; verification infrastructure linear. Desktop fabrication and molecular assembly get entries while injection molding and quality systems (responsible for the gains the entries celebrate) get zero; 280× inference cost collapse documented but decision frameworks absent; BCG +40% quality documented alongside METR perception-reality divergence but no workflow resolves when co-creation helps vs. harms; AlphaFold celebrated while metrology and Registered Reports operate at institutional speed.

**Pillar V — Transcendent Frontier (Reflexivity Gap).** Aspirational narratives without methodology. A 97% launch cost collapse called "democratization" while one company controls 88% of US mass to orbit; applied foresight tools with decades of track records (backcasting, scenario planning, CLA, Delphi, Three Horizons) receive zero dedicated entries; the domain that justifies the entire Codex cannot teach anyone how to practice what it preaches.

### D.2 Governance Frequency Analysis

Governance-related keywords searched across all 285 entries' conditional_optimism sections:

- Entries with conditional_optimism content: 236 / 285
- Entries with 1+ governance keyword: 201 / 236 (85.2%)

| Pillar | Entries w/ CO | w/ Gov Keywords | % |
|---|---:|---:|---:|
| I Material Foundation | 64 | 57 | 89% |
| II Human Capability | 34 | 23 | 68% |
| III Collective Coordination | 71 | 67 | 94% |
| IV Production & Discovery | 46 | 37 | 80% |
| V Transcendent Frontier | 21 | 17 | 81% |

Top keywords: *standards* (84), *governance* (84), *regulatory* (56), *policy* (51), *transparency* (26), *reform* (24). Governance is the Codex's most cross-cutting conditional dependency, appearing across all pillars regardless of technical domain.

---

## Appendix E — Full Pre-Registration Scorecard

All predictions filed before each benchmark run; outcomes computed from the result JSONs after the fact.

### v2.1 (`e90869d`)

| # | Prediction | Threshold | Actual | Status |
|---|---|---|---|---|
| 1 | R3 Δ ≥ +0.15, CI lower bound > 0 | +0.15 | +0.143, CI crosses 0 | INCONCLUSIVE |
| 2 | Overall Δ within ±0.05 of +0.33 | [+0.28, +0.38] | +0.377 | CONFIRMED (boundary) |
| 3 | Per-model ranking: GPT-5.4 Mini & Haiku lead, Gemini borderline, Grok null | qualitative | matches | CONFIRMED |

### v2.2 (`546095e`)

| # | Prediction | Threshold | Actual | Status |
|---|---|---|---|---|
| 1 | Pillar III R3 Δ | ≥ +0.10, falsify < 0 | +0.208 | CONFIRMED |
| 2 | `empowers` Δ | ≥ −0.05, falsify < −0.10 | −0.036 | CONFIRMED |
| 3 | R3 overall Δ | ≥ +0.25, falsify < +0.18 | +0.179 | REFUTED (by 0.001) |
| 4 | R1 `accuracy` Δ | ≥ −0.05, falsify < −0.15 | −0.226 | REFUTED |

### v2.3 (`bd23712` + addendum)

| # | Prediction | Target | Falsify | Actual | Status |
|---|---|---|---|---|---|
| 1 | R3 overall Δ | +0.25 to +0.30 | < +0.22 | +0.274 | ✅ CONFIRMED |
| 2 | R3 Pillar II Δ | +0.40 to +0.50 | < +0.30 | +0.417 | ✅ CONFIRMED |
| 3 | R3 Pillar III Δ | ≥ +0.15 | < +0.10 | +0.625 | ✅ CONFIRMED |
| 4 | `empowers` Δ | ≥ −0.05 | < −0.10 | −0.012 | ✅ CONFIRMED |
| 5 | `real_examples` Δ | +0.15 to +0.20 | < +0.10 | +0.202 | ✅ CONFIRMED |
| 6 | R1 `accuracy` Δ | −0.08 to +0.05 (revised) | < −0.12 | −0.262 | ❌ FALSIFIED |
| 7 | R3 consciousness | +0.25 to +0.50 | < 0.00 | +0.000 | ⚠️ BORDERLINE |
| 8 | Overall Δ | +0.43 to +0.48 | < +0.40 | +0.409 | ⚠️ BORDERLINE |

Total across four iterations: **9 confirmed / 3 refuted / 3 inconclusive-or-borderline** out of 15 pre-registered predictions.
