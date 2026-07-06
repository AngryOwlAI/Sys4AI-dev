"""AgentJob boundary and Git-diff validation."""

from __future__ import annotations

from fnmatch import fnmatchcase
from pathlib import Path
import subprocess
from typing import Any

from ..registry_io import read_registry_rows
from .job_selection import load_agentjob


def validate_agentjob_boundaries(
    agentjob_id: str,
    root: str | Path = ".",
    use_git: bool = False,
    changed_paths: list[str] | None = None,
) -> dict[str, Any]:
    """Validate changed paths against an AgentJob boundary."""

    context = _resolve_context(root)
    agentjob = load_agentjob(agentjob_id, context.product_root)
    if agentjob is None:
        return {
            "ok": False,
            "agentjob_id": agentjob_id,
            "changed_paths": [],
            "allowed": [],
            "violations": [{"path": "", "reason": "unknown_agentjob"}],
            "warnings": [],
        }

    raw_paths = changed_paths
    if raw_paths is None:
        raw_paths = collect_git_changed_paths(context.repo_root) if use_git else []

    changed = sorted({_to_repo_path(path, context) for path in raw_paths if str(path).strip()})
    evaluation = _evaluate_paths(changed, agentjob.raw, context)
    return {
        "ok": not evaluation["violations"],
        "agentjob_id": agentjob_id,
        "changed_paths": changed,
        "allowed": evaluation["allowed"],
        "violations": evaluation["violations"],
        "warnings": evaluation["warnings"],
    }


def validate_check_diff(agentjob_id: str, root: str | Path = ".") -> dict[str, Any]:
    """Validate current Git diff paths against an AgentJob boundary."""

    return validate_agentjob_boundaries(agentjob_id, root=root, use_git=True)


def collect_git_changed_paths(repo_root: str | Path = ".") -> list[str]:
    """Collect unstaged, staged, and untracked paths from Git."""

    root = _find_git_root(Path(repo_root).resolve())
    commands = [
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    paths: set[str] = set()
    for command in commands:
        result = subprocess.run(
            command,
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        )
        for line in result.stdout.splitlines():
            value = line.strip()
            if value:
                paths.add(value)
    return sorted(paths)


def _evaluate_paths(changed_paths: list[str], agentjob: dict[str, Any], context: "_BoundaryContext") -> dict[str, Any]:
    allowed_patterns = _string_list(agentjob.get("allowed_writes")) + _string_list(agentjob.get("generated_paths"))
    generated_patterns = _string_list(agentjob.get("generated_paths"))
    forbidden_patterns = _glob_forbidden_patterns(_string_list(agentjob.get("forbidden_paths")))
    ignored_patterns = _string_list(agentjob.get("ignored_paths")) + _string_list(agentjob.get("boundary_ignore_paths"))
    generated_derivatives = _generated_derivative_paths(context.product_root)
    canonical_derivatives = _canonical_generated_derivative_paths(context.product_root)

    allowed: list[str] = []
    violations: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    for path in changed_paths:
        if _matches_any(path, ignored_patterns):
            continue
        path_violations: list[dict[str, str]] = []
        if _matches_any(path, forbidden_patterns):
            path_violations.append({"path": path, "reason": "forbidden_path"})
        if path in generated_derivatives and not _matches_any(path, generated_patterns):
            path_violations.append(
                {"path": path, "reason": "generated_derivative_without_generated_path_authorization"}
            )
        if path in canonical_derivatives:
            path_violations.append({"path": path, "reason": "generated_derivative_registered_as_canonical_source"})
        if not _matches_any(path, allowed_patterns):
            path_violations.append({"path": path, "reason": "outside_allowed_writes"})
        if path_violations:
            violations.extend(path_violations)
        else:
            allowed.append(path)

    return {"allowed": allowed, "violations": violations, "warnings": warnings}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item.strip()]


def _glob_forbidden_patterns(patterns: list[str]) -> list[str]:
    return [pattern for pattern in patterns if " as canonical source" not in pattern]


def _matches_any(path: str, patterns: list[str]) -> bool:
    if not patterns:
        return False
    normalized = _clean_path(path)
    candidates = {normalized}
    if normalized.startswith("sys-for-ai/"):
        candidates.add(normalized.removeprefix("sys-for-ai/"))
    else:
        candidates.add(f"sys-for-ai/{normalized}")
    return any(_matches_pattern(candidate, pattern) for candidate in candidates for pattern in patterns)


def _matches_pattern(path: str, pattern: str) -> bool:
    normalized = _clean_path(pattern)
    if fnmatchcase(path, normalized):
        return True
    if normalized.endswith("/**"):
        return path.startswith(normalized[:-3] + "/")
    return False


def _generated_derivative_paths(product_root: Path) -> set[str]:
    registry = product_root / "registries/derivative_registry.csv"
    if not registry.exists():
        return set()
    return {
        _product_to_repo_path(row.get("path", ""), product_root)
        for row in read_registry_rows(registry)
        if row.get("path")
    }


def _canonical_generated_derivative_paths(product_root: Path) -> set[str]:
    registry = product_root / "registries/source_registry.csv"
    if not registry.exists():
        return set()
    paths: set[str] = set()
    for row in read_registry_rows(registry):
        path = row.get("path", "")
        status = row.get("authority_status", "")
        if path.startswith("sys-for-ai/docs/generated/") and status in {"canonical", "canonical_draft"}:
            paths.add(_clean_path(path))
    return paths


def _to_repo_path(path: str, context: "_BoundaryContext") -> str:
    value = _clean_path(path)
    if value.startswith("sys-for-ai/"):
        return value
    if context.product_root == context.start_root and not value.startswith("../"):
        return f"sys-for-ai/{value}"
    return value


def _product_to_repo_path(path: str, product_root: Path) -> str:
    value = _clean_path(path)
    if value.startswith("sys-for-ai/"):
        return value
    if product_root.name == "sys-for-ai":
        return f"sys-for-ai/{value}"
    return value


def _clean_path(path: str) -> str:
    value = str(path).strip().replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


class _BoundaryContext:
    def __init__(self, start_root: Path, repo_root: Path, product_root: Path) -> None:
        self.start_root = start_root
        self.repo_root = repo_root
        self.product_root = product_root


def _resolve_context(root: str | Path) -> _BoundaryContext:
    start = Path(root).resolve()
    repo_root = _find_git_root(start)
    product_root = _find_product_root(start, repo_root)
    return _BoundaryContext(start, repo_root, product_root)


def _find_git_root(start: Path) -> Path:
    current = start
    if current.is_file():
        current = current.parent
    while True:
        if (current / ".git").exists():
            return current
        if current.parent == current:
            return start
        current = current.parent


def _find_product_root(start: Path, repo_root: Path) -> Path:
    candidates = [
        start,
        repo_root / "sys-for-ai",
        repo_root,
    ]
    for candidate in candidates:
        if (candidate / "registries/agentjob_registry.csv").exists():
            return candidate
    return repo_root
