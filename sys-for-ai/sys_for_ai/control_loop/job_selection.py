"""AgentJob selection for /continue."""

from __future__ import annotations

from pathlib import Path

from ..registry_io import read_registry_rows, resolve_registered_path
from ..yaml_io import load_yaml
from .director import load_active_director_decision, load_director_decision
from .handoff import load_handoff_by_id, next_agentjob_from_handoff
from .model import AgentJobRecord, JobSelection, ProgramState


def load_agentjob(agentjob_id: str, root: str | Path = ".") -> AgentJobRecord | None:
    """Load an AgentJob by ID from the operational registry."""

    base = Path(root)
    for row in read_registry_rows(base / "registries/agentjob_registry.csv"):
        if row.get("agentjob_id") != agentjob_id:
            continue
        path = resolve_registered_path(row.get("path", ""), base)
        data = load_yaml(path)
        role_id = row.get("role_id") or data.get("role_binding", {}).get("role_id", "")
        return AgentJobRecord(
            agentjob_id=agentjob_id,
            path=path,
            status=row.get("status", ""),
            role_id=role_id,
            raw=data,
            registry_row=row,
        )
    return None


def active_agentjobs(root: str | Path = ".") -> list[AgentJobRecord]:
    """Return active AgentJobs."""

    base = Path(root)
    records: list[AgentJobRecord] = []
    for row in read_registry_rows(base / "registries/agentjob_registry.csv"):
        if row.get("status") != "active":
            continue
        loaded = load_agentjob(row.get("agentjob_id", ""), base)
        if loaded is not None:
            records.append(loaded)
    return records


def select_or_reuse_one_agentjob(state: ProgramState, root: str | Path = ".") -> JobSelection:
    """Select exactly one AgentJob or return a blocking selection result."""

    base = Path(root)
    active = active_agentjobs(base)
    if len(active) > 1:
        return JobSelection(
            kind="conflict",
            reason="multiple_active_agentjobs",
            evidence=[{"agentjob_id": item.agentjob_id, "status": item.status} for item in active],
        )
    if state.active_agentjob_id:
        job = load_agentjob(state.active_agentjob_id, base)
        if job is None:
            return JobSelection(kind="conflict", reason="active_agentjob_missing")
        return JobSelection(kind="selected", reason="program_state_active_agentjob", agentjob=job)
    if len(active) == 1:
        return JobSelection(kind="selected", reason="single_active_agentjob", agentjob=active[0])

    if state.latest_handoff_id:
        handoff = load_handoff_by_id(state.latest_handoff_id, base)
        next_agentjob_id = next_agentjob_from_handoff(handoff)
        if next_agentjob_id:
            job = load_agentjob(next_agentjob_id, base)
            if job and job.status == "pending":
                return JobSelection(kind="selected", reason="latest_handoff_next_agentjob", agentjob=job)

    decision = None
    if state.active_director_decision_id:
        decision = load_director_decision(state.active_director_decision_id, base)
    if decision is None:
        decision = load_active_director_decision(base)
    if decision and decision.selected_agentjob_id:
        job = load_agentjob(decision.selected_agentjob_id, base)
        if job and job.status in {"pending", "active"}:
            return JobSelection(kind="selected", reason="active_director_decision", agentjob=job)
        return JobSelection(kind="director_decision_required", reason="director_decision_agentjob_missing")

    return JobSelection(
        kind="director_decision_required",
        reason="No active AgentJob and no active Director decision authorizes creation.",
        evidence=[{"required_record_type": "director_decision"}],
    )
