"""Deterministic AgentJob finalization for the /continue loop."""

from __future__ import annotations

import csv
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any

from ..registry_io import read_registry, resolve_registered_path
from ..validators import _validate_instance_with_schema
from ..yaml_io import dump_yaml, load_yaml
from .handoff import load_handoff_path
from .job_selection import load_agentjob
from .receipts import completion_next_handoff_id, load_completion_receipt

DETERMINISTIC_VALIDATED_AT = "2026-07-06T00:00:00Z"


def finalize_agentjob(completion_path: str | Path, root: str | Path = ".") -> dict[str, Any]:
    """Finalize one AgentJob from a completion receipt.

    The operation is file-backed and deterministic: it validates the receipt,
    verifies the referenced AgentJob and write allowlist, updates continuation
    registries, updates program state, and writes a bounded state snapshot.
    """

    base = Path(root)
    completion_file = _resolve_path(completion_path, base)
    completion = load_completion_receipt(completion_file)
    messages = _validate_completion(completion, completion_file, base)
    if messages:
        return {
            "ok": False,
            "packet_type": "continue_finalize",
            "status": "BLOCKED",
            "completion_path": str(completion_file),
            "messages": messages,
        }

    handoff_id = completion_next_handoff_id(completion)
    if handoff_id:
        handoff_path = load_handoff_path(handoff_id, base)
        if handoff_path is None:
            return {
                "ok": False,
                "packet_type": "continue_finalize",
                "status": "BLOCKED",
                "completion_path": str(completion_file),
                "messages": [f"{completion_file}: next_handoff_id {handoff_id!r} has no registered handoff"],
            }
        handoff_errors = _validate_instance_with_schema(
            load_yaml(handoff_path),
            "schemas/contracts/handoff_v0_2.schema.json",
            str(handoff_path),
        )
        if handoff_errors:
            return {
                "ok": False,
                "packet_type": "continue_finalize",
                "status": "BLOCKED",
                "completion_path": str(completion_file),
                "messages": handoff_errors,
            }

    timestamp = str(completion.get("completed_at") or DETERMINISTIC_VALIDATED_AT)
    _upsert_completion_registry(base, completion_file, completion, handoff_id, timestamp)
    if handoff_id:
        _upsert_handoff_registry(base, handoff_id, completion, timestamp)
    state_snapshot_path = _write_state_snapshot(base, completion, timestamp)
    program_state_path = _update_program_state(base, completion, handoff_id, timestamp)

    return {
        "ok": True,
        "packet_type": "continue_finalize",
        "status": "FINALIZED",
        "completion_receipt_id": completion.get("completion_receipt_id"),
        "agentjob_id": completion.get("agentjob_id"),
        "next_handoff_id": handoff_id,
        "program_state_path": str(program_state_path),
        "state_snapshot_path": str(state_snapshot_path),
        "messages": ["finalization completed"],
    }


def _validate_completion(completion: dict[str, Any], completion_file: Path, root: Path) -> list[str]:
    messages = _validate_instance_with_schema(
        completion,
        "schemas/contracts/completion_receipt_v0_2.schema.json",
        str(completion_file),
    )
    if messages:
        return messages

    agentjob_id = str(completion.get("agentjob_id", ""))
    agentjob = load_agentjob(agentjob_id, root)
    if agentjob is None:
        return [f"{completion_file}: unknown agentjob_id {agentjob_id!r}"]

    role = completion.get("role")
    expected_role = agentjob.role_id
    if expected_role and role != expected_role:
        messages.append(f"{completion_file}: role {role!r} does not match AgentJob role {expected_role!r}")

    changed = completion.get("changed_artifacts", [])
    if not isinstance(changed, list):
        messages.append(f"{completion_file}: changed_artifacts must be a list")
        return messages

    allowed = list(agentjob.raw.get("allowed_writes", [])) + list(agentjob.raw.get("generated_paths", []))
    forbidden = list(agentjob.raw.get("forbidden_paths", []))
    for item in changed:
        if not isinstance(item, dict):
            messages.append(f"{completion_file}: changed_artifacts entries must be mappings")
            continue
        path = str(item.get("path", ""))
        if not path:
            messages.append(f"{completion_file}: changed_artifacts entry missing path")
            continue
        if _matches_any(path, forbidden):
            messages.append(f"{completion_file}: changed artifact {path!r} is forbidden by AgentJob")
        if not _matches_any(path, allowed):
            messages.append(f"{completion_file}: changed artifact {path!r} is outside AgentJob allowed_writes")

    missing_validators = _missing_validator_evidence(completion, list(agentjob.raw.get("validators", [])))
    for command in missing_validators:
        messages.append(f"{completion_file}: declared validator has no passing receipt evidence: {command}")

    return messages


def _missing_validator_evidence(completion: dict[str, Any], validators: list[str]) -> list[str]:
    evidence = completion.get("validation_evidence", {})
    if not isinstance(evidence, dict):
        return validators
    commands = evidence.get("commands_run", [])
    passed = {
        str(item.get("command", ""))
        for item in commands
        if isinstance(item, dict) and str(item.get("result", "")).lower() == "pass"
    }
    return [command for command in validators if command not in passed]


def _matches_any(path: str, patterns: list[str]) -> bool:
    normalized = path.strip().replace("\\", "/")
    candidates = {normalized}
    if normalized.startswith("sys-for-ai/"):
        candidates.add(normalized.removeprefix("sys-for-ai/"))
    else:
        candidates.add(f"sys-for-ai/{normalized}")
    return any(_matches_pattern(candidate, pattern) for candidate in candidates for pattern in patterns)


def _matches_pattern(path: str, pattern: str) -> bool:
    normalized = str(pattern).strip().replace("\\", "/")
    if fnmatchcase(path, normalized):
        return True
    if normalized.endswith("/**"):
        return path.startswith(normalized[:-3] + "/")
    return False


def _update_program_state(root: Path, completion: dict[str, Any], handoff_id: str | None, timestamp: str) -> Path:
    path = root / "control_records/program_state.yaml"
    state = load_yaml(path)
    state["active_agentjob_id"] = None
    state["latest_completion_receipt_id"] = completion.get("completion_receipt_id")
    state["latest_handoff_id"] = handoff_id
    state["latest_memory_preflight_receipt_id"] = completion.get("memory_preflight_receipt_id")
    state["state_status"] = _state_status_from_result(str(completion.get("result", "")))
    state["human_gate_required"] = state["state_status"] == "human_gated"
    state["blocked_reason"] = completion.get("blocked_reason") if state["state_status"] == "blocked" else None
    state["allowed_next_actions"] = [
        "run_memory_preflight",
        "inspect_latest_handoff",
        "select_one_agentjob",
        "emit_execution_packet",
        "validate_completion_receipt",
    ]
    validation = state.setdefault("validation_status", {})
    validation["last_validated_at"] = timestamp
    validators = list(validation.get("validators", []))
    for validator in ("validate-handoffs", "validate-completion-receipts", "validate-state-snapshots"):
        if validator not in validators:
            validators.append(validator)
    validation["validators"] = validators
    dump_yaml(path, state)
    return path


def _state_status_from_result(result: str) -> str:
    if result in {"FAIL", "BLOCKED"}:
        return "blocked"
    if result == "HUMAN_GATED":
        return "human_gated"
    return "active"


def _write_state_snapshot(root: Path, completion: dict[str, Any], timestamp: str) -> Path:
    default_path = root / "control_records/state_snapshots" / f"STATE-{completion.get('completion_receipt_id')}.yaml"
    configured = completion.get("state_snapshot_path")
    path = _resolve_path(configured, root) if isinstance(configured, str) and configured else default_path
    snapshot = {
        "state_snapshot_id": f"STATE-{completion.get('completion_receipt_id')}",
        "snapshot_scope": "completion_finalization",
        "created_by_role": completion.get("role"),
        "current_agentjob_id": completion.get("agentjob_id"),
        "phase": "implementation_initialization",
        "known_registries": [
            "registries/agentjob_registry.csv",
            "registries/completion_receipt_registry.csv",
            "registries/handoff_registry.csv",
            "registries/control_record_registry.csv",
        ],
        "validation_status": {
            "last_validated_at": timestamp,
            "validators": [
                "validate-handoffs",
                "validate-completion-receipts",
                "validate-state-snapshots",
            ],
            "source_completion_receipt_id": completion.get("completion_receipt_id"),
        },
        "next_allowed_actions": [
            "inspect_latest_handoff",
            "run_memory_preflight",
            "select_one_agentjob",
            "emit_execution_packet",
        ],
        "blocked_actions": [
            "execute_multiple_agentjobs",
            "use_chat_memory_as_authority",
            "treat_generated_derivative_as_canonical",
            "mutate_activated_control_record_without_supersession",
        ],
    }
    dump_yaml(path, snapshot)
    return path


def _upsert_completion_registry(root: Path, completion_file: Path, completion: dict[str, Any], handoff_id: str | None, timestamp: str) -> None:
    path = root / "registries/completion_receipt_registry.csv"
    header, rows = _registry(path)
    row = {
        "completion_receipt_id": str(completion.get("completion_receipt_id", "")),
        "path": _registered_path(completion_file, root),
        "agentjob_id": str(completion.get("agentjob_id", "")),
        "result": str(completion.get("result", "")),
        "validation_status": "validated",
        "changed_artifacts_count": str(len(completion.get("changed_artifacts", []))),
        "next_handoff_id": handoff_id or "",
        "source_hash": "pending",
        "last_validated_at": timestamp,
        "notes": "Finalized by continue-finalize",
    }
    _upsert_row(path, header, rows, "completion_receipt_id", row)


def _upsert_handoff_registry(root: Path, handoff_id: str, completion: dict[str, Any], timestamp: str) -> None:
    path = root / "registries/handoff_registry.csv"
    header, rows = _registry(path)
    handoff_path = load_handoff_path(handoff_id, root)
    handoff = load_yaml(handoff_path) if handoff_path else {}
    control_notes = handoff.get("control_loop_notes", {}) if isinstance(handoff, dict) else {}
    row = {
        "handoff_id": handoff_id,
        "path": _registered_path(handoff_path, root) if handoff_path else "",
        "status": "completed",
        "producing_agentjob_id": str(completion.get("agentjob_id", "")),
        "next_recommended_role": str(handoff.get("recommended_next_role", "")) if isinstance(handoff, dict) else "",
        "next_agentjob_id": str(control_notes.get("next_agentjob_id", "")) if isinstance(control_notes, dict) else "",
        "source_ids": "SRC-AJ-SELFHOST-CONTINUE-KERNEL-001",
        "supersedes": "",
        "source_hash": "pending",
        "last_validated_at": timestamp,
        "notes": "Finalized by continue-finalize",
    }
    _upsert_row(path, header, rows, "handoff_id", row)


def _registry(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if path.exists():
        return read_registry(path)
    return [], []


def _upsert_row(path: Path, header: list[str], rows: list[dict[str, str]], id_field: str, row: dict[str, str]) -> None:
    if not header:
        header = list(row)
    updated = False
    for index, existing in enumerate(rows):
        if existing.get(id_field) == row.get(id_field):
            rows[index] = {field: row.get(field, existing.get(field, "")) for field in header}
            updated = True
            break
    if not updated:
        rows.append({field: row.get(field, "") for field in header})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _registered_path(path: Path | None, root: Path) -> str:
    if path is None:
        return ""
    base = root.resolve()
    target = path.resolve()
    try:
        return target.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def _resolve_path(path: str | Path | None, root: Path) -> Path:
    if path is None:
        raise ValueError("missing path")
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    resolved = resolve_registered_path(str(candidate), root)
    if resolved.exists():
        return resolved
    return root / candidate
