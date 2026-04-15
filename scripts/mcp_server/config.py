"""Path resolution for the MCP server.

JSONL location is resolved in this order:
1. ``ABUNDANCE_CODEX_JSONL`` environment variable (absolute or relative)
2. ``<repo>/export/abundance-codex.jsonl`` (in-repo default)
"""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_JSONL = REPO_ROOT / "export" / "abundance-codex.jsonl"


def resolve_jsonl_path() -> Path:
    env = os.environ.get("ABUNDANCE_CODEX_JSONL")
    if env:
        p = Path(env).expanduser()
        if not p.is_absolute():
            p = (Path.cwd() / p).resolve()
        return p
    return DEFAULT_JSONL
