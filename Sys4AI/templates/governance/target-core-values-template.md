---
schema_version: 0.1.0
artifact_type: target_core_values
core_values_set_id: VALUES-CAND-<TARGET>-001
value_ids:
  - VALUE-CAND-<TARGET>-001
rejected_candidate_ids: []
target_system_id: <TARGET-SYSTEM-ID>
subject_layer: target_system_instance
content_approval_state: candidate
source_authority_state: controlled_candidate
validation_state: unvalidated
approval:
  status: not_approved
  approved_by: null
  principal_role: null
  approved_at: null
  approval_evidence: null
review_cadence: <CADENCE-OR-TRIGGER>
version: 0.1.0
source_hash: pending
waiver:
  status: none
impact_analysis:
  state: not_started
  reviewed_surfaces: []
  evidence: null
supersession:
  state: current
  supersedes: null
  superseded_by: null
  evidence: null
---

# Target Core Values

## Metadata And Target Identity

Record the value-set ID, active `VALUE-CAND-*` or `VALUE-*` IDs, rejected candidate IDs, target identity, subject layer, independent states, review cadence, version, hash, waiver, and supersession metadata.

## Governance Floor

Applicable law, mandatory platform policy, safety, security, privacy, compliance, source authority, host permissions, project permissions, and required human approval outrank target values.

## Stable Value Inventory

| Value ID | Short name | State | Owner | Source evidence |
|---|---|---|---|---|
| VALUE-CAND-<TARGET>-001 | <name> | candidate | <owner> | <source> |

Approved active values use `VALUE-*` identifiers. Candidate, stakeholder-review, and rejected entries retain `VALUE-CAND-*` identifiers.

## Per-Value Commitment And Rationale

For each active value, state the commitment and explain why it matters to represented stakeholders.

## Positive And Prohibited Behaviors

For each active value, list observable positive behaviors and prohibited behaviors, including anti-values and misuse cases.

## Decision Tests

For each active value, define a concrete decision test that can distinguish compliant from conflicting choices.

## Design And Operational Implications

Trace each value to material architecture, permission, data, deployment, monitoring, incident, support, and maintenance implications.

## Testing And Evaluation Implications

Define test, verification, validation, evaluation, and human-review evidence. Values do not grade or approve themselves.

## Conflict And Precedence Rules

Record value-to-value conflicts, precedence or balancing rules, rejected alternatives, escalation owners, and conditions requiring accountable human judgment.

## Source Owner And Evidence

Name the source, owner, affected stakeholders, evidence type, confidence, and any inference or missing-authority state for every value.

## Inherited Sys4AI Constraints

List binding inherited constraints separately from target-specific values. Inheritance does not transfer approval or expand permissions.

## Target-Specific Commitments

Identify commitments that apply only to this target system and their scope.

## Known Tensions And Escalation

List known tensions, anti-values, unresolved stakeholder conflicts, missing evidence, escalation route, and stop conditions.

## Downstream Trace

Trace material requirements, architecture decisions, permission decisions, risk acceptances, evaluation scenarios, release decisions, maintenance changes, improvement proposals, and retirement decisions to affected value IDs.

## Approval And Review Cadence

Record the accountable human principal, role, date, evidence, scheduled cadence, and event-driven review triggers. `model`, `ai`, a Meta-Agent Runtime ID as sole principal, silence, or missing response cannot approve the set.

## Waiver And Baseline Exception

Use `status: none` unless an accountable authority records every required `WAIVER-*` field. An expired waiver blocks a new baseline or release and never converts candidate content into approved content.

## Impact Analysis

For a material revision, review requirements, architecture, roles and permissions, data, threat model, tests and evaluations, release, operations, maintenance, improvement, and retirement obligations.

## Revision Version Hash And Supersession

Record revision triggers, semantic version, `sha256:` source hash, active-version relationship, prior version, successor, and supersession evidence. Never overwrite approved evidence in place.
