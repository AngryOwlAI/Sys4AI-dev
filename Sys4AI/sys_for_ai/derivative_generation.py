"""Generated derivative validation for Phase 1."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

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
from .toml_io import load_toml
from .validators import ValidationResult
from .yaml_io import load_yaml


GENERATED_NOTICE = "This page is a generated reader surface. It is not canonical."
GOVERNANCE_GENERATOR = "sys_for_ai.derivative_generation.governance_generated_docs:0.2.0"

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
    "der_strategic_intent_contracts": Path("docs/generated/governance/strategic-intent-contracts.md"),
    "der_strategic_intent_evidence_graph": Path("docs/generated/governance/strategic-intent-evidence-graph.md"),
    "der_host_capability_profile": Path("docs/generated/governance/host-capability-profile.md"),
    "der_lifecycle_and_patterns": Path("docs/generated/governance/lifecycle-and-patterns.md"),
    "der_capability_migration_status": Path("docs/generated/governance/capability-migration-status.md"),
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
    trace_rows = _read_registry_rows(base, "requirement_trace_registry.csv")

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
        base / "docs/generated/governance/strategic-intent-contracts.md": _strategic_intent_contracts_page(
            base, artifact_rows, source_rows
        ),
        base / "docs/generated/governance/strategic-intent-evidence-graph.md": _strategic_intent_evidence_graph_page(
            base, source_rows, trace_rows
        ),
        base / "docs/generated/governance/host-capability-profile.md": _host_capability_profile_page(
            base, source_rows
        ),
        base / "docs/generated/governance/lifecycle-and-patterns.md": _lifecycle_and_patterns_page(
            base, source_rows
        ),
        base / "docs/generated/governance/capability-migration-status.md": _capability_migration_status_page(
            base, source_rows
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
                        row.get("may_create_execution_transactions", ""),
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
                        bindings_by_role.get(row.get("role_id", ""), {}).get("allowed_transaction_types", "pending"),
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


def _strategic_intent_contracts_page(
    root: Path,
    artifact_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> str:
    contract_ids = {
        "artifact_target_vision",
        "artifact_target_core_values",
        "artifact_execution_transaction",
        "artifact_target_system_package_manifest",
        "artifact_self_change_safety_evaluation_packet",
    }
    rows = [row for row in artifact_rows if row.get("artifact_contract_id") in contract_ids]
    g08_status = _framework_g08_status(root)
    body = "\n\n".join(
        [
            "This generated page exposes the registered strategic-intent contract chain. Contract conformance does not approve target intent, authorize execution, verify a host, or establish production fitness.",
            "## Registry Trace",
            registry_trace_table(root, ["der_strategic_intent_contracts"]),
            "## Strategic Contract Rows",
            markdown_table(
                [
                    "artifact_contract_id",
                    "artifact_type",
                    "producer_role_ids",
                    "consumer_role_ids",
                    "authority_default",
                    "validation_contract_id",
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
                        row.get("promotion_rule", ""),
                    ]
                    for row in rows
                ],
            ),
            "## Approval And Permission Boundary",
            f"Framework G-08 status is `{g08_status}`. G-08 approves only the exact framework vision and values recorded by the registered human decision. Target-system intent, execution permission, G-07 host verification, production readiness, operational authority, stakeholder consensus, and domain truth require their own evidence.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Strategic Intent Contracts",
        derivative_id="der_strategic_intent_contracts",
        derivative_type="strategic_intent_contract_index",
        source_registries=[
            "registries/artifact_contract_registry.csv",
            "registries/derivative_registry.csv",
            "../PRDs/Sys4AI_phase-0_product_system_design_prd.md",
            "control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G08-001.yaml",
        ],
        validation_contracts=sorted(
            {row.get("validation_contract_id", "") for row in rows if row.get("validation_contract_id")}
        ),
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(source_rows + rows),
        body=body,
    )


def _strategic_intent_evidence_graph_page(
    root: Path,
    source_rows: list[dict[str, str]],
    trace_rows: list[dict[str, str]],
) -> str:
    capability_counts = Counter(row.get("capability_status", "pending") for row in trace_rows)
    verification_counts = Counter(row.get("verification_status", "pending") for row in trace_rows)
    evidence_counts = Counter(row.get("evidence_status", "pending") for row in trace_rows)
    g08_status = _framework_g08_status(root)
    approved = g08_status == "accepted_G_08"
    graph_rows = [
        ["stakeholder evidence", "approved_bounded" if approved else g08_status, "SRC-DDR-STRATEGIC-BASELINE-G08-001", "Exact framework G-08 decision only"],
        ["vision", "approved" if approved else "candidate", "SRC-PRD-P0", "SFA-VISION-001 version 1.0"],
        ["values", "approved" if approved else "candidate", "SRC-PRD-P0", "SFA-VALUE-001 through SFA-VALUE-008"],
        ["requirements", "current_mixed_capability", "SRC-REG-REQ-TRACE", _format_counts(capability_counts)],
        ["architecture", "current_design_basis", "SRC-PRD-P0", "Pattern and maturity remain independent"],
        ["permissions", "bounded", "SRC-SCHEMA-EXECUTION-TRANSACTION", "Values do not grant permission"],
        ["tests", "current_local_evidence", "SRC-TEST-SAFETY-EVALUATION", _format_counts(verification_counts)],
        ["evaluations", "current_with_gaps", "SRC-SAFETY-EVALUATION-PACKET-TX17", _format_counts(evidence_counts)],
        ["operations", "planned_not_operational", "SRC-SAFETY-EVALUATION-PACKET-TX17", "No operational authority"],
        ["maintenance", "planned", "SRC-PRD-P0", "Requires current operational evidence"],
        ["improvement proposals", "governed_not_self_authorizing", "SRC-SAFETY-EVALUATION-PACKET-TX17", "Independent review and rollback required"],
    ]
    body = "\n\n".join(
        [
            "This graph is a generated navigation view over registered evidence. Status labels summarize source state and never replace the named authority.",
            "## Registry Trace",
            registry_trace_table(root, ["der_strategic_intent_evidence_graph"]),
            "## Evidence Nodes",
            markdown_table(["node", "state", "source_id", "boundary"], graph_rows),
            "## Directed Evidence Flow",
            "`stakeholder evidence -> vision and values -> requirements -> architecture and permissions -> tests and evaluations -> operations, maintenance, and improvement`",
            "## State Distinctions",
            "Approved strategic content remains distinct from current source authority, capability, verification, evidence freshness, host verification, operational maturity, and target-specific acceptance. Missing or planned evidence is not converted to current evidence by this graph.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Strategic Intent Evidence Graph",
        derivative_id="der_strategic_intent_evidence_graph",
        derivative_type="strategic_intent_evidence_graph",
        source_registries=[
            "registries/source_registry.csv",
            "registries/object_relationship_registry.csv",
            "registries/requirement_trace_registry.csv",
            "registries/derivative_registry.csv",
        ],
        validation_contracts=["contract_requirement_trace_registry_row"],
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(source_rows + trace_rows),
        body=body,
    )


def _host_capability_profile_page(root: Path, source_rows: list[dict[str, str]]) -> str:
    profile_path = root / "configs/host_profiles/codex_app_reference.toml"
    profile = load_toml(profile_path)
    metadata = profile.get("profile", {})
    interfaces = profile.get("interfaces", [])
    body = "\n\n".join(
        [
            "This page summarizes the controlled reference-host profile. Structural validation does not satisfy G-07 or prove observable host behavior.",
            "## Registry Trace",
            registry_trace_table(root, ["der_host_capability_profile"]),
            "## Profile Status",
            markdown_table(
                ["profile_id", "version", "verification_state", "gate", "scope", "executable"],
                [[
                    metadata.get("profile_id", ""),
                    metadata.get("profile_version", ""),
                    metadata.get("verification_state", ""),
                    metadata.get("verification_gate", ""),
                    metadata.get("verification_scope", ""),
                    str(metadata.get("portable_execution_contract_executable", False)).lower(),
                ]],
            ),
            "## Interface States",
            markdown_table(
                ["interface_id", "capability_status", "execution_allowed", "fallback_mode", "evidence_status"],
                [[
                    item.get("interface_id", ""),
                    item.get("capability_status", ""),
                    str(item.get("execution_allowed", False)).lower(),
                    item.get("fallback_mode", ""),
                    item.get("evidence_status", ""),
                ] for item in interfaces],
            ),
            "## Boundary",
            "G-07 remains open. This reader grants no host, tool, filesystem, network, sub-agent, thread-state, cancellation, permission, production, or operational authority.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Host Capability Profile",
        derivative_id="der_host_capability_profile",
        derivative_type="host_capability_profile_summary",
        source_registries=[
            "registries/config_source_registry.csv",
            "configs/host_profiles/codex_app_reference.toml",
            "registries/derivative_registry.csv",
        ],
        validation_contracts=["contract_host_capability_profile"],
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(source_rows),
        body=body,
    )


def _lifecycle_and_patterns_page(root: Path, source_rows: list[dict[str, str]]) -> str:
    prd = (root.parent / "PRDs/Sys4AI_phase-0_product_system_design_prd.md").read_text(encoding="utf-8")
    stages = _backtick_values(_requirement_text(prd, "SFA-CORE-LIFE-001"))
    patterns = _backtick_values(_requirement_text(prd, "SFA-CORE-PATTERN-002"))
    maturity = _table_first_column(prd, "| `concept` |", "Pattern and maturity must be stored")
    body = "\n\n".join(
        [
            "This page summarizes the canonical lifecycle and the independent coordination-pattern and operational-maturity taxonomies.",
            "## Registry Trace",
            registry_trace_table(root, ["der_lifecycle_and_patterns"]),
            "## Lifecycle Stages",
            markdown_table(["order", "stage"], [[str(index), stage] for index, stage in enumerate(stages, start=1)]),
            "## Coordination Patterns",
            markdown_table(["pattern", "state"], [[pattern, "permitted taxonomy value"] for pattern in patterns]),
            "## Operational Maturity",
            markdown_table(["maturity", "state"], [[item, "independent taxonomy value"] for item in maturity]),
            "## Boundary",
            "A coordination pattern does not prove production approval or operational maturity. Lifecycle and taxonomy validation does not establish implementation, G-07, production readiness, operational authority, stakeholder consensus, or domain truth.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Lifecycle And Patterns",
        derivative_id="der_lifecycle_and_patterns",
        derivative_type="lifecycle_and_pattern_summary",
        source_registries=[
            "../PRDs/Sys4AI_phase-0_product_system_design_prd.md",
            "registries/requirement_trace_registry.csv",
            "registries/derivative_registry.csv",
        ],
        validation_contracts=["contract_requirement_trace_registry_row"],
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(source_rows),
        body=body,
    )


def _capability_migration_status_page(root: Path, source_rows: list[dict[str, str]]) -> str:
    config_path = root / "configs/capability_migration.toml"
    config = load_toml(config_path)
    classifications = config.get("classifications", [])
    state_counts = Counter(item.get("state", "pending") for item in classifications)
    body = "\n\n".join(
        [
            "This page summarizes the registered retired-runtime migration classifications. It does not restore AgentJob, `/continue`, or any removed runtime capability.",
            "## Registry Trace",
            registry_trace_table(root, ["der_capability_migration_status"]),
            "## Classification State Counts",
            markdown_table(["state", "count"], [[state, str(count)] for state, count in sorted(state_counts.items())]),
            "## Classification Rows",
            markdown_table(
                ["classification_id", "state", "authority_scope", "disposition"],
                [[
                    item.get("classification_id", ""),
                    item.get("state", ""),
                    item.get("authority_scope", ""),
                    item.get("disposition", ""),
                ] for item in classifications],
            ),
            "## Boundary",
            "Historical and compatibility references remain provenance only. Generated readers remain noncanonical; current capability requires separate implementation, verification, authority, and host evidence.",
            "## Allowed Promotion Path",
            PROMOTION_PATH,
        ]
    )
    return render_page(
        title="Capability Migration Status",
        derivative_id="der_capability_migration_status",
        derivative_type="capability_migration_status_summary",
        source_registries=[
            "configs/capability_migration.toml",
            "registries/requirement_trace_registry.csv",
            "registries/derivative_registry.csv",
        ],
        validation_contracts=["contract_capability_migration_manifest"],
        generator=GOVERNANCE_GENERATOR,
        source_hashes=source_hashes_from_rows(source_rows),
        body=body,
    )


def _requirement_text(markdown: str, requirement_id: str) -> str:
    match = re.search(rf"`{re.escape(requirement_id)}`:\s*(.+)", markdown)
    return match.group(1).strip() if match else ""


def _backtick_values(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def _table_first_column(markdown: str, start: str, end_marker: str) -> list[str]:
    start_index = markdown.find(start)
    end_index = markdown.find(end_marker, start_index)
    if start_index < 0:
        return []
    segment = markdown[start_index:end_index if end_index >= 0 else None]
    return re.findall(r"^\| `([^`]+)` \|", segment, flags=re.MULTILINE)


def _format_counts(counts: Counter[str]) -> str:
    return "; ".join(f"{key}={value}" for key, value in sorted(counts.items())) or "none"


def _framework_g08_status(root: Path) -> str:
    state = load_yaml(root / "control_records/program_state.yaml")
    summary = state.get("capability_status_summary", {})
    return str(summary.get("strategic_approval", "candidate"))


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
