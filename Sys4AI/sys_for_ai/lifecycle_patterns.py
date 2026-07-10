"""Lifecycle, coordination-pattern, and maturity consistency validation."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any, Mapping

from .registry_io import resolve_registered_path
from .validation_semantics import STRUCTURAL_LIMITATION
from .validators import ValidationResult


LIFECYCLE_STAGES = ("Design", "Develop", "Implement", "Test", "Run", "Maintain", "Improve", "Retire")
COORDINATION_PATTERNS = (
    "linear_workflow",
    "goal_directed_autonomous_agent",
    "role_based_multi_agent",
    "production_orchestration",
    "hybrid",
)
OPERATIONAL_MATURITY = (
    "concept",
    "prototype",
    "validated_prototype",
    "production_candidate",
    "production_approved",
    "operational",
    "maintenance",
    "retired",
)
ALLOWED_TRANSITIONS = {
    "Design": {"Develop"},
    "Develop": {"Design", "Implement"},
    "Implement": {"Design", "Develop", "Test"},
    "Test": {"Design", "Develop", "Implement", "Run"},
    "Run": {"Maintain", "Improve", "Retire"},
    "Maintain": {"Test", "Run", "Improve", "Retire"},
    "Improve": {"Design", "Develop", "Implement", "Test"},
    "Retire": set(),
}
STAGE_FIELDS = (
    "Entry criteria",
    "Required inputs",
    "Responsible and approving roles",
    "Permission requirements",
    "Activities",
    "Expected outputs",
    "Required evidence",
    "Exit criteria and primary gate",
    "Failure or degraded mode",
    "Allowed transitions",
    "Rollback or return",
    "Monitoring and review cadence",
)
PATTERN_DECISION_FIELDS = (
    "target_problem",
    "system_of_interest",
    "coordination_pattern",
    "operational_maturity",
    "predictability",
    "role_specialization",
    "autonomy",
    "interfaces",
    "communication_protocol",
    "task_and_state_model",
    "monitoring",
    "failure_and_degraded_behavior",
    "reliability_and_recovery",
    "security_and_data_boundaries",
    "promotion_criteria",
    "rejected_alternatives",
    "rationale",
    "owner",
    "review_triggers",
    "supersession",
)
PRODUCTION_EVIDENCE_FIELDS = (
    "evaluation",
    "security",
    "integration",
    "ownership",
    "rollback",
    "monitoring",
    "incident_response",
    "service_threshold",
    "human_approval",
)


def validate_lifecycle_and_patterns(
    prd_path: str | Path = "PRDs/Sys4AI_phase-0_product_system_design_prd.md",
) -> ValidationResult:
    """Validate the accepted Phase 0 lifecycle and pattern baseline."""

    target = resolve_registered_path(str(prd_path))
    try:
        text = target.read_text(encoding="utf-8")
    except OSError as exc:
        return ValidationResult(False, [f"{target}: cannot read lifecycle baseline: {exc}"])

    messages: list[str] = []
    for stage in LIFECYCLE_STAGES:
        section = _stage_section(text, stage)
        if not section:
            messages.append(f"{target}: missing lifecycle stage {stage}")
            continue
        for field in STAGE_FIELDS:
            if not re.search(rf"^\|\s*{re.escape(field)}\s*\|", section, re.MULTILINE):
                messages.append(f"{target}: lifecycle stage {stage} missing contract field {field!r}")

    for value in (*COORDINATION_PATTERNS, *OPERATIONAL_MATURITY):
        if f"`{value}`" not in text:
            messages.append(f"{target}: missing controlled lifecycle/pattern value {value!r}")

    required_phrases = (
        "No transition may skip required test, verification, validation, evaluation, security, permission, release, or human-approval gates.",
        "Testing shall be both a named lifecycle stage and a cross-cutting gate",
        "Improvement shall be evidence-driven",
        "Production target systems shall define retirement, archival, data disposition, credential and authority withdrawal",
        "Every target system requires an Agentic System Pattern Decision.",
        "A prototype shall not become operational without evaluation, security, integration, ownership, rollback, monitoring, incident-response, and accountable production-approval evidence.",
    )
    for phrase in required_phrases:
        if phrase not in text:
            messages.append(f"{target}: missing lifecycle or pattern invariant {phrase!r}")

    pattern_section = _between(text, "#### 6.2.5 Candidate Agentic System Pattern Decision contract", "### 6.3")
    decision_labels = (
        "Target problem and system of interest",
        "Coordination pattern",
        "Operational maturity",
        "Predictability versus open-endedness",
        "Single-agent versus multi-agent need",
        "Role specialization and authority",
        "Autonomy level",
        "APIs, databases, and business workflows",
        "Communication protocol",
        "Task and state model",
        "Monitoring and observability",
        "Failure and degraded-mode behavior",
        "Reliability and recovery",
        "Security and data boundaries",
        "Prototype-to-production criteria",
        "Alternatives rejected and rationale",
    )
    for label in decision_labels:
        if not re.search(rf"^\|\s*{re.escape(label)}\s*\|", pattern_section, re.MULTILINE):
            messages.append(f"{target}: pattern decision missing field {label!r}")

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            f"{target}: lifecycle and pattern validation passed "
            f"({len(LIFECYCLE_STAGES)} stages; {len(COORDINATION_PATTERNS)} patterns; "
            f"{len(OPERATIONAL_MATURITY)} maturity states)",
            STRUCTURAL_LIMITATION,
        ],
    )


def validate_transition(source: str, target: str, evidence: Mapping[str, Any]) -> ValidationResult:
    """Validate one requested lifecycle transition against the controlled graph."""

    messages: list[str] = []
    if source not in ALLOWED_TRANSITIONS:
        messages.append(f"unknown lifecycle source stage {source!r}")
    elif target not in ALLOWED_TRANSITIONS[source]:
        messages.append(f"invalid lifecycle transition {source!r} -> {target!r}")
    for field in ("authority", "verification", "rollback", "next_state_owner"):
        if not evidence.get(field):
            messages.append(f"lifecycle transition {source!r} -> {target!r} missing {field} evidence")
    if target == "Run" and not evidence.get("human_approval"):
        messages.append("Run transition requires accountable human approval evidence")
    return ValidationResult(not messages, messages or [f"lifecycle transition {source} -> {target} passed"])


def validate_pattern_decision(decision: Mapping[str, Any]) -> ValidationResult:
    """Validate a typed pattern decision fixture without inferring maturity."""

    messages = [f"pattern decision missing {field}" for field in PATTERN_DECISION_FIELDS if not decision.get(field)]
    pattern = decision.get("coordination_pattern")
    maturity = decision.get("operational_maturity")
    if pattern not in COORDINATION_PATTERNS:
        messages.append(f"unknown coordination_pattern {pattern!r}")
    if maturity not in OPERATIONAL_MATURITY:
        messages.append(f"unknown operational_maturity {maturity!r}")
    if maturity in {"production_approved", "operational", "maintenance"}:
        evidence = decision.get("production_evidence")
        evidence = evidence if isinstance(evidence, Mapping) else {}
        for field in PRODUCTION_EVIDENCE_FIELDS:
            if not evidence.get(field):
                messages.append(f"production maturity requires {field} evidence")
    return ValidationResult(not messages, messages or ["pattern decision validation passed"])


def _stage_section(text: str, stage: str) -> str:
    match = re.search(rf"^#####\s+{re.escape(stage)}\s*$", text, re.MULTILINE)
    if match is None:
        return ""
    next_heading = re.search(r"^#{1,5}\s+", text[match.end() :], re.MULTILINE)
    if next_heading is None:
        return text[match.end() :]
    return text[match.end() : match.end() + next_heading.start()]


def _between(text: str, start: str, next_marker: str) -> str:
    start_index = text.find(start)
    if start_index < 0:
        return ""
    content_start = start_index + len(start)
    end_index = text.find(next_marker, content_start)
    return text[content_start:] if end_index < 0 else text[content_start:end_index]
