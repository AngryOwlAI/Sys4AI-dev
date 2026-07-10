---
schema_version: 0.1.0
artifact_type: target_core_values
core_values_set_id: VALUES-CAND-BROWNFIELD-001
value_ids:
  - VALUE-CAND-BROWNFIELD-001
  - VALUE-CAND-BROWNFIELD-002
rejected_candidate_ids:
  - VALUE-CAND-BROWNFIELD-003
target_system_id: example_existing_incident_router
subject_layer: target_system_instance
content_approval_state: stakeholder_review
source_authority_state: controlled_candidate
validation_state: schema_valid
approval:
  status: not_approved
  approved_by: null
  principal_role: null
  approved_at: null
  approval_evidence: null
review_cadence: unknown pending accountable owner and stakeholder confirmation
version: 0.2.0
source_hash: pending
waiver:
  status: none
impact_analysis:
  state: blocked
  reviewed_surfaces:
    - existing runbooks
    - incident records
  evidence: Missing operator affected-user and product-owner confirmation
supersession:
  state: current
  supersedes: null
  superseded_by: null
  evidence: EXAMPLE-CANDIDATE-ROW-BROWNFIELD-001
---

# Target Core Values

## Metadata And Target Identity

This candidate set is inferred from brownfield evidence and remains unapproved despite structural validity.

## Governance Floor

Law, platform policy, safety, security, privacy, source authority, permissions, and required human approval outrank the candidates.

## Stable Value Inventory

| Value ID | Short name | State | Owner | Source evidence |
|---|---|---|---|---|
| VALUE-CAND-BROWNFIELD-001 | Visible degradation | stakeholder_review | missing | EXAMPLE-INCIDENT-BROWNFIELD-017 |
| VALUE-CAND-BROWNFIELD-002 | Recoverable evidence | stakeholder_review | missing | EXAMPLE-RUNBOOK-BROWNFIELD-001 |
| VALUE-CAND-BROWNFIELD-003 | Always appear available | rejected_candidate | missing | EXAMPLE-REVIEW-BROWNFIELD-001 |

## Per-Value Commitment And Rationale

- `VALUE-CAND-BROWNFIELD-001`: Expose degraded state because silent failure obscured ownership in the example incident.
- `VALUE-CAND-BROWNFIELD-002`: Preserve recoverable routing evidence because the runbook relies on reconstruction.

## Positive And Prohibited Behaviors

Positive candidates expose uncertainty and retain evidence. Hiding connector failure or fabricating continuity is prohibited.

## Decision Tests

- Degradation test: does the interface distinguish unknown or denied capability from availability?
- Evidence test: can an authorized operator reconstruct the last accepted route?

## Design And Operational Implications

Candidate implications include explicit degraded state, append-only evidence, replay controls, and human escalation.

## Testing And Evaluation Implications

Proposed tests cover connector denial, stale host evidence, replay, missing ownership, and human override. No test result can approve the values.

## Conflict And Precedence Rules

The rejected `VALUE-CAND-BROWNFIELD-003` would hide failure to preserve an appearance of availability. Evidence integrity and operator awareness take precedence, subject to stakeholder confirmation.

## Source Owner And Evidence

The source is limited to example runbooks and incident records. No accountable value owner has been confirmed.

## Inherited Sys4AI Constraints

Source-first authority, least privilege, independent approval, and fail-closed unknown capability are binding process constraints, not evidence that stakeholders approve these candidates.

## Target-Specific Commitments

Visible degradation and recoverable routing evidence are candidate commitments for this illustrative incident router only.

## Known Tensions And Escalation

Availability messaging conflicts with transparent uncertainty. The accountable product owner and represented operators must resolve the tension.

## Downstream Trace

No approved downstream trace exists. Candidate requirements and evaluations may reference these IDs only as unapproved discovery evidence.

## Approval And Review Cadence

Approval principal and cadence are missing. Silence is not consent, so promotion is blocked.

## Waiver And Baseline Exception

No waiver exists. Missing approval blocks a new baseline or release.

## Impact Analysis

Runbooks and incidents were inspected. Requirements, permissions, data, evaluations, release, operations, maintenance, and retirement impacts remain incomplete.

## Revision Version Hash And Supersession

Version `0.2.0` remains a candidate with `source_hash: pending`. A later approval or rejection must preserve this evidence and record the successor relationship.
