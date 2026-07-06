"""Program state loading."""

from __future__ import annotations

from pathlib import Path

from ..yaml_io import load_yaml
from .model import ProgramState


def load_program_state(root: str | Path = ".") -> ProgramState:
    """Load tracked program state from *root*."""

    base = Path(root)
    data = load_yaml(base / "control_records/program_state.yaml")
    return ProgramState(
        program_state_id=str(data.get("program_state_id", "")),
        active_agentjob_id=data.get("active_agentjob_id"),
        active_director_decision_id=data.get("active_director_decision_id"),
        latest_handoff_id=data.get("latest_handoff_id"),
        state_status=str(data.get("state_status", "")),
        human_gate_required=bool(data.get("human_gate_required", False)),
        raw=data,
    )


def program_state_to_dict(state: ProgramState) -> dict[str, object]:
    """Return stable JSON for program state status."""

    return {
        "program_state_id": state.program_state_id,
        "state_status": state.state_status,
        "active_agentjob_id": state.active_agentjob_id,
        "active_director_decision_id": state.active_director_decision_id,
        "latest_handoff_id": state.latest_handoff_id,
        "human_gate_required": state.human_gate_required,
        "current_phase": state.raw.get("current_phase"),
        "allowed_next_actions": state.raw.get("allowed_next_actions", []),
        "blocked_actions": state.raw.get("blocked_actions", []),
    }
