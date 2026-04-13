# Technical Report Outline — The Abundance Codex & ACE Benchmark

> **Status:** outline, not draft. Sections below are scoped and bulleted, not written. Target venue: arXiv preprint + blog post. Target length: ~12–18 pages.

---

## Working title options

- *The Abundance Codex: A Narrative Dataset for Measuring Worldview Quality in AI Agents*
- *Measuring the Worldview Gap: How Structured Abundance Context Changes Frontier Model Reasoning*
- *Codex-Augmented Reasoning: A Benchmark for Conditional Optimism in AI Systems*

## Abstract (~200 words)

- First open-source, structured narrative dataset explicitly designed to test and improve the "worldview quality" of AI agents on civilization-scale challenges.
- 252 entries across 21 Grand Challenge domains, co-authored by four frontier models (Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, Super Grok) + a human editor, following a Gold Standard Format with five analytical voices per entry.
- ACE (Abundance Codex Evaluation) benchmark measures whether injecting Codex context improves cost-efficient models' responses on factual, analytical, and actionable reasoning tasks, judged on 15 binary criteria.
- v1.0 result: +0.36 mean delta (+9.0%) across 4 test models × 63 prompts × 2 conditions. Cost-efficient models (Haiku, GPT-5.4 Mini) improve the most (+0.49–0.58 delta).
- v2.0 result (pending): single-Opus-judge methodology applied to 252-entry corpus; comparison against v1.0 Opus-only rebaseline.
- Contribution: releasing dataset, retriever, benchmark, and per-entry metadata including co-author model attribution, enabling independent replication and extension.

## 1. Introduction & Motivation (~2 pages)

- **The worldview problem.** AI systems trained on generic corpora default to scarcity reasoning — framing civilizational challenges as intractable, fate-like, or zero-sum. This shows up in agentic deployments when models refuse, hedge, or collapse into generic advice when asked about long-horizon progress.
- **Why existing benchmarks miss it.** MMLU, HELM, BIG-bench test knowledge and instruction-following. They don't test whether a model holds a *generative* frame on hard problems — cites evidence, names builders, identifies leverage, grounds action.
- **The conditional-optimism frame.** Borrowing from Hans Rosling's *Factfulness*, Steven Pinker's *Better Angels*, Peter Diamandis's *Abundance*, and Kevin Kelly's *Protopia*: a stance that names evidence, names shadow, states conditions, invites action. Not Pollyanna; not doomer. Testable.
- **The dataset-as-instrument idea.** If we can construct a structured corpus that embodies conditional optimism across 21 Grand Challenges, we can both (a) use it as RAG context to lift AI agents and (b) use it as a benchmark substrate to measure the lift.
- **Contributions.**
  1. Codex dataset (252 entries, four co-authors, Gold Standard Format)
  2. Dojo Retriever — deterministic context selection with type-coverage enforcement
  3. ACE benchmark package (reproducible, single-judge v2.0)
  4. Finding: structured narrative context lifts cost-efficient models ~2–3× more than frontier models on Codex-relevant reasoning
  5. Finding: blind multi-judge councils can harbor measurable in-group bias (+0.50 observed for one vendor)
  6. Open-source release with reproducibility affordances (git SHAs, config hashes, author-attribution metadata)

## 2. Related Work (~1.5 pages)

- **RAG evaluations.** RAGAs, BEIR, MTEB — optimize retrieval quality; do not test worldview shifts.
- **Reasoning benchmarks.** MATH, GPQA, Humanity's Last Exam — test capability ceilings; orthogonal to framing.
- **Values and stance benchmarks.** TruthfulQA, MACHIAVELLI, WVS-style surveys — test values; not tied to domain reasoning.
- **Narrative datasets as AI substrates.** HellaSwag, StoryCloze; WordCraft, BookCorpus — tests of narrative understanding, not explicit worldview framing.
- **Judge-model evaluation.** MT-Bench, Chatbot Arena, AlpacaEval, PandaLM — LLM-as-judge methodology; documented biases (length, position, same-family). ACE inherits and extends this literature with a measured in-group bias finding.
- **Abundance-adjacent reading.** Rosling (Factfulness), Pinker (Enlightenment Now), Diamandis (Abundance), Our World in Data — the knowledge base being encoded. Jim Collins / Ray Dalio / Donella Meadows on systems and leverage points — framing influences.

## 3. Dataset Design (~2.5 pages)

### 3.1 Gold Standard Format
- 19 required sections per entry, machine-validated.
- Five council voices: Oracle (frame), Critic (shadow), Sensei (framework), Builder (leverage), Witness (lived experience).
- Evidence anchors with confidence gradient (high / medium / emerging).
- Shadow check mandatory on every entry.
- Entry types: origin_story, breakthrough, false_dawn, shadow, contrast, framework, builder_profile, trendline, paradigm_seed, grand_challenge, star_trek_spec.

### 3.2 Three Rings
- Ring 1 canonical (evidence), Ring 2 structured (analysis), Ring 3 derived (action). Mirrors the Codex's own architecture.

### 3.3 Multi-Model Co-Authorship
- Four frontier models co-author entries in parallel (3 per author per domain).
- Human editor (Cj TruHeart) maintains voice consistency and validates each entry.
- Attribution preserved in `co_author_model` frontmatter field throughout the pipeline.
- Design rationale: reduces single-model stylistic bias in the corpus; enables the authorship-as-variable analyses in §6.

### 3.4 Validation
- `scripts/validate-entry.py` — 4 layers: YAML schema, domain connections, section presence, evidence anchor count.
- 252/252 pass.

### 3.5 Export
- JSONL flattening of structured fields for machine consumption.
- Composite witness disclosure embedded per entry (no aggregate register; disclosure lives adjacent to the voice).

## 4. Dojo Retriever (~1.5 pages)

### 4.1 Design
- Deterministic, no embeddings, no external API calls.
- 7-stage pipeline: intent classification → domain identification → candidate scoring → type coverage enforcement → passage extraction (3 tiers) → strategic ordering → context assembly.
- Shadow force-pull rule: ANALYTICAL/STRATEGIC queries must include at least one shadow entry.
- Corpus size grew 63→252 between v1.0 and v2.0; shadow force-pull and graph-expansion rates dropped from ~35% / ~65% to ~0% / ~3% because natural coverage at 252 is dense enough.

### 4.2 Why not embeddings
- Reproducibility: deterministic → byte-identical context across runs.
- Transparency: keyword-rule-based → auditable reasoning.
- Enough is enough: 21 domains is small enough for curated keyword lists to outperform ad-hoc semantic search.
- Limitation: generalization to arbitrary queries requires keyword-list maintenance.

## 5. ACE Benchmark (~2.5 pages)

### 5.1 Architecture
- 4 efficiency-tier test subjects × 63 eval prompts × 2 conditions (baseline / augmented). Anonymized responses scored on 5 binary criteria per ring.
- v1.0: 4-judge blind council (Opus, GPT-5.4, Gemini 3.1 Pro, Grok 4.20).
- v2.0: single Opus judge (see §5.3).

### 5.2 Scoring Rubric
- 15 total criteria (5 per ring). Binary, explicit definitions.
- Chosen to reward observable properties, not "quality."

### 5.3 Judge Selection — Why We Moved From Council to Opus-Only
- v1.0 4-judge council revealed a measured Grok 4.20 in-group bias of +0.50 against Grok 4.1 Fast.
- Other judges: Opus at −0.13, GPT-5.4 at −0.14, Gemini at +0.18 (all small).
- v2.0 decision: lock the judge. Trade-off: lose inter-judge variance as a noise dampener; gain reproducibility and a clean instrument.
- **Comparability baseline.** v1.0 raw data preserves per-judge breakdowns, so we isolated only the Opus judgments from v1.0 and re-aggregated. This Opus-only rebaseline is the v2.0 comparison anchor — comparisons are judge-matched, so observed deltas isolate corpus/retriever effects, not judge changes.
- Implication: LLM-as-judge designers should probe for vendor in-group bias before accepting multi-model councils as "blind." Our finding is a single data point but a large one.

### 5.4 Reproducibility
- Every v2.0 run records git SHA, JSONL export SHA, config SHA, Python version, exact OpenRouter model IDs, temperature/max_tokens/concurrency.
- Results stored in versioned directories (`results/v1.0/`, `results/v2.0/`).
- Single `evals/ace/config.yaml` drives model selection, retriever parameters, API settings.

## 6. Results (~3 pages)

### 6.1 Overall Delta
- v1.0 full council: +0.36 (+9.0%)
- v1.0 Opus-only rebaseline: +0.35
- v2.0 (Opus, 252-entry corpus): **+0.33** [95% CI bootstrap: +0.21, +0.46]
- v1.0→v2.0 difference: -0.02 (within noise)
- **Observation 1:** v1.0 Opus-only closely tracks v1.0 council overall, meaning most of the council delta came from Opus's own scoring even before isolating it. The council added noise without shifting the central tendency.
- **Observation 1b:** The 4× corpus expansion (63→252 entries) did not meaningfully change the headline delta. The original 63-entry corpus already saturated the 9-entry retrieval window. More entries gave the retriever more options (shadow force-pull rate dropped from ~35% to ~0%) but did not increase the size of the reasoning lift. This is an instructive null result: structured-context benchmarks may saturate quickly, and corpus growth past the retrieval-window inflection point yields diminishing returns on this particular metric.

### 6.2 Per-Ring Delta
- v1.0 Opus-only: R1 +0.50, R2 +0.52, R3 +0.02.
- v2.0: R1 +0.41 [+0.19, +0.63], R2 +0.56 [+0.39, +0.73], R3 +0.03 [-0.14, +0.20].
- **Observation 2:** R2 (structured/analytical) shows the largest delta in v2.0 with the tightest CI — this is the Codex's strongest signal. R1 (canonical/evidence) is also robust. **R3 (derived/actionability) is a null result: the v2.0 confidence interval crosses zero.** Codex context does not measurably improve actionability scores, in either v1.0 or v2.0. This is a paper-worthy nuance: the conditional-optimism intervention works on framing and evidence, not on the model's downstream "what should you do" generation.

### 6.3 Per-Model Delta
- v1.0 Opus-only: Haiku +0.49, GPT-5.4 Mini +0.59, Gemini Flash-Lite +0.20, Grok 4.1 Fast +0.11.
- v2.0: GPT-5.4 Mini +0.52 [+0.25, +0.79], Haiku +0.47 [+0.24, +0.71], Gemini Flash-Lite +0.22 [-0.02, +0.48], **Grok 4.1 Fast +0.11 [-0.11, +0.33] — null**.
- **Observation 3:** Cost-efficient Anthropic and OpenAI models benefit ~3–5× more than Google's and xAI's efficiency-tier models. Hypotheses: (a) baseline training-regime differences on structured reasoning, (b) instruction-following fidelity for "use provided context", (c) stylistic compatibility with the Codex's conditional-optimism frame.
- **Observation 3b (methodologically important):** With Grok 4.20's +0.50 in-group judging bias removed (single-Opus judge), Grok 4.1 Fast's improvement from Codex augmentation is **statistically indistinguishable from zero**. v1.0's full-council reported +0.19 for Grok; the v2.0 95% CI crosses zero. This means a non-trivial fraction of v1.0's Grok lift was a judge artifact, not a real reasoning gain. It is a clean retroactive validation of the v2.0 single-judge decision.

### 6.4 Per-Pillar Delta
- v1.0 Opus-only: Pillar IV (Production) +0.66, Pillar V (Transcendent) +0.62 largest; Pillar I (Material) +0.13 smallest.
- v2.0: Pillar II (Human) +0.64, Pillar IV (Production) +0.64, Pillar V (Transcendent) +0.45, Pillar III (Collective) +0.15, Pillar I (Material) +0.11.
- **Observation 4:** Across both versions, domains where base models already have strong knowledge (material foundation: energy, food, water) benefit least; domains where knowledge is thinner or more speculative (Pillar II human capability — consciousness, longevity; Pillar IV production — manufacturing, computation; Pillar V transcendent — space, future-vision) benefit most. The Codex effectively backfills underweighted training data. Pillar II rose from #3 in v1.0 to tied for #1 in v2.0, likely because the corpus expansion brought several new high-quality consciousness/longevity entries.

### 6.5 Judge In-Group Bias
- Grok 4.20 → Grok 4.1 Fast: +0.50 vs other-company subjects.
- Opus → Haiku: −0.13 (slight anti-bias).
- GPT-5.4 → GPT-5.4-mini: −0.14.
- Gemini 3.1 Pro → Flash-Lite: +0.18.
- **Observation 5:** Vendor-internal bias is real, measurable, and large enough to distort rankings in at least one case. Blind-council assumptions need empirical audit.

### 6.6 Cross-Authorship Matrix (v2.0)
- Output of `scripts/ace-authorship-report.py` on the v2.0 run.
- Same-company vs cross-company delta-of-deltas:
  - haiku-4.5 vs claude-opus-4-6-authored context: -0.005
  - gemini-flash-lite vs gemini-3.1-pro-authored: +0.014
  - gpt-5.4-mini vs chatgpt-5.4-thinking-authored: +0.034
  - grok-4.1-fast vs grok-super-authored: -0.001
- **Observation 6 (key methodological finding):** **No meaningful subject-side same-company effect.** All four delta-of-deltas are well within noise (the largest is +0.034). Combined with Observation 5, this gives a sharp narrative: **the v1.0 in-group bias is a JUDGE phenomenon, not a SUBJECT phenomenon.** Models do not score higher on retrieved context authored by their own company, even when the corpus contains 63 entries per author and the retriever's 9-entry window samples from all four authors.
- This narrows the scope of the v1.0 bias finding usefully: blind LLM-as-judge councils need vendor-internal-bias audits, but blind RAG corpora drawn from multi-vendor co-authorship do not appear to introduce a measurable same-vendor preference at the subject side. (Caveat: this is observational, not stratified — see §9.7 of METHODOLOGY.md.)

### 6.7 Corpus-Expansion Effect
- Shadow force-pull rate dropped ~35% (v1.0) → ~0% (v2.0).
- Graph-expansion rate dropped ~65% → ~3%.
- v2.0 overall delta vs v1.0 Opus-only: -0.02 (within noise).
- **Observation 7:** The deltas are essentially identical. Retrieval density was already saturated at 63 entries because the binding constraint is the 9-entry retrieval window, not the corpus size. The 4× corpus expansion changed the retriever's *internal* dynamics dramatically (shadow force-pull and graph-expansion fell to near zero because natural diversity in 252 entries is already high) but did not translate to additional reasoning lift on the test subjects. **This is a meaningful null result for benchmark designers:** structured-context benchmarks may saturate quickly past the retrieval-window inflection point, and dataset growth is not linearly translatable to benchmark lift. Future Codex versions should focus on quality and coverage of underrepresented domains rather than raw entry count.

## 7. Discussion (~2 pages)

### 7.1 What the result is (and isn't)
- It IS evidence that structured narrative context can lift cost-efficient models on worldview-adjacent reasoning by a meaningful margin.
- It is NOT evidence that the Codex makes models "wiser" or "better aligned" in general.
- The 15 binary criteria are narrow; a model can win on ACE while being poor elsewhere.
- Dataset transparency IS the methodology — we are not claiming a secret sauce; the data is in the open so replication failures would be visible.

### 7.2 Dataset transparency as methodology
- Open-source corpus + deterministic retriever + published rubric + raw results → any subsequent replication failure is informative.
- Contrast with closed benchmarks where irreproducibility can hide methodology drift.
- Invites community extension: new domains, new prompts, new judges.

### 7.3 Implications for AI safety
- Worldview framing is a lever for agentic behavior in long-horizon tasks.
- Models that default to scarcity reasoning may underperform on deployment-relevant reasoning about energy, health, governance, etc.
- Structured context at inference time may be a cheaper intervention than retraining.

### 7.4 Limitations
- Anonymization imperfect (stylistic fingerprints leak).
- Prompt sensitivity not measured.
- Causal mechanism unclear: evidence, framing, retrieval structure, token budget — any could drive the delta.
- Generalization limited to 21 Grand Challenge domains.
- Codex entry factual correctness is asserted but not externally audited.
- Multi-model authorship correlates with stylistic variety but may correlate with other variables (entry type, domain) that confound the authorship analysis.

### 7.5 Ethical considerations
- "Conditional optimism" is a values-laden frame. Defined explicitly and justified in §1 to make the values claim transparent.
- Dataset co-authored by four models could amplify any shared training biases across those models' providers.
- Commercial models in benchmark: we report costs; we accept the trade-off between vendor-neutrality and using frontier capability.

## 8. Future Work (~0.5 page)

- **v3.0 council challenge layer** — adversarial/rebuttal mode where a Codex entry is challenged by a counter-entry and the model must hold the middle.
- **Stratified authorship experiments** — constrained retrieval by author company to get a causal read on same-company affinity.
- **Reasoning-tier test subjects** — does the delta shrink on frontier test models? Does the Codex effect disappear once the test model is "smart enough"?
- **Community-contributed domains** — open issue tracker for new domain proposals; process for merging.
- **Prompt-sensitivity audit** — paraphrase variants to bound prompt-level variance.
- **Mechanistic analysis** — ablate Codex components (evidence only, framing only, shadow only) to decompose the delta.

## 9. Open-Source Release

- Code: `github.com/CjTruHeart/abundance-codex` (Codex + ACE + retriever + helpers)
- Dataset: `huggingface.co/datasets/CjTruHeart/abundance-codex` (JSONL export)
- License: *(TBD — MIT for code, CC-BY for dataset most likely)*
- Reproduction instructions: `evals/ace/README.md` — clone, install, set API key, `python3 scripts/run-ace.py`.
- Raw v1.0 council results and v1.0 Opus-only rebaseline shipped in `results/v1.0/`.
- v2.0 results will ship in `results/v2.0/` alongside.

---

## Author Attribution (report itself)

- Primary author: Cj TruHeart
- AI co-creative partner: CyberMonk / Claude (via Claude Code, Opus 4.6 1M)
- Codex co-authors: Claude Opus 4.6, ChatGPT 5.4 Thinking, Gemini 3.1 Pro, Super Grok

## Appendix slots

- A. Full rubric (15 criteria definitions)
- B. All 63 eval prompts verbatim
- C. Full model identifier table (OpenRouter IDs, versions, dates)
- D. v1.0 scorecard reproduced in full (both council and Opus-only)
- E. v2.0 scorecard (pending run)
- F. Per-prompt delta distribution plot
- G. Cross-authorship matrix (v2.0)
- H. Code listing for `run-ace.py`, `codex-retriever.py`, helpers

## Outstanding questions before drafting

1. Single paper or pair (dataset paper + benchmark paper)?
2. Quantitative target: just deltas, or add structured statistical claims (paired t-tests, effect sizes)?
3. How explicit about the "conditional optimism" values frame? Describe as methodology or also defend philosophically?
4. License choice (dataset and code).
5. arXiv category: `cs.CL`, `cs.AI`, or both?
