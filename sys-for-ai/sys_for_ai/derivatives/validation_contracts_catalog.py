"""Validation Contracts Catalog generator."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from ..registry_io import read_registry_rows
from ..validators import ValidationResult
from .templates import (
    PROMOTION_PATH,
    STRUCTURAL_WARNING,
    check_or_write_pages,
    markdown_table,
    product_root,
    registry_trace_table,
    render_page,
    source_hashes_from_rows,
)

GENERATOR = "sys_for_ai.derivatives.validation_contracts_catalog:0.1.0"


def expected_validation_contracts_catalog_pages(root: str | Path = ".") -> dict[Path, str]:
    """Return deterministic Validation Contracts Catalog page content."""

    base = product_root(root)
    contract_rows = read_registry_rows(base / "registries/validation_contract_registry.csv")
    return {
        base / "docs/generated/validation_contracts/index.md": _index_page(base, contract_rows),
        base / "docs/generated/validation_contracts/contracts-by-target.md": _by_target_page(contract_rows),
    }


def check_validation_contracts_catalog(root: str | Path = ".") -> ValidationResult:
    """Check generated Validation Contracts Catalog pages."""

    return check_or_write_pages(
        expected_validation_contracts_catalog_pages(root),
        write=False,
        label="generate-validation-contracts-catalog",
    )


def write_validation_contracts_catalog(root: str | Path = ".") -> ValidationResult:
    """Write generated Validation Contracts Catalog pages."""

    return check_or_write_pages(
        expected_validation_contracts_catalog_pages(root),
        write=True,
        label="generate-validation-contracts-catalog",
    )


def _index_page(root: Path, contract_rows: list[dict[str, str]]) -> str:
    body = "\n\n".join(
        [
            "This generated page indexes executable validation contracts. It is a reader catalog, not a contract authority.",
            "## Registry Trace",
            registry_trace_table(root, ["der_validation_contracts_index", "der_validation_contracts_by_target"]),
            "## Structural Versus Semantic Warning",
            STRUCTURAL_WARNING,
            "## Contract Rows",
            _contract_table(contract_rows),
            "## Known Limitations",
            "Validators listed here check declared structure and registered paths. They do not replace source review, semantic review, or human approval gates.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Validation Contracts Catalog",
        derivative_id="der_validation_contracts_index",
        derivative_type="validation_contracts_catalog_page",
        source_registries=["registries/validation_contract_registry.csv"],
        validation_contracts=[row.get("contract_id", "") for row in contract_rows],
        generator=GENERATOR,
        source_hashes=source_hashes_from_rows(contract_rows),
        body=body,
    )


def _by_target_page(contract_rows: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in contract_rows:
        key = f"{row.get('target_format', 'pending')} / {row.get('target_artifact_type', 'pending')}"
        grouped[key].append(row)
    sections: list[str] = [
        "Contracts grouped by target format and artifact class.",
        "## Structural Versus Semantic Warning",
        STRUCTURAL_WARNING,
    ]
    for key in sorted(grouped):
        sections.append(f"## {key}")
        sections.append(_contract_table(grouped[key]))
    sections.extend(
        [
            "## Known Limitations",
            "Target groups are derived from registry rows. A row with stale metadata can mislead this page until the registry is corrected.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Contracts By Target",
        derivative_id="der_validation_contracts_by_target",
        derivative_type="validation_contracts_catalog_page",
        source_registries=["registries/validation_contract_registry.csv"],
        validation_contracts=[row.get("contract_id", "") for row in contract_rows],
        generator=GENERATOR,
        source_hashes=source_hashes_from_rows(contract_rows),
        body="\n\n".join(sections),
    )


def _contract_table(contract_rows: list[dict[str, str]]) -> str:
    return markdown_table(
        [
            "contract_id",
            "path",
            "dialect",
            "target_format",
            "target_artifact_type",
            "target_glob",
            "validator_command",
            "owner",
            "authority_status",
            "supersedes",
            "source_hash",
        ],
        [
            [
                row.get("contract_id", ""),
                row.get("path", ""),
                row.get("dialect", ""),
                row.get("target_format", ""),
                row.get("target_artifact_type", ""),
                row.get("target_glob", ""),
                row.get("validator_command", ""),
                row.get("owner", ""),
                row.get("authority_status", ""),
                row.get("supersedes", ""),
                row.get("source_hash", ""),
            ]
            for row in contract_rows
        ],
    )
