"""Unit tests for the MCP server tools.

These exercise each of the 5 tools end-to-end against the real codex JSONL
(loaded once via the singleton in scripts.mcp_server.server). Run with:

    cd <repo> && .venv/bin/python -m pytest scripts/mcp_server/tests/ -v

We use the real export rather than a fixture because the retriever's intent
classifier and domain identifier are tightly coupled to the actual keyword
distribution, so a 3-entry fixture would test almost nothing useful.
"""
from __future__ import annotations

import asyncio

import pytest

from scripts.mcp_server.server import build_server


@pytest.fixture(scope="module")
def server():
    return build_server()


def call(server, tool_name: str, **kwargs):
    """Invoke a tool by name and return the structured result dict."""
    result = asyncio.run(server.call_tool(tool_name, kwargs))
    # FastMCP returns a ToolResult; the structured payload lives on .data
    # (with .content carrying the text rendering for older clients).
    if hasattr(result, "data") and result.data is not None:
        return result.data
    if hasattr(result, "structured_content") and result.structured_content is not None:
        return result.structured_content
    raise AssertionError(f"Tool {tool_name!r} returned no structured data: {result!r}")


# ---------------------------------------------------------------------------
# list_domains
# ---------------------------------------------------------------------------

def test_list_domains_returns_all_21(server):
    out = call(server, "list_domains")
    assert out["total_domains"] == 21
    assert out["total_entries"] == 273
    names = [d["domain"] for d in out["domains"]]
    assert "energy" in names
    assert "future-vision" in names
    # Every domain should report whether it has a council_synthesis
    for d in out["domains"]:
        assert isinstance(d["has_council_synthesis"], bool)
        assert d["entry_count"] > 0
        assert isinstance(d["entry_types"], list)


def test_list_domains_synthesis_coverage(server):
    out = call(server, "list_domains")
    with_synth = [d for d in out["domains"] if d["has_council_synthesis"]]
    assert len(with_synth) == 21, "all 21 domains should have a council_synthesis"


# ---------------------------------------------------------------------------
# search_by_domain
# ---------------------------------------------------------------------------

def test_search_by_domain_energy(server):
    out = call(server, "search_by_domain", domain="energy")
    assert "error" not in out
    assert out["domain"] == "energy"
    assert out["total_matched"] > 0
    assert all(e["domain"] == "energy" for e in out["entries"])


def test_search_by_domain_with_type_filter(server):
    out = call(server, "search_by_domain", domain="energy", entry_type="shadow")
    assert "error" not in out
    assert all(e["entry_type"] == "shadow" for e in out["entries"])


def test_search_by_domain_unknown(server):
    out = call(server, "search_by_domain", domain="not-a-real-domain")
    assert "error" in out
    assert "available_domains" in out
    assert "energy" in out["available_domains"]


# ---------------------------------------------------------------------------
# get_entry
# ---------------------------------------------------------------------------

def test_get_entry_by_known_id(server):
    # First, find a real ID via search_by_domain to avoid hard-coding
    listing = call(server, "search_by_domain", domain="energy", limit=1)
    real_id = listing["entries"][0]["id"]

    out = call(server, "get_entry", entry_id=real_id)
    assert "error" not in out
    assert out["entry"]["id"] == real_id
    # Frontmatter sections should be present
    assert "council" in out["entry"]
    assert "evidence_anchors" in out["entry"]
    assert "shadow_check" in out["entry"]


def test_get_entry_unknown_id(server):
    out = call(server, "get_entry", entry_id="ac-does-not-exist")
    assert "error" in out
    assert out["id"] == "ac-does-not-exist"


# ---------------------------------------------------------------------------
# get_council_synthesis
# ---------------------------------------------------------------------------

def test_get_council_synthesis_energy(server):
    out = call(server, "get_council_synthesis", domain="energy")
    assert "error" not in out
    assert out["domain"] == "energy"
    assert out["entry"]["entry_type"] == "council_synthesis"
    # The reasoning_scaffold is the whole point of council_synthesis entries
    rs = out["entry"]["reasoning_scaffold"]
    assert rs, "council_synthesis must have a non-empty reasoning_scaffold"


def test_get_council_synthesis_unknown_domain(server):
    out = call(server, "get_council_synthesis", domain="bogus")
    assert "error" in out
    assert "available_domains" in out


# ---------------------------------------------------------------------------
# retrieve_context
# ---------------------------------------------------------------------------

def test_retrieve_context_factual_query(server):
    out = call(
        server,
        "retrieve_context",
        query="What evidence exists that solar energy costs are declining?",
        max_entries=6,
    )
    assert out["intent"] in {"FACTUAL", "ANALYTICAL"}
    assert "energy" in [d["domain"] for d in out["domains"]]
    assert len(out["entries"]) > 0
    assert out["context_markdown"].startswith("# Abundance Codex")
    # Each entry should have a passage
    assert all(e["passage"] for e in out["entries_full"])


def test_retrieve_context_strategic_uses_reasoning_slot(server):
    out = call(
        server,
        "retrieve_context",
        query="What should governments prioritize first to scale clean energy?",
        max_entries=9,
    )
    assert out["intent"] == "STRATEGIC"
    assert out["metadata"]["reasoning_slot_used"] is True
    # A council_synthesis entry should be in the results
    types = {e["entry_type"] for e in out["entries"]}
    assert "council_synthesis" in types


def test_retrieve_context_with_forced_domain_and_ring(server):
    out = call(
        server,
        "retrieve_context",
        query="abundance",
        domain="food",
        ring=2,
        max_entries=5,
    )
    assert out["intent"] == "ANALYTICAL"
    assert out["domains"][0]["domain"] == "food"


def test_retrieve_context_parity_view_subset(server):
    """The parity_view embedded in retrieve_context must match the
    documented JSON contract from codex-retriever.py --format json."""
    out = call(server, "retrieve_context", query="solar energy costs", max_entries=4)
    parity = out["parity_view"]
    expected_keys = {"intent", "domains", "token_estimate", "metadata", "entries"}
    assert set(parity.keys()) == expected_keys
    for e in parity["entries"]:
        assert set(e.keys()) == {
            "id",
            "entry_type",
            "domain",
            "score",
            "source",
            "tier",
            "passage_length",
        }
