# Abundance Codex — MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) server that exposes
the [`DojoRetriever`](../codex-retriever.py) as five narrow, typed tools so any
MCP-aware agent (Claude Desktop, Claude Code, Cursor, Zed, custom SDK clients)
can read and reason over the Codex with zero integration work.

Built with [FastMCP](https://github.com/prefecthq/fastmcp) (Python). Stdio
transport. Thin wrapper — all retrieval logic still lives in
`scripts/codex-retriever.py`, so the MCP path stays bit-identical to the CLI
path (enforced by `tests/test_parity_golden.py`).

## Tools

| Tool | What it does |
|---|---|
| `retrieve_context` | Full intent → domain → passage pipeline for a natural-language query. The primary tool. Returns markdown context, per-entry passages, and metadata. |
| `get_entry` | Fetch one entry by ID; returns full structured frontmatter. |
| `list_domains` | Enumerate all 21 domains with entry counts and synthesis availability. |
| `search_by_domain` | Filter entries by domain (and optional `entry_type`). |
| `get_council_synthesis` | Fetch the council_synthesis meta-entry for a domain — direct access to the reasoning slot payload. |

## Install

From the repo root:

```bash
python -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
```

This installs `fastmcp`, `pydantic`, and `pytest` (test deps) alongside the
existing Codex requirements.

## Run

```bash
.venv/bin/python -m scripts.mcp_server
```

The server speaks MCP over stdio. It resolves the JSONL export from, in order:

1. `$ABUNDANCE_CODEX_JSONL` env var (absolute or relative path)
2. `<repo>/export/abundance-codex.jsonl` (default)

Diagnostics print to stderr, leaving stdout clean for the MCP framing.

## Wire it up to Claude Desktop / Claude Code

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`
(macOS) or the equivalent on your platform:

```json
{
  "mcpServers": {
    "abundance-codex": {
      "command": "/absolute/path/to/abundance-codex/.venv/bin/python",
      "args": ["-m", "scripts.mcp_server"],
      "cwd": "/absolute/path/to/abundance-codex",
      "env": {
        "ABUNDANCE_CODEX_JSONL": "/absolute/path/to/abundance-codex/export/abundance-codex.jsonl"
      }
    }
  }
}
```

For Claude Code, add the same block to `.mcp.json` at the project root, or
use `claude mcp add abundance-codex ...`.

## Verify with MCP Inspector

```bash
npx @modelcontextprotocol/inspector \
  /absolute/path/to/abundance-codex/.venv/bin/python -m scripts.mcp_server
```

The Inspector will list the five tools, show their JSON schemas, and let you
fire test calls.

## Tests

```bash
.venv/bin/python -m pytest scripts/mcp_server/tests/ -v
```

- **`test_tools.py`** (13 tests) — exercises each tool against the real export.
- **`test_parity_golden.py`** (3 tests) — runs `codex-retriever.py --format json`
  as a subprocess and asserts the MCP `retrieve_context` tool returns
  bit-identical JSON for the same inputs across FACTUAL, STRATEGIC, and
  forced-domain/ring cases. **This is the non-negotiable invariant**: if it
  fails, the MCP layer has introduced silent retrieval drift and any benchmark
  numbers measured through it are no longer comparable to upstream ACE results.

## Design notes

- **Five narrow tools, not one god-tool.** Tool names alone tell the LLM when
  to call them, which scores better on tool-use evals than a single
  `query_codex` black box.
- **Structured frontmatter is preserved**, not flattened to prose. Confidence
  scores, shadow checks, evidence anchors, and reasoning scaffolds all flow
  through unchanged — that's the whole point of the Codex.
- **The MCP layer is a translator, not a reimplementation.** All retrieval
  logic stays in `codex-retriever.py`; the server only handles transport,
  schema, and serialization.
- **Stdio only for v1.** Streamable HTTP can be layered on later if remote
  hosting becomes worth the operational complexity.
