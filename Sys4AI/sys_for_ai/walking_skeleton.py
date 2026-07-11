"""Manifest-driven Phase 2 strategic walking-skeleton validation."""

from __future__ import annotations

import csv
from dataclasses import dataclass, fields
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .registry_io import read_registry_rows, rows_by_id
from .target_package import DEFAULT_PACKAGE_ROOT, validate_target_package
from .trace_flow import (
    WalkingSkeletonArtifact,
    WalkingSkeletonFlowReport,
    WalkingSkeletonLifecycleStage,
)
from .validation_semantics import STRUCTURAL_LIMITATION
from .validators import ValidationResult
from .yaml_io import YamlLoadError, load_yaml


FLOW_ID = "SFA-P2-STRATEGIC-WALKING-SKELETON-001"
REPORT_DERIVATIVE_ID = "der_walking_skeleton_flow"
REPORT_PATH = Path("docs/generated/governance/walking-skeleton-flow.md")
REPORT_GENERATOR = "sys_for_ai.walking_skeleton:0.3.0"
GENERATED_NOTICE = "This page is a generated reader surface. It is not canonical."

TX16_PATH = "Sys4AI/control_records/execution_transactions/TX-16-WALKING-SKELETON.yaml"
TX16_RECEIPT_PATH = "Sys4AI/control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX16-001.yaml"
TX16_HANDOFF_PATH = "Sys4AI/control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX16-001.yaml"
FRAMEWORK_TRACE_PATH = "Sys4AI/registries/requirement_trace_registry.csv"

PHASE2_ADDENDUM_REQUIREMENT_IDS = (
    "SFA-P2-ADD-STRAT-001",
    "SFA-P2-ADD-STRAT-002",
    "SFA-P2-ADD-APPROVAL-001",
    "SFA-P2-ADD-HOST-001",
    "SFA-P2-ADD-PATTERN-001",
    "SFA-P2-ADD-LIFE-001",
    "SFA-P2-ADD-EXEC-001",
    "SFA-P2-ADD-STATE-001",
    "SFA-P2-ADD-TRACE-001",
    "SFA-P2-ADD-PACKAGE-001",
    "SFA-P2-ADD-SEM-001",
    "SFA-P2-ADD-FLOW-001",
    "SFA-P2-ADD-SAFETY-001",
)

REQUIRED_ACTIVE_ARTIFACT_TYPES = {
    "target_system_manifest",
    "requirements_discovery_record",
    "target_vision",
    "target_core_values",
    "approval_or_waiver_evidence",
    "agentic_system_pattern_decision",
    "host_capability_profile",
    "host_capability_evidence",
    "product_requirements",
    "implementation_plan",
    "portable_execution_transaction",
    "implementation_evidence",
    "test_and_evaluation_evidence",
    "strategic_trace",
    "validation_summary",
    "framework_requirement_trace",
    "completion_receipt",
    "handoff",
    "generated_derivative",
}

HISTORICAL_FLOW_PATHS = (
    (
        "historical-phase2-rdr",
        "requirements_discovery_record",
        "Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md",
    ),
    (
        "historical-phase2-prd",
        "prd",
        "PRDs/Sys4AI_phase-2_walking_skeleton_prd.md",
    ),
    (
        "historical-phase2-plan",
        "implementation_plan",
        "implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md",
    ),
    (
        "historical-aj20-flow",
        "agentjob",
        "Sys4AI/control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml",
    ),
    (
        "historical-aj21-package-smoke",
        "agentjob",
        "Sys4AI/control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml",
    ),
    (
        "historical-aj22-demo",
        "agentjob",
        "Sys4AI/control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml",
    ),
    (
        "historical-demo-report",
        "acceptance_report",
        "implementation_plans/acceptance_reports/PHASE2-WALKING-SKELETON-DEMO-SFADEV-22.md",
    ),
)


@dataclass(frozen=True)
class _ArtifactSpec:
    artifact_id: str
    flow_step: str
    artifact_type: str
    path: Path
    subject_layer: str
    authority_status: str
    evidence_class: str
    upstream_ids: tuple[str, ...]
    downstream_ids: tuple[str, ...]
    report_self_check: bool = False


LIFECYCLE_STAGES = (
    WalkingSkeletonLifecycleStage(
        stage="Design",
        inputs="validated target RDR, vision, core values, approval or waiver, and host constraints",
        responsible_role="requirements_manager",
        approving_role="accountable human principal",
        permissions="read registered sources; write only controlled target design artifacts",
        activities="classify the target, resolve intent, select the pattern, and define requirements",
        outputs="pattern decision and product requirements",
        entry_criteria="target and subject layer classified; RDR validated",
        exit_criteria="intent state and pattern decision are explicit and traceable",
        failure_behavior="stop on missing approval, waiver, authority, or required host evidence",
        rollback_or_return="return to discovery or candidate intent without promoting authority",
        evidence="target manifest, RDR, strategic-intent artifacts, approval evidence, and pattern decision",
    ),
    WalkingSkeletonLifecycleStage(
        stage="Develop",
        inputs="controlled requirements, pattern decision, and host limitations",
        responsible_role="implementation_planner",
        approving_role="accountable transaction approval principal",
        permissions="plan only within the declared target and framework write surfaces",
        activities="define the bounded implementation sequence, validators, stops, and rollback",
        outputs="implementation plan and authorized portable execution transactions",
        entry_criteria="design evidence is current and the implementation boundary is authorized",
        exit_criteria="each transaction binds authority, permissions, validation, and safe stop behavior",
        failure_behavior="leave the transaction unexecuted when authority or capability is absent",
        rollback_or_return="supersede the plan or return to Design; do not rewrite activated evidence",
        evidence="implementation plan, package transactions, and TX-16 execution transaction",
    ),
    WalkingSkeletonLifecycleStage(
        stage="Implement",
        inputs="authorized transactions and current source-backed state",
        responsible_role="system_engineer",
        approving_role="transaction approval principal",
        permissions="execute only declared reads, writes, tools, and external actions",
        activities="produce the bounded package, flow, trace, and closeout evidence",
        outputs="implementation artifacts, artifact index, and source-backed transition state",
        entry_criteria="permission envelope and required host capabilities are current",
        exit_criteria="implementation artifacts exist and the exact next state is recorded",
        failure_behavior="stop at the nearest safe boundary and retain accepted evidence",
        rollback_or_return="revert the bounded packet or supersede it with explicit evidence",
        evidence="artifact index, framework trace, completion receipt, and handoff",
    ),
    WalkingSkeletonLifecycleStage(
        stage="Test",
        inputs="implementation artifacts and declared acceptance criteria",
        responsible_role="verification_engineer",
        approving_role="accountable acceptance principal for any later promotion",
        permissions="run repository-local checks without expanding target or production authority",
        activities="separate test execution, requirements verification, stakeholder validation, and evaluation",
        outputs="test, verification, validation, and evaluation evidence with explicit gaps",
        entry_criteria="implemented artifacts and deterministic validators are available",
        exit_criteria="structural checks pass and all unrun semantic, stakeholder, and production evidence remains explicit",
        failure_behavior="fail closed and do not advance flow or maturity",
        rollback_or_return="return to Implement for bounded repair or to Design for requirement conflict",
        evidence="test-and-evaluation summary, validation summary, generated flow report, and validator results",
    ),
)


def walking_skeleton_status(
    root: str | Path = ".",
    package_root: str | Path = DEFAULT_PACKAGE_ROOT,
) -> dict[str, Any]:
    """Return a compact strategic walking-skeleton status payload."""

    payload = validate_walking_skeleton_flow(root, package_root=package_root)
    return {
        "ok": payload["ok"],
        "status": payload["status"],
        "flow_id": payload["flow_id"],
        "target_system_id": payload["target_system_id"],
        "package_root": payload["package_root"],
        "result": payload["result"],
        "artifacts_checked": payload["artifacts_checked"],
        "missing_artifacts": payload["missing_artifacts"],
        "trace_gaps": payload["trace_gaps"],
        "warnings": payload["warnings"],
    }


def validate_walking_skeleton_flow(
    root: str | Path = ".",
    *,
    package_root: str | Path = DEFAULT_PACKAGE_ROOT,
    check_report: bool | None = None,
) -> dict[str, Any]:
    """Validate the active manifest-driven flow and preserved historical appendix."""

    base = product_root(root)
    resolved_package = _resolve_package_root(base, package_root)
    if check_report is None:
        check_report = resolved_package == (base / DEFAULT_PACKAGE_ROOT).resolve()
    report = build_walking_skeleton_flow_report(
        base,
        package_root=resolved_package,
        check_report=check_report,
    )
    payload = report.as_dict()
    ok = report.result == "pass"
    payload.update(
        {
            "ok": ok,
            "status": "PASS" if ok else "FAIL",
            "validated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "limitation": STRUCTURAL_LIMITATION,
        }
    )
    return payload


def write_walking_skeleton_flow_report(root: str | Path = ".") -> ValidationResult:
    """Write the deterministic generated report for the registered smoke package."""

    base = product_root(root)
    target = base / REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(expected_walking_skeleton_report_markdown(base), encoding="utf-8")
    return ValidationResult(True, [f"{target}: wrote generated derivative"])


def build_walking_skeleton_flow_report(
    root: str | Path = ".",
    *,
    package_root: str | Path = DEFAULT_PACKAGE_ROOT,
    check_report: bool = True,
) -> WalkingSkeletonFlowReport:
    """Build the current active flow plus a historical-evidence appendix."""

    base = product_root(root)
    package = _resolve_package_root(base, package_root)
    missing: list[str] = []
    trace_gaps: list[str] = []
    warnings: list[str] = []

    package_result = validate_target_package(package)
    missing.extend(f"target-package: {item}" for item in package_result.get("missing_files", []))
    trace_gaps.extend(f"target-package: {item}" for item in package_result.get("trace_gaps", []))

    manifest = _load_mapping(package / "target-system-manifest.yaml", trace_gaps)
    specs = _active_artifact_specs(base, package, manifest, trace_gaps)
    artifacts = tuple(_materialize(spec, base, missing, check_report) for spec in specs)
    historical = _historical_artifacts(base, missing)

    _check_active_graph(artifacts, trace_gaps)
    _check_lifecycle_stages(trace_gaps)
    _check_test_evidence_classes(package, manifest, trace_gaps)
    _check_framework_trace(base, trace_gaps)
    _check_closeout_records(base, trace_gaps)
    _check_derivative_row(base, trace_gaps)

    if package_result.get("ok"):
        warnings.append("Target package evidence is structural and derivative-only.")
    warnings.extend(
        (
            "G-07 host verification remains open.",
            "G-08 framework strategic approval is accepted; target-system approval and domain acceptance remain independent.",
            "Production readiness, operational authority, stakeholder consensus, and domain acceptance remain open.",
        )
    )

    if check_report:
        report_path = base / REPORT_PATH
        if not report_path.exists():
            missing.append(_repo_path(report_path, base))
        else:
            expected = expected_walking_skeleton_report_markdown(base)
            if report_path.read_text(encoding="utf-8") != expected:
                trace_gaps.append(f"{_repo_path(report_path, base)}: generated report drift")

    missing = sorted(dict.fromkeys(missing))
    trace_gaps = sorted(dict.fromkeys(trace_gaps))
    result = "pass" if not missing and not trace_gaps else "fail"
    return WalkingSkeletonFlowReport(
        flow_id=FLOW_ID,
        target_system_id=str(manifest.get("target_system_id", "unknown")),
        package_root=_repo_path(package, base),
        result=result,
        artifacts=artifacts,
        lifecycle_stages=LIFECYCLE_STAGES,
        historical_artifacts=historical,
        missing_artifacts=tuple(missing),
        trace_gaps=tuple(trace_gaps),
        warnings=tuple(sorted(dict.fromkeys(warnings))),
    )


def expected_walking_skeleton_report_markdown(root: str | Path = ".") -> str:
    """Return the deterministic generated walking-skeleton report text."""

    base = product_root(root)
    report = build_walking_skeleton_flow_report(base, check_report=False)
    artifact_rows = [
        [
            artifact.flow_step,
            artifact.artifact_id,
            artifact.artifact_type,
            artifact.authority_status,
            artifact.evidence_class,
            artifact.validation_status,
            artifact.path,
        ]
        for artifact in report.artifacts
    ]
    lifecycle_rows = [
        [
            stage.stage,
            stage.inputs,
            stage.responsible_role,
            stage.approving_role,
            stage.permissions,
            stage.activities,
            stage.outputs,
            stage.entry_criteria,
            stage.exit_criteria,
            stage.failure_behavior,
            stage.rollback_or_return,
            stage.evidence,
        ]
        for stage in report.lifecycle_stages
    ]
    historical_rows = [
        [artifact.artifact_id, artifact.artifact_type, artifact.authority_status, artifact.validation_status, artifact.path]
        for artifact in report.historical_artifacts
    ]
    lines = [
        "# Strategic Walking Skeleton Flow",
        "",
        "page_metadata:",
        f"  derivative_id: {REPORT_DERIVATIVE_ID}",
        "  derivative_type: walking_skeleton_flow_report",
        "  authority_status: generated_noncanonical",
        f"  generator: {REPORT_GENERATOR}",
        f"  flow_id: {FLOW_ID}",
        f"  target_system_id: {report.target_system_id}",
        "",
        GENERATED_NOTICE,
        "",
        "## Flow Result",
        "",
        f"- result: {report.result}",
        f"- package_root: {report.package_root}",
        f"- active_artifacts_checked: {len(report.artifacts)}",
        f"- historical_artifacts_preserved: {len(report.historical_artifacts)}",
        f"- missing_artifacts: {len(report.missing_artifacts)}",
        f"- trace_gaps: {len(report.trace_gaps)}",
        "",
        "## Active Revised Artifact Flow",
        "",
        _markdown_table(
            [
                "step",
                "artifact_id",
                "artifact_type",
                "authority_status",
                "evidence_class",
                "validation_status",
                "path",
            ],
            artifact_rows,
        ),
        "",
        "The active flow contains portable execution transactions and no retired packet node.",
        "",
        "## Scoped Lifecycle Evidence",
        "",
        _markdown_table(
            [
                "stage",
                "inputs",
                "responsible_role",
                "approving_role",
                "permissions",
                "activities",
                "outputs",
                "entry_criteria",
                "exit_criteria",
                "failure_behavior",
                "rollback_or_return",
                "evidence",
            ],
            lifecycle_rows,
        ),
        "",
        "## Distinct Test And Evaluation Evidence",
        "",
        "- Test execution: repository-local unit, CLI, and aggregate checks.",
        "- Requirements verification: generalized framework trace plus package-local trace.",
        "- Stakeholder or system validation: not run; framework G-08 is accepted, while target-system validation and domain acceptance remain open.",
        "- Behavioral or performance evaluation: not run; TX-17 and production evidence remain later work.",
        "",
        "## Historical Evidence Appendix",
        "",
        "Historical packet-era artifacts remain available as activated evidence. They are not active runtime nodes.",
        "",
        _markdown_table(
            ["artifact_id", "artifact_type", "authority_status", "validation_status", "path"],
            historical_rows,
        ),
        "",
        "## Warnings And Open Gates",
        "",
        _markdown_list(report.warnings),
        "",
        "## Missing Artifacts",
        "",
        _markdown_list(report.missing_artifacts),
        "",
        "## Trace Gaps",
        "",
        _markdown_list(report.trace_gaps),
        "",
        "## Boundary",
        "",
        STRUCTURAL_LIMITATION,
        "",
        "The example remains a derivative smoke package at validated_prototype maturity. Its fictional demonstration approval does not establish target-system validation, G-07, production readiness, operational authority, stakeholder consensus, or domain acceptance; framework G-08 is independently accepted.",
        "",
    ]
    return "\n".join(lines)


def product_root(root: str | Path = ".") -> Path:
    """Resolve the Sys4AI product root from a workspace or product path."""

    start = Path(root).resolve()
    if (start / "registries").exists() and (start / "sys_for_ai").exists():
        return start
    if (start / "Sys4AI/registries").exists():
        return start / "Sys4AI"
    current = start
    while current.parent != current:
        if (current / "registries").exists() and (current / "sys_for_ai").exists():
            return current
        if (current / "Sys4AI/registries").exists():
            return current / "Sys4AI"
        current = current.parent
    return start


def _active_artifact_specs(
    base: Path,
    package: Path,
    manifest: dict[str, Any],
    trace_gaps: list[str],
) -> tuple[_ArtifactSpec, ...]:
    contents = manifest.get("contents") if isinstance(manifest.get("contents"), dict) else {}
    subject_layer = str(manifest.get("subject_layer", "target_system_instance"))
    authority = str(manifest.get("source_authority_status", "derivative_draft"))

    def package_path(key: str) -> Path:
        raw = contents.get(key)
        if not isinstance(raw, str) or not raw.strip():
            trace_gaps.append(f"target-system-manifest.yaml: missing contents.{key} for active flow")
            return package / f"missing-{key}"
        return _safe_package_path(package, raw, f"contents.{key}", trace_gaps)

    execution_root = package_path("execution_root")
    transactions = sorted(path for path in execution_root.glob("*") if path.is_file()) if execution_root.is_dir() else []
    if not transactions:
        trace_gaps.append("active flow requires at least one manifest-declared portable execution transaction")
    transaction_ids = tuple(f"target-execution-{index:03d}" for index, _ in enumerate(transactions, start=1))
    first_transaction = transaction_ids[:1]
    last_transaction = transaction_ids[-1:] or ("target-implementation-plan",)
    approval_kind = "waiver" if manifest.get("content_approval_status") == "waived" else "approval"

    specs: list[_ArtifactSpec] = [
        _ArtifactSpec(
            "target-manifest",
            "01 init classification",
            "target_system_manifest",
            package / "target-system-manifest.yaml",
            subject_layer,
            authority,
            "classification_evidence",
            (),
            ("target-rdr",),
        ),
        _ArtifactSpec(
            "target-rdr",
            "02 requirements discovery",
            "requirements_discovery_record",
            package_path("rdr"),
            subject_layer,
            authority,
            "discovery_evidence",
            ("target-manifest",),
            ("target-vision", "target-core-values"),
        ),
        _ArtifactSpec(
            "target-vision",
            "03 target vision",
            "target_vision",
            package_path("vision"),
            subject_layer,
            authority,
            "strategic_intent_evidence",
            ("target-rdr",),
            ("approval-or-waiver",),
        ),
        _ArtifactSpec(
            "target-core-values",
            "04 target core values",
            "target_core_values",
            package_path("core_values"),
            subject_layer,
            authority,
            "strategic_intent_evidence",
            ("target-rdr",),
            ("approval-or-waiver",),
        ),
        _ArtifactSpec(
            "approval-or-waiver",
            f"05 accountable {approval_kind} evidence",
            "approval_or_waiver_evidence",
            package_path("approval_evidence"),
            subject_layer,
            authority,
            "approval_evidence" if approval_kind == "approval" else "waiver_evidence",
            ("target-vision", "target-core-values"),
            ("pattern-decision", "host-profile"),
        ),
        _ArtifactSpec(
            "pattern-decision",
            "06 pattern decision",
            "agentic_system_pattern_decision",
            package_path("pattern_decision"),
            subject_layer,
            authority,
            "architecture_decision_evidence",
            ("approval-or-waiver",),
            ("target-prd",),
        ),
        _ArtifactSpec(
            "host-profile",
            "06 host profile",
            "host_capability_profile",
            _resolve_repo_path(str(manifest.get("host_profile", "missing-host-profile")), base),
            "framework_product",
            "controlled",
            "host_profile_evidence",
            ("approval-or-waiver",),
            ("host-capability-summary",),
        ),
        _ArtifactSpec(
            "host-capability-summary",
            "06 host capability evidence",
            "host_capability_evidence",
            package_path("host_capability_summary"),
            subject_layer,
            authority,
            "host_verification_gap_evidence",
            ("host-profile",),
            first_transaction or ("target-implementation-plan",),
        ),
        _ArtifactSpec(
            "target-prd",
            "07 controlled requirements",
            "product_requirements",
            package_path("prd"),
            subject_layer,
            authority,
            "requirements_evidence",
            ("pattern-decision",),
            ("target-implementation-plan",),
        ),
        _ArtifactSpec(
            "target-implementation-plan",
            "08 implementation plan",
            "implementation_plan",
            package_path("implementation_plan"),
            subject_layer,
            authority,
            "planning_evidence",
            ("target-prd",),
            first_transaction + ("tx16-execution-transaction",),
        ),
    ]
    for index, (transaction_id, path) in enumerate(zip(transaction_ids, transactions)):
        upstream = (
            ("target-implementation-plan", "host-capability-summary")
            if index == 0
            else (transaction_ids[index - 1],)
        )
        downstream = (transaction_ids[index + 1],) if index + 1 < len(transaction_ids) else ("artifact-index",)
        specs.append(
            _ArtifactSpec(
                transaction_id,
                "09 portable execution transaction",
                "portable_execution_transaction",
                path,
                subject_layer,
                authority,
                "instructional_execution_evidence",
                upstream,
                downstream,
            )
        )
    specs.extend(
        (
            _ArtifactSpec(
                "tx16-execution-transaction",
                "09 authorized framework transaction",
                "portable_execution_transaction",
                _resolve_repo_path(TX16_PATH, base),
                "framework_product",
                "controlled",
                "execution_authorization_evidence",
                ("target-implementation-plan",),
                ("framework-trace",),
            ),
            _ArtifactSpec(
                "artifact-index",
                "10 implementation evidence",
                "implementation_evidence",
                package_path("artifact_index"),
                subject_layer,
                authority,
                "implementation_evidence",
                last_transaction,
                ("strategic-trace", "test-and-evaluation"),
            ),
            _ArtifactSpec(
                "test-and-evaluation",
                "10 distinct test and evaluation evidence",
                "test_and_evaluation_evidence",
                package_path("test_and_evaluation_summary"),
                subject_layer,
                authority,
                "test_verification_validation_evaluation_evidence",
                ("artifact-index",),
                ("validation-summary",),
            ),
            _ArtifactSpec(
                "strategic-trace",
                "11 strategic trace and package",
                "strategic_trace",
                package_path("requirement_trace"),
                subject_layer,
                authority,
                "target_trace_evidence",
                ("artifact-index",),
                ("validation-summary",),
            ),
            _ArtifactSpec(
                "validation-summary",
                "12 validation evidence",
                "validation_summary",
                package_path("validation_summary"),
                subject_layer,
                authority,
                "structural_validation_evidence",
                ("test-and-evaluation", "strategic-trace"),
                ("framework-trace",),
            ),
            _ArtifactSpec(
                "framework-trace",
                "12 framework trace",
                "framework_requirement_trace",
                _resolve_repo_path(FRAMEWORK_TRACE_PATH, base),
                "framework_product",
                "controlled",
                "requirement_verification_evidence",
                ("validation-summary", "tx16-execution-transaction"),
                ("tx16-completion-receipt",),
            ),
            _ArtifactSpec(
                "tx16-completion-receipt",
                "12 closeout evidence",
                "completion_receipt",
                _resolve_repo_path(TX16_RECEIPT_PATH, base),
                "framework_product",
                "controlled",
                "closeout_evidence",
                ("framework-trace",),
                ("tx16-handoff",),
            ),
            _ArtifactSpec(
                "tx16-handoff",
                "12 next-state evidence",
                "handoff",
                _resolve_repo_path(TX16_HANDOFF_PATH, base),
                "framework_product",
                "controlled",
                "continuation_evidence",
                ("tx16-completion-receipt",),
                ("walking-skeleton-flow-report",),
            ),
            _ArtifactSpec(
                "walking-skeleton-flow-report",
                "12 generated reader",
                "generated_derivative",
                base / REPORT_PATH,
                "derivative_surface",
                "generated_derivative",
                "noncanonical_reader",
                ("tx16-handoff",),
                (),
                report_self_check=True,
            ),
        )
    )
    return tuple(specs)


def _materialize(
    spec: _ArtifactSpec,
    base: Path,
    missing: list[str],
    check_report: bool,
) -> WalkingSkeletonArtifact:
    present = spec.path.exists() or (spec.report_self_check and not check_report)
    if not present:
        missing.append(_repo_path(spec.path, base))
    return WalkingSkeletonArtifact(
        artifact_id=spec.artifact_id,
        flow_step=spec.flow_step,
        artifact_type=spec.artifact_type,
        path=_repo_path(spec.path, base),
        subject_layer=spec.subject_layer,
        authority_status=spec.authority_status,
        evidence_class=spec.evidence_class,
        upstream_ids=spec.upstream_ids,
        downstream_ids=spec.downstream_ids,
        validation_status="present" if present else "missing",
    )


def _historical_artifacts(base: Path, missing: list[str]) -> tuple[WalkingSkeletonArtifact, ...]:
    artifacts: list[WalkingSkeletonArtifact] = []
    for artifact_id, artifact_type, path_text in HISTORICAL_FLOW_PATHS:
        path = _resolve_repo_path(path_text, base)
        present = path.exists()
        if not present:
            missing.append(path_text)
        artifacts.append(
            WalkingSkeletonArtifact(
                artifact_id=artifact_id,
                flow_step="historical appendix",
                artifact_type=artifact_type,
                path=path_text,
                subject_layer="framework_product",
                authority_status="historical",
                evidence_class="activated_historical_evidence",
                upstream_ids=(),
                downstream_ids=(),
                validation_status="historical_preserved" if present else "missing",
            )
        )
    return tuple(artifacts)


def _check_active_graph(artifacts: tuple[WalkingSkeletonArtifact, ...], trace_gaps: list[str]) -> None:
    index = {artifact.artifact_id: artifact for artifact in artifacts}
    if len(index) != len(artifacts):
        trace_gaps.append("active flow artifact IDs must be unique")
    artifact_types = {artifact.artifact_type for artifact in artifacts}
    for artifact_type in sorted(REQUIRED_ACTIVE_ARTIFACT_TYPES - artifact_types):
        trace_gaps.append(f"active flow missing artifact type {artifact_type}")
    for artifact in artifacts:
        active_text = f"{artifact.artifact_id} {artifact.artifact_type} {artifact.path}".lower()
        if "agentjob" in active_text or "/continue" in active_text:
            trace_gaps.append(f"{artifact.artifact_id}: retired runtime vocabulary cannot be an active flow node")
        for upstream_id in artifact.upstream_ids:
            upstream = index.get(upstream_id)
            if upstream is None:
                trace_gaps.append(f"{artifact.artifact_id}: unknown upstream node {upstream_id}")
            elif artifact.artifact_id not in upstream.downstream_ids:
                trace_gaps.append(f"{artifact.artifact_id}: upstream edge {upstream_id} is not reciprocal")
        for downstream_id in artifact.downstream_ids:
            downstream = index.get(downstream_id)
            if downstream is None:
                trace_gaps.append(f"{artifact.artifact_id}: unknown downstream node {downstream_id}")
            elif artifact.artifact_id not in downstream.upstream_ids:
                trace_gaps.append(f"{artifact.artifact_id}: downstream edge {downstream_id} is not reciprocal")


def _check_lifecycle_stages(trace_gaps: list[str]) -> None:
    if tuple(stage.stage for stage in LIFECYCLE_STAGES) != ("Design", "Develop", "Implement", "Test"):
        trace_gaps.append("walking-skeleton lifecycle must define Design Develop Implement and Test in order")
    for stage in LIFECYCLE_STAGES:
        for field in fields(stage):
            if not str(getattr(stage, field.name)).strip():
                trace_gaps.append(f"lifecycle stage {stage.stage}: missing {field.name}")


def _check_test_evidence_classes(package: Path, manifest: dict[str, Any], trace_gaps: list[str]) -> None:
    contents = manifest.get("contents") if isinstance(manifest.get("contents"), dict) else {}
    raw = contents.get("test_and_evaluation_summary")
    if not isinstance(raw, str):
        return
    path = _safe_package_path(package, raw, "contents.test_and_evaluation_summary", trace_gaps)
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8").lower()
    for heading in (
        "test execution",
        "requirements verification",
        "stakeholder or system validation",
        "behavioral or performance evaluation",
    ):
        if heading not in text:
            trace_gaps.append(f"{_display_path(path)}: missing distinct evidence class {heading}")


def _check_framework_trace(base: Path, trace_gaps: list[str]) -> None:
    path = _resolve_repo_path(FRAMEWORK_TRACE_PATH, base)
    if not path.exists():
        return
    with path.open(newline="", encoding="utf-8") as handle:
        rows = {row.get("requirement_id", ""): row for row in csv.DictReader(handle)}
    for requirement_id in PHASE2_ADDENDUM_REQUIREMENT_IDS:
        row = rows.get(requirement_id)
        if row is None:
            trace_gaps.append(f"framework trace missing {requirement_id}")
            continue
        if row.get("verification_status") != "pass":
            trace_gaps.append(f"{requirement_id}: TX-16 end-to-end verification is not pass")
        for field in ("implementation_artifacts", "validation_evidence", "evidence_paths"):
            if not row.get(field, "").strip():
                trace_gaps.append(f"{requirement_id}: missing {field}")


def _check_closeout_records(base: Path, trace_gaps: list[str]) -> None:
    expected = (
        (TX16_PATH, "execution_transaction_id", "TX-16-WALKING-SKELETON"),
        (TX16_RECEIPT_PATH, "result", "PASS"),
        (TX16_HANDOFF_PATH, "next_execution_transaction_id", "TX-17-SAFETY-EVALUATION"),
    )
    for path_text, field, value in expected:
        path = _resolve_repo_path(path_text, base)
        if not path.exists():
            continue
        data = _load_mapping(path, trace_gaps)
        if data.get(field) != value:
            trace_gaps.append(f"{path_text}: {field} must be {value}")
    transaction = _resolve_repo_path(TX16_PATH, base)
    if transaction.exists():
        data = _load_mapping(transaction, trace_gaps)
        state = data.get("state") if isinstance(data.get("state"), dict) else {}
        if state.get("status") != "completed":
            trace_gaps.append(f"{TX16_PATH}: state.status must be completed")
    handoff = _resolve_repo_path(TX16_HANDOFF_PATH, base)
    if handoff.exists():
        data = _load_mapping(handoff, trace_gaps)
        if data.get("status") != "ready":
            trace_gaps.append(f"{TX16_HANDOFF_PATH}: status must be ready")


def _check_derivative_row(base: Path, trace_gaps: list[str]) -> None:
    rows = rows_by_id(read_registry_rows(base / "registries/derivative_registry.csv"), "derivative_id")
    row = rows.get(REPORT_DERIVATIVE_ID)
    if row is None:
        trace_gaps.append(f"{REPORT_DERIVATIVE_ID}: missing derivative registry row")
        return
    if row.get("path") != REPORT_PATH.as_posix():
        trace_gaps.append(f"{REPORT_DERIVATIVE_ID}: derivative path must be {REPORT_PATH.as_posix()}")
    if row.get("generation_method") != REPORT_GENERATOR:
        trace_gaps.append(f"{REPORT_DERIVATIVE_ID}: generation method must be {REPORT_GENERATOR}")
    if row.get("status") != "generated_derivative":
        trace_gaps.append(f"{REPORT_DERIVATIVE_ID}: status must remain generated_derivative")
    required_sources = (
        "SRC-PRD-P2-STRATEGIC-BASELINE-ADDENDUM",
        "SRC-STRATEGIC-BASELINE-MIGRATION-PLAN",
        "SRC-EXAMPLE-REPO-STEWARD-PACKAGE",
        "SRC-WALKING-SKELETON-FLOW-MODULE",
    )
    for source_id in required_sources:
        if source_id not in row.get("source_ids", "").split(";"):
            trace_gaps.append(f"{REPORT_DERIVATIVE_ID}: missing current source id {source_id}")


def _resolve_package_root(base: Path, package_root: str | Path) -> Path:
    candidate = Path(package_root)
    if candidate.is_absolute():
        return candidate.resolve()
    if candidate.parts and candidate.parts[0] == "Sys4AI":
        return (base.parent / candidate).resolve()
    return (base / candidate).resolve()


def _resolve_repo_path(path: str, base: Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    if path.startswith("Sys4AI/"):
        return base.parent / path
    if path.startswith(("PRDs/", "implementation_plans/", "temp_handoff/")):
        return base.parent / path
    return base / path


def _safe_package_path(root: Path, value: str, label: str, trace_gaps: list[str]) -> Path:
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        trace_gaps.append(f"target-system-manifest.yaml: {label} escapes package root")
        return root / f"invalid-{label.replace('.', '-')}"
    return candidate


def _load_mapping(path: Path, trace_gaps: list[str]) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        loaded = load_yaml(path)
    except YamlLoadError as exc:
        trace_gaps.append(str(exc))
        return {}
    if not isinstance(loaded, dict):
        trace_gaps.append(f"{_display_path(path)}: expected a YAML mapping")
        return {}
    return loaded


def _repo_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.parent.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_escape_cell(item) for item in row) + " |")
    return "\n".join(lines)


def _markdown_list(items: tuple[str, ...]) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
