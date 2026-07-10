"""Generic target-system package validation with explicit authority boundaries."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
from pathlib import Path
import re
from typing import Any, Iterable

import yaml

from .jsonschema_io import check_schema, load_json, validate_instance
from .lifecycle_patterns import validate_pattern_decision
from .registry_io import resolve_registered_path
from .strategic_intent import validate_strategic_intent
from .validation_semantics import STRUCTURAL_LIMITATION
from .yaml_io import YamlLoadError, load_yaml


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PRODUCT_ROOT.parent
DEFAULT_PACKAGE_ROOT = Path("examples/target_systems/repo_steward_agent_package")
MANIFEST_SCHEMA_PATH = "schemas/contracts/target_system_package_manifest.schema.json"
EXPECTED_SUBJECT_LAYERS = {"target_system_instance", "target_system_template"}
DERIVATIVE_AUTHORITY_STATUSES = {"derivative_draft", "generated_derivative", "scaffold_reference"}
MINIMAL_CONTENT_KEYS = (
    "readme",
    "rdr",
    "vision",
    "core_values",
    "pattern_decision",
    "approval_evidence",
    "prd",
    "implementation_plan",
    "execution_root",
    "requirement_trace",
    "artifact_index",
    "validation_summary",
    "strategic_intent_summary",
    "host_capability_summary",
    "test_and_evaluation_summary",
)
REQUIRED_TRACE_HEADERS = (
    "requirement_id",
    "source_artifact",
    "target_artifact",
    "coverage_status",
    "evidence_path",
    "notes",
)
REQUIRED_ARTIFACT_HEADERS = (
    "artifact_id",
    "path",
    "artifact_type",
    "authority_status",
    "subject_layer",
    "notes",
)
REQUIRED_BOUNDARY_PHRASES = ("smoke example", "derivative draft", "not a production target system")
SMOKE_PROHIBITED_CLAIMS = (
    "production_ready: true",
    "package_status: production",
    "is a production target system",
    "semantic correctness proven",
    "domain correctness proven",
    "autonomous operation ready",
)
RETIRED_ACTIVE_TERMS = ("agentjob", "/continue")
MODEL_PRINCIPALS = {"model", "ai", "meta-agent", "runtime"}


def validate_target_package(package_root: str | Path = DEFAULT_PACKAGE_ROOT) -> dict[str, Any]:
    """Validate a manifest-driven target-system package without granting authority."""

    root = resolve_package_root(package_root)
    missing_files: list[str] = []
    trace_gaps: list[str] = []
    warnings: list[str] = []
    manifest: dict[str, Any] = {}

    if not root.exists():
        missing_files.append(_display_path(root))
    elif not root.is_dir():
        trace_gaps.append(f"{_display_path(root)}: package root is not a directory")

    manifest_path = root / "target-system-manifest.yaml"
    if root.is_dir() and not manifest_path.exists():
        missing_files.append("target-system-manifest.yaml")
    elif manifest_path.exists():
        manifest = _load_manifest(manifest_path, trace_gaps)
        _check_manifest_schema(manifest, trace_gaps)
        _check_manifest_semantics(manifest, trace_gaps)

    contents = manifest.get("contents") if isinstance(manifest.get("contents"), dict) else {}
    declared = _check_declared_contents(root, contents, missing_files, trace_gaps)
    strategic_metadata = _check_strategic_intent(root, manifest, declared, trace_gaps)
    _check_approval_or_waiver(root, manifest, strategic_metadata, declared, trace_gaps)
    _check_pattern_decision(root, manifest, declared, trace_gaps)
    _check_host_requirements(root, manifest, declared, trace_gaps)
    _check_hashes(root, manifest, contents, declared, trace_gaps)
    _check_requirement_trace(declared.get("requirement_trace"), trace_gaps)
    _check_artifact_index(declared.get("artifact_index"), manifest, contents, trace_gaps)
    _check_execution_transactions(declared.get("execution_root"), trace_gaps)
    _check_validation_summaries(manifest, declared, trace_gaps)
    _check_boundary_text(root, manifest, trace_gaps)

    missing_files = sorted(dict.fromkeys(missing_files))
    trace_gaps = sorted(dict.fromkeys(trace_gaps))
    warnings = sorted(dict.fromkeys(warnings))
    ok = not missing_files and not trace_gaps
    return {
        "ok": ok,
        "status": "PASS" if ok else "FAIL",
        "package_root": _display_path(root),
        "target_system_id": manifest.get("target_system_id"),
        "package_status": manifest.get("package_status"),
        "subject_layer": manifest.get("subject_layer"),
        "source_authority_status": manifest.get("source_authority_status"),
        "files_checked": 1 + len(declared),
        "missing_files": missing_files,
        "trace_gaps": trace_gaps,
        "warnings": warnings,
        "limitation": STRUCTURAL_LIMITATION,
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
        "limitation": payload["limitation"],
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


def _load_manifest(path: Path, trace_gaps: list[str]) -> dict[str, Any]:
    try:
        loaded = load_yaml(path)
    except YamlLoadError as exc:
        trace_gaps.append(str(exc))
        return {}
    if not isinstance(loaded, dict):
        trace_gaps.append("target-system-manifest.yaml: manifest must be a mapping")
        return {}
    return loaded


def _check_manifest_schema(manifest: dict[str, Any], trace_gaps: list[str]) -> None:
    schema_path = resolve_registered_path(MANIFEST_SCHEMA_PATH)
    try:
        schema = load_json(schema_path)
    except RuntimeError as exc:
        trace_gaps.append(str(exc))
        return
    for error in check_schema(schema):
        trace_gaps.append(f"{_display_path(schema_path)}: invalid JSON Schema: {error}")
    for error in validate_instance(manifest, schema):
        trace_gaps.append(f"target-system-manifest.yaml: {error}")


def _check_manifest_semantics(manifest: dict[str, Any], trace_gaps: list[str]) -> None:
    if manifest.get("subject_layer") not in EXPECTED_SUBJECT_LAYERS:
        trace_gaps.append(
            "target-system-manifest.yaml: subject_layer must be target_system_instance or target_system_template"
        )
    if manifest.get("package_status") == "smoke_example":
        if manifest.get("source_authority_status") not in DERIVATIVE_AUTHORITY_STATUSES:
            trace_gaps.append(
                "target-system-manifest.yaml: smoke examples must remain derivative or scaffold authority"
            )
        if manifest.get("operational_maturity") not in {"concept", "prototype", "validated_prototype"}:
            trace_gaps.append(
                "target-system-manifest.yaml: smoke examples cannot exceed validated_prototype maturity"
            )

    source_trace = manifest.get("source_trace")
    if not isinstance(source_trace, list) or not source_trace:
        trace_gaps.append("target-system-manifest.yaml: source_trace must list source files")
    else:
        for item in source_trace:
            if not isinstance(item, str):
                trace_gaps.append("target-system-manifest.yaml: source_trace entries must be strings")
                continue
            if not _resolve_source_trace(item).exists():
                trace_gaps.append(f"target-system-manifest.yaml: stale source_trace pointer {item}")

    host_profile = manifest.get("host_profile")
    if not isinstance(host_profile, str) or not _resolve_source_trace(host_profile).exists():
        trace_gaps.append("target-system-manifest.yaml: host_profile must reference an existing profile")

    contents = manifest.get("contents") if isinstance(manifest.get("contents"), dict) else {}
    cross_pointers = {
        "vision_path": contents.get("vision"),
        "core_values_path": contents.get("core_values"),
    }
    approval = manifest.get("approval_evidence")
    if isinstance(approval, dict):
        if approval.get("path") != contents.get("approval_evidence"):
            trace_gaps.append("target-system-manifest.yaml: approval_evidence.path must match contents.approval_evidence")
    pattern = manifest.get("pattern_decision")
    if isinstance(pattern, dict) and pattern.get("path") != contents.get("pattern_decision"):
        trace_gaps.append("target-system-manifest.yaml: pattern_decision.path must match contents.pattern_decision")
    execution = manifest.get("execution_profile")
    if isinstance(execution, dict) and execution.get("transaction_root") != contents.get("execution_root"):
        trace_gaps.append("target-system-manifest.yaml: execution_profile.transaction_root must match contents.execution_root")
    for field, expected in cross_pointers.items():
        actual = manifest.get(field)
        if actual != expected:
            trace_gaps.append(f"target-system-manifest.yaml: {field} must match its contents path")

    validation = manifest.get("validation") if isinstance(manifest.get("validation"), dict) else {}
    expected_summaries = {
        contents.get("validation_summary"),
        contents.get("strategic_intent_summary"),
        contents.get("host_capability_summary"),
        contents.get("test_and_evaluation_summary"),
    }
    actual_summaries = set(validation.get("summary_paths", [])) if isinstance(validation.get("summary_paths"), list) else set()
    if actual_summaries != expected_summaries:
        trace_gaps.append("target-system-manifest.yaml: validation.summary_paths must match the four declared summaries")


def _check_declared_contents(
    root: Path,
    contents: dict[str, Any],
    missing_files: list[str],
    trace_gaps: list[str],
) -> dict[str, Path]:
    declared: dict[str, Path] = {}
    if not contents:
        trace_gaps.append("target-system-manifest.yaml: contents must be a mapping")
        return declared
    for key in MINIMAL_CONTENT_KEYS:
        raw = contents.get(key)
        if not isinstance(raw, str) or not raw.strip():
            trace_gaps.append(f"target-system-manifest.yaml: missing contents.{key}")
            continue
        path = _safe_package_path(root, raw, f"contents.{key}", trace_gaps)
        if path is None:
            continue
        declared[key] = path
        if not path.exists():
            missing_files.append(raw)
        elif key == "execution_root" and not path.is_dir():
            trace_gaps.append(f"target-system-manifest.yaml: contents.{key} must reference a directory")
        elif key != "execution_root" and not path.is_file():
            trace_gaps.append(f"target-system-manifest.yaml: contents.{key} must reference a file")
    return declared


def _check_strategic_intent(
    root: Path,
    manifest: dict[str, Any],
    declared: dict[str, Path],
    trace_gaps: list[str],
) -> dict[str, dict[str, Any]]:
    vision_path = declared.get("vision")
    values_path = declared.get("core_values")
    if vision_path is None or values_path is None or not vision_path.exists() or not values_path.exists():
        return {}

    pair_result = validate_strategic_intent(vision_path.parent)
    if not pair_result.ok:
        trace_gaps.extend(pair_result.messages)

    vision = _load_front_matter(vision_path, trace_gaps)
    values = _load_front_matter(values_path, trace_gaps)
    target_id = manifest.get("target_system_id")
    expected = (
        (vision_path, vision, "vision_id", manifest.get("vision_id"), manifest.get("vision_version")),
        (
            values_path,
            values,
            "core_values_set_id",
            manifest.get("core_values_set_id"),
            manifest.get("core_values_version"),
        ),
    )
    for path, metadata, id_field, expected_id, expected_version in expected:
        if metadata.get("target_system_id") != target_id:
            trace_gaps.append(f"{_display_path(path)}: target_system_id does not match manifest")
        if metadata.get(id_field) != expected_id:
            trace_gaps.append(f"{_display_path(path)}: {id_field} does not match manifest")
        if metadata.get("version") != expected_version:
            trace_gaps.append(f"{_display_path(path)}: active version does not match manifest")
        manifest_approval = manifest.get("content_approval_status")
        artifact_approval = metadata.get("content_approval_state")
        if manifest_approval == "waived":
            if artifact_approval not in {"candidate", "stakeholder_review"}:
                trace_gaps.append(f"{_display_path(path)}: waived package content must remain unapproved")
        elif artifact_approval != manifest_approval:
            trace_gaps.append(f"{_display_path(path)}: content approval state does not match manifest")
        supersession = metadata.get("supersession")
        if not isinstance(supersession, dict) or supersession.get("state") != "current":
            trace_gaps.append(f"{_display_path(path)}: manifest points to a stale or superseded version")

    value_ids = values.get("value_ids") if isinstance(values.get("value_ids"), list) else []
    if value_ids != manifest.get("core_value_ids"):
        trace_gaps.append(f"{_display_path(values_path)}: core value IDs do not match manifest order")

    identifiers = [
        manifest.get("vision_id"),
        manifest.get("core_values_set_id"),
        *(manifest.get("core_value_ids") if isinstance(manifest.get("core_value_ids"), list) else []),
    ]
    _check_duplicate_ids(identifiers, "strategic-intent", trace_gaps)
    return {"vision": vision, "core_values": values}


def _check_approval_or_waiver(
    root: Path,
    manifest: dict[str, Any],
    strategic: dict[str, dict[str, Any]],
    declared: dict[str, Path],
    trace_gaps: list[str],
) -> None:
    status = manifest.get("content_approval_status")
    if status == "approved":
        approval = manifest.get("approval_evidence")
        approval_path = declared.get("approval_evidence")
        if not isinstance(approval, dict) or approval_path is None or not approval_path.exists():
            trace_gaps.append("target-system-manifest.yaml: approved content requires approval_evidence")
            return
        evidence = _load_yaml_mapping(approval_path, trace_gaps)
        checks = {
            "approval_evidence_id": approval.get("id"),
            "target_system_id": manifest.get("target_system_id"),
            "vision_id": manifest.get("vision_id"),
        }
        for field, expected in checks.items():
            if evidence.get(field) != expected:
                trace_gaps.append(f"{_display_path(approval_path)}: {field} does not match manifest")
        if evidence.get("core_value_ids") != manifest.get("core_value_ids"):
            trace_gaps.append(f"{_display_path(approval_path)}: core_value_ids do not match manifest")
        approved_by = str(evidence.get("approved_by") or "")
        if not approved_by or _is_model_principal(approved_by) or evidence.get("model_self_approval") is not False:
            trace_gaps.append(f"{_display_path(approval_path)}: approval requires an accountable non-model principal")
        if evidence.get("production_authority") is not False:
            trace_gaps.append(f"{_display_path(approval_path)}: demonstration approval cannot grant production authority")
        if manifest.get("package_status") == "smoke_example" and evidence.get("fictional") is not True:
            trace_gaps.append(f"{_display_path(approval_path)}: smoke approval evidence must be explicitly fictional")
    elif status == "waived":
        waiver_id = manifest.get("waiver_id")
        for kind, metadata in strategic.items():
            waiver = metadata.get("waiver") if isinstance(metadata.get("waiver"), dict) else {}
            if waiver.get("status") != "active" or waiver.get("waiver_id") != waiver_id:
                trace_gaps.append(f"target-system-manifest.yaml: {kind} lacks the active manifest waiver")
        waiver_path = declared.get("approval_evidence")
        if waiver_path is None or not waiver_path.exists():
            trace_gaps.append("target-system-manifest.yaml: waived content requires package waiver evidence")
            return
        evidence = _load_yaml_mapping(waiver_path, trace_gaps)
        if evidence.get("waiver_evidence_id") != waiver_id:
            trace_gaps.append(f"{_display_path(waiver_path)}: waiver_evidence_id does not match manifest")
        if evidence.get("target_system_id") != manifest.get("target_system_id"):
            trace_gaps.append(f"{_display_path(waiver_path)}: target_system_id does not match manifest")
        if evidence.get("status") != "active":
            trace_gaps.append(f"{_display_path(waiver_path)}: manifest waiver evidence must be active")
        if evidence.get("model_self_approval") is not False:
            trace_gaps.append(f"{_display_path(waiver_path)}: waiver requires accountable non-model authority")
        if evidence.get("permission_expansion_allowed") is not False:
            trace_gaps.append(f"{_display_path(waiver_path)}: waiver cannot expand permission")


def _check_pattern_decision(
    root: Path,
    manifest: dict[str, Any],
    declared: dict[str, Path],
    trace_gaps: list[str],
) -> None:
    pointer = manifest.get("pattern_decision")
    path = declared.get("pattern_decision")
    if not isinstance(pointer, dict) or path is None or not path.exists():
        return
    decision = _load_yaml_mapping(path, trace_gaps)
    result = validate_pattern_decision(decision)
    if not result.ok:
        trace_gaps.extend(f"{_display_path(path)}: {message}" for message in result.messages)
    comparisons = {
        "pattern_decision_id": pointer.get("id"),
        "target_system_id": manifest.get("target_system_id"),
        "coordination_pattern": manifest.get("coordination_pattern"),
        "operational_maturity": manifest.get("operational_maturity"),
    }
    for field, expected in comparisons.items():
        if decision.get(field) != expected:
            trace_gaps.append(f"{_display_path(path)}: {field} does not match manifest")
    if not decision.get("human_oversight"):
        trace_gaps.append(f"{_display_path(path)}: pattern decision requires human_oversight")


def _check_host_requirements(
    root: Path,
    manifest: dict[str, Any],
    declared: dict[str, Path],
    trace_gaps: list[str],
) -> None:
    requirements = manifest.get("host_requirements")
    if not isinstance(requirements, list):
        return
    capability_ids: list[Any] = []
    permission_dependent = False
    for requirement in requirements:
        if not isinstance(requirement, dict):
            continue
        capability_ids.append(requirement.get("capability_id"))
        availability = requirement.get("availability")
        if availability == "unknown":
            trace_gaps.append(
                f"target-system-manifest.yaml: required host capability {requirement.get('capability_id')} is unknown"
            )
        if availability == "permission_dependent":
            permission_dependent = True
        evidence_path = requirement.get("evidence_path")
        if not isinstance(evidence_path, str):
            continue
        resolved = _safe_package_path(root, evidence_path, "host_requirements.evidence_path", trace_gaps)
        if resolved is not None and not resolved.exists():
            trace_gaps.append(f"target-system-manifest.yaml: stale host evidence pointer {evidence_path}")
    _check_duplicate_ids(capability_ids, "host capability", trace_gaps)
    if manifest.get("package_status") == "smoke_example" and not permission_dependent:
        trace_gaps.append("target-system-manifest.yaml: smoke example requires a permission-dependent host capability")
    host_summary = declared.get("host_capability_summary")
    if host_summary and host_summary.exists():
        text = host_summary.read_text(encoding="utf-8").casefold()
        for phrase in ("permission-dependent", "degraded behavior", "cancellation behavior"):
            if phrase not in text:
                trace_gaps.append(f"{_display_path(host_summary)}: missing host boundary phrase {phrase!r}")


def _check_hashes(
    root: Path,
    manifest: dict[str, Any],
    contents: dict[str, Any],
    declared: dict[str, Path],
    trace_gaps: list[str],
) -> None:
    entries = manifest.get("hashes")
    if not isinstance(entries, list):
        return
    seen: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        raw_path = entry.get("path")
        digest = entry.get("sha256")
        if not isinstance(raw_path, str) or not isinstance(digest, str):
            continue
        if raw_path in seen:
            trace_gaps.append(f"target-system-manifest.yaml: duplicate hash path {raw_path}")
            continue
        seen[raw_path] = digest
        path = _safe_package_path(root, raw_path, "hashes.path", trace_gaps)
        if path is None or not path.exists() or not path.is_file():
            trace_gaps.append(f"target-system-manifest.yaml: stale hash pointer {raw_path}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != actual:
            trace_gaps.append(f"target-system-manifest.yaml: stale hash for {raw_path}; expected {actual}")

    required = {
        str(contents[key])
        for key, path in declared.items()
        if key != "execution_root" and path.is_file()
    }
    execution_root = declared.get("execution_root")
    if execution_root and execution_root.is_dir():
        package_root = root.resolve()
        required.update(
            path.resolve().relative_to(package_root).as_posix()
            for path in execution_root.rglob("*")
            if path.is_file()
        )
    missing = sorted(required - set(seen))
    if missing:
        trace_gaps.append(f"target-system-manifest.yaml: hashes omit declared files: {', '.join(missing)}")


def _check_requirement_trace(path: Path | None, trace_gaps: list[str]) -> None:
    if path is None or not path.exists():
        return
    rows = _read_csv(path, REQUIRED_TRACE_HEADERS, trace_gaps)
    for index, row in enumerate(rows, start=2):
        evidence = row.get("evidence_path", "")
        if not evidence:
            trace_gaps.append(f"{_display_path(path)}:{index}: missing evidence_path")


def _check_artifact_index(
    path: Path | None,
    manifest: dict[str, Any],
    contents: dict[str, Any],
    trace_gaps: list[str],
) -> None:
    if path is None or not path.exists():
        return
    rows = _read_csv(path, REQUIRED_ARTIFACT_HEADERS, trace_gaps)
    artifact_ids = [row.get("artifact_id") for row in rows]
    _check_duplicate_ids(artifact_ids, "artifact index", trace_gaps)
    indexed_paths = {row.get("path", "") for row in rows}
    required_paths = {str(value) for value in contents.values() if isinstance(value, str)}
    required_paths.add("target-system-manifest.yaml")
    missing = sorted(required_paths - indexed_paths)
    if missing:
        trace_gaps.append(f"{_display_path(path)}: artifact index omits manifest-declared paths: {', '.join(missing)}")
    if manifest.get("package_status") == "smoke_example":
        for row in rows:
            if row.get("authority_status") not in DERIVATIVE_AUTHORITY_STATUSES:
                trace_gaps.append(
                    f"{_display_path(path)}: {row.get('artifact_id')}: smoke artifact must remain derivative"
                )


def _check_execution_transactions(path: Path | None, trace_gaps: list[str]) -> None:
    if path is None or not path.exists() or not path.is_dir():
        return
    transactions = sorted(item for item in path.rglob("*") if item.is_file())
    if not transactions:
        trace_gaps.append(f"{_display_path(path)}: execution transaction root is empty")
        return
    for transaction in transactions:
        text = transaction.read_text(encoding="utf-8").casefold()
        for phrase in ("execution transaction", "authority", "validation", "stop condition"):
            if phrase not in text:
                trace_gaps.append(f"{_display_path(transaction)}: portable packet must mention {phrase}")
        for retired in RETIRED_ACTIVE_TERMS:
            if retired in text:
                trace_gaps.append(f"{_display_path(transaction)}: active packet uses retired term {retired!r}")


def _check_validation_summaries(
    manifest: dict[str, Any],
    declared: dict[str, Path],
    trace_gaps: list[str],
) -> None:
    for key in (
        "validation_summary",
        "strategic_intent_summary",
        "host_capability_summary",
        "test_and_evaluation_summary",
    ):
        path = declared.get(key)
        if path is None or not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        if STRUCTURAL_LIMITATION not in normalized:
            trace_gaps.append(f"{_display_path(path)}: missing structural validation limitation statement")


def _check_boundary_text(root: Path, manifest: dict[str, Any], trace_gaps: list[str]) -> None:
    if not root.exists():
        return
    text_parts = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".yaml", ".csv"}:
            text_parts.append(path.read_text(encoding="utf-8"))
    text = "\n".join(text_parts).casefold()
    if manifest.get("package_status") == "smoke_example":
        authority_notice = str(manifest.get("authority_notice", "")).casefold()
        for phrase in REQUIRED_BOUNDARY_PHRASES:
            if phrase not in authority_notice:
                trace_gaps.append(f"target-system-manifest.yaml: authority_notice must contain {phrase!r}")
            if phrase not in text:
                trace_gaps.append(f"package boundary text must contain {phrase!r}")
        for claim in SMOKE_PROHIBITED_CLAIMS:
            if claim in text:
                trace_gaps.append(f"package contains prohibited smoke authority claim: {claim}")


def _read_csv(path: Path, expected: tuple[str, ...], trace_gaps: list[str]) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            headers = tuple(reader.fieldnames or ())
            rows = list(reader)
    except OSError as exc:
        trace_gaps.append(f"{_display_path(path)}: cannot read CSV: {exc}")
        return []
    if headers != expected:
        trace_gaps.append(f"{_display_path(path)}: CSV headers must be {','.join(expected)}")
    if not rows:
        trace_gaps.append(f"{_display_path(path)}: CSV must contain at least one row")
    return rows


def _load_yaml_mapping(path: Path, trace_gaps: list[str]) -> dict[str, Any]:
    try:
        data = load_yaml(path)
    except YamlLoadError as exc:
        trace_gaps.append(str(exc))
        return {}
    if not isinstance(data, dict):
        trace_gaps.append(f"{_display_path(path)}: YAML document must be a mapping")
        return {}
    return data


def _load_front_matter(path: Path, trace_gaps: list[str]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    match = re.match(r"^---\n(?P<metadata>.*?)\n---(?:\n|$)", text, re.DOTALL)
    if match is None:
        trace_gaps.append(f"{_display_path(path)}: missing YAML front matter")
        return {}
    try:
        data = yaml.safe_load(match.group("metadata"))
    except yaml.YAMLError as exc:
        trace_gaps.append(f"{_display_path(path)}: invalid YAML front matter: {exc}")
        return {}
    if not isinstance(data, dict):
        trace_gaps.append(f"{_display_path(path)}: YAML front matter must be a mapping")
        return {}
    return data


def _safe_package_path(root: Path, value: str, label: str, trace_gaps: list[str]) -> Path | None:
    candidate = Path(value)
    if candidate.is_absolute():
        trace_gaps.append(f"target-system-manifest.yaml: {label} must be package-relative")
        return None
    resolved = (root / candidate).resolve()
    package_root = root.resolve()
    if resolved != package_root and package_root not in resolved.parents:
        trace_gaps.append(f"target-system-manifest.yaml: {label} escapes the package root")
        return None
    return resolved


def _resolve_source_trace(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    if path.startswith("Sys4AI/"):
        return WORKSPACE_ROOT / path
    if path.startswith(("PRDs/", "implementation_plans/")):
        return WORKSPACE_ROOT / path
    return PRODUCT_ROOT / path


def _check_duplicate_ids(values: Iterable[Any], label: str, trace_gaps: list[str]) -> None:
    normalized = [str(value) for value in values if value]
    duplicates = sorted(value for value, count in Counter(normalized).items() if count > 1)
    if duplicates:
        trace_gaps.append(f"target-system-manifest.yaml: duplicate {label} IDs: {', '.join(duplicates)}")


def _is_model_principal(value: str) -> bool:
    normalized = value.strip().casefold().replace("_", "-")
    return normalized in MODEL_PRINCIPALS or normalized.startswith(("meta-agent-", "runtime-"))


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()
