"""Focused verification for the bounded core format-governance evidence family."""

from __future__ import annotations

from pathlib import Path

from .memory import lookup_memory
from .registry_io import read_registry_rows, resolve_registered_path
from .validators import ValidationResult, validate_format_profiles


CORE_PROFILES = {
    "fmt_markdown_source": {
        "extension": ".md",
        "format_family": "Markdown",
        "primary_role": "human_authored_source",
        "default_authority_class": "source_document",
        "registry_required": "true",
        "validator_required": "false",
        "promotion_rule": "source_promotion_transaction",
        "secrets_allowed": "false",
    },
    "fmt_csv_registry": {
        "extension": ".csv",
        "format_family": "CSV",
        "primary_role": "registry_ledger",
        "default_authority_class": "registry_row",
        "registry_required": "true",
        "validator_required": "true",
        "promotion_rule": "registry_change_transaction",
        "secrets_allowed": "false",
    },
    "fmt_yaml_control": {
        "extension": ".yaml",
        "format_family": "YAML",
        "primary_role": "agent_control_state",
        "default_authority_class": "control_record",
        "registry_required": "true",
        "validator_required": "true",
        "promotion_rule": "source_import_transaction",
        "secrets_allowed": "false",
    },
    "fmt_toml_config": {
        "extension": ".toml",
        "format_family": "TOML",
        "primary_role": "project_configuration",
        "default_authority_class": "configuration_source",
        "registry_required": "true",
        "validator_required": "true",
        "promotion_rule": "config_change_transaction",
        "secrets_allowed": "false",
    },
    "fmt_jsonschema_contract": {
        "extension": ".schema.json",
        "format_family": "JSON Schema",
        "primary_role": "validation_contract",
        "default_authority_class": "validation_contract",
        "registry_required": "true",
        "validator_required": "true",
        "promotion_rule": "contract_change_transaction",
        "secrets_allowed": "false",
    },
}
REQUIRED_PROFILE_FIELDS = (
    "primary_role",
    "canonical_roots",
    "derivative_surfaces",
    "registry_required",
    "validator_required",
    "default_authority_class",
    "promotion_rule",
    "secrets_allowed",
    "notes",
)
REQUIRED_POLICY_TERMS = (
    "## Authority Notice",
    "## Core Profiles",
    "## Registry Requirements",
    "## Validation Requirements",
    "## Derivative Surface Requirements",
    "## Promotion Workflow",
    "## Security And Secrets Rules",
    "## Drift, Orphan, And Stale Rules",
    "## Project-Specific Profile Extension Workflow",
    "shall not weaken the core authority hierarchy",
    "Generated derivatives, local vault notes, semantic caches, and summaries do not become canonical",
)
MEMORY_PROBES = {
    "SRC-PRD-P0": "fmt_markdown_source",
    "SRC-REG-FORMAT-PROFILES": "fmt_csv_registry",
    "ctrl_program_state": "fmt_yaml_control",
    "cfg_pyproject": "fmt_toml_config",
    "contract_format_profile_registry_row": "fmt_jsonschema_contract",
}
MEMORY_FIELDS = {
    "path",
    "format_profile_id",
    "authority_class",
    "registry",
    "registry_row_id",
    "validation_status",
    "derivative_freshness",
}


def validate_format_governance_surface(
    format_profiles: str | Path = "registries/format_profile_registry.csv",
    policy: str | Path = "docs/format_profile_policy.md",
    memory_root: str | Path = ".",
) -> ValidationResult:
    """Verify the ten implemented format-governance requirements without promoting derivatives."""

    format_path = resolve_registered_path(str(format_profiles))
    policy_path = resolve_registered_path(str(policy))
    messages: list[str] = []

    structural = validate_format_profiles(format_path)
    if not structural.ok:
        messages.extend(structural.messages)
    try:
        rows = read_registry_rows(format_path)
    except RuntimeError as exc:
        return ValidationResult(False, [str(exc)])

    rows_by_id = {row.get("format_id", ""): row for row in rows}
    if set(rows_by_id) != set(CORE_PROFILES):
        messages.append(f"{format_path}: the current core registry must contain exactly the five governed profiles")
    for format_id, expected in CORE_PROFILES.items():
        row = rows_by_id.get(format_id)
        if row is None:
            continue
        for field in REQUIRED_PROFILE_FIELDS:
            if not row.get(field, "").strip():
                messages.append(f"{format_path}: {format_id} {field} must be populated")
        for field, value in expected.items():
            if row.get(field) != value:
                messages.append(f"{format_path}: {format_id} {field} must be {value!r}")

    try:
        policy_text = policy_path.read_text(encoding="utf-8")
    except OSError as exc:
        messages.append(f"Cannot read format policy {policy_path}: {exc}")
    else:
        for term in REQUIRED_POLICY_TERMS:
            if term not in policy_text:
                messages.append(f"{policy_path}: missing governed format policy term {term!r}")

    for object_id, expected_profile in MEMORY_PROBES.items():
        payload = lookup_memory(object_id, memory_root)
        result = payload.get("result")
        if not payload.get("ok") or not isinstance(result, dict):
            messages.append(f"memory lookup {object_id}: registered artifact is not retrievable")
            continue
        missing_fields = sorted(MEMORY_FIELDS - set(result))
        if missing_fields:
            messages.append(f"memory lookup {object_id}: missing inspectability fields {', '.join(missing_fields)}")
        if result.get("format_profile_id") != expected_profile:
            messages.append(
                f"memory lookup {object_id}: expected format profile {expected_profile}, "
                f"found {result.get('format_profile_id')!r}"
            )

    derivative = lookup_memory("der_configuration_control_index", memory_root)
    derivative_result = derivative.get("result")
    if not derivative.get("ok") or not isinstance(derivative_result, dict):
        messages.append("memory lookup der_configuration_control_index: derivative is not retrievable")
    else:
        if derivative_result.get("authority_class") != "generated_derivative":
            messages.append("memory lookup der_configuration_control_index: derivative authority is not explicit")
        if derivative_result.get("derivative_freshness") != "current":
            messages.append("memory lookup der_configuration_control_index: current derivative freshness is not explicit")

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            "Format governance surface: 10/10 requirements verified across five core profiles, policy, and memory retrieval.",
            "All profile axes are populated; project-specific extensions require controlled validation and cannot weaken core authority.",
            "Memory retrieval exposes source path, format profile, authority class, registry evidence, validator status, and derivative freshness.",
        ],
    )
