"""Deterministic memory search."""

from __future__ import annotations

from pathlib import Path

from ..registry_io import resolve_registered_path
from .authority import required_next_action
from .model import MemoryHit, MemoryObject
from .registry_catalog import build_catalog


TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".csv", ".toml", ".py"}


def search_memory(query: str, limit: int = 10, root: str | Path = ".") -> dict[str, object]:
    """Search registered memory objects using deterministic token scoring."""

    catalog = build_catalog(root)
    tokens = _tokenize(query)
    hits: list[MemoryHit] = []
    for memory_object in catalog.objects:
        resolved = resolve_registered_path(memory_object.path, root)
        text = _read_search_text(resolved)
        haystack = " ".join([memory_object.object_id, memory_object.path, memory_object.artifact_class, text]).lower()
        token_hits = sum(haystack.count(token) for token in tokens)
        if token_hits <= 0:
            continue
        score = token_hits * 10 + _authority_bonus(memory_object)
        hits.append(
            MemoryHit(
                query=query,
                object_id=memory_object.object_id,
                path=memory_object.path,
                title=_extract_title(text),
                snippet=_snippet(text, tokens),
                score=score,
                authority_status=memory_object.authority_status,
                format_profile_id=memory_object.format_profile_id,
                registry_evidence=memory_object.registry_evidence,
                validation_evidence=memory_object.validation_evidence,
                derivative_evidence=memory_object.derivative_evidence,
                required_next_action=required_next_action(memory_object),
            )
        )

    ranked = sorted(hits, key=lambda hit: (-hit.score, hit.object_id))[:limit]
    return {
        "ok": True,
        "query": query,
        "hits": [_hit_to_dict(hit) for hit in ranked],
        "warnings": catalog.warnings,
    }


def _hit_to_dict(hit: MemoryHit) -> dict[str, object]:
    return {
        "object_id": hit.object_id,
        "path": hit.path,
        "title": hit.title,
        "snippet": hit.snippet,
        "score": hit.score,
        "authority_status": hit.authority_status,
        "format_profile_id": hit.format_profile_id,
        "registry": hit.registry_evidence.registry_name,
        "registry_row_id": hit.registry_evidence.row_id,
        "validation_status": hit.validation_evidence.validation_status,
        "required_next_action": hit.required_next_action,
        "derivative": hit.derivative_evidence is not None,
    }


def _tokenize(query: str) -> list[str]:
    return [part.strip().lower() for part in query.split() if part.strip()]


def _read_search_text(path: Path) -> str:
    if not path.exists() or path.is_dir() or path.suffix not in TEXT_SUFFIXES:
        return ""
    if any(part in {".git", ".venv", ".local", "__pycache__"} for part in path.parts):
        return ""
    try:
        return path.read_text(encoding="utf-8")[:20000]
    except UnicodeDecodeError:
        return ""


def _extract_title(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or None
    return None


def _snippet(text: str, tokens: list[str]) -> str | None:
    lowered = text.lower()
    for token in tokens:
        index = lowered.find(token)
        if index >= 0:
            start = max(0, index - 80)
            end = min(len(text), index + 160)
            return " ".join(text[start:end].split())
    return None


def _authority_bonus(memory_object: MemoryObject) -> int:
    if memory_object.authority_status == "canonical":
        return 30
    if memory_object.authority_status == "canonical_draft":
        return 20
    if memory_object.registry_evidence.registry_name == "derivative_registry.csv":
        return -20
    if memory_object.authority_status == "controlled":
        return 10
    return 0
