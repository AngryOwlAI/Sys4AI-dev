"""Deterministic TX-23 evidence-closure ledger generation and validation."""

from __future__ import annotations

import csv
from collections import Counter
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
) -> ValidationResult:
    trace_path = resolve_registered_path(str(trace_registry))
    ledger_path = resolve_registered_path(str(ledger))
    try:
        trace_rows = read_registry_rows(trace_path)
        actual = read_registry_rows(ledger_path)
    except (OSError, RuntimeError) as exc:
        return ValidationResult(False, [str(exc)])

    messages: list[str] = []
    expected = expected_evidence_closure_rows(trace_rows)
    if not actual or tuple(actual[0].keys()) != LEDGER_FIELDS:
        messages.append(f"{ledger_path}: unexpected or empty ledger header")
    if actual != expected:
        messages.append(f"{ledger_path}: ledger does not exactly classify the current trace gaps")

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

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            _summary(actual),
            "Classification is planning evidence only; trace statuses, waivers, G-10, production, and operations remain unchanged.",
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
