"""TX-13 semantic checks for the single active generalized trace validator."""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from .registry_io import read_registry_rows, resolve_registered_path
from .toml_io import load_toml
from .validation_semantics import STRUCTURAL_LIMITATION
from .validators import ValidationResult
from .yaml_io import load_yaml


DEFAULT_POLICY_PATH = Path("configs/capability_migration.toml")
GENERATED_PREFIXES = ("Sys4AI/docs/generated/", "docs/generated/")
HOST_PROFILE_MARKERS = (
    "host_profile",
    "host profile",
    "configs/host_profiles/",
    "optional_profile",
    "optional profile",
)
HISTORICAL_MARKERS = ("agentjob", "/continue", "control_loop", "historical")


def validate_generalized_trace_semantics(
    trace_registry: str | Path = "registries/requirement_trace_registry.csv",
    *,
    program_state: str | Path = "control_records/program_state.yaml",
    source_registry: str | Path = "registries/source_registry.csv",
    derivative_registry: str | Path = "registries/derivative_registry.csv",
    policy_path: str | Path = DEFAULT_POLICY_PATH,
) -> ValidationResult:
    """Enforce implementation, profile, state, freshness, and authority invariants."""

    trace_path = resolve_registered_path(str(trace_registry))
    state_path = resolve_registered_path(str(program_state))
    source_path = resolve_registered_path(str(source_registry))
    derivative_path = resolve_registered_path(str(derivative_registry))
    messages: list[str] = []
    try:
        rows = read_registry_rows(trace_path)
        source_rows = read_registry_rows(source_path)
        derivative_rows = read_registry_rows(derivative_path)
        state = load_yaml(state_path)
    except (OSError, RuntimeError) as exc:
        return ValidationResult(False, [str(exc)])
    if not rows or any(row.get("schema_version") != "2.0.0" for row in rows):
        return ValidationResult(False, [f"{trace_path}: TX-13 semantics require generalized 2.0.0 rows"])
    if not isinstance(state, dict):
        return ValidationResult(False, [f"{state_path}: program state must be a mapping"])

    policy, policy_messages = _load_policy(policy_path)
    messages.extend(policy_messages)
    generated_paths = {
        _normalize_path(row.get("path", ""))
        for row in derivative_rows
        if row.get("path")
    }
    source_index = {row.get("source_id", ""): row for row in source_rows if row.get("source_id")}
    source_by_path = {
        _normalize_path(row.get("path", "")): row
        for row in source_rows
        if row.get("path")
    }
    as_of = _program_state_date(state, state_path, messages)
    maximum_age = int(policy.get("max_current_evidence_age_days", 30))

    for index, row in enumerate(rows, start=2):
        trace_id = row.get("trace_id", "")
        label = f"{trace_path}:{index}: {trace_id}"
        implementation = _paths(row.get("implementation_artifacts", ""))
        validation = _paths(row.get("validation_evidence", ""))
        evidence = _paths(row.get("evidence_paths", ""))
        capability = row.get("capability_status")
        verification = row.get("verification_status")

        if capability in {"implemented", "operational"}:
            if not implementation:
                messages.append(f"{label}: implemented capability requires exact implementation paths")
            elif not any(not _is_generated(path, generated_paths) for path in implementation):
                messages.append(f"{label}: generated derivative cannot be the sole implementation authority")
        if capability == "operational":
            if verification != "pass" or row.get("evidence_status") != "current" or not validation:
                messages.append(f"{label}: operational capability requires passing current operational evidence")

        applicability = row.get("applicability_status")
        profile_blob = " ".join(
            str(row.get(field, ""))
            for field in ("implementation_artifacts", "evidence_paths", "semantic_justification", "notes")
        ).casefold()
        if applicability == "optional_profile" and not any(marker in profile_blob for marker in HOST_PROFILE_MARKERS):
            messages.append(f"{label}: optional_profile row must identify its profile boundary")
        if applicability == "required" and capability in {"implemented", "operational"} and implementation:
            if all("host_profiles/" in path for path in implementation):
                messages.append(f"{label}: optional host profile cannot be sole proof of required capability")

        source = source_index.get(row.get("requirement_source_id", ""))
        if source is None:
            messages.append(f"{label}: requirement_source_id is not registered")
        elif source.get("authority_status") in {"derivative_draft", "generated_derivative", "noncanonical"}:
            messages.append(f"{label}: requirement source cannot be a generated or derivative authority")

        for field, paths in (
            ("implementation_artifacts", implementation),
            ("validation_evidence", validation),
            ("evidence_paths", evidence),
        ):
            for path in paths:
                if not resolve_registered_path(path).exists():
                    messages.append(f"{label}: missing {field} path {path}")
        if verification == "pass":
            if not validation:
                messages.append(f"{label}: passing verification requires exact validation evidence")
            elif all(_is_generated(path, generated_paths) for path in validation):
                messages.append(f"{label}: generated derivative cannot be the sole passing validation evidence")
        if row.get("evidence_status") == "current":
            if not evidence:
                messages.append(f"{label}: current evidence requires exact evidence paths")
            elif all(_is_generated(path, generated_paths) for path in evidence):
                messages.append(f"{label}: generated derivative cannot be the sole current source evidence")
            review_date = _parse_date(row.get("semantic_review_date"))
            if as_of is not None and (review_date is None or review_date < as_of - timedelta(days=maximum_age)):
                messages.append(f"{label}: current evidence is stale against the controlled program-state date")

        if capability in {"implemented", "operational"} or verification == "pass":
            current_paths = [*implementation, *validation, *evidence]
            if current_paths and all(
                _is_historical(path, source_by_path) or _is_generated(path, generated_paths)
                for path in current_paths
            ):
                messages.append(f"{label}: historical or generated evidence cannot prove current capability")

    messages.extend(_validate_program_state_alignment(state_path, state))
    if _is_live_policy(trace_path, policy):
        counts = {
            "needs_evidence": Counter(row.get("semantic_review_verdict") for row in rows)["needs_evidence"],
            "planned": Counter(row.get("verification_status") for row in rows)["planned"],
            "operational": Counter(row.get("capability_status") for row in rows)["operational"],
        }
        for name, policy_key in (
            ("needs_evidence", "expected_needs_evidence"),
            ("planned", "expected_planned_verification"),
            ("operational", "expected_operational_capability"),
        ):
            expected = policy.get(policy_key)
            if expected is not None and counts[name] != int(expected):
                messages.append(f"{trace_path}: expected {name}={expected}, found {counts[name]}")

    if messages:
        return ValidationResult(False, sorted(dict.fromkeys(messages)))
    return ValidationResult(
        True,
        [
            f"{trace_path}: TX-13 generalized trace semantics passed "
            f"(implementation paths, optional profiles, program state, freshness, generated authority)",
            STRUCTURAL_LIMITATION,
        ],
    )


def _load_policy(path: str | Path) -> tuple[dict[str, Any], list[str]]:
    target = resolve_registered_path(str(path))
    if not target.exists():
        return {}, []
    try:
        data = load_toml(target)
    except RuntimeError as exc:
        return {}, [str(exc)]
    policy = data.get("trace_validation", {})
    if not isinstance(policy, dict):
        return {}, [f"{target}: [trace_validation] must be a table"]
    return policy, []


def _validate_program_state_alignment(path: Path, state: dict[str, Any]) -> list[str]:
    phase = state.get("current_phase")
    summary = state.get("capability_status_summary")
    summary = summary if isinstance(summary, dict) else {}
    allowed = set(state.get("allowed_next_actions", []))
    blocked = set(state.get("blocked_actions", []))
    validators = set((state.get("validation_status") or {}).get("validators", []))
    messages: list[str] = []
    if state.get("execution_profile_id") != "portable_execution_transaction_v1":
        messages.append(f"{path}: program state must use portable_execution_transaction_v1")
    if state.get("active_execution_transaction_id") is not None:
        messages.append(f"{path}: closeout-ready program state requires no active execution transaction")
    if "make validate-requirement-trace" not in validators:
        messages.append(f"{path}: program state validators omit make validate-requirement-trace")

    if phase == "strategic_baseline_migration_after_TX_12":
        if summary.get("broader_semantic_validation") != "deferred":
            messages.append(f"{path}: pre-TX-13 state must mark broader_semantic_validation deferred")
        if "execute_TX_13_VALIDATORS_only_after_TX_12_shared_baseline" not in allowed:
            messages.append(f"{path}: pre-TX-13 state does not allow the exact TX-13 route")
        if "claim_TX_13_semantic_validation_complete" not in blocked:
            messages.append(f"{path}: pre-TX-13 state must block premature semantic completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX12-001":
            messages.append(f"{path}: pre-TX-13 state is not aligned to the TX-12 handoff")
    elif phase == "strategic_baseline_migration_after_TX_13":
        if summary.get("broader_semantic_validation") != "implemented":
            messages.append(f"{path}: post-TX-13 state must mark broader_semantic_validation implemented")
        if "execute_TX_14_PHASE2_only_after_TX_13_shared_baseline" not in allowed:
            messages.append(f"{path}: post-TX-13 state does not allow the exact TX-14 route")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX13-001":
            messages.append(f"{path}: post-TX-13 state is not aligned to the TX-13 handoff")
    elif phase == "strategic_baseline_migration_after_TX_14":
        if summary.get("broader_semantic_validation") != "implemented":
            messages.append(f"{path}: post-TX-14 state must retain broader_semantic_validation implemented")
        if "execute_TX_15_TARGET_PACKAGE_only_after_TX_14_shared_baseline" not in allowed:
            messages.append(f"{path}: post-TX-14 state does not allow the exact TX-15 route")
        if "begin_TX_16_before_TX_15_closes" not in blocked:
            messages.append(f"{path}: post-TX-14 state must block premature TX-16 work")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX14-001":
            messages.append(f"{path}: post-TX-14 state is not aligned to the TX-14 handoff")
    elif phase == "strategic_baseline_migration_after_TX_15":
        if summary.get("broader_semantic_validation") != "implemented":
            messages.append(f"{path}: post-TX-15 state must retain broader_semantic_validation implemented")
        if "execute_TX_16_WALKING_SKELETON_only_after_TX_15_shared_baseline" not in allowed:
            messages.append(f"{path}: post-TX-15 state does not allow the exact TX-16 route")
        if "begin_TX_17_before_TX_16_closes" not in blocked:
            messages.append(f"{path}: post-TX-15 state must block premature TX-17 work")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX15-001":
            messages.append(f"{path}: post-TX-15 state is not aligned to the TX-15 handoff")
    elif phase == "strategic_baseline_migration_after_TX_16":
        if summary.get("broader_semantic_validation") != "implemented":
            messages.append(f"{path}: post-TX-16 state must retain broader_semantic_validation implemented")
        if "execute_TX_17_SAFETY_EVALUATION_only_after_TX_16_shared_baseline" not in allowed:
            messages.append(f"{path}: post-TX-16 state does not allow the exact TX-17 route")
        if "begin_TX_18_before_TX_17_closes" not in blocked:
            messages.append(f"{path}: post-TX-16 state must block premature TX-18 work")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX16-001":
            messages.append(f"{path}: post-TX-16 state is not aligned to the TX-16 handoff")
    elif phase == "strategic_baseline_migration_after_TX_17":
        if summary.get("broader_semantic_validation") != "implemented":
            messages.append(f"{path}: post-TX-17 state must retain broader_semantic_validation implemented")
        if summary.get("safety_evaluation_controls") != "implemented":
            messages.append(f"{path}: post-TX-17 state must mark safety_evaluation_controls implemented")
        if "execute_TX_18_HUMAN_APPROVAL_only_after_TX_17_shared_baseline" not in allowed:
            messages.append(f"{path}: post-TX-17 state does not allow the exact TX-18 human gate")
        if "begin_TX_19_before_G_08_acceptance" not in blocked:
            messages.append(f"{path}: post-TX-17 state must block premature TX-19 work")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX17-001":
            messages.append(f"{path}: post-TX-17 state is not aligned to the TX-17 handoff")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-17 state must remain human gated")
    elif phase == "strategic_baseline_migration_after_TX_18":
        if summary.get("broader_semantic_validation") != "implemented":
            messages.append(f"{path}: post-TX-18 state must retain broader_semantic_validation implemented")
        if summary.get("safety_evaluation_controls") != "implemented":
            messages.append(f"{path}: post-TX-18 state must retain safety_evaluation_controls implemented")
        if summary.get("strategic_approval") != "accepted_G_08":
            messages.append(f"{path}: post-TX-18 state must mark strategic_approval accepted_G_08")
        if "execute_TX_19_MODULES_only_after_TX_18_shared_baseline" not in allowed:
            messages.append(f"{path}: post-TX-18 state does not allow the exact TX-19 module route")
        if "begin_TX_20_before_TX_19_closes" not in blocked:
            messages.append(f"{path}: post-TX-18 state must block premature TX-20 work")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX18-001":
            messages.append(f"{path}: post-TX-18 state is not aligned to the TX-18 handoff")
        if state.get("state_status") != "active" or state.get("human_gate_required") is not False:
            messages.append(f"{path}: post-TX-18 state must be active with the G-08 human gate closed")
    elif phase == "strategic_baseline_migration_after_TX_19":
        if summary.get("broader_semantic_validation") != "implemented":
            messages.append(f"{path}: post-TX-19 state must retain broader_semantic_validation implemented")
        if summary.get("safety_evaluation_controls") != "implemented":
            messages.append(f"{path}: post-TX-19 state must retain safety_evaluation_controls implemented")
        if summary.get("strategic_approval") != "accepted_G_08":
            messages.append(f"{path}: post-TX-19 state must retain strategic_approval accepted_G_08")
        if "execute_TX_20_GENERATED_DOCS_only_after_TX_19_shared_baseline" not in allowed:
            messages.append(f"{path}: post-TX-19 state does not allow the exact TX-20 generated-docs route")
        if "begin_TX_21_before_TX_20_closes" not in blocked:
            messages.append(f"{path}: post-TX-19 state must block premature TX-21 work")
        if "claim_G_09_complete_before_TX_20_closes" not in blocked:
            messages.append(f"{path}: post-TX-19 state must keep G-09 open until TX-20 closes")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX19-001":
            messages.append(f"{path}: post-TX-19 state is not aligned to the TX-19 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX19-001":
            messages.append(f"{path}: post-TX-19 state is not aligned to the TX-19 handoff")
        if state.get("state_status") != "active" or state.get("human_gate_required") is not False:
            messages.append(f"{path}: post-TX-19 state must remain active without claiming a new human gate")
    elif phase == "strategic_baseline_migration_after_TX_20":
        if summary.get("broader_semantic_validation") != "implemented":
            messages.append(f"{path}: post-TX-20 state must retain broader_semantic_validation implemented")
        if summary.get("strategic_approval") != "accepted_G_08":
            messages.append(f"{path}: post-TX-20 state must retain strategic_approval accepted_G_08")
        if summary.get("derivative_regeneration") != "complete_G_09":
            messages.append(f"{path}: post-TX-20 state must mark derivative_regeneration complete_G_09")
        if "execute_TX_21_FINAL_ACCEPTANCE_only_after_TX_20_shared_baseline" not in allowed:
            messages.append(f"{path}: post-TX-20 state does not allow the exact TX-21 final-acceptance route")
        if "claim_G_10_before_TX_21_acceptance" not in blocked:
            messages.append(f"{path}: post-TX-20 state must block premature G-10 acceptance")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX20-001":
            messages.append(f"{path}: post-TX-20 state is not aligned to the TX-20 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX20-001":
            messages.append(f"{path}: post-TX-20 state is not aligned to the TX-20 handoff")
        if state.get("state_status") != "active" or state.get("human_gate_required") is not False:
            messages.append(f"{path}: post-TX-20 state must remain active without claiming final acceptance")
    else:
        messages.append(f"{path}: unsupported strategic-baseline program phase {phase!r}")
    return messages


def _program_state_date(state: dict[str, Any], path: Path, messages: list[str]) -> date | None:
    validation_status = state.get("validation_status")
    value = validation_status.get("last_validated_at") if isinstance(validation_status, dict) else None
    if not isinstance(value, str):
        messages.append(f"{path}: missing controlled validation date for freshness checks")
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        messages.append(f"{path}: invalid controlled validation date {value!r}")
        return None


def _is_live_policy(trace_path: Path, policy: dict[str, Any]) -> bool:
    value = policy.get("trace_registry_path")
    return bool(value) and resolve_registered_path(str(value)).resolve() == trace_path.resolve()


def _paths(value: str) -> list[str]:
    return [item.strip() for item in str(value).split(";") if item.strip()]


def _normalize_path(value: str) -> str:
    return value.removeprefix("./")


def _is_generated(path: str, registered: set[str]) -> bool:
    normalized = _normalize_path(path)
    return normalized.startswith(GENERATED_PREFIXES) or normalized in registered


def _is_historical(path: str, source_by_path: dict[str, dict[str, str]]) -> bool:
    normalized = _normalize_path(path)
    row = source_by_path.get(normalized)
    if row and row.get("authority_status") == "historical":
        return True
    folded = normalized.casefold()
    return any(marker in folded for marker in HISTORICAL_MARKERS)


def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None
