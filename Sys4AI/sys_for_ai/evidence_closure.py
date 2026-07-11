"""Deterministic TX-23 planning and TX-24 local-evidence validation."""

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
            "TX-23 planning history is frozen; TX-24 changes only accepted semantic-review evidence and grants no waiver, G-10, production, or operational authority.",
        ],
    )


def validate_local_evidence_execution(
    trace_registry: str | Path = "registries/requirement_trace_registry.csv",
    ledger: str | Path = "registries/evidence_closure_plan_registry.csv",
    execution_registry: str | Path = "registries/local_evidence_execution_registry.csv",
) -> ValidationResult:
    """Validate the exact first TX-24 semantic-review evidence family."""

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
    expected_closures = {
        "CLOSE-SFA-CORE-ID-001-SEMANTIC-REVIEW",
        "CLOSE-SFA-CORE-ID-002-SEMANTIC-REVIEW",
        "CLOSE-SFA-CORE-ID-003-SEMANTIC-REVIEW",
        "CLOSE-SFA-P0-FR-001-SEMANTIC-REVIEW",
        "CLOSE-SFA-P0-FR-002-SEMANTIC-REVIEW",
        "CLOSE-SFA-P0-FR-003-SEMANTIC-REVIEW",
        "CLOSE-SFA-P0-FR-004-SEMANTIC-REVIEW",
    }
    actual_closures = {row.get("closure_id", "") for row in execution_rows}
    if actual_closures != expected_closures or len(execution_rows) != len(expected_closures):
        messages.append(f"{execution_path}: TX-24 must contain exactly the seven authorized semantic closures")

    for index, row in enumerate(execution_rows, start=2):
        label = f"{execution_path}:{index}"
        closure = ledger_by_id.get(row.get("closure_id", ""))
        trace = trace_by_id.get(row.get("trace_id", ""))
        if closure is None:
            messages.append(f"{label}: closure_id is absent from the frozen TX-23 ledger")
            continue
        if closure.get("closure_route") != "locally_executable_evidence" or closure.get("gap_dimension") != "semantic_review":
            messages.append(f"{label}: closure is not an authorized local semantic-review route")
        if row.get("requirement_id") != closure.get("requirement_id") or row.get("trace_id") != closure.get("trace_id"):
            messages.append(f"{label}: closure trace and requirement binding drifted")
        if row.get("prior_state") != "needs_evidence" or row.get("resulting_state") != "sufficient":
            messages.append(f"{label}: semantic state transition must be needs_evidence to sufficient")
        if row.get("status") != "accepted" or row.get("execution_transaction_id") != "TX-24-LOCAL-EVIDENCE-SEMANTIC-REVIEW":
            messages.append(f"{label}: execution status or transaction binding is invalid")
        if row.get("reviewer_role") != "requirements_verifier" or row.get("review_date") != "2026-07-11":
            messages.append(f"{label}: accountable review identity or date is invalid")
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
        if trace.get("semantic_review_verdict") != "sufficient":
            messages.append(f"{label}: trace semantic_review_verdict is not sufficient")
        if trace.get("semantic_review_owner") != "requirements_verifier" or trace.get("semantic_review_date") != "2026-07-11":
            messages.append(f"{label}: trace review identity is not aligned")
        if trace.get("capability_status") != "scaffolded" or trace.get("verification_status") != "planned":
            messages.append(f"{label}: TX-24 improperly promoted capability or verification state")
        for field in ("implementation_artifacts", "validation_evidence"):
            if not set(_paths(row.get(field, ""))).issubset(set(_paths(trace.get(field, "")))):
                messages.append(f"{label}: execution {field} is not preserved in the trace row")
        if row.get("evidence_report_path") not in _paths(trace.get("evidence_paths", "")):
            messages.append(f"{label}: evidence report is not preserved in the trace row")

    verdict_counts = Counter(row.get("semantic_review_verdict") for row in trace_rows)
    if verdict_counts.get("needs_evidence", 0) != 0 or verdict_counts.get("sufficient", 0) != len(trace_rows):
        messages.append(f"{trace_path}: TX-24 semantic-review counts are not sufficient={len(trace_rows)} needs_evidence=0")

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            "TX-24 local evidence: 7 semantic-review obligations accepted; 67 local verification obligations and 410 plan-scope candidates remain.",
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
