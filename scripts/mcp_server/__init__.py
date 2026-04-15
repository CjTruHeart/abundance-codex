"""Abundance Codex MCP server — exposes DojoRetriever as MCP tools.

Importing submodules lazily so ``python -m scripts.mcp_server.server`` and
``python -m scripts.mcp_server`` both work without RuntimeWarnings.
"""
__all__ = ["build_server", "main"]


def __getattr__(name: str):
    if name in __all__:
        from . import server as _server
        return getattr(_server, name)
    raise AttributeError(name)
