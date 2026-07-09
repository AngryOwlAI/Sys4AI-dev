"""Role-governance validators for controlled role registries and derivatives."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .registry_io import read_registry_rows, resolve_registered_path
from .roles import (
    GENERATED_ROLE_DOC_NOTICE,
    ROLE_CLASSES,
    TEMPORARY_ROLE_CLASS,
    crosswalk_by_role,
    expected_role_docs,
    load_crosswalk_rows,
    load_execution_binding_rows,
    load_role_rows,
    split_semicolon,
)
from .validators import (
    ROW_CONTRACTS,
    ValidationResult,
    _check_layer_scope,
    _known_proposed_skill_ids,
    _known_system_layers,
    _load_skill_ids,
    _split_selectors,
    _validate_rows_against_contract,
)
from .yaml_io import load_yaml


PASS_MARKERS = ("row validation passed", "validation passed")


def validate_role_registry(path: str | Path = "registries/role_registry.csv") -> ValidationResult:
    result = _validate_rows_against_contract(path, ROW_CONTRACTS["role_registry.csv"], "role_id")
    messages: list[str] = []
    known_layers = _known_system_layers()
    known_skills = _load_skill_ids() | _known_proposed_skill_ids()

    for row in load_role_rows(path):
        role_id = row.get("role_id", "")
        role_class = row.get("role_class", "")
        if role_class not in ROLE_CLASSES:
            messages.append(f"{path}: {role_id}: unknown role_class {role_class!r}")
        messages.extend(_check_layer_scope(f"{path}: {role_id}", row.get("system_layer_scope", ""), known_layers))
        required = set(split_semicolon(row.get("required_skills", "")))
        optional = set(split_semicolon(row.get("optional_skills", "")))
        forbidden = set(split_semicolon(row.get("forbidden_skills", "")))
        for field_name, values in (
            ("required_skills", required),
            ("optional_skills", optional),
            ("forbidden_skills", forbidden),
        ):
            for skill_id in sorted(values):
                if skill_id not in known_skills:
                    messages.append(f"{path}: {role_id}: {field_name} references unknown or unapproved skill {skill_id!r}")
        overlap = sorted(forbidden & (required | optional))
        if overlap:
            messages.append(f"{path}: {role_id}: forbidden skills also required or optional: {';'.join(overlap)}")

    result.messages.extend(messages)
    result.ok = not _error_messages(result.messages)
    return result


def validate_role_skill_crosswalk(path: str | Path = "registries/role_skill_crosswalk.csv") -> ValidationResult:
    result = _validate_rows_against_contract(path, ROW_CONTRACTS["role_skill_crosswalk.csv"], "crosswalk_id")
    messages: list[str] = []
    role_ids = {row.get("role_id", "") for row in load_role_rows()}
    known_layers = _known_system_layers()
    known_skills = _load_skill_ids() | _known_proposed_skill_ids()

    for row in load_crosswalk_rows(path):
        crosswalk_id = row.get("crosswalk_id", "")
        role_id = row.get("role_id", "")
        skill_id = row.get("skill_id", "")
        if role_id not in role_ids:
            messages.append(f"{path}: {crosswalk_id}: unknown role_id {role_id!r}")
        if skill_id not in known_skills:
            messages.append(f"{path}: {crosswalk_id}: unknown or unapproved skill_id {skill_id!r}")
        messages.extend(_check_layer_scope(f"{path}: {crosswalk_id}", row.get("system_layer_scope", ""), known_layers))
        evidence = resolve_registered_path(row.get("evidence_path", ""))
        if not evidence.exists():
            messages.append(f"{path}: {crosswalk_id}: missing evidence_path {evidence}")

    result.messages.extend(messages)
    result.ok = not _error_messages(result.messages)
    return result


def validate_role_execution_bindings(
    path: str | Path = "registries/role_execution_binding_registry.csv",
) -> ValidationResult:
    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["role_execution_binding_registry.csv"],
        "binding_id",
    )
    messages: list[str] = []
    roles = load_role_rows()
    role_ids = {row.get("role_id", "") for row in roles}
    temporary_roles = {row.get("role_id", "") for row in roles if row.get("role_class") == TEMPORARY_ROLE_CLASS}
    bound_temporary_roles: set[str] = set()

    for row in load_execution_binding_rows(path):
        binding_id = row.get("binding_id", "")
        role_id = row.get("role_id", "")
        if role_id not in role_ids:
            messages.append(f"{path}: {binding_id}: unknown role_id {role_id!r}")
        if role_id in temporary_roles:
            bound_temporary_roles.add(role_id)
            expiry = row.get("expiry_policy", "").strip()
            if not expiry or expiry == "registered role no expiry":
                messages.append(f"{path}: {binding_id}: temporary role requires bounded expiry_policy")

    missing_temporary_bindings = sorted(temporary_roles - bound_temporary_roles)
    for role_id in missing_temporary_bindings:
        messages.append(f"{path}: {role_id}: temporary role missing execution binding")

    result.messages.extend(messages)
    result.ok = not _error_messages(result.messages)
    return result


def validate_role_graph(
    role_registry: str | Path = "registries/role_registry.csv",
    crosswalk: str | Path = "registries/role_skill_crosswalk.csv",
    execution_bindings: str | Path = "registries/role_execution_binding_registry.csv",
) -> ValidationResult:
    messages: list[str] = []
    roles = load_role_rows(role_registry)
    role_ids = {row.get("role_id", "") for row in roles}
    crosswalk_rows = load_crosswalk_rows(crosswalk)
    by_role = crosswalk_by_role(crosswalk_rows)

    for role_id, rows in by_role.items():
        bindings_by_skill: dict[str, set[str]] = {}
        for row in rows:
            bindings_by_skill.setdefault(row.get("skill_id", ""), set()).add(row.get("binding_type", ""))
        for skill_id, binding_types in sorted(bindings_by_skill.items()):
            if "forbidden" in binding_types and (binding_types - {"forbidden"}):
                messages.append(f"{crosswalk}: {role_id}: {skill_id}: forbidden binding conflicts with {sorted(binding_types)}")

    active_skills = _active_runtime_skill_ids()
    bound_skills = {
        row.get("skill_id", "")
        for row in crosswalk_rows
        if row.get("binding_type") != "forbidden" and row.get("skill_id")
    }
    for skill_id in sorted(active_skills - bound_skills):
        messages.append(f"{crosswalk}: active runtime skill {skill_id!r} has no role binding")

    for path, role_id in _agentjob_role_references():
        if role_id and role_id not in role_ids:
            messages.append(f"{path}: legacy control role {role_id!r} is not in role registry")

    binding_role_ids = {row.get("role_id", "") for row in load_execution_binding_rows(execution_bindings)}
    for role in roles:
        role_id = role.get("role_id", "")
        if role.get("may_create_agentjobs") == "true" and role_id not in binding_role_ids:
            messages.append(f"{execution_bindings}: {role_id}: legacy AgentJob creation is enabled but no execution binding exists")

    return ValidationResult(not messages, messages or ["role graph validation passed"])


def validate_generated_role_docs(docs_root: str | Path = "docs/generated/roles") -> ValidationResult:
    root = Path(docs_root)
    messages: list[str] = []
    if not root.exists():
        return ValidationResult(False, [f"{root}: missing generated role docs directory"])

    expected = expected_role_docs(docs_root=root)
    derivative_rows = read_registry_rows("registries/derivative_registry.csv")
    derivatives_by_path = {row.get("path", ""): row for row in derivative_rows}

    for path, expected_text in sorted(expected.items()):
        registry_path = path.as_posix()
        if not path.exists():
            messages.append(f"{path}: missing generated role doc")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected_text:
            messages.append(f"{path}: generated role doc is stale")
        if GENERATED_ROLE_DOC_NOTICE not in actual:
            messages.append(f"{path}: missing generated derivative notice")
        row = derivatives_by_path.get(registry_path)
        if row is None:
            messages.append(f"registries/derivative_registry.csv: missing derivative row for {registry_path}")
            continue
        if row.get("status") != "generated_derivative":
            messages.append(f"registries/derivative_registry.csv: {row.get('derivative_id')}: role doc is not generated_derivative")
        if row.get("derivative_type") != "role_governance_page":
            messages.append(f"registries/derivative_registry.csv: {row.get('derivative_id')}: unexpected derivative_type")

    return ValidationResult(not messages, messages or ["generated role docs validation passed"])


def validate_roles(
    role_registry: str | Path = "registries/role_registry.csv",
    crosswalk: str | Path = "registries/role_skill_crosswalk.csv",
    execution_bindings: str | Path = "registries/role_execution_binding_registry.csv",
) -> ValidationResult:
    result = validate_role_registry(role_registry)
    result.extend(validate_role_skill_crosswalk(crosswalk))
    result.extend(validate_role_execution_bindings(execution_bindings))
    result.extend(validate_role_graph(role_registry, crosswalk, execution_bindings))
    result.extend(validate_generated_role_docs())
    result.ok = not _error_messages(result.messages)
    if result.ok and not result.messages:
        result.messages.append("roles: validation passed")
    return result


def _active_runtime_skill_ids(path: str | Path = "../.agents/skill_registry/SKILL_REGISTRY.yaml") -> set[str]:
    registry = Path(path)
    if not registry.exists():
        return set()
    data = load_yaml(registry)
    if not isinstance(data, dict):
        return set()
    skill_ids: set[str] = set()
    for item in data.get("skills", []):
        if isinstance(item, dict) and item.get("status") == "active" and item.get("skill_id"):
            skill_ids.add(str(item["skill_id"]))
    return skill_ids


def _agentjob_role_references(root: str | Path = "control_records/agentjobs") -> list[tuple[Path, str]]:
    target = Path(root)
    references: list[tuple[Path, str]] = []
    if not target.exists():
        return references
    for path in sorted(target.glob("*.yaml")):
        data = load_yaml(path)
        if not isinstance(data, dict):
            continue
        role_id = _agentjob_role_id(data)
        references.append((path, role_id))
    return references


def _agentjob_role_id(data: dict[str, Any]) -> str:
    role_binding = data.get("role_binding")
    if isinstance(role_binding, dict) and role_binding.get("role_id"):
        return str(role_binding["role_id"])
    if data.get("role"):
        return str(data["role"])
    return ""


def _error_messages(messages: list[str]) -> list[str]:
    return [message for message in messages if not any(marker in message for marker in PASS_MARKERS)]
