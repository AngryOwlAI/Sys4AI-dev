"""Structural validation for versioned reference-host capability profiles."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .jsonschema_io import check_schema, load_json, validate_instance
from .registry_io import read_registry_rows, resolve_registered_path
from .security_checks import find_secret_like_values
from .toml_io import load_toml
from .validators import ValidationResult
from .yaml_io import load_yaml


DEFAULT_PROFILE_ROOT = Path("configs/host_profiles")
DEFAULT_SCHEMA_PATH = Path("schemas/contracts/host_capability_profile.schema.json")
DEFAULT_DIRECTOR_DECISION_REGISTRY = Path("registries/director_decision_registry.csv")

REQUIRED_INTERFACE_IDS = (
    "user_interaction",
    "workspace_filesystem",
    "terminal_and_tests",
    "tools_connectors_and_network",
    "sub_agents",
    "task_and_thread_state",
    "memory_and_retrieval",
    "target_runtime",
)

ALLOWED_CAPABILITY_STATES = {
    "verified_available",
    "verified_unavailable",
    "permission_dependent",
    "environment_dependent",
    "unknown",
    "deprecated",
}

NON_EXECUTABLE_CAPABILITY_STATES = {
    "verified_unavailable",
    "permission_dependent",
    "environment_dependent",
    "unknown",
    "deprecated",
}

EXPECTED_PERMISSION_PRECEDENCE = (
    "platform_and_system_constraints",
    "host_permissions",
    "project_authorization",
    "bounded_transaction_permission_envelope",
    "task_objective",
)

PENDING_VERIFICATION_STATE = "draft_pending_G_07"
VERIFIED_VERIFICATION_STATE = "verified_G_07"
PENDING_G07 = "pending_G_07"
PENDING_TX09 = "pending_TX_09"

REQUIRED_INTERFACE_FIELDS = (
    "capability_status",
    "execution_allowed",
    "fallback_mode",
    "host_mechanism",
    "permission_source",
    "source_evidence",
    "evidence_status",
    "evidence_checked_at",
    "evidence_fresh_until",
    "positive_probe",
    "denial_or_absence_probe",
    "degraded_behavior",
    "cancellation_behavior",
    "evidence_capture",
    "known_limitations",
    "review_trigger",
)


def validate_host_capability_profiles(
    root: str | Path = DEFAULT_PROFILE_ROOT,
    schema_path: str | Path = DEFAULT_SCHEMA_PATH,
    director_decision_registry_path: str | Path = DEFAULT_DIRECTOR_DECISION_REGISTRY,
) -> ValidationResult:
    """Validate host profiles structurally without satisfying host gate G-07."""

    profile_root = resolve_registered_path(str(root))
    contract_path = resolve_registered_path(str(schema_path))
    messages: list[str] = []

    if not contract_path.exists():
        return ValidationResult(False, [f"{contract_path}: missing host capability profile schema"])

    try:
        schema = load_json(contract_path)
    except RuntimeError as exc:
        return ValidationResult(False, [str(exc)])

    schema_errors = check_schema(schema)
    if schema_errors:
        return ValidationResult(
            False,
            [f"{contract_path}: invalid JSON Schema: {error}" for error in schema_errors],
        )

    profile_paths = _profile_paths(profile_root)
    if not profile_paths:
        return ValidationResult(False, [f"{profile_root}: no host capability profile TOML files found"])

    for profile_path in profile_paths:
        try:
            data = load_toml(profile_path)
        except RuntimeError as exc:
            messages.append(str(exc))
            continue

        messages.extend(
            f"{profile_path}: schema: {error}"
            for error in validate_instance(data, schema)
        )
        messages.extend(
            f"{profile_path}: {finding}"
            for finding in find_secret_like_values(data)
        )
        messages.extend(
            _validate_profile_invariants(
                profile_path,
                data,
                director_decision_registry_path,
            )
        )

    if messages:
        return ValidationResult(False, messages)

    return ValidationResult(
        True,
        [
            f"{profile_root}: host capability profile structural contract passed; "
            "G-07 remains open and this result does not verify host capability"
        ],
    )


def _profile_paths(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    if not root.exists() or not root.is_dir():
        return []
    return sorted(path for path in root.glob("*.toml") if path.is_file())


def _validate_profile_invariants(
    path: Path,
    data: dict[str, Any],
    director_decision_registry_path: str | Path,
) -> list[str]:
    messages: list[str] = []
    now = datetime.now(timezone.utc)
    profile = data.get("profile")
    if not isinstance(profile, dict):
        return [f"{path}: profile must be a TOML table"]

    verification_state = profile.get("verification_state")
    contract_version = profile.get("portable_execution_contract_version")
    contract_executable = profile.get("portable_execution_contract_executable")

    if profile.get("purpose_authority") is not False:
        messages.append(f"{path}: profile.purpose_authority must be false")
    if profile.get("values_authority") is not False:
        messages.append(f"{path}: profile.values_authority must be false")

    if contract_version == PENDING_TX09 and contract_executable is not False:
        messages.append(
            f"{path}: pending_TX_09 portable execution contract must not be executable"
        )

    messages.extend(_validate_profile_verification(path, profile, now))
    if verification_state == VERIFIED_VERIFICATION_STATE:
        messages.extend(
            _validate_g07_verification_decision(
                path,
                profile.get("verification_decision"),
                director_decision_registry_path,
            )
        )
    messages.extend(_validate_permission_precedence(path, data.get("permission_precedence")))

    interfaces = data.get("interfaces")
    if not isinstance(interfaces, list):
        messages.append(f"{path}: interfaces must be an array of TOML tables")
        return messages

    interface_ids = [
        item.get("interface_id") if isinstance(item, dict) else None
        for item in interfaces
    ]
    duplicates = sorted(
        {
            interface_id
            for interface_id in interface_ids
            if isinstance(interface_id, str) and interface_ids.count(interface_id) > 1
        }
    )
    if duplicates:
        messages.append(f"{path}: duplicate interface IDs: {', '.join(duplicates)}")

    found_ids = {item for item in interface_ids if isinstance(item, str)}
    required_ids = set(REQUIRED_INTERFACE_IDS)
    missing = sorted(required_ids - found_ids)
    unexpected = sorted(found_ids - required_ids)
    if missing:
        messages.append(f"{path}: missing required interface IDs: {', '.join(missing)}")
    if unexpected:
        messages.append(f"{path}: unexpected interface IDs: {', '.join(unexpected)}")
    if len(interfaces) != len(REQUIRED_INTERFACE_IDS):
        messages.append(
            f"{path}: expected exactly {len(REQUIRED_INTERFACE_IDS)} interface entries, "
            f"found {len(interfaces)}"
        )

    for index, interface in enumerate(interfaces):
        label = f"{path}: interfaces[{index}]"
        if not isinstance(interface, dict):
            messages.append(f"{label}: interface entry must be a TOML table")
            continue
        interface_id = interface.get("interface_id")
        if isinstance(interface_id, str) and interface_id:
            label = f"{path}: interface {interface_id}"

        for field in REQUIRED_INTERFACE_FIELDS:
            if field not in interface or not _has_value(interface.get(field)):
                messages.append(f"{label}: missing or empty {field}")

        capability_status = interface.get("capability_status")
        execution_allowed = interface.get("execution_allowed")
        evidence_status = interface.get("evidence_status")

        if capability_status not in ALLOWED_CAPABILITY_STATES:
            messages.append(f"{label}: invalid capability_status {capability_status!r}")

        if verification_state == PENDING_VERIFICATION_STATE:
            if capability_status != "unknown":
                messages.append(
                    f"{label}: {PENDING_VERIFICATION_STATE} requires capability_status 'unknown'"
                )
            if execution_allowed is not False:
                messages.append(
                    f"{label}: {PENDING_VERIFICATION_STATE} must not allow execution"
                )

        if capability_status in NON_EXECUTABLE_CAPABILITY_STATES and execution_allowed is not False:
            messages.append(
                f"{label}: capability_status {capability_status!r} must not allow execution"
            )

        if _is_pending_or_stale_evidence(evidence_status) and execution_allowed is not False:
            messages.append(
                f"{label}: evidence_status {evidence_status!r} must not allow execution"
            )

        if (
            capability_status in {"verified_available", "verified_unavailable"}
            and verification_state != VERIFIED_VERIFICATION_STATE
        ):
            messages.append(
                f"{label}: verified capability requires "
                f"profile.verification_state={VERIFIED_VERIFICATION_STATE!r}"
            )

        if execution_allowed is True:
            if verification_state != VERIFIED_VERIFICATION_STATE:
                messages.append(
                    f"{label}: execution requires "
                    f"profile.verification_state={VERIFIED_VERIFICATION_STATE!r}"
                )
            if contract_version == PENDING_TX09 or _is_pending_value(contract_version):
                messages.append(
                    f"{label}: execution requires a nonpending portable execution contract version"
                )
            if contract_executable is not True:
                messages.append(
                    f"{label}: execution requires "
                    "profile.portable_execution_contract_executable=true"
                )

        if verification_state == VERIFIED_VERIFICATION_STATE or execution_allowed is True:
            messages.extend(
                _validate_current_interface_evidence(
                    label,
                    interface=interface,
                    now=now,
                )
            )
        elif not _is_pending_value(interface.get("evidence_checked_at")):
            checked_at, checked_error = _parse_rfc3339(interface.get("evidence_checked_at"))
            if not checked_error and checked_at is not None and checked_at > now:
                messages.append(f"{label}: evidence_checked_at must not be in the future")

    return messages


def _validate_g07_verification_decision(
    profile_path: Path,
    decision_id: Any,
    registry_path: str | Path,
) -> list[str]:
    messages: list[str] = []
    if not isinstance(decision_id, str) or not decision_id.strip():
        return [f"{profile_path}: verified G-07 profile requires verification_decision"]

    resolved_registry = resolve_registered_path(str(registry_path))
    if not resolved_registry.exists():
        return [
            f"{profile_path}: verification_decision {decision_id!r} cannot be resolved; "
            f"missing {resolved_registry}"
        ]

    try:
        rows = read_registry_rows(resolved_registry)
    except RuntimeError as exc:
        return [f"{profile_path}: cannot read G-07 decision registry: {exc}"]

    matches = [row for row in rows if row.get("director_decision_id") == decision_id]
    if len(matches) != 1:
        return [
            f"{profile_path}: verification_decision {decision_id!r} requires exactly one "
            f"director_decision_registry.csv row; found {len(matches)}"
        ]

    row = matches[0]
    if row.get("status") != "completed":
        messages.append(
            f"{profile_path}: verification_decision {decision_id!r} registry status must be 'completed'"
        )
    if row.get("authority_status") not in {"controlled", "canonical"}:
        messages.append(
            f"{profile_path}: verification_decision {decision_id!r} registry authority_status "
            "must be controlled or canonical"
        )

    decision_path = _resolve_decision_path(row.get("path"), resolved_registry)
    if decision_path is None or not decision_path.exists():
        messages.append(
            f"{profile_path}: verification_decision {decision_id!r} registry path does not exist"
        )
        return messages

    try:
        decision = load_yaml(decision_path)
    except RuntimeError as exc:
        messages.append(f"{profile_path}: cannot load verification_decision {decision_id!r}: {exc}")
        return messages
    if not isinstance(decision, dict):
        messages.append(
            f"{profile_path}: verification_decision {decision_id!r} YAML root must be a mapping"
        )
        return messages

    if decision.get("director_decision_id") != decision_id:
        messages.append(
            f"{profile_path}: verification_decision YAML director_decision_id must match {decision_id!r}"
        )
    if decision.get("decision_status") != "completed":
        messages.append(
            f"{profile_path}: verification_decision {decision_id!r} decision_status must be 'completed'"
        )

    decision_context = decision.get("decision_context")
    if not isinstance(decision_context, dict) or decision_context.get("gate_id") != "G-07":
        messages.append(
            f"{profile_path}: verification_decision {decision_id!r} must bind decision_context.gate_id='G-07'"
        )

    authority_boundary = decision.get("authority_boundary")
    if (
        not isinstance(authority_boundary, dict)
        or authority_boundary.get("accepts_gate_G_07") is not True
    ):
        messages.append(
            f"{profile_path}: verification_decision {decision_id!r} must record "
            "authority_boundary.accepts_gate_G_07=true"
        )

    human_authorization = decision.get("human_authorization")
    if not isinstance(human_authorization, dict):
        messages.append(
            f"{profile_path}: verification_decision {decision_id!r} requires human_authorization"
        )
    else:
        if human_authorization.get("model_self_approval") is not False:
            messages.append(
                f"{profile_path}: verification_decision {decision_id!r} requires "
                "human_authorization.model_self_approval=false"
            )
        if not _has_value(human_authorization.get("approval_evidence")):
            messages.append(
                f"{profile_path}: verification_decision {decision_id!r} requires nonempty "
                "human_authorization.approval_evidence"
            )

    return messages


def _resolve_decision_path(value: Any, registry_path: Path) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate

    registry_root = (
        registry_path.parent.parent
        if registry_path.parent.name == "registries"
        else registry_path.parent
    )
    registry_relative = registry_root / candidate
    if registry_relative.exists():
        return registry_relative
    return resolve_registered_path(value)


def _validate_profile_verification(
    path: Path,
    profile: dict[str, Any],
    now: datetime,
) -> list[str]:
    messages: list[str] = []
    verification_state = profile.get("verification_state")
    verification_decision = profile.get("verification_decision")
    verified_at = profile.get("verified_at")
    verified_by = profile.get("verified_by")

    if verification_state == PENDING_VERIFICATION_STATE:
        if verification_decision != PENDING_G07:
            messages.append(
                f"{path}: pending G-07 profile requires "
                f"profile.verification_decision={PENDING_G07!r}"
            )
        if verified_at != PENDING_G07:
            messages.append(
                f"{path}: pending G-07 profile requires profile.verified_at={PENDING_G07!r}"
            )
        if verified_by != PENDING_G07:
            messages.append(
                f"{path}: pending G-07 profile requires profile.verified_by={PENDING_G07!r}"
            )
        return messages

    if verification_state == VERIFIED_VERIFICATION_STATE:
        if _is_pending_value(verification_decision):
            messages.append(
                f"{path}: verified G-07 profile requires a nonpending verification_decision"
            )
        if _is_pending_value(verified_by):
            messages.append(f"{path}: verified G-07 profile requires a nonpending verifier")

    if not _is_pending_value(verified_at):
        verified_time, verified_error = _parse_rfc3339(verified_at)
        if verified_error:
            messages.append(f"{path}: profile.verified_at {verified_error}")
        elif verified_time is not None and verified_time > now:
            messages.append(f"{path}: profile.verified_at must not be in the future")
    elif verification_state == VERIFIED_VERIFICATION_STATE:
        messages.append(
            f"{path}: verified G-07 profile requires a nonpending RFC3339 profile.verified_at"
        )

    return messages


def _validate_permission_precedence(path: Path, value: Any) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path}: permission_precedence must be a TOML table"]

    order = value.get("order")
    if isinstance(order, str):
        observed = tuple(_normalize_precedence_item(part) for part in order.split("->"))
    elif isinstance(order, list) and all(isinstance(part, str) for part in order):
        observed = tuple(_normalize_precedence_item(part) for part in order)
    else:
        return [f"{path}: permission_precedence.order must be a string or string array"]

    if observed != EXPECTED_PERMISSION_PRECEDENCE:
        expected = " -> ".join(item.replace("_", " ") for item in EXPECTED_PERMISSION_PRECEDENCE)
        return [f"{path}: permission precedence must be exactly: {expected}"]
    return []


def _validate_current_interface_evidence(
    label: str,
    *,
    interface: dict[str, Any],
    now: datetime,
) -> list[str]:
    messages: list[str] = []
    for field in (
        "source_evidence",
        "positive_probe",
        "denial_or_absence_probe",
        "evidence_capture",
    ):
        if _is_pending_value(interface.get(field)):
            messages.append(f"{label}: current G-07 evidence requires nonpending {field}")

    if interface.get("evidence_status") != "current":
        messages.append(f"{label}: verified G-07 profile requires evidence_status 'current'")

    checked_at, checked_error = _parse_rfc3339(interface.get("evidence_checked_at"))
    fresh_until, fresh_error = _parse_rfc3339(interface.get("evidence_fresh_until"))
    if checked_error:
        messages.append(f"{label}: evidence_checked_at {checked_error}")
    if fresh_error:
        messages.append(f"{label}: evidence_fresh_until {fresh_error}")

    if checked_at is not None and checked_at > now:
        messages.append(f"{label}: evidence_checked_at must not be in the future")
    if fresh_until is not None and fresh_until <= now:
        messages.append(f"{label}: verified capability evidence is stale")
    if checked_at is not None and fresh_until is not None and checked_at > fresh_until:
        messages.append(f"{label}: evidence_checked_at must not follow evidence_fresh_until")

    return messages


def _parse_rfc3339(value: Any) -> tuple[datetime | None, str | None]:
    if not isinstance(value, str) or not value.strip():
        return None, "must be a nonempty RFC3339 timestamp"
    if _is_pending_value(value):
        return None, "must be a nonpending RFC3339 timestamp"
    text = value.strip()
    if "T" not in text:
        return None, "must be an RFC3339 timestamp"
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None, "must be an RFC3339 timestamp"
    if parsed.tzinfo is None:
        return None, "must include an RFC3339 timezone offset"
    return parsed.astimezone(timezone.utc), None


def _normalize_precedence_item(value: str) -> str:
    return "_".join(value.strip().casefold().replace("-", " ").split())


def _has_value(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(_has_value(item) for item in value)
    return value is not None


def _is_pending_value(value: Any) -> bool:
    if isinstance(value, list):
        return not value or any(_is_pending_value(item) for item in value)
    if not isinstance(value, str) or not value.strip():
        return True
    normalized = value.strip().casefold().replace("-", "_").replace(" ", "_")
    return "pending" in normalized or normalized in {
        "unknown",
        "unverified",
        "not_run",
        "tbd",
        "tbr",
    }


def _is_pending_or_stale_evidence(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip().casefold().replace("-", "_").replace(" ", "_")
    return normalized == "stale" or normalized.startswith("pending")
