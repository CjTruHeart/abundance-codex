<!-- Last verified: 2026-04-18, commit a0aeb92 -->

# export/ — JSONL and schema artifacts

This directory contains the generated, machine-readable export of the Abundance Codex. Files here are regenerated from `domains/` via `scripts/export-to-jsonl.py`; do not edit them directly.

| File | Purpose |
|------|---------|
| `abundance-codex.jsonl` | One JSON object per entry (285 lines). Primary consumable for RAG pipelines and downstream training. |
| `abundance-codex-eval-context.json` | Condensed context object used by the ACE benchmark harness. |
| `schema.json` | Human-facing JSON schema reference for entry fields. Canonical machine schema lives at `schema/entry-schema.json`. |

## Dataset card

The authoritative dataset card — description, pillar/domain breakdown, entry type counts, benchmark summary, licensing, and citation — lives in [`huggingface/README.md`](../huggingface/README.md), which is what Hugging Face publishes at [`CjTruHeart/abundance-codex`](https://huggingface.co/datasets/CjTruHeart/abundance-codex).

This folder intentionally does not maintain a parallel dataset card; a single source of truth prevents the two cards from drifting apart.

## License

Dataset content: CC-BY 4.0. Code (including the export scripts): MIT. See `LICENSE` and `LICENSE-CC-BY` in the repo root.

## Regenerating

```bash
python3 scripts/export-to-jsonl.py
python3 scripts/validate-jsonl.py
```

CI runs both on every push.
