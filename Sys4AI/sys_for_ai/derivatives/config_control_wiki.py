"""Configuration and Control Wiki generator."""

from __future__ import annotations

from pathlib import Path

from ..registry_io import read_registry_rows
from ..validators import ValidationResult
from .templates import (
    PROMOTION_PATH,
    check_or_write_pages,
    markdown_table,
    product_root,
    registry_trace_table,
    render_page,
    source_hashes_from_rows,
)

GENERATOR = "sys_for_ai.derivatives.config_control_wiki:0.2.0"


def expected_config_control_wiki_pages(root: str | Path = ".") -> dict[Path, str]:
    """Return deterministic Configuration and Control Wiki page content."""

    base = product_root(root)
    format_rows = read_registry_rows(base / "registries/format_profile_registry.csv")
    config_rows = read_registry_rows(base / "registries/config_source_registry.csv")
    control_rows = read_registry_rows(base / "registries/control_record_registry.csv")
    contract_rows = read_registry_rows(base / "registries/validation_contract_registry.csv")
    contracts_by_id = {row.get("contract_id", ""): row for row in contract_rows}

    pages = {
        base / "docs/generated/configuration_control/index.md": _index_page(
            base,
            format_rows,
            config_rows,
            control_rows,
        ),
        base / "docs/generated/configuration_control/yaml-control-records.md": _yaml_page(
            control_rows,
            contracts_by_id,
        ),
        base / "docs/generated/configuration_control/toml-configuration-sources.md": _toml_page(
            config_rows,
            contracts_by_id,
        ),
    }
    return pages


def check_config_control_wiki(root: str | Path = ".") -> ValidationResult:
    """Check generated Configuration and Control Wiki pages."""

    return check_or_write_pages(
        expected_config_control_wiki_pages(root),
        write=False,
        label="generate-config-control-wiki",
    )


def write_config_control_wiki(root: str | Path = ".") -> ValidationResult:
    """Write generated Configuration and Control Wiki pages."""

    return check_or_write_pages(
        expected_config_control_wiki_pages(root),
        write=True,
        label="generate-config-control-wiki",
    )


def _index_page(
    root: Path,
    format_rows: list[dict[str, str]],
    config_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
) -> str:
    body = "\n\n".join(
        [
            "This generated page indexes registered configuration and control surfaces. It is navigation, not authority.",
            "## Registry Trace",
            registry_trace_table(
                root,
                [
                    "der_configuration_control_index",
                    "der_configuration_control_yaml",
                    "der_configuration_control_toml",
                ],
            ),
            "## Format Profile IDs",
            markdown_table(
                ["format_id", "extension", "family", "authority_class", "validator_required"],
                [
                    [
                        row.get("format_id", ""),
                        row.get("extension", ""),
                        row.get("format_family", ""),
                        row.get("default_authority_class", ""),
                        row.get("validator_required", ""),
                    ]
                    for row in format_rows
                ],
            ),
            "## Registered Surface Counts",
            markdown_table(
                ["surface", "count", "source_path"],
                [
                    ["format profiles", str(len(format_rows)), "registries/format_profile_registry.csv"],
                    ["configuration sources", str(len(config_rows)), "registries/config_source_registry.csv"],
                    ["control records", str(len(control_rows)), "registries/control_record_registry.csv"],
                ],
            ),
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Configuration And Control Wiki",
        derivative_id="der_configuration_control_index",
        derivative_type="configuration_control_wiki_page",
        source_registries=[
            "registries/format_profile_registry.csv",
            "registries/config_source_registry.csv",
            "registries/control_record_registry.csv",
        ],
        validation_contracts=_contract_ids_from_rows(config_rows + control_rows),
        generator=GENERATOR,
        format_profile_ids=["fmt_yaml_control", "fmt_toml_config"],
        source_hashes=source_hashes_from_rows(config_rows + control_rows),
        body=body,
    )


def _yaml_page(control_rows: list[dict[str, str]], contracts_by_id: dict[str, dict[str, str]]) -> str:
    body = "\n\n".join(
        [
            "Registered YAML control records are listed below. Their source files and registry rows remain authoritative.",
            "## Control Record Rows",
            markdown_table(
                [
                    "control_record_id",
                    "path",
                    "record_type",
                    "authority_status",
                    "owner",
                    "validation_contract_id",
                    "source_hash",
                ],
                [
                    [
                        row.get("control_record_id", ""),
                        row.get("path", ""),
                        row.get("record_type", ""),
                        row.get("authority_status", ""),
                        row.get("owner", ""),
                        row.get("validation_contract_id", ""),
                        row.get("source_hash", ""),
                    ]
                    for row in control_rows
                ],
            ),
            "## Validation Contract Trace",
            _contract_trace_table(_contract_ids_from_rows(control_rows), contracts_by_id),
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="YAML Control Records",
        derivative_id="der_configuration_control_yaml",
        derivative_type="configuration_control_wiki_page",
        source_registries=[
            "registries/control_record_registry.csv",
            "registries/validation_contract_registry.csv",
            "registries/format_profile_registry.csv",
        ],
        validation_contracts=_contract_ids_from_rows(control_rows),
        generator=GENERATOR,
        format_profile_ids=["fmt_yaml_control"],
        source_hashes=source_hashes_from_rows(control_rows),
        body=body,
    )


def _toml_page(config_rows: list[dict[str, str]], contracts_by_id: dict[str, dict[str, str]]) -> str:
    body = "\n\n".join(
        [
            "Registered TOML configuration sources are listed below. Runtime values and secrets are not generated here.",
            "## Configuration Source Rows",
            markdown_table(
                [
                    "config_id",
                    "path",
                    "domain",
                    "authority_status",
                    "owner",
                    "validation_contract_id",
                    "source_hash",
                ],
                [
                    [
                        row.get("config_id", ""),
                        row.get("path", ""),
                        row.get("config_domain", ""),
                        row.get("authority_status", ""),
                        row.get("owner", ""),
                        row.get("validation_contract_id", ""),
                        row.get("source_hash", ""),
                    ]
                    for row in config_rows
                ],
            ),
            "## Validation Contract Trace",
            _contract_trace_table(_contract_ids_from_rows(config_rows), contracts_by_id),
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="TOML Configuration Sources",
        derivative_id="der_configuration_control_toml",
        derivative_type="configuration_control_wiki_page",
        source_registries=[
            "registries/config_source_registry.csv",
            "registries/validation_contract_registry.csv",
            "registries/format_profile_registry.csv",
        ],
        validation_contracts=_contract_ids_from_rows(config_rows),
        generator=GENERATOR,
        format_profile_ids=["fmt_toml_config"],
        source_hashes=source_hashes_from_rows(config_rows),
        body=body,
    )


def _contract_ids_from_rows(rows: list[dict[str, str]]) -> list[str]:
    ids = sorted({row.get("validation_contract_id", "") for row in rows if row.get("validation_contract_id")})
    return ids or ["pending"]


def _contract_trace_table(contract_ids: list[str], contracts_by_id: dict[str, dict[str, str]]) -> str:
    return markdown_table(
        ["contract_id", "path", "target_format", "target_artifact_type", "validator_command"],
        [
            [
                contract_id,
                contracts_by_id.get(contract_id, {}).get("path", ""),
                contracts_by_id.get(contract_id, {}).get("target_format", ""),
                contracts_by_id.get(contract_id, {}).get("target_artifact_type", ""),
                contracts_by_id.get(contract_id, {}).get("validator_command", ""),
            ]
            for contract_id in contract_ids
        ],
    )
