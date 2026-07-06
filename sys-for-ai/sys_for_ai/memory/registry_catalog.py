"""Registry-backed memory catalog."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from ..registry_io import read_registry, read_registry_rows, resolve_registered_path, rows_by_id
from ..validators import REGISTRY_HEADERS, validate_registry_headers
from .authority import required_next_action
from .model import DerivativeEvidence, MemoryObject, RegistryEvidence, ValidationEvidence


REGISTRY_ID_FIELDS = {
    "source_registry.csv": "source_id",
    "control_record_registry.csv": "control_record_id",
    "config_source_registry.csv": "config_id",
    "validation_contract_registry.csv": "contract_id",
    "derivative_registry.csv": "derivative_id",
    "skill_registry.csv": "skill_id",
    "agentjob_registry.csv": "agentjob_id",
    "director_decision_registry.csv": "director_decision_id",
    "handoff_registry.csv": "handoff_id",
    "completion_receipt_registry.csv": "completion_receipt_id",
    "memory_preflight_receipt_registry.csv": "memory_preflight_receipt_id",
}


@dataclass
class MemoryCatalog:
    root: Path
    objects: list[MemoryObject]
    warnings: list[str]

    @property
    def objects_by_id(self) -> dict[str, MemoryObject]:
        return {item.object_id: item for item in self.objects}

    @property
    def objects_by_path(self) -> dict[str, MemoryObject]:
        return {item.path: item for item in self.objects}

    def lookup(self, query: str) -> MemoryObject | None:
        if query in self.objects_by_id:
            return self.objects_by_id[query]
        normalized = _normalize_query_path(query, self.root)
        by_path = self.objects_by_path
        if normalized in by_path:
            return by_path[normalized]
        for item in self.objects:
            if _normalize_path(item.path) == normalized:
                return item
        return None


def build_catalog(root: str | Path = ".") -> MemoryCatalog:
    """Build a deterministic catalog from known registries."""

    base = Path(root)
    registry_root = base / "registries"
    warnings: list[str] = []
    objects: list[MemoryObject] = []

    header_result = validate_registry_headers(registry_root)
    if not header_result.ok:
        warnings.extend(header_result.messages)

    format_profiles = _read_index(registry_root / "format_profile_registry.csv", "format_id")
    validation_contracts = _read_index(registry_root / "validation_contract_registry.csv", "contract_id")
    derivative_rows = _read_index(registry_root / "derivative_registry.csv", "derivative_id")

    for registry_name in sorted(REGISTRY_ID_FIELDS):
        registry_path = registry_root / registry_name
        if not registry_path.exists():
            warnings.append(f"{registry_path}: missing registry")
            continue
        _, rows = read_registry(registry_path)
        id_field = REGISTRY_ID_FIELDS[registry_name]
        seen: set[str] = set()
        for row in rows:
            object_id = row.get(id_field, "")
            if not object_id:
                warnings.append(f"{registry_path}: row missing {id_field}")
                continue
            if object_id in seen:
                warnings.append(f"{registry_path}: duplicate {id_field} {object_id}")
            seen.add(object_id)
            memory_object = _row_to_memory_object(
                registry_name=registry_name,
                row=row,
                id_field=id_field,
                format_profiles=format_profiles,
                validation_contracts=validation_contracts,
                derivative_rows=derivative_rows,
            )
            objects.append(memory_object)
            _record_path_warnings(base, memory_object, warnings)

    return MemoryCatalog(base, sorted(objects, key=lambda item: (item.registry_evidence.registry_name, item.object_id)), warnings)


def memory_status(root: str | Path = ".") -> dict[str, object]:
    """Return JSON-serializable memory status."""

    catalog = build_catalog(root)
    hard_failures = [warning for warning in catalog.warnings if "missing" in warning and "source_hash" not in warning]
    derivative_authority = [
        item.object_id
        for item in catalog.objects
        if item.registry_evidence.registry_name == "derivative_registry.csv"
        and item.authority_status in {"canonical", "canonical_draft"}
    ]
    status = "PASS"
    if hard_failures or derivative_authority:
        status = "FAIL"
    elif catalog.warnings:
        status = "PASS_WITH_WARNINGS"
    return {
        "ok": status != "FAIL",
        "status": status,
        "objects_count": len(catalog.objects),
        "warnings": catalog.warnings,
        "derivative_authority_inversions": derivative_authority,
    }


def memory_object_to_dict(memory_object: MemoryObject) -> dict[str, object]:
    """Convert a memory object to stable JSON."""

    return {
        "object_id": memory_object.object_id,
        "path": memory_object.path,
        "artifact_class": memory_object.artifact_class,
        "authority_status": memory_object.authority_status,
        "format_profile_id": memory_object.format_profile_id,
        "registry": memory_object.registry_evidence.registry_name,
        "registry_row_id": memory_object.registry_evidence.row_id,
        "validation_status": memory_object.validation_evidence.validation_status,
        "validation_contract_id": memory_object.validation_evidence.validation_contract_id,
        "validator_command": memory_object.validation_evidence.validator_command,
        "required_next_action": required_next_action(memory_object),
        "source_hash": memory_object.source_hash,
    }


def _row_to_memory_object(
    registry_name: str,
    row: dict[str, str],
    id_field: str,
    format_profiles: dict[str, dict[str, str]],
    validation_contracts: dict[str, dict[str, str]],
    derivative_rows: dict[str, dict[str, str]],
) -> MemoryObject:
    object_id = row[id_field]
    path = row.get("path") or row.get("local_path") or row.get("target_glob") or ""
    artifact_class = (
        row.get("source_type")
        or row.get("record_type")
        or row.get("target_artifact_type")
        or row.get("config_domain")
        or row.get("derivative_type")
        or registry_name.removesuffix(".csv")
    )
    authority_status = row.get("authority_status") or row.get("status") or row.get("adaptation_status") or "registered"
    validation_contract_id = row.get("validation_contract_id") or row.get("contract_id") or None
    contract_row = validation_contracts.get(validation_contract_id or "", {})
    format_profile_id = _guess_format_profile(path, format_profiles)
    derivative = None
    if registry_name == "derivative_registry.csv":
        derivative = DerivativeEvidence(
            derivative_id=object_id,
            source_ids=_split_semicolon(row.get("source_ids", "")),
            stale_or_orphan_status=row.get("status") or None,
            generation_method=row.get("generation_method") or None,
        )
    elif object_id in derivative_rows:
        der_row = derivative_rows[object_id]
        derivative = DerivativeEvidence(
            derivative_id=object_id,
            source_ids=_split_semicolon(der_row.get("source_ids", "")),
            stale_or_orphan_status=der_row.get("status") or None,
            generation_method=der_row.get("generation_method") or None,
        )

    return MemoryObject(
        object_id=object_id,
        path=path,
        artifact_class=artifact_class,
        format_profile_id=format_profile_id,
        authority_status=authority_status,
        registry_evidence=RegistryEvidence(registry_name, object_id, row),
        validation_evidence=ValidationEvidence(
            validation_status=row.get("last_validated_at") or "not_applicable",
            validation_contract_id=validation_contract_id,
            validator_command=contract_row.get("validator_command") or row.get("validator_command") or None,
            last_validated_at=row.get("last_validated_at") or None,
        ),
        derivative_evidence=derivative,
        owner=row.get("owner") or None,
        source_hash=row.get("source_hash") or None,
        secrets_allowed=_parse_bool(row.get("secrets_allowed")),
    )


def _record_path_warnings(base: Path, memory_object: MemoryObject, warnings: list[str]) -> None:
    path = memory_object.path
    if not path or "*" in path:
        return
    if memory_object.registry_evidence.registry_name == "skill_registry.csv":
        path = f"sys-for-ai/{path}" if not path.startswith("sys-for-ai/") else path
    resolved = resolve_registered_path(path, base)
    if not resolved.exists():
        warnings.append(f"{memory_object.registry_evidence.registry_name}: {memory_object.object_id}: missing path {path}")
    if (
        "source_hash" in memory_object.registry_evidence.row
        and memory_object.source_hash in {"", "pending", None}
        and "registry" in memory_object.registry_evidence.registry_name
    ):
        warnings.append(f"{memory_object.registry_evidence.registry_name}: {memory_object.object_id}: source_hash pending")


def _read_index(path: Path, id_field: str) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    return rows_by_id(read_registry_rows(path), id_field)


def _guess_format_profile(path: str, format_profiles: dict[str, dict[str, str]]) -> str | None:
    suffix = Path(path).suffix if path else ""
    for row in format_profiles.values():
        extensions = [part.strip() for part in row.get("extension", "").split(";")]
        if suffix and suffix in extensions:
            return row.get("format_id") or None
    if path.endswith(".schema.json"):
        return "fmt_jsonschema_contract"
    return None


def _split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def _parse_bool(value: str | None) -> bool | None:
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def _normalize_query_path(query: str, root: Path) -> str:
    candidate = Path(query)
    if candidate.is_absolute():
        try:
            return candidate.resolve().relative_to(root.resolve().parent).as_posix()
        except ValueError:
            return candidate.as_posix()
    return _normalize_path(query)


def _normalize_path(path: str) -> str:
    return Path(path).as_posix().lstrip("./")
