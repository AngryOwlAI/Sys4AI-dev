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
    elif phase == "strategic_baseline_migration_TX_21_audit_complete_G_10_deferred":
        if summary.get("broader_semantic_validation") != "implemented":
            messages.append(f"{path}: post-TX-21 deferred state must retain broader_semantic_validation implemented")
        if summary.get("strategic_approval") != "accepted_G_08":
            messages.append(f"{path}: post-TX-21 deferred state must retain strategic_approval accepted_G_08")
        if summary.get("derivative_regeneration") != "complete_G_09":
            messages.append(f"{path}: post-TX-21 deferred state must retain derivative_regeneration complete_G_09")
        if "propose_separately_authorized_G_07_observable_host_verification" not in allowed:
            messages.append(f"{path}: post-TX-21 deferred state must expose the separately authorized G-07 route")
        if "propose_separately_authorized_evidence_closure" not in allowed:
            messages.append(f"{path}: post-TX-21 deferred state must expose the evidence-closure route")
        if "claim_G_10_after_TX_21_audit_without_G_07_and_evidence_closure" not in blocked:
            messages.append(f"{path}: post-TX-21 deferred state must block unsupported G-10 acceptance")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX21-001":
            messages.append(f"{path}: post-TX-21 deferred state is not aligned to the TX-21 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX21-001":
            messages.append(f"{path}: post-TX-21 deferred state is not aligned to the TX-21 handoff")
        if "DDR-SFADEV-STRATEGIC-BASELINE-G10-001" not in set(state.get("current_state_evidence", [])):
            messages.append(f"{path}: post-TX-21 deferred state omits the G-10 disposition evidence")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-21 deferred state must remain blocked with escalation pending")
        if state.get("state_status") != "blocked" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-21 deferred state must remain blocked and human gated")
    elif phase == "strategic_baseline_migration_G_07_accepted_evidence_closure_ready":
        if summary.get("strategic_approval") != "accepted_G_08":
            messages.append(f"{path}: post-G-07 state must retain strategic_approval accepted_G_08")
        if summary.get("derivative_regeneration") != "complete_G_09":
            messages.append(f"{path}: post-G-07 state must retain derivative_regeneration complete_G_09")
        if summary.get("host_verification") != "accepted_G_07_mixed_profile":
            messages.append(f"{path}: post-G-07 state must record the accepted mixed host profile")
        if "execute_TX_23_EVIDENCE_CLOSURE_PLAN_only" not in allowed:
            messages.append(f"{path}: post-G-07 state must expose only the bounded TX-23 evidence-closure planning route")
        if "claim_G_10_after_TX_21_audit_without_G_07_and_evidence_closure" not in blocked:
            messages.append(f"{path}: post-G-07 state must block unsupported G-10 acceptance")
        if "treat_G_07_as_production_operational_target_runtime_or_permission_authority" not in blocked:
            messages.append(f"{path}: post-G-07 state must block host-verification authority expansion")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX22-001":
            messages.append(f"{path}: post-G-07 state is not aligned to the TX-22 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX22-001":
            messages.append(f"{path}: post-G-07 state is not aligned to the TX-22 handoff")
        if "DDR-SFADEV-STRATEGIC-BASELINE-G07-001" not in set(state.get("current_state_evidence", [])):
            messages.append(f"{path}: post-G-07 state omits the accepted G-07 decision evidence")
        if state.get("continuation_state") != "ready" or state.get("escalation_state") != "not_required":
            messages.append(f"{path}: post-G-07 state must be ready without a new authorization escalation")
        if state.get("state_status") != "active" or state.get("human_gate_required") is not False:
            messages.append(f"{path}: post-G-07 state must be active without a new human gate")
    elif phase == "strategic_baseline_migration_TX_23_evidence_closure_planned":
        if summary.get("strategic_approval") != "accepted_G_08":
            messages.append(f"{path}: post-TX-23 state must retain strategic_approval accepted_G_08")
        if summary.get("derivative_regeneration") != "complete_G_09":
            messages.append(f"{path}: post-TX-23 state must retain derivative_regeneration complete_G_09")
        if summary.get("host_verification") != "accepted_G_07_mixed_profile":
            messages.append(f"{path}: post-TX-23 state must retain accepted G-07 mixed host evidence")
        if "seek_accountable_G_11_EVIDENCE_SCOPE_decision" not in allowed:
            messages.append(f"{path}: post-TX-23 state must expose the accountable G-11 evidence-scope gate")
        for required_block in (
            "begin_TX_24_or_later_without_accountable_G_11_route_selection",
            "begin_bulk_evidence_status_mutation_without_G_11_scope_decision",
            "treat_TX_23_classification_as_executed_evidence",
            "approve_evidence_waiver_from_TX_23_candidate_classification",
            "supersede_the_plan_from_TX_23_candidate_classification",
            "claim_G_10_after_TX_21_audit_without_G_07_and_evidence_closure",
            "treat_G_07_as_production_operational_target_runtime_or_permission_authority",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-23 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX23-001":
            messages.append(f"{path}: post-TX-23 state is not aligned to the TX-23 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX23-001":
            messages.append(f"{path}: post-TX-23 state is not aligned to the TX-23 handoff")
        if "TX-23-EVIDENCE-CLOSURE-PLAN" not in set(state.get("current_state_evidence", [])):
            messages.append(f"{path}: post-TX-23 state omits TX-23 transaction evidence")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-23 state must remain blocked with G-11 escalation pending")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-23 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_24_local_semantic_evidence_complete":
        if summary.get("strategic_approval") != "accepted_G_08":
            messages.append(f"{path}: post-TX-24 state must retain strategic_approval accepted_G_08")
        if summary.get("derivative_regeneration") != "complete_G_09":
            messages.append(f"{path}: post-TX-24 state must retain derivative_regeneration complete_G_09")
        if summary.get("host_verification") != "accepted_G_07_mixed_profile":
            messages.append(f"{path}: post-TX-24 state must retain accepted G-07 mixed host evidence")
        if summary.get("semantic_review_evidence") != "accepted_TX_24_7_of_7":
            messages.append(f"{path}: post-TX-24 state must record the seven accepted semantic reviews")
        for required_route in (
            "seek_separate_authorization_for_next_TX_24_local_verification_family",
            "seek_accountable_plan_interpretation_for_410_candidates",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-24 state omits controlled next route {required_route}")
        for required_block in (
            "begin_another_local_evidence_family_without_separate_authorization",
            "begin_bulk_evidence_status_mutation_without_family_evidence",
            "approve_evidence_waiver_from_TX_23_candidate_classification",
            "supersede_the_plan_from_TX_23_candidate_classification",
            "claim_G_10_after_TX_21_audit_without_retained_evidence_closure",
            "claim_production_readiness_or_operational_authority",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-24 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX24-001":
            messages.append(f"{path}: post-TX-24 state is not aligned to the TX-24 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX24-001":
            messages.append(f"{path}: post-TX-24 state is not aligned to the TX-24 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-001",
            "TX-24-LOCAL-EVIDENCE-SEMANTIC-REVIEW",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX24-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-24 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-24 state must stop at a new bounded authorization gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-24 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_25_plan_interpretation_complete":
        if summary.get("strategic_approval") != "accepted_G_08":
            messages.append(f"{path}: post-TX-25 state must retain strategic_approval accepted_G_08")
        if summary.get("derivative_regeneration") != "complete_G_09":
            messages.append(f"{path}: post-TX-25 state must retain derivative_regeneration complete_G_09")
        if summary.get("host_verification") != "accepted_G_07_mixed_profile":
            messages.append(f"{path}: post-TX-25 state must retain accepted G-07 mixed host evidence")
        if summary.get("semantic_review_evidence") != "accepted_TX_24_7_of_7":
            messages.append(f"{path}: post-TX-25 state must retain the seven accepted semantic reviews")
        if summary.get("plan_scope_interpretation") != "accepted_TX_25_410_future_work":
            messages.append(f"{path}: post-TX-25 state must record the exact 410-row future-work interpretation")
        for required_route in (
            "seek_separate_authorization_for_remaining_67_local_verification_obligations",
            "seek_accountable_external_evidence_scope",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-25 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_authorization",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "mutate_trace_state_from_plan_interpretation",
            "claim_G_10_after_TX_25_without_retained_evidence_closure",
            "claim_production_readiness_or_operational_authority",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-25 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX25-001":
            messages.append(f"{path}: post-TX-25 state is not aligned to the TX-25 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX25-001":
            messages.append(f"{path}: post-TX-25 state is not aligned to the TX-25 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-002",
            "TX-25-PLAN-INTERPRETATION",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX25-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-25 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-25 state must stop at a new bounded authorization gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-25 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_26_python_package_verification_complete":
        if summary.get("strategic_approval") != "accepted_G_08":
            messages.append(f"{path}: post-TX-26 state must retain strategic_approval accepted_G_08")
        if summary.get("derivative_regeneration") != "complete_G_09":
            messages.append(f"{path}: post-TX-26 state must retain derivative_regeneration complete_G_09")
        if summary.get("host_verification") != "accepted_G_07_mixed_profile":
            messages.append(f"{path}: post-TX-26 state must retain accepted G-07 mixed host evidence")
        if summary.get("semantic_review_evidence") != "accepted_TX_24_7_of_7":
            messages.append(f"{path}: post-TX-26 state must retain the seven accepted semantic reviews")
        if summary.get("plan_scope_interpretation") != "accepted_TX_25_410_future_work":
            messages.append(f"{path}: post-TX-26 state must retain the exact 410-row future-work interpretation")
        if summary.get("python_package_verification") != "accepted_TX_26_4_of_4":
            messages.append(f"{path}: post-TX-26 state must record the four accepted Python/package verifications")
        for required_route in (
            "seek_separate_authorization_for_remaining_63_local_verification_obligations",
            "seek_accountable_external_evidence_scope",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-26 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_authorization",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "claim_G_10_after_TX_26_without_retained_evidence_closure",
            "claim_production_readiness_or_operational_authority",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-26 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX26-001":
            messages.append(f"{path}: post-TX-26 state is not aligned to the TX-26 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX26-001":
            messages.append(f"{path}: post-TX-26 state is not aligned to the TX-26 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-003",
            "TX-26-LOCAL-EVIDENCE-PYTHON-PACKAGE",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX26-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-26 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-26 state must stop at a new bounded authorization gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-26 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_27_yaml_control_verification_complete":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-27 {field} must be {expected}")
        for required_route in (
            "seek_separate_authorization_for_remaining_52_local_verification_obligations",
            "seek_accountable_external_evidence_scope",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-27 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_authorization",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "claim_G_10_after_TX_27_without_retained_evidence_closure",
            "claim_production_readiness_or_operational_authority",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-27 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX27-001":
            messages.append(f"{path}: post-TX-27 state is not aligned to the TX-27 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX27-001":
            messages.append(f"{path}: post-TX-27 state is not aligned to the TX-27 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-004",
            "TX-27-LOCAL-EVIDENCE-YAML-CONTROL",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX27-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-27 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-27 state must stop at a new bounded authorization gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-27 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_28_format_governance_verification_complete":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-28 {field} must be {expected}")
        for required_route in (
            "seek_separate_authorization_for_remaining_42_local_verification_obligations",
            "seek_accountable_external_evidence_scope",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-28 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_authorization",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "claim_G_10_after_TX_28_without_retained_evidence_closure",
            "claim_production_readiness_or_operational_authority",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-28 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX28-001":
            messages.append(f"{path}: post-TX-28 state is not aligned to the TX-28 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX28-001":
            messages.append(f"{path}: post-TX-28 state is not aligned to the TX-28 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-005",
            "TX-28-LOCAL-EVIDENCE-FORMAT-GOVERNANCE",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX28-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-28 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-28 state must stop at a new bounded authorization gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-28 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_29_csv_registry_verification_complete":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-29 {field} must be {expected}")
        for required_route in (
            "seek_separate_authorization_for_remaining_37_local_verification_obligations",
            "seek_accountable_external_evidence_scope",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-29 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_authorization",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "claim_G_10_after_TX_29_without_retained_evidence_closure",
            "claim_production_readiness_or_operational_authority",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-29 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX29-001":
            messages.append(f"{path}: post-TX-29 state is not aligned to the TX-29 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX29-001":
            messages.append(f"{path}: post-TX-29 state is not aligned to the TX-29 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-006",
            "TX-29-LOCAL-EVIDENCE-CSV-REGISTRY",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX29-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-29 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-29 state must stop at a new bounded authorization gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-29 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_30_markdown_source_verification_complete":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-30 {field} must be {expected}")
        for required_route in (
            "seek_separate_authorization_for_remaining_33_local_verification_obligations",
            "seek_accountable_external_evidence_scope",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-30 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_authorization",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "claim_G_10_after_TX_30_without_retained_evidence_closure",
            "claim_production_readiness_or_operational_authority",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-30 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX30-001":
            messages.append(f"{path}: post-TX-30 state is not aligned to the TX-30 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX30-001":
            messages.append(f"{path}: post-TX-30 state is not aligned to the TX-30 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-007",
            "TX-30-LOCAL-EVIDENCE-MARKDOWN-SOURCE",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX30-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-30 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-30 state must stop at a new bounded authorization gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-30 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_31_toml_config_verification_complete":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-31 {field} must be {expected}")
        for required_route in (
            "seek_separate_authorization_for_remaining_24_local_verification_obligations",
            "execute_authorized_external_evidence_scope_only_through_a_bounded_transaction",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-31 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_transaction_control",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "claim_G_10_after_TX_31_without_retained_evidence_closure",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-31 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX31-001":
            messages.append(f"{path}: post-TX-31 state is not aligned to the TX-31 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX31-001":
            messages.append(f"{path}: post-TX-31 state is not aligned to the TX-31 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-008",
            "TX-31-LOCAL-EVIDENCE-TOML-CONFIG",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX31-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-31 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-31 state must stop at a new bounded transaction gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-31 state must remain human gated for evidence-dependent acceptance")
    elif phase == "strategic_baseline_migration_TX_32_jsonschema_contract_verification_complete":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
            "jsonschema_contract_verification": "accepted_TX_32_10_of_10",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-32 {field} must be {expected}")
        for required_route in (
            "seek_separate_authorization_for_remaining_14_local_verification_obligations",
            "execute_authorized_external_evidence_scope_only_through_a_bounded_transaction",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-32 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_transaction_control",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "claim_G_10_after_TX_32_without_retained_evidence_closure",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-32 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX32-001":
            messages.append(f"{path}: post-TX-32 state is not aligned to the TX-32 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX32-001":
            messages.append(f"{path}: post-TX-32 state is not aligned to the TX-32 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-009",
            "TX-32-LOCAL-EVIDENCE-JSON-SCHEMA",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX32-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-32 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-32 state must stop at a new bounded transaction gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-32 state must remain human gated for evidence-dependent acceptance")
    elif phase == "strategic_baseline_migration_TX_33_generated_reader_verification_complete":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
            "jsonschema_contract_verification": "accepted_TX_32_10_of_10",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-33 {field} must be {expected}")
        for required_route in (
            "select_dependency_ready_retained_external_evidence_transaction",
            "execute_authorized_external_evidence_scope_only_through_a_bounded_transaction",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-33 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_transaction_control",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "claim_G_10_after_TX_33_without_retained_external_evidence_closure",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-33 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX33-001":
            messages.append(f"{path}: post-TX-33 state is not aligned to the TX-33 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX33-001":
            messages.append(f"{path}: post-TX-33 state is not aligned to the TX-33 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-010",
            "TX-33-LOCAL-EVIDENCE-GENERATED-READERS",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX33-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-33 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-33 state must stop at a new bounded external-evidence transaction gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-33 state must remain human gated for evidence-dependent acceptance")
    elif phase == "strategic_baseline_migration_TX_34_cross_version_CI_complete":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
            "jsonschema_contract_verification": "accepted_TX_32_10_of_10",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-34 {field} must be {expected}")
        for required_route in (
            "select_dependency_ready_retained_external_evidence_transaction",
            "execute_authorized_external_evidence_scope_only_through_a_bounded_transaction",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-34 state omits controlled next route {required_route}")
        for required_block in (
            "begin_later_evidence_or_acceptance_work_without_separate_transaction_control",
            "treat_410_future_work_dispositions_as_trace_completion_or_waivers",
            "claim_G_10_after_TX_34_without_remaining_retained_external_evidence_closure",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-34 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX34-001":
            messages.append(f"{path}: post-TX-34 state is not aligned to the TX-34 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX34-001":
            messages.append(f"{path}: post-TX-34 state is not aligned to the TX-34 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-011",
            "TX-34-CROSS-VERSION-PYTHON-CI",
            "GHA-RUN-29197460029-SUCCESS",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX34-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-34 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-34 state must stop at the next bounded external-evidence gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-34 state must remain human gated for evidence-dependent acceptance")
    elif phase == "strategic_baseline_migration_TX_35_quantitative_measurement_pending_human_acceptance":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
            "jsonschema_contract_verification": "accepted_TX_32_10_of_10",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-35 {field} must be {expected}")
        for required_route in (
            "review_TX_35_metric_definitions_thresholds_sources_intervals_results_and_limitations",
            "explicitly_accept_reject_or_revise_TX_35_metric_standard_and_results",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-35 state omits controlled human route {required_route}")
        for required_block in (
            "treat_TX_35_candidate_metrics_as_accepted_without_accountable_human_evidence",
            "claim_user_benefit_stakeholder_domain_production_operational_permission_or_G_10_evidence_from_TX_35_repository_metrics",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-35 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX35-001":
            messages.append(f"{path}: post-TX-35 state is not aligned to the TX-35 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX35-001":
            messages.append(f"{path}: post-TX-35 state is not aligned to the TX-35 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-012",
            "TX-35-QUANTITATIVE-STRATEGIC-EVIDENCE",
            "TX35-MEASUREMENT-REPRODUCED-4-OF-4",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX35-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-35 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-35 state must stop at accountable human acceptance")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-35 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_36_quantitative_measurement_accepted":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
            "jsonschema_contract_verification": "accepted_TX_32_10_of_10",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-36 {field} must be {expected}")
        for required_route in (
            "review_accepted_TX_35_measurement_and_TX_36_acceptance_evidence",
            "select_dependency_ready_retained_external_evidence_transaction",
            "execute_authorized_external_evidence_scope_only_through_a_bounded_transaction",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-36 state omits controlled next route {required_route}")
        for required_block in (
            "mutate_accepted_TX_35_measurement_without_accountable_supersession_and_remeasurement",
            "begin_later_evidence_or_acceptance_work_without_separate_transaction_control",
            "claim_user_benefit_stakeholder_domain_production_operational_permission_or_G_10_evidence_from_TX_35_repository_metrics",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-36 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX36-001":
            messages.append(f"{path}: post-TX-36 state is not aligned to the TX-36 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX36-001":
            messages.append(f"{path}: post-TX-36 state is not aligned to the TX-36 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-013",
            "TX-36-QUANTITATIVE-STRATEGIC-EVIDENCE-ACCEPTANCE",
            "TX36-TX35-MEASUREMENT-ACCEPTED-4-OF-4",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX36-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-36 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-36 state must stop at the next accountable evidence-scope gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-36 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_37_independent_evaluation_protocol_ready":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
            "jsonschema_contract_verification": "accepted_TX_32_10_of_10",
            "independent_evaluation_protocol": "ready_TX_37_external_execution_not_run",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-37 {field} must be {expected}")
        for required_route in (
            "review_TX_37_protocol_and_external_prerequisites",
            "nominate_independent_evaluator_and_supply_conflict_attestation",
            "authorize_minimal_artifact_transfer_and_external_execution_only_after_named_evaluator_acceptance",
            "seek_accountable_G_10_reacceptance_only_after_retained_evidence_closure",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-37 state omits controlled next route {required_route}")
        for required_block in (
            "mutate_accepted_TX_35_measurement_without_accountable_supersession_and_remeasurement",
            "treat_TX_37_protocol_as_executed_independent_evidence",
            "create_or_store_confidential_holdouts_in_repository",
            "transmit_artifacts_without_separate_permission_envelope",
            "accept_external_evaluation_without_complete_result_receipt",
            "claim_G_10_after_TX_37_without_executed_independent_and_remaining_retained_evidence",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-37 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX37-001":
            messages.append(f"{path}: post-TX-37 state is not aligned to the TX-37 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX37-001":
            messages.append(f"{path}: post-TX-37 state is not aligned to the TX-37 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-014",
            "TX-37-INDEPENDENT-ROTATED-EVALUATION-PROTOCOL",
            "TX37-INDEPENDENT-EVALUATION-PROTOCOL-READY",
            "TX37-INDEPENDENT-EVALUATION-NOT-EXECUTED",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX37-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-37 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-37 state must stop at the named external-evaluator gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-37 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_38_independent_evaluation_retained_future_work":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
            "jsonschema_contract_verification": "accepted_TX_32_10_of_10",
            "independent_evaluation_protocol": "ready_TX_37_external_execution_not_run",
            "independent_evaluation_disposition": "retained_active_future_work_G_11_015",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-38 {field} must be {expected}")
        for required_route in (
            "review_TX_38_independent_evaluation_future_work_disposition",
            "decide_broad_stakeholder_and_affected_party_review_requirement_for_bounded_nonproduction_migration",
            "decide_target_domain_acceptance_requirement_for_bounded_nonproduction_migration",
            "decide_production_and_operational_evidence_requirement_for_bounded_nonproduction_migration",
            "seek_accountable_G_10_reacceptance_only_after_every_other_retained_obligation_has_evidence_or_accountable_disposition",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-38 state omits controlled next route {required_route}")
        for required_block in (
            "treat_TX_37_protocol_as_executed_independent_evidence",
            "treat_TX_38_future_work_disposition_as_independent_evaluation_evidence_waiver_or_deletion",
            "reactivate_independent_evaluation_for_current_migration_without_accountable_supersession",
            "begin_remaining_evidence_families_automatically_after_TX_38",
            "claim_G_10_after_TX_38_without_remaining_retained_obligation_evidence_or_accountable_dispositions",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-38 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX38-001":
            messages.append(f"{path}: post-TX-38 state is not aligned to the TX-38 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX38-001":
            messages.append(f"{path}: post-TX-38 state is not aligned to the TX-38 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-015",
            "TX-38-INDEPENDENT-EVALUATION-FUTURE-WORK-DISPOSITION",
            "TX38-INDEPENDENT-EVALUATION-RETAINED-ACTIVE-FUTURE-WORK",
            "TX38-TX37-PROTOCOL-READINESS-PRESERVED",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX38-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-38 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-38 state must stop at the remaining evidence-family disposition gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-38 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_39_remaining_evidence_families_retained_future_work":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
            "jsonschema_contract_verification": "accepted_TX_32_10_of_10",
            "independent_evaluation_protocol": "ready_TX_37_external_execution_not_run",
            "independent_evaluation_disposition": "retained_active_future_work_G_11_015",
            "stakeholder_affected_party_review_disposition": "retained_active_future_work_G_11_016",
            "target_domain_acceptance_disposition": "retained_active_future_work_G_11_016",
            "production_operational_evidence_disposition": "retained_active_future_work_G_11_016",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-39 {field} must be {expected}")
        for required_route in (
            "review_TX_39_remaining_evidence_families_future_work_disposition",
            "seek_separate_accountable_G_10_reconsideration_for_bounded_nonproduction_migration_only_after_TX_39_shared_baseline",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-39 state omits controlled next route {required_route}")
        for required_block in (
            "treat_TX_37_protocol_as_executed_independent_evidence",
            "treat_TX_38_future_work_disposition_as_independent_evaluation_evidence_waiver_or_deletion",
            "treat_TX_39_future_work_dispositions_as_stakeholder_domain_production_operational_evidence_waivers_or_deletions",
            "reactivate_any_TX_39_retained_family_without_accountable_context_specific_supersession",
            "execute_stakeholder_affected_party_domain_production_or_operational_work_from_TX_39",
            "reconsider_accept_or_supersede_G_10_inside_TX_39",
            "claim_G_10_from_TX_39_dispositions_without_separate_accountable_reconsideration",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-39 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX39-001":
            messages.append(f"{path}: post-TX-39 state is not aligned to the TX-39 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX39-001":
            messages.append(f"{path}: post-TX-39 state is not aligned to the TX-39 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G11-016",
            "TX-39-REMAINING-EVIDENCE-FAMILIES-FUTURE-WORK-DISPOSITION",
            "TX39-STAKEHOLDER-AFFECTED-PARTY-REVIEW-RETAINED-ACTIVE-FUTURE-WORK",
            "TX39-TARGET-DOMAIN-ACCEPTANCE-RETAINED-ACTIVE-FUTURE-WORK",
            "TX39-PRODUCTION-OPERATIONAL-EVIDENCE-RETAINED-ACTIVE-FUTURE-WORK",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX39-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-39 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-39 state must stop at the separate G-10 reconsideration gate")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-39 state must remain human gated")
    elif phase == "strategic_baseline_migration_TX_40_G_10_reconsidered_deferred_no_inferred_acceptance":
        required_summary = {
            "strategic_approval": "accepted_G_08",
            "derivative_regeneration": "complete_G_09",
            "host_verification": "accepted_G_07_mixed_profile",
            "semantic_review_evidence": "accepted_TX_24_7_of_7",
            "plan_scope_interpretation": "accepted_TX_25_410_future_work",
            "python_package_verification": "accepted_TX_26_4_of_4",
            "yaml_control_verification": "accepted_TX_27_11_of_11",
            "format_governance_verification": "accepted_TX_28_10_of_10",
            "csv_registry_verification": "accepted_TX_29_5_of_5",
            "markdown_source_verification": "accepted_TX_30_4_of_4",
            "toml_config_verification": "accepted_TX_31_9_of_9",
            "jsonschema_contract_verification": "accepted_TX_32_10_of_10",
            "independent_evaluation_protocol": "ready_TX_37_external_execution_not_run",
            "independent_evaluation_disposition": "retained_active_future_work_G_11_015",
            "stakeholder_affected_party_review_disposition": "retained_active_future_work_G_11_016",
            "target_domain_acceptance_disposition": "retained_active_future_work_G_11_016",
            "production_operational_evidence_disposition": "retained_active_future_work_G_11_016",
            "g10_reconsideration": "deferred_G_10_002_no_inferred_acceptance",
        }
        for field, expected in required_summary.items():
            if summary.get(field) != expected:
                messages.append(f"{path}: post-TX-40 {field} must be {expected}")
        for required_route in (
            "review_TX_40_G_10_reconsidered_deferred_disposition",
            "seek_explicit_accountable_G_10_accept_or_reject_route_for_shared_baseline_9996771",
        ):
            if required_route not in allowed:
                messages.append(f"{path}: post-TX-40 state omits controlled next route {required_route}")
        for required_block in (
            "treat_TX_38_future_work_disposition_as_independent_evaluation_evidence_waiver_or_deletion",
            "treat_TX_39_future_work_dispositions_as_stakeholder_domain_production_operational_evidence_waivers_or_deletions",
            "infer_G_10_acceptance_or_rejection_from_TX_40_reconsideration",
            "accept_G_10_without_explicit_accountable_human_route_selection_for_exact_shared_baseline",
            "treat_TX_40_as_retained_evidence_execution_acceptance_waiver_or_deletion",
            "execute_or_reactivate_any_retained_evidence_family_from_TX_40",
            "claim_production_readiness_or_operational_authority_without_executed_evidence",
        ):
            if required_block not in blocked:
                messages.append(f"{path}: post-TX-40 state omits blocked action {required_block}")
        if state.get("latest_closeout_evidence_id") != "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX40-001":
            messages.append(f"{path}: post-TX-40 state is not aligned to the TX-40 completion")
        if state.get("latest_handoff_evidence_id") != "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX40-001":
            messages.append(f"{path}: post-TX-40 state is not aligned to the TX-40 handoff")
        for evidence_id in (
            "DDR-SFADEV-STRATEGIC-BASELINE-G10-002",
            "TX-40-G10-ACCOUNTABLE-RECONSIDERATION",
            "TX40-G10-RECONSIDERED-DEFERRED-NO-INFERRED-ACCEPTANCE",
            "TX40-RETAINED-EVIDENCE-FAMILIES-UNEXECUTED-AND-PRESERVED",
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX40-001",
        ):
            if evidence_id not in set(state.get("current_state_evidence", [])):
                messages.append(f"{path}: post-TX-40 state omits {evidence_id}")
        if state.get("continuation_state") != "blocked" or state.get("escalation_state") != "pending":
            messages.append(f"{path}: post-TX-40 state must stop at explicit accountable G-10 route selection")
        if state.get("state_status") != "human_gated" or state.get("human_gate_required") is not True:
            messages.append(f"{path}: post-TX-40 state must remain human gated")
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
