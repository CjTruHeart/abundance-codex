"""Import the hyphenated codex-retriever.py module.

The retriever lives one directory up at ``scripts/codex-retriever.py``. The
hyphen makes it impossible to import with a normal ``import`` statement, so we
follow the same importlib pattern that ``scripts/codex-query.py`` already uses.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_RETRIEVER_PATH = Path(__file__).resolve().parent.parent / "codex-retriever.py"

_spec = importlib.util.spec_from_file_location("codex_retriever", _RETRIEVER_PATH)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Could not load spec for {_RETRIEVER_PATH}")

codex_retriever = importlib.util.module_from_spec(_spec)
sys.modules["codex_retriever"] = codex_retriever
_spec.loader.exec_module(codex_retriever)

DojoRetriever = codex_retriever.DojoRetriever
CodexEntry = codex_retriever.CodexEntry
CodexIndex = codex_retriever.CodexIndex
QueryIntent = codex_retriever.QueryIntent
ScoredDomain = codex_retriever.ScoredDomain
ExtractedEntry = codex_retriever.ExtractedEntry
RetrievalResult = codex_retriever.RetrievalResult
load_codex = codex_retriever.load_codex
DOMAIN_DESCRIPTORS = codex_retriever.DOMAIN_DESCRIPTORS
