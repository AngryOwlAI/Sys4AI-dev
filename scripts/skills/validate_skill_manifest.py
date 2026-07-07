#!/usr/bin/env python3
"""Validate skill operating-layer manifests with only the Python standard library.

This is not a complete JSON Schema Draft 2020-12 implementation. It is a
repository-local validator for the fields and invariants defined by the Phase 1
schemas and Phase 2 scaffolding.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SKILL_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DOMAIN_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
ROLE_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
BASELINE_ROLES = {"system_analyst", "system_engineer", "software_engineer"}
VALIDATOR_CLASSES = {
    "schema_validation",
    "path_validation",
    "dependency_validation",
    "trace_validation",
    "process_validation",
    "domain_validation",
    "claim_validation",
}
LIFECYCLE_STATUSES = {
    "proposed",
    "imported_unadapted",
    "adapter_shell",
    "adapted_runtime_active",
    "product_scaffold_reference",
    "deprecated",
    "superseded",
    "blocked",
}
EXECUTABLE_RUNTIME_LIFECYCLES = {"adapted_runtime_active"}


@dataclass(frozen=True)
class Finding:
    path: Path
    kind: str
    message: str


class SimpleYamlError(ValueError):
    """Raised when a file uses YAML outside the supported subset."""


def strip_yaml_comment(line: str) -> str:
    quote: str | None = None
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if quote and char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char == "#":
            return line[:index]
    return line


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item) for item in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if re.fullmatch(r"-?[0-9]+", value):
        return int(value)
    return value


def split_inline_mapping_item(value: str) -> tuple[str, str] | None:
    match = re.match(r"^([A-Za-z0-9_.-]+):(?:\s+(.*)|$)", value)
    if not match:
        return None
    return match.group(1), match.group(2) or ""


def parse_simple_yaml(text: str, path: Path) -> Any:
    lines: list[tuple[int, int, str]] = []
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        if "\t" in raw_line[: len(raw_line) - len(raw_line.lstrip())]:
            raise SimpleYamlError(f"{path}:{line_number}: tabs are not supported")
        line = strip_yaml_comment(raw_line).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        lines.append((line_number, indent, line[indent:]))

    if not lines:
        return None

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(lines):
            return {}, index
        line_number, current_indent, content = lines[index]
        if current_indent < indent:
            return {}, index
        if current_indent > indent:
            raise SimpleYamlError(
                f"{path}:{line_number}: unexpected indentation level {current_indent}"
            )
        if content.startswith("- "):
            return parse_sequence(index, indent)
        return parse_mapping(index, indent)

    def parse_mapping(index: int, indent: int) -> tuple[dict[str, Any], int]:
        data: dict[str, Any] = {}
        while index < len(lines):
            line_number, current_indent, content = lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise SimpleYamlError(
                    f"{path}:{line_number}: unexpected indentation level {current_indent}"
                )
            if content.startswith("- "):
                break
            key, separator, remainder = content.partition(":")
            if not separator or not key.strip():
                raise SimpleYamlError(f"{path}:{line_number}: expected key: value")
            key = key.strip()
            remainder = remainder.strip()
            index += 1
            if remainder:
                data[key] = parse_scalar(remainder)
                continue
            if index < len(lines) and lines[index][1] > current_indent:
                data[key], index = parse_block(index, lines[index][1])
            else:
                data[key] = {}
        return data, index

    def parse_sequence(index: int, indent: int) -> tuple[list[Any], int]:
        values: list[Any] = []
        while index < len(lines):
            line_number, current_indent, content = lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise SimpleYamlError(
                    f"{path}:{line_number}: unexpected indentation level {current_indent}"
                )
            if not content.startswith("- "):
                break
            item = content[2:].strip()
            index += 1
            if not item:
                if index < len(lines) and lines[index][1] > current_indent:
                    value, index = parse_block(index, lines[index][1])
                else:
                    value = None
                values.append(value)
                continue
            inline_mapping = split_inline_mapping_item(item)
            if inline_mapping:
                key, remainder = inline_mapping
                value = parse_scalar(remainder) if remainder else {}
                item_data: dict[str, Any] = {key: value}
                if index < len(lines) and lines[index][1] > current_indent:
                    child, index = parse_block(index, lines[index][1])
                    if not isinstance(child, dict):
                        raise SimpleYamlError(
                            f"{path}:{line_number}: sequence mapping expects nested keys"
                        )
                    item_data.update(child)
                values.append(item_data)
                continue
            values.append(parse_scalar(item))
        return values, index

    value, next_index = parse_block(0, lines[0][1])
    if next_index != len(lines):
        line_number = lines[next_index][0]
        raise SimpleYamlError(f"{path}:{line_number}: could not parse remaining content")
    return value


def load_structured_file(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    if path.suffix in {".yaml", ".yml"}:
        return parse_simple_yaml(text, path)
    raise ValueError(f"unsupported file extension: {path.suffix}")


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_string_list(value: Any, *, non_empty: bool = False) -> bool:
    if not isinstance(value, list):
        return False
    if non_empty and not value:
        return False
    return all(is_non_empty_string(item) for item in value)


def is_unique_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) == len(set(value))


def relative_path_is_safe(value: Any) -> bool:
    return is_non_empty_string(value) and not str(value).startswith("/")


def add_required_errors(
    findings: list[Finding], path: Path, kind: str, data: Any, required: list[str]
) -> None:
    if not isinstance(data, dict):
        findings.append(Finding(path, kind, "top-level value must be a mapping"))
        return
    for key in required:
        if key not in data:
            findings.append(Finding(path, kind, f"missing required key: {key}"))


def check_skill_id_list(
    findings: list[Finding], path: Path, kind: str, field: str, value: Any
) -> None:
    if not isinstance(value, list):
        findings.append(Finding(path, kind, f"{field} must be a list"))
        return
    if not is_unique_list(value):
        findings.append(Finding(path, kind, f"{field} must not contain duplicates"))
    for skill_id in value:
        if not isinstance(skill_id, str) or not SKILL_ID_RE.fullmatch(skill_id):
            findings.append(Finding(path, kind, f"{field} contains invalid skill id: {skill_id!r}"))


def validate_skill_manifest(data: Any, path: Path, repo_root: Path) -> list[Finding]:
    kind = "skill_manifest"
    findings: list[Finding] = []
    required = [
        "skill_id",
        "version",
        "status",
        "lifecycle_status",
        "canonical_path",
        "summary",
        "scope",
        "domain_emphasis",
        "required_role_posture",
        "activation",
        "inputs",
        "outputs",
        "dependencies",
        "authority",
        "validation",
        "handoff",
    ]
    add_required_errors(findings, path, kind, data, required)
    if findings:
        return findings

    skill_id = data["skill_id"]
    if not isinstance(skill_id, str) or not SKILL_ID_RE.fullmatch(skill_id):
        findings.append(Finding(path, kind, "skill_id must use lowercase kebab-case"))
    if path.name in {"skill.yaml", "skill.yml"} and path.parent.name != skill_id:
        findings.append(
            Finding(path, kind, f"skill_id {skill_id!r} must match folder {path.parent.name!r}")
        )
    if not isinstance(data["version"], str) or not SEMVER_RE.fullmatch(data["version"]):
        findings.append(Finding(path, kind, "version must be semantic versioning"))
    if data["status"] not in {"candidate", "draft", "template", "active", "deprecated", "shim"}:
        findings.append(Finding(path, kind, "status is not an allowed lifecycle value"))
    lifecycle_status = data.get("lifecycle_status")
    if lifecycle_status not in LIFECYCLE_STATUSES:
        findings.append(Finding(path, kind, "lifecycle_status is not in the controlled vocabulary"))
    elif data["status"] == "active" and lifecycle_status not in EXECUTABLE_RUNTIME_LIFECYCLES:
        findings.append(Finding(path, kind, "active skill manifests must use adapted_runtime_active lifecycle_status"))
    if not relative_path_is_safe(data["canonical_path"]):
        findings.append(Finding(path, kind, "canonical_path must be a relative path"))
    elif str(data["canonical_path"]).startswith(".codex/"):
        findings.append(Finding(path, kind, "canonical_path must not point at a compatibility shim"))
    if not is_non_empty_string(data["summary"]):
        findings.append(Finding(path, kind, "summary must be a non-empty string"))

    scope = data["scope"]
    if not isinstance(scope, dict):
        findings.append(Finding(path, kind, "scope must be a mapping"))
    else:
        if not isinstance(scope.get("system_agnostic"), bool):
            findings.append(Finding(path, kind, "scope.system_agnostic must be boolean"))
        if not is_string_list(scope.get("target_system_types"), non_empty=True):
            findings.append(
                Finding(path, kind, "scope.target_system_types must be a non-empty string list")
            )

    if not is_string_list(data["domain_emphasis"], non_empty=True):
        findings.append(Finding(path, kind, "domain_emphasis must be a non-empty string list"))

    roles = data["required_role_posture"]
    if not is_string_list(roles, non_empty=True):
        findings.append(Finding(path, kind, "required_role_posture must be a non-empty list"))
    else:
        for role in roles:
            if not ROLE_ID_RE.fullmatch(role):
                findings.append(Finding(path, kind, f"invalid role identifier: {role}"))
        exemptions = set(scope.get("exemptions", [])) if isinstance(scope, dict) else set()
        if "required_role_posture" not in exemptions and not BASELINE_ROLES.issubset(set(roles)):
            missing = ", ".join(sorted(BASELINE_ROLES.difference(set(roles))))
            findings.append(Finding(path, kind, f"missing baseline role posture: {missing}"))

    activation = data["activation"]
    if not isinstance(activation, dict) or not is_string_list(
        activation.get("triggers"), non_empty=True
    ):
        findings.append(Finding(path, kind, "activation.triggers must be a non-empty list"))

    inputs = data["inputs"]
    if not isinstance(inputs, dict):
        findings.append(Finding(path, kind, "inputs must be a mapping"))
    else:
        if not is_string_list(inputs.get("required", [])):
            findings.append(Finding(path, kind, "inputs.required must be a string list"))
        if not is_string_list(inputs.get("optional", [])):
            findings.append(Finding(path, kind, "inputs.optional must be a string list"))

    outputs = data["outputs"]
    if not isinstance(outputs, dict):
        findings.append(Finding(path, kind, "outputs must be a mapping"))
    elif not (
        is_string_list(outputs.get("primary"), non_empty=True)
        or is_string_list(outputs.get("evidence"), non_empty=True)
    ):
        findings.append(Finding(path, kind, "outputs must define primary or evidence entries"))

    dependencies = data["dependencies"]
    if not isinstance(dependencies, dict):
        findings.append(Finding(path, kind, "dependencies must be a mapping"))
    else:
        for field in ["required_skills", "optional_skills"]:
            check_skill_id_list(findings, path, kind, f"dependencies.{field}", dependencies.get(field))
        python_deps = dependencies.get("python")
        if python_deps is not None:
            if not isinstance(python_deps, dict):
                findings.append(Finding(path, kind, "dependencies.python must be null or a mapping"))
            else:
                req_file = python_deps.get("requirements_file")
                if req_file is not None:
                    if not relative_path_is_safe(req_file):
                        findings.append(
                            Finding(path, kind, "dependencies.python.requirements_file must be relative")
                        )
                    elif not (path.parent / req_file).exists() and not (repo_root / req_file).exists():
                        findings.append(
                            Finding(
                                path,
                                kind,
                                f"requirements file does not exist: {req_file}",
                            )
                        )

    authority = data["authority"]
    if not isinstance(authority, dict):
        findings.append(Finding(path, kind, "authority must be a mapping"))
    else:
        for field, non_empty in [("may_read", True), ("may_write", False), ("may_not", True)]:
            if not is_string_list(authority.get(field), non_empty=non_empty):
                findings.append(Finding(path, kind, f"authority.{field} must be a string list"))

    validation = data["validation"]
    if not isinstance(validation, dict):
        findings.append(Finding(path, kind, "validation must be a mapping"))
    else:
        commands = validation.get("commands")
        if not isinstance(commands, list):
            findings.append(Finding(path, kind, "validation.commands must be a list"))
        elif not commands and not is_non_empty_string(
            validation.get("contextual_validation_rationale")
        ):
            findings.append(
                Finding(
                    path,
                    kind,
                    "empty validation.commands requires contextual_validation_rationale",
                )
            )
        classes = validation.get("validator_classes")
        if not is_string_list(classes, non_empty=True):
            findings.append(
                Finding(path, kind, "validation.validator_classes must be a non-empty list")
            )
        else:
            for validator_class in classes:
                if validator_class not in VALIDATOR_CLASSES:
                    findings.append(
                        Finding(path, kind, f"unknown validator class: {validator_class}")
                    )

    handoff = data["handoff"]
    if not isinstance(handoff, dict):
        findings.append(Finding(path, kind, "handoff must be a mapping"))
    else:
        if not isinstance(handoff.get("requires_completion_receipt"), bool):
            findings.append(
                Finding(path, kind, "handoff.requires_completion_receipt must be boolean")
            )
        if not is_string_list(handoff.get("evidence"), non_empty=True):
            findings.append(Finding(path, kind, "handoff.evidence must be a non-empty list"))

    return findings


def validate_registry(data: Any, path: Path, repo_root: Path) -> tuple[list[Finding], set[str]]:
    kind = "skill_registry"
    findings: list[Finding] = []
    skill_ids: set[str] = set()
    add_required_errors(findings, path, kind, data, ["version", "status", "skills"])
    if findings:
        return findings, skill_ids
    if data["status"] not in {"draft", "active", "deprecated"}:
        findings.append(Finding(path, kind, "status must be draft, active, or deprecated"))
    skills = data["skills"]
    if not isinstance(skills, list):
        findings.append(Finding(path, kind, "skills must be a list"))
        return findings, skill_ids

    for index, entry in enumerate(skills):
        prefix = f"skills[{index}]"
        if not isinstance(entry, dict):
            findings.append(Finding(path, kind, f"{prefix} must be a mapping"))
            continue
        skill_id = entry.get("skill_id")
        if not isinstance(skill_id, str) or not SKILL_ID_RE.fullmatch(skill_id):
            findings.append(Finding(path, kind, f"{prefix}.skill_id is invalid"))
            continue
        if skill_id in skill_ids:
            findings.append(Finding(path, kind, f"duplicate skill_id: {skill_id}"))
        skill_ids.add(skill_id)
        lifecycle_status = entry.get("lifecycle_status")
        migration_phase = entry.get("migration_phase")
        if lifecycle_status not in LIFECYCLE_STATUSES:
            findings.append(Finding(path, kind, f"{skill_id}: lifecycle_status is not in the controlled vocabulary"))
        if migration_phase is not None and lifecycle_status is not None and migration_phase != lifecycle_status:
            findings.append(Finding(path, kind, f"{skill_id}: migration_phase must match lifecycle_status during transition"))
        if entry.get("status") == "active" and lifecycle_status not in EXECUTABLE_RUNTIME_LIFECYCLES:
            findings.append(Finding(path, kind, f"{skill_id}: active registry entry must use adapted_runtime_active lifecycle_status"))
        skill_path = entry.get("canonical_path") or entry.get("template_path")
        if not relative_path_is_safe(skill_path):
            findings.append(Finding(path, kind, f"{skill_id}: canonical_path must be relative"))
        elif str(skill_path).startswith(".codex/"):
            findings.append(Finding(path, kind, f"{skill_id}: canonical_path must not point at .codex compatibility shim"))
        else:
            resolved = repo_root / str(skill_path)
            if not resolved.exists():
                findings.append(Finding(path, kind, f"{skill_id}: path does not exist: {skill_path}"))
            elif not (resolved / "SKILL.md").exists():
                findings.append(Finding(path, kind, f"{skill_id}: SKILL.md missing at {skill_path}"))
        for shim_path in entry.get("compatibility_shims", []):
            if not isinstance(shim_path, str) or not shim_path.startswith(".codex/"):
                findings.append(Finding(path, kind, f"{skill_id}: compatibility_shims must point under .codex"))
            if shim_path == skill_path:
                findings.append(Finding(path, kind, f"{skill_id}: compatibility shim cannot be canonical_path"))
        manifest_path = entry.get("manifest_path")
        if manifest_path is not None:
            if not relative_path_is_safe(manifest_path):
                findings.append(Finding(path, kind, f"{skill_id}: manifest_path must be relative"))
            elif not (repo_root / str(manifest_path)).exists():
                findings.append(
                    Finding(path, kind, f"{skill_id}: manifest_path does not exist: {manifest_path}")
                )
        required_skills = entry.get("required_skills", [])
        check_skill_id_list(findings, path, kind, f"{skill_id}.required_skills", required_skills)
        optional_skills = entry.get("optional_skills", [])
        check_skill_id_list(findings, path, kind, f"{skill_id}.optional_skills", optional_skills)
        python_requirements = entry.get("python_requirements")
        if python_requirements is not None:
            if not relative_path_is_safe(python_requirements):
                findings.append(
                    Finding(path, kind, f"{skill_id}: python_requirements must be relative")
                )
            elif not (repo_root / str(python_requirements)).exists():
                findings.append(
                    Finding(
                        path,
                        kind,
                        f"{skill_id}: python requirements missing: {python_requirements}",
                    )
                )

    for entry in skills:
        if not isinstance(entry, dict):
            continue
        skill_id = entry.get("skill_id")
        if not isinstance(skill_id, str):
            continue
        for required_skill in entry.get("required_skills", []):
            if required_skill not in skill_ids:
                findings.append(
                    Finding(path, kind, f"{skill_id}: missing required skill {required_skill}")
                )

    return findings, skill_ids


def validate_skill_bundle(
    data: Any, path: Path, registry_skill_ids: set[str] | None
) -> list[Finding]:
    kind = "skill_bundle"
    findings: list[Finding] = []
    required = ["bundle_id", "version", "status", "description", "includes", "install", "lock"]
    add_required_errors(findings, path, kind, data, required)
    if findings:
        return findings
    if not isinstance(data["bundle_id"], str) or not SKILL_ID_RE.fullmatch(data["bundle_id"]):
        findings.append(Finding(path, kind, "bundle_id must use lowercase kebab-case"))
    if not isinstance(data["version"], str) or not SEMVER_RE.fullmatch(data["version"]):
        findings.append(Finding(path, kind, "version must be semantic versioning"))
    if data["status"] not in {"draft", "active", "deprecated"}:
        findings.append(Finding(path, kind, "status must be draft, active, or deprecated"))
    if not is_non_empty_string(data["description"]):
        findings.append(Finding(path, kind, "description must be a non-empty string"))

    includes = data["includes"]
    if not isinstance(includes, dict):
        findings.append(Finding(path, kind, "includes must be a mapping"))
    else:
        check_skill_id_list(findings, path, kind, "includes.skills", includes.get("skills"))
        domain_packs = includes.get("domain_packs")
        if not isinstance(domain_packs, list):
            findings.append(Finding(path, kind, "includes.domain_packs must be a list"))
        else:
            for domain_id in domain_packs:
                if not isinstance(domain_id, str) or not DOMAIN_ID_RE.fullmatch(domain_id):
                    findings.append(
                        Finding(path, kind, f"includes.domain_packs has invalid id: {domain_id}")
                    )
        if registry_skill_ids is not None:
            for skill_id in includes.get("skills", []):
                if skill_id not in registry_skill_ids:
                    findings.append(
                        Finding(path, kind, f"includes unknown registry skill: {skill_id}")
                    )

    install = data["install"]
    if not isinstance(install, dict):
        findings.append(Finding(path, kind, "install must be a mapping"))
    else:
        if not isinstance(install.get("python"), bool):
            findings.append(Finding(path, kind, "install.python must be boolean"))
        external_tools = install.get("external_tools")
        if not isinstance(external_tools, dict):
            findings.append(Finding(path, kind, "install.external_tools must be a mapping"))

    lock = data["lock"]
    if not isinstance(lock, dict) or not relative_path_is_safe(lock.get("output")):
        findings.append(Finding(path, kind, "lock.output must be a relative path"))
    return findings


def validate_domain_pack(data: Any, path: Path, registry_skill_ids: set[str] | None) -> list[Finding]:
    kind = "domain_pack"
    findings: list[Finding] = []
    required = [
        "domain_id",
        "version",
        "status",
        "summary",
        "vocabulary",
        "constraints",
        "artifacts",
        "verification",
        "risks",
        "continuation_policy",
    ]
    add_required_errors(findings, path, kind, data, required)
    if findings:
        return findings
    if not isinstance(data["domain_id"], str) or not DOMAIN_ID_RE.fullmatch(data["domain_id"]):
        findings.append(Finding(path, kind, "domain_id must use lowercase snake_case"))
    if not isinstance(data["version"], str) or not SEMVER_RE.fullmatch(data["version"]):
        findings.append(Finding(path, kind, "version must be semantic versioning"))
    if data["status"] not in {"draft", "active", "deprecated"}:
        findings.append(Finding(path, kind, "status must be draft, active, or deprecated"))
    for field in ["vocabulary", "constraints", "artifacts", "verification", "risks"]:
        if not isinstance(data.get(field), list) or not data[field]:
            findings.append(Finding(path, kind, f"{field} must be a non-empty list"))
    for field in ["domain_required_skills", "recommended_skills"]:
        if field in data:
            check_skill_id_list(findings, path, kind, field, data[field])
            if registry_skill_ids is not None:
                for skill_id in data[field]:
                    if skill_id not in registry_skill_ids:
                        findings.append(Finding(path, kind, f"{field} references unknown skill {skill_id}"))
    if not isinstance(data["continuation_policy"], dict):
        findings.append(Finding(path, kind, "continuation_policy must be a mapping"))
    return findings


def discover_default_paths(repo_root: Path) -> dict[str, list[Path]]:
    registry = repo_root / ".agents" / "skill_registry" / "SKILL_REGISTRY.yaml"
    return {
        "registry": [registry] if registry.exists() else [],
        "manifest": sorted(repo_root.glob("skills/*/skill.y*ml"))
        + sorted(repo_root.glob(".agents/skills/*/skill.y*ml")),
        "bundle": sorted((repo_root / ".agents" / "skill_registry" / "SKILL_BUNDLES").glob("*.y*ml")),
        "domain_pack": sorted((repo_root / ".agents" / "domain_packs").glob("*.y*ml")),
    }


def validate_file(
    path: Path,
    kind: str,
    repo_root: Path,
    registry_skill_ids: set[str] | None,
) -> tuple[list[Finding], set[str] | None]:
    try:
        data = load_structured_file(path)
    except Exception as exc:  # noqa: BLE001 - this is a CLI boundary.
        return [Finding(path, kind, f"could not parse file: {exc}")], None

    if kind == "manifest":
        return validate_skill_manifest(data, path, repo_root), None
    if kind == "registry":
        findings, skill_ids = validate_registry(data, path, repo_root)
        return findings, skill_ids
    if kind == "bundle":
        return validate_skill_bundle(data, path, registry_skill_ids), None
    if kind == "domain_pack":
        return validate_domain_pack(data, path, registry_skill_ids), None
    raise ValueError(f"unknown validation kind: {kind}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Phase 1/2 skill operating-layer files without external packages."
    )
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--manifest", action="append", default=[], help="skill.yaml path to validate.")
    parser.add_argument("--registry", action="append", default=[], help="SKILL_REGISTRY.yaml path.")
    parser.add_argument("--bundle", action="append", default=[], help="Skill bundle YAML path.")
    parser.add_argument("--domain-pack", action="append", default=[], help="Domain pack YAML path.")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print failures. The exit code still reports success or failure.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = Path(args.root).resolve()

    explicit = any([args.manifest, args.registry, args.bundle, args.domain_pack])
    if explicit:
        paths = {
            "registry": [Path(item) for item in args.registry],
            "manifest": [Path(item) for item in args.manifest],
            "bundle": [Path(item) for item in args.bundle],
            "domain_pack": [Path(item) for item in args.domain_pack],
        }
    else:
        paths = discover_default_paths(repo_root)

    all_findings: list[Finding] = []
    registry_skill_ids: set[str] | None = None
    successful: list[tuple[Path, str]] = []

    for raw_registry_path in paths["registry"]:
        registry_path = (
            raw_registry_path if raw_registry_path.is_absolute() else repo_root / raw_registry_path
        )
        findings, skill_ids = validate_file(registry_path, "registry", repo_root, None)
        all_findings.extend(findings)
        if not findings:
            successful.append((registry_path, "skill_registry"))
            registry_skill_ids = skill_ids or set()

    for kind in ["manifest", "bundle", "domain_pack"]:
        for raw_path in paths[kind]:
            path = raw_path if raw_path.is_absolute() else repo_root / raw_path
            findings, _ = validate_file(path, kind, repo_root, registry_skill_ids)
            all_findings.extend(findings)
            if not findings:
                label = {"manifest": "skill_manifest", "bundle": "skill_bundle", "domain_pack": "domain_pack"}[
                    kind
                ]
                successful.append((path, label))

    if all_findings:
        for finding in all_findings:
            print(f"FAIL {finding.kind}: {finding.path}: {finding.message}", file=sys.stderr)
        return 1

    if not args.quiet:
        if not successful:
            print("OK: no matching files discovered")
        for path, label in successful:
            print(f"OK {label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
