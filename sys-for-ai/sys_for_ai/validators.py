"""Small deterministic validators for Phase 1 scaffolding."""

from __future__ import annotations

from collections import Counter
from fnmatch import fnmatchcase
import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .registry_io import read_registry, read_registry_rows, resolve_registered_path, rows_by_id
from .security_checks import find_secret_like_values
from .yaml_io import load_yaml


@dataclass
class ValidationResult:
    ok: bool
    messages: list[str]

    def extend(self, other: "ValidationResult") -> None:
        self.ok = self.ok and other.ok
        self.messages.extend(other.messages)


@dataclass(frozen=True)
class RequirementDeclaration:
    requirement_id: str
    path: Path
    line_number: int


REQUIREMENT_ID_PATTERN = r"SFA-[A-Z0-9]+(?:-[A-Z0-9]+)*"
BACKTICK_REQUIREMENT_RE = re.compile(rf"^\s*`(?P<id>{REQUIREMENT_ID_PATTERN})`\s*:")
TABLE_REQUIREMENT_RE = re.compile(rf"^\|\s*(?P<id>{REQUIREMENT_ID_PATTERN})\s*\|")
PHASE0_REQUIREMENT_PREFIXES = ("SFA-CORE-", "SFA-P0-FR-", "SFA-P0-NFR-")
PHASE1_REQUIREMENT_PREFIX = "SFA-P1-INIT-"
TRACE_COVERAGE_STATUSES = {"covered", "partial", "deferred", "not_applicable"}
TRACE_CLASSES = {"implemented", "scaffolded", "deferred", "out_of_phase"}
TRACE_CLASSES_BY_COVERAGE = {
    "covered": {"implemented"},
    "partial": {"scaffolded", "deferred", "out_of_phase"},
    "deferred": {"deferred"},
    "not_applicable": {"out_of_phase"},
}
SEMANTIC_REVIEW_VERDICTS = {"sufficient", "needs_evidence", "incorrect_mapping"}
SYSTEM_LAYER_IDS = {
    "development_system",
    "framework_product",
    "target_system_template",
    "target_system_instance",
    "derivative_surface",
}
SKILL_LIFECYCLE_STATUS_NAMES = {
    "proposed",
    "imported_unadapted",
    "adapter_shell",
    "adapted_runtime_active",
    "product_scaffold_reference",
    "deprecated",
    "superseded",
    "blocked",
}

AGENTJOB_REQUIRED_FIELDS = {
    "agentjob_id",
    "objective",
    "role",
    "allowed_reads",
    "allowed_writes",
    "forbidden_actions",
    "expected_outputs",
    "validators",
    "stop_conditions",
}

SKILL_MANIFEST_REQUIRED_SKILLS = {
    "codex-usage-metrics",
    "continue",
    "system-definition-interview",
    "system-definition-interview-context-45",
    "source-first-memory",
    "conversation-to-prd",
    "decision-grilling",
    "decision-grilling-context-45",
    "domain-grilling-with-docs",
    "domain-grilling-with-docs-context-45",
    "mermaid-diagrams",
    "plantuml-diagrams",
    "prd-to-implementation-plan",
    "skill-import-generalizer",
    "technical-writing-quality-gate",
}

SKILL_ADAPTER_REQUIRED_FILES = {
    "SKILL.md",
    "README.md",
    "AGENTS.md",
    "examples/portable-example.md",
}

REGISTRY_HEADERS: dict[str, list[str]] = {
    "source_registry.csv": [
        "source_id",
        "path",
        "source_type",
        "authority_status",
        "owner",
        "last_reviewed",
        "notes",
    ],
    "derivative_registry.csv": [
        "derivative_id",
        "path",
        "derivative_type",
        "source_ids",
        "generation_method",
        "last_generated",
        "status",
        "notes",
    ],
    "object_relationship_registry.csv": [
        "relationship_id",
        "subject_id",
        "predicate",
        "object_id",
        "evidence_path",
        "notes",
    ],
    "skill_registry.csv": [
        "skill_id",
        "local_path",
        "source_repo",
        "source_path",
        "family",
        "adaptation_status",
        "lifecycle_status",
        "last_reviewed",
        "notes",
    ],
    "format_profile_registry.csv": [
        "format_id",
        "extension",
        "format_family",
        "primary_role",
        "canonical_roots",
        "derivative_surfaces",
        "registry_required",
        "validator_required",
        "default_authority_class",
        "promotion_rule",
        "secrets_allowed",
        "notes",
    ],
    "config_source_registry.csv": [
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
        "supersedes",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "control_record_registry.csv": [
        "control_record_id",
        "path",
        "record_type",
        "authority_status",
        "owner",
        "validation_contract_id",
        "allowed_writers",
        "allowed_readers",
        "related_agentjob_id",
        "supersedes",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "validation_contract_registry.csv": [
        "contract_id",
        "path",
        "dialect",
        "target_format",
        "target_artifact_type",
        "target_glob",
        "authority_status",
        "owner",
        "validator_command",
        "supersedes",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "requirement_trace_registry.csv": [
        "trace_id",
        "phase0_selector",
        "phase0_source",
        "coverage_status",
        "trace_class",
        "semantic_justification",
        "semantic_review_verdict",
        "phase1_selectors",
        "evidence_paths",
        "notes",
    ],
    "agentjob_registry.csv": [
        "agentjob_id",
        "path",
        "status",
        "role_id",
        "task_id",
        "created_at",
        "activated_at",
        "completed_at",
        "completion_receipt_id",
        "handoff_id",
        "authority_status",
        "supersedes",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "director_decision_registry.csv": [
        "director_decision_id",
        "path",
        "status",
        "task_id",
        "selected_route",
        "selected_agentjob_id",
        "authority_status",
        "supersedes",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "handoff_registry.csv": [
        "handoff_id",
        "path",
        "status",
        "producing_agentjob_id",
        "next_recommended_role",
        "next_agentjob_id",
        "source_ids",
        "supersedes",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "completion_receipt_registry.csv": [
        "completion_receipt_id",
        "path",
        "agentjob_id",
        "result",
        "validation_status",
        "changed_artifacts_count",
        "next_handoff_id",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "memory_preflight_receipt_registry.csv": [
        "memory_preflight_receipt_id",
        "path",
        "agentjob_id",
        "created_at",
        "status",
        "queries_count",
        "hits_count",
        "canonical_inspections_count",
        "stale_risks_count",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "system_layer_registry.csv": [
        "layer_id",
        "layer_name",
        "layer_type",
        "canonical_roots",
        "mutable_roots",
        "derivative_roots",
        "authority_notes",
        "requires_director_decision_for_mutation",
        "default_validators",
        "owner",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "discovery_record_registry.csv": [
        "discovery_record_id",
        "path",
        "subject_system_id",
        "subject_layer",
        "status",
        "producer_agentjob_id",
        "source_authority_status",
        "candidate_requirement_count",
        "open_question_count",
        "downstream_usrd_path",
        "validation_status",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "role_registry.csv": [
        "role_id",
        "role_name",
        "role_class",
        "system_layer_scope",
        "primary_mission",
        "required_skills",
        "optional_skills",
        "forbidden_skills",
        "primary_outputs",
        "allowed_artifact_classes",
        "may_create_agentjobs",
        "requires_director_decision",
        "authority_status",
        "owner",
        "supersedes",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "role_skill_crosswalk.csv": [
        "crosswalk_id",
        "role_id",
        "skill_id",
        "binding_type",
        "required_when",
        "system_layer_scope",
        "invocation_policy",
        "authority_status",
        "evidence_path",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "role_execution_binding_registry.csv": [
        "binding_id",
        "role_id",
        "allowed_agentjob_types",
        "allowed_reads",
        "allowed_writes",
        "forbidden_actions",
        "required_validators",
        "completion_evidence",
        "expiry_policy",
        "authority_status",
        "owner",
        "supersedes",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "artifact_contract_registry.csv": [
        "artifact_contract_id",
        "artifact_type",
        "canonical_filename_or_pattern",
        "producer_role_ids",
        "consumer_role_ids",
        "system_layer_scope",
        "authority_default",
        "required_sections",
        "validation_contract_id",
        "registry_required",
        "derivative_surfaces",
        "promotion_rule",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "core_skill_proposal_registry.csv": [
        "proposal_id",
        "skill_id",
        "skill_family",
        "priority",
        "status",
        "core_or_project_specific",
        "required_by_roles",
        "source_rationale",
        "target_runtime_path",
        "product_scaffold_path",
        "validator_plan",
        "owner",
        "source_hash",
        "last_validated_at",
        "notes",
    ],
    "skill_lifecycle_status_registry.csv": [
        "status_id",
        "status_name",
        "may_execute_runtime",
        "may_be_used_as_authority",
        "requires_provenance",
        "requires_manifest",
        "requires_skill_md",
        "requires_validator",
        "allowed_roots",
        "notes",
    ],
}

EXPECTED_FORMAT_PROFILE_IDS = {
    "fmt_markdown_source",
    "fmt_csv_registry",
    "fmt_yaml_control",
    "fmt_toml_config",
    "fmt_jsonschema_contract",
}

ROW_CONTRACTS = {
    "format_profile_registry.csv": "schemas/contracts/format_profile_registry_row.schema.json",
    "config_source_registry.csv": "schemas/contracts/config_source_registry_row.schema.json",
    "control_record_registry.csv": "schemas/contracts/control_record_registry_row.schema.json",
    "validation_contract_registry.csv": "schemas/contracts/validation_contract_registry_row.schema.json",
    "requirement_trace_registry.csv": "schemas/contracts/requirement_trace_registry_row.schema.json",
    "agentjob_registry.csv": "schemas/contracts/agentjob_registry_row.schema.json",
    "director_decision_registry.csv": "schemas/contracts/director_decision_registry_row.schema.json",
    "handoff_registry.csv": "schemas/contracts/handoff_registry_row.schema.json",
    "completion_receipt_registry.csv": "schemas/contracts/completion_receipt_registry_row.schema.json",
    "memory_preflight_receipt_registry.csv": "schemas/contracts/memory_preflight_receipt_registry_row.schema.json",
    "system_layer_registry.csv": "schemas/contracts/system_layer_registry_row.schema.json",
    "discovery_record_registry.csv": "schemas/contracts/discovery_record_registry_row.schema.json",
    "role_registry.csv": "schemas/contracts/role_registry_row.schema.json",
    "role_skill_crosswalk.csv": "schemas/contracts/role_skill_crosswalk_row.schema.json",
    "role_execution_binding_registry.csv": "schemas/contracts/role_execution_binding_registry_row.schema.json",
    "artifact_contract_registry.csv": "schemas/contracts/artifact_contract_registry_row.schema.json",
    "core_skill_proposal_registry.csv": "schemas/contracts/core_skill_proposal_registry_row.schema.json",
    "skill_lifecycle_status_registry.csv": "schemas/contracts/skill_lifecycle_status_registry_row.schema.json",
}


def _require_mapping(data: Any, path: Path) -> list[str]:
    if not isinstance(data, dict):
        return [f"{path}: expected a YAML mapping at the document root"]
    return []


def validate_agentjob(path: str | Path) -> ValidationResult:
    target = Path(path)
    messages: list[str] = []
    data = load_yaml(target)
    messages.extend(_require_mapping(data, target))
    if messages:
        return ValidationResult(False, messages)

    if data.get("schema_version") == "0.2.0":
        messages.extend(_validate_instance_with_schema(data, "schemas/contracts/agentjob_v0_2.schema.json", str(target)))
        return ValidationResult(not messages, messages or [f"{target}: AgentJob v0.2 validation passed"])

    missing = sorted(AGENTJOB_REQUIRED_FIELDS - set(data))
    if missing:
        messages.append(f"{target}: missing required AgentJob fields: {', '.join(missing)}")

    list_fields = [
        "allowed_reads",
        "allowed_writes",
        "forbidden_actions",
        "expected_outputs",
        "validators",
        "stop_conditions",
    ]
    for field in list_fields:
        if field in data and not isinstance(data[field], list):
            messages.append(f"{target}: field {field!r} must be a list")

    return ValidationResult(not messages, messages or [f"{target}: AgentJob validation passed"])


def validate_skill_manifest(path: str | Path) -> ValidationResult:
    target = Path(path)
    root = target.parent
    messages: list[str] = []
    data = load_yaml(target)
    messages.extend(_require_mapping(data, target))
    if messages:
        return ValidationResult(False, messages)

    skills = data.get("skills")
    if not isinstance(skills, list):
        return ValidationResult(False, [f"{target}: expected 'skills' to be a list"])

    seen: set[str] = set()
    for index, item in enumerate(skills, start=1):
        if not isinstance(item, dict):
            messages.append(f"{target}: skill entry #{index} must be a mapping")
            continue
        skill_id = item.get("id")
        if not isinstance(skill_id, str) or not skill_id:
            messages.append(f"{target}: skill entry #{index} has missing string id")
            continue
        seen.add(skill_id)
        adaptation_status = str(item.get("adaptation_status", ""))
        lifecycle_status = str(item.get("lifecycle_status", ""))
        expected_lifecycle = _product_lifecycle_from_adaptation(adaptation_status)
        known_lifecycle_statuses = _known_skill_lifecycle_statuses()
        if not lifecycle_status:
            messages.append(f"{target}: {skill_id} missing lifecycle_status")
        elif lifecycle_status not in known_lifecycle_statuses:
            messages.append(f"{target}: {skill_id} unknown lifecycle_status {lifecycle_status!r}")
        if expected_lifecycle and lifecycle_status and expected_lifecycle != lifecycle_status:
            messages.append(
                f"{target}: {skill_id} lifecycle_status {lifecycle_status!r} does not match adaptation_status {adaptation_status!r}"
            )
        if lifecycle_status == "adapted_runtime_active":
            messages.append(f"{target}: {skill_id} product scaffold skill cannot be runtime-active")
        local_path = item.get("local_path", f"core/{skill_id}")
        adapter = root / str(local_path)
        if not adapter.exists():
            messages.append(f"{target}: adapter folder missing for {skill_id}: {adapter}")
            continue
        for rel in sorted(SKILL_ADAPTER_REQUIRED_FILES):
            if not (adapter / rel).exists():
                messages.append(f"{target}: {skill_id} missing required adapter file {rel}")
        scripts = item.get("scripts", [])
        if scripts is None:
            scripts = []
        if not isinstance(scripts, list):
            messages.append(f"{target}: {skill_id} field 'scripts' must be a list when present")
        else:
            for rel_script in scripts:
                if not isinstance(rel_script, str) or not rel_script:
                    messages.append(
                        f"{target}: {skill_id} has invalid script path entry: {rel_script!r}"
                    )
                    continue
                if not (adapter / rel_script).exists():
                    messages.append(f"{target}: {skill_id} missing declared script {rel_script}")

    missing_skills = sorted(SKILL_MANIFEST_REQUIRED_SKILLS - seen)
    extra_skills = sorted(seen - SKILL_MANIFEST_REQUIRED_SKILLS)
    if missing_skills:
        messages.append(f"{target}: missing core skills: {', '.join(missing_skills)}")
    if extra_skills:
        messages.append(f"{target}: non-core skills listed for Phase 1 review: {', '.join(extra_skills)}")

    return ValidationResult(not messages, messages or [f"{target}: skill manifest validation passed"])


def validate_registry_headers(registry_dir: str | Path) -> ValidationResult:
    root = Path(registry_dir)
    messages: list[str] = []
    for filename, expected_header in REGISTRY_HEADERS.items():
        path = root / filename
        if not path.exists():
            messages.append(f"{path}: missing registry file")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        first_line = lines[0] if lines else ""
        actual = [part.strip() for part in first_line.split(",")]
        if actual != expected_header:
            messages.append(
                f"{path}: header mismatch. Expected {expected_header!r}, found {actual!r}"
            )
    return ValidationResult(not messages, messages or [f"{root}: registry header validation passed"])


def _extract_requirement_declarations(path: str | Path) -> tuple[list[RequirementDeclaration], list[str]]:
    target = resolve_registered_path(str(path))
    if not target.exists():
        return [], [f"{path}: PRD file not found at {target}"]

    declarations: list[RequirementDeclaration] = []
    for line_number, line in enumerate(target.read_text(encoding="utf-8").splitlines(), start=1):
        match = BACKTICK_REQUIREMENT_RE.match(line) or TABLE_REQUIREMENT_RE.match(line)
        if match is None:
            continue
        declarations.append(
            RequirementDeclaration(
                requirement_id=match.group("id"),
                path=target,
                line_number=line_number,
            )
        )
    return declarations, []


def _split_selectors(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def _matches_selector(selector: str, candidates: Iterable[str]) -> list[str]:
    return sorted(candidate for candidate in candidates if fnmatchcase(candidate, selector))


def _check_layer_scope(label: str, value: str, known_layers: set[str]) -> list[str]:
    messages: list[str] = []
    for layer_id in _split_selectors(value):
        if layer_id not in known_layers:
            messages.append(f"{label}: unknown system layer {layer_id!r}")
    return messages


def _load_skill_ids() -> set[str]:
    skill_ids: set[str] = set()
    root_registry = Path("../.agents/skill_registry/SKILL_REGISTRY.yaml")
    if root_registry.exists():
        data = load_yaml(root_registry)
        if isinstance(data, dict):
            for item in data.get("skills", []):
                if isinstance(item, dict) and item.get("skill_id"):
                    skill_ids.add(str(item["skill_id"]))

    product_manifest = Path("skills/core_skill_manifest.yaml")
    if product_manifest.exists():
        data = load_yaml(product_manifest)
        if isinstance(data, dict):
            for item in data.get("skills", []):
                if isinstance(item, dict) and item.get("id"):
                    skill_ids.add(str(item["id"]))
    return skill_ids


def _load_runtime_skill_lifecycle() -> dict[str, str]:
    lifecycle: dict[str, str] = {}
    for item in _load_runtime_skill_entries():
        skill_id = item.get("skill_id")
        if skill_id:
            lifecycle[str(skill_id)] = str(item.get("lifecycle_status") or item.get("migration_phase") or "")
    return lifecycle


def _load_product_skill_lifecycle() -> dict[str, str]:
    lifecycle: dict[str, str] = {}
    product_manifest = Path("skills/core_skill_manifest.yaml")
    if product_manifest.exists():
        data = load_yaml(product_manifest)
        if isinstance(data, dict):
            for item in data.get("skills", []):
                if not isinstance(item, dict):
                    continue
                skill_id = item.get("id")
                if skill_id:
                    lifecycle[str(skill_id)] = str(
                        item.get("lifecycle_status")
                        or _product_lifecycle_from_adaptation(str(item.get("adaptation_status", "")))
                    )
    return lifecycle


def _load_runtime_skill_entries(path: str | Path = "../.agents/skill_registry/SKILL_REGISTRY.yaml") -> list[dict[str, Any]]:
    registry = Path(path)
    if not registry.exists():
        return []
    data = load_yaml(registry)
    if not isinstance(data, dict):
        return []
    return [item for item in data.get("skills", []) if isinstance(item, dict)]


def _product_lifecycle_from_adaptation(adaptation_status: str) -> str:
    if adaptation_status == "scaffold_template":
        return "product_scaffold_reference"
    return adaptation_status


def _known_skill_lifecycle_statuses(path: str | Path = "registries/skill_lifecycle_status_registry.csv") -> set[str]:
    registry = Path(path)
    if not registry.exists():
        return set(SKILL_LIFECYCLE_STATUS_NAMES)
    return {row.get("status_name", "") for row in read_registry_rows(registry) if row.get("status_name")}


def _find_duplicate_requirement_ids(declarations: Iterable[RequirementDeclaration]) -> list[str]:
    seen: dict[str, RequirementDeclaration] = {}
    messages: list[str] = []
    for declaration in declarations:
        previous = seen.get(declaration.requirement_id)
        if previous is not None:
            messages.append(
                "duplicate requirement ID "
                f"{declaration.requirement_id}: "
                f"{previous.path}:{previous.line_number} and "
                f"{declaration.path}:{declaration.line_number}"
            )
            continue
        seen[declaration.requirement_id] = declaration
    return messages


def validate_requirement_trace(
    trace_registry: str | Path = "registries/requirement_trace_registry.csv",
    phase0_prd: str | Path = "PRDs/sys-for-ai_phase-0_product_system_design_prd.md",
    phase1_prd: str | Path = "PRDs/sys-for-ai_phase-1_implementation_initialization_prd.md",
) -> ValidationResult:
    """Validate PRD ID uniqueness and Phase 0 to Phase 1 trace coverage."""

    target = Path(trace_registry)
    messages: list[str] = []

    row_result = _validate_rows_against_contract(
        target,
        ROW_CONTRACTS["requirement_trace_registry.csv"],
        "trace_id",
    )
    if not row_result.ok:
        messages.extend(row_result.messages)

    phase0_declarations, phase0_errors = _extract_requirement_declarations(phase0_prd)
    phase1_declarations, phase1_errors = _extract_requirement_declarations(phase1_prd)
    messages.extend(phase0_errors)
    messages.extend(phase1_errors)
    messages.extend(_find_duplicate_requirement_ids([*phase0_declarations, *phase1_declarations]))

    phase0_ids = sorted(
        {
            declaration.requirement_id
            for declaration in phase0_declarations
            if declaration.requirement_id.startswith(PHASE0_REQUIREMENT_PREFIXES)
        }
    )
    phase1_ids = sorted(
        {
            declaration.requirement_id
            for declaration in phase1_declarations
            if declaration.requirement_id.startswith(PHASE1_REQUIREMENT_PREFIX)
        }
    )
    if not phase0_ids:
        messages.append(f"{phase0_prd}: no Phase 0 requirement IDs found")
    if not phase1_ids:
        messages.append(f"{phase1_prd}: no Phase 1 requirement IDs found")

    coverage: dict[str, list[str]] = {requirement_id: [] for requirement_id in phase0_ids}
    trace_class_counts: Counter[str] = Counter()
    semantic_review_counts: Counter[str] = Counter()
    rows = read_registry_rows(target)
    for row in rows:
        trace_id = row.get("trace_id", "")
        status = row.get("coverage_status", "")
        if status not in TRACE_COVERAGE_STATUSES:
            messages.append(f"{target}: {trace_id}: invalid coverage_status {status!r}")
        trace_class = row.get("trace_class", "")
        if trace_class not in TRACE_CLASSES:
            messages.append(f"{target}: {trace_id}: invalid trace_class {trace_class!r}")
        else:
            trace_class_counts[trace_class] += 1
            allowed_classes = TRACE_CLASSES_BY_COVERAGE.get(status, set())
            if allowed_classes and trace_class not in allowed_classes:
                messages.append(
                    f"{target}: {trace_id}: trace_class {trace_class!r} does not match "
                    f"coverage_status {status!r}"
                )
        semantic_justification = row.get("semantic_justification", "").strip()
        if status == "partial" and not semantic_justification:
            messages.append(f"{target}: {trace_id}: partial row requires semantic_justification")
        if trace_class in {"scaffolded", "deferred", "out_of_phase"} and not semantic_justification:
            messages.append(
                f"{target}: {trace_id}: trace_class {trace_class!r} requires semantic_justification"
            )
        semantic_review_verdict = row.get("semantic_review_verdict", "").strip()
        if semantic_review_verdict:
            if semantic_review_verdict not in SEMANTIC_REVIEW_VERDICTS:
                messages.append(
                    f"{target}: {trace_id}: invalid semantic_review_verdict "
                    f"{semantic_review_verdict!r}"
                )
            else:
                semantic_review_counts[semantic_review_verdict] += 1
        if trace_class in {"scaffolded", "deferred", "out_of_phase"} and not semantic_review_verdict:
            messages.append(
                f"{target}: {trace_id}: trace_class {trace_class!r} requires "
                "semantic_review_verdict"
            )

        phase0_selectors = _split_selectors(row.get("phase0_selector", ""))
        if not phase0_selectors:
            messages.append(f"{target}: {trace_id}: missing phase0_selector")
        elif len(phase0_selectors) != 1:
            messages.append(
                f"{target}: {trace_id}: phase0_selector must contain exactly one Phase 0 requirement ID"
            )
        for selector in phase0_selectors:
            matches = _matches_selector(selector, phase0_ids)
            if not matches:
                messages.append(f"{target}: {trace_id}: phase0 selector {selector!r} matches no Phase 0 requirement IDs")
                continue
            if len(matches) != 1 or selector != matches[0]:
                messages.append(
                    f"{target}: {trace_id}: phase0 selector {selector!r} must be one literal Phase 0 requirement ID"
                )
                continue
            for requirement_id in matches:
                coverage.setdefault(requirement_id, []).append(trace_id)

        phase1_selectors = _split_selectors(row.get("phase1_selectors", ""))
        if status in {"covered", "partial"} and not phase1_selectors:
            messages.append(f"{target}: {trace_id}: {status} row requires at least one phase1 selector")
        if status in {"deferred", "not_applicable"} and not row.get("notes", "").strip():
            messages.append(f"{target}: {trace_id}: {status} row requires notes")
        for selector in phase1_selectors:
            matches = _matches_selector(selector, phase1_ids)
            if not matches:
                messages.append(f"{target}: {trace_id}: phase1 selector {selector!r} matches no Phase 1 requirement IDs")

        evidence_paths = _split_selectors(row.get("evidence_paths", ""))
        if not evidence_paths:
            messages.append(f"{target}: {trace_id}: missing evidence_paths")
        for evidence_path in evidence_paths:
            resolved = resolve_registered_path(evidence_path)
            if not resolved.exists():
                messages.append(f"{target}: {trace_id}: missing evidence path {evidence_path}")

    missing = [requirement_id for requirement_id, trace_ids in coverage.items() if not trace_ids]
    if missing:
        messages.append(f"{target}: missing Phase 0 trace coverage for: {', '.join(missing)}")

    duplicated = {
        requirement_id: trace_ids
        for requirement_id, trace_ids in coverage.items()
        if len(trace_ids) > 1
    }
    for requirement_id, trace_ids in sorted(duplicated.items()):
        messages.append(
            f"{target}: Phase 0 requirement {requirement_id} is covered by multiple trace rows: "
            f"{', '.join(trace_ids)}"
        )

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            f"{target}: requirement trace validation passed "
            f"({len(phase0_ids)} Phase 0 requirements traced by explicit rows; "
            f"{len(phase1_ids)} Phase 1 requirements indexed; "
            f"trace classes: {_format_trace_class_counts(trace_class_counts)}; "
            f"semantic review: {_format_semantic_review_counts(semantic_review_counts)})"
        ],
    )


def _format_trace_class_counts(counts: Counter[str]) -> str:
    return ", ".join(
        f"{trace_class}={counts[trace_class]}"
        for trace_class in ("implemented", "scaffolded", "deferred", "out_of_phase")
        if counts[trace_class]
    )


def _format_semantic_review_counts(counts: Counter[str]) -> str:
    summary = [
        f"{verdict}={counts[verdict]}"
        for verdict in ("sufficient", "needs_evidence", "incorrect_mapping")
        if counts[verdict]
    ]
    return ", ".join(summary) if summary else "none"


def _load_contract_schema(path: str | Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        from .jsonschema_io import check_schema, load_json
    except ModuleNotFoundError as exc:
        return None, [f"jsonschema dependency unavailable: {exc}"]

    target = resolve_registered_path(str(path))
    try:
        schema = load_json(target)
    except RuntimeError as exc:
        return None, [str(exc)]
    errors = check_schema(schema)
    if errors:
        return None, [f"{target}: invalid JSON Schema: {error}" for error in errors]
    return schema, []


def _validate_instance_with_schema(instance: Any, schema_path: str | Path, label: str) -> list[str]:
    try:
        from .jsonschema_io import validate_instance
    except ModuleNotFoundError as exc:
        return [f"jsonschema dependency unavailable: {exc}"]

    schema, errors = _load_contract_schema(schema_path)
    if schema is None:
        return errors
    return [f"{label}: {error}" for error in validate_instance(instance, schema)]


def _validate_rows_against_contract(
    path: str | Path,
    schema_path: str | Path,
    id_field: str,
) -> ValidationResult:
    target = Path(path)
    messages: list[str] = []
    header, rows = read_registry(target)
    expected = REGISTRY_HEADERS.get(target.name)
    if expected and header != expected:
        messages.append(f"{target}: header mismatch. Expected {expected!r}, found {header!r}")

    seen: set[str] = set()
    for index, row in enumerate(rows, start=2):
        row_id = row.get(id_field, "")
        if not row_id:
            messages.append(f"{target}:{index}: missing {id_field}")
        elif row_id in seen:
            messages.append(f"{target}:{index}: duplicate {id_field} {row_id!r}")
        else:
            seen.add(row_id)
        messages.extend(_validate_instance_with_schema(row, schema_path, f"{target}:{index}"))

    return ValidationResult(not messages, messages or [f"{target}: row validation passed"])


def _contract_index(
    registry_path: str | Path = "registries/validation_contract_registry.csv",
) -> dict[str, dict[str, str]]:
    rows = read_registry_rows(registry_path)
    return rows_by_id(rows, "contract_id")


def _contract_path(contract_id: str, contracts: dict[str, dict[str, str]]) -> str | None:
    row = contracts.get(contract_id)
    if row is None:
        return None
    return row.get("path") or None


def validate_format_profiles(path: str | Path) -> ValidationResult:
    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["format_profile_registry.csv"],
        "format_id",
    )
    if result.ok:
        rows = read_registry_rows(path)
        seen = {row.get("format_id", "") for row in rows}
        missing = sorted(EXPECTED_FORMAT_PROFILE_IDS - seen)
        if missing:
            result.ok = False
            result.messages.append(f"{path}: missing expected format profile IDs: {', '.join(missing)}")
    return result


def validate_config_sources(path: str | Path) -> ValidationResult:
    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["config_source_registry.csv"],
        "config_id",
    )
    contracts = _contract_index()
    rows = read_registry_rows(path)
    for row in rows:
        contract_id = row.get("validation_contract_id", "")
        if contract_id and contract_id not in contracts:
            result.ok = False
            result.messages.append(f"{path}: {row.get('config_id')}: unknown contract {contract_id!r}")
        resolved = resolve_registered_path(row.get("path", ""))
        if not resolved.exists():
            result.ok = False
            result.messages.append(f"{path}: {row.get('config_id')}: missing config source {resolved}")
    return result


def validate_control_records(path: str | Path) -> ValidationResult:
    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["control_record_registry.csv"],
        "control_record_id",
    )
    contracts = _contract_index()
    for row in read_registry_rows(path):
        record_path = resolve_registered_path(row.get("path", ""))
        if not record_path.exists():
            result.ok = False
            result.messages.append(f"{path}: {row.get('control_record_id')}: missing control record {record_path}")
            continue
        data = load_yaml(record_path)
        secret_findings = find_secret_like_values(data)
        if secret_findings:
            result.ok = False
            result.messages.extend(f"{record_path}: {finding}" for finding in secret_findings)
        contract_id = row.get("validation_contract_id", "")
        if not contract_id:
            continue
        schema_path = _contract_path(contract_id, contracts)
        if schema_path is None:
            result.ok = False
            result.messages.append(f"{path}: {row.get('control_record_id')}: unknown contract {contract_id!r}")
            continue
        errors = _validate_instance_with_schema(data, schema_path, str(record_path))
        if errors:
            result.ok = False
            result.messages.extend(errors)
    return result


def validate_program_state(path: str | Path = "control_records/program_state.yaml") -> ValidationResult:
    """Validate tracked /continue program state."""

    target = Path(path)
    messages: list[str] = []
    data = load_yaml(target)
    messages.extend(_require_mapping(data, target))
    if messages:
        return ValidationResult(False, messages)

    messages.extend(_validate_instance_with_schema(data, "schemas/contracts/program_state.schema.json", str(target)))

    state_status = data.get("state_status")
    blocked_reason = data.get("blocked_reason")
    if state_status == "blocked" and not blocked_reason:
        messages.append(f"{target}: blocked state requires blocked_reason")
    if state_status == "human_gated" and data.get("human_gate_required") is not True:
        messages.append(f"{target}: human_gated state requires human_gate_required=true")

    blocked_actions = set(data.get("blocked_actions", []))
    required_blocks = {
        "execute_multiple_agentjobs",
        "use_chat_memory_as_authority",
        "treat_generated_derivative_as_canonical",
        "mutate_activated_control_record_without_supersession",
    }
    missing_blocks = sorted(required_blocks - blocked_actions)
    if missing_blocks:
        messages.append(f"{target}: missing blocked_actions: {', '.join(missing_blocks)}")

    return ValidationResult(not messages, messages or [f"{target}: program state validation passed"])


def validate_director_decisions(root: str | Path = "control_records/director_decisions") -> ValidationResult:
    """Validate Director Decision Record YAML files under *root*."""

    return _validate_yaml_records_in_root(root, "director_decision.schema.json", "director_decision_id")


def validate_handoffs(root: str | Path = "control_records/handoffs") -> ValidationResult:
    """Validate operational handoff v0.2 YAML files under *root*."""

    return _validate_yaml_records_in_root(root, "handoff_v0_2.schema.json", "handoff_id")


def validate_completion_receipts(root: str | Path = "control_records/completions") -> ValidationResult:
    """Validate operational completion receipt v0.2 YAML files under *root*."""

    result = _validate_yaml_records_in_root(root, "completion_receipt_v0_2.schema.json", "completion_receipt_id")
    if not result.ok:
        return result

    messages = list(result.messages)
    base = _registry_base_from_control_path(root)
    agentjob_ids = _known_agentjob_ids(base)
    handoff_ids = _known_handoff_ids(base)
    for path in _yaml_paths(root):
        data = load_yaml(path)
        agentjob_id = data.get("agentjob_id")
        if agentjob_id not in agentjob_ids:
            messages.append(f"{path}: unknown agentjob_id {agentjob_id!r}")
        handoff_id = data.get("next_handoff_id")
        if isinstance(handoff_id, str) and handoff_id and handoff_id not in handoff_ids:
            fallback = base / "control_records/handoffs" / f"{handoff_id}.yaml"
            if not fallback.exists():
                messages.append(f"{path}: unknown next_handoff_id {handoff_id!r}")
        changed = data.get("changed_artifacts", [])
        if not isinstance(changed, list):
            messages.append(f"{path}: changed_artifacts must be a list")
            continue
        for item in changed:
            if not isinstance(item, dict) or not item.get("path"):
                messages.append(f"{path}: changed_artifacts entries must be mappings with path")
    failures = [msg for msg in messages if "validation passed" not in msg and "no operational" not in msg]
    return ValidationResult(not failures, messages)


def validate_state_snapshots(root: str | Path = "control_records/state_snapshots") -> ValidationResult:
    """Validate bounded state snapshot YAML files under *root*."""

    result = _validate_yaml_records_in_root(root, "state_snapshot.schema.json", "state_snapshot_id")
    if not result.ok:
        return result

    messages = list(result.messages)
    base = _registry_base_from_control_path(root)
    agentjob_ids = _known_agentjob_ids(base)
    for path in _yaml_paths(root):
        data = load_yaml(path)
        agentjob_id = data.get("current_agentjob_id")
        if agentjob_id not in agentjob_ids:
            messages.append(f"{path}: unknown current_agentjob_id {agentjob_id!r}")
    failures = [msg for msg in messages if "validation passed" not in msg and "no operational" not in msg]
    return ValidationResult(not failures, messages)


def validate_memory_preflight_receipts(root: str | Path = "control_records/memory_preflights") -> ValidationResult:
    """Validate memory preflight receipt YAML files under *root*."""

    result = _validate_yaml_records_in_root(root, "memory_preflight_receipt.schema.json", "memory_preflight_receipt_id")
    if not result.ok:
        return result

    messages = list(result.messages)
    paths = _yaml_paths(root)
    agentjob_ids = _known_agentjob_ids()
    source_rows = rows_by_id(read_registry_rows("registries/source_registry.csv"), "source_id")
    for path in paths:
        data = load_yaml(path)
        agentjob_id = data.get("agentjob_id")
        if agentjob_id not in agentjob_ids:
            messages.append(f"{path}: unknown agentjob_id {agentjob_id!r}")
        if data.get("usable_for_routing") is True:
            if not data.get("queries"):
                messages.append(f"{path}: usable_for_routing=true requires queries")
            if not data.get("canonical_sources_inspected") and not data.get("registry_rows_inspected"):
                messages.append(f"{path}: usable_for_routing=true requires source or registry inspection evidence")
        for item in data.get("canonical_sources_inspected", []):
            if not isinstance(item, dict):
                messages.append(f"{path}: canonical_sources_inspected items must be mappings")
                continue
            row_id = str(item.get("row_id", ""))
            if row_id and row_id not in source_rows:
                messages.append(f"{path}: canonical source row_id {row_id!r} not found in source_registry.csv")
        for item in data.get("registry_rows_inspected", []):
            if not isinstance(item, dict):
                messages.append(f"{path}: registry_rows_inspected items must be mappings")
                continue
            registry = str(item.get("registry", ""))
            row_id = str(item.get("row_id", ""))
            if registry and row_id and not _registry_row_exists(registry, row_id):
                messages.append(f"{path}: registry row {registry}:{row_id} not found")

    return ValidationResult(not [msg for msg in messages if "validation passed" not in msg and "no operational" not in msg], messages)


def validate_agentjob_registry(path: str | Path = "registries/agentjob_registry.csv") -> ValidationResult:
    return _validate_rows_against_contract(path, ROW_CONTRACTS["agentjob_registry.csv"], "agentjob_id")


def validate_director_decision_registry(path: str | Path = "registries/director_decision_registry.csv") -> ValidationResult:
    return _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["director_decision_registry.csv"],
        "director_decision_id",
    )


def validate_handoff_registry(path: str | Path = "registries/handoff_registry.csv") -> ValidationResult:
    return _validate_rows_against_contract(path, ROW_CONTRACTS["handoff_registry.csv"], "handoff_id")


def validate_completion_receipt_registry(path: str | Path = "registries/completion_receipt_registry.csv") -> ValidationResult:
    return _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["completion_receipt_registry.csv"],
        "completion_receipt_id",
    )


def validate_memory_preflight_registry(path: str | Path = "registries/memory_preflight_receipt_registry.csv") -> ValidationResult:
    return _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["memory_preflight_receipt_registry.csv"],
        "memory_preflight_receipt_id",
    )


def validate_system_layers(path: str | Path = "registries/system_layer_registry.csv") -> ValidationResult:
    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["system_layer_registry.csv"],
        "layer_id",
    )
    rows = read_registry_rows(path)
    seen = {row.get("layer_id", "") for row in rows}
    missing = sorted(SYSTEM_LAYER_IDS - seen)
    if missing:
        result.ok = False
        result.messages.append(f"{path}: missing expected system layer IDs: {', '.join(missing)}")
    for row in rows:
        if row.get("layer_id") != row.get("layer_type"):
            result.ok = False
            result.messages.append(
                f"{path}: {row.get('layer_id')}: layer_type must match layer_id"
            )
    return result


def validate_discovery_records(path: str | Path = "registries/discovery_record_registry.csv") -> ValidationResult:
    from .discovery import validate_discovery_record

    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["discovery_record_registry.csv"],
        "discovery_record_id",
    )
    known_layers = _known_system_layers()
    for row in read_registry_rows(path):
        record_id = row.get("discovery_record_id", "")
        subject_layer = row.get("subject_layer", "")
        if subject_layer not in known_layers:
            result.ok = False
            result.messages.append(f"{path}: {record_id}: unknown subject_layer {subject_layer!r}")
        record_path = resolve_registered_path(row.get("path", ""))
        if not record_path.exists():
            result.ok = False
            result.messages.append(f"{path}: {record_id}: missing discovery record {record_path}")
            continue
        record_result = validate_discovery_record(record_path, require_evidence_row=True)
        result.extend(record_result)
        source_hash = row.get("source_hash", "").strip()
        if source_hash and source_hash != "pending":
            actual = hashlib.sha256(record_path.read_bytes()).hexdigest()
            if source_hash != actual:
                result.ok = False
                result.messages.append(f"{path}: {record_id}: source_hash mismatch")
        downstream = row.get("downstream_usrd_path", "").strip()
        if downstream and not resolve_registered_path(downstream).exists():
            result.messages.append(f"{path}: {record_id}: downstream USRD path not found yet: {downstream}")
    return result


def validate_roles(
    role_registry: str | Path = "registries/role_registry.csv",
    crosswalk: str | Path = "registries/role_skill_crosswalk.csv",
    execution_bindings: str | Path = "registries/role_execution_binding_registry.csv",
) -> ValidationResult:
    from .role_validators import validate_roles as validate_role_governance

    return validate_role_governance(role_registry, crosswalk, execution_bindings)


def validate_artifact_contracts(path: str | Path = "registries/artifact_contract_registry.csv") -> ValidationResult:
    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["artifact_contract_registry.csv"],
        "artifact_contract_id",
    )
    known_roles = _known_roles()
    known_layers = _known_system_layers()
    contract_ids = _known_contract_ids()
    for row in read_registry_rows(path):
        artifact_id = row.get("artifact_contract_id", "")
        result.messages.extend(_unknown_roles_message(path, artifact_id, "producer_role_ids", row.get("producer_role_ids", ""), known_roles))
        result.messages.extend(_unknown_roles_message(path, artifact_id, "consumer_role_ids", row.get("consumer_role_ids", ""), known_roles))
        result.messages.extend(_check_layer_scope(f"{path}: {artifact_id}", row.get("system_layer_scope", ""), known_layers))
        contract_id = row.get("validation_contract_id", "").strip()
        if contract_id and contract_id not in contract_ids:
            result.messages.append(f"{path}: {artifact_id}: unknown validation_contract_id {contract_id!r}")
    result.ok = not [msg for msg in result.messages if "row validation passed" not in msg]
    return result


def validate_core_skill_proposals(path: str | Path = "registries/core_skill_proposal_registry.csv") -> ValidationResult:
    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["core_skill_proposal_registry.csv"],
        "proposal_id",
    )
    known_roles = _known_roles()
    for row in read_registry_rows(path):
        proposal_id = row.get("proposal_id", "")
        if row.get("core_or_project_specific") != "core":
            result.ok = False
            result.messages.append(f"{path}: {proposal_id}: core_or_project_specific must be core")
        result.messages.extend(
            _unknown_roles_message(path, proposal_id, "required_by_roles", row.get("required_by_roles", ""), known_roles)
        )
    result.ok = not [msg for msg in result.messages if "row validation passed" not in msg]
    return result


def validate_skill_lifecycle(path: str | Path = "registries/skill_lifecycle_status_registry.csv") -> ValidationResult:
    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["skill_lifecycle_status_registry.csv"],
        "status_id",
    )
    rows = read_registry_rows(path)
    statuses = {row.get("status_name", "") for row in rows}
    missing = sorted(SKILL_LIFECYCLE_STATUS_NAMES - statuses)
    if missing:
        result.ok = False
        result.messages.append(f"{path}: missing expected lifecycle statuses: {', '.join(missing)}")

    executable_statuses = {
        row.get("status_name", "")
        for row in rows
        if row.get("may_execute_runtime") == "true" and row.get("may_be_used_as_authority") == "true"
    }
    blocked_required_lifecycles = {"deprecated", "superseded", "blocked"}

    runtime_lifecycle = _load_runtime_skill_lifecycle()
    for item in _load_runtime_skill_entries():
        skill_id = str(item.get("skill_id", ""))
        lifecycle = str(item.get("lifecycle_status") or item.get("migration_phase") or "")
        migration_phase = str(item.get("migration_phase", ""))
        if item.get("lifecycle_status") and migration_phase and item.get("lifecycle_status") != migration_phase:
            result.ok = False
            result.messages.append(
                f"../.agents/skill_registry/SKILL_REGISTRY.yaml: {skill_id}: lifecycle_status must match migration_phase during transition"
            )
        if str(item.get("canonical_path", "")).startswith(".codex/"):
            result.ok = False
            result.messages.append(f"../.agents/skill_registry/SKILL_REGISTRY.yaml: {skill_id}: canonical_path points at shim")
        for shim_path in item.get("compatibility_shims", []):
            if not isinstance(shim_path, str) or not shim_path.startswith(".codex/"):
                result.ok = False
                result.messages.append(f"../.agents/skill_registry/SKILL_REGISTRY.yaml: {skill_id}: invalid compatibility shim {shim_path!r}")
        manifest_path = Path("..") / str(item.get("manifest_path", ""))
        if manifest_path.exists():
            manifest = load_yaml(manifest_path)
            if isinstance(manifest, dict):
                manifest_lifecycle = manifest.get("lifecycle_status")
                if manifest_lifecycle != lifecycle:
                    result.ok = False
                    result.messages.append(
                        f"{manifest_path}: {skill_id}: manifest lifecycle_status must match runtime registry"
                    )

    for skill_id, lifecycle in runtime_lifecycle.items():
        if lifecycle not in statuses:
            result.ok = False
            result.messages.append(f"../.agents/skill_registry/SKILL_REGISTRY.yaml: {skill_id}: unknown lifecycle {lifecycle!r}")
        if lifecycle and lifecycle not in executable_statuses:
            result.ok = False
            result.messages.append(
                f"../.agents/skill_registry/SKILL_REGISTRY.yaml: {skill_id}: active runtime skill has non-executable lifecycle {lifecycle!r}"
            )
    product_lifecycle = _load_product_skill_lifecycle()
    for skill_id, lifecycle in product_lifecycle.items():
        if lifecycle and lifecycle not in statuses:
            result.ok = False
            result.messages.append(f"skills/core_skill_manifest.yaml: {skill_id}: unknown lifecycle {lifecycle!r}")
        if lifecycle == "adapted_runtime_active":
            result.ok = False
            result.messages.append(f"skills/core_skill_manifest.yaml: {skill_id}: product scaffold cannot be runtime-active")

    skill_registry = Path("registries/skill_registry.csv")
    if skill_registry.exists():
        for row in read_registry_rows(skill_registry):
            skill_id = row.get("skill_id", "")
            lifecycle = row.get("lifecycle_status", "")
            expected = _product_lifecycle_from_adaptation(row.get("adaptation_status", ""))
            if lifecycle not in statuses:
                result.ok = False
                result.messages.append(f"{skill_registry}: {skill_id}: unknown lifecycle_status {lifecycle!r}")
            if expected and lifecycle != expected:
                result.ok = False
                result.messages.append(
                    f"{skill_registry}: {skill_id}: lifecycle_status {lifecycle!r} does not match adaptation_status {row.get('adaptation_status', '')!r}"
                )
            if lifecycle == "product_scaffold_reference" and not row.get("local_path", "").startswith("skills/core/"):
                result.ok = False
                result.messages.append(f"{skill_registry}: {skill_id}: product scaffold reference must live under skills/core")

    skill_lifecycle = {**product_lifecycle, **runtime_lifecycle}
    for row in read_registry_rows("registries/role_registry.csv"):
        role_id = row.get("role_id", "")
        for skill_id in _split_selectors(row.get("required_skills", "")):
            if skill_lifecycle.get(skill_id) in blocked_required_lifecycles:
                result.ok = False
                result.messages.append(f"registries/role_registry.csv: {role_id}: required skill {skill_id} has blocked lifecycle")
    return result


def _known_system_layers(path: str | Path = "registries/system_layer_registry.csv") -> set[str]:
    registry = Path(path)
    if not registry.exists():
        return set()
    return {row.get("layer_id", "") for row in read_registry_rows(registry) if row.get("layer_id")}


def _known_roles(path: str | Path = "registries/role_registry.csv") -> set[str]:
    registry = Path(path)
    if not registry.exists():
        return set()
    return {row.get("role_id", "") for row in read_registry_rows(registry) if row.get("role_id")}


def _known_contract_ids(path: str | Path = "registries/validation_contract_registry.csv") -> set[str]:
    registry = Path(path)
    if not registry.exists():
        return set()
    return {row.get("contract_id", "") for row in read_registry_rows(registry) if row.get("contract_id")}


def _known_proposed_skill_ids(path: str | Path = "registries/core_skill_proposal_registry.csv") -> set[str]:
    registry = Path(path)
    if not registry.exists():
        return set()
    return {
        row.get("skill_id", "")
        for row in read_registry_rows(registry)
        if row.get("skill_id") and row.get("status") not in {"blocked", "superseded"}
    }


def _unknown_roles_message(
    path: str | Path,
    row_id: str,
    field_name: str,
    value: str,
    known_roles: set[str],
) -> list[str]:
    messages: list[str] = []
    for role_id in _split_selectors(value):
        if role_id in {"all_agents", "human_sponsor"}:
            continue
        if role_id not in known_roles:
            messages.append(f"{path}: {row_id}: {field_name} references unknown role {role_id!r}")
    return messages


def _validate_role_relationships(
    role_registry: str | Path,
    crosswalk: str | Path,
    execution_bindings: str | Path,
) -> list[str]:
    messages: list[str] = []
    roles = read_registry_rows(role_registry)
    role_ids = {row.get("role_id", "") for row in roles}
    known_layers = _known_system_layers()
    known_skills = _load_skill_ids() | _known_proposed_skill_ids()

    for row in roles:
        role_id = row.get("role_id", "")
        messages.extend(_check_layer_scope(f"{role_registry}: {role_id}", row.get("system_layer_scope", ""), known_layers))
        for field_name in ("required_skills", "optional_skills", "forbidden_skills"):
            for skill_id in _split_selectors(row.get(field_name, "")):
                if skill_id not in known_skills:
                    messages.append(f"{role_registry}: {role_id}: {field_name} references unknown skill {skill_id!r}")

    for row in read_registry_rows(crosswalk):
        crosswalk_id = row.get("crosswalk_id", "")
        role_id = row.get("role_id", "")
        skill_id = row.get("skill_id", "")
        if role_id not in role_ids:
            messages.append(f"{crosswalk}: {crosswalk_id}: unknown role_id {role_id!r}")
        if skill_id not in known_skills:
            messages.append(f"{crosswalk}: {crosswalk_id}: unknown skill_id {skill_id!r}")
        messages.extend(_check_layer_scope(f"{crosswalk}: {crosswalk_id}", row.get("system_layer_scope", ""), known_layers))
        evidence_path = resolve_registered_path(row.get("evidence_path", ""))
        if not evidence_path.exists():
            messages.append(f"{crosswalk}: {crosswalk_id}: missing evidence_path {evidence_path}")

    for row in read_registry_rows(execution_bindings):
        binding_id = row.get("binding_id", "")
        role_id = row.get("role_id", "")
        if role_id not in role_ids:
            messages.append(f"{execution_bindings}: {binding_id}: unknown role_id {role_id!r}")
    return messages


def _validate_yaml_records_in_root(root: str | Path, schema_name: str, id_field: str) -> ValidationResult:
    target_root = Path(root)
    messages: list[str] = []
    if not target_root.exists():
        return ValidationResult(False, [f"{target_root}: missing record directory"])

    paths = [target_root] if target_root.is_file() else sorted(target_root.glob("*.yaml"))
    for path in paths:
        data = load_yaml(path)
        messages.extend(_require_mapping(data, path))
        if not isinstance(data, dict):
            continue
        if not data.get(id_field):
            messages.append(f"{path}: missing {id_field}")
        messages.extend(_validate_instance_with_schema(data, f"schemas/contracts/{schema_name}", str(path)))
        secret_findings = find_secret_like_values(data)
        if secret_findings:
            messages.extend(f"{path}: {finding}" for finding in secret_findings)

    if not paths:
        return ValidationResult(True, [f"{target_root}: no operational YAML records to validate yet"])
    return ValidationResult(not messages, messages or [f"{target_root}: operational YAML validation passed"])


def _yaml_paths(root: str | Path) -> list[Path]:
    target = Path(root)
    if target.is_file():
        return [target]
    if not target.exists():
        return []
    return sorted(target.glob("*.yaml"))


def _registry_base_from_control_path(path: str | Path) -> Path:
    target = Path(path)
    parts = target.parts
    if "control_records" in parts:
        index = parts.index("control_records")
        if index == 0:
            return Path(".")
        return Path(*parts[:index])
    return Path(".")


def _known_agentjob_ids(root: str | Path = ".") -> set[str]:
    base = Path(root)
    ids: set[str] = set()
    agentjob_registry = base / "registries/agentjob_registry.csv"
    control_registry = base / "registries/control_record_registry.csv"
    if agentjob_registry.exists():
        ids.update(row.get("agentjob_id", "") for row in read_registry_rows(agentjob_registry))
    if control_registry.exists():
        rows = read_registry_rows(control_registry)
        ids.update(row.get("related_agentjob_id", "") for row in rows)
    return {item for item in ids if item}


def _known_handoff_ids(root: str | Path = ".") -> set[str]:
    path = Path(root) / "registries/handoff_registry.csv"
    if not path.exists():
        return set()
    return {
        row.get("handoff_id", "")
        for row in read_registry_rows(path)
        if row.get("handoff_id")
    }


def _registry_row_exists(registry: str, row_id: str, root: str | Path = ".") -> bool:
    path = Path(root) / "registries" / registry
    if not path.exists():
        return False
    header, rows = read_registry(path)
    id_field = header[0] if header else ""
    return row_id in rows_by_id(rows, id_field)


def validate_validation_contract_registry(path: str | Path) -> ValidationResult:
    result = _validate_rows_against_contract(
        path,
        ROW_CONTRACTS["validation_contract_registry.csv"],
        "contract_id",
    )
    for row in read_registry_rows(path):
        contract_path = resolve_registered_path(row.get("path", ""))
        if not contract_path.exists():
            result.ok = False
            result.messages.append(f"{path}: {row.get('contract_id')}: missing contract {contract_path}")
            continue
        _, errors = _load_contract_schema(contract_path)
        if errors:
            result.ok = False
            result.messages.extend(errors)
    return result


def validate_toml_config(
    registry_path: str | Path = "registries/config_source_registry.csv",
) -> ValidationResult:
    try:
        from .toml_io import load_toml
    except ModuleNotFoundError as exc:
        return ValidationResult(False, [f"TOML parser dependency unavailable: {exc}"])

    messages: list[str] = []
    contracts = _contract_index()
    for row in read_registry_rows(registry_path):
        if row.get("format") != "toml":
            continue
        config_path = resolve_registered_path(row.get("path", ""))
        if not config_path.exists():
            messages.append(f"{registry_path}: {row.get('config_id')}: missing TOML file {config_path}")
            continue
        try:
            data = load_toml(config_path)
        except RuntimeError as exc:
            messages.append(str(exc))
            continue
        secret_findings = find_secret_like_values(data)
        if secret_findings:
            messages.extend(f"{config_path}: {finding}" for finding in secret_findings)
        contract_id = row.get("validation_contract_id", "")
        schema_path = _contract_path(contract_id, contracts)
        if schema_path is None:
            messages.append(f"{registry_path}: {row.get('config_id')}: unknown contract {contract_id!r}")
            continue
        messages.extend(_validate_instance_with_schema(data, schema_path, str(config_path)))
    return ValidationResult(not messages, messages or [f"{registry_path}: TOML config validation passed"])


def validate_jsonschema_contracts(root: str | Path) -> ValidationResult:
    target = Path(root)
    messages: list[str] = []
    if not target.exists():
        return ValidationResult(False, [f"{target}: missing JSON Schema contracts directory"])
    for path in sorted(target.glob("*.schema.json")):
        _, errors = _load_contract_schema(path)
        if errors:
            messages.extend(errors)
    return ValidationResult(not messages, messages or [f"{target}: JSON Schema contract validation passed"])


def validate_registry_graph(registry_dir: str | Path) -> ValidationResult:
    root = Path(registry_dir)
    messages: list[str] = []
    header_result = validate_registry_headers(root)
    if not header_result.ok:
        messages.extend(header_result.messages)

    contract_rows = read_registry_rows(root / "validation_contract_registry.csv")
    contract_ids = {row.get("contract_id", "") for row in contract_rows}

    for row in read_registry_rows(root / "source_registry.csv"):
        path = row.get("path", "")
        if path and not resolve_registered_path(path).exists():
            messages.append(f"{root / 'source_registry.csv'}: {row.get('source_id')}: missing source {path}")

    for row in read_registry_rows(root / "derivative_registry.csv"):
        derivative_id = row.get("derivative_id", "")
        path = row.get("path", "")
        status = row.get("status", "")
        if status in {"canonical", "canonical_draft"}:
            messages.append(f"{root / 'derivative_registry.csv'}: {derivative_id}: generated derivative cannot be {status}")
        if not row.get("source_ids", "").strip():
            messages.append(f"{root / 'derivative_registry.csv'}: {derivative_id}: missing source_ids")
        if path and not resolve_registered_path(path).exists():
            messages.append(f"{root / 'derivative_registry.csv'}: {derivative_id}: missing derivative {path}")

    config_paths: set[Path] = set()
    for row in read_registry_rows(root / "config_source_registry.csv"):
        path = resolve_registered_path(row.get("path", ""))
        config_paths.add(path.resolve())
        if not path.exists():
            messages.append(f"{root / 'config_source_registry.csv'}: {row.get('config_id')}: missing config {row.get('path')}")
        contract_id = row.get("validation_contract_id", "")
        if contract_id and contract_id not in contract_ids:
            messages.append(f"{root / 'config_source_registry.csv'}: {row.get('config_id')}: missing contract {contract_id}")

    control_paths: set[Path] = set()
    for row in read_registry_rows(root / "control_record_registry.csv"):
        path = resolve_registered_path(row.get("path", ""))
        control_paths.add(path.resolve())
        if not path.exists():
            messages.append(f"{root / 'control_record_registry.csv'}: {row.get('control_record_id')}: missing control record {row.get('path')}")
        contract_id = row.get("validation_contract_id", "")
        if contract_id and contract_id not in contract_ids:
            messages.append(f"{root / 'control_record_registry.csv'}: {row.get('control_record_id')}: missing contract {contract_id}")

    contract_paths: set[Path] = set()
    for row in contract_rows:
        path = resolve_registered_path(row.get("path", ""))
        contract_paths.add(path.resolve())
        if not path.exists():
            messages.append(f"{root / 'validation_contract_registry.csv'}: {row.get('contract_id')}: missing contract file {row.get('path')}")

    for path in sorted(Path(".").glob("configs/**/*.toml")):
        if path.resolve() not in config_paths:
            messages.append(f"{path}: TOML configuration source missing config registry row")
    pyproject = Path("pyproject.toml").resolve()
    if pyproject.exists() and pyproject not in config_paths:
        messages.append("pyproject.toml: TOML configuration source missing config registry row")

    for path in sorted(Path("control_records").glob("**/*.yaml")):
        if path.resolve() not in control_paths:
            messages.append(f"{path}: YAML control record missing control registry row")

    for path in sorted(Path("schemas/contracts").glob("*.schema.json")):
        if path.resolve() not in contract_paths:
            messages.append(f"{path}: JSON Schema contract missing validation contract registry row")

    known_layers = _known_system_layers(root / "system_layer_registry.csv")
    known_roles = _known_roles(root / "role_registry.csv")
    known_skills = _load_skill_ids() | _known_proposed_skill_ids(root / "core_skill_proposal_registry.csv")
    lifecycle_statuses = {
        row.get("status_name", "")
        for row in read_registry_rows(root / "skill_lifecycle_status_registry.csv")
        if row.get("status_name")
    }

    for row in read_registry_rows(root / "role_registry.csv"):
        role_id = row.get("role_id", "")
        messages.extend(_check_layer_scope(f"{root / 'role_registry.csv'}: {role_id}", row.get("system_layer_scope", ""), known_layers))
        for field_name in ("required_skills", "optional_skills", "forbidden_skills"):
            for skill_id in _split_selectors(row.get(field_name, "")):
                if skill_id not in known_skills:
                    messages.append(f"{root / 'role_registry.csv'}: {role_id}: {field_name} references unknown skill {skill_id!r}")

    for row in read_registry_rows(root / "role_skill_crosswalk.csv"):
        crosswalk_id = row.get("crosswalk_id", "")
        role_id = row.get("role_id", "")
        skill_id = row.get("skill_id", "")
        if role_id not in known_roles:
            messages.append(f"{root / 'role_skill_crosswalk.csv'}: {crosswalk_id}: unknown role_id {role_id!r}")
        if skill_id not in known_skills:
            messages.append(f"{root / 'role_skill_crosswalk.csv'}: {crosswalk_id}: unknown skill_id {skill_id!r}")
        messages.extend(_check_layer_scope(f"{root / 'role_skill_crosswalk.csv'}: {crosswalk_id}", row.get("system_layer_scope", ""), known_layers))
        evidence_path = resolve_registered_path(row.get("evidence_path", ""))
        if not evidence_path.exists():
            messages.append(f"{root / 'role_skill_crosswalk.csv'}: {crosswalk_id}: missing evidence_path {evidence_path}")

    for row in read_registry_rows(root / "role_execution_binding_registry.csv"):
        binding_id = row.get("binding_id", "")
        if row.get("role_id", "") not in known_roles:
            messages.append(f"{root / 'role_execution_binding_registry.csv'}: {binding_id}: unknown role_id {row.get('role_id')!r}")

    for row in read_registry_rows(root / "artifact_contract_registry.csv"):
        artifact_id = row.get("artifact_contract_id", "")
        messages.extend(_unknown_roles_message(root / "artifact_contract_registry.csv", artifact_id, "producer_role_ids", row.get("producer_role_ids", ""), known_roles))
        messages.extend(_unknown_roles_message(root / "artifact_contract_registry.csv", artifact_id, "consumer_role_ids", row.get("consumer_role_ids", ""), known_roles))
        messages.extend(_check_layer_scope(f"{root / 'artifact_contract_registry.csv'}: {artifact_id}", row.get("system_layer_scope", ""), known_layers))
        contract_id = row.get("validation_contract_id", "").strip()
        if contract_id and contract_id not in contract_ids:
            messages.append(f"{root / 'artifact_contract_registry.csv'}: {artifact_id}: unknown validation_contract_id {contract_id!r}")

    for row in read_registry_rows(root / "discovery_record_registry.csv"):
        discovery_id = row.get("discovery_record_id", "")
        discovery_path = resolve_registered_path(row.get("path", ""))
        if not discovery_path.exists():
            messages.append(f"{root / 'discovery_record_registry.csv'}: {discovery_id}: missing discovery record {row.get('path')}")
        if row.get("subject_layer", "") not in known_layers:
            messages.append(f"{root / 'discovery_record_registry.csv'}: {discovery_id}: unknown subject_layer {row.get('subject_layer')!r}")

    for row in read_registry_rows(root / "core_skill_proposal_registry.csv"):
        proposal_id = row.get("proposal_id", "")
        if row.get("core_or_project_specific") != "core":
            messages.append(f"{root / 'core_skill_proposal_registry.csv'}: {proposal_id}: core_or_project_specific must be core")
        messages.extend(_unknown_roles_message(root / "core_skill_proposal_registry.csv", proposal_id, "required_by_roles", row.get("required_by_roles", ""), known_roles))

    for skill_id, lifecycle in {**_load_product_skill_lifecycle(), **_load_runtime_skill_lifecycle()}.items():
        if lifecycle and lifecycle not in lifecycle_statuses:
            messages.append(f"skill lifecycle: {skill_id}: unknown lifecycle status {lifecycle!r}")

    return ValidationResult(not messages, messages or [f"{root}: registry graph validation passed"])


def validate_metrics_script(path: str | Path) -> ValidationResult:
    script = Path(path)
    if not script.exists():
        return ValidationResult(False, [f"{script}: missing metrics script"])
    proc = subprocess.run(
        [sys.executable, str(script), "--help"],
        text=True,
        capture_output=True,
        check=False,
    )
    output = proc.stdout.strip() or proc.stderr.strip() or f"{script}: --help produced no output"
    if proc.returncode != 0:
        return ValidationResult(False, [output])
    return ValidationResult(True, [f"{script}: metrics script --help validation passed"])


def print_result(result: ValidationResult) -> int:
    for message in result.messages:
        print(message)
    return 0 if result.ok else 1
