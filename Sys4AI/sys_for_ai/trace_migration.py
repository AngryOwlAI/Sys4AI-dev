"""Deterministic TX-11/TX-12 requirement-trace migration support."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import io
import os
from pathlib import Path
import re
import tempfile
from typing import Mapping

from .jsonschema_io import load_json, validate_instance
from .registry_io import resolve_registered_path
from .validators import ValidationResult


TRACE_SCHEMA_VERSION = "2.0.0"
TX11_LEGACY_SHA256 = "95e59cf5befc4f9fd29d857d1f609a4c0d2c321c1b3adf1efca1a69cdb01b28c"
TX12_REVIEW_OWNER = "requirements_verifier"
TX12_REVIEW_DATE = "2026-07-10"
TX24_REVIEW_DATE = "2026-07-11"
DEFAULT_TRACE_REGISTRY = Path("registries/requirement_trace_registry.csv")
DEFAULT_TRACE_SCHEMA = Path("schemas/contracts/requirement_trace_registry_row.schema.json")

LEGACY_HEADER = (
    "trace_id",
    "phase0_selector",
    "phase0_source",
    "coverage_status",
    "trace_class",
    "semantic_justification",
    "semantic_review_verdict",
    "phase1_selectors",
    "evidence_paths",
    "notes",
)

GENERALIZED_HEADER = (
    "schema_version",
    "trace_id",
    "requirement_id",
    "requirement_source_id",
    "requirement_lifecycle",
    "applicability_status",
    "coverage_status",
    "capability_status",
    "verification_status",
    "verification_waiver_id",
    "evidence_status",
    "implementation_artifacts",
    "validation_evidence",
    "evidence_paths",
    "semantic_review_owner",
    "semantic_review_date",
    "semantic_review_verdict",
    "supersedes",
    "phase0_selector",
    "phase0_source",
    "legacy_coverage_status",
    "trace_class",
    "semantic_justification",
    "legacy_semantic_review_verdict",
    "phase1_selectors",
    "notes",
)

_COVERAGE_MAP = {
    "covered": "covered",
    "partial": "partial",
    "deferred": "missing",
    "not_applicable": "not_applicable",
}

_CAPABILITY_MAP = {
    "implemented": "scaffolded",
    "scaffolded": "scaffolded",
    "deferred": "absent",
    "out_of_phase": "absent",
}

_IMPLEMENTATION_PREFIXES = (
    ".agents/skills/",
    ".codex/skills/",
    "Sys4AI/configs/",
    "Sys4AI/control_records/examples/",
    "Sys4AI/control_records/program_state.yaml",
    "Sys4AI/control_records/system_definition/",
    "Sys4AI/docs/",
    "Sys4AI/examples/",
    "Sys4AI/Makefile",
    "Sys4AI/pyproject.toml",
    "Sys4AI/README.md",
    "Sys4AI/registries/",
    "Sys4AI/requirements.txt",
    "Sys4AI/schemas/",
    "Sys4AI/skills/",
    "Sys4AI/sys_for_ai/",
    "Sys4AI/templates/",
)

_NON_IMPLEMENTATION_PREFIXES = (
    "Sys4AI/docs/generated/",
    "Sys4AI/tests/",
)

_TRACE_IMPLEMENTATION_REQUIREMENTS = {
    "SFA-CORE-TRACE-001",
    "SFA-P0-FR-008",
    "SFA-P0-NFR-003",
    "SFA-P0-NFR-006",
    "SFA-P0-NFR-013",
}

_TRACE_IMPLEMENTATION_PATHS = (
    "Sys4AI/schemas/contracts/requirement_trace_registry_row.schema.json",
    "Sys4AI/sys_for_ai/trace_migration.py",
    "Sys4AI/sys_for_ai/validators.py",
)

_TRACE_VALIDATION_PATHS = (
    "Sys4AI/tests/test_trace_schema_migration.py",
    "implementation_plans/completion_receipts/CR-SFADEV-STRATEGIC-BASELINE-TX11-001.md",
)

_STRATEGIC_RECEIPT_RE = re.compile(
    r"^implementation_plans/completion_receipts/"
    r"CR-SFADEV-STRATEGIC-BASELINE-TX(?:0[3-9]|10|11)-001\.md$"
)

_LEGACY_RUNTIME_MARKERS = (
    "/agentjobs/",
    "agentjob",
    "/continue",
    "self_hosting_memory_continue",
)

_TX24_LEGACY_FIELDS = {
    "TRACE-SFA-CORE-ID-001": {
        "evidence_paths": "PRDs/Sys4AI_phase-0_product_system_design_prd.md;PRDs/Sys4AI_phase-1_implementation_initialization_prd.md;PRDs/modules/Sys4AI_system_layers_and_self_hosting_prd.md",
        "notes": "Expanded from TRACE-P0-IDENTITY. Phase 1 preserves the Phase 0 authority surface outside the implementation package. AJ24 draft module owner: PRD-MOD-SYSTEM-LAYERS-SELF-HOSTING; not canonical.",
    },
    "TRACE-SFA-CORE-ID-002": {
        "evidence_paths": "PRDs/Sys4AI_phase-0_product_system_design_prd.md;PRDs/Sys4AI_phase-1_implementation_initialization_prd.md;PRDs/modules/Sys4AI_system_layers_and_self_hosting_prd.md",
        "notes": "Expanded from TRACE-P0-IDENTITY. Phase 1 preserves the Phase 0 authority surface outside the implementation package. AJ24 draft module owner: PRD-MOD-SYSTEM-LAYERS-SELF-HOSTING; not canonical.",
    },
    "TRACE-SFA-CORE-ID-003": {
        "evidence_paths": "PRDs/Sys4AI_phase-0_product_system_design_prd.md;PRDs/Sys4AI_phase-1_implementation_initialization_prd.md;PRDs/modules/Sys4AI_system_layers_and_self_hosting_prd.md",
        "notes": "Expanded from TRACE-P0-IDENTITY. Phase 1 preserves the Phase 0 authority surface outside the implementation package. AJ24 draft module owner: PRD-MOD-SYSTEM-LAYERS-SELF-HOSTING; not canonical.",
    },
    "TRACE-SFA-P0-FR-001": {
        "evidence_paths": "PRDs/Sys4AI_phase-0_product_system_design_prd.md;PRDs/Sys4AI_phase-1_implementation_initialization_prd.md",
        "notes": "Expanded from TRACE-P0-IDENTITY. Phase 1 preserves the Phase 0 authority surface outside the implementation package.",
    },
    "TRACE-SFA-P0-FR-002": {
        "evidence_paths": "PRDs/Sys4AI_phase-0_product_system_design_prd.md;PRDs/Sys4AI_phase-1_implementation_initialization_prd.md",
        "notes": "Expanded from TRACE-P0-IDENTITY. Phase 1 preserves the Phase 0 authority surface outside the implementation package.",
    },
    "TRACE-SFA-P0-FR-003": {
        "evidence_paths": "PRDs/Sys4AI_phase-0_product_system_design_prd.md;PRDs/Sys4AI_phase-1_implementation_initialization_prd.md",
        "notes": "Expanded from TRACE-P0-IDENTITY. Phase 1 preserves the Phase 0 authority surface outside the implementation package.",
    },
    "TRACE-SFA-P0-FR-004": {
        "evidence_paths": "PRDs/Sys4AI_phase-0_product_system_design_prd.md;PRDs/Sys4AI_phase-1_implementation_initialization_prd.md;PRDs/modules/Sys4AI_domain_pack_prd.md",
        "notes": "Expanded from TRACE-P0-IDENTITY. Phase 1 preserves the Phase 0 authority surface outside the implementation package. AJ24 draft module owner: PRD-MOD-DOMAIN-PACK; not canonical.",
    },
}


def migrate_legacy_trace_row(row: Mapping[str, str]) -> dict[str, str]:
    """Map one legacy row to a conservative, reversible generalized draft row.

    The mapping is intentionally provisional. It preserves legacy fields exactly,
    makes no implemented or current-evidence claim, and leaves semantic promotion
    to TX-12 review.
    """

    missing = [field for field in LEGACY_HEADER if field not in row]
    if missing:
        raise ValueError(f"legacy row missing fields: {', '.join(missing)}")

    coverage_status = row["coverage_status"]
    trace_class = row["trace_class"]
    if coverage_status not in _COVERAGE_MAP:
        raise ValueError(f"unsupported legacy coverage_status {coverage_status!r}")
    if trace_class not in _CAPABILITY_MAP:
        raise ValueError(f"unsupported legacy trace_class {trace_class!r}")

    migrated = {
        "schema_version": TRACE_SCHEMA_VERSION,
        "trace_id": row["trace_id"],
        "requirement_id": row["phase0_selector"],
        "requirement_source_id": row["phase0_source"],
        "requirement_lifecycle": "proposed",
        "applicability_status": "not_reviewed",
        "coverage_status": _COVERAGE_MAP[coverage_status],
        "capability_status": _CAPABILITY_MAP[trace_class],
        "verification_status": "not_run",
        "verification_waiver_id": "",
        "evidence_status": "missing",
        "implementation_artifacts": "",
        "validation_evidence": "",
        "evidence_paths": row["evidence_paths"],
        "semantic_review_owner": "requirements_verifier",
        "semantic_review_date": "",
        "semantic_review_verdict": "not_reviewed",
        "supersedes": "",
        "phase0_selector": row["phase0_selector"],
        "phase0_source": row["phase0_source"],
        "legacy_coverage_status": coverage_status,
        "trace_class": trace_class,
        "semantic_justification": row["semantic_justification"],
        "legacy_semantic_review_verdict": row["semantic_review_verdict"],
        "phase1_selectors": row["phase1_selectors"],
        "notes": row["notes"],
    }
    if tuple(migrated) != GENERALIZED_HEADER:
        raise RuntimeError("generalized trace mapping header drift")
    return migrated


def reverse_generalized_trace_row(row: Mapping[str, str]) -> dict[str, str]:
    """Recover the exact legacy row fields retained by the v2 compatibility layer."""
    reversed_row = {
        "trace_id": row["trace_id"],
        "phase0_selector": row["phase0_selector"],
        "phase0_source": row["phase0_source"],
        "coverage_status": row["legacy_coverage_status"],
        "trace_class": row["trace_class"],
        "semantic_justification": row["semantic_justification"],
        "semantic_review_verdict": row["legacy_semantic_review_verdict"],
        "phase1_selectors": row["phase1_selectors"],
        "evidence_paths": row["evidence_paths"],
        "notes": row["notes"],
    }
    legacy = _TX24_LEGACY_FIELDS.get(row.get("trace_id", ""))
    if legacy is not None and row.get("semantic_review_date") == TX24_REVIEW_DATE:
        reversed_row["semantic_justification"] = ""
        reversed_row["evidence_paths"] = legacy["evidence_paths"]
        reversed_row["notes"] = legacy["notes"]
    return reversed_row


def review_legacy_trace_row(
    row: Mapping[str, str],
    review_date: str = TX12_REVIEW_DATE,
) -> dict[str, str]:
    """Apply the controlled TX-12 semantic-review policy to one legacy row.

    Coverage remains independent from current capability. A legacy
    ``implemented`` classification is retained as implemented only when an exact
    current implementation artifact can be identified. Current operational
    capability is never inferred from a path, a generated derivative, or
    historical AgentJob/continue evidence.
    """

    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", review_date):
        raise ValueError(f"invalid TX-12 semantic review date {review_date!r}")

    reviewed = migrate_legacy_trace_row(row)
    evidence_paths = _split_paths(row["evidence_paths"])
    implementation_artifacts = [
        path for path in evidence_paths if _is_current_implementation_artifact(path)
    ]
    validation_evidence = [
        path for path in evidence_paths if _is_current_validation_evidence(path)
    ]

    requirement_id = row["phase0_selector"]
    if requirement_id in _TRACE_IMPLEMENTATION_REQUIREMENTS:
        implementation_artifacts.extend(_TRACE_IMPLEMENTATION_PATHS)
        validation_evidence.extend(_TRACE_VALIDATION_PATHS)

    implementation_artifacts = _stable_unique(implementation_artifacts)
    validation_evidence = _stable_unique(validation_evidence)

    legacy_trace_class = row["trace_class"]
    if legacy_trace_class == "implemented":
        capability_status = "implemented" if implementation_artifacts else "scaffolded"
    elif legacy_trace_class == "scaffolded":
        capability_status = "scaffolded"
    else:
        capability_status = "absent"

    if capability_status == "absent":
        implementation_artifacts = []

    semantic_review_verdict = "sufficient"
    if legacy_trace_class == "implemented" and capability_status != "implemented":
        semantic_review_verdict = "needs_evidence"

    reviewed.update(
        {
            "requirement_lifecycle": "active",
            "applicability_status": "required",
            "capability_status": capability_status,
            "verification_status": "pass" if validation_evidence else "planned",
            "evidence_status": "current",
            "implementation_artifacts": ";".join(implementation_artifacts),
            "validation_evidence": ";".join(validation_evidence),
            "semantic_review_owner": TX12_REVIEW_OWNER,
            "semantic_review_date": review_date,
            "semantic_review_verdict": semantic_review_verdict,
        }
    )
    return reviewed


def migrate_requirement_trace_registry(
    trace_registry: str | Path = DEFAULT_TRACE_REGISTRY,
    schema_path: str | Path = DEFAULT_TRACE_SCHEMA,
    review_date: str = TX12_REVIEW_DATE,
) -> ValidationResult:
    """Atomically replace the exact TX-11 legacy baseline with reviewed v2 rows."""

    if review_date != TX12_REVIEW_DATE:
        return ValidationResult(
            False,
            [
                f"TX-12 review date is controlled as {TX12_REVIEW_DATE}; "
                f"found {review_date}"
            ],
        )

    target = resolve_registered_path(str(trace_registry))
    schema_target = resolve_registered_path(str(schema_path))
    if not target.exists():
        return ValidationResult(False, [f"{target}: missing requirement trace registry"])
    if not schema_target.exists():
        return ValidationResult(False, [f"{schema_target}: missing requirement trace row schema"])

    before = target.read_bytes()
    before_hash = hashlib.sha256(before).hexdigest()
    if before_hash != TX11_LEGACY_SHA256:
        return ValidationResult(
            False,
            [
                f"{target}: TX-12 input digest mismatch; "
                f"expected {TX11_LEGACY_SHA256}, found {before_hash}"
            ],
        )

    try:
        with target.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fieldnames = tuple(reader.fieldnames or ())
            legacy_rows = list(reader)
    except (OSError, csv.Error) as exc:
        return ValidationResult(False, [f"{target}: unable to read trace registry: {exc}"])

    if fieldnames != LEGACY_HEADER:
        return ValidationResult(
            False,
            [f"{target}: TX-12 writer requires the exact legacy header"],
        )

    try:
        schema = load_json(schema_target)
        reviewed_rows = [review_legacy_trace_row(row, review_date) for row in legacy_rows]
    except (OSError, RuntimeError, ValueError) as exc:
        return ValidationResult(False, [f"{target}: TX-12 review failed: {exc}"])

    messages = _validate_reviewed_rows(target, reviewed_rows, schema)
    reconstructed = _serialize_legacy_rows(
        [reverse_generalized_trace_row(row) for row in reviewed_rows]
    )
    if reconstructed != before:
        messages.append(f"{target}: TX-12 reviewed rows do not reconstruct the exact legacy baseline")
    if messages:
        return ValidationResult(False, messages)

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            newline="",
            encoding="utf-8",
            dir=target.parent,
            prefix=f".{target.name}.tx12-",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            writer = csv.DictWriter(
                handle,
                fieldnames=GENERALIZED_HEADER,
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(reviewed_rows)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, target)
    except OSError as exc:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        return ValidationResult(False, [f"{target}: atomic TX-12 write failed: {exc}"])

    result = validate_requirement_trace_migration(target, schema_target)
    if not result.ok:
        return ValidationResult(
            False,
            [
                *result.messages,
                f"{target}: post-write validation failed; revert the complete TX-12 packet",
            ],
        )
    return result


def validate_requirement_trace_migration(
    trace_registry: str | Path = DEFAULT_TRACE_REGISTRY,
    schema_path: str | Path = DEFAULT_TRACE_SCHEMA,
) -> ValidationResult:
    """Validate the TX-11 dry-run or a generalized registry preserving TX-12."""

    target = resolve_registered_path(str(trace_registry))
    schema_target = resolve_registered_path(str(schema_path))
    if not target.exists():
        return ValidationResult(False, [f"{target}: missing requirement trace registry"])
    if not schema_target.exists():
        return ValidationResult(False, [f"{schema_target}: missing requirement trace row schema"])

    before_hash = _sha256(target)
    try:
        with target.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fieldnames = tuple(reader.fieldnames or ())
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        return ValidationResult(False, [f"{target}: unable to read trace registry: {exc}"])

    messages: list[str] = []
    if fieldnames == GENERALIZED_HEADER:
        return _validate_generalized_registry(
            target,
            rows,
            schema_target,
            before_hash,
        )
    if fieldnames != LEGACY_HEADER:
        messages.append(
            f"{target}: trace migration requires the exact legacy or generalized header; "
            f"found {','.join(fieldnames)}"
        )
        return ValidationResult(False, messages)
    if not rows:
        return ValidationResult(False, [f"{target}: trace migration input is empty"])

    trace_ids = [row["trace_id"] for row in rows]
    requirement_ids = [row["phase0_selector"] for row in rows]
    messages.extend(_duplicate_messages(target, "trace ID", trace_ids))
    messages.extend(_duplicate_messages(target, "requirement ID", requirement_ids))

    try:
        schema = load_json(schema_target)
    except RuntimeError as exc:
        return ValidationResult(False, [str(exc)])

    migrated_rows: list[dict[str, str]] = []
    for index, legacy_row in enumerate(rows, start=2):
        if legacy_row.get(None):
            messages.append(f"{target}:{index}: row contains unexpected extra CSV values")
            continue
        missing_values = [field for field in LEGACY_HEADER if legacy_row.get(field) is None]
        if missing_values:
            messages.append(
                f"{target}:{index}: row is missing CSV values for: {', '.join(missing_values)}"
            )
            continue
        try:
            migrated = migrate_legacy_trace_row(legacy_row)
        except (KeyError, ValueError, RuntimeError) as exc:
            messages.append(f"{target}:{index}: migration failed: {exc}")
            continue
        errors = validate_instance(migrated, schema)
        messages.extend(
            f"{target}:{index}: generalized row invalid: {error}" for error in errors
        )
        reversed_row = reverse_generalized_trace_row(migrated)
        expected_legacy = {field: legacy_row[field] for field in LEGACY_HEADER}
        if reversed_row != expected_legacy:
            messages.append(f"{target}:{index}: generalized row is not exactly reversible")
        migrated_rows.append(migrated)

    migrated_trace_ids = [row["trace_id"] for row in migrated_rows]
    migrated_requirement_ids = [row["requirement_id"] for row in migrated_rows]
    if len(migrated_rows) != len(rows):
        messages.append(
            f"{target}: row-count parity failed: legacy={len(rows)} migrated={len(migrated_rows)}"
        )
    if set(migrated_trace_ids) != set(trace_ids):
        messages.append(f"{target}: trace-ID parity failed")
    if set(migrated_requirement_ids) != set(requirement_ids):
        messages.append(f"{target}: requirement-ID parity failed")
    if _sha256(target) != before_hash:
        messages.append(f"{target}: source registry changed during dry-run")

    if messages:
        return ValidationResult(False, messages)

    return ValidationResult(
        True,
        [
            f"{target}: TX-11 requirement trace migration dry-run passed",
            f"legacy_sha256={before_hash}",
            f"rows={len(rows)} trace_ids={len(set(trace_ids))} "
            f"requirement_ids={len(set(requirement_ids))}",
            f"coverage_status: {_format_counts(migrated_rows, 'coverage_status')}",
            f"applicability_status: {_format_counts(migrated_rows, 'applicability_status')}",
            f"capability_status: {_format_counts(migrated_rows, 'capability_status')}",
            f"verification_status: {_format_counts(migrated_rows, 'verification_status')}",
            f"evidence_status: {_format_counts(migrated_rows, 'evidence_status')}",
            f"semantic_review_verdict: {_format_counts(migrated_rows, 'semantic_review_verdict')}",
            "dry-run only: wrote no trace rows; TX-12 semantic review and data migration remain required",
        ],
    )


def _validate_generalized_registry(
    target: Path,
    rows: list[dict[str, str]],
    schema_target: Path,
    current_hash: str,
) -> ValidationResult:
    if not rows:
        return ValidationResult(False, [f"{target}: reviewed trace registry is empty"])
    try:
        schema = load_json(schema_target)
    except RuntimeError as exc:
        return ValidationResult(False, [str(exc)])

    messages = _validate_reviewed_rows(target, rows, schema)
    trace_ids = [row.get("trace_id", "") for row in rows]
    requirement_ids = [row.get("requirement_id", "") for row in rows]
    messages.extend(_duplicate_messages(target, "trace ID", trace_ids))
    messages.extend(_duplicate_messages(target, "requirement ID", requirement_ids))

    tx12_rows = [row for row in rows if row.get("requirement_source_id") == "SRC-PRD-P0"]
    additive_rows = [row for row in rows if row.get("requirement_source_id") != "SRC-PRD-P0"]
    reversed_rows = [reverse_generalized_trace_row(row) for row in tx12_rows]
    rollback_bytes = _serialize_legacy_rows(reversed_rows)
    rollback_hash = hashlib.sha256(rollback_bytes).hexdigest()
    if rollback_hash != TX11_LEGACY_SHA256:
        messages.append(
            f"{target}: rollback digest mismatch; "
            f"expected {TX11_LEGACY_SHA256}, found {rollback_hash}"
        )
    if len(tx12_rows) != 214:
        messages.append(f"{target}: expected 214 preserved TX-12 rows, found {len(tx12_rows)}")

    if messages:
        return ValidationResult(False, messages)

    return ValidationResult(
        True,
        [
            f"{target}: TX-12 reviewed requirement trace migration validation passed",
            f"generalized_sha256={current_hash}",
            f"rollback_legacy_sha256={rollback_hash}",
            f"rows={len(rows)} tx12_rows={len(tx12_rows)} additive_rows={len(additive_rows)} "
            f"trace_ids={len(set(trace_ids))} "
            f"requirement_ids={len(set(requirement_ids))}",
            f"requirement_lifecycle: {_format_counts(rows, 'requirement_lifecycle')}",
            f"applicability_status: {_format_counts(rows, 'applicability_status')}",
            f"coverage_status: {_format_counts(rows, 'coverage_status')}",
            f"capability_status: {_format_counts(rows, 'capability_status')}",
            f"verification_status: {_format_counts(rows, 'verification_status')}",
            f"evidence_status: {_format_counts(rows, 'evidence_status')}",
            f"semantic_review_verdict: {_format_counts(rows, 'semantic_review_verdict')}",
            f"legacy_runtime_evidence_rows={sum(row_uses_legacy_runtime_evidence(row) for row in rows)}",
        ],
    )


def _validate_reviewed_rows(
    target: Path,
    rows: list[dict[str, str]],
    schema: Mapping[str, object],
) -> list[str]:
    messages: list[str] = []
    for index, row in enumerate(rows, start=2):
        errors = validate_instance(row, schema)
        messages.extend(f"{target}:{index}: generalized row invalid: {error}" for error in errors)
        trace_id = row.get("trace_id", "")
        if row.get("requirement_lifecycle") == "proposed":
            messages.append(f"{target}:{index}: {trace_id}: provisional requirement lifecycle remains")
        if row.get("applicability_status") == "not_reviewed":
            messages.append(f"{target}:{index}: {trace_id}: applicability remains unreviewed")
        is_tx12_row = row.get("requirement_source_id") == "SRC-PRD-P0"
        if is_tx12_row and row.get("verification_status") in {"not_run"}:
            messages.append(f"{target}:{index}: {trace_id}: provisional verification state remains")
        if row.get("evidence_status") == "missing":
            messages.append(f"{target}:{index}: {trace_id}: provisional evidence state remains")
        if row.get("semantic_review_verdict") == "not_reviewed":
            messages.append(f"{target}:{index}: {trace_id}: semantic review remains incomplete")
        if is_tx12_row and row.get("semantic_review_owner") != TX12_REVIEW_OWNER:
            messages.append(f"{target}:{index}: {trace_id}: unexpected semantic review owner")
        is_tx24_review = (
            trace_id in _TX24_LEGACY_FIELDS
            and "STRATEGIC-BASELINE-MIGRATION-LOCAL-EVIDENCE-SEMANTIC-REVIEW-SFADEV-TX24.md"
            in row.get("evidence_paths", "")
        )
        expected_date = TX24_REVIEW_DATE if is_tx24_review else TX12_REVIEW_DATE
        if is_tx12_row and row.get("semantic_review_date") != expected_date:
            messages.append(f"{target}:{index}: {trace_id}: unexpected semantic review date")
        for field in ("implementation_artifacts", "validation_evidence", "evidence_paths"):
            for path in _split_paths(row.get(field, "")):
                if not resolve_registered_path(path).exists():
                    messages.append(f"{target}:{index}: {trace_id}: missing {field} path {path}")
    return messages


def row_uses_legacy_runtime_evidence(row: Mapping[str, str]) -> bool:
    """Return whether compatibility evidence names retired runtime surfaces."""

    blob = " ".join(
        str(row.get(field, ""))
        for field in ("evidence_paths", "semantic_justification", "notes")
    ).lower()
    return any(marker in blob for marker in _LEGACY_RUNTIME_MARKERS)


def _is_current_implementation_artifact(path: str) -> bool:
    if path == "Sys4AI/registries/requirement_trace_registry.csv":
        return False
    if path.startswith(_NON_IMPLEMENTATION_PREFIXES):
        return False
    return path.startswith(_IMPLEMENTATION_PREFIXES)


def _is_current_validation_evidence(path: str) -> bool:
    return path.startswith("Sys4AI/tests/") or bool(_STRATEGIC_RECEIPT_RE.fullmatch(path))


def _split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def _stable_unique(values: list[str] | tuple[str, ...]) -> list[str]:
    return list(dict.fromkeys(values))


def _serialize_legacy_rows(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=LEGACY_HEADER, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def _duplicate_messages(target: Path, label: str, values: list[str]) -> list[str]:
    counts = Counter(values)
    return [
        f"{target}: duplicate {label} {value!r}"
        for value, count in sorted(counts.items())
        if not value or count > 1
    ]


def _format_counts(rows: list[dict[str, str]], field: str) -> str:
    counts = Counter(row[field] for row in rows)
    return ", ".join(f"{key}={counts[key]}" for key in sorted(counts))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
