"""Fail-closed boundary scanning for retired capability references."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fnmatch import fnmatchcase
import hashlib
from pathlib import Path
import re
from typing import Any

from .jsonschema_io import check_schema, load_json, validate_instance
from .registry_io import resolve_registered_path
from .toml_io import load_toml
from .trace_validation import validate_generalized_trace_semantics
from .validation_semantics import STRUCTURAL_LIMITATION
from .validators import ValidationResult


DEFAULT_MANIFEST_PATH = Path("configs/capability_migration.toml")
DEFAULT_SCHEMA_PATH = Path("Sys4AI/schemas/contracts/capability_migration.schema.json")
MAX_SCANNED_TEXT_BYTES = 2_000_000

@dataclass(frozen=True)
class ClassificationSnapshot:
    """Deterministic retired-reference inventory for one manifest classification."""

    classification_id: str
    files: int
    references: int
    inventory_sha256: str


def capability_inventory_digest(entries: dict[str, Counter[str]]) -> str:
    """Hash normalized path, retired term, and count tuples deterministically."""

    lines = [
        f"{path}\t{term}\t{count}"
        for path, terms in sorted(entries.items())
        for term, count in sorted(terms.items())
    ]
    payload = "\n".join(lines).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_capability_migration(
    manifest_path: str | Path = DEFAULT_MANIFEST_PATH,
    repository_root: str | Path | None = None,
) -> ValidationResult:
    """Validate the controlled G-05 inventory without claiming semantic completion."""

    target = resolve_registered_path(str(manifest_path))
    if not target.exists():
        return ValidationResult(False, [f"{target}: missing capability-migration manifest"])

    try:
        data = load_toml(target)
    except RuntimeError as exc:
        return ValidationResult(False, [str(exc)])

    root = Path(repository_root).resolve() if repository_root else _infer_repository_root(target)
    messages = _validate_manifest_schema(data, root)
    if messages:
        return ValidationResult(False, messages)

    manifest = data["manifest"]
    classifications = sorted(data["classifications"], key=lambda item: item["priority"])
    messages.extend(_validate_classification_contracts(classifications, root))
    messages.extend(_validate_removed_paths(manifest["removed_paths"], root))

    pattern = _legacy_reference_pattern(manifest["legacy_terms"])
    inventories: dict[str, dict[str, Counter[str]]] = {
        item["classification_id"]: {} for item in classifications
    }
    unclassified: list[str] = []

    scan_paths, scan_errors = _scan_paths(manifest, root)
    messages.extend(scan_errors)
    for path in scan_paths:
        relative = path.relative_to(root).as_posix()
        try:
            size = path.stat().st_size
            if size > MAX_SCANNED_TEXT_BYTES:
                messages.append(
                    f"{relative}: exceeds {MAX_SCANNED_TEXT_BYTES} byte scanner limit"
                )
                continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            messages.append(f"{relative}: cannot scan text: {exc}")
            continue

        matches = Counter(match.group(0).lower() for match in pattern.finditer(text))
        if not matches:
            continue

        classification = _classify_path(relative, classifications)
        if classification is None:
            unclassified.append(
                f"{relative}: {sum(matches.values())} retired-capability references are unclassified"
            )
            continue
        inventories[classification["classification_id"]][relative] = matches

    messages.extend(sorted(unclassified))

    mode = manifest["mode"]
    snapshots: list[ClassificationSnapshot] = []
    for classification in classifications:
        classification_id = classification["classification_id"]
        entries = inventories[classification_id]
        snapshot = ClassificationSnapshot(
            classification_id=classification_id,
            files=len(entries),
            references=sum(sum(counts.values()) for counts in entries.values()),
            inventory_sha256=capability_inventory_digest(entries),
        )
        snapshots.append(snapshot)
        messages.extend(_compare_snapshot(classification, snapshot))
        if snapshot.references and mode not in classification["allowed_modes"]:
            messages.append(
                f"{classification_id}: state {classification['state']!r} is not allowed in mode {mode!r}"
            )

    trace_messages: list[str] = []
    trace_policy = data.get("trace_validation")
    if isinstance(trace_policy, dict):
        trace_result = validate_generalized_trace_semantics(
            root / trace_policy["trace_registry_path"],
            program_state=root / trace_policy["program_state_path"],
            source_registry=root / trace_policy["source_registry_path"],
            derivative_registry=root / trace_policy["derivative_registry_path"],
            policy_path=target,
        )
        if trace_result.ok:
            trace_messages.extend(trace_result.messages)
        else:
            messages.extend(trace_result.messages)

    if messages:
        return ValidationResult(False, messages + _snapshot_messages(snapshots))

    total_files = sum(snapshot.files for snapshot in snapshots)
    total_references = sum(snapshot.references for snapshot in snapshots)
    return ValidationResult(
        True,
        [
            f"{target}: G-05 boundary inventory passed in {mode} mode; "
            f"{total_references} references across {total_files} classified files",
            *_snapshot_messages(snapshots),
            *trace_messages,
            STRUCTURAL_LIMITATION,
        ],
    )


def _infer_repository_root(manifest_path: Path) -> Path:
    resolved = manifest_path.resolve()
    if resolved.parent.name == "configs" and resolved.parent.parent.name == "Sys4AI":
        return resolved.parent.parent.parent
    return Path.cwd().resolve()


def _validate_manifest_schema(data: dict[str, Any], root: Path) -> list[str]:
    manifest = data.get("manifest")
    if not isinstance(manifest, dict):
        return ["capability-migration manifest requires a [manifest] table"]

    schema_value = manifest.get("schema_path", str(DEFAULT_SCHEMA_PATH))
    schema_path = root / str(schema_value)
    if not schema_path.exists():
        return [f"{schema_path}: missing capability-migration schema"]
    try:
        schema = load_json(schema_path)
    except RuntimeError as exc:
        return [str(exc)]

    messages = [
        f"{schema_path}: invalid JSON Schema: {error}"
        for error in check_schema(schema)
    ]
    messages.extend(
        f"capability-migration manifest schema: {error}"
        for error in validate_instance(data, schema)
    )
    return messages


def _validate_classification_contracts(
    classifications: list[dict[str, Any]],
    root: Path,
) -> list[str]:
    messages: list[str] = []
    ids = [item["classification_id"] for item in classifications]
    priorities = [item["priority"] for item in classifications]
    for value in sorted({item for item in ids if ids.count(item) > 1}):
        messages.append(f"duplicate classification_id {value!r}")
    for value in sorted({item for item in priorities if priorities.count(item) > 1}):
        messages.append(f"duplicate classification priority {value}")

    for item in classifications:
        classification_id = item["classification_id"]
        for value in item.get("paths", []):
            if not (root / value).exists():
                messages.append(f"{classification_id}: classified path does not exist: {value}")
    return messages


def _validate_removed_paths(values: list[str], root: Path) -> list[str]:
    return [
        f"{value}: retired runtime path has been restored"
        for value in values
        if (root / value).exists() or (root / value).is_symlink()
    ]


def _legacy_reference_pattern(terms: list[str]) -> re.Pattern[str]:
    ordered = sorted({term for term in terms if term}, key=lambda value: (-len(value), value))
    return re.compile("|".join(re.escape(term) for term in ordered), re.IGNORECASE)


def _scan_paths(
    manifest: dict[str, Any],
    root: Path,
) -> tuple[list[Path], list[str]]:
    extensions = set(manifest["text_extensions"])
    excluded = manifest["excluded_paths"]
    paths: set[Path] = set()
    messages: list[str] = []
    for value in manifest["scan_roots"]:
        scan_root = root / value
        if not scan_root.exists():
            messages.append(f"{value}: declared scan root does not exist")
            continue
        candidates = [scan_root] if scan_root.is_file() else scan_root.rglob("*")
        for path in candidates:
            if not path.is_file() or path.suffix.lower() not in extensions:
                continue
            relative = path.relative_to(root).as_posix()
            if any(fnmatchcase(relative, glob) for glob in excluded):
                continue
            paths.add(path)
    return sorted(paths), messages


def _classify_path(
    relative_path: str,
    classifications: list[dict[str, Any]],
) -> dict[str, Any] | None:
    for item in classifications:
        if relative_path in item.get("paths", []):
            return item
        if any(fnmatchcase(relative_path, glob) for glob in item.get("path_globs", [])):
            return item
    return None


def _compare_snapshot(
    classification: dict[str, Any],
    snapshot: ClassificationSnapshot,
) -> list[str]:
    classification_id = snapshot.classification_id
    messages: list[str] = []
    expected_files = classification["expected_files"]
    expected_references = classification["expected_references"]
    expected_hash = classification["expected_inventory_sha256"]
    if snapshot.files != expected_files:
        messages.append(
            f"{classification_id}: expected {expected_files} files, found {snapshot.files}"
        )
    if snapshot.references != expected_references:
        messages.append(
            f"{classification_id}: expected {expected_references} references, "
            f"found {snapshot.references}"
        )
    if snapshot.inventory_sha256 != expected_hash:
        messages.append(
            f"{classification_id}: inventory fingerprint mismatch; "
            f"expected {expected_hash}, found {snapshot.inventory_sha256}"
        )
    return messages


def _snapshot_messages(snapshots: list[ClassificationSnapshot]) -> list[str]:
    return [
        f"{snapshot.classification_id}: files={snapshot.files} "
        f"references={snapshot.references} sha256={snapshot.inventory_sha256}"
        for snapshot in snapshots
    ]
