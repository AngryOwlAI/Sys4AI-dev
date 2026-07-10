"""Command-line entry point for the Phase 1 Sys4AI scaffold."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .capability_migration import validate_capability_migration
from .discovery import validate_discovery_record
from .derivative_generation import (
    check_governance_generated_docs,
    validate_generated_derivatives,
    write_governance_generated_docs,
)
from .derivatives import (
    check_config_control_wiki,
    check_validation_contracts_catalog,
    write_config_control_wiki,
    write_validation_contracts_catalog,
)
from .host_profiles import validate_host_capability_profiles
from .memory import bootstrap_registries
from .memory import hash_path as memory_hash_path
from .memory import lookup_memory, memory_status, run_memory_preflight, search_memory, update_hashes, validate_hashes
from .prd_modules import validate_prd_modules
from .walking_skeleton import (
    validate_walking_skeleton_flow,
    walking_skeleton_status,
    write_walking_skeleton_flow_report,
)
from .target_package import target_package_status, validate_target_package
from .validators import (
    ValidationResult,
    print_result,
    validate_artifact_contracts,
    validate_config_sources,
    validate_completion_receipt_registry,
    validate_completion_receipts,
    validate_control_records,
    validate_core_skill_proposals,
    validate_director_decision_registry,
    validate_director_decisions,
    validate_discovery_records,
    validate_format_profiles,
    validate_handoff_registry,
    validate_handoffs,
    validate_jsonschema_contracts,
    validate_memory_preflight_registry,
    validate_memory_preflight_receipts,
    validate_metrics_script,
    validate_program_state,
    validate_registry_graph,
    validate_registry_headers,
    validate_requirement_trace,
    validate_roles,
    validate_skill_lifecycle,
    validate_skill_manifest,
    validate_state_snapshots,
    validate_system_layers,
    validate_toml_config,
    validate_validation_contract_registry,
)


def _doctor() -> ValidationResult:
    messages: list[str] = []
    ok = True

    messages.append(f"Python: {platform.python_version()} at {sys.executable}")

    yaml_spec = importlib.util.find_spec("yaml")
    if yaml_spec is None:
        ok = False
        messages.append("PyYAML: missing. Run: python -m pip install -r requirements.txt")
    else:
        import yaml  # type: ignore

        messages.append(f"PyYAML: {getattr(yaml, '__version__', 'unknown')}")

    if importlib.util.find_spec("tomllib") is not None:
        messages.append("TOML parser: tomllib available")
    elif importlib.util.find_spec("tomli") is not None:
        messages.append("TOML parser: tomli available")
    else:
        ok = False
        messages.append("TOML parser: missing tomllib/tomli. Run: python -m pip install -r requirements.txt")

    jsonschema_spec = importlib.util.find_spec("jsonschema")
    if jsonschema_spec is None:
        ok = False
        messages.append("jsonschema: missing. Run: python -m pip install -r requirements.txt")
    else:
        try:
            jsonschema_version = version("jsonschema")
        except PackageNotFoundError:
            jsonschema_version = "unknown"
        messages.append(f"jsonschema: {jsonschema_version}")

    expected_dirs = [
        Path("configs"),
        Path("schemas"),
        Path("schemas/contracts"),
        Path("control_records"),
        Path("registries"),
        Path("skills"),
        Path("docs"),
        Path("docs/generated/configuration_control"),
        Path("docs/generated/validation_contracts"),
        Path("templates"),
    ]
    for directory in expected_dirs:
        if directory.exists():
            messages.append(f"Directory: {directory} present")
        else:
            ok = False
            messages.append(f"Directory: {directory} missing")

    return ValidationResult(ok, messages)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Sys4AI", description="Phase 1 Sys4AI scaffold commands")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check Python, dependencies, imports, and expected folders")

    validate = sub.add_parser("validate", help="Run all default Phase 1 validations")
    validate.add_argument("--skills", default="skills/core_skill_manifest.yaml")
    validate.add_argument("--metrics", default="skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py")
    validate.add_argument("--discovery-template", default="templates/system_definition/requirements-discovery-record-template.md")
    validate.add_argument("--registries", default="registries")
    validate.add_argument("--format-profiles", default="registries/format_profile_registry.csv")
    validate.add_argument("--config-sources", default="registries/config_source_registry.csv")
    validate.add_argument("--control-records", default="registries/control_record_registry.csv")
    validate.add_argument("--system-layers", default="registries/system_layer_registry.csv")
    validate.add_argument("--discovery-records", default="registries/discovery_record_registry.csv")
    validate.add_argument("--artifact-contracts", default="registries/artifact_contract_registry.csv")
    validate.add_argument("--core-skill-proposals", default="registries/core_skill_proposal_registry.csv")
    validate.add_argument("--skill-lifecycle", default="registries/skill_lifecycle_status_registry.csv")
    validate.add_argument("--validation-contracts", default="registries/validation_contract_registry.csv")
    validate.add_argument("--requirement-trace", default="registries/requirement_trace_registry.csv")
    validate.add_argument("--prd-modules", default="registries/prd_module_registry.csv")
    validate.add_argument("--contracts-root", default="schemas/contracts")
    validate.add_argument("--capability-migration-manifest", default="configs/capability_migration.toml")
    validate.add_argument("--generated-docs", default="docs/generated")

    validate_skills = sub.add_parser("validate-skills", help="Validate the core skill manifest")
    validate_skills.add_argument("path")

    validate_metrics = sub.add_parser("validate-metrics", help="Validate local Codex usage metrics script entry point")
    validate_metrics.add_argument(
        "path",
        default="skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py",
        nargs="?",
    )

    validate_discovery = sub.add_parser("validate-discovery-record", help="Validate a requirements discovery record")
    validate_discovery.add_argument("path")

    bootstrap = sub.add_parser("bootstrap-memory", help="Create missing memory registry files")
    bootstrap.add_argument("registry_dir", default="registries", nargs="?")

    memory = sub.add_parser("memory", help="Source-first memory commands")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)

    memory_status_parser = memory_sub.add_parser("status", help="Report memory catalog status")
    memory_status_parser.add_argument("--json", action="store_true")

    memory_lookup_parser = memory_sub.add_parser("lookup", help="Lookup a registered memory object by ID or path")
    memory_lookup_parser.add_argument("query")
    memory_lookup_parser.add_argument("--json", action="store_true")

    memory_search_parser = memory_sub.add_parser("search", help="Search registered memory objects")
    memory_search_parser.add_argument("query")
    memory_search_parser.add_argument("--limit", type=int, default=10)
    memory_search_parser.add_argument("--json", action="store_true")

    memory_preflight_parser = memory_sub.add_parser("preflight", help="Run memory preflight and optionally write a receipt")
    memory_preflight_parser.add_argument("--agentjob")
    memory_preflight_parser.add_argument("--handoff")
    memory_preflight_parser.add_argument("--query", action="append")
    memory_preflight_parser.add_argument("--write-receipt", action="store_true")
    memory_preflight_parser.add_argument("--json", action="store_true")

    memory_hash_parser = memory_sub.add_parser("hash-path", help="Hash a path with sha256")
    memory_hash_parser.add_argument("path")
    memory_hash_parser.add_argument("--json", action="store_true")

    memory_validate_hashes_parser = memory_sub.add_parser("validate-hashes", help="Validate populated registry hashes")
    memory_validate_hashes_parser.add_argument("--json", action="store_true")

    memory_update_hashes_parser = memory_sub.add_parser("update-hashes", help="Check or write registry source_hash values")
    update_mode = memory_update_hashes_parser.add_mutually_exclusive_group(required=True)
    update_mode.add_argument("--check", action="store_true")
    update_mode.add_argument("--write", action="store_true")
    memory_update_hashes_parser.add_argument("--json", action="store_true")

    validate_formats = sub.add_parser("validate-format-profiles", help="Validate format-profile registry rows")
    validate_formats.add_argument("path", default="registries/format_profile_registry.csv", nargs="?")

    validate_configs = sub.add_parser("validate-config-sources", help="Validate configuration-source registry rows")
    validate_configs.add_argument("path", default="registries/config_source_registry.csv", nargs="?")

    validate_controls = sub.add_parser("validate-control-records", help="Validate control-record registry rows and examples")
    validate_controls.add_argument("path", default="registries/control_record_registry.csv", nargs="?")

    validate_system_layer_rows = sub.add_parser("validate-system-layers", help="Validate system-layer registry rows")
    validate_system_layer_rows.add_argument("path", default="registries/system_layer_registry.csv", nargs="?")

    validate_discovery_rows = sub.add_parser("validate-discovery-records", help="Validate discovery-record registry rows")
    validate_discovery_rows.add_argument("path", default="registries/discovery_record_registry.csv", nargs="?")

    sub.add_parser("validate-roles", help="Validate role registries and role relationship references")

    validate_artifact_rows = sub.add_parser("validate-artifact-contracts", help="Validate artifact-contract registry rows")
    validate_artifact_rows.add_argument("path", default="registries/artifact_contract_registry.csv", nargs="?")

    validate_core_skill_rows = sub.add_parser("validate-core-skill-proposals", help="Validate core skill proposal registry rows")
    validate_core_skill_rows.add_argument("path", default="registries/core_skill_proposal_registry.csv", nargs="?")

    validate_skill_lifecycle_rows = sub.add_parser("validate-skill-lifecycle", help="Validate skill lifecycle status registry rows")
    validate_skill_lifecycle_rows.add_argument("path", default="registries/skill_lifecycle_status_registry.csv", nargs="?")

    validate_state = sub.add_parser("validate-program-state", help="Validate legacy tracked program state")
    validate_state.add_argument("path", default="control_records/program_state.yaml", nargs="?")

    validate_directors = sub.add_parser("validate-director-decisions", help="Validate Director Decision Records")
    validate_directors.add_argument("root", default="control_records/director_decisions", nargs="?")

    validate_director_reg = sub.add_parser(
        "validate-director-decision-registry",
        help="Validate Director decision registry rows",
    )
    validate_director_reg.add_argument("path", default="registries/director_decision_registry.csv", nargs="?")

    validate_handoff_reg = sub.add_parser("validate-handoff-registry", help="Validate handoff registry rows")
    validate_handoff_reg.add_argument("path", default="registries/handoff_registry.csv", nargs="?")

    validate_completion_reg = sub.add_parser(
        "validate-completion-receipt-registry",
        help="Validate completion receipt registry rows",
    )
    validate_completion_reg.add_argument("path", default="registries/completion_receipt_registry.csv", nargs="?")

    validate_memory_pref_reg = sub.add_parser(
        "validate-memory-preflight-registry",
        help="Validate memory preflight receipt registry rows",
    )
    validate_memory_pref_reg.add_argument("path", default="registries/memory_preflight_receipt_registry.csv", nargs="?")

    validate_handoff_records = sub.add_parser("validate-handoffs", help="Validate operational handoff records")
    validate_handoff_records.add_argument("root", default="control_records/handoffs", nargs="?")

    validate_completion_records = sub.add_parser(
        "validate-completion-receipts",
        help="Validate operational completion receipts",
    )
    validate_completion_records.add_argument("root", default="control_records/completions", nargs="?")

    validate_memory_pref = sub.add_parser("validate-memory-preflight", help="Validate memory preflight receipts")
    validate_memory_pref.add_argument("root", default="control_records/memory_preflights", nargs="?")

    validate_snapshots = sub.add_parser("validate-state-snapshots", help="Validate bounded state snapshot records")
    validate_snapshots.add_argument("root", default="control_records/state_snapshots", nargs="?")

    validate_contract_registry = sub.add_parser(
        "validate-validation-contract-registry",
        help="Validate validation-contract registry rows and schema files",
    )
    validate_contract_registry.add_argument("path", default="registries/validation_contract_registry.csv", nargs="?")

    validate_host_profiles = sub.add_parser(
        "validate-host-capability-profiles",
        help="Validate reference-host profiles structurally without satisfying G-07",
    )
    validate_host_profiles.add_argument("root", default="configs/host_profiles", nargs="?")
    validate_host_profiles.add_argument(
        "--schema",
        default="schemas/contracts/host_capability_profile.schema.json",
    )
    validate_host_profiles.add_argument("--json", action="store_true")

    validate_capability = sub.add_parser(
        "validate-capability-migration",
        help="Validate the G-05 retired-capability boundary inventory",
    )
    validate_capability.add_argument(
        "manifest",
        default="configs/capability_migration.toml",
        nargs="?",
    )
    validate_capability.add_argument("--repository-root")
    validate_capability.add_argument("--json", action="store_true")

    validate_toml = sub.add_parser("validate-toml-config", help="Validate registered TOML configuration sources")
    validate_toml.add_argument("path", default="registries/config_source_registry.csv", nargs="?")

    validate_contracts = sub.add_parser("validate-jsonschema-contracts", help="Validate JSON Schema contract files")
    validate_contracts.add_argument("root", default="schemas/contracts", nargs="?")

    validate_graph = sub.add_parser("validate-registry-graph", help="Validate cross-registry path and contract references")
    validate_graph.add_argument("registry_dir", default="registries", nargs="?")

    validate_trace = sub.add_parser(
        "validate-requirement-trace",
        help="Validate PRD requirement IDs and Phase 0 to Phase 1 trace coverage",
    )
    validate_trace.add_argument("path", default="registries/requirement_trace_registry.csv", nargs="?")
    validate_trace.add_argument("--phase0-prd", default="PRDs/Sys4AI_phase-0_product_system_design_prd.md")
    validate_trace.add_argument("--phase1-prd", default="PRDs/Sys4AI_phase-1_implementation_initialization_prd.md")

    validate_prd_module_rows = sub.add_parser("validate-prd-modules", help="Validate PRD module registry rows")
    validate_prd_module_rows.add_argument("path", default="registries/prd_module_registry.csv", nargs="?")

    generate_cc = sub.add_parser("generate-config-control-wiki", help="Generate Configuration and Control Wiki pages")
    generate_cc_mode = generate_cc.add_mutually_exclusive_group()
    generate_cc_mode.add_argument("--check", action="store_true", help="Check generated pages without writing")
    generate_cc_mode.add_argument("--write", action="store_true", help="Write generated pages")

    generate_vc = sub.add_parser("generate-validation-contracts-catalog", help="Generate Validation Contracts Catalog pages")
    generate_vc_mode = generate_vc.add_mutually_exclusive_group()
    generate_vc_mode.add_argument("--check", action="store_true", help="Check generated pages without writing")
    generate_vc_mode.add_argument("--write", action="store_true", help="Write generated pages")

    generate_governance = sub.add_parser("generate-governance-docs", help="Generate governance summary pages")
    generate_governance_mode = generate_governance.add_mutually_exclusive_group()
    generate_governance_mode.add_argument("--check", action="store_true", help="Check generated pages without writing")
    generate_governance_mode.add_argument("--write", action="store_true", help="Write generated pages")

    validate_generated = sub.add_parser("validate-generated-derivatives", help="Validate generated derivative stubs")
    validate_generated.add_argument("docs_root", default="docs/generated", nargs="?")
    validate_generated.add_argument("derivative_registry", default="registries/derivative_registry.csv", nargs="?")

    walking = sub.add_parser("walking-skeleton", help="Phase 2 walking-skeleton commands")
    walking_sub = walking.add_subparsers(dest="walking_command", required=True)

    walking_status = walking_sub.add_parser("status", help="Report walking-skeleton flow status")
    walking_status.add_argument("--json", action="store_true")

    walking_validate = walking_sub.add_parser("validate-flow", help="Validate the walking-skeleton flow")
    walking_validate.add_argument("--json", action="store_true")

    walking_report = walking_sub.add_parser("write-report", help="Write the generated walking-skeleton flow report")
    walking_report.add_argument("--json", action="store_true")

    target_package = sub.add_parser("target-package", help="Target package smoke commands")
    target_package_sub = target_package.add_subparsers(dest="target_package_command", required=True)

    target_package_status_parser = target_package_sub.add_parser("status", help="Report target package status")
    target_package_status_parser.add_argument("package_root", nargs="?", default="examples/target_systems/repo_steward_agent_package")
    target_package_status_parser.add_argument("--json", action="store_true")

    target_package_validate = target_package_sub.add_parser("validate", help="Validate a target package smoke surface")
    target_package_validate.add_argument("package_root", nargs="?", default="examples/target_systems/repo_steward_agent_package")
    target_package_validate.add_argument("--json", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        return print_result(_doctor())

    if args.command == "validate-skills":
        return print_result(validate_skill_manifest(args.path))

    if args.command == "validate-metrics":
        return print_result(validate_metrics_script(args.path))

    if args.command == "validate-discovery-record":
        return print_result(validate_discovery_record(args.path))

    if args.command == "bootstrap-memory":
        return print_result(bootstrap_registries(args.registry_dir))

    if args.command == "memory":
        return _handle_memory_command(args)

    if args.command == "walking-skeleton":
        return _handle_walking_skeleton_command(args)

    if args.command == "target-package":
        return _handle_target_package_command(args)

    if args.command == "validate-format-profiles":
        return print_result(validate_format_profiles(args.path))

    if args.command == "validate-config-sources":
        return print_result(validate_config_sources(args.path))

    if args.command == "validate-control-records":
        return print_result(validate_control_records(args.path))

    if args.command == "validate-system-layers":
        return print_result(validate_system_layers(args.path))

    if args.command == "validate-discovery-records":
        return print_result(validate_discovery_records(args.path))

    if args.command == "validate-roles":
        return print_result(validate_roles())

    if args.command == "validate-artifact-contracts":
        return print_result(validate_artifact_contracts(args.path))

    if args.command == "validate-core-skill-proposals":
        return print_result(validate_core_skill_proposals(args.path))

    if args.command == "validate-skill-lifecycle":
        return print_result(validate_skill_lifecycle(args.path))

    if args.command == "validate-program-state":
        return print_result(validate_program_state(args.path))

    if args.command == "validate-director-decisions":
        return print_result(validate_director_decisions(args.root))

    if args.command == "validate-director-decision-registry":
        return print_result(validate_director_decision_registry(args.path))

    if args.command == "validate-handoff-registry":
        return print_result(validate_handoff_registry(args.path))

    if args.command == "validate-completion-receipt-registry":
        return print_result(validate_completion_receipt_registry(args.path))

    if args.command == "validate-memory-preflight-registry":
        return print_result(validate_memory_preflight_registry(args.path))

    if args.command == "validate-handoffs":
        return print_result(validate_handoffs(args.root))

    if args.command == "validate-completion-receipts":
        return print_result(validate_completion_receipts(args.root))

    if args.command == "validate-memory-preflight":
        return print_result(validate_memory_preflight_receipts(args.root))

    if args.command == "validate-state-snapshots":
        return print_result(validate_state_snapshots(args.root))

    if args.command == "validate-validation-contract-registry":
        return print_result(validate_validation_contract_registry(args.path))

    if args.command == "validate-host-capability-profiles":
        return _emit_validation_result(
            validate_host_capability_profiles(args.root, args.schema),
            args.json,
        )

    if args.command == "validate-capability-migration":
        return _emit_validation_result(
            validate_capability_migration(args.manifest, args.repository_root),
            args.json,
        )

    if args.command == "validate-toml-config":
        return print_result(validate_toml_config(args.path))

    if args.command == "validate-jsonschema-contracts":
        return print_result(validate_jsonschema_contracts(args.root))

    if args.command == "validate-registry-graph":
        return print_result(validate_registry_graph(args.registry_dir))

    if args.command == "validate-requirement-trace":
        return print_result(validate_requirement_trace(args.path, args.phase0_prd, args.phase1_prd))

    if args.command == "validate-prd-modules":
        return print_result(validate_prd_modules(args.path))

    if args.command == "generate-config-control-wiki":
        return print_result(write_config_control_wiki() if args.write else check_config_control_wiki())

    if args.command == "generate-validation-contracts-catalog":
        return print_result(
            write_validation_contracts_catalog() if args.write else check_validation_contracts_catalog()
        )

    if args.command == "generate-governance-docs":
        return print_result(write_governance_generated_docs() if args.write else check_governance_generated_docs())

    if args.command == "validate-generated-derivatives":
        return print_result(validate_generated_derivatives(args.docs_root, args.derivative_registry))

    if args.command == "validate":
        result = _doctor()
        result.extend(validate_skill_manifest(args.skills))
        result.extend(validate_metrics_script(args.metrics))
        result.extend(validate_discovery_record(args.discovery_template))
        result.extend(validate_registry_headers(args.registries))
        result.extend(validate_format_profiles(args.format_profiles))
        result.extend(validate_config_sources(args.config_sources))
        result.extend(validate_control_records(args.control_records))
        result.extend(validate_system_layers(args.system_layers))
        result.extend(validate_discovery_records(args.discovery_records))
        result.extend(validate_roles())
        result.extend(validate_artifact_contracts(args.artifact_contracts))
        result.extend(validate_core_skill_proposals(args.core_skill_proposals))
        result.extend(validate_skill_lifecycle(args.skill_lifecycle))
        result.extend(validate_director_decision_registry())
        result.extend(validate_handoff_registry())
        result.extend(validate_completion_receipt_registry())
        result.extend(validate_memory_preflight_registry())
        result.extend(validate_handoffs())
        result.extend(validate_completion_receipts())
        result.extend(validate_state_snapshots())
        result.extend(validate_validation_contract_registry(args.validation_contracts))
        result.extend(validate_host_capability_profiles())
        result.extend(validate_toml_config(args.config_sources))
        result.extend(validate_jsonschema_contracts(args.contracts_root))
        result.extend(validate_registry_graph(args.registries))
        result.extend(validate_capability_migration(args.capability_migration_manifest))
        result.extend(validate_requirement_trace(args.requirement_trace))
        result.extend(validate_prd_modules(args.prd_modules))
        result.extend(check_governance_generated_docs())
        result.extend(validate_generated_derivatives(args.generated_docs, "registries/derivative_registry.csv"))
        return print_result(result)

    parser.error(f"Unknown command: {args.command}")
    return 2


def _handle_walking_skeleton_command(args: argparse.Namespace) -> int:
    if args.walking_command == "status":
        return _emit_payload(walking_skeleton_status(), args.json)
    if args.walking_command == "validate-flow":
        return _emit_payload(validate_walking_skeleton_flow(), args.json)
    if args.walking_command == "write-report":
        result = write_walking_skeleton_flow_report()
        return print_result(result)
    return 2


def _handle_target_package_command(args: argparse.Namespace) -> int:
    if args.target_package_command == "status":
        return _emit_payload(target_package_status(args.package_root), args.json)
    if args.target_package_command == "validate":
        return _emit_payload(validate_target_package(args.package_root), args.json)
    return 2


def _handle_memory_command(args: argparse.Namespace) -> int:
    if args.memory_command == "status":
        return _emit_memory_payload(memory_status(), args.json)
    if args.memory_command == "lookup":
        payload = lookup_memory(args.query)
        return _emit_memory_payload(payload, args.json)
    if args.memory_command == "search":
        payload = search_memory(args.query, limit=args.limit)
        return _emit_memory_payload(payload, args.json)
    if args.memory_command == "preflight":
        payload = run_memory_preflight(
            agentjob_id=args.agentjob,
            handoff_id=args.handoff,
            queries=args.query,
            write_receipt=args.write_receipt,
        )
        return _emit_memory_payload(payload, args.json)
    if args.memory_command == "hash-path":
        payload = memory_hash_path(args.path)
        return _emit_memory_payload(payload, args.json)
    if args.memory_command == "validate-hashes":
        payload = validate_hashes()
        return _emit_memory_payload(payload, args.json)
    if args.memory_command == "update-hashes":
        payload = update_hashes(write=args.write)
        return _emit_memory_payload(payload, args.json)
    return 2


def _emit_memory_payload(payload: dict[str, object], json_output: bool) -> int:
    return _emit_payload(payload, json_output)


def _emit_payload(payload: dict[str, object], json_output: bool) -> int:
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload.get("status", "OK"))
        for warning in payload.get("warnings", []) if isinstance(payload.get("warnings", []), list) else []:
            print(warning)
    return 0 if payload.get("ok") else 1


def _emit_validation_result(result: ValidationResult, json_output: bool) -> int:
    if json_output:
        print(
            json.dumps(
                {
                    "messages": result.messages,
                    "ok": result.ok,
                    "status": "PASS" if result.ok else "FAIL",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0 if result.ok else 1
    return print_result(result)


if __name__ == "__main__":
    raise SystemExit(main())
