"""Focused verification for the bounded TOML configuration evidence family."""

from __future__ import annotations

import ast
from collections import Counter
from fnmatch import fnmatchcase
from pathlib import Path

from .derivatives import check_config_control_wiki
from .registry_io import RegistryLoadError, read_registry_rows, resolve_registered_path
from .toml_io import TomlLoadError, load_toml
from .validators import (
    ValidationResult,
    validate_config_sources,
    validate_control_records,
    validate_toml_config,
)


TOML_PROFILE = {
    "extension": ".toml",
    "format_family": "TOML",
    "primary_role": "project_configuration",
    "canonical_roots": "pyproject.toml;configs/;templates/config/",
    "derivative_surfaces": "configuration_control_wiki",
    "registry_required": "true",
    "validator_required": "true",
    "default_authority_class": "configuration_source",
    "promotion_rule": "config_change_transaction",
    "secrets_allowed": "false",
}
REQUIRED_CONFIG_FIELDS = (
    "config_id",
    "path",
    "format",
    "config_domain",
    "authority_status",
    "owner",
    "parser",
    "validation_contract_id",
    "consumers",
    "secrets_allowed",
    "environment_scope",
    "notes",
)
REQUIRED_ASSIGNMENT_TERMS = (
    "TOML is for project, package, tool, runtime, framework, and target-project configuration.",
    "TOML sources require size-limited parsing and contract validation where a contract exists.",
    "Phase 1 provides scaffold validation. It does not implement a production memory database, full wiki engine, TOML writing, or semantic acceptance validation.",
)
REQUIRED_WIKI_TERMS = (
    "Covered TOML artifacts include project, package, framework, tool, runtime, and target-project configuration.",
    "The Configuration and Control Wiki is a generated reader surface. It is not canonical.",
)
FORBIDDEN_WRITE_CALLS = {"open", "write_text", "write_bytes", "dump", "dumps"}


def validate_toml_config_surface(
    pyproject: str | Path = "pyproject.toml",
    requirements: str | Path = "requirements.txt",
    format_profiles: str | Path = "registries/format_profile_registry.csv",
    config_sources: str | Path = "registries/config_source_registry.csv",
    validation_contracts: str | Path = "registries/validation_contract_registry.csv",
    control_records: str | Path = "registries/control_record_registry.csv",
    format_policy: str | Path = "docs/format_profile_policy.md",
    wiki_policy: str | Path = "docs/configuration_control_wiki_policy.md",
    generated_toml_page: str | Path = "docs/generated/configuration_control/toml-configuration-sources.md",
    toml_io_source: str | Path = "sys_for_ai/toml_io.py",
    product_root: str | Path = ".",
) -> ValidationResult:
    """Verify seven TOML requirements and two Phase 0 assignments fail closed."""

    root = Path(product_root).resolve()
    pyproject_path = resolve_registered_path(str(pyproject), root)
    requirements_path = resolve_registered_path(str(requirements), root)
    format_path = resolve_registered_path(str(format_profiles), root)
    config_path = resolve_registered_path(str(config_sources), root)
    contract_path = resolve_registered_path(str(validation_contracts), root)
    control_path = resolve_registered_path(str(control_records), root)
    format_policy_path = resolve_registered_path(str(format_policy), root)
    wiki_policy_path = resolve_registered_path(str(wiki_policy), root)
    generated_toml_path = resolve_registered_path(str(generated_toml_page), root)
    toml_io_path = resolve_registered_path(str(toml_io_source), root)
    messages: list[str] = []

    try:
        format_rows = read_registry_rows(format_path)
        config_rows = read_registry_rows(config_path)
        contract_rows = read_registry_rows(contract_path)
    except RegistryLoadError as exc:
        return ValidationResult(False, [str(exc)])

    profiles = [row for row in format_rows if row.get("format_id") == "fmt_toml_config"]
    if len(profiles) != 1:
        messages.append(f"{format_path}: expected exactly one fmt_toml_config row")
    else:
        for field, value in TOML_PROFILE.items():
            if profiles[0].get(field) != value:
                messages.append(f"{format_path}: fmt_toml_config {field} must be {value!r}")

    config_ids = [row.get("config_id", "") for row in config_rows]
    config_paths = [row.get("path", "") for row in config_rows]
    messages.extend(_duplicates(config_path, "config_id", config_ids))
    messages.extend(_duplicates(config_path, "path", config_paths))
    if not config_rows:
        messages.append(f"{config_path}: no registered TOML configuration sources")

    contracts = {row.get("contract_id", ""): row for row in contract_rows}
    for index, row in enumerate(config_rows, start=2):
        config_id = row.get("config_id", "") or f"row-{index}"
        label = f"{config_path}:{index}: {config_id}"
        for field in REQUIRED_CONFIG_FIELDS:
            if not row.get(field, "").strip():
                messages.append(f"{label}: {field} must be populated")
        if row.get("format") != "toml":
            messages.append(f"{label}: format must be 'toml'")
        if row.get("parser") != "tomllib_or_tomli":
            messages.append(f"{label}: parser must be 'tomllib_or_tomli'")
        if row.get("secrets_allowed") != "false":
            messages.append(f"{label}: secrets_allowed must be 'false'")

        source = resolve_registered_path(row.get("path", ""), root)
        if source.suffix.lower() != ".toml":
            messages.append(f"{label}: registered source must use the .toml extension")
        elif source.exists():
            try:
                document = load_toml(source)
            except TomlLoadError as exc:
                messages.append(str(exc))
            else:
                if not isinstance(document, dict):
                    messages.append(f"{source}: parsed TOML root must be a dictionary")

        contract_id = row.get("validation_contract_id", "")
        contract = contracts.get(contract_id)
        if contract is None:
            messages.append(f"{label}: unknown validation contract {contract_id!r}")
        else:
            if contract.get("target_format") != "toml":
                messages.append(f"{label}: contract {contract_id} must target TOML")
            target_globs = {part for part in contract.get("target_glob", "").split(";") if part}
            if not any(fnmatchcase(row.get("path", ""), pattern) for pattern in target_globs):
                messages.append(f"{label}: contract {contract_id} does not target {row.get('path')!r}")

    structural = validate_config_sources(config_path)
    if not structural.ok:
        messages.extend(structural.messages)
    parsed = validate_toml_config(config_path)
    if not parsed.ok:
        messages.extend(parsed.messages)

    messages.extend(_validate_parser_policy(pyproject_path, requirements_path, toml_io_path))
    messages.extend(_validate_policy(format_policy_path, REQUIRED_ASSIGNMENT_TERMS))
    messages.extend(_validate_policy(wiki_policy_path, REQUIRED_WIKI_TERMS))
    messages.extend(_validate_generated_toml_page(generated_toml_path, config_rows))

    yaml_secret_check = validate_control_records(control_path)
    if not yaml_secret_check.ok:
        messages.extend(f"YAML/TOML example secret policy: {message}" for message in yaml_secret_check.messages)

    generated = check_config_control_wiki(root)
    if not generated.ok:
        messages.extend(generated.messages)

    if messages:
        return ValidationResult(False, sorted(dict.fromkeys(messages)))
    return ValidationResult(
        True,
        [
            "TOML configuration surface: 9/9 requirements verified across assignment, registration, parsing, contracts, secret policy, and generated indexing.",
            f"Registered TOML: {len(config_rows)} controlled configuration sources parse to mappings and bind to TOML validation contracts.",
            "Python 3.10 fallback, parse-only scope, secret-like values, registry drift, missing contracts, and stale Configuration and Control Wiki output fail closed.",
        ],
    )


def _duplicates(path: Path, field: str, values: list[str]) -> list[str]:
    duplicates = sorted(value for value, count in Counter(values).items() if value and count > 1)
    return [f"{path}: duplicate {field} {value!r}" for value in duplicates]


def _validate_policy(path: Path, terms: tuple[str, ...]) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Cannot read TOML policy {path}: {exc}"]
    return [f"{path}: missing TOML policy term {term!r}" for term in terms if term not in text]


def _validate_generated_toml_page(path: Path, rows: list[dict[str, str]]) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Cannot read generated TOML index {path}: {exc}"]
    messages: list[str] = []
    for row in rows:
        config_id = row.get("config_id", "")
        source_path = row.get("path", "")
        if config_id not in text or source_path not in text:
            messages.append(f"{path}: stale generated TOML index omits {config_id} at {source_path}")
    if "generated reader surface. It is not canonical" not in text:
        messages.append(f"{path}: generated TOML index lacks noncanonical authority notice")
    return messages


def _validate_parser_policy(pyproject: Path, requirements: Path, toml_io_source: Path) -> list[str]:
    messages: list[str] = []
    try:
        project = load_toml(pyproject)
    except TomlLoadError as exc:
        return [str(exc)]
    project_table = project.get("project", {})
    requires_python = project_table.get("requires-python") if isinstance(project_table, dict) else None
    dependencies = project_table.get("dependencies", []) if isinstance(project_table, dict) else []
    fallback = "tomli>=2.0,<3.0; python_version < '3.11'"
    if requires_python != ">=3.10":
        messages.append(f"{pyproject}: supported Python range must remain '>=3.10'")
    if not isinstance(dependencies, list) or fallback not in dependencies:
        messages.append(f"{pyproject}: conditional Python 3.10 tomli fallback is missing")
    try:
        requirements_text = requirements.read_text(encoding="utf-8")
    except OSError as exc:
        messages.append(f"Cannot read dependency policy {requirements}: {exc}")
    else:
        if fallback not in requirements_text.splitlines():
            messages.append(f"{requirements}: conditional Python 3.10 tomli fallback is missing")

    try:
        source = toml_io_source.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(toml_io_source))
    except (OSError, SyntaxError) as exc:
        messages.append(f"{toml_io_source}: cannot inspect TOML parser policy: {exc}")
        return messages
    for term in ("import tomllib", "except ModuleNotFoundError", "import tomli as tomllib"):
        if term not in source:
            messages.append(f"{toml_io_source}: missing parser fallback term {term!r}")
    public_functions = {
        node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    }
    if public_functions != {"load_toml"}:
        messages.append(f"{toml_io_source}: Phase 1 TOML API must remain parse-only")
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.id if isinstance(node.func, ast.Name) else (
            node.func.attr if isinstance(node.func, ast.Attribute) else ""
        )
        if name in FORBIDDEN_WRITE_CALLS:
            messages.append(f"{toml_io_source}:{node.lineno}: TOML writing call {name!r} is out of scope")
    return messages
