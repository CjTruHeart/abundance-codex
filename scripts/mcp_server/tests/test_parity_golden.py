"""Golden-file parity test (Dr. Oyelaran's non-negotiable).

Asserts the MCP ``retrieve_context`` tool returns JSON bit-identical to
``scripts/codex-retriever.py --retrieve <query> --format json`` for the same
inputs. If this fails, the MCP layer has introduced silent retrieval drift
and any benchmark numbers measured through it are no longer comparable to
the upstream ACE results.

Run with:
    cd <repo> && .venv/bin/python -m pytest scripts/mcp_server/tests/test_parity_golden.py -v
"""
from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RETRIEVER = REPO_ROOT / "scripts" / "codex-retriever.py"

# Three queries chosen to exercise different intents and the reasoning slot.
PARITY_CASES = [
    {
        "query": "What evidence exists that solar energy costs are declining?",
        "max_entries": 6,
        "domain": None,
        "ring": None,
    },
    {
        "query": "What should governments prioritize first to scale clean energy?",
        "max_entries": 9,
        "domain": None,
        "ring": None,
    },
    {
        "query": "Where does food security stand?",
        "max_entries": 7,
        "domain": "food",
        "ring": 2,
    },
]


def _run_cli(query: str, max_entries: int, domain: str | None, ring: int | None) -> dict:
    cmd = [
        sys.executable,
        str(RETRIEVER),
        "--retrieve",
        query,
        "--format",
        "json",
        "--max-entries",
        str(max_entries),
    ]
    if domain:
        cmd += ["--domain", domain]
    if ring is not None:
        cmd += ["--ring", str(ring)]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def _run_mcp(server, query: str, max_entries: int, domain: str | None, ring: int | None) -> dict:
    result = asyncio.run(
        server.call_tool(
            "retrieve_context",
            {
                "query": query,
                "domain": domain,
                "ring": ring,
                "max_entries": max_entries,
            },
        )
    )
    payload = result.data if getattr(result, "data", None) is not None else result.structured_content
    return payload["parity_view"]


@pytest.fixture(scope="module")
def server():
    from scripts.mcp_server.server import build_server

    return build_server()


@pytest.mark.parametrize("case", PARITY_CASES, ids=lambda c: c["query"][:40])
def test_parity(server, case):
    cli_json = _run_cli(case["query"], case["max_entries"], case["domain"], case["ring"])
    mcp_json = _run_mcp(server, case["query"], case["max_entries"], case["domain"], case["ring"])

    # Top-level keys must match exactly
    assert set(cli_json.keys()) == set(mcp_json.keys()), (
        f"key mismatch: cli={set(cli_json.keys())} mcp={set(mcp_json.keys())}"
    )

    # Bit-identical comparison via canonical JSON
    cli_canonical = json.dumps(cli_json, sort_keys=True, ensure_ascii=False)
    mcp_canonical = json.dumps(mcp_json, sort_keys=True, ensure_ascii=False)
    assert cli_canonical == mcp_canonical, (
        f"\nCLI:\n{cli_canonical[:500]}\n\nMCP:\n{mcp_canonical[:500]}"
    )
