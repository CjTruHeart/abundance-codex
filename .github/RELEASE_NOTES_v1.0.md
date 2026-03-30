# Abundance Codex v1.0

The first complete release of the Abundance Codex — an open-source narrative dataset
that measurably improves AI reasoning quality.

## What's Included

**Dataset**
- 63 entries across 21 Grand Challenge domains
- 5 pillars: Material Foundation, Human Capability, Collective Coordination,
  Production & Discovery, Transcendent Frontier
- 11 entry types including origin stories, breakthroughs, trendlines, shadows,
  and false dawns
- 8 systemic shadow entries functioning as the dataset's immune system
- Gold Standard Format v1.1 with YAML frontmatter, Shift Arc, Five Council Voices,
  Evidence Anchors, Shadow Check, 6D Position, and Conditional Optimism

**Tooling**
- `validate-entry.py` — 4-layer validation
- `export-to-jsonl.py` — JSONL export (Ring 3)
- `codex-retriever.py` — Dojo Retriever v1.0 (intent-aware, type-diverse RAG)
- `run-ace.py` — ACE benchmark harness (63 prompts, multi-model, council-judged)

**Benchmark Results (ACE v1.0)**
- Overall: +9.0% improvement (baseline 3.99/5 → augmented 4.35/5)
- 2,016 judgments: 63 prompts × 4 test models × 2 conditions × 4 judges
- GPT-5.4 mini: +15.4% | Claude Haiku 4.5: +14.5%
- Zero model self-evaluation. Anonymized cross-company judging.
- Largest gains in domains where baseline knowledge is weakest

**Architecture**
- Three-Ring model: Canonical Core → Structured Metadata → Derived Exports
- Dojo Retriever: intent classification → domain retrieval → type coverage
  enforcement → passage extraction → strategic ordering
- Cross-domain connection graph: 286 edges across 21 domains

## Quick Start

```bash
# Read an entry
open domains/01-energy/01-the-solar-revolution.md

# Validate all entries
python3 scripts/validate-entry.py domains/

# Export to JSONL
python3 scripts/export-to-jsonl.py

# Run the benchmark
python3 scripts/run-ace.py --dry-run
```

## Attribution

Co-created by Cj TruHeart, Claude Opus 4.6, and CyberMonk.

Licensed under MIT.
