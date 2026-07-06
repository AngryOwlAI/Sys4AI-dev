"""Source-first memory registry bootstrap helpers."""

from __future__ import annotations

import csv
from pathlib import Path

from ..validators import REGISTRY_HEADERS, ValidationResult, validate_registry_headers


def bootstrap_registries(registry_dir: str | Path) -> ValidationResult:
    """Create missing registry files using the declared headers."""

    root = Path(registry_dir)
    root.mkdir(parents=True, exist_ok=True)
    messages: list[str] = []

    for filename, header in REGISTRY_HEADERS.items():
        path = root / filename
        if path.exists():
            messages.append(f"{path}: exists, left unchanged")
            continue
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
        messages.append(f"{path}: created")

    validation = validate_registry_headers(root)
    ok = validation.ok
    messages.extend(validation.messages)
    return ValidationResult(ok, messages)
