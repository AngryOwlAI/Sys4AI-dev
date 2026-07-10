"""Focused semantic boundary checks for the canonical Sys4AI PRDs."""

from __future__ import annotations

from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any

from .registry_io import resolve_registered_path
from .toml_io import load_toml
from .validation_semantics import STRUCTURAL_LIMITATION
from .validators import ValidationResult


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


def validate_prd_semantics(
    phase0_prd: str | Path = "PRDs/Sys4AI_phase-0_product_system_design_prd.md",
    phase1_prd: str | Path = "PRDs/Sys4AI_phase-1_implementation_initialization_prd.md",
    *,
    capability_manifest: str | Path = "configs/capability_migration.toml",
    modules_root: str | Path = "../PRDs/modules",
    repository_root: str | Path | None = None,
) -> ValidationResult:
    """Validate canonical identity, execution, lifecycle, and authority semantics."""

    phase0 = resolve_registered_path(str(phase0_prd))
    phase1 = resolve_registered_path(str(phase1_prd))
    messages: list[str] = []
    texts: dict[Path, str] = {}
    for path, markers in ((phase0, PHASE0_MARKERS), (phase1, PHASE1_MARKERS)):
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
            f"canonical PRD semantic validation passed ({phase0.name}; {phase1.name})",
            STRUCTURAL_LIMITATION,
        ],
    )


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
