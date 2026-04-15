"""FastMCP server exposing the Abundance Codex DojoRetriever as MCP tools.

Five narrow tools (per the council's design):

  - retrieve_context      — full intent→domain→passage pipeline
  - get_entry             — fetch one entry by ID
  - list_domains          — enumerate the 21 domains with counts
  - search_by_domain      — filter entries by domain (and optional type)
  - get_council_synthesis — fetch the meta-analytical council_synthesis for a domain

Stdio transport only (v1).  Run with:
    python -m scripts.mcp_server.server
or via Claude Desktop / Claude Code MCP config.
"""
from __future__ import annotations

import sys
from typing import Any

from fastmcp import FastMCP

from . import adapters
from ._loader import DojoRetriever
from .config import resolve_jsonl_path


# ---------------------------------------------------------------------------
# Lazy retriever singleton
# ---------------------------------------------------------------------------

_retriever: DojoRetriever | None = None


def get_retriever() -> DojoRetriever:
    global _retriever
    if _retriever is None:
        path = resolve_jsonl_path()
        if not path.exists():
            raise FileNotFoundError(
                f"Codex JSONL not found at {path}. "
                f"Set ABUNDANCE_CODEX_JSONL or run scripts/export-to-jsonl.py first."
            )
        # load_codex prints diagnostics to stderr — keep that, it's the only
        # signal a stdio MCP client gets that the server booted cleanly.
        print(f"[mcp_server] Loading codex from {path}", file=sys.stderr)
        _retriever = DojoRetriever(str(path))
    return _retriever


# ---------------------------------------------------------------------------
# Server factory
# ---------------------------------------------------------------------------

def build_server() -> FastMCP:
    mcp = FastMCP(
        name="abundance-codex",
        instructions=(
            "Abundance Codex — a curated knowledge base of 273 evidence-anchored "
            "entries across 21 civilization-scale domains. Use these tools to "
            "retrieve structured context, individual entries, or domain-level "
            "council syntheses. Prefer `retrieve_context` for natural-language "
            "queries; use the targeted tools when you already know the entry "
            "ID, domain, or want to fetch reasoning scaffolds directly."
        ),
    )

    @mcp.tool(
        name="retrieve_context",
        description=(
            "Run the DojoRetriever pipeline on a natural-language query. "
            "Classifies intent (FACTUAL / ANALYTICAL / STRATEGIC / ADVERSARIAL / "
            "NARRATIVE), scores domains by keyword overlap, expands via the "
            "connection graph, enforces type-coverage diversity, and extracts "
            "passages at MINIMAL/CONDENSED/FULL tiers. Returns assembled "
            "markdown context plus per-entry passages and metadata. This is "
            "the primary tool — call it first for any query about abundance, "
            "scarcity, civilization-scale challenges, or future scenarios."
        ),
    )
    def retrieve_context(
        query: str,
        domain: str | None = None,
        ring: int | None = None,
        max_entries: int = 9,
    ) -> dict[str, Any]:
        """Retrieve Codex context for a query.

        Args:
            query: Natural-language question or prompt.
            domain: Optional — force a specific domain (e.g. "energy", "food").
            ring: Optional — force intent ring (1=factual, 2=analytical, 3=strategic).
            max_entries: Maximum entries to return (default 9, matches DojoRetriever).
        """
        retriever = get_retriever()
        result = retriever.retrieve(
            query=query,
            known_domain=domain,
            known_ring=ring,
            max_entries=max_entries,
        )
        return adapters.retrieval_result_to_full_dict(result)

    @mcp.tool(
        name="get_entry",
        description=(
            "Fetch a single Codex entry by its ID (e.g. 'ac-20260404-engy'). "
            "Returns the full structured frontmatter: shift_arc, council voices, "
            "evidence_anchors, shadow_check, conditional_optimism, "
            "reasoning_scaffold, practice_hook, and domain_connections."
        ),
    )
    def get_entry(entry_id: str) -> dict[str, Any]:
        """Look up an entry by ID. Returns the first match if duplicates exist."""
        retriever = get_retriever()
        matches = retriever.index.by_id.get(entry_id, [])
        if not matches:
            return {"error": f"No entry with id={entry_id!r}", "id": entry_id}
        entry = matches[0]
        result: dict[str, Any] = {"entry": adapters.entry_to_dict(entry, include_full_content=True)}
        if len(matches) > 1:
            result["warning"] = (
                f"{len(matches)} entries share id={entry_id!r}; returning the first. "
                f"Domains: {[m.domain for m in matches]}"
            )
        return result

    @mcp.tool(
        name="list_domains",
        description=(
            "Enumerate all 21 civilization-scale domains in the Codex with "
            "entry counts and the count of council_synthesis meta-entries. "
            "Use this to discover the available domain vocabulary before "
            "calling search_by_domain or get_council_synthesis."
        ),
    )
    def list_domains() -> dict[str, Any]:
        """List every domain with entry counts and synthesis availability."""
        retriever = get_retriever()
        idx = retriever.index
        synthesis_domains = {
            e.domain for e in idx.by_type.get("council_synthesis", [])
        }
        domains = []
        for name in sorted(idx.by_domain.keys()):
            entries = idx.by_domain[name]
            domains.append(
                {
                    "domain": name,
                    "entry_count": len(entries),
                    "has_council_synthesis": name in synthesis_domains,
                    "entry_types": sorted({e.entry_type for e in entries}),
                }
            )
        return {
            "total_entries": idx.total_entries,
            "total_domains": len(domains),
            "domains": domains,
        }

    @mcp.tool(
        name="search_by_domain",
        description=(
            "Return all entries in a specific domain, optionally filtered by "
            "entry_type (e.g. 'breakthrough', 'shadow', 'framework', "
            "'council_synthesis'). Use list_domains first if you don't know "
            "the exact domain name."
        ),
    )
    def search_by_domain(
        domain: str,
        entry_type: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        """Filter entries by domain and (optionally) entry_type."""
        retriever = get_retriever()
        entries = retriever.index.by_domain.get(domain, [])
        if not entries:
            available = sorted(retriever.index.by_domain.keys())
            return {
                "error": f"Unknown domain {domain!r}",
                "available_domains": available,
            }
        if entry_type:
            entries = [e for e in entries if e.entry_type == entry_type]
        sliced = entries[:limit]
        return {
            "domain": domain,
            "entry_type_filter": entry_type,
            "total_matched": len(entries),
            "returned": len(sliced),
            "entries": [
                adapters.entry_to_dict(e, include_full_content=False) for e in sliced
            ],
        }

    @mcp.tool(
        name="get_council_synthesis",
        description=(
            "Fetch the council_synthesis meta-entry for a specific domain. "
            "These are the 21 reasoning-scaffold entries that the retriever "
            "reserves for the dedicated 'reasoning slot' on STRATEGIC and "
            "ADVERSARIAL queries. Each contains a Reframe Chain, Contrastive "
            "Pair, Scarcity Trap analysis, and Agent Practice Hook. Call this "
            "directly when you want the meta-analytical layer without running "
            "a full retrieval pipeline."
        ),
    )
    def get_council_synthesis(domain: str) -> dict[str, Any]:
        """Return the council_synthesis entry for a domain."""
        retriever = get_retriever()
        all_synth = retriever.index.by_type.get("council_synthesis", [])
        matches = [e for e in all_synth if e.domain == domain]
        if not matches:
            available = sorted({e.domain for e in all_synth})
            return {
                "error": f"No council_synthesis for domain={domain!r}",
                "available_domains": available,
            }
        return {
            "domain": domain,
            "entry": adapters.entry_to_dict(matches[0], include_full_content=True),
        }

    return mcp


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    server = build_server()
    server.run()  # stdio transport by default


if __name__ == "__main__":
    main()
