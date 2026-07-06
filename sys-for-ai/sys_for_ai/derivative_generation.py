"""Generated derivative validation for Phase 1."""

from __future__ import annotations

from pathlib import Path

from .derivatives import check_config_control_wiki, check_validation_contracts_catalog
from .registry_io import read_registry_rows, resolve_registered_path, rows_by_id
from .validators import ValidationResult


GENERATED_NOTICE = "This page is a generated reader surface. It is not canonical."

EXPECTED_DERIVATIVES = {
    "der_configuration_control_index": Path("docs/generated/configuration_control/index.md"),
    "der_configuration_control_yaml": Path("docs/generated/configuration_control/yaml-control-records.md"),
    "der_configuration_control_toml": Path("docs/generated/configuration_control/toml-configuration-sources.md"),
    "der_validation_contracts_index": Path("docs/generated/validation_contracts/index.md"),
    "der_validation_contracts_by_target": Path("docs/generated/validation_contracts/contracts-by-target.md"),
}


def validate_generated_derivatives(
    docs_root: str | Path = "docs/generated",
    derivative_registry: str | Path = "registries/derivative_registry.csv",
) -> ValidationResult:
    """Validate committed generated derivatives and registry rows."""

    _ = Path(docs_root)
    registry_path = Path(derivative_registry)
    base = registry_path.parent.parent if registry_path.parent.name == "registries" else Path(".")
    messages: list[str] = []
    rows = read_registry_rows(derivative_registry)
    indexed = rows_by_id(rows, "derivative_id")

    for derivative_id, rel_path in EXPECTED_DERIVATIVES.items():
        row = indexed.get(derivative_id)
        if row is None:
            messages.append(f"{derivative_registry}: missing derivative row {derivative_id}")
            continue

        status = row.get("status", "")
        if status in {"canonical", "canonical_draft"}:
            messages.append(f"{derivative_id}: generated derivative cannot have status {status!r}")

        if not row.get("source_ids", "").strip():
            messages.append(f"{derivative_id}: missing source_ids")

        path = resolve_registered_path(row.get("path", str(rel_path)), base)
        if not path.exists():
            messages.append(f"{derivative_id}: generated page missing at {path}")
            continue

        text = path.read_text(encoding="utf-8")
        if GENERATED_NOTICE not in text:
            messages.append(f"{path}: missing generated derivative notice")
        if "page_metadata:" not in text:
            messages.append(f"{path}: missing page_metadata block")
        if derivative_id not in text:
            messages.append(f"{path}: missing derivative_id metadata")

    result = ValidationResult(not messages, messages or ["docs/generated: generated derivative registry validation passed"])
    result.extend(check_config_control_wiki(base))
    result.extend(check_validation_contracts_catalog(base))
    return result
