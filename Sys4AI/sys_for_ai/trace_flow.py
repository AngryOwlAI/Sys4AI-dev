"""Walking-skeleton trace flow data model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WalkingSkeletonArtifact:
    """One artifact in the Phase 2 walking-skeleton flow."""

    artifact_id: str
    artifact_type: str
    path: str
    subject_layer: str
    authority_status: str
    upstream_ids: tuple[str, ...]
    downstream_ids: tuple[str, ...]
    validation_status: str

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type,
            "path": self.path,
            "subject_layer": self.subject_layer,
            "authority_status": self.authority_status,
            "upstream_ids": list(self.upstream_ids),
            "downstream_ids": list(self.downstream_ids),
            "validation_status": self.validation_status,
        }


@dataclass(frozen=True)
class WalkingSkeletonFlowReport:
    """Validation summary for the Phase 2 walking-skeleton flow."""

    flow_id: str
    result: str
    artifacts: tuple[WalkingSkeletonArtifact, ...]
    missing_artifacts: tuple[str, ...]
    trace_gaps: tuple[str, ...]
    warnings: tuple[str, ...]
    pending_artifacts: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return {
            "flow_id": self.flow_id,
            "result": self.result,
            "artifacts_checked": len(self.artifacts),
            "artifacts": [artifact.as_dict() for artifact in self.artifacts],
            "missing_artifacts": list(self.missing_artifacts),
            "trace_gaps": list(self.trace_gaps),
            "warnings": list(self.warnings),
            "pending_artifacts": list(self.pending_artifacts),
        }
