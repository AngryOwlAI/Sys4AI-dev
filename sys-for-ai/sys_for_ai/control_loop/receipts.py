"""Completion receipt helpers for /continue finalization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..yaml_io import load_yaml


def load_completion_receipt(path: str | Path) -> dict[str, Any]:
    """Load a completion receipt from *path*."""

    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected completion receipt YAML mapping")
    return data


def completion_next_handoff_id(completion: dict[str, Any]) -> str | None:
    """Return the next handoff id declared by a completion receipt."""

    value = completion.get("next_handoff_id")
    if isinstance(value, str) and value:
        return value
    handoff = completion.get("handoff")
    if isinstance(handoff, dict):
        value = handoff.get("next_handoff_id") or handoff.get("handoff_id")
        if isinstance(value, str) and value:
            return value
    return None
