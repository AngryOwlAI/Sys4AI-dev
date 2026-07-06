"""Control-loop validators."""

from __future__ import annotations

from pathlib import Path

from ..registry_io import read_registry_rows
from ..validators import ValidationResult, validate_director_decisions, validate_program_state
from .execution_packet import continue_packet, continue_select, continue_status


def validate_one_active_agentjob(root: str | Path = ".") -> ValidationResult:
    """Fail when more than one AgentJob is active."""

    base = Path(root)
    active = [
        row.get("agentjob_id", "")
        for row in read_registry_rows(base / "registries/agentjob_registry.csv")
        if row.get("status") == "active"
    ]
    messages: list[str] = []
    if len(active) > 1:
        messages.append(f"multiple active AgentJobs: {', '.join(active)}")
    rows = read_registry_rows(base / "registries/agentjob_registry.csv")
    for row in rows:
        if row.get("status") == "completed" and not row.get("completion_receipt_id"):
            messages.append(f"{row.get('agentjob_id')}: completed AgentJob missing completion_receipt_id")
    return ValidationResult(not messages, messages or ["agentjob_registry.csv: one-active-AgentJob validation passed"])


def validate_control_loop(root: str | Path = ".") -> ValidationResult:
    """Validate the minimal /continue control-loop state."""

    base = Path(root)
    result = ValidationResult(True, [])
    result.extend(validate_program_state(base / "control_records/program_state.yaml"))
    result.extend(validate_director_decisions(base / "control_records/director_decisions"))
    result.extend(validate_one_active_agentjob(base))
    status = continue_status(base)
    selection = continue_select(base)
    packet = continue_packet(base)
    for label, payload in (("continue-status", status), ("continue-select", selection), ("continue-packet", packet)):
        if payload.get("packet_type") == "stop":
            result.ok = False
            result.messages.append(f"{label}: unexpected stop packet: {payload.get('reason')}")
        else:
            result.messages.append(f"{label}: {payload.get('packet_type')} {payload.get('status')}")
    return result
