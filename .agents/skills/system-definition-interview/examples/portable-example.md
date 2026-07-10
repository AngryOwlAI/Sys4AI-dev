# Portable Example: Maintenance Request Coordination System

## Scenario

An operations team wants to replace an informal maintenance request process
with a small coordination system. The team knows the pain points but has not
defined the system boundary, stakeholder classes, operational scenarios, or
candidate requirements.

## Example Interview Start

```text
Analysis:
The situation appears to be a new system with documentation recovery elements,
because current work is handled informally and no stable source document exists.

Question:
What outcome would prove the maintenance request system is working: faster
triage, fewer lost requests, better auditability, lower operator workload, or
another measurable result?

Recommendation:
Use "fewer lost requests and visible triage ownership" as the first success
criterion if the current failure mode is work disappearing between request and
assignment.
```

## Example Discovery Entries

```md
## System Intent Profile

| ID | Need | Source | Evidence Status |
|---|---|---|---|
| NEED-001 | Reduce lost maintenance requests and make triage ownership visible. | Operations lead interview | stated |

## Strategic Intent Candidates

| ID | Candidate | Source | Evidence Status |
|---|---|---|---|
| VISION-CAND-001 | Every accepted request remains visible, owned, and recoverable. | Operations lead interview | stated; unapproved |
| VALUE-CAND-001 | Visible ownership | Operations lead interview | stated; unapproved |
| VALUE-CAND-002 | Speed above evidence integrity | Agent inference | rejected_candidate |

## Stakeholders And Roles

| ID | Class | Role In System | Primary Need | Evidence |
|---|---|---|---|---|
| STK-001 | user | Submits maintenance requests | Clear status and acknowledgement | Interview |
| STK-002 | operator | Triages incoming requests | Queue ownership and priority visibility | Interview |
| STK-003 | maintainer | Resolves assigned requests | Complete task context and closeout path | Interview |

## Operational Scenarios And ConOps Seeds

| ID | Scenario | Actors | Trigger | Normal Flow | Exception Or Degraded Flow |
|---|---|---|---|---|---|
| SCN-001 | Submit and triage request | User, operator | User submits request | Request is acknowledged, queued, assigned, and status is visible | Missing location or priority requires clarification |

## Candidate Requirements

| ID | Candidate Requirement | Source Scenario Or Need | Rationale | Status |
|---|---|---|---|---|
| REQ-CAND-001 | The system should record each submitted request with requester, location, description, priority, status, and owner. | NEED-001, SCN-001 | Prevents unowned or untraceable requests. | candidate |

## Verification And Validation Seeds

| ID | Candidate Evidence Or Check | Traces To | Method | Owner Or Gate |
|---|---|---|---|---|
| VVE-001 | Demonstrate that a submitted request cannot remain unowned after triage. | REQ-CAND-001 | demonstration | Operations owner |
```

## Routing Outcome

- Use `decision-grilling-context-45` if stakeholders disagree about whether
  priority is user-selected or operator-assigned.
- Use `domain-grilling-with-docs-context-45` if terms such as request, task,
  incident, and work order conflict with existing documentation.
- Use `conversation-to-prd` only after the discovery record has stable
  stakeholders, boundaries, scenarios, candidate requirements, and open
  questions.

## Validation

- The example records intent before PRD creation.
- Candidate requirements remain labeled as candidates.
- Candidate vision and values remain unapproved until accountable human evidence exists.
- Each candidate can trace back to a need or scenario.
- Verification thinking begins early without claiming final acceptance tests.
