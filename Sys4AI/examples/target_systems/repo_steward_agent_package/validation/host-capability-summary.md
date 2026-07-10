# Host-Capability Validation Summary

Validation ID: `VAL-REPO-STEWARD-HOST-001`
Status: pass with explicit permission dependency

## Required Capabilities

- `workspace_filesystem`: permission-dependent on explicit user authorization for
  the repository scope. It is not inferred from the package or host profile.
- `local_validation`: available only for the authorized repository-local command.

## Degraded Behavior

Denied, blocked, stale, or unknown required capability stops the demonstration and
records the gap. No value, goal, or model output may expand permission.

## Cancellation Behavior

Cancellation preserves the last accepted source evidence and stops at the nearest
safe transaction boundary.

This is a smoke example and derivative draft. It is not a production target system
and does not satisfy the still-open `G-07` host-verification gate.

## Limitation

Structural validation does not prove strategic quality, ethical correctness,
stakeholder consensus, behavioral alignment, production readiness, or domain truth.
Those claims require accountable review and additional evidence.
