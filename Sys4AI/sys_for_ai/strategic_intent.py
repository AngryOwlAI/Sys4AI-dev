"""Focused validation for target vision and core-values Markdown artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
from pathlib import Path
import re
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
import yaml

from .jsonschema_io import check_schema, load_json
from .registry_io import read_registry_rows, resolve_registered_path
from .validation_semantics import STRUCTURAL_LIMITATION
from .validators import ValidationResult


VISION_HEADINGS = (
    "Target Vision Statement",
    "Metadata",
    "Target System And Subject Layer",
    "Authority And Non-Anthropomorphism Notice",
    "Mission Versus Vision",
    "Future-State Statement",
    "Intended Users And Beneficiaries",
    "Desired Condition And Impact",
    "Time Horizon",
    "Scope Exclusions And Non-Goals",
    "Success Signals",
    "Source Evidence And RDR Candidates",
    "Assumptions Tensions And Open Questions",
    "Approval Principal And Evidence",
    "Independent State Model",
    "Waiver And Baseline Exception",
    "Impact Analysis",
    "Revision Version Hash And Supersession",
)

VALUES_HEADINGS = (
    "Target Core Values",
    "Metadata And Target Identity",
    "Governance Floor",
    "Stable Value Inventory",
    "Per-Value Commitment And Rationale",
    "Positive And Prohibited Behaviors",
    "Decision Tests",
    "Design And Operational Implications",
    "Testing And Evaluation Implications",
    "Conflict And Precedence Rules",
    "Source Owner And Evidence",
    "Inherited Sys4AI Constraints",
    "Target-Specific Commitments",
    "Known Tensions And Escalation",
    "Downstream Trace",
    "Approval And Review Cadence",
    "Waiver And Baseline Exception",
    "Impact Analysis",
    "Revision Version Hash And Supersession",
)

_SCHEMA_BY_TYPE = {
    "target_vision_statement": "schemas/contracts/target_vision_statement.schema.json",
    "target_core_values": "schemas/contracts/target_core_values.schema.json",
}


@dataclass(frozen=True)
class StrategicIntentArtifact:
    path: Path
    metadata: dict[str, Any]
    body: str
    headings: tuple[str, ...]


def validate_strategic_intent(
    path: str | Path | None = None,
    *,
    source_registry: str | Path = "registries/source_registry.csv",
    today: date | None = None,
) -> ValidationResult:
    """Validate one artifact, one pair directory, or all registered examples/templates."""

    targets = _discover_targets(path)
    if not targets:
        label = path if path is not None else "registered strategic-intent surfaces"
        return ValidationResult(False, [f"{label}: no strategic-intent artifacts found"])

    messages: list[str] = []
    artifacts: list[StrategicIntentArtifact] = []
    for target in targets:
        artifact, errors = _load_artifact(target)
        messages.extend(errors)
        if artifact is None:
            continue
        artifacts.append(artifact)
        messages.extend(_validate_artifact(artifact, today or date.today()))

    messages.extend(_validate_pair_and_id_consistency(artifacts, path))
    if path is None:
        messages.extend(_validate_registered_surfaces(targets, source_registry))

    if messages:
        return ValidationResult(False, sorted(dict.fromkeys(messages)))
    return ValidationResult(
        True,
        [
            f"strategic-intent validation passed ({len(artifacts)} artifacts; "
            f"{sum(item.metadata.get('artifact_type') == 'target_vision_statement' for item in artifacts)} vision; "
            f"{sum(item.metadata.get('artifact_type') == 'target_core_values' for item in artifacts)} values)",
            STRUCTURAL_LIMITATION,
        ],
    )


def _discover_targets(path: str | Path | None) -> list[Path]:
    if path is None:
        values = [
            resolve_registered_path("templates/governance/target-vision-statement-template.md"),
            resolve_registered_path("templates/governance/target-core-values-template.md"),
        ]
        examples = resolve_registered_path("examples/strategic_intent")
        if examples.exists():
            values.extend(examples.rglob("*.md"))
        return sorted(item for item in values if item.name != "README.md")

    target = resolve_registered_path(str(path))
    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(
            item
            for item in target.rglob("*.md")
            if item.name in {"vision-statement.md", "core-values.md"}
        )
    return []


def _load_artifact(path: Path) -> tuple[StrategicIntentArtifact | None, list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"{path}: cannot read artifact: {exc}"]
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, [f"{path}: missing opening YAML front-matter delimiter"]
    closing = next((index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if closing is None:
        return None, [f"{path}: missing closing YAML front-matter delimiter"]
    try:
        metadata = yaml.safe_load("".join(lines[1:closing]))
    except yaml.YAMLError as exc:
        return None, [f"{path}: invalid YAML front matter: {exc}"]
    if not isinstance(metadata, dict):
        return None, [f"{path}: YAML front matter must be a mapping"]
    body = "".join(lines[closing + 1 :])
    headings = tuple(
        match.group(1).strip()
        for line in body.splitlines()
        if (match := re.fullmatch(r"#{1,6}\s+(.+?)\s*", line))
    )
    return StrategicIntentArtifact(path, metadata, body, headings), []


def _validate_artifact(artifact: StrategicIntentArtifact, today: date) -> list[str]:
    path = artifact.path
    metadata = artifact.metadata
    artifact_type = metadata.get("artifact_type")
    expected_headings = (
        VISION_HEADINGS if artifact_type == "target_vision_statement" else VALUES_HEADINGS
        if artifact_type == "target_core_values"
        else ()
    )
    messages: list[str] = []
    if not expected_headings:
        return [f"{path}: unknown artifact_type {artifact_type!r}"]
    for heading in expected_headings:
        if heading not in artifact.headings:
            messages.append(f"{path}: missing required heading {heading!r}")

    if _is_template(path):
        if metadata.get("content_approval_state") != "candidate":
            messages.append(f"{path}: template must remain candidate")
        if metadata.get("source_hash") != "pending":
            messages.append(f"{path}: template source_hash must remain pending")
        return messages

    messages.extend(_validate_against_schema(path, metadata, artifact_type))
    state = str(metadata.get("content_approval_state", ""))
    approval = metadata.get("approval") if isinstance(metadata.get("approval"), dict) else {}
    approved_by = str(approval.get("approved_by") or "")
    if _is_model_principal(approved_by):
        messages.append(f"{path}: approved_by must be an accountable non-model principal")
    if state == "approved":
        if approval.get("status") != "approved":
            messages.append(f"{path}: approved content requires approval.status='approved'")
        for field in ("approved_by", "principal_role", "approved_at", "approval_evidence"):
            if not approval.get(field):
                messages.append(f"{path}: approved content requires approval.{field}")
        if approval.get("approved_at") and _parse_date(approval.get("approved_at")) is None:
            messages.append(f"{path}: approved content requires a valid approval date")
        expected_hash = _source_hash(path)
        if metadata.get("source_hash") != f"sha256:{expected_hash}":
            messages.append(f"{path}: stale source_hash; expected sha256:{expected_hash}")
        impact = metadata.get("impact_analysis")
        if not isinstance(impact, dict) or impact.get("state") not in {"complete", "not_applicable"}:
            messages.append(f"{path}: approved content requires completed or not-applicable impact analysis")

    waiver = metadata.get("waiver")
    if isinstance(waiver, dict) and waiver.get("status") == "active":
        expiry = _parse_date(waiver.get("expiry"))
        if expiry is None:
            messages.append(f"{path}: active waiver requires a valid expiry date")
        elif expiry < today:
            messages.append(f"{path}: active waiver expired on {expiry.isoformat()}")

    supersession = metadata.get("supersession")
    if isinstance(supersession, dict):
        if supersession.get("state") == "current" and supersession.get("superseded_by"):
            messages.append(f"{path}: superseded document cannot remain active")
        if supersession.get("state") == "superseded" and not supersession.get("superseded_by"):
            messages.append(f"{path}: superseded document requires superseded_by")

    if artifact_type == "target_core_values":
        value_ids = metadata.get("value_ids") if isinstance(metadata.get("value_ids"), list) else []
        for value_id in value_ids:
            if artifact.body.count(str(value_id)) < 2:
                messages.append(f"{path}: value {value_id!r} lacks inventory and behavior trace")
        governance = _section(artifact.body, "Governance Floor")
        governance_floor = governance.casefold()
        required_floor_terms = ("law", "safety", "security", "privacy", "permission", "human approval")
        if (
            any(term not in governance_floor for term in required_floor_terms)
            or not any(
                phrase in governance_floor
                for phrase in ("outrank these values", "outrank the candidates")
            )
        ):
            messages.append(f"{path}: governance floor must prevent value-based permission expansion")
        if not _section(artifact.body, "Decision Tests").strip():
            messages.append(f"{path}: every value set requires decision tests")
        for heading in ("Inherited Sys4AI Constraints", "Target-Specific Commitments"):
            if not _section(artifact.body, heading).strip():
                messages.append(f"{path}: missing inherited-versus-target-specific value content in {heading!r}")
    else:
        if not _section(artifact.body, "Source Evidence And RDR Candidates").strip():
            messages.append(f"{path}: vision requires source evidence")
    return messages


def _validate_against_schema(path: Path, metadata: dict[str, Any], artifact_type: str) -> list[str]:
    schema_path = resolve_registered_path(_SCHEMA_BY_TYPE[artifact_type])
    common_path = resolve_registered_path("schemas/contracts/strategic_intent_common.schema.json")
    try:
        schema = load_json(schema_path)
        common = load_json(common_path)
    except RuntimeError as exc:
        return [str(exc)]
    messages = [f"{path}: invalid schema: {error}" for error in check_schema(schema)]
    if messages:
        return messages
    registry = Registry().with_resource(str(common["$id"]), Resource.from_contents(common))
    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(metadata), key=lambda error: (list(error.path), error.message))
    return [f"{path}: {'.'.join(map(str, error.path)) or 'metadata'}: {error.message}" for error in errors]


def _validate_pair_and_id_consistency(
    artifacts: Iterable[StrategicIntentArtifact],
    requested_path: str | Path | None,
) -> list[str]:
    items = list(artifacts)
    messages: list[str] = []
    ids: dict[str, Path] = {}
    pairs: dict[tuple[Path, str], dict[str, StrategicIntentArtifact]] = {}
    for item in items:
        metadata = item.metadata
        primary_ids = [metadata.get("vision_id"), metadata.get("core_values_set_id")]
        primary_ids.extend(metadata.get("value_ids", []) if isinstance(metadata.get("value_ids"), list) else [])
        for raw_id in primary_ids:
            if not raw_id:
                continue
            value = str(raw_id)
            if value in ids:
                messages.append(f"{item.path}: duplicate strategic-intent ID {value!r}; first in {ids[value]}")
            else:
                ids[value] = item.path
        key = (item.path.parent, str(metadata.get("target_system_id", "")))
        pairs.setdefault(key, {})[str(metadata.get("artifact_type"))] = item

    for (directory, target_id), pair in sorted(pairs.items(), key=lambda item: str(item[0])):
        if _is_template(directory):
            continue
        if requested_path is not None and Path(requested_path).suffix:
            continue
        missing = {"target_vision_statement", "target_core_values"} - set(pair)
        if missing:
            messages.append(f"{directory}: target {target_id!r} missing pair artifact(s): {', '.join(sorted(missing))}")
            continue
        states = {item.metadata.get("content_approval_state") for item in pair.values()}
        if len(states) != 1:
            messages.append(f"{directory}: vision and values approval states disagree: {sorted(map(str, states))}")
    return messages


def _validate_registered_surfaces(targets: list[Path], source_registry: str | Path) -> list[str]:
    registry_path = resolve_registered_path(str(source_registry))
    try:
        rows = read_registry_rows(registry_path)
    except OSError as exc:
        return [f"{registry_path}: cannot read source registry: {exc}"]
    registered = [resolve_registered_path(row.get("path", "")) for row in rows if row.get("path")]
    messages: list[str] = []
    for target in targets:
        if not any(target == path or path in target.parents for path in registered):
            messages.append(f"{target}: strategic-intent surface is not registered")
    return messages


def _source_hash(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"^source_hash:.*$", "source_hash: pending", text, count=1, flags=re.MULTILINE)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _section(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    return match.group("body") if match else ""


def _is_template(path: Path) -> bool:
    return "templates" in path.parts or "<" in path.name


def _is_model_principal(value: str) -> bool:
    normalized = value.strip().casefold().replace("_", "-")
    return normalized in {"model", "ai"} or normalized.startswith(("meta-agent", "runtime"))


def _parse_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None
