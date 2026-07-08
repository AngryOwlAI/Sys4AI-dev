"""Validators for governed PRD module decomposition."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .registry_io import read_registry, read_registry_rows, resolve_registered_path
from .validators import ValidationResult, _validate_rows_against_contract


EXPECTED_HEADER = [
    "prd_module_id",
    "path",
    "title",
    "status",
    "subject_layer",
    "authority_scope",
    "owns_requirement_prefixes",
    "references_source_prds",
    "supersedes",
    "source_authority_status",
    "owner_role",
    "validation_status",
    "source_hash",
    "last_validated_at",
    "notes",
]

VALID_STATUSES = {"planned", "draft", "controlled", "canonical_draft", "canonical", "superseded"}
VALID_SOURCE_AUTHORITY_STATUSES = {
    "derivative_draft",
    "controlled",
    "canonical_draft",
    "canonical",
    "superseded",
    "historical_reference",
}
CANONICAL_STATUSES = {"canonical", "canonical_draft"}
PLANNED_TRACE_STATUSES = {"planned", "todo", "not_run", "pending"}


def validate_prd_modules(path: str | Path = "registries/prd_module_registry.csv") -> ValidationResult:
    """Validate the PRD module registry and active module file metadata."""

    target = Path(path)
    messages: list[str] = []
    if not target.exists():
        return ValidationResult(False, [f"{target}: missing PRD module registry"])

    header, rows = read_registry(target)
    if header != EXPECTED_HEADER:
        messages.append(f"{target}: header mismatch. Expected {EXPECTED_HEADER!r}, found {header!r}")

    row_result = _validate_rows_against_contract(
        target,
        "schemas/contracts/prd_module_registry_row.schema.json",
        "prd_module_id",
    )
    if not row_result.ok:
        messages.extend(row_result.messages)

    known_layers = _known_values(target.parent / "system_layer_registry.csv", "layer_id")
    known_roles = _known_values(target.parent / "role_registry.csv", "role_id")
    requirement_trace_blob = _requirement_trace_blob(target.parent / "requirement_trace_registry.csv")
    canonical_owners: dict[str, list[str]] = defaultdict(list)
    seen_ids: set[str] = set()

    for index, row in enumerate(rows, start=2):
        module_id = row.get("prd_module_id", "")
        label = f"{target}:{index}: {module_id or '<missing>'}"
        if not module_id:
            messages.append(f"{label}: missing prd_module_id")
        elif module_id in seen_ids:
            messages.append(f"{label}: duplicate prd_module_id")
        else:
            seen_ids.add(module_id)

        for field in EXPECTED_HEADER:
            if field in {"supersedes", "notes"}:
                continue
            if not row.get(field, "").strip():
                messages.append(f"{label}: missing required field {field}")

        status = row.get("status", "")
        authority_status = row.get("source_authority_status", "")
        if status not in VALID_STATUSES:
            messages.append(f"{label}: unknown status {status!r}")
        if authority_status not in VALID_SOURCE_AUTHORITY_STATUSES:
            messages.append(f"{label}: unknown source_authority_status {authority_status!r}")
        if status in {"planned", "draft"} and authority_status in CANONICAL_STATUSES:
            messages.append(f"{label}: {status} module cannot claim {authority_status} authority")

        subject_layer = row.get("subject_layer", "")
        if known_layers and subject_layer not in known_layers:
            messages.append(f"{label}: unknown subject_layer {subject_layer!r}")
        owner_role = row.get("owner_role", "")
        if known_roles and owner_role not in known_roles:
            messages.append(f"{label}: unknown owner_role {owner_role!r}")

        source_prds = _split_list(row.get("references_source_prds", ""))
        if not source_prds:
            messages.append(f"{label}: references_source_prds must name at least one source PRD")
        for source_prd in source_prds:
            if not resolve_registered_path(source_prd).exists():
                messages.append(f"{label}: source PRD not found: {source_prd}")

        supersedes = _split_list(row.get("supersedes", ""))
        for superseded_path in supersedes:
            if superseded_path not in source_prds:
                messages.append(f"{label}: superseded source must remain in references_source_prds: {superseded_path}")

        prefixes = _split_list(row.get("owns_requirement_prefixes", ""))
        if not prefixes:
            messages.append(f"{label}: owns_requirement_prefixes must name at least one prefix")
        if authority_status in CANONICAL_STATUSES and status != "superseded":
            for prefix in prefixes:
                canonical_owners[prefix].append(module_id)

        module_path = resolve_registered_path(row.get("path", ""))
        if status == "planned":
            if row.get("validation_status") != "planned":
                messages.append(f"{label}: planned modules must have validation_status planned")
            if module_path.exists():
                messages.extend(_validate_module_file(module_path, row, label))
        else:
            if not module_path.exists():
                messages.append(f"{label}: module file not found: {row.get('path')}")
            else:
                messages.extend(_validate_module_file(module_path, row, label))

        if row.get("validation_status") not in PLANNED_TRACE_STATUSES and module_id not in requirement_trace_blob:
            messages.append(f"{label}: requirement trace does not mention module ID {module_id}")

    for prefix, owners in sorted(canonical_owners.items()):
        if len(owners) > 1:
            messages.append(
                f"{target}: requirement prefix {prefix!r} has multiple canonical owners: {', '.join(sorted(owners))}"
            )

    return ValidationResult(not messages, messages or [f"{target}: PRD module registry validation passed"])


def _validate_module_file(path: Path, row: dict[str, str], label: str) -> list[str]:
    content = path.read_text(encoding="utf-8")
    lower = content.lower()
    messages: list[str] = []
    if "authority notice" not in lower:
        messages.append(f"{label}: module file missing authority notice")
    if "source prds" not in lower:
        messages.append(f"{label}: module file missing Source PRDs metadata")
    if row.get("subject_layer", "") not in content:
        messages.append(f"{label}: module file missing subject layer {row.get('subject_layer')!r}")
    if row.get("source_authority_status", "") not in content:
        messages.append(
            f"{label}: module file missing source authority status {row.get('source_authority_status')!r}"
        )
    return messages


def _known_values(path: Path, field: str) -> set[str]:
    if not path.exists():
        return set()
    return {row.get(field, "") for row in read_registry_rows(path) if row.get(field)}


def _requirement_trace_blob(path: Path) -> str:
    if not path.exists():
        return ""
    return "\n".join(";".join(row.values()) for row in read_registry_rows(path))


def _split_list(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]
