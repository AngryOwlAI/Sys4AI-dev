"""Fail-closed quantitative measurement checks for the approved Sys4AI vision."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .jsonschema_io import JsonSchemaLoadError, load_json, validate_instance
from .registry_io import RegistryLoadError, read_registry_rows, resolve_registered_path
from .validators import ValidationResult


EXPECTED_RESULTS = {
    "QSM-001": (11, 11),
    "QSM-002": (25, 25),
    "QSM-003": (227, 227),
    "QSM-004": (5, 5),
}
ACCEPTANCE_DECISION_ID = "DDR-SFADEV-STRATEGIC-BASELINE-G11-013"
TRACE_DISPOSITION_FIELDS = (
    "requirement_lifecycle",
    "applicability_status",
    "coverage_status",
    "capability_status",
    "verification_status",
    "evidence_status",
    "evidence_paths",
    "trace_class",
    "semantic_review_verdict",
)


def validate_strategic_vision_measurement(
    measurement: str | Path = "assurance/strategic_vision_measurement_tx35.yaml",
    schema: str | Path = "schemas/contracts/strategic_vision_measurement.schema.json",
    product_root: str | Path = ".",
    acceptance_decision: str | Path = (
        "control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-013.yaml"
    ),
) -> ValidationResult:
    """Validate the TX-35 measurement contract and recompute all four results."""

    root = Path(product_root).resolve()
    measurement_path = resolve_registered_path(str(measurement), root)
    schema_path = resolve_registered_path(str(schema), root)
    messages: list[str] = []
    try:
        document = yaml.safe_load(measurement_path.read_text(encoding="utf-8"))
        contract = load_json(schema_path)
    except (OSError, yaml.YAMLError, JsonSchemaLoadError) as exc:
        return ValidationResult(False, [f"Cannot load strategic measurement contract: {exc}"])

    schema_errors = validate_instance(document, contract)
    if schema_errors:
        return ValidationResult(
            False,
            [f"{measurement_path}: {error}" for error in schema_errors],
        )

    metrics = {metric["metric_id"]: metric for metric in document["metrics"]}
    if set(metrics) != set(EXPECTED_RESULTS):
        messages.append("Strategic measurement must contain exactly QSM-001 through QSM-004")

    actual = {
        "QSM-001": _decision_accountability(root, messages),
        "QSM-002": _transaction_closeout(root, messages),
        "QSM-003": _trace_dispositions(root, messages),
        "QSM-004": _cross_version_result(root, messages),
    }
    for metric_id, result in actual.items():
        if metric_id not in metrics:
            continue
        recorded = metrics[metric_id]["result"]
        expected_value = result[0] / result[1]
        if (recorded["numerator"], recorded["denominator"]) != result:
            messages.append(
                f"{metric_id}: recorded {recorded['numerator']}/{recorded['denominator']} "
                f"does not match recomputed {result[0]}/{result[1]}"
            )
        if recorded["value"] != expected_value:
            messages.append(f"{metric_id}: recorded value does not match recomputed fraction")
        comparison = "meets_accepted_threshold" if expected_value >= 1.0 else "does_not_meet_accepted_threshold"
        if recorded["threshold_comparison"] != comparison:
            messages.append(f"{metric_id}: threshold comparison does not match recomputed result")

    _validate_acceptance_decision(root, acceptance_decision, messages)

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            "Quantitative strategic measurement: 4/4 metric results reproduced.",
            "Observed results: accountable decisions 11/11; controlled closeouts 25/25; trace dispositions 227/227; external CI jobs 5/5.",
            "Definitions, thresholds, named sources, observation intervals, results, and limitations are accepted by the accountable human.",
        ],
    )


def _validate_acceptance_decision(
    root: Path,
    acceptance_decision: str | Path,
    messages: list[str],
) -> None:
    decision_path = resolve_registered_path(str(acceptance_decision), root)
    decision = _load_yaml(decision_path, messages)
    authorization = decision.get("human_authorization", {})
    selected_route = decision.get("selected_route", {})
    boundary = decision.get("authority_boundary", {})
    reviewed = decision.get("reviewed_content", {})
    if not (
        decision.get("director_decision_id") == ACCEPTANCE_DECISION_ID
        and decision.get("decision_status") == "completed"
        and authorization.get("principal_name") == "Alex Omegapy"
        and authorization.get("principal_role") == "repository_maintainer_and_product_owner"
        and authorization.get("model_self_approval") is False
        and selected_route.get("route_id") == "accept_exact_TX_35_measurement_standard_and_results"
        and boundary.get("accepts_TX_35_measurement_standard_and_results") is True
        and boundary.get("accepts_gate_G_10_now") is False
        and reviewed.get("measurement_id") == "VISION-MEASURE-SFADEV-TX35-001"
        and reviewed.get("metric_ids") == ["QSM-001", "QSM-002", "QSM-003", "QSM-004"]
    ):
        messages.append(
            f"{decision_path}: accepted strategic measurement lacks exact accountable human decision evidence"
        )


def _decision_accountability(root: Path, messages: list[str]) -> tuple[int, int]:
    passed = 0
    for number in range(1, 12):
        path = root / "control_records/director_decisions" / (
            f"DDR-SFADEV-STRATEGIC-BASELINE-G11-{number:03d}.yaml"
        )
        data = _load_yaml(path, messages)
        authorization = data.get("human_authorization", {}) if isinstance(data, dict) else {}
        if (
            data.get("decision_status") == "completed"
            and authorization.get("principal_name") == "Alex Omegapy"
            and authorization.get("principal_role") == "repository_maintainer_and_product_owner"
            and authorization.get("model_self_approval") is False
        ):
            passed += 1
    return passed, 11


def _transaction_closeout(root: Path, messages: list[str]) -> tuple[int, int]:
    try:
        receipt_rows = read_registry_rows(root / "registries/completion_receipt_registry.csv")
        handoff_rows = read_registry_rows(root / "registries/handoff_registry.csv")
    except RegistryLoadError as exc:
        messages.append(str(exc))
        return 0, 25
    receipt_ids = {row["execution_transaction_id"] for row in receipt_rows}
    handoff_ids = {row["producing_execution_transaction_id"] for row in handoff_rows}
    passed = 0
    for number in range(10, 35):
        candidates = list((root / "control_records/execution_transactions").glob(f"TX-{number:02d}-*.yaml"))
        if len(candidates) != 1:
            messages.append(f"TX-{number:02d}: expected exactly one execution transaction record")
            continue
        data = _load_yaml(candidates[0], messages)
        transaction_id = data.get("execution_transaction_id") if isinstance(data, dict) else None
        if (
            data.get("state", {}).get("status") == "completed"
            and data.get("closeout_evidence", {}).get("status") == "complete"
            and transaction_id in receipt_ids
            and transaction_id in handoff_ids
        ):
            passed += 1
    return passed, 25


def _trace_dispositions(root: Path, messages: list[str]) -> tuple[int, int]:
    try:
        rows = read_registry_rows(root / "registries/requirement_trace_registry.csv")
    except RegistryLoadError as exc:
        messages.append(str(exc))
        return 0, 227
    passed = sum(
        all(row.get(field) for field in TRACE_DISPOSITION_FIELDS)
        and row.get("verification_status") in {"pass", "planned"}
        for row in rows
    )
    if len(rows) != 227:
        messages.append(f"QSM-003: expected frozen baseline population 227, observed {len(rows)}")
    return passed, len(rows) or 1


def _cross_version_result(root: Path, messages: list[str]) -> tuple[int, int]:
    path = root / "control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX34-001.yaml"
    data = _load_yaml(path, messages)
    evidence = data.get("validation_evidence", {}) if isinstance(data, dict) else {}
    passed = 5 if (
        evidence.get("github_actions_run_id") == 29197460029
        and evidence.get("github_actions_run_result") == "PASS"
        and evidence.get("python_matrix") == "PASS_5_OF_5_3_10_THROUGH_3_14"
    ) else 0
    return passed, 5


def _load_yaml(path: Path, messages: list[str]) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        messages.append(f"Cannot load {path}: {exc}")
        return {}
    if not isinstance(data, dict):
        messages.append(f"{path}: expected mapping")
        return {}
    return data
