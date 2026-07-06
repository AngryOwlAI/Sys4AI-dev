"""Director decision loading."""

from __future__ import annotations

from pathlib import Path

from ..registry_io import read_registry_rows, resolve_registered_path
from ..yaml_io import load_yaml
from .model import DirectorDecisionRecord


def load_director_decision(decision_id: str, root: str | Path = ".") -> DirectorDecisionRecord | None:
    """Load a Director Decision Record by ID."""

    base = Path(root)
    for row in read_registry_rows(base / "registries/director_decision_registry.csv"):
        if row.get("director_decision_id") != decision_id:
            continue
        path = resolve_registered_path(row.get("path", ""), base)
        data = load_yaml(path)
        selected_agentjob_id = row.get("selected_agentjob_id") or data.get("selected_route", {}).get("creates_agentjob_id")
        return DirectorDecisionRecord(
            director_decision_id=decision_id,
            path=path,
            status=row.get("status", ""),
            selected_agentjob_id=selected_agentjob_id,
            raw=data,
            registry_row=row,
        )
    return None


def load_active_director_decision(root: str | Path = ".") -> DirectorDecisionRecord | None:
    """Load the first active Director decision, if any."""

    base = Path(root)
    for row in read_registry_rows(base / "registries/director_decision_registry.csv"):
        if row.get("status") != "active":
            continue
        decision_id = row.get("director_decision_id", "")
        if decision_id:
            return load_director_decision(decision_id, root=base)
    return None
