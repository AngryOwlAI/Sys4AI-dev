"""Focused semantic boundary checks for the canonical Sys4AI PRDs."""

from __future__ import annotations

from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any

from .registry_io import resolve_registered_path
from .toml_io import load_toml
from .validation_semantics import STRUCTURAL_LIMITATION
from .validators import ValidationResult
from .yaml_io import load_yaml


LEGACY_TERMS = ("/continue", "AgentJob", "control_loop")
PHASE0_MARKERS = (
    "Meta-Agentic AI Framework System",
    "Sys4AI Framework Product",
    "Sys4AI Meta-Agent Runtime",
    "Codex App Host Harness",
    "Authorized user",
    "SFA-CORE-LIFE-008",
    "SFA-CORE-PATTERN-005",
    "SFA-CORE-TRACE-001",
    "SFA-VISION-001",
    "SFA-VALUE-008",
    "G-08",
    "Approved Sys4AI vision",
    "Approved Sys4AI core values",
    "DDR-SFADEV-STRATEGIC-BASELINE-G08-001",
    "structural validation",
)
PHASE1_MARKERS = (
    "SFA-P1-INIT-STRAT-005",
    "SFA-P1-INIT-EXEC-003",
    "SFA-P1-INIT-STATE-001",
    "SFA-P1-INIT-STATUS-001",
    "SFA-P1-INIT-STATUS-002",
    "SFA-P1-INIT-SEM-001",
    "SFA-P1-INIT-LIFE-006",
    "SFA-P1-INIT-PATTERN-005",
    "SFA-P1-INIT-HOST-003",
    "SFA-P1-INIT-ARCH-001",
    "Portable Successor Transaction and Historical Packet Provenance",
    "structural validation",
)
PHASE2_ADDENDUM_MARKERS = (
    "SFA-P2-ADD-STRAT-001",
    "SFA-P2-ADD-STRAT-002",
    "SFA-P2-ADD-APPROVAL-001",
    "SFA-P2-ADD-HOST-001",
    "SFA-P2-ADD-PATTERN-001",
    "SFA-P2-ADD-LIFE-001",
    "SFA-P2-ADD-EXEC-001",
    "SFA-P2-ADD-STATE-001",
    "SFA-P2-ADD-TRACE-001",
    "SFA-P2-ADD-PACKAGE-001",
    "SFA-P2-ADD-SEM-001",
    "SFA-P2-ADD-FLOW-001",
    "SFA-P2-ADD-SAFETY-001",
    "validated_prototype",
    "Structural validation does not prove strategic quality",
)


def validate_prd_semantics(
    phase0_prd: str | Path = "PRDs/Sys4AI_phase-0_product_system_design_prd.md",
    phase1_prd: str | Path = "PRDs/Sys4AI_phase-1_implementation_initialization_prd.md",
    phase2_addendum: str | Path = "PRDs/Sys4AI_phase-2_strategic_baseline_addendum.md",
    *,
    capability_manifest: str | Path = "configs/capability_migration.toml",
    program_state: str | Path = "control_records/program_state.yaml",
    g08_decision: str | Path = "control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G08-001.yaml",
    modules_root: str | Path = "../PRDs/modules",
    repository_root: str | Path | None = None,
) -> ValidationResult:
    """Validate canonical identity, execution, lifecycle, and authority semantics."""

    phase0 = resolve_registered_path(str(phase0_prd))
    phase1 = resolve_registered_path(str(phase1_prd))
    phase2 = resolve_registered_path(str(phase2_addendum))
    messages: list[str] = []
    texts: dict[Path, str] = {}
    for path, markers in (
        (phase0, PHASE0_MARKERS),
        (phase1, PHASE1_MARKERS),
        (phase2, PHASE2_ADDENDUM_MARKERS),
    ):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            messages.append(f"{path}: cannot read canonical PRD: {exc}")
            continue
        texts[path] = text
        for marker in markers:
            if marker not in text:
                messages.append(f"{path}: missing canonical semantic marker {marker!r}")
        messages.extend(_legacy_reference_context_errors(path, text))

    phase0_text = texts.get(phase0)
    if phase0_text is not None:
        messages.extend(_validate_strategic_approval_state(phase0_text, program_state, g08_decision))

    manifest_path = resolve_registered_path(str(capability_manifest))
    try:
        manifest = load_toml(manifest_path)
    except RuntimeError as exc:
        messages.append(str(exc))
        manifest = {}
    root = Path(repository_root).resolve() if repository_root else _repository_root(phase0)
    classifications = manifest.get("classifications", []) if isinstance(manifest, dict) else []
    for path, text in texts.items():
        if not any(term.casefold() in text.casefold() for term in LEGACY_TERMS):
            continue
        try:
            relative = path.resolve().relative_to(root).as_posix()
        except ValueError:
            relative = path.as_posix()
        classification = _classification(relative, classifications)
        if classification is None:
            messages.append(f"{path}: active removed command reference is not classified")
            continue
        state = classification.get("state")
        disposition = str(classification.get("disposition", "")).casefold()
        if state not in {"active_valid", "legacy_compatibility", "historical", "authority_deferred"}:
            messages.append(f"{path}: legacy reference classification {state!r} is not allowed")
        if not any(word in disposition for word in ("historical", "retired", "compatibility", "removed", "absence")):
            messages.append(f"{path}: legacy reference disposition does not state its non-active semantics")

    module_root = resolve_registered_path(str(modules_root))
    if module_root.exists():
        for module in sorted(module_root.glob("*.md")):
            text = module.read_text(encoding="utf-8")
            if "**Source authority status:** derivative_draft" not in text:
                messages.append(f"{module}: derivative module lacks derivative_draft authority status")
            if "**Promotion status:** not_promoted" not in text:
                messages.append(f"{module}: derivative module lacks not_promoted status")

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            f"canonical PRD semantic validation passed ({phase0.name}; {phase1.name}; {phase2.name})",
            STRUCTURAL_LIMITATION,
        ],
    )


def _validate_strategic_approval_state(
    phase0_text: str,
    program_state: str | Path,
    g08_decision: str | Path,
) -> list[str]:
    """Bind post-TX-18 approved PRD status to accountable human decision evidence."""

    state_path = resolve_registered_path(str(program_state))
    try:
        state = load_yaml(state_path)
    except RuntimeError as exc:
        return [str(exc)]
    if state.get("current_phase") not in {
        "strategic_baseline_migration_after_TX_18",
        "strategic_baseline_migration_after_TX_19",
        "strategic_baseline_migration_after_TX_20",
    }:
        return []

    messages: list[str] = []
    required_markers = (
        "### 5.1 Approved Sys4AI vision",
        "| Content approval status | `approved`; accepted at `G-08`",
        "### 5.2 Approved Sys4AI core values",
        "### 6.1.1 Active vision and core-values requirements",
        "`G-08` is accepted by `DDR-SFADEV-STRATEGIC-BASELINE-G08-001`",
    )
    for marker in required_markers:
        if marker not in phase0_text:
            messages.append(f"post-TX-18 Phase 0 is missing approved strategic marker {marker!r}")

    decision_path = resolve_registered_path(str(g08_decision))
    try:
        decision = load_yaml(decision_path)
    except RuntimeError as exc:
        messages.append(str(exc))
        return messages

    if decision.get("director_decision_id") != "DDR-SFADEV-STRATEGIC-BASELINE-G08-001":
        messages.append(f"{decision_path}: unexpected G-08 Director Decision ID")
    if decision.get("decision_status") != "completed":
        messages.append(f"{decision_path}: G-08 Director Decision must be completed")

    human = decision.get("human_authorization")
    human = human if isinstance(human, dict) else {}
    principal = str(human.get("principal_name", "")).casefold()
    if not principal or any(term in principal for term in ("model", "agent", "runtime", "assistant")):
        messages.append(f"{decision_path}: G-08 approval principal must be an accountable human")
    if human.get("model_self_approval") is not False:
        messages.append(f"{decision_path}: G-08 must explicitly reject model self-approval")
    if not human.get("approval_evidence") or not human.get("approval_scope"):
        messages.append(f"{decision_path}: G-08 requires explicit human approval evidence and scope")

    selected = decision.get("selected_route")
    selected = selected if isinstance(selected, dict) else {}
    if selected.get("route_id") != "approve_exact_strategic_baseline_with_bounded_TX17_acceptance":
        messages.append(f"{decision_path}: G-08 selected route does not match the approved bounded route")

    reviewed = decision.get("reviewed_content")
    reviewed = reviewed if isinstance(reviewed, dict) else {}
    vision = reviewed.get("vision") if isinstance(reviewed.get("vision"), dict) else {}
    values = reviewed.get("core_values") if isinstance(reviewed.get("core_values"), dict) else {}
    expected_values = {f"SFA-VALUE-{index:03d}" for index in range(1, 9)}
    if vision.get("vision_id") != "SFA-VISION-001" or vision.get("disposition") != "approved":
        messages.append(f"{decision_path}: G-08 must approve SFA-VISION-001 exactly")
    if values.get("disposition") != "approved" or set(values.get("value_ids", [])) != expected_values:
        messages.append(f"{decision_path}: G-08 must approve exactly SFA-VALUE-001 through SFA-VALUE-008")

    boundary = decision.get("authority_boundary")
    boundary = boundary if isinstance(boundary, dict) else {}
    if boundary.get("accepts_gate_G_08") is not True:
        messages.append(f"{decision_path}: authority boundary does not accept G-08")
    forbidden_true = (
        "may_claim_G_07_host_verification",
        "may_claim_production_readiness",
        "may_grant_operational_authority",
        "may_claim_broad_stakeholder_consensus",
        "may_claim_domain_truth_or_domain_acceptance",
        "may_expand_host_project_or_transaction_permissions",
        "may_treat_values_as_permission_sources",
        "may_claim_G_10_final_acceptance",
    )
    for field in forbidden_true:
        if boundary.get(field) is not False:
            messages.append(f"{decision_path}: G-08 authority boundary must keep {field}=false")

    summary = state.get("capability_status_summary")
    summary = summary if isinstance(summary, dict) else {}
    if summary.get("strategic_approval") != "accepted_G_08":
        messages.append(f"{state_path}: post-TX-18 state must record strategic_approval=accepted_G_08")
    return messages


def _classification(relative: str, values: Any) -> dict[str, Any] | None:
    if not isinstance(values, list):
        return None
    for item in sorted(
        (value for value in values if isinstance(value, dict)),
        key=lambda value: value.get("priority", 0),
    ):
        if relative in item.get("paths", []):
            return item
        if any(fnmatchcase(relative, glob) for glob in item.get("path_globs", [])):
            return item
    return None


def _legacy_reference_context_errors(path: Path, text: str) -> list[str]:
    qualifiers = (
        "historical",
        "retired",
        "removed",
        "optional-profile",
        "optional profile",
        "compatibility",
        "not restore",
        "does not authorize",
        "prohibit",
        "absence",
    )
    lines = text.splitlines()
    heading_stack: dict[int, str] = {}
    messages: list[str] = []
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            if level and stripped[level :].startswith(" "):
                heading_stack = {key: value for key, value in heading_stack.items() if key < level}
                heading_stack[level] = stripped[level + 1 :]
        if not any(term.casefold() in line.casefold() for term in LEGACY_TERMS):
            continue
        context = " ".join(
            [*heading_stack.values(), *lines[max(0, index - 2) : min(len(lines), index + 3)]]
        ).casefold()
        if not any(qualifier in context for qualifier in qualifiers):
            messages.append(
                f"{path}:{index + 1}: active removed command reference lacks explicit historical, removed, or optional-profile context"
            )
    return messages


def _repository_root(path: Path) -> Path:
    resolved = path.resolve()
    for parent in (resolved.parent, *resolved.parents):
        if (parent / "Sys4AI").is_dir() and (parent / "PRDs").is_dir():
            return parent
    return Path.cwd().resolve()
