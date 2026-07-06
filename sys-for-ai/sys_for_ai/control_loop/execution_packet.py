"""Execution packet generation for /continue."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..memory import run_memory_preflight
from ..validators import validate_agentjob, validate_program_state
from .job_selection import select_or_reuse_one_agentjob
from .model import selection_to_dict
from .state import load_program_state, program_state_to_dict


def continue_status(root: str | Path = ".") -> dict[str, object]:
    """Return current /continue status."""

    state = load_program_state(root)
    result = validate_program_state(Path(root) / "control_records/program_state.yaml")
    return {
        "ok": result.ok,
        "packet_type": "continue_status",
        "status": "READY" if result.ok else "BLOCKED",
        "program_state": program_state_to_dict(state),
        "validation_messages": result.messages,
    }


def continue_preflight(root: str | Path = ".") -> dict[str, object]:
    """Run memory preflight from current program state."""

    state = load_program_state(root)
    payload = run_memory_preflight(
        root=root,
        agentjob_id=state.active_agentjob_id,
        handoff_id=state.latest_handoff_id,
        queries=["source-first memory continue handoff AgentJob"],
    )
    return {
        "ok": bool(payload.get("ok")),
        "packet_type": "continue_preflight",
        "status": payload.get("status"),
        "preflight": payload,
    }


def continue_select(root: str | Path = ".") -> dict[str, object]:
    """Select at most one AgentJob or return a blocking packet."""

    state = load_program_state(root)
    selection = select_or_reuse_one_agentjob(state, root=root)
    if selection.kind == "selected":
        return {
            "ok": True,
            "packet_type": "continue_select",
            **selection_to_dict(selection),
        }
    return {
        "ok": False,
        "packet_type": "director_decision_required" if selection.kind == "director_decision_required" else "stop",
        **selection_to_dict(selection),
    }


def continue_packet(root: str | Path = ".") -> dict[str, object]:
    """Return an execution packet or a blocking packet."""

    state = load_program_state(root)
    preflight = continue_preflight(root)
    if not preflight.get("ok"):
        return {
            "ok": False,
            "packet_type": "stop",
            "status": "BLOCKED",
            "reason": "memory_preflight_failed",
            "evidence": preflight,
        }

    selection = select_or_reuse_one_agentjob(state, root=root)
    if selection.kind != "selected" or selection.agentjob is None:
        return {
            "ok": False,
            "packet_type": "director_decision_required" if selection.kind == "director_decision_required" else "stop",
            "status": "BLOCKED",
            "reason": selection.reason,
            "evidence": selection.evidence or [],
        }

    job_validation = validate_agentjob(selection.agentjob.path)
    if not job_validation.ok:
        return {
            "ok": False,
            "packet_type": "stop",
            "status": "BLOCKED",
            "reason": "agentjob_validation_failed",
            "evidence": job_validation.messages,
        }

    job = selection.agentjob.raw
    receipt = _nested(preflight, "preflight", "receipt")
    return {
        "ok": True,
        "packet_type": "execution_packet",
        "status": "READY",
        "program_state_id": state.program_state_id,
        "agentjob_id": selection.agentjob.agentjob_id,
        "role_id": selection.agentjob.role_id,
        "selection_reason": selection.reason,
        "allowed_reads": job.get("allowed_reads", []),
        "allowed_writes": job.get("allowed_writes", []),
        "generated_paths": job.get("generated_paths", []),
        "forbidden_paths": job.get("forbidden_paths", []),
        "validators": job.get("validators", []),
        "stop_conditions": job.get("stop_conditions", []),
        "memory_preflight_receipt_id": receipt.get("memory_preflight_receipt_id") if isinstance(receipt, dict) else None,
    }


def _nested(payload: dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current
