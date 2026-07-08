"""Target-system package smoke validation."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .yaml_io import YamlLoadError, load_yaml


DEFAULT_PACKAGE_ROOT = Path("examples/target_systems/repo_steward_agent_package")
EXPECTED_TARGET_SYSTEM_ID = "repo_steward_agent_sample"
EXPECTED_SUBJECT_LAYERS = {"target_system_instance", "target_system_template"}
DERIVATIVE_AUTHORITY_STATUSES = {"derivative_draft", "generated_derivative", "scaffold_reference"}
REQUIRED_FILES = (
    "README.md",
    "target-system-manifest.yaml",
    "requirements-discovery-record.md",
    "product-requirements.md",
    "implementation-plan.md",
    "task-packets/TASK-001-read-only-repo-inspection.md",
    "task-packets/TASK-002-current-state-baseline.md",
    "task-packets/TASK-003-governed-next-action-plan.md",
    "registries/requirement-trace.csv",
    "registries/artifact-index.csv",
    "validation/validation-summary.md",
)
REQUIRED_TRACE_HEADERS = ("requirement_id", "source_artifact", "target_artifact", "coverage_status", "evidence_path", "notes")
REQUIRED_ARTIFACT_HEADERS = ("artifact_id", "path", "artifact_type", "authority_status", "subject_layer", "notes")
REQUIRED_BOUNDARY_PHRASES = ("smoke example", "derivative draft", "not a production target system")
PROHIBITED_CLAIMS = (
    "production_ready: true",
    "package_status: production",
    "source_authority_status: canonical",
    "authority_status: canonical",
    "is a production target system",
    "semantic correctness proven",
    "domain correctness proven",
    "autonomous operation ready",
)


def validate_target_package(package_root: str | Path = DEFAULT_PACKAGE_ROOT) -> dict[str, Any]:
    """Validate a local target-system package smoke surface."""

    root = resolve_package_root(package_root)
    missing_files: list[str] = []
    trace_gaps: list[str] = []
    warnings: list[str] = []
    manifest: dict[str, Any] = {}

    if not root.exists():
        missing_files.append(_display_path(root))
    elif not root.is_dir():
        trace_gaps.append(f"{_display_path(root)}: package root is not a directory")

    for relative in REQUIRED_FILES:
        if not (root / relative).exists():
            missing_files.append(relative)

    manifest_path = root / "target-system-manifest.yaml"
    if manifest_path.exists():
        try:
            loaded = load_yaml(manifest_path)
        except YamlLoadError as exc:
            trace_gaps.append(str(exc))
            loaded = {}
        if not isinstance(loaded, dict):
            trace_gaps.append("target-system-manifest.yaml: manifest must be a mapping")
            loaded = {}
        manifest = loaded
        _check_manifest(manifest, root, trace_gaps, warnings)

    _check_csv_headers(root / "registries/requirement-trace.csv", REQUIRED_TRACE_HEADERS, trace_gaps)
    _check_csv_headers(root / "registries/artifact-index.csv", REQUIRED_ARTIFACT_HEADERS, trace_gaps)
    _check_task_packets(root, trace_gaps)
    _check_boundary_text(root, trace_gaps)

    ok = not missing_files and not trace_gaps
    return {
        "ok": ok,
        "status": "PASS" if ok else "FAIL",
        "package_root": _display_path(root),
        "target_system_id": manifest.get("target_system_id"),
        "package_status": manifest.get("package_status"),
        "subject_layer": manifest.get("subject_layer"),
        "source_authority_status": manifest.get("source_authority_status"),
        "files_checked": len(REQUIRED_FILES),
        "missing_files": missing_files,
        "trace_gaps": trace_gaps,
        "warnings": warnings,
    }


def target_package_status(package_root: str | Path = DEFAULT_PACKAGE_ROOT) -> dict[str, Any]:
    """Return compact status for a target package."""

    payload = validate_target_package(package_root)
    return {
        "ok": payload["ok"],
        "status": payload["status"],
        "package_root": payload["package_root"],
        "target_system_id": payload["target_system_id"],
        "missing_files": payload["missing_files"],
        "trace_gaps": payload["trace_gaps"],
        "warnings": payload["warnings"],
    }


def resolve_package_root(package_root: str | Path = DEFAULT_PACKAGE_ROOT) -> Path:
    """Resolve package paths from either workspace-root or product-root context."""

    candidate = Path(package_root)
    if candidate.is_absolute():
        return candidate

    cwd = Path.cwd().resolve()
    candidates = [cwd / candidate]
    if candidate.parts and candidate.parts[0] == "Sys4AI":
        candidates.append(cwd.parent / candidate)
    else:
        candidates.append(cwd / "Sys4AI" / candidate)

    for item in candidates:
        if item.exists():
            return item
    return candidates[0]


def _check_manifest(manifest: dict[str, Any], root: Path, trace_gaps: list[str], warnings: list[str]) -> None:
    if manifest.get("target_system_id") != EXPECTED_TARGET_SYSTEM_ID:
        trace_gaps.append(f"target-system-manifest.yaml: target_system_id must be {EXPECTED_TARGET_SYSTEM_ID}")
    if manifest.get("package_status") != "smoke_example":
        trace_gaps.append("target-system-manifest.yaml: package_status must be smoke_example")
    if manifest.get("subject_layer") not in EXPECTED_SUBJECT_LAYERS:
        trace_gaps.append("target-system-manifest.yaml: subject_layer must be target_system_instance or target_system_template")
    if manifest.get("source_authority_status") not in DERIVATIVE_AUTHORITY_STATUSES:
        trace_gaps.append("target-system-manifest.yaml: source_authority_status must remain derivative or scaffold authority")

    contents = manifest.get("contents")
    if not isinstance(contents, dict):
        trace_gaps.append("target-system-manifest.yaml: contents must be a mapping")
    else:
        for key in ("rdr", "prd", "implementation_plan", "task_packet_root", "requirement_trace"):
            if key not in contents:
                trace_gaps.append(f"target-system-manifest.yaml: missing contents.{key}")

    validation = manifest.get("validation")
    if not isinstance(validation, dict):
        trace_gaps.append("target-system-manifest.yaml: validation must be a mapping")
    else:
        if validation.get("status") not in {"not_run", "pass", "warn", "fail"}:
            trace_gaps.append("target-system-manifest.yaml: validation.status must be not_run, pass, warn, or fail")
        commands = validation.get("commands")
        if not isinstance(commands, list) or not commands:
            trace_gaps.append("target-system-manifest.yaml: validation.commands must list the package validator")

    authority_notice = str(manifest.get("authority_notice", "")).lower()
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in authority_notice:
            trace_gaps.append(f"target-system-manifest.yaml: authority_notice must contain '{phrase}'")

    source_trace = manifest.get("source_trace")
    if not isinstance(source_trace, list) or not source_trace:
        trace_gaps.append("target-system-manifest.yaml: source_trace must list source files")
        return
    for item in source_trace:
        if not isinstance(item, str):
            trace_gaps.append("target-system-manifest.yaml: source_trace entries must be strings")
            continue
        resolved = _resolve_source_trace(item, root)
        if not resolved.exists():
            trace_gaps.append(f"target-system-manifest.yaml: source_trace missing {item}")
    if len(source_trace) < 3:
        warnings.append("target-system-manifest.yaml: source_trace has fewer than three entries")


def _check_csv_headers(path: Path, expected: tuple[str, ...], trace_gaps: list[str]) -> None:
    if not path.exists():
        return
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            headers = tuple(reader.fieldnames or ())
            rows = list(reader)
    except OSError as exc:
        trace_gaps.append(f"{_display_path(path)}: cannot read CSV: {exc}")
        return
    if headers != expected:
        trace_gaps.append(f"{_display_path(path)}: CSV headers must be {','.join(expected)}")
    if not rows:
        trace_gaps.append(f"{_display_path(path)}: CSV must contain at least one row")


def _check_task_packets(root: Path, trace_gaps: list[str]) -> None:
    task_root = root / "task-packets"
    if not task_root.exists():
        return
    task_packets = sorted(task_root.glob("TASK-*.md"))
    if len(task_packets) < 3:
        trace_gaps.append("task-packets: at least three task packet files are required")
    for path in task_packets:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in ("agentjob", "validation", "authority"):
            if phrase not in text:
                trace_gaps.append(f"{_display_path(path)}: task packet must mention {phrase}")


def _check_boundary_text(root: Path, trace_gaps: list[str]) -> None:
    if not root.exists():
        return
    text_parts = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".yaml", ".csv"}:
            text_parts.append(path.read_text(encoding="utf-8"))
    text = "\n".join(text_parts).lower()
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in text:
            trace_gaps.append(f"package boundary text must contain '{phrase}'")
    for claim in PROHIBITED_CLAIMS:
        if claim in text:
            trace_gaps.append(f"package contains prohibited authority claim: {claim}")


def _resolve_source_trace(path: str, package_root: Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    product_root = package_root.parents[2]
    workspace_root = product_root.parent
    if path.startswith("Sys4AI/"):
        return workspace_root / path
    if path.startswith(("PRDs/", "implementation_plans/")):
        return workspace_root / path
    return product_root / path


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()
