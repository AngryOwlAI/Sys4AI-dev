"""Memory lookup commands."""

from __future__ import annotations

from pathlib import Path

from .registry_catalog import build_catalog, memory_object_to_dict


def lookup_memory(query: str, root: str | Path = ".") -> dict[str, object]:
    """Lookup a memory object by registry ID or path."""

    catalog = build_catalog(root)
    result = catalog.lookup(query)
    if result is None:
        return {
            "ok": False,
            "query": query,
            "result": None,
            "warnings": catalog.warnings,
        }
    return {
        "ok": True,
        "query": query,
        "result": memory_object_to_dict(result),
        "warnings": catalog.warnings,
    }
