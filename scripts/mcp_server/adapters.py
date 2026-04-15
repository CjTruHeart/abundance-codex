"""Serialize DojoRetriever data classes to JSON-safe dicts.

Pydantic models are intentionally not used here — the goal is to mirror the
exact JSON shape of ``codex-query.py --format json`` so the parity test can
diff bit-for-bit. The MCP tools then return these dicts, and FastMCP infers a
schema from the function's TypedDict / dict[str, Any] return annotation.
"""
from __future__ import annotations

from typing import Any

from ._loader import (
    CodexEntry,
    ExtractedEntry,
    RetrievalResult,
    ScoredDomain,
)


def entry_to_dict(entry: CodexEntry, include_full_content: bool = True) -> dict[str, Any]:
    """Serialize a CodexEntry. ``include_full_content=False`` strips the heavy sections."""
    base: dict[str, Any] = {
        "id": entry.id,
        "entry_type": entry.entry_type,
        "domain": entry.domain,
        "status": entry.status,
        "version": entry.version,
        "confidence": entry.confidence,
        "codex_version": entry.codex_version,
        "co_author_model": entry.co_author_model,
        "co_author_human": entry.co_author_human,
        "co_creative_partner": entry.co_creative_partner,
        "tags": list(entry.tags),
        "one_line_essence": entry.one_line_essence,
        "source_file": entry.source_file,
        "token_estimate": entry.token_estimate,
        "created": entry.created,
        "updated": entry.updated,
    }
    if include_full_content:
        base.update(
            {
                "shift_arc": dict(entry.shift_arc),
                "council": dict(entry.council),
                "evidence_anchors": [dict(ea) for ea in entry.evidence_anchors],
                "shadow_check": dict(entry.shadow_check),
                "six_d_position": dict(entry.six_d_position),
                "connections": dict(entry.connections),
                "conditional_optimism": dict(entry.conditional_optimism),
                "practice_hook": dict(entry.practice_hook),
                "reasoning_scaffold": dict(entry.reasoning_scaffold),
                "governance": dict(entry.governance),
                "domain_connections": [dict(dc) for dc in entry.domain_connections],
            }
        )
    return base


def domain_to_dict(scored: ScoredDomain) -> dict[str, Any]:
    return {
        "domain": scored.domain,
        "confidence": scored.confidence,
        "primary": scored.primary,
    }


def extracted_entry_summary(extracted: ExtractedEntry) -> dict[str, Any]:
    """Match the per-entry shape produced by ``codex-query.py --format json``."""
    return {
        "id": extracted.entry.id,
        "entry_type": extracted.entry.entry_type,
        "domain": extracted.entry.domain,
        "score": round(extracted.score, 4),
        "source": extracted.source,
        "tier": extracted.tier.value,
        "passage_length": len(extracted.passage),
    }


def retrieval_result_to_parity_dict(result: RetrievalResult) -> dict[str, Any]:
    """Bit-identical match for ``codex-retriever.py --retrieve --format json`` output.

    This is the contract the parity test enforces. Do not add or rename fields.
    """
    return {
        "intent": result.intent.value,
        "domains": [domain_to_dict(d) for d in result.domains],
        "token_estimate": result.token_estimate,
        "metadata": result.metadata,
        "entries": [extracted_entry_summary(ex) for ex in result.entries],
    }


def retrieval_result_to_full_dict(result: RetrievalResult) -> dict[str, Any]:
    """Richer return for the MCP ``retrieve_context`` tool.

    Includes the parity-shape fields *plus* the assembled markdown context and
    each entry's extracted passage text — which is what the agent actually needs
    in order to reason. The parity dict is embedded as ``parity_view`` so the
    test can diff without recomputing.
    """
    parity = retrieval_result_to_parity_dict(result)
    return {
        **parity,
        "context_markdown": result.context,
        "entries_full": [
            {
                **extracted_entry_summary(ex),
                "passage": ex.passage,
                "one_line_essence": ex.entry.one_line_essence,
                "confidence": ex.entry.confidence,
            }
            for ex in result.entries
        ],
        "parity_view": parity,
    }
