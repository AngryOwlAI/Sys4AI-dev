"""Discovery record validation helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .validators import ValidationResult
from .yaml_io import load_yaml


DEFAULT_SCHEMA_PATH = Path("schemas/discovery_record.schema.yaml")

BASELINE_REQUIREMENT_ID_RE = re.compile(r"\b(?:REQ|NFR)-\d{3,}\b")
MARKDOWN_HEADING_RE = re.compile(
    r"^\s{0,3}(?P<level>#{1,6})\s+(?P<title>.+?)\s*(?:#+\s*)?$",
    re.MULTILINE,
)

FALLBACK_REQUIRED_SECTIONS = [
    "Authority Notice",
    "System Intent Profile",
    "Needs",
    "Stakeholders And Roles",
    "System Boundary",
    "As-Is State",
    "To-Be State",
    "Operational Scenarios And ConOps Seeds",
    "Candidate Requirements",
    "Architecture Drivers",
    "Interface Candidates",
    "Verification And Validation Seeds",
    "Evidence Register",
    "Assumptions, Risks, And Constraints",
    "Open Questions",
    "Downstream Routing Recommendation",
    "Completion Evidence",
]

FORBIDDEN_AUTHORITY_PHRASES = [
    "canonical requirements baseline",
    "approved requirements baseline",
    "baselined requirement",
]

AUTHORITY_GUARD_PHRASES = [
    "not a canonical",
    "not canonical",
    "not an approved",
    "not approved",
    "not a baselined",
    "not baselined",
    "must not",
    "does not",
    "do not",
    "unless promoted",
    "until promoted",
    "without promotion",
]


def _normalize_heading(title: str) -> str:
    title = title.strip().strip("#").strip()
    title = re.sub(r"^\d+(?:\.\d+)*\.\s+", "", title)
    return " ".join(title.casefold().split())


def _section_titles(text: str) -> set[str]:
    return {_normalize_heading(match.group("title")) for match in MARKDOWN_HEADING_RE.finditer(text)}


def _section_body(text: str, section: str) -> str:
    wanted = _normalize_heading(section)
    matches = list(MARKDOWN_HEADING_RE.finditer(text))
    for index, match in enumerate(matches):
        if _normalize_heading(match.group("title")) != wanted:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[start:end]
    return ""


def _load_contract(schema_path: str | Path) -> dict[str, Any]:
    target = Path(schema_path)
    if not target.exists():
        return {}
    data = load_yaml(target)
    return data if isinstance(data, dict) else {}


def _required_sections(contract: dict[str, Any]) -> list[str]:
    sections = contract.get("required_sections")
    if not isinstance(sections, list):
        return FALLBACK_REQUIRED_SECTIONS
    return [section for section in sections if isinstance(section, str) and section]


def _authority_policy(contract: dict[str, Any]) -> dict[str, Any]:
    policy = contract.get("authority_policy")
    return policy if isinstance(policy, dict) else {}


def _line_is_guarded(line: str) -> bool:
    lower = line.casefold()
    return any(guard in lower for guard in AUTHORITY_GUARD_PHRASES)


def validate_discovery_record(
    path: str | Path,
    schema_path: str | Path = DEFAULT_SCHEMA_PATH,
) -> ValidationResult:
    target = Path(path)
    messages: list[str] = []
    if not target.exists():
        return ValidationResult(False, [f"{target}: missing discovery record"])

    try:
        text = target.read_text(encoding="utf-8")
    except OSError as exc:
        return ValidationResult(False, [f"{target}: cannot read discovery record: {exc}"])

    contract = _load_contract(schema_path)
    headings = _section_titles(text)
    for section in _required_sections(contract):
        if _normalize_heading(section) not in headings:
            messages.append(f"{target}: missing required section {section!r}")

    if "REQ-CAND-" not in text and "NFR-CAND-" not in text:
        messages.append(f"{target}: no candidate requirement IDs found")

    for match in BASELINE_REQUIREMENT_ID_RE.finditer(text):
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if not _line_is_guarded(line):
            messages.append(f"{target}: possible baselined requirement ID found: {match.group(0)!r}")

    authority_body = _section_body(text, "Authority Notice")
    if authority_body:
        authority_lower = authority_body.casefold()
        if not (
            "not a canonical requirements baseline" in authority_lower
            or "draft discovery" in authority_lower
            or "does not baseline requirements" in authority_lower
        ):
            messages.append(f"{target}: authority notice does not clearly mark discovery status")

    policy = _authority_policy(contract)
    default_status = policy.get("default_status")
    if isinstance(default_status, str) and default_status and default_status not in text:
        messages.append(f"{target}: missing expected discovery status marker {default_status!r}")

    source_status = policy.get("source_authority_status")
    if isinstance(source_status, str) and source_status and source_status not in text:
        messages.append(f"{target}: missing expected source authority marker {source_status!r}")

    lowered_lines = text.casefold().splitlines()
    for phrase in FORBIDDEN_AUTHORITY_PHRASES:
        phrase_lower = phrase.casefold()
        for line_number, line in enumerate(lowered_lines, start=1):
            if phrase_lower in line and not _line_is_guarded(line):
                messages.append(
                    f"{target}: possible authority inversion phrase at line {line_number}: {phrase!r}"
                )

    return ValidationResult(not messages, messages or [f"{target}: discovery record validation passed"])
