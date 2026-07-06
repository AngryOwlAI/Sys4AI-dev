"""Hash support for registered memory sources."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from ..registry_io import read_registry, resolve_registered_path


HASHED_REGISTRIES = (
    "registries/config_source_registry.csv",
    "registries/control_record_registry.csv",
    "registries/validation_contract_registry.csv",
)


def hash_path(path: str | Path) -> dict[str, object]:
    """Return the sha256 hash for *path*."""

    target = Path(path)
    if not target.exists():
        return {"ok": False, "path": str(path), "error": "missing_path"}
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return {"ok": True, "path": str(path), "sha256": digest}


def validate_hashes(root: str | Path = ".") -> dict[str, object]:
    """Validate populated source_hash fields and warn for pending fields."""

    base = Path(root)
    warnings: list[str] = []
    failures: list[dict[str, str]] = []
    checked = 0
    for registry in HASHED_REGISTRIES:
        registry_path = base / registry
        if not registry_path.exists():
            failures.append({"registry": registry, "reason": "missing_registry"})
            continue
        _, rows = read_registry(registry_path)
        for row in rows:
            source_hash = row.get("source_hash", "")
            if source_hash in {"", "pending"}:
                warnings.append(f"{registry}: {row.get('path', '')}: source_hash pending")
                continue
            resolved = resolve_registered_path(row.get("path", ""), base)
            if not resolved.exists():
                failures.append({"registry": registry, "path": row.get("path", ""), "reason": "missing_path"})
                continue
            checked += 1
            actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
            if source_hash != actual:
                failures.append({"registry": registry, "path": row.get("path", ""), "reason": "hash_mismatch"})
    return {
        "ok": not failures,
        "status": "FAIL" if failures else ("PASS_WITH_WARNINGS" if warnings else "PASS"),
        "checked": checked,
        "warnings": warnings,
        "failures": failures,
    }


def update_hashes(root: str | Path = ".", write: bool = False) -> dict[str, object]:
    """Check or update populated registry source_hash fields."""

    base = Path(root)
    updates: list[dict[str, str]] = []
    for registry in HASHED_REGISTRIES:
        registry_path = base / registry
        if not registry_path.exists():
            continue
        header, rows = read_registry(registry_path)
        changed = False
        for row in rows:
            path = row.get("path", "")
            resolved = resolve_registered_path(path, base)
            if not resolved.exists():
                continue
            digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
            if row.get("source_hash") != digest:
                updates.append({"registry": registry, "path": path, "old": row.get("source_hash", ""), "new": digest})
                if write:
                    row["source_hash"] = digest
                    changed = True
        if write and changed:
            with registry_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=header)
                writer.writeheader()
                writer.writerows(rows)
    return {"ok": True, "mode": "write" if write else "check", "updates": updates}
