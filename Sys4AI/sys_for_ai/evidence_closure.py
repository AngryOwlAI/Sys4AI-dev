"""Deterministic evidence-closure planning, execution, and scope validation."""

from __future__ import annotations

import csv
from collections import Counter
import hashlib
from pathlib import Path

from .registry_io import read_registry_rows, resolve_registered_path
from .validators import ValidationResult


LEDGER_FIELDS = (
    "closure_id",
    "trace_id",
    "requirement_id",
    "gap_dimension",
    "current_state",
    "closure_route",
    "accountable_role",
    "prerequisite",
    "planned_evidence",
    "status",
    "notes",
)
OPEN_STATES = {
    "verification": ("verification_status", {"planned"}),
    "capability": ("capability_status", {"scaffolded", "absent"}),
    "coverage": ("coverage_status", {"partial"}),
    "semantic_review": ("semantic_review_verdict", {"needs_evidence"}),
}
ROUTES = {
    "locally_executable_evidence",
    "external_dependency",
    "accountable_waiver_candidate",
    "plan_supersession_candidate",
    "blocked_gap",
}
TX23_LEDGER_SHA256 = "1e9e2b2a0a7bc4f589addd65b8d34642899a3f812e7ce35be6e62a2c0fcc6138"
LOCAL_EXECUTION_FIELDS = (
    "execution_evidence_id",
    "closure_id",
    "trace_id",
    "requirement_id",
    "evidence_family",
    "prior_state",
    "resulting_state",
    "evidence_report_path",
    "implementation_artifacts",
    "validation_evidence",
    "reviewer_role",
    "review_date",
    "status",
    "execution_transaction_id",
    "notes",
)
PLAN_INTERPRETATION_FIELDS = (
    "disposition_id",
    "closure_id",
    "trace_id",
    "requirement_id",
    "gap_dimension",
    "retained_trace_state",
    "plan_interpretation",
    "g10_migration_effect",
    "requirement_lifecycle_effect",
    "trace_mutation",
    "waiver_id",
    "decision_id",
    "execution_transaction_id",
    "evidence_report_path",
    "reviewer_role",
    "review_date",
    "status",
    "notes",
)
PLAN_INTERPRETATION_DECISION_ID = "DDR-SFADEV-STRATEGIC-BASELINE-G11-002"
PLAN_INTERPRETATION_TRANSACTION_ID = "TX-25-PLAN-INTERPRETATION"
PLAN_INTERPRETATION_REPORT = (
    "implementation_plans/acceptance_reports/"
    "STRATEGIC-BASELINE-MIGRATION-PLAN-INTERPRETATION-SFADEV-TX25.md"
)
PLAN_INTERPRETATION_SHA256 = "9ed89d6ff5872ee2fb2b740791c268d9048e97f31eae8ff7d3b4d2d8929d5f38"
TX24_SEMANTIC_CLOSURES = {
    "CLOSE-SFA-CORE-ID-001-SEMANTIC-REVIEW",
    "CLOSE-SFA-CORE-ID-002-SEMANTIC-REVIEW",
    "CLOSE-SFA-CORE-ID-003-SEMANTIC-REVIEW",
    "CLOSE-SFA-P0-FR-001-SEMANTIC-REVIEW",
    "CLOSE-SFA-P0-FR-002-SEMANTIC-REVIEW",
    "CLOSE-SFA-P0-FR-003-SEMANTIC-REVIEW",
    "CLOSE-SFA-P0-FR-004-SEMANTIC-REVIEW",
}
TX26_PYTHON_PACKAGE_CLOSURES = {
    "CLOSE-SFA-CORE-PY-001-VERIFICATION",
    "CLOSE-SFA-CORE-PY-002-VERIFICATION",
    "CLOSE-SFA-CORE-PY-003-VERIFICATION",
    "CLOSE-SFA-P0-NFR-015-VERIFICATION",
}
TX27_YAML_CONTROL_CLOSURES = {
    *{f"CLOSE-SFA-CORE-YAML-{index:03d}-VERIFICATION" for index in range(1, 11)},
    "CLOSE-SFA-P0-FR-033-VERIFICATION",
}
TX28_FORMAT_GOVERNANCE_CLOSURES = {
    *{f"CLOSE-SFA-CORE-FORMAT-{index:03d}-VERIFICATION" for index in range(1, 7)},
    "CLOSE-SFA-P0-FR-031-VERIFICATION",
    "CLOSE-SFA-P0-FR-032-VERIFICATION",
    "CLOSE-SFA-P0-FR-045-VERIFICATION",
    "CLOSE-SFA-P0-NFR-014-VERIFICATION",
}
TX29_CSV_REGISTRY_CLOSURES = {
    *{f"CLOSE-SFA-CORE-CSV-{index:03d}-VERIFICATION" for index in range(1, 6)},
}
TX30_MARKDOWN_SOURCE_CLOSURES = {
    *{f"CLOSE-SFA-CORE-MD-{index:03d}-VERIFICATION" for index in range(1, 4)},
    "CLOSE-SFA-P0-FR-036-VERIFICATION",
}
TX31_TOML_CONFIG_CLOSURES = {
    *{f"CLOSE-SFA-CORE-TOML-{index:03d}-VERIFICATION" for index in range(1, 8)},
    "CLOSE-SFA-P0-FR-034-VERIFICATION",
    "CLOSE-SFA-P0-FR-043-VERIFICATION",
}
TX32_JSONSCHEMA_CONTRACT_CLOSURES = {
    *{f"CLOSE-SFA-CORE-JSONSCHEMA-{index:03d}-VERIFICATION" for index in range(1, 8)},
    "CLOSE-SFA-P0-FR-035-VERIFICATION",
    "CLOSE-SFA-P0-FR-039-VERIFICATION",
    "CLOSE-SFA-P0-FR-042-VERIFICATION",
}
TX33_GENERATED_READER_CLOSURES = {
    *{f"CLOSE-SFA-CORE-CCWIKI-{index:03d}-VERIFICATION" for index in range(1, 6)},
    *{f"CLOSE-SFA-CORE-VCCAT-{index:03d}-VERIFICATION" for index in range(1, 6)},
    "CLOSE-SFA-P0-FR-037-VERIFICATION",
    "CLOSE-SFA-P0-FR-038-VERIFICATION",
    "CLOSE-SFA-P0-FR-044-VERIFICATION",
    "CLOSE-SFA-P0-NFR-017-VERIFICATION",
}


def expected_evidence_closure_rows(trace_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Build the exact planning ledger without changing authoritative trace state."""

    expected: list[dict[str, str]] = []
    for trace in trace_rows:
        for dimension, (field, open_values) in OPEN_STATES.items():
            state = trace.get(field, "")
            if state not in open_values:
                continue
            route = _route_for(trace, dimension)
            local = route == "locally_executable_evidence"
            expected.append(
                {
                    "closure_id": f"CLOSE-{trace['trace_id'][6:]}-{dimension.upper().replace('_', '-')}",
                    "trace_id": trace["trace_id"],
                    "requirement_id": trace["requirement_id"],
                    "gap_dimension": dimension,
                    "current_state": state,
                    "closure_route": route,
                    "accountable_role": "verification_engineer" if local else "system_director",
                    "prerequisite": (
                        "current_local_implementation_and_test_evidence"
                        if local
                        else "accountable_G_10_scope_and_plan_decision"
                    ),
                    "planned_evidence": (
                        "exact_non_generated_artifact_and_executed_validation_or_review"
                        if local
                        else "approved_plan_supersession_or_explicit_retention_as_future_framework_work"
                    ),
                    "status": "planned",
                    "notes": (
                        "TX-23 classifies only; execute evidence in a separately authorized packet."
                        if local
                        else "Current state remains truthful; do not bulk-promote, waive, or treat it as migration completion."
                    ),
                }
            )
    return expected


def write_evidence_closure_ledger(
    trace_registry: str | Path = "registries/requirement_trace_registry.csv",
    ledger: str | Path = "registries/evidence_closure_plan_registry.csv",
) -> ValidationResult:
    trace_path = resolve_registered_path(str(trace_registry))
    ledger_path = resolve_registered_path(str(ledger))
    execution_path = ledger_path.with_name("local_evidence_execution_registry.csv")
    if execution_path.exists() and execution_path.stat().st_size:
        return ValidationResult(
            False,
            [
                f"{ledger_path}: TX-23 ledger is frozen after local evidence execution; "
                "preserve it and record later evidence in the execution registry"
            ],
        )
    try:
        rows = expected_evidence_closure_rows(read_registry_rows(trace_path))
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with ledger_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    except (OSError, RuntimeError, KeyError) as exc:
        return ValidationResult(False, [str(exc)])
    return ValidationResult(True, [_summary(rows), "Ledger generation changes no requirement-trace state."])


def validate_evidence_closure_plan(
    trace_registry: str | Path = "registries/requirement_trace_registry.csv",
    ledger: str | Path = "registries/evidence_closure_plan_registry.csv",
    execution_registry: str | Path = "registries/local_evidence_execution_registry.csv",
) -> ValidationResult:
    trace_path = resolve_registered_path(str(trace_registry))
    ledger_path = resolve_registered_path(str(ledger))
    try:
        actual = read_registry_rows(ledger_path)
    except (OSError, RuntimeError) as exc:
        return ValidationResult(False, [str(exc)])

    messages: list[str] = []
    if not actual or tuple(actual[0].keys()) != LEDGER_FIELDS:
        messages.append(f"{ledger_path}: unexpected or empty ledger header")
    if ledger_path.exists() and hashlib.sha256(ledger_path.read_bytes()).hexdigest() != TX23_LEDGER_SHA256:
        messages.append(f"{ledger_path}: activated TX-23 ledger bytes changed instead of being superseded")

    closure_ids = [row.get("closure_id", "") for row in actual]
    if len(closure_ids) != len(set(closure_ids)):
        messages.append(f"{ledger_path}: duplicate closure_id")
    for index, row in enumerate(actual, start=2):
        if row.get("closure_route") not in ROUTES:
            messages.append(f"{ledger_path}:{index}: unsupported closure_route")
        if row.get("status") != "planned":
            messages.append(f"{ledger_path}:{index}: TX-23 ledger status must remain planned")

    counts = Counter(row["gap_dimension"] for row in actual)
    required_counts = {
        "verification": 200,
        "capability": 142,
        "coverage": 135,
        "semantic_review": 7,
    }
    if counts != required_counts:
        messages.append(f"{ledger_path}: expected open-state counts {required_counts}, observed {dict(counts)}")
    route_counts = Counter(row["closure_route"] for row in actual)
    if route_counts != {"locally_executable_evidence": 74, "plan_supersession_candidate": 410}:
        messages.append(f"{ledger_path}: unexpected route counts {dict(route_counts)}")

    execution_result = validate_local_evidence_execution(
        trace_registry=trace_path,
        ledger=ledger_path,
        execution_registry=execution_registry,
    )
    messages.extend(execution_result.messages if not execution_result.ok else [])

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            _summary(actual),
            *execution_result.messages,
            "TX-23 planning history is frozen; TX-24 and TX-26 through TX-33 evidence is additive and grants no waiver, G-10, production, or operational authority.",
        ],
    )


def validate_local_evidence_execution(
    trace_registry: str | Path = "registries/requirement_trace_registry.csv",
    ledger: str | Path = "registries/evidence_closure_plan_registry.csv",
    execution_registry: str | Path = "registries/local_evidence_execution_registry.csv",
) -> ValidationResult:
    """Validate the exact activated bounded local-evidence families."""

    trace_path = resolve_registered_path(str(trace_registry))
    ledger_path = resolve_registered_path(str(ledger))
    execution_path = resolve_registered_path(str(execution_registry))
    try:
        trace_rows = read_registry_rows(trace_path)
        ledger_rows = read_registry_rows(ledger_path)
        execution_rows = read_registry_rows(execution_path)
    except (OSError, RuntimeError) as exc:
        return ValidationResult(False, [str(exc)])

    messages: list[str] = []
    if not execution_rows or tuple(execution_rows[0].keys()) != LOCAL_EXECUTION_FIELDS:
        messages.append(f"{execution_path}: unexpected or empty execution registry header")
        return ValidationResult(False, messages)

    ledger_by_id = {row.get("closure_id", ""): row for row in ledger_rows}
    trace_by_id = {row.get("trace_id", ""): row for row in trace_rows}
    expected_closures = (
        TX24_SEMANTIC_CLOSURES
        | TX26_PYTHON_PACKAGE_CLOSURES
        | TX27_YAML_CONTROL_CLOSURES
        | TX28_FORMAT_GOVERNANCE_CLOSURES
        | TX29_CSV_REGISTRY_CLOSURES
        | TX30_MARKDOWN_SOURCE_CLOSURES
        | TX31_TOML_CONFIG_CLOSURES
        | TX32_JSONSCHEMA_CONTRACT_CLOSURES
        | TX33_GENERATED_READER_CLOSURES
    )
    actual_closures = {row.get("closure_id", "") for row in execution_rows}
    if actual_closures != expected_closures or len(execution_rows) != len(expected_closures):
        messages.append(f"{execution_path}: must contain exactly the 74 activated TX-24 and TX-26 through TX-33 closures")

    for index, row in enumerate(execution_rows, start=2):
        label = f"{execution_path}:{index}"
        closure = ledger_by_id.get(row.get("closure_id", ""))
        trace = trace_by_id.get(row.get("trace_id", ""))
        if closure is None:
            messages.append(f"{label}: closure_id is absent from the frozen TX-23 ledger")
            continue
        dimension = closure.get("gap_dimension")
        if closure.get("closure_route") != "locally_executable_evidence" or dimension not in {
            "semantic_review",
            "verification",
        }:
            messages.append(f"{label}: closure is not an authorized local evidence route")
        if row.get("requirement_id") != closure.get("requirement_id") or row.get("trace_id") != closure.get("trace_id"):
            messages.append(f"{label}: closure trace and requirement binding drifted")
        semantic_family = row.get("closure_id") in TX24_SEMANTIC_CLOSURES
        python_family = row.get("closure_id") in TX26_PYTHON_PACKAGE_CLOSURES
        yaml_family = row.get("closure_id") in TX27_YAML_CONTROL_CLOSURES
        format_family = row.get("closure_id") in TX28_FORMAT_GOVERNANCE_CLOSURES
        csv_family = row.get("closure_id") in TX29_CSV_REGISTRY_CLOSURES
        markdown_family = row.get("closure_id") in TX30_MARKDOWN_SOURCE_CLOSURES
        toml_family = row.get("closure_id") in TX31_TOML_CONFIG_CLOSURES
        jsonschema_family = row.get("closure_id") in TX32_JSONSCHEMA_CONTRACT_CLOSURES
        generated_reader_family = row.get("closure_id") in TX33_GENERATED_READER_CLOSURES
        if semantic_family:
            if row.get("prior_state") != "needs_evidence" or row.get("resulting_state") != "sufficient":
                messages.append(f"{label}: semantic state transition must be needs_evidence to sufficient")
            if row.get("evidence_family") != "identity_and_system_boundary_semantic_review":
                messages.append(f"{label}: TX-24 evidence family binding is invalid")
            if row.get("execution_transaction_id") != "TX-24-LOCAL-EVIDENCE-SEMANTIC-REVIEW":
                messages.append(f"{label}: TX-24 transaction binding is invalid")
            if row.get("reviewer_role") != "requirements_verifier":
                messages.append(f"{label}: TX-24 reviewer role is invalid")
        elif python_family:
            if row.get("prior_state") != "planned" or row.get("resulting_state") != "pass":
                messages.append(f"{label}: verification state transition must be planned to pass")
            if row.get("evidence_family") != "python_reference_and_dependency_policy_verification":
                messages.append(f"{label}: TX-26 evidence family binding is invalid")
            if row.get("execution_transaction_id") != "TX-26-LOCAL-EVIDENCE-PYTHON-PACKAGE":
                messages.append(f"{label}: TX-26 transaction binding is invalid")
            if row.get("reviewer_role") != "verification_engineer":
                messages.append(f"{label}: TX-26 reviewer role is invalid")
        elif yaml_family:
            if row.get("prior_state") != "planned" or row.get("resulting_state") != "pass":
                messages.append(f"{label}: verification state transition must be planned to pass")
            if row.get("evidence_family") != "yaml_control_state_and_safe_parsing_verification":
                messages.append(f"{label}: TX-27 evidence family binding is invalid")
            if row.get("execution_transaction_id") != "TX-27-LOCAL-EVIDENCE-YAML-CONTROL":
                messages.append(f"{label}: TX-27 transaction binding is invalid")
            if row.get("reviewer_role") != "verification_engineer":
                messages.append(f"{label}: TX-27 reviewer role is invalid")
        elif format_family:
            if row.get("prior_state") != "planned" or row.get("resulting_state") != "pass":
                messages.append(f"{label}: verification state transition must be planned to pass")
            if row.get("evidence_family") != "core_format_profile_governance_and_memory_inspectability_verification":
                messages.append(f"{label}: TX-28 evidence family binding is invalid")
            if row.get("execution_transaction_id") != "TX-28-LOCAL-EVIDENCE-FORMAT-GOVERNANCE":
                messages.append(f"{label}: TX-28 transaction binding is invalid")
            if row.get("reviewer_role") != "verification_engineer":
                messages.append(f"{label}: TX-28 reviewer role is invalid")
        elif csv_family:
            if row.get("prior_state") != "planned" or row.get("resulting_state") != "pass":
                messages.append(f"{label}: verification state transition must be planned to pass")
            if row.get("evidence_family") != "csv_registry_and_graph_governance_verification":
                messages.append(f"{label}: TX-29 evidence family binding is invalid")
            if row.get("execution_transaction_id") != "TX-29-LOCAL-EVIDENCE-CSV-REGISTRY":
                messages.append(f"{label}: TX-29 transaction binding is invalid")
            if row.get("reviewer_role") != "verification_engineer":
                messages.append(f"{label}: TX-29 reviewer role is invalid")
        elif markdown_family:
            if row.get("prior_state") != "planned" or row.get("resulting_state") != "pass":
                messages.append(f"{label}: verification state transition must be planned to pass")
            if row.get("evidence_family") != "markdown_source_authority_verification":
                messages.append(f"{label}: TX-30 evidence family binding is invalid")
            if row.get("execution_transaction_id") != "TX-30-LOCAL-EVIDENCE-MARKDOWN-SOURCE":
                messages.append(f"{label}: TX-30 transaction binding is invalid")
            if row.get("reviewer_role") != "verification_engineer":
                messages.append(f"{label}: TX-30 reviewer role is invalid")
        elif toml_family:
            if row.get("prior_state") != "planned" or row.get("resulting_state") != "pass":
                messages.append(f"{label}: verification state transition must be planned to pass")
            if row.get("evidence_family") != "toml_configuration_and_secret_policy_verification":
                messages.append(f"{label}: TX-31 evidence family binding is invalid")
            if row.get("execution_transaction_id") != "TX-31-LOCAL-EVIDENCE-TOML-CONFIG":
                messages.append(f"{label}: TX-31 transaction binding is invalid")
            if row.get("reviewer_role") != "verification_engineer":
                messages.append(f"{label}: TX-31 reviewer role is invalid")
        elif jsonschema_family:
            if row.get("prior_state") != "planned" or row.get("resulting_state") != "pass":
                messages.append(f"{label}: verification state transition must be planned to pass")
            if row.get("evidence_family") != "jsonschema_validation_contract_verification":
                messages.append(f"{label}: TX-32 evidence family binding is invalid")
            if row.get("execution_transaction_id") != "TX-32-LOCAL-EVIDENCE-JSON-SCHEMA":
                messages.append(f"{label}: TX-32 transaction binding is invalid")
            if row.get("reviewer_role") != "verification_engineer":
                messages.append(f"{label}: TX-32 reviewer role is invalid")
        elif generated_reader_family:
            if row.get("prior_state") != "planned" or row.get("resulting_state") != "pass":
                messages.append(f"{label}: verification state transition must be planned to pass")
            if row.get("evidence_family") != "generated_reader_surface_verification":
                messages.append(f"{label}: TX-33 evidence family binding is invalid")
            if row.get("execution_transaction_id") != "TX-33-LOCAL-EVIDENCE-GENERATED-READERS":
                messages.append(f"{label}: TX-33 transaction binding is invalid")
            if row.get("reviewer_role") != "verification_engineer":
                messages.append(f"{label}: TX-33 reviewer role is invalid")
        else:
            messages.append(f"{label}: closure is outside the activated local families")
        expected_review_date = "2026-07-12" if markdown_family or toml_family or jsonschema_family or generated_reader_family else "2026-07-11"
        if row.get("status") != "accepted" or row.get("review_date") != expected_review_date:
            messages.append(f"{label}: execution status or review date is invalid")
        for field in ("evidence_report_path", "implementation_artifacts", "validation_evidence"):
            paths = _paths(row.get(field, ""))
            if not paths:
                messages.append(f"{label}: {field} must name exact evidence paths")
            for value in paths:
                if not resolve_registered_path(value).exists():
                    messages.append(f"{label}: missing {field} path {value}")
        if trace is None:
            messages.append(f"{label}: trace row is missing")
            continue
        if semantic_family:
            if trace.get("semantic_review_verdict") != "sufficient":
                messages.append(f"{label}: trace semantic_review_verdict is not sufficient")
            if trace.get("semantic_review_owner") != "requirements_verifier" or trace.get("semantic_review_date") != "2026-07-11":
                messages.append(f"{label}: trace review identity is not aligned")
            if trace.get("capability_status") != "scaffolded" or trace.get("verification_status") != "planned":
                messages.append(f"{label}: TX-24 improperly promoted capability or verification state")
        elif python_family or yaml_family or format_family or csv_family or markdown_family or toml_family or jsonschema_family or generated_reader_family:
            if trace.get("verification_status") != "pass":
                messages.append(f"{label}: trace verification_status is not pass")
            if trace.get("capability_status") != "implemented" or trace.get("coverage_status") != "covered":
                messages.append(f"{label}: accepted verification requires implemented and covered trace state")
            if trace.get("verification_waiver_id"):
                messages.append(f"{label}: accepted verification must not use a waiver")
        for field in ("implementation_artifacts", "validation_evidence"):
            if not set(_paths(row.get(field, ""))).issubset(set(_paths(trace.get(field, "")))):
                messages.append(f"{label}: execution {field} is not preserved in the trace row")
        trace_report_field = "evidence_paths" if semantic_family else "validation_evidence"
        if row.get("evidence_report_path") not in _paths(trace.get(trace_report_field, "")):
            messages.append(f"{label}: evidence report is not preserved in the trace row")

    verdict_counts = Counter(row.get("semantic_review_verdict") for row in trace_rows)
    if verdict_counts.get("needs_evidence", 0) != 0 or verdict_counts.get("sufficient", 0) != len(trace_rows):
        messages.append(f"{trace_path}: TX-24 semantic-review counts are not sufficient={len(trace_rows)} needs_evidence=0")

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            "Local evidence: 7 TX-24 semantic reviews and 67 verifications across TX-26 through TX-33 accepted; zero local verification obligations remain. The 410 frozen plan-scope candidates retain their TX-25 interpretation.",
        ],
    )


def expected_plan_interpretation_rows(
    ledger_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Build the exact G-11 disposition set without changing trace or TX-23 history."""

    return [
        {
            "disposition_id": f"DISP-{row['closure_id'][6:]}",
            "closure_id": row["closure_id"],
            "trace_id": row["trace_id"],
            "requirement_id": row["requirement_id"],
            "gap_dimension": row["gap_dimension"],
            "retained_trace_state": row["current_state"],
            "plan_interpretation": "explicit_future_framework_work",
            "g10_migration_effect": "not_a_strategic_baseline_migration_blocker",
            "requirement_lifecycle_effect": "remains_active_required",
            "trace_mutation": "none",
            "waiver_id": "none",
            "decision_id": PLAN_INTERPRETATION_DECISION_ID,
            "execution_transaction_id": PLAN_INTERPRETATION_TRANSACTION_ID,
            "evidence_report_path": PLAN_INTERPRETATION_REPORT,
            "reviewer_role": "system_director",
            "review_date": "2026-07-11",
            "status": "accepted",
            "notes": (
                "Retain truthful full-framework maturity state as future work; "
                "do not promote, waive, close, or use it as a G-10 migration blocker."
            ),
        }
        for row in ledger_rows
        if row.get("closure_route") == "plan_supersession_candidate"
    ]


def write_plan_interpretation_registry(
    ledger: str | Path = "registries/evidence_closure_plan_registry.csv",
    registry: str | Path = "registries/plan_scope_interpretation_registry.csv",
) -> ValidationResult:
    """Write the deterministic 410-row explicit-future-work disposition registry."""

    ledger_path = resolve_registered_path(str(ledger))
    registry_path = resolve_registered_path(str(registry))
    if registry_path.exists() and registry_path.stat().st_size:
        result = validate_plan_interpretation(ledger=ledger_path, registry=registry_path)
        if result.ok:
            return ValidationResult(
                True,
                [
                    *result.messages,
                    "Activated TX-25 interpretation registry is already current and was not rewritten.",
                ],
            )
        return ValidationResult(
            False,
            [
                f"{registry_path}: activated TX-25 interpretation registry cannot be regenerated in place",
                *result.messages,
            ],
        )
    try:
        rows = expected_plan_interpretation_rows(read_registry_rows(ledger_path))
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        with registry_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=PLAN_INTERPRETATION_FIELDS,
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(rows)
    except (OSError, RuntimeError, KeyError) as exc:
        return ValidationResult(False, [str(exc)])
    return ValidationResult(
        len(rows) == 410,
        [
            f"Plan interpretation registry: {len(rows)} explicit future-work dispositions.",
            "Generation changes no requirement-trace state, waiver, or frozen TX-23 byte.",
        ],
    )


def validate_plan_interpretation(
    trace_registry: str | Path = "registries/requirement_trace_registry.csv",
    ledger: str | Path = "registries/evidence_closure_plan_registry.csv",
    registry: str | Path = "registries/plan_scope_interpretation_registry.csv",
) -> ValidationResult:
    """Validate exact disposition of all 410 plan-scope candidates."""

    trace_path = resolve_registered_path(str(trace_registry))
    ledger_path = resolve_registered_path(str(ledger))
    registry_path = resolve_registered_path(str(registry))
    try:
        trace_rows = read_registry_rows(trace_path)
        ledger_rows = read_registry_rows(ledger_path)
        actual = read_registry_rows(registry_path)
    except (OSError, RuntimeError) as exc:
        return ValidationResult(False, [str(exc)])

    messages: list[str] = []
    if not actual or tuple(actual[0].keys()) != PLAN_INTERPRETATION_FIELDS:
        return ValidationResult(False, [f"{registry_path}: unexpected or empty registry header"])
    expected = expected_plan_interpretation_rows(ledger_rows)
    expected_by_closure = {row["closure_id"]: row for row in expected}
    trace_by_id = {row.get("trace_id", ""): row for row in trace_rows}
    actual_closures = [row.get("closure_id", "") for row in actual]
    if len(actual) != 410 or set(actual_closures) != set(expected_by_closure):
        messages.append(f"{registry_path}: must disposition exactly all 410 plan-scope closures")
    if len(actual_closures) != len(set(actual_closures)):
        messages.append(f"{registry_path}: duplicate closure_id")

    trace_fields = {
        "verification": "verification_status",
        "capability": "capability_status",
        "coverage": "coverage_status",
    }
    for index, row in enumerate(actual, start=2):
        label = f"{registry_path}:{index}"
        expected_row = expected_by_closure.get(row.get("closure_id", ""))
        if expected_row is None:
            messages.append(f"{label}: closure is not a frozen TX-23 plan-scope candidate")
            continue
        for field in PLAN_INTERPRETATION_FIELDS:
            if row.get(field) != expected_row.get(field):
                messages.append(f"{label}: {field} drifted from the controlled interpretation")
        trace = trace_by_id.get(row.get("trace_id", ""))
        if trace is None:
            messages.append(f"{label}: trace row is missing")
            continue
        state_field = trace_fields.get(row.get("gap_dimension", ""))
        if state_field is None or trace.get(state_field) != row.get("retained_trace_state"):
            messages.append(f"{label}: retained trace state no longer matches the live trace")
        if trace.get("requirement_lifecycle") != "active" or trace.get("applicability_status") != "required":
            messages.append(f"{label}: future-work requirement is no longer active and required")
        if trace.get("verification_waiver_id"):
            messages.append(f"{label}: plan interpretation must not create or consume a waiver")
        if not resolve_registered_path(row.get("evidence_report_path", "")).exists():
            messages.append(f"{label}: missing controlled interpretation report")

    if hashlib.sha256(ledger_path.read_bytes()).hexdigest() != TX23_LEDGER_SHA256:
        messages.append(f"{ledger_path}: activated TX-23 ledger bytes changed")
    if hashlib.sha256(registry_path.read_bytes()).hexdigest() != PLAN_INTERPRETATION_SHA256:
        messages.append(f"{registry_path}: activated TX-25 interpretation registry bytes changed")
    if messages:
        return ValidationResult(False, messages)
    dimensions = Counter(row["gap_dimension"] for row in actual)
    return ValidationResult(
        True,
        [
            "Plan interpretation: 410/410 explicit future-work dispositions accepted; "
            f"verification={dimensions['verification']}, capability={dimensions['capability']}, "
            f"coverage={dimensions['coverage']}.",
            "Trace states remain active, required, unwaived, and unchanged; G-10 remains separately gated.",
        ],
    )


def _route_for(trace: dict[str, str], dimension: str) -> str:
    if dimension == "semantic_review":
        return "locally_executable_evidence"
    if dimension == "verification" and trace.get("capability_status") == "implemented":
        return "locally_executable_evidence"
    return "plan_supersession_candidate"


def _summary(rows: list[dict[str, str]]) -> str:
    dimensions = Counter(row["gap_dimension"] for row in rows)
    routes = Counter(row["closure_route"] for row in rows)
    return (
        f"Evidence closure ledger: {len(rows)} obligations; "
        f"verification={dimensions['verification']}, capability={dimensions['capability']}, "
        f"coverage={dimensions['coverage']}, semantic_review={dimensions['semantic_review']}; "
        f"local={routes['locally_executable_evidence']}, "
        f"plan_supersession={routes['plan_supersession_candidate']}"
    )


def _paths(value: str) -> list[str]:
    return [item.strip() for item in str(value).split(";") if item.strip()]
