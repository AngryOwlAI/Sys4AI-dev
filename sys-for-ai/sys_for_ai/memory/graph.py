"""Small graph helpers for memory catalog relationships."""

from __future__ import annotations

from pathlib import Path

from ..registry_io import read_registry_rows


def load_relationships(root: str | Path = ".") -> list[dict[str, str]]:
    """Load object relationship registry rows if present."""

    path = Path(root) / "registries/object_relationship_registry.csv"
    if not path.exists():
        return []
    return read_registry_rows(path)
