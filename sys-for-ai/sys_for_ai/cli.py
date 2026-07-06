"""Command-line entry point for the Phase 1 sys-for-ai scaffold."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .discovery import validate_discovery_record
from .derivative_generation import validate_generated_derivatives
from .derivatives import (
    check_config_control_wiki,
    check_validation_contracts_catalog,
    write_config_control_wiki,
    write_validation_contracts_catalog,
)
from .memory import bootstrap_registries
from .memory import hash_path as memory_hash_path
from .memory import lookup_memory, memory_status, run_memory_preflight, search_memory, update_hashes, validate_hashes
from .control_loop import (
    continue_packet,
    continue_preflight,
    continue_select,
    continue_status,
    finalize_agentjob,
    validate_agentjob_boundaries,
    validate_check_diff,
    validate_control_loop,
    validate_one_active_agentjob,
)
from .validators import (
    ValidationResult,
    print_result,
    validate_agentjob,
    validate_agentjob_registry,
    validate_config_sources,
    validate_completion_receipt_registry,
    validate_completion_receipts,
    validate_control_records,
    validate_director_decision_registry,
    validate_director_decisions,
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
    validate_skill_manifest,
    validate_state_snapshots,
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
    parser = argparse.ArgumentParser(prog="sys-for-ai", description="Phase 1 sys-for-ai scaffold commands")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check Python, dependencies, imports, and expected folders")

    continue_status_parser = sub.add_parser("continue-status", help="Report current /continue state")
    continue_status_parser.add_argument("--json", action="store_true")

    continue_preflight_parser = sub.add_parser("continue-preflight", help="Run /continue memory preflight")
    continue_preflight_parser.add_argument("--json", action="store_true")

    continue_select_parser = sub.add_parser("continue-select", help="Select one authorized AgentJob")
    continue_select_parser.add_argument("--json", action="store_true")

    continue_packet_parser = sub.add_parser("continue-packet", help="Emit a /continue execution packet")
    continue_packet_parser.add_argument("--json", action="store_true")

    continue_finalize_parser = sub.add_parser("continue-finalize", help="Finalize an AgentJob from a completion receipt")
    continue_finalize_parser.add_argument("--completion", required=True)
    continue_finalize_parser.add_argument("--json", action="store_true")

    validate = sub.add_parser("validate", help="Run all default Phase 1 validations")
    validate.add_argument("--agentjob", default="control_records/examples/phase1_smoke_agentjob.yaml")
    validate.add_argument("--skills", default="skills/core_skill_manifest.yaml")
    validate.add_argument("--metrics", default="skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py")
    validate.add_argument("--discovery-template", default="templates/system_definition/requirements-discovery-record-template.md")
    validate.add_argument("--registries", default="registries")
    validate.add_argument("--format-profiles", default="registries/format_profile_registry.csv")
    validate.add_argument("--config-sources", default="registries/config_source_registry.csv")
    validate.add_argument("--control-records", default="registries/control_record_registry.csv")
    validate.add_argument("--validation-contracts", default="registries/validation_contract_registry.csv")
    validate.add_argument("--requirement-trace", default="registries/requirement_trace_registry.csv")
    validate.add_argument("--contracts-root", default="schemas/contracts")
    validate.add_argument("--generated-docs", default="docs/generated")

    validate_agent = sub.add_parser("validate-agentjob", help="Validate one AgentJob YAML file")
    validate_agent.add_argument("path")

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

    validate_state = sub.add_parser("validate-program-state", help="Validate tracked /continue program state")
    validate_state.add_argument("path", default="control_records/program_state.yaml", nargs="?")

    validate_directors = sub.add_parser("validate-director-decisions", help="Validate Director Decision Records")
    validate_directors.add_argument("root", default="control_records/director_decisions", nargs="?")

    validate_agentjob_reg = sub.add_parser("validate-agentjob-registry", help="Validate AgentJob registry rows")
    validate_agentjob_reg.add_argument("path", default="registries/agentjob_registry.csv", nargs="?")

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

    validate_boundaries = sub.add_parser("validate-agentjob-boundaries", help="Validate changed paths against an AgentJob boundary")
    validate_boundaries.add_argument("--agentjob", required=True)
    validate_boundaries.add_argument("--git", action="store_true")
    validate_boundaries.add_argument("--json", action="store_true")

    validate_diff = sub.add_parser("validate-check-diff", help="Validate the current Git diff against an AgentJob boundary")
    validate_diff.add_argument("--agentjob", required=True)
    validate_diff.add_argument("--json", action="store_true")

    sub.add_parser("validate-one-active-agentjob", help="Validate the one-active-AgentJob invariant")
    sub.add_parser("validate-control-loop", help="Validate the /continue control-loop kernel")

    validate_contract_registry = sub.add_parser(
        "validate-validation-contract-registry",
        help="Validate validation-contract registry rows and schema files",
    )
    validate_contract_registry.add_argument("path", default="registries/validation_contract_registry.csv", nargs="?")

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
    validate_trace.add_argument("--phase0-prd", default="PRDs/sys-for-ai_phase-0_product_system_design_prd.md")
    validate_trace.add_argument("--phase1-prd", default="PRDs/sys-for-ai_phase-1_implementation_initialization_prd.md")

    generate_cc = sub.add_parser("generate-config-control-wiki", help="Generate Configuration and Control Wiki pages")
    generate_cc_mode = generate_cc.add_mutually_exclusive_group()
    generate_cc_mode.add_argument("--check", action="store_true", help="Check generated pages without writing")
    generate_cc_mode.add_argument("--write", action="store_true", help="Write generated pages")

    generate_vc = sub.add_parser("generate-validation-contracts-catalog", help="Generate Validation Contracts Catalog pages")
    generate_vc_mode = generate_vc.add_mutually_exclusive_group()
    generate_vc_mode.add_argument("--check", action="store_true", help="Check generated pages without writing")
    generate_vc_mode.add_argument("--write", action="store_true", help="Write generated pages")

    validate_generated = sub.add_parser("validate-generated-derivatives", help="Validate generated derivative stubs")
    validate_generated.add_argument("docs_root", default="docs/generated", nargs="?")
    validate_generated.add_argument("derivative_registry", default="registries/derivative_registry.csv", nargs="?")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        return print_result(_doctor())

    if args.command == "continue-status":
        return _emit_payload(continue_status(), args.json)

    if args.command == "continue-preflight":
        return _emit_payload(continue_preflight(), args.json)

    if args.command == "continue-select":
        return _emit_payload(continue_select(), args.json)

    if args.command == "continue-packet":
        return _emit_payload(continue_packet(), args.json)

    if args.command == "continue-finalize":
        return _emit_payload(finalize_agentjob(args.completion), args.json)

    if args.command == "validate-agentjob":
        return print_result(validate_agentjob(args.path))

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

    if args.command == "validate-format-profiles":
        return print_result(validate_format_profiles(args.path))

    if args.command == "validate-config-sources":
        return print_result(validate_config_sources(args.path))

    if args.command == "validate-control-records":
        return print_result(validate_control_records(args.path))

    if args.command == "validate-program-state":
        return print_result(validate_program_state(args.path))

    if args.command == "validate-director-decisions":
        return print_result(validate_director_decisions(args.root))

    if args.command == "validate-agentjob-registry":
        return print_result(validate_agentjob_registry(args.path))

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

    if args.command == "validate-agentjob-boundaries":
        return _emit_payload(validate_agentjob_boundaries(args.agentjob, use_git=args.git), args.json)

    if args.command == "validate-check-diff":
        return _emit_payload(validate_check_diff(args.agentjob), args.json)

    if args.command == "validate-one-active-agentjob":
        return print_result(validate_one_active_agentjob())

    if args.command == "validate-control-loop":
        return print_result(validate_control_loop())

    if args.command == "validate-validation-contract-registry":
        return print_result(validate_validation_contract_registry(args.path))

    if args.command == "validate-toml-config":
        return print_result(validate_toml_config(args.path))

    if args.command == "validate-jsonschema-contracts":
        return print_result(validate_jsonschema_contracts(args.root))

    if args.command == "validate-registry-graph":
        return print_result(validate_registry_graph(args.registry_dir))

    if args.command == "validate-requirement-trace":
        return print_result(validate_requirement_trace(args.path, args.phase0_prd, args.phase1_prd))

    if args.command == "generate-config-control-wiki":
        return print_result(write_config_control_wiki() if args.write else check_config_control_wiki())

    if args.command == "generate-validation-contracts-catalog":
        return print_result(
            write_validation_contracts_catalog() if args.write else check_validation_contracts_catalog()
        )

    if args.command == "validate-generated-derivatives":
        return print_result(validate_generated_derivatives(args.docs_root, args.derivative_registry))

    if args.command == "validate":
        result = _doctor()
        result.extend(validate_agentjob(args.agentjob))
        result.extend(validate_skill_manifest(args.skills))
        result.extend(validate_metrics_script(args.metrics))
        result.extend(validate_discovery_record(args.discovery_template))
        result.extend(validate_registry_headers(args.registries))
        result.extend(validate_format_profiles(args.format_profiles))
        result.extend(validate_config_sources(args.config_sources))
        result.extend(validate_control_records(args.control_records))
        result.extend(validate_program_state())
        result.extend(validate_agentjob_registry())
        result.extend(validate_director_decision_registry())
        result.extend(validate_handoff_registry())
        result.extend(validate_completion_receipt_registry())
        result.extend(validate_memory_preflight_registry())
        result.extend(validate_handoffs())
        result.extend(validate_completion_receipts())
        result.extend(validate_state_snapshots())
        result.extend(validate_memory_preflight_receipts())
        result.extend(validate_validation_contract_registry(args.validation_contracts))
        result.extend(validate_toml_config(args.config_sources))
        result.extend(validate_jsonschema_contracts(args.contracts_root))
        result.extend(validate_registry_graph(args.registries))
        boundary_payload = validate_check_diff("AJ-P1-SELFHOST-ACCEPTANCE-001")
        result.extend(
            ValidationResult(
                bool(boundary_payload.get("ok")),
                _boundary_messages(boundary_payload),
            )
        )
        result.extend(validate_one_active_agentjob())
        result.extend(validate_control_loop())
        result.extend(validate_requirement_trace(args.requirement_trace))
        result.extend(validate_generated_derivatives(args.generated_docs, "registries/derivative_registry.csv"))
        return print_result(result)

    parser.error(f"Unknown command: {args.command}")
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


def _boundary_messages(payload: dict[str, object]) -> list[str]:
    agentjob_id = payload.get("agentjob_id", "")
    messages = [f"{agentjob_id}: AgentJob boundary validation passed"] if payload.get("ok") else []
    for item in payload.get("violations", []) if isinstance(payload.get("violations", []), list) else []:
        if isinstance(item, dict):
            messages.append(f"{agentjob_id}: {item.get('path')}: {item.get('reason')}")
    for item in payload.get("warnings", []) if isinstance(payload.get("warnings", []), list) else []:
        if isinstance(item, dict):
            messages.append(f"{agentjob_id}: warning {item.get('path')}: {item.get('reason')}")
    return messages or [f"{agentjob_id}: AgentJob boundary validation failed"]


if __name__ == "__main__":
    raise SystemExit(main())
