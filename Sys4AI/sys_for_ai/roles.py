"""Role registry helpers and generated role documentation builders."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .registry_io import read_registry_rows


ROLE_CLASSES = {
    "framework_governance",
    "system_design_core",
    "system_design_support",
    "implementation",
    "verification",
    "maintenance",
    "runtime_control",
    "temporary_legacy_role",
    "project_specific",
}
TEMPORARY_ROLE_CLASS = "temporary_legacy_role"
GENERATED_ROLE_DOC_NOTICE = (
    "> Generated derivative. Canonical role authority remains with "
    "`registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and "
    "`registries/role_execution_binding_registry.csv`."
)
ROLE_DOCS_ROOT = Path("docs/generated/roles")


def split_semicolon(value: str) -> list[str]:
    """Split semicolon-separated registry cells into non-empty selectors."""

    return [part.strip() for part in value.split(";") if part.strip()]


def load_role_rows(path: str | Path = "registries/role_registry.csv") -> list[dict[str, str]]:
    return sorted(read_registry_rows(path), key=lambda row: row.get("role_id", ""))


def load_crosswalk_rows(path: str | Path = "registries/role_skill_crosswalk.csv") -> list[dict[str, str]]:
    return sorted(read_registry_rows(path), key=lambda row: row.get("crosswalk_id", ""))


def load_execution_binding_rows(
    path: str | Path = "registries/role_execution_binding_registry.csv",
) -> list[dict[str, str]]:
    return sorted(read_registry_rows(path), key=lambda row: row.get("binding_id", ""))


def role_doc_filename(role_id: str) -> str:
    return f"{role_id}.md"


def expected_role_doc_path(role_id: str, docs_root: str | Path = ROLE_DOCS_ROOT) -> Path:
    return Path(docs_root) / role_doc_filename(role_id)


def crosswalk_by_role(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("role_id", "")].append(row)
    return {role_id: sorted(items, key=lambda row: row.get("crosswalk_id", "")) for role_id, items in grouped.items()}


def execution_bindings_by_role(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("role_id", "")].append(row)
    return {role_id: sorted(items, key=lambda row: row.get("binding_id", "")) for role_id, items in grouped.items()}


def expected_role_index_text(role_rows: list[dict[str, str]]) -> str:
    lines = [
        "# Role Governance",
        "",
        GENERATED_ROLE_DOC_NOTICE,
        "",
        "This directory is generated from controlled role registries. It is navigation only.",
        "",
        "## Roles",
        "",
        "| Role ID | Role Name | Role Class | System Layer Scope |",
        "|---|---|---|---|",
    ]
    for row in sorted(role_rows, key=lambda item: item.get("role_id", "")):
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(row.get("role_id", "")),
                    _cell(row.get("role_name", "")),
                    _cell(row.get("role_class", "")),
                    _cell(row.get("system_layer_scope", "")),
                ]
            )
            + " |"
        )
    lines.extend(["", "Canonical inputs:", "", "- `registries/role_registry.csv`"])
    lines.extend(["- `registries/role_skill_crosswalk.csv`", "- `registries/role_execution_binding_registry.csv`", ""])
    return "\n".join(lines)


def expected_role_doc_text(
    role: dict[str, str],
    crosswalk_rows: list[dict[str, str]],
    execution_binding_rows: list[dict[str, str]],
) -> str:
    role_id = role.get("role_id", "")
    lines = [
        f"# {role.get('role_name', role_id)}",
        "",
        GENERATED_ROLE_DOC_NOTICE,
        "",
        "## Role",
        "",
        f"- Role ID: `{role_id}`",
        f"- Role class: `{role.get('role_class', '')}`",
        f"- System layer scope: `{role.get('system_layer_scope', '')}`",
        f"- Primary mission: {role.get('primary_mission', '')}",
        f"- Primary outputs: `{role.get('primary_outputs', '')}`",
        f"- Allowed artifact classes: `{role.get('allowed_artifact_classes', '')}`",
        f"- Legacy AgentJob creation enabled: `{role.get('may_create_agentjobs', '')}`",
        f"- Requires Director decision: `{role.get('requires_director_decision', '')}`",
        "",
        "## Registry Skills",
        "",
        f"- Required skills: `{role.get('required_skills', '')}`",
        f"- Optional skills: `{role.get('optional_skills', '')}`",
        f"- Forbidden skills: `{role.get('forbidden_skills', '')}`",
        "",
        "## Crosswalk Bindings",
        "",
    ]
    if crosswalk_rows:
        lines.extend(
            [
                "| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |",
                "|---|---|---|---|---|",
            ]
        )
        for row in crosswalk_rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        _cell(row.get("skill_id", "")),
                        _cell(row.get("binding_type", "")),
                        _cell(row.get("required_when", "")),
                        _cell(row.get("system_layer_scope", "")),
                        _cell(row.get("evidence_path", "")),
                    ]
                )
                + " |"
            )
    else:
        lines.append("No role-skill crosswalk bindings are registered for this role.")
    lines.extend(["", "## Execution Bindings", ""])
    if execution_binding_rows:
        lines.extend(
            [
                "| Binding ID | Binding Scope | Required Validators | Expiry Policy |",
                "|---|---|---|---|",
            ]
        )
        for row in execution_binding_rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        _cell(row.get("binding_id", "")),
                        _cell(row.get("allowed_agentjob_types", "")),
                        _cell(row.get("required_validators", "")),
                        _cell(row.get("expiry_policy", "")),
                    ]
                )
                + " |"
            )
    else:
        lines.append("No role execution binding is registered for this role.")
    lines.extend(["", "Canonical inputs remain the three role registries listed in the notice.", ""])
    return "\n".join(lines)


def expected_role_docs(
    role_registry: str | Path = "registries/role_registry.csv",
    crosswalk: str | Path = "registries/role_skill_crosswalk.csv",
    execution_bindings: str | Path = "registries/role_execution_binding_registry.csv",
    docs_root: str | Path = ROLE_DOCS_ROOT,
) -> dict[Path, str]:
    roles = load_role_rows(role_registry)
    crosswalks = crosswalk_by_role(load_crosswalk_rows(crosswalk))
    bindings = execution_bindings_by_role(load_execution_binding_rows(execution_bindings))
    root = Path(docs_root)
    docs: dict[Path, str] = {root / "README.md": expected_role_index_text(roles)}
    for role in roles:
        role_id = role.get("role_id", "")
        docs[root / role_doc_filename(role_id)] = expected_role_doc_text(
            role,
            crosswalks.get(role_id, []),
            bindings.get(role_id, []),
        )
    return docs


def write_role_docs(
    role_registry: str | Path = "registries/role_registry.csv",
    crosswalk: str | Path = "registries/role_skill_crosswalk.csv",
    execution_bindings: str | Path = "registries/role_execution_binding_registry.csv",
    docs_root: str | Path = ROLE_DOCS_ROOT,
) -> list[Path]:
    docs = expected_role_docs(role_registry, crosswalk, execution_bindings, docs_root)
    for path, text in docs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return sorted(docs)


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()
