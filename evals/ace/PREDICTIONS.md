# ACE v2.1 Pre-Registered Predictions

> **Filed:** 2026-04-13
> **Author:** Cj TruHeart
> **Context:** Pre-registered before forging 21 council_synthesis entries (domains 01–21)
> **Baseline:** ACE v2.0 results at 252 entries (`ace-20260413-103133.json`)

---

## Intervention

21 `council_synthesis` entries will be added to the Codex (one per domain, 273 total entries). These are meta-entries where four frontier models independently assess each domain's 12 existing entries for collective blind spots, and the human curator synthesizes findings into a Gold Standard Format entry with heavy Practice Hook (400w+) and Builder (400w) sections. The entries are specifically designed to target the R3 (actionability) null result from v2.0.

A Dojo Retriever v1.1 update will reserve one retrieval slot for `council_synthesis` entries on STRATEGIC and ADVERSARIAL intent queries.

---

## Primary Prediction — R3 Actionability

**Prediction:** The council_synthesis layer will move the R3 (Derived/Action) delta from +0.03 to **at least +0.15**, with the 95% bootstrap CI lower bound above zero.

**Rationale:** The v2.0 R3 null is hypothesized to result from a content-format mismatch — existing entries are narrative-and-evidence, not step sequences. Council synthesis entries include explicit numbered action steps in 400w+ Practice Hook sections. If the null persists despite this targeted intervention, the actionability gap is structural (not content-addressable by retrieval augmentation), which is itself a publishable finding.

**Falsification:** If the R3 delta remains below +0.10 or the CI crosses zero, the intervention failed. Report this honestly.

---

## Secondary Prediction — Overall Delta Stability

**Prediction:** The overall delta will remain within ±0.05 of the v2.0 value (+0.33), landing between +0.28 and +0.38.

**Rationale:** The v1.0→v2.0 corpus expansion (63→252 entries) produced no change in overall delta (−0.02), demonstrating retrieval window saturation. Adding 21 entries to 252 should not change the binding constraint. However, if council_synthesis entries are qualitatively different enough to shift retrieval dynamics (because they're preferentially selected for STRATEGIC/ADVERSARIAL queries via the retriever update), a delta outside this range would indicate the entries are architecturally distinct in a measurable way — an interesting finding either direction.

**Falsification:** If the overall delta moves beyond ±0.05, the retrieval window saturation hypothesis needs revision.

---

## Tertiary Prediction — Per-Model Pattern Stability

**Prediction:** The per-model ranking will hold: GPT-5.4 Mini and Haiku will show the largest deltas, Gemini Flash-Lite borderline, Grok 4.1 Fast null or near-null.

**Rationale:** Model receptivity to structured context appears to be a stable property rather than a corpus-size artifact. If Grok suddenly shows a robust delta at 273 entries, it suggests the council_synthesis content addresses a specific gap in Grok's baseline reasoning — worth investigating which domains drive the change.

---

## Evaluation Protocol

- Run ACE v2.1 with identical parameters to v2.0 (single Opus judge, temperature 0.0, max_tokens 2048, concurrency 8)
- Compare R3 delta against primary prediction threshold (+0.15)
- Compare overall delta against secondary prediction range (±0.05 of +0.33)
- Compare per-model deltas against tertiary prediction
- Report all results regardless of outcome
- Cross-reference with v2.0 results JSON for structural consistency
