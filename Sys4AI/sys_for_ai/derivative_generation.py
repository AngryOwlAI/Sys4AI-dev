"""Generated derivative validation for Phase 1."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from .derivatives import check_config_control_wiki, check_validation_contracts_catalog
from .derivatives.templates import (
    PROMOTION_PATH,
    STRUCTURAL_WARNING,
    check_or_write_pages,
    markdown_table,
    product_root,
    registry_trace_table,
    render_page,
    source_hashes_from_rows,
)
from .registry_io import read_registry, read_registry_rows, resolve_registered_path, rows_by_id
from .validators import ValidationResult


GENERATED_NOTICE = "This page is a generated reader surface. It is not canonical."
GOVERNANCE_GENERATOR = "sys_for_ai.derivative_generation.governance_generated_docs:0.1.0"

EXPECTED_DERIVATIVES = {
    "der_configuration_control_index": Path("docs/generated/configuration_control/index.md"),
    "der_configuration_control_yaml": Path("docs/generated/configuration_control/yaml-control-records.md"),
    "der_configuration_control_toml": Path("docs/generated/configuration_control/toml-configuration-sources.md"),
    "der_validation_contracts_index": Path("docs/generated/validation_contracts/index.md"),
    "der_validation_contracts_by_target": Path("docs/generated/validation_contracts/contracts-by-target.md"),
    "der_registry_catalog_index": Path("docs/generated/registry_catalog/index.md"),
    "der_system_layers_index": Path("docs/generated/system_layers/index.md"),
    "der_artifact_contracts_index": Path("docs/generated/artifact_contracts/index.md"),
    "der_core_skills_index": Path("docs/generated/core_skills/index.md"),
    "der_role_governance_summary": Path("docs/generated/roles/role-governance-summary.md"),
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
    result.extend(check_governance_generated_docs(base))
    return result


def expected_governance_generated_docs(root: str | Path = ".") -> dict[Path, str]:
    """Return deterministic governance generated documentation pages."""

    base = product_root(root)
    source_rows = _read_registry_rows(base, "source_registry.csv")
    derivative_rows = _read_registry_rows(base, "derivative_registry.csv")
    system_layer_rows = _read_registry_rows(base, "system_layer_registry.csv")
    artifact_rows = _read_registry_rows(base, "artifact_contract_registry.csv")
    role_rows = _read_registry_rows(base, "role_registry.csv")
    crosswalk_rows = _read_registry_rows(base, "role_skill_crosswalk.csv")
    binding_rows = _read_registry_rows(base, "role_execution_binding_registry.csv")
    skill_rows = _read_registry_rows(base, "skill_registry.csv")
    proposal_rows = _read_registry_rows(base, "core_skill_proposal_registry.csv")
    lifecycle_rows = _read_registry_rows(base, "skill_lifecycle_status_registry.csv")

    return {
        base / "docs/generated/registry_catalog/index.md": _registry_catalog_page(
            base,
            source_rows,
            derivative_rows,
        ),
        base / "docs/generated/system_layers/index.md": _system_layers_page(base, system_layer_rows),
        base / "docs/generated/artifact_contracts/index.md": _artifact_contracts_page(base, artifact_rows),
        base / "docs/generated/core_skills/index.md": _core_skills_page(
            base,
            skill_rows,
            proposal_rows,
            lifecycle_rows,
        ),
        base / "docs/generated/roles/role-governance-summary.md": _role_governance_summary_page(
            base,
            role_rows,
            crosswalk_rows,
            binding_rows,
        ),
    }


def check_governance_generated_docs(root: str | Path = ".") -> ValidationResult:
    """Check generated governance documentation pages."""

    return check_or_write_pages(
        expected_governance_generated_docs(root),
        write=False,
        label="generate-governance-docs",
    )


def write_governance_generated_docs(root: str | Path = ".") -> ValidationResult:
    """Write generated governance documentation pages."""

    return check_or_write_pages(
        expected_governance_generated_docs(root),
        write=True,
        label="generate-governance-docs",
    )


def _registry_catalog_page(
    root: Path,
    source_rows: list[dict[str, str]],
    derivative_rows: list[dict[str, str]],
) -> str:
    registry_rows = _registry_catalog_rows(root, source_rows)
    body = "\n\n".join(
        [
            "This generated page indexes registered CSV registries. It is a navigation surface, not a registry authority.",
            "## Registry Trace",
            registry_trace_table(root, ["der_registry_catalog_index"]),
            "## Registered Registries",
            markdown_table(
                ["registry_file", "registered_source_id", "source_type", "authority_status", "row_count", "owner"],
                registry_rows,
            ),
            "## Generation Boundary",
            "The catalog is derived from CSV file presence plus source-registry rows. Missing or stale source rows must be corrected in the source registries, not here.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Registry Catalog",
        derivative_id="der_registry_catalog_index",
        derivative_type="governance_registry_catalog_page",
        source_registries=_all_registry_paths(root),
        validation_contracts=["contract_registry_header"],
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(source_rows + derivative_rows),
        body=body,
    )


def _system_layers_page(root: Path, rows: list[dict[str, str]]) -> str:
    body = "\n\n".join(
        [
            "This generated page summarizes registered system layers and their authority boundaries.",
            "## Registry Trace",
            registry_trace_table(root, ["der_system_layers_index"]),
            "## Layer Rows",
            markdown_table(
                [
                    "layer_id",
                    "layer_type",
                    "canonical_roots",
                    "derivative_roots",
                    "requires_decision",
                    "default_validators",
                    "owner",
                ],
                [
                    [
                        row.get("layer_id", ""),
                        row.get("layer_type", ""),
                        row.get("canonical_roots", ""),
                        row.get("derivative_roots", ""),
                        row.get("requires_director_decision_for_mutation", ""),
                        row.get("default_validators", ""),
                        row.get("owner", ""),
                    ]
                    for row in rows
                ],
            ),
            "## Boundary Note",
            "Generated derivative surfaces remain noncanonical unless explicitly promoted by a source-authority decision.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="System Layers",
        derivative_id="der_system_layers_index",
        derivative_type="governance_system_layers_page",
        source_registries=["registries/system_layer_registry.csv", "registries/derivative_registry.csv"],
        validation_contracts=["contract_system_layer_registry_row"],
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(rows),
        body=body,
    )


def _artifact_contracts_page(root: Path, rows: list[dict[str, str]]) -> str:
    contract_ids = sorted(
        {
            "contract_artifact_contract_registry_row",
            *[row.get("validation_contract_id", "") for row in rows if row.get("validation_contract_id")],
        }
    )
    body = "\n\n".join(
        [
            "This generated page summarizes artifact contracts, producers, consumers, derivative surfaces, and promotion rules.",
            "## Registry Trace",
            registry_trace_table(root, ["der_artifact_contracts_index"]),
            "## Structural Versus Semantic Warning",
            STRUCTURAL_WARNING,
            "## Artifact Contract Rows",
            markdown_table(
                [
                    "artifact_contract_id",
                    "artifact_type",
                    "producer_role_ids",
                    "consumer_role_ids",
                    "authority_default",
                    "validation_contract_id",
                    "derivative_surfaces",
                    "promotion_rule",
                ],
                [
                    [
                        row.get("artifact_contract_id", ""),
                        row.get("artifact_type", ""),
                        row.get("producer_role_ids", ""),
                        row.get("consumer_role_ids", ""),
                        row.get("authority_default", ""),
                        row.get("validation_contract_id", ""),
                        row.get("derivative_surfaces", ""),
                        row.get("promotion_rule", ""),
                    ]
                    for row in rows
                ],
            ),
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Artifact Contracts",
        derivative_id="der_artifact_contracts_index",
        derivative_type="governance_artifact_contracts_page",
        source_registries=["registries/artifact_contract_registry.csv", "registries/derivative_registry.csv"],
        validation_contracts=contract_ids or ["contract_artifact_contract_registry_row"],
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(rows),
        body=body,
    )


def _core_skills_page(
    root: Path,
    skill_rows: list[dict[str, str]],
    proposal_rows: list[dict[str, str]],
    lifecycle_rows: list[dict[str, str]],
) -> str:
    body = "\n\n".join(
        [
            "This generated page summarizes product scaffold skills and proposed core organizational skills.",
            "## Registry Trace",
            registry_trace_table(root, ["der_core_skills_index"]),
            "## Product Skill Registry Rows",
            markdown_table(
                ["skill_id", "family", "adaptation_status", "lifecycle_status", "local_path"],
                [
                    [
                        row.get("skill_id", ""),
                        row.get("family", ""),
                        row.get("adaptation_status", ""),
                        row.get("lifecycle_status", ""),
                        row.get("local_path", ""),
                    ]
                    for row in skill_rows
                ],
            ),
            "## Core Skill Proposal Rows",
            markdown_table(
                [
                    "proposal_id",
                    "skill_id",
                    "priority",
                    "status",
                    "required_by_roles",
                    "target_runtime_path",
                    "validator_plan",
                ],
                [
                    [
                        row.get("proposal_id", ""),
                        row.get("skill_id", ""),
                        row.get("priority", ""),
                        row.get("status", ""),
                        row.get("required_by_roles", ""),
                        row.get("target_runtime_path", ""),
                        row.get("validator_plan", ""),
                    ]
                    for row in proposal_rows
                ],
            ),
            "## Lifecycle Vocabulary Rows",
            markdown_table(
                [
                    "status_id",
                    "status_name",
                    "may_execute_runtime",
                    "may_be_used_as_authority",
                    "requires_manifest",
                    "allowed_roots",
                ],
                [
                    [
                        row.get("status_id", ""),
                        row.get("status_name", ""),
                        row.get("may_execute_runtime", ""),
                        row.get("may_be_used_as_authority", ""),
                        row.get("requires_manifest", ""),
                        row.get("allowed_roots", ""),
                    ]
                    for row in lifecycle_rows
                ],
            ),
            "## Authority Boundary",
            "Product scaffold skills are reference surfaces. Active runtime authority remains with registered runtime skill surfaces unless separately promoted.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Core Skills",
        derivative_id="der_core_skills_index",
        derivative_type="governance_core_skills_page",
        source_registries=[
            "registries/skill_registry.csv",
            "registries/core_skill_proposal_registry.csv",
            "registries/skill_lifecycle_status_registry.csv",
            "registries/derivative_registry.csv",
        ],
        validation_contracts=[
            "contract_core_skill_proposal_registry_row",
            "contract_skill_lifecycle_status_registry_row",
        ],
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(skill_rows + proposal_rows + lifecycle_rows),
        body=body,
    )


def _role_governance_summary_page(
    root: Path,
    role_rows: list[dict[str, str]],
    crosswalk_rows: list[dict[str, str]],
    binding_rows: list[dict[str, str]],
) -> str:
    crosswalk_counts = _crosswalk_counts(crosswalk_rows)
    bindings_by_role = {row.get("role_id", ""): row for row in binding_rows}
    body = "\n\n".join(
        [
            "This generated page summarizes role governance registries and execution binding coverage.",
            "## Registry Trace",
            registry_trace_table(root, ["der_role_governance_summary"]),
            "## Role Rows",
            markdown_table(
                [
                    "role_id",
                    "role_class",
                    "required_skills",
                    "optional_skills",
                    "legacy_agentjob_creation_enabled",
                    "requires_director_decision",
                ],
                [
                    [
                        row.get("role_id", ""),
                        row.get("role_class", ""),
                        row.get("required_skills", ""),
                        row.get("optional_skills", ""),
                        row.get("may_create_agentjobs", ""),
                        row.get("requires_director_decision", ""),
                    ]
                    for row in role_rows
                ],
            ),
            "## Crosswalk Coverage Counts",
            markdown_table(
                ["role_id", "required", "optional", "forbidden", "conditional", "recommended"],
                [
                    [
                        row.get("role_id", ""),
                        str(crosswalk_counts[(row.get("role_id", ""), "required")]),
                        str(crosswalk_counts[(row.get("role_id", ""), "optional")]),
                        str(crosswalk_counts[(row.get("role_id", ""), "forbidden")]),
                        str(crosswalk_counts[(row.get("role_id", ""), "conditional")]),
                        str(crosswalk_counts[(row.get("role_id", ""), "recommended")]),
                    ]
                    for row in role_rows
                ],
            ),
            "## Execution Binding Rows",
            markdown_table(
                ["role_id", "binding_id", "binding_scope", "required_validators", "completion_evidence"],
                [
                    [
                        row.get("role_id", ""),
                        bindings_by_role.get(row.get("role_id", ""), {}).get("binding_id", "pending"),
                        bindings_by_role.get(row.get("role_id", ""), {}).get("allowed_agentjob_types", "pending"),
                        bindings_by_role.get(row.get("role_id", ""), {}).get("required_validators", "pending"),
                        bindings_by_role.get(row.get("role_id", ""), {}).get("completion_evidence", "pending"),
                    ]
                    for row in role_rows
                ],
            ),
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Role Governance Summary",
        derivative_id="der_role_governance_summary",
        derivative_type="governance_role_summary_page",
        source_registries=[
            "registries/role_registry.csv",
            "registries/role_skill_crosswalk.csv",
            "registries/role_execution_binding_registry.csv",
            "registries/derivative_registry.csv",
        ],
        validation_contracts=[
            "contract_role_registry_row",
            "contract_role_skill_crosswalk_row",
            "contract_role_execution_binding_registry_row",
        ],
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(role_rows + crosswalk_rows + binding_rows),
        body=body,
    )


def _registry_catalog_rows(root: Path, source_rows: list[dict[str, str]]) -> list[list[str]]:
    source_by_path = _source_rows_by_relative_path(source_rows)
    rows: list[list[str]] = []
    for path in sorted((root / "registries").glob("*.csv")):
        rel_path = f"registries/{path.name}"
        _header, registry_rows = read_registry(path)
        source_row = source_by_path.get(rel_path, {})
        rows.append(
            [
                rel_path,
                source_row.get("source_id", "pending"),
                source_row.get("source_type", "pending"),
                source_row.get("authority_status", "pending"),
                str(len(registry_rows)),
                source_row.get("owner", "pending"),
            ]
        )
    return rows


def _all_registry_paths(root: Path) -> list[str]:
    return [f"registries/{path.name}" for path in sorted((root / "registries").glob("*.csv"))]


def _source_rows_by_relative_path(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        path = row.get("path", "")
        if not path:
            continue
        indexed[path] = row
        if path.startswith("Sys4AI/"):
            indexed[path.removeprefix("Sys4AI/")] = row
    return indexed


def _crosswalk_counts(rows: list[dict[str, str]]) -> Counter[tuple[str, str]]:
    counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        role_id = row.get("role_id", "")
        binding_type = row.get("binding_type", "")
        if role_id and binding_type:
            counts[(role_id, binding_type)] += 1
    return counts


def _read_registry_rows(root: Path, registry_name: str) -> list[dict[str, str]]:
    path = root / "registries" / registry_name
    if not path.exists():
        return []
    return read_registry_rows(path)
