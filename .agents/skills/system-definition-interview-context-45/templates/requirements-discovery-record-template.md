# Requirements Discovery Record

## Record Metadata

- System name: <SYSTEM_NAME>
- Situation classification: <new system | existing system | partially built system | documentation recovery>
- Interview date: <DATE>
- Prepared by: <ROLE_OR_AGENT>
- Output status: <working draft | review draft | controlled artifact>
- Primary authority: <PROJECT_AUTHORITY>
- Output path: <OUTPUT_DIRECTORY>/requirements-discovery-record.md
- Continuation skill: `/system-definition-interview-context-45 temp_prd`
- Subject system ID: <SYSTEM_ID>
- Subject layer: <development_system | framework_product | target_system_template | target_system_instance | derivative_surface>
- Discovery gate: system-definition-interview-context-45
- Producer authority: <AUTHORITY_ID_OR_DIRECTOR_DECISION_ID>
- Discovery registry row: <discovery_record_registry.csv row ID>
- Downstream artifact status: <no USRD yet | USRD proposed | USRD created | discovery waived>

## Authority Notice

This Requirements Discovery Record is discovery evidence. It is not a canonical
requirements baseline unless promoted through the target project's
source-authority process.

Candidate requirements must remain labeled as `REQ-CAND-*` or `NFR-CAND-*`
until promoted by target-project authority.

## System Layer Classification

| Field | Value | Evidence | Open Issues |
|---|---|---|---|
| Subject layer | <layer> | <source> | <OPEN-*> |
| Active authority root | <path or registry> | <source> | <OPEN-*> |
| Product scaffold involved? | <yes | no | unknown> | <source> | <OPEN-*> |
| Target-system instance involved? | <yes | no | unknown> | <source> | <OPEN-*> |
| Derivative surfaces involved? | <yes | no | unknown> | <source> | <OPEN-*> |

## Discovery Gate Exit Checklist

| Check | Status | Evidence | Blocking Issues |
|---|---|---|---|
| Subject layer classified | <pass | warn | fail> | <evidence> | <OPEN-*> |
| Mission need captured or marked missing | <pass | warn | fail> | <evidence> | <OPEN-*> |
| Problem statement captured or marked missing | <pass | warn | fail> | <evidence> | <OPEN-*> |
| System-of-interest identified | <pass | warn | fail> | <evidence> | <OPEN-*> |
| Stakeholders identified | <pass | warn | fail> | <evidence> | <OPEN-*> |
| Boundaries captured | <pass | warn | fail> | <evidence> | <OPEN-*> |
| Candidate requirements remain candidate-labeled | <pass | warn | fail> | <evidence> | <OPEN-*> |
| Evidence register populated | <pass | warn | fail> | <evidence> | <OPEN-*> |
| Open questions routed | <pass | warn | fail> | <evidence> | <OPEN-*> |
| Next route recommended | <pass | warn | fail> | <evidence> | <OPEN-*> |

## System Intent Profile

### Mission Need

| ID | Need | Source | Evidence Status |
|---|---|---|---|
| NEED-001 | <mission need> | <stakeholder or source> | <observed | stated | inferred | missing> |

### Problem Statement

<What problem exists, who experiences it, and why the current state is insufficient.>

### Desired Outcome

<Observable outcome that would make the system worth building, changing, or documenting.>

### Value And Feasibility Notes

<Business case, feasibility constraints, schedule, cost, operational limits, or adoption concerns.>

### Success Criteria

| ID | Success Criterion | Evidence Or Owner |
|---|---|---|
| NEED-002 | <criterion> | <source> |

## Strategic Intent Candidates

Candidate strategic intent is discovery evidence. Use `VISION-CAND-*`, `VALUE-CAND-*`, and `WAIVER-CAND-*` until an accountable human approves separate registered artifacts. Silence, model authorship, controlled-file location, and structural validation are not approval.

| Field | Candidate value | Source | Evidence or approval state |
|---|---|---|---|
| Mission versus vision | <distinction> | <source> | stated / inferred / missing |
| Future-state vision | VISION-CAND-001: <statement> | <source> | candidate / stakeholder_review / rejected |
| Intended users and beneficiaries | <stakeholders> | <source> | represented / missing |
| Core values | VALUE-CAND-001: <commitment> | <source> | candidate / stakeholder_review / rejected |
| Anti-values and prohibited behaviors | <anti-values> | <source> | stated / inferred / missing |
| Conflicts and precedence | <rule or OPEN-*> | <source> | candidate / unresolved |
| Accountable approval principal | <human role or missing> | <source> | identified / missing |
| Inherited constraints | <constraints> | <source> | binding / candidate / unknown |
| Waiver | <WAIVER-CAND-* or none> | <authority> | proposed / active / expired / superseded / none |
| Review cadence and triggers | <cadence> | <owner> | candidate |
| Pattern and operational maturity | <pattern and maturity> | <source> | stated / inferred / missing |
| Autonomy, integrations, and communication | <boundary and interfaces> | <source> | stated / inferred / missing |
| Monitoring, degraded mode, and promotion evidence | <evidence> | <source> | candidate / missing |

## Stakeholders And Roles

| ID | Class | Role In System | Primary Need | Evidence |
|---|---|---|---|---|
| STK-001 | <user | operator | maintainer | owner | affected party | approver> | <role> | <need> | <source> |

## System Boundary

### In Scope

- <capability, responsibility, data, workflow, or interface>

### Out Of Scope

- <excluded capability or responsibility>

### External Systems And Interfaces

| ID | External System Or Actor | Interface Candidate | Direction | Notes |
|---|---|---|---|---|
| IF-001 | <system or actor> | <interface> | <inbound | outbound | bidirectional> | <notes> |

## Current And Target State

### As-Is State

<Observed current behavior, documentation state, or implementation state.>

### To-Be State

<Desired future behavior or documentation state.>

### Gaps

| ID | Gap | Impact | Evidence |
|---|---|---|---|
| OPEN-001 | <gap> | <impact> | <source or missing evidence> |

## Operational Scenarios And ConOps Seeds

| ID | Scenario | Actors | Trigger | Normal Flow | Exception Or Degraded Flow |
|---|---|---|---|---|---|
| SCN-001 | <scenario> | <actors> | <trigger> | <flow> | <exception path> |

## Candidate Requirements

### Functional Candidates

| ID | Candidate Requirement | Source Scenario Or Need | Rationale | Status |
|---|---|---|---|---|
| REQ-CAND-001 | <system shall candidate> | <NEED-* or SCN-*> | <why it matters> | <candidate | blocked | deferred> |

### Quality Attribute Candidates

| ID | Quality Attribute | Candidate Requirement | Rationale | Verification Seed |
|---|---|---|---|---|
| NFR-CAND-001 | <performance | reliability | safety | security | usability | maintainability | accessibility | supportability> | <candidate> | <why it matters> | <VVE-*> |

## Architecture Drivers

| ID | Driver | Type | Impact | Source |
|---|---|---|---|---|
| DRV-001 | <driver> | <constraint | quality | interface | operational | lifecycle> | <impact> | <source> |

## Verification And Validation Seeds

| ID | Candidate Evidence Or Check | Traces To | Method | Owner Or Gate |
|---|---|---|---|---|
| VVE-001 | <check or evidence> | <REQ-CAND-* | NFR-CAND-* | SCN-* | NEED-*> | <test | inspection | analysis | demonstration | review> | <owner or gate> |

## Assumptions, Risks, And Constraints

### Assumptions

| ID | Assumption | Impact If Wrong | How To Resolve |
|---|---|---|---|
| OPEN-002 | <assumption> | <impact> | <evidence or decision needed> |

### Risks

| ID | Risk | Likelihood | Impact | Mitigation Seed |
|---|---|---|---|---|
| OPEN-003 | <risk> | <low | medium | high> | <low | medium | high> | <mitigation> |

### Constraints

- <constraint and source>

## Evidence Register

| ID | Source | Type | What It Supports | Reliability |
|---|---|---|---|---|
| EVD-001 | <source> | <interview | document | repository | observation | standard> | <trace IDs> | <high | medium | low | unknown> |

## Open Questions

| ID | Question | Why It Matters | Recommended Route |
|---|---|---|---|
| OPEN-004 | <question> | <impact> | <decision-grilling-context-45 | domain-grilling-with-docs-context-45 | owner review | evidence search> |

## Continuation State

- Last question asked:
- User answer:
- Recommended next branch:
- Metrics snapshot:
- Prior temp PRD integration:

## Downstream Routing

- Decision clarification: <route or not needed>
- Terminology and documentation review: <route or not needed>
- PRD synthesis: <route or not ready>
- Requirements analysis: <future route or not ready>
- Formal systems-document package: <future route or not ready>

## Completion Receipt

- Inputs reviewed:
- Record path:
- Questions asked:
- Key decisions captured:
- Evidence gaps:
- Validation performed:
- Skipped checks and reasons:
- Logical next step:
