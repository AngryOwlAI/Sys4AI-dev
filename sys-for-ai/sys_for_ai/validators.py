"""Small deterministic validators for Phase 1 scaffolding."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .yaml_io import load_yaml


@dataclass
class ValidationResult:
    ok: bool
    messages: list[str]

    def extend(self, other: "ValidationResult") -> None:
        self.ok = self.ok and other.ok
        self.messages.extend(other.messages)


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
    "system-definition-interview",
    "system-definition-interview-context-45",
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
        "last_reviewed",
        "notes",
    ],
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
        first_line = path.read_text(encoding="utf-8").splitlines()[0] if path.read_text(encoding="utf-8").splitlines() else ""
        actual = [part.strip() for part in first_line.split(",")]
        if actual != expected_header:
            messages.append(
                f"{path}: header mismatch. Expected {expected_header!r}, found {actual!r}"
            )
    return ValidationResult(not messages, messages or [f"{root}: registry header validation passed"])


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
