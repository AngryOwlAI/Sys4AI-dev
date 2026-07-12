"""Fail-closed verification for generated configuration and contract readers."""

from __future__ import annotations

from pathlib import Path

from .derivatives import check_config_control_wiki, check_validation_contracts_catalog
from .derivatives.config_control_wiki import GENERATOR as CONFIG_GENERATOR
from .derivatives.validation_contracts_catalog import (
    ENTRY_LIMITATION,
    GENERATOR as CATALOG_GENERATOR,
)
from .registry_io import RegistryLoadError, read_registry_rows, resolve_registered_path
from .validators import ValidationResult


REQUIREMENT_IDS = (
    "SFA-CORE-CCWIKI-001",
    "SFA-CORE-CCWIKI-002",
    "SFA-CORE-CCWIKI-003",
    "SFA-CORE-CCWIKI-004",
    "SFA-CORE-CCWIKI-005",
    "SFA-CORE-VCCAT-001",
    "SFA-CORE-VCCAT-002",
    "SFA-CORE-VCCAT-003",
    "SFA-CORE-VCCAT-004",
    "SFA-CORE-VCCAT-005",
    "SFA-P0-FR-037",
    "SFA-P0-FR-038",
    "SFA-P0-FR-044",
    "SFA-P0-NFR-017",
)

EXPECTED_DERIVATIVES = {
    "der_configuration_control_index": (
        "docs/generated/configuration_control/index.md",
        "configuration_control_wiki_page",
        CONFIG_GENERATOR,
    ),
    "der_configuration_control_yaml": (
        "docs/generated/configuration_control/yaml-control-records.md",
        "configuration_control_wiki_page",
        CONFIG_GENERATOR,
    ),
    "der_configuration_control_toml": (
        "docs/generated/configuration_control/toml-configuration-sources.md",
        "configuration_control_wiki_page",
        CONFIG_GENERATOR,
    ),
    "der_validation_contracts_index": (
        "docs/generated/validation_contracts/index.md",
        "validation_contracts_catalog_page",
        CATALOG_GENERATOR,
    ),
    "der_validation_contracts_by_target": (
        "docs/generated/validation_contracts/contracts-by-target.md",
        "validation_contracts_catalog_page",
        CATALOG_GENERATOR,
    ),
}

REQUIRED_PAGE_TERMS = (
    "This page is a generated reader surface. It is not canonical.",
    "authority_status: generated_noncanonical",
    "validation_status: generated_content_checked",
    "stale_or_orphan_status: current",
    "generated_at:",
    "generator:",
    "source_registries:",
    "validation_contracts:",
    "source_hashes:",
    "## Allowed Promotion Path",
)


def validate_generated_reader_surface(
    format_profiles: str | Path = "registries/format_profile_registry.csv",
    config_sources: str | Path = "registries/config_source_registry.csv",
    control_records: str | Path = "registries/control_record_registry.csv",
    validation_contracts: str | Path = "registries/validation_contract_registry.csv",
    artifact_contracts: str | Path = "registries/artifact_contract_registry.csv",
    derivatives: str | Path = "registries/derivative_registry.csv",
    wiki_policy: str | Path = "docs/configuration_control_wiki_policy.md",
    catalog_policy: str | Path = "docs/validation_contracts_catalog_policy.md",
    product_root: str | Path = ".",
) -> ValidationResult:
    """Verify the fourteen generated-reader requirements as one bounded family."""

    root = Path(product_root).resolve()
    paths = {
        "formats": resolve_registered_path(str(format_profiles), root),
        "configs": resolve_registered_path(str(config_sources), root),
        "controls": resolve_registered_path(str(control_records), root),
        "contracts": resolve_registered_path(str(validation_contracts), root),
        "artifacts": resolve_registered_path(str(artifact_contracts), root),
        "derivatives": resolve_registered_path(str(derivatives), root),
    }
    try:
        rows = {key: read_registry_rows(path) for key, path in paths.items()}
    except RegistryLoadError as exc:
        return ValidationResult(False, [str(exc)])

    messages: list[str] = []
    messages.extend(_format_profile_errors(paths["formats"], rows["formats"]))

    contracts_by_id = {row.get("contract_id", ""): row for row in rows["contracts"]}
    messages.extend(
        _registered_source_errors(
            paths["configs"], rows["configs"], "config_id", root, contracts_by_id
        )
    )
    messages.extend(
        _registered_source_errors(
            paths["controls"], rows["controls"], "control_record_id", root, contracts_by_id
        )
    )
    messages.extend(_derivative_errors(paths["derivatives"], rows["derivatives"], root))
    messages.extend(_policy_errors(resolve_registered_path(str(wiki_policy), root), "wiki"))
    messages.extend(_policy_errors(resolve_registered_path(str(catalog_policy), root), "catalog"))

    wiki_result = check_config_control_wiki(root)
    catalog_result = check_validation_contracts_catalog(root)
    if not wiki_result.ok:
        messages.extend(wiki_result.messages)
    if not catalog_result.ok:
        messages.extend(catalog_result.messages)

    page_text = _page_text(root, messages)
    for path, text in page_text.items():
        for term in REQUIRED_PAGE_TERMS:
            if term not in text:
                messages.append(f"{path}: missing generated-reader contract term {term!r}")
        if "authority_status: canonical" in text:
            messages.append(f"{path}: generated reader claims canonical authority")

    messages.extend(_wiki_trace_errors(root, page_text, rows["configs"], rows["controls"]))
    messages.extend(
        _catalog_trace_errors(
            root,
            page_text,
            rows["contracts"],
            rows["artifacts"],
            rows["configs"],
            rows["controls"],
        )
    )

    if messages:
        return ValidationResult(False, sorted(dict.fromkeys(messages)))
    return ValidationResult(
        True,
        [
            "Generated reader surface: 14/14 requirements verified across configuration/control pages, validation-contract entries, declaration links, authority banners, freshness, and promotion boundaries.",
            f"Configuration/control coverage: {len(rows['controls'])} YAML control rows and {len(rows['configs'])} TOML configuration rows are source- and contract-traced.",
            f"Validation catalog coverage: {len(rows['contracts'])} contracts and {_declaration_count(rows)} declaring rows are linked with complete generated metadata.",
            "Missing sources, registry IDs, format profiles, contracts, declaration links, metadata, stale pages, canonical claims, JSON-wiki promotion, and non-derivative mirrors fail closed.",
        ],
    )


def _format_profile_errors(path: Path, rows: list[dict[str, str]]) -> list[str]:
    expected = {
        "fmt_yaml_control": (".yaml", "YAML", "configuration_control_wiki"),
        "fmt_toml_config": (".toml", "TOML", "configuration_control_wiki"),
        "fmt_jsonschema_contract": (".schema.json", "JSON Schema", "validation_contracts_catalog"),
    }
    by_id = {row.get("format_id", ""): row for row in rows}
    messages: list[str] = []
    for profile_id, (extension, family, derivative) in expected.items():
        row = by_id.get(profile_id)
        if row is None:
            messages.append(f"{path}: missing required format profile {profile_id}")
            continue
        if row.get("extension") != extension or row.get("format_family") != family:
            messages.append(f"{path}: {profile_id} extension or format family drifted")
        if derivative not in row.get("derivative_surfaces", "").split(";"):
            messages.append(f"{path}: {profile_id} omits derivative surface {derivative}")
        if row.get("registry_required") != "true" or row.get("validator_required") != "true":
            messages.append(f"{path}: {profile_id} must require registry and validator evidence")
    return messages


def _registered_source_errors(
    path: Path,
    rows: list[dict[str, str]],
    id_field: str,
    root: Path,
    contracts_by_id: dict[str, dict[str, str]],
) -> list[str]:
    messages: list[str] = []
    for index, row in enumerate(rows, start=2):
        row_id = row.get(id_field, "").strip()
        label = f"{path}:{index}: {row_id or 'missing-row-id'}"
        if not row_id:
            messages.append(f"{label}: missing registry row ID")
        source = row.get("path", "").strip()
        if not source:
            messages.append(f"{label}: missing canonical source path")
        elif not resolve_registered_path(source, root).exists():
            messages.append(f"{label}: canonical source path does not exist: {source}")
        contract_id = row.get("validation_contract_id", "").strip()
        if not contract_id:
            messages.append(f"{label}: missing validation_contract_id")
        elif contract_id not in contracts_by_id:
            messages.append(f"{label}: unknown validation contract {contract_id}")
    return messages


def _derivative_errors(path: Path, rows: list[dict[str, str]], root: Path) -> list[str]:
    by_id = {row.get("derivative_id", ""): row for row in rows}
    messages: list[str] = []
    for derivative_id, (expected_path, expected_type, generator) in EXPECTED_DERIVATIVES.items():
        row = by_id.get(derivative_id)
        if row is None:
            messages.append(f"{path}: missing derivative row {derivative_id}")
            continue
        for field, expected in (
            ("path", expected_path),
            ("derivative_type", expected_type),
            ("generation_method", generator),
            ("status", "generated_derivative"),
        ):
            if row.get(field) != expected:
                messages.append(f"{path}: {derivative_id} {field} must be {expected!r}")
        if not resolve_registered_path(row.get("path", ""), root).exists():
            messages.append(f"{path}: {derivative_id} points to a missing reader page")

    for index, row in enumerate(rows, start=2):
        identity = " ".join(
            (row.get("derivative_id", ""), row.get("derivative_type", ""), row.get("path", ""))
        ).lower()
        if "json_wiki" in identity or "json-wiki" in identity or "/json/" in identity:
            messages.append(f"{path}:{index}: standalone JSON wiki is not an approved reader surface")
        if "configuration_control" in identity or "obsidian" in identity:
            if row.get("status") != "generated_derivative":
                messages.append(f"{path}:{index}: configuration or mirror reader must remain derivative")
            if not row.get("path", "").startswith("docs/generated/"):
                messages.append(f"{path}:{index}: configuration or mirror reader must remain under docs/generated")
    return messages


def _policy_errors(path: Path, policy: str) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Cannot read generated-reader policy {path}: {exc}"]
    required = {
        "wiki": (
            "The Configuration and Control Wiki is a generated reader surface. It is not canonical.",
            "A generated page is invalid if it omits source trace",
            "Obsidian mirrors are optional derivatives",
        ),
        "catalog": (
            "The Validation Contracts Catalog is a generated reader surface for validation contracts. It is not canonical.",
            "Phase 1 creates a Validation Contracts Catalog, not a standalone JSON wiki.",
            "link contracts to registry rows, control records, configuration sources, templates, or registries",
        ),
    }[policy]
    return [f"{path}: missing generated-reader policy term {term!r}" for term in required if term not in text]


def _page_text(root: Path, messages: list[str]) -> dict[Path, str]:
    pages: dict[Path, str] = {}
    for expected_path, _, _ in EXPECTED_DERIVATIVES.values():
        path = root / expected_path
        try:
            pages[path] = path.read_text(encoding="utf-8")
        except OSError as exc:
            messages.append(f"Cannot read generated reader {path}: {exc}")
    return pages


def _wiki_trace_errors(
    root: Path,
    pages: dict[Path, str],
    config_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
) -> list[str]:
    messages: list[str] = []
    expected = {
        root / "docs/generated/configuration_control/index.md": ("fmt_yaml_control", "fmt_toml_config"),
        root / "docs/generated/configuration_control/yaml-control-records.md": ("fmt_yaml_control",),
        root / "docs/generated/configuration_control/toml-configuration-sources.md": ("fmt_toml_config",),
    }
    for path, profile_ids in expected.items():
        text = pages.get(path, "")
        for profile_id in profile_ids:
            if profile_id not in text:
                messages.append(f"{path}: missing format profile trace {profile_id}")
    yaml_text = pages.get(root / "docs/generated/configuration_control/yaml-control-records.md", "")
    toml_text = pages.get(root / "docs/generated/configuration_control/toml-configuration-sources.md", "")
    for row in control_rows:
        for value in (row.get("control_record_id", ""), row.get("path", ""), row.get("validation_contract_id", "")):
            if value and value not in yaml_text:
                messages.append(f"YAML Configuration and Control Wiki omits {value}")
    for row in config_rows:
        for value in (row.get("config_id", ""), row.get("path", ""), row.get("validation_contract_id", "")):
            if value and value not in toml_text:
                messages.append(f"TOML Configuration and Control Wiki omits {value}")
    return messages


def _catalog_trace_errors(
    root: Path,
    pages: dict[Path, str],
    contract_rows: list[dict[str, str]],
    artifact_rows: list[dict[str, str]],
    config_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
) -> list[str]:
    catalog_paths = (
        root / "docs/generated/validation_contracts/index.md",
        root / "docs/generated/validation_contracts/contracts-by-target.md",
    )
    messages: list[str] = []
    required_headers = (
        "generator_version",
        "generation_timestamp",
        "stale_or_orphan_status",
        "known_limitations",
        "declaring_registry",
        "registry_row_id",
    )
    for path in catalog_paths:
        text = pages.get(path, "")
        for header in required_headers:
            if header not in text:
                messages.append(f"{path}: catalog omits required entry field {header}")
        if "fmt_jsonschema_contract" not in text:
            messages.append(f"{path}: catalog omits JSON Schema format profile trace")
        if ENTRY_LIMITATION not in text:
            messages.append(f"{path}: catalog entries omit known limitations")
        for row in contract_rows:
            for field in (
                "contract_id",
                "path",
                "dialect",
                "target_format",
                "target_artifact_type",
                "target_glob",
                "validator_command",
                "owner",
                "authority_status",
            ):
                value = row.get(field, "").strip()
                if not value:
                    messages.append(f"validation contract {row.get('contract_id', '')}: missing {field}")
                elif value not in text:
                    messages.append(f"{path}: catalog omits {field} value {value}")

    declaring_specs = (
        ("artifact_contract_registry.csv", artifact_rows, "artifact_contract_id", "canonical_filename_or_pattern"),
        ("config_source_registry.csv", config_rows, "config_id", "path"),
        ("control_record_registry.csv", control_rows, "control_record_id", "path"),
    )
    combined = "\n".join(pages.get(path, "") for path in catalog_paths)
    contract_ids = {row.get("contract_id", "") for row in contract_rows}
    for registry, rows, id_field, source_field in declaring_specs:
        for row in rows:
            contract_id = row.get("validation_contract_id", "").strip()
            if not contract_id:
                continue
            if contract_id not in contract_ids:
                messages.append(f"registries/{registry}: {row.get(id_field, '')} declares unknown contract {contract_id}")
            for value in (f"registries/{registry}", row.get(id_field, ""), row.get(source_field, ""), contract_id):
                if value and value not in combined:
                    messages.append(f"Validation Contracts Catalog omits declaration trace {value}")
    return messages


def _declaration_count(rows: dict[str, list[dict[str, str]]]) -> int:
    return sum(
        1
        for key in ("artifacts", "configs", "controls")
        for row in rows[key]
        if row.get("validation_contract_id", "").strip()
    )
