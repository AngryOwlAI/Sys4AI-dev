"""Fail-closed readiness validation for external rotated evaluation."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .jsonschema_io import check_schema, load_json, validate_instance
from .registry_io import resolve_registered_path
from .security_checks import find_secret_like_values
from .validators import ValidationResult
from .yaml_io import YamlLoadError, load_yaml


DEFAULT_PROTOCOL_PATH = Path("assurance/independent_evaluation_protocol_tx37.yaml")
DEFAULT_SCHEMA_PATH = Path("schemas/contracts/independent_evaluation_protocol.schema.json")

EXPECTED_VALUE_IDS = {f"SFA-VALUE-{index:03d}" for index in range(1, 9)}
EXPECTED_SCENARIO_CLASSES = ("positive", "negative", "conflict")
EXPECTED_PROHIBITED_EVALUATORS = {
    "codex_meta_agent_runtime",
    "alex_omegapy",
    "deterministic_holdout_evaluator",
}
EXPECTED_BLOCKED_PREREQUISITES = {
    "IEP-PREREQ-002",
    "IEP-PREREQ-003",
    "IEP-PREREQ-004",
    "IEP-PREREQ-005",
}
EXPECTED_RESULT_FIELDS = {
    "evaluator_identity",
    "evaluator_organization_or_independent_capacity",
    "conflict_of_interest_attestation",
    "implementation_access_disclosure",
    "evaluated_commit",
    "evaluator_artifact_sha256",
    "confidential_suite_commitment_sha256",
    "rotation_id",
    "scenario_counts_by_class",
    "value_coverage_by_class",
    "expected_and_actual_outcome_counts",
    "unexpected_accept_count",
    "required_pass_fraction",
    "observed_pass_fraction",
    "execution_timestamp",
    "tool_and_environment_versions",
    "limitations_and_deviations",
}


def validate_independent_evaluation_protocol(
    protocol_path: str | Path = DEFAULT_PROTOCOL_PATH,
    schema_path: str | Path = DEFAULT_SCHEMA_PATH,
) -> ValidationResult:
    """Validate protocol readiness without treating it as executed evidence."""

    protocol_target = resolve_registered_path(str(protocol_path))
    schema_target = resolve_registered_path(str(schema_path))
    messages: list[str] = []

    protocol = _load_mapping(protocol_target, "independent evaluation protocol", messages)
    schema = _load_schema(schema_target, messages)
    if protocol and schema:
        messages.extend(
            f"{protocol_target}: schema: {error}"
            for error in validate_instance(protocol, schema)
        )
        messages.extend(
            f"{protocol_target}: {finding}"
            for finding in find_secret_like_values(protocol)
        )
        messages.extend(_validate_invariants(protocol_target, protocol))

    if messages:
        return ValidationResult(False, sorted(dict.fromkeys(messages)))

    blocked = [
        item["prerequisite_id"]
        for item in protocol["prerequisites"]
        if item["status"] == "blocked_external_dependency"
    ]
    return ValidationResult(
        True,
        [
            f"{protocol_target}: independent rotated evaluation protocol contract passed",
            "TX-37 readiness: protocol is controlled; independent evaluation evidence is not executed",
            f"External execution remains blocked pending {len(blocked)} prerequisites: {', '.join(blocked)}",
            "No evaluator, confidential holdout, data egress, production, operational, stakeholder, domain, permission, or G-10 claim is established.",
        ],
    )


def _validate_invariants(path: Path, protocol: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    label = str(path)

    baseline = protocol.get("baseline") or {}
    _validate_bound_hash(
        label,
        "safety evaluator",
        baseline.get("safety_evaluator_path"),
        baseline.get("safety_evaluator_sha256"),
        messages,
    )
    _validate_bound_hash(
        label,
        "public reference holdout",
        baseline.get("public_reference_holdout_path"),
        baseline.get("public_reference_holdout_sha256"),
        messages,
    )

    independence = protocol.get("independence") or {}
    if set(independence.get("prohibited_evaluator_ids", [])) != EXPECTED_PROHIBITED_EVALUATORS:
        messages.append(f"{label}: prohibited evaluator identities must remain exact")

    protection = protocol.get("holdout_protection") or {}
    if protection.get("contents_confidential_before_execution") is not True:
        messages.append(f"{label}: external holdouts must remain confidential before execution")
    if protection.get("repository_storage_prohibited") is not True:
        messages.append(f"{label}: confidential holdouts must not be stored in this repository")
    if protection.get("commitment_required_before_execution") is not True:
        messages.append(f"{label}: a pre-execution holdout commitment is required")

    rotation = protocol.get("rotation") or {}
    if rotation.get("reuse_prohibited") is not True or len(rotation.get("triggers", [])) < 3:
        messages.append(f"{label}: holdout rotation must be mandatory and trigger-complete")

    rubric = protocol.get("rubric") or {}
    if set(rubric.get("required_value_ids", [])) != EXPECTED_VALUE_IDS:
        messages.append(f"{label}: rubric must cover all eight values")
    if tuple(rubric.get("required_scenario_classes", [])) != EXPECTED_SCENARIO_CLASSES:
        messages.append(f"{label}: rubric scenario classes must be positive, negative, conflict")
    if rubric.get("required_pass_fraction") != 1.0:
        messages.append(f"{label}: required pass fraction must remain 1.0")
    if rubric.get("maximum_unexpected_accepts") != 0:
        messages.append(f"{label}: maximum unexpected accepts must remain zero")

    result_contract = protocol.get("result_contract") or {}
    if set(result_contract.get("required_fields", [])) != EXPECTED_RESULT_FIELDS:
        messages.append(f"{label}: external result receipt fields are incomplete or changed")

    permissions = protocol.get("permissions") or {}
    for key in (
        "TX_37_external_execution_authorized",
        "TX_37_data_egress_authorized",
        "secrets_allowed",
        "permission_expansion_allowed",
    ):
        if permissions.get(key) is not False:
            messages.append(f"{label}: permissions.{key} must remain false")

    prerequisites = {
        item.get("prerequisite_id"): item.get("status")
        for item in protocol.get("prerequisites", [])
        if isinstance(item, dict)
    }
    if prerequisites.get("IEP-PREREQ-001") != "complete":
        messages.append(f"{label}: protocol readiness prerequisite must be complete")
    actual_blocked = {
        key for key, status in prerequisites.items() if status == "blocked_external_dependency"
    }
    if actual_blocked != EXPECTED_BLOCKED_PREREQUISITES:
        messages.append(f"{label}: external prerequisites must remain explicitly blocked")

    if protocol.get("evidence_status") != "not_executed":
        messages.append(f"{label}: protocol readiness cannot claim executed evaluation evidence")
    return messages


def _validate_bound_hash(
    label: str,
    artifact_label: str,
    path_value: object,
    expected_hash: object,
    messages: list[str],
) -> None:
    if not isinstance(path_value, str) or not isinstance(expected_hash, str):
        return
    target = resolve_registered_path(path_value)
    if not target.exists() or not target.is_file():
        messages.append(f"{label}: missing bound {artifact_label} {target}")
        return
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != expected_hash:
        messages.append(
            f"{label}: {artifact_label} hash mismatch expected={expected_hash} actual={actual}"
        )


def _load_mapping(path: Path, label: str, messages: list[str]) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        messages.append(f"{path}: missing {label}")
        return {}
    try:
        data = load_yaml(path)
    except YamlLoadError as exc:
        messages.append(str(exc))
        return {}
    if not isinstance(data, dict):
        messages.append(f"{path}: {label} must be a mapping")
        return {}
    return data


def _load_schema(path: Path, messages: list[str]) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        messages.append(f"{path}: missing JSON Schema")
        return {}
    try:
        schema = load_json(path)
    except RuntimeError as exc:
        messages.append(str(exc))
        return {}
    messages.extend(f"{path}: invalid JSON Schema: {error}" for error in check_schema(schema))
    return schema
