---
schema_version: 0.1.0
artifact_type: target_core_values
core_values_set_id: VALUES-GREENFIELD-001
value_ids:
  - VALUE-GREENFIELD-001
  - VALUE-GREENFIELD-002
rejected_candidate_ids:
  - VALUE-CAND-GREENFIELD-003
target_system_id: example_maintenance_coordination
subject_layer: target_system_instance
content_approval_state: approved
source_authority_state: controlled
validation_state: schema_valid
approval:
  status: approved
  approved_by: Example Product Owner
  principal_role: accountable_product_owner
  approved_at: "2026-07-09"
  approval_evidence: EXAMPLE-APPROVAL-GREENFIELD-001
review_cadence: quarterly and on material incident or boundary change
version: 1.0.0
source_hash: sha256:b3450caf3780f4a0527265951becd72836754289e1568cdcc627a88624a62085
waiver:
  status: none
impact_analysis:
  state: not_applicable
  reviewed_surfaces: []
  evidence: EXAMPLE-FIRST-BASELINE-001
supersession:
  state: current
  supersedes: null
  superseded_by: null
  evidence: EXAMPLE-ACTIVE-VERSION-001
---

# Target Core Values

## Metadata And Target Identity

This illustrative approved set contains two active stable values and one retained rejected candidate.

## Governance Floor

Law, platform policy, safety, security, privacy, source authority, permissions, and required human approval outrank these values.

## Stable Value Inventory

| Value ID | Short name | State | Owner | Source evidence |
|---|---|---|---|---|
| VALUE-GREENFIELD-001 | Visible ownership | approved | Example Product Owner | EXAMPLE-INTERVIEW-OPS-001 |
| VALUE-GREENFIELD-002 | Recoverable reliability | approved | Example Product Owner | EXAMPLE-INTERVIEW-OPS-001 |
| VALUE-CAND-GREENFIELD-003 | Speed above all | rejected | Example Product Owner | EXAMPLE-REVIEW-GREENFIELD-001 |

## Per-Value Commitment And Rationale

- `VALUE-GREENFIELD-001`: Every accepted request has a visible accountable owner because unowned work is the principal loss mode.
- `VALUE-GREENFIELD-002`: State and handoffs remain recoverable because outages must not erase accepted work.

## Positive And Prohibited Behaviors

Positive behavior exposes ownership changes and recovery evidence. Prohibited behavior hides stalled work, discards evidence, or removes human override to gain speed.

## Decision Tests

- Ownership test: can an authorized user identify who must act next?
- Recovery test: can the last accepted state be reconstructed after a failed integration?

## Design And Operational Implications

The design needs explicit ownership, append-only transitions, degraded-mode queues, and recovery runbooks.

## Testing And Evaluation Implications

Tests cover orphaned requests, transition evidence, queue loss, recovery, and operator override. Human review assesses whether visibility is useful without exposing restricted data.

## Conflict And Precedence Rules

Reliability and evidence integrity outrank unqualified speed. `VALUE-CAND-GREENFIELD-003` was rejected because its proposed speed-first rule would permit invisible loss and removal of recovery checks.

## Source Owner And Evidence

The Example Product Owner owns the set; example operator and requester interviews provide noncanonical source evidence.

## Inherited Sys4AI Constraints

The example inherits source-first authority, least privilege, independent approval, and fail-closed validation constraints without treating them as target-stakeholder approval.

## Target-Specific Commitments

Visible request ownership and recoverable handoffs apply specifically to the illustrative maintenance-coordination target.

## Known Tensions And Escalation

Throughput pressure may conflict with recovery checks. Material threshold changes escalate to the accountable product owner and operations reviewer.

## Downstream Trace

Example requirements, queue architecture, permission decisions, recovery evaluations, release gates, and maintenance reviews reference the two active value IDs.

## Approval And Review Cadence

The Example Product Owner approved this illustrative set after stakeholder review. It is reviewed quarterly and after incidents or material boundary changes.

## Waiver And Baseline Exception

No waiver applies.

## Impact Analysis

This first illustrative baseline has no predecessor. Downstream architecture and evaluation work remains planned.

## Revision Version Hash And Supersession

Version `1.0.0` is active only within this noncanonical example. A revision creates a registered successor and preserves this evidence.
