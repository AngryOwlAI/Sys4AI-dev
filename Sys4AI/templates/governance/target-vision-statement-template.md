---
schema_version: 0.1.0
artifact_type: target_vision_statement
vision_id: VISION-CAND-<TARGET>-001
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

# Target Vision Statement

## Metadata

Record the stable candidate or approved ID, target-system ID, independent content-approval, source-authority, and validation states, version, hash, active-version state, and registry rows.

## Target System And Subject Layer

Identify the target system and classify it as `target_system_template` or `target_system_instance`. Name the active authority root and any derivative surfaces.

## Authority And Non-Anthropomorphism Notice

This document represents source-backed stakeholder intent. It is not a model's personal desire, consciousness, moral agency, or purpose-setting authority. Structural validation and model authorship do not constitute approval.

## Mission Versus Vision

State the present mission need separately from the desired future condition. Explain how the vision extends the mission without duplicating it.

## Future-State Statement

Write one concise, testable future-state statement. Candidate content uses a `VISION-CAND-*` ID until accountable human approval.

## Intended Users And Beneficiaries

Name direct users, operators, maintainers, affected parties, and intended beneficiaries. Identify missing or unrepresented stakeholders.

## Desired Condition And Impact

Describe the condition that should exist and the intended positive impact. Separate stated evidence from inference.

## Time Horizon

State the time horizon and any review milestones.

## Scope Exclusions And Non-Goals

Define included scope, exclusions, and explicit non-goals.

## Success Signals

List observable outcome signals. Do not substitute implementation completion or structural validation for stakeholder outcomes.

## Source Evidence And RDR Candidates

Trace every material statement to stakeholder evidence, registered sources, and relevant `RDR`, `VISION-CAND-*`, `REQ-CAND-*`, or decision IDs.

## Assumptions Tensions And Open Questions

Record assumptions, unsupported inferences, conflicts, missing evidence, and unresolved questions with owners and blocking effects.

## Approval Principal And Evidence

Record the accountable human principal, role, date, and evidence. `model`, `ai`, a Meta-Agent Runtime ID as sole principal, silence, or missing response cannot approve this content.

## Independent State Model

| State axis | Value | Evidence |
|---|---|---|
| Content approval | candidate / stakeholder_review / approved / rejected / superseded | <evidence> |
| Source authority | derivative_draft / controlled_candidate / controlled / canonical | <evidence> |
| Structural validation | unvalidated / schema_valid / validated / failed | <evidence> |
| Capability or implementation | unknown / planned / implemented / verified | <evidence> |

## Waiver And Baseline Exception

Use `status: none` unless an accountable authority records a `WAIVER-*` ID, missing artifact or approval, reason, risk, scope, downstream handling, expiry, revisit trigger, affected requirements and decisions, and status. An expired waiver blocks a new baseline or release.

## Impact Analysis

For a material revision, review requirements, architecture, roles and permissions, data, threat model, tests and evaluations, release, operations, maintenance, improvement, and retirement obligations.

## Revision Version Hash And Supersession

Record revision triggers, semantic version, `sha256:` source hash, active-version relationship, prior version, successor, and supersession evidence. Never overwrite approved evidence in place.
