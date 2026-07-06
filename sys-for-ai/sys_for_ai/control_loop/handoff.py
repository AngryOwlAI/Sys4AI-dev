"""Handoff helpers for /continue."""

from __future__ import annotations

from pathlib import Path

from ..registry_io import read_registry_rows, resolve_registered_path
from ..yaml_io import load_yaml


def load_handoff_by_id(handoff_id: str, root: str | Path = ".") -> dict[str, object] | None:
    """Load an operational handoff by ID."""

    path = load_handoff_path(handoff_id, root)
    if path is not None:
        return load_yaml(path)
    return None


def load_handoff_path(handoff_id: str, root: str | Path = ".") -> Path | None:
    """Resolve an operational handoff path by ID."""

    base = Path(root)
    for row in read_registry_rows(base / "registries/handoff_registry.csv"):
        if row.get("handoff_id") != handoff_id:
            continue
        return resolve_registered_path(row.get("path", ""), base)
    fallback = base / "control_records/handoffs" / f"{handoff_id}.yaml"
    if fallback.exists():
        return fallback
    return None


def next_agentjob_from_handoff(handoff: dict[str, object] | None) -> str | None:
    """Extract a next AgentJob id from a handoff object."""

    if not handoff:
        return None
    value = handoff.get("next_agentjob_id")
    if isinstance(value, str) and value:
        return value
    control_notes = handoff.get("control_loop_notes")
    if isinstance(control_notes, dict):
        value = control_notes.get("next_agentjob_id")
        if isinstance(value, str) and value:
            return value
    return None
