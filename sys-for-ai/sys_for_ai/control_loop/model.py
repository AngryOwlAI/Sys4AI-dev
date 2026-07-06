"""Data models for the /continue control loop."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProgramState:
    program_state_id: str
    active_agentjob_id: str | None
    active_director_decision_id: str | None
    latest_handoff_id: str | None
    state_status: str
    human_gate_required: bool
    raw: dict[str, Any]


@dataclass(frozen=True)
class AgentJobRecord:
    agentjob_id: str
    path: Path
    status: str
    role_id: str
    raw: dict[str, Any]
    registry_row: dict[str, str]


@dataclass(frozen=True)
class DirectorDecisionRecord:
    director_decision_id: str
    path: Path
    status: str
    selected_agentjob_id: str | None
    raw: dict[str, Any]
    registry_row: dict[str, str]


@dataclass(frozen=True)
class JobSelection:
    kind: str
    reason: str
    agentjob: AgentJobRecord | None = None
    evidence: list[dict[str, Any]] | None = None


def selection_to_dict(selection: JobSelection) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "selection_type": selection.kind,
        "reason": selection.reason,
        "agentjob_id": selection.agentjob.agentjob_id if selection.agentjob else None,
        "status": "READY" if selection.kind == "selected" else "BLOCKED",
        "evidence": selection.evidence or [],
    }
    if selection.agentjob:
        payload["role_id"] = selection.agentjob.role_id
        payload["agentjob_status"] = selection.agentjob.status
    return payload
