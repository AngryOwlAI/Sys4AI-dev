"""Phase 2 walking-skeleton flow validation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .registry_io import read_registry_rows, resolve_registered_path, rows_by_id
from .trace_flow import WalkingSkeletonArtifact, WalkingSkeletonFlowReport
from .validators import ValidationResult
from .yaml_io import load_yaml


FLOW_ID = "SFA-P2-WALKING-SKELETON-001"
REPORT_DERIVATIVE_ID = "der_walking_skeleton_flow"
REPORT_PATH = Path("docs/generated/governance/walking-skeleton-flow.md")
REPORT_GENERATOR = "sys_for_ai.walking_skeleton:0.1.0"
GENERATED_NOTICE = "This page is a generated reader surface. It is not canonical."

PHASE2_REQUIREMENT_IDS = (
    "SFA-P2-WS-FLOW-001",
    "SFA-P2-WS-FLOW-002",
    "SFA-P2-WS-RDR-001",
    "SFA-P2-WS-PRD-001",
    "SFA-P2-WS-PLAN-001",
    "SFA-P2-WS-AJ-001",
    "SFA-P2-WS-PACKAGE-001",
    "SFA-P2-WS-TRACE-001",
    "SFA-P2-WS-VAL-001",
    "SFA-P2-WS-NFR-001",
    "SFA-P2-WS-NFR-002",
)


@dataclass(frozen=True)
class ExpectedArtifact:
    artifact_id: str
    artifact_type: str
    path: str
    subject_layer: str
    authority_status: str
    upstream_ids: tuple[str, ...]
    downstream_ids: tuple[str, ...]
    source_id: str | None = None
    must_exist: bool = True
    planned_by_agentjob: str | None = None


EXPECTED_ARTIFACTS = (
    ExpectedArtifact(
        artifact_id="phase2-rdr",
        artifact_type="requirements_discovery_record",
        path="Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md",
        subject_layer="framework_product",
        authority_status="controlled",
        upstream_ids=(),
        downstream_ids=("phase2-prd",),
        source_id="SRC-RDR-PHASE2-WALKING-SKELETON-001",
    ),
    ExpectedArtifact(
        artifact_id="phase2-prd",
        artifact_type="prd",
        path="PRDs/Sys4AI_phase-2_walking_skeleton_prd.md",
        subject_layer="framework_product",
        authority_status="controlled",
        upstream_ids=("phase2-rdr",),
        downstream_ids=("phase2-implementation-plan",),
        source_id="SRC-PRD-P2-WALKING-SKELETON",
    ),
    ExpectedArtifact(
        artifact_id="phase2-implementation-plan",
        artifact_type="implementation_plan",
        path="implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md",
        subject_layer="framework_product",
        authority_status="controlled",
        upstream_ids=("phase2-prd",),
        downstream_ids=("aj20-flow", "aj21-package-smoke", "aj22-demo"),
        source_id="SRC-P2-WALKING-SKELETON-IMPLEMENTATION-PLAN",
    ),
    ExpectedArtifact(
        artifact_id="aj20-flow",
        artifact_type="agentjob",
        path="Sys4AI/control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml",
        subject_layer="framework_product",
        authority_status="controlled",
        upstream_ids=("phase2-implementation-plan",),
        downstream_ids=("walking-skeleton-flow-report", "aj21-package-smoke"),
        source_id="SRC-AJ-WALKING-SKELETON-FLOW-001",
    ),
    ExpectedArtifact(
        artifact_id="aj21-package-smoke",
        artifact_type="agentjob",
        path="Sys4AI/control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml",
        subject_layer="framework_product",
        authority_status="controlled",
        upstream_ids=("phase2-implementation-plan", "aj20-flow"),
        downstream_ids=("planned-target-package", "aj22-demo"),
        source_id="SRC-AJ-TARGET-PACKAGE-SMOKE-001",
    ),
    ExpectedArtifact(
        artifact_id="aj22-demo",
        artifact_type="agentjob",
        path="Sys4AI/control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml",
        subject_layer="framework_product",
        authority_status="controlled",
        upstream_ids=("phase2-implementation-plan", "aj21-package-smoke"),
        downstream_ids=("planned-demo-receipt",),
        source_id="SRC-AJ-WALKING-SKELETON-DEMO-001",
    ),
    ExpectedArtifact(
        artifact_id="prior-planning-receipt",
        artifact_type="completion_receipt",
        path="Sys4AI/control_records/completions/RECEIPT-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml",
        subject_layer="framework_product",
        authority_status="controlled",
        upstream_ids=("phase2-implementation-plan",),
        downstream_ids=("aj20-flow",),
        source_id="SRC-COMPLETION-PHASE2-WALKING-SKELETON-PLAN-001",
    ),
    ExpectedArtifact(
        artifact_id="prior-planning-handoff",
        artifact_type="handoff",
        path="Sys4AI/control_records/handoffs/HANDOFF-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml",
        subject_layer="framework_product",
        authority_status="controlled",
        upstream_ids=("prior-planning-receipt",),
        downstream_ids=("aj20-flow",),
        source_id="SRC-HANDOFF-PHASE2-WALKING-SKELETON-PLAN-001",
    ),
    ExpectedArtifact(
        artifact_id="walking-skeleton-flow-report",
        artifact_type="generated_derivative",
        path="Sys4AI/docs/generated/governance/walking-skeleton-flow.md",
        subject_layer="derivative_surface",
        authority_status="generated_derivative",
        upstream_ids=("phase2-rdr", "phase2-prd", "phase2-implementation-plan", "aj20-flow"),
        downstream_ids=("aj21-package-smoke", "aj22-demo"),
        must_exist=True,
    ),
    ExpectedArtifact(
        artifact_id="planned-target-package",
        artifact_type="planned_target_package",
        path="Sys4AI/examples/target_systems/repo_steward_agent_package",
        subject_layer="target_system_instance",
        authority_status="planned_derivative_draft",
        upstream_ids=("aj21-package-smoke",),
        downstream_ids=("aj22-demo",),
        must_exist=False,
        planned_by_agentjob="AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001",
    ),
    ExpectedArtifact(
        artifact_id="planned-demo-receipt",
        artifact_type="planned_completion_receipt",
        path="Sys4AI/control_records/completions/RECEIPT-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml",
        subject_layer="framework_product",
        authority_status="planned_controlled",
        upstream_ids=("aj22-demo",),
        downstream_ids=(),
        must_exist=False,
        planned_by_agentjob="AJ-SFADEV-22-WALKING-SKELETON-DEMO-001",
    ),
)


def walking_skeleton_status(root: str | Path = ".") -> dict[str, Any]:
    """Return a compact walking-skeleton status payload."""

    payload = validate_walking_skeleton_flow(root)
    return {
        "ok": payload["ok"],
        "status": payload["status"],
        "flow_id": payload["flow_id"],
        "result": payload["result"],
        "artifacts_checked": payload["artifacts_checked"],
        "missing_artifacts": payload["missing_artifacts"],
        "trace_gaps": payload["trace_gaps"],
        "pending_artifacts": payload["pending_artifacts"],
        "warnings": payload["warnings"],
    }


def validate_walking_skeleton_flow(root: str | Path = ".") -> dict[str, Any]:
    """Validate the current Phase 2 walking-skeleton artifact flow."""

    base = product_root(root)
    report = build_walking_skeleton_flow_report(base, check_report=True)
    payload = report.as_dict()
    ok = report.result == "pass"
    payload.update(
        {
            "ok": ok,
            "status": "PASS" if ok else "FAIL",
            "validated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        }
    )
    return payload


def write_walking_skeleton_flow_report(root: str | Path = ".") -> ValidationResult:
    """Write the generated walking-skeleton flow report."""

    base = product_root(root)
    target = base / REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(expected_walking_skeleton_report_markdown(base), encoding="utf-8")
    return ValidationResult(True, [f"{target}: wrote generated derivative"])


def build_walking_skeleton_flow_report(
    root: str | Path = ".",
    *,
    check_report: bool = True,
) -> WalkingSkeletonFlowReport:
    """Build the current flow report model."""

    base = product_root(root)
    source_rows = _safe_rows(base / "registries/source_registry.csv")
    derivative_rows = _safe_rows(base / "registries/derivative_registry.csv")
    source_index = rows_by_id(source_rows, "source_id")
    derivative_index = rows_by_id(derivative_rows, "derivative_id")

    artifacts: list[WalkingSkeletonArtifact] = []
    missing: list[str] = []
    trace_gaps: list[str] = []
    warnings: list[str] = []
    pending: list[str] = []

    for expected in EXPECTED_ARTIFACTS:
        actual = _resolve_repo_path(expected.path, base)
        validation_status = "present" if actual.exists() else "planned"
        is_report_self_check = expected.artifact_id == "walking-skeleton-flow-report" and not check_report
        if is_report_self_check:
            validation_status = "present"
        elif expected.must_exist and not actual.exists():
            missing.append(expected.path)
            validation_status = "missing"
        if not expected.must_exist:
            pending.append(expected.path)
            if expected.planned_by_agentjob:
                _check_planned_path_declared(base, expected, trace_gaps)
                warnings.append(f"{expected.artifact_id}: planned by {expected.planned_by_agentjob}")
        if expected.source_id:
            _check_source_row(expected, source_index, base, trace_gaps)
        artifacts.append(
            WalkingSkeletonArtifact(
                artifact_id=expected.artifact_id,
                artifact_type=expected.artifact_type,
                path=expected.path,
                subject_layer=expected.subject_layer,
                authority_status=expected.authority_status,
                upstream_ids=expected.upstream_ids,
                downstream_ids=expected.downstream_ids,
                validation_status=validation_status,
            )
        )

    _check_derivative_row(derivative_index, base, trace_gaps)
    _check_text_trace(base, trace_gaps)
    _check_agentjob_count(base, trace_gaps)
    _check_handoff_routes_to_aj20(base, trace_gaps)

    if check_report:
        expected_report = expected_walking_skeleton_report_markdown(base)
        report_path = base / REPORT_PATH
        if not report_path.exists():
            missing.append(_repo_path(report_path, base))
        elif report_path.read_text(encoding="utf-8") != expected_report:
            trace_gaps.append(f"{_repo_path(report_path, base)}: generated report drift")

    result = "pass" if not missing and not trace_gaps else "fail"
    return WalkingSkeletonFlowReport(
        flow_id=FLOW_ID,
        result=result,
        artifacts=tuple(artifacts),
        missing_artifacts=tuple(missing),
        trace_gaps=tuple(trace_gaps),
        warnings=tuple(sorted(set(warnings))),
        pending_artifacts=tuple(sorted(set(pending))),
    )


def expected_walking_skeleton_report_markdown(root: str | Path = ".") -> str:
    """Return the deterministic generated walking-skeleton report text."""

    base = product_root(root)
    report = build_walking_skeleton_flow_report(base, check_report=False)
    artifact_rows = [
        [
            artifact.artifact_id,
            artifact.artifact_type,
            artifact.authority_status,
            artifact.validation_status,
            artifact.path,
        ]
        for artifact in report.artifacts
    ]
    lines = [
        "# Walking Skeleton Flow",
        "",
        "page_metadata:",
        f"  derivative_id: {REPORT_DERIVATIVE_ID}",
        "  derivative_type: walking_skeleton_flow_report",
        "  authority_status: generated_noncanonical",
        f"  generator: {REPORT_GENERATOR}",
        "  flow_id: SFA-P2-WALKING-SKELETON-001",
        "",
        GENERATED_NOTICE,
        "",
        "## Flow Result",
        "",
        f"- result: {report.result}",
        f"- artifacts_checked: {len(report.artifacts)}",
        f"- missing_artifacts: {len(report.missing_artifacts)}",
        f"- trace_gaps: {len(report.trace_gaps)}",
        f"- pending_artifacts: {len(report.pending_artifacts)}",
        "",
        "## Artifact Chain",
        "",
        _markdown_table(
            ["artifact_id", "artifact_type", "authority_status", "validation_status", "path"],
            artifact_rows,
        ),
        "",
        "## Pending Artifacts",
        "",
        _markdown_list(report.pending_artifacts),
        "",
        "## Warnings",
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
        "This report proves structural connectivity only. It does not prove target-system semantic correctness, production runtime readiness, autonomous operation safety, or human acceptance.",
        "",
    ]
    return "\n".join(lines)


def product_root(root: str | Path = ".") -> Path:
    """Resolve the Sys4AI product root from a repo or product path."""

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


def _safe_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_registry_rows(path)


def _resolve_repo_path(path: str, base: Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    if path.startswith("Sys4AI/"):
        return base.parent / path
    if path.startswith(("PRDs/", "implementation_plans/", "temp_handoff/")):
        return base.parent / path
    return base / path


def _repo_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.parent.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _check_source_row(
    expected: ExpectedArtifact,
    source_index: dict[str, dict[str, str]],
    base: Path,
    trace_gaps: list[str],
) -> None:
    row = source_index.get(expected.source_id or "")
    if row is None:
        trace_gaps.append(f"{expected.artifact_id}: missing source row {expected.source_id}")
        return
    registered_path = row.get("path", "")
    if registered_path != expected.path:
        try:
            resolved = resolve_registered_path(registered_path, base)
        except Exception:
            resolved = _resolve_repo_path(registered_path, base)
        if resolved.resolve() != _resolve_repo_path(expected.path, base).resolve():
            trace_gaps.append(f"{expected.source_id}: path {registered_path} does not match {expected.path}")
    if row.get("authority_status", "") in {"canonical", "canonical_draft"} and expected.authority_status == "generated_derivative":
        trace_gaps.append(f"{expected.source_id}: generated derivative cannot be canonical")


def _check_derivative_row(derivative_index: dict[str, dict[str, str]], base: Path, trace_gaps: list[str]) -> None:
    row = derivative_index.get(REPORT_DERIVATIVE_ID)
    if row is None:
        trace_gaps.append(f"{REPORT_DERIVATIVE_ID}: missing derivative registry row")
        return
    if row.get("path") != REPORT_PATH.as_posix():
        trace_gaps.append(f"{REPORT_DERIVATIVE_ID}: derivative path must be {REPORT_PATH.as_posix()}")
    if row.get("status") in {"canonical", "canonical_draft"}:
        trace_gaps.append(f"{REPORT_DERIVATIVE_ID}: generated derivative cannot be canonical")
    for source_id in ("SRC-RDR-PHASE2-WALKING-SKELETON-001", "SRC-PRD-P2-WALKING-SKELETON", "SRC-P2-WALKING-SKELETON-IMPLEMENTATION-PLAN"):
        if source_id not in row.get("source_ids", ""):
            trace_gaps.append(f"{REPORT_DERIVATIVE_ID}: missing source id {source_id}")


def _check_text_trace(base: Path, trace_gaps: list[str]) -> None:
    prd = _resolve_repo_path("PRDs/Sys4AI_phase-2_walking_skeleton_prd.md", base)
    plan = _resolve_repo_path("implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md", base)
    for path, label in ((prd, "Phase 2 PRD"), (plan, "Phase 2 implementation plan")):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for requirement_id in PHASE2_REQUIREMENT_IDS:
            if requirement_id not in text:
                trace_gaps.append(f"{label}: missing requirement trace {requirement_id}")
    if plan.exists():
        text = plan.read_text(encoding="utf-8")
        for agentjob_id in (
            "AJ-SFADEV-20-WALKING-SKELETON-FLOW-001",
            "AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001",
            "AJ-SFADEV-22-WALKING-SKELETON-DEMO-001",
        ):
            if agentjob_id not in text:
                trace_gaps.append(f"Phase 2 implementation plan: missing AgentJob trace {agentjob_id}")


def _check_agentjob_count(base: Path, trace_gaps: list[str]) -> None:
    existing = [
        item
        for item in (
            _resolve_repo_path("Sys4AI/control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml", base),
            _resolve_repo_path("Sys4AI/control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml", base),
            _resolve_repo_path("Sys4AI/control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml", base),
        )
        if item.exists()
    ]
    if len(existing) < 3:
        trace_gaps.append("Phase 2 flow requires at least three bounded AgentJob files")


def _check_handoff_routes_to_aj20(base: Path, trace_gaps: list[str]) -> None:
    handoff = _resolve_repo_path("Sys4AI/control_records/handoffs/HANDOFF-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml", base)
    if not handoff.exists():
        return
    data = load_yaml(handoff)
    control_notes = data.get("control_loop_notes", {}) if isinstance(data, dict) else {}
    if control_notes.get("next_agentjob_id") != "AJ-SFADEV-20-WALKING-SKELETON-FLOW-001":
        trace_gaps.append("HANDOFF-SFADEV-19 does not route to AJ-SFADEV-20-WALKING-SKELETON-FLOW-001")


def _check_planned_path_declared(base: Path, expected: ExpectedArtifact, trace_gaps: list[str]) -> None:
    if not expected.planned_by_agentjob:
        return
    job_path = _resolve_repo_path(f"Sys4AI/control_records/agentjobs/{expected.planned_by_agentjob}.yaml", base)
    if not job_path.exists():
        trace_gaps.append(f"{expected.artifact_id}: missing planning AgentJob {expected.planned_by_agentjob}")
        return
    data = load_yaml(job_path)
    allowed_writes = data.get("allowed_writes", []) if isinstance(data, dict) else []
    if not any(_planned_path_matches(expected.path, str(pattern)) for pattern in allowed_writes):
        trace_gaps.append(f"{expected.artifact_id}: {expected.planned_by_agentjob} does not declare {expected.path}")


def _planned_path_matches(path: str, pattern: str) -> bool:
    clean_path = path.rstrip("/")
    clean_pattern = pattern.rstrip("/")
    return clean_pattern == clean_path or clean_pattern == f"{clean_path}/**" or clean_pattern.startswith(f"{clean_path}/")


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
    return value.replace("|", "\\|")
