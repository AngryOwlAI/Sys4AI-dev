"""Data models for source-first memory."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegistryEvidence:
    registry_name: str
    row_id: str
    row: dict[str, str]


@dataclass(frozen=True)
class ValidationEvidence:
    validation_status: str
    validation_contract_id: str | None
    validator_command: str | None
    last_validated_at: str | None


@dataclass(frozen=True)
class DerivativeEvidence:
    derivative_id: str | None
    source_ids: list[str]
    stale_or_orphan_status: str | None
    generation_method: str | None


@dataclass(frozen=True)
class MemoryObject:
    object_id: str
    path: str
    artifact_class: str
    format_profile_id: str | None
    authority_status: str
    registry_evidence: RegistryEvidence
    validation_evidence: ValidationEvidence
    derivative_evidence: DerivativeEvidence | None
    owner: str | None
    source_hash: str | None
    secrets_allowed: bool | None


@dataclass(frozen=True)
class MemoryHit:
    query: str
    object_id: str
    path: str
    title: str | None
    snippet: str | None
    score: int
    authority_status: str
    format_profile_id: str | None
    registry_evidence: RegistryEvidence
    validation_evidence: ValidationEvidence
    derivative_evidence: DerivativeEvidence | None
    required_next_action: str
