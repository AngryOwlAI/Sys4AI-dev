# Portable Example: Long Maintenance Request Discovery Interview

## Scenario

An operations team wants to replace an informal maintenance request process
with a small coordination system. The discovery session may span multiple
discussions because several stakeholder groups need to clarify boundaries,
triage ownership, and exception handling.

## Example Interaction

```text
Analysis:
The situation appears to be a new system with documentation recovery elements.
The highest-leverage missing information is the first success criterion.

Question:
What outcome would prove the maintenance request system is working: fewer lost
requests, faster triage, better auditability, lower operator workload, or
another measurable result?

Recommendation:
Use "fewer lost requests and visible triage ownership" as the first success
criterion if the current failure mode is work disappearing between request and
assignment.
```

After the user answers, the agent records the answer in the working context and
runs:

```sh
python3 <SKILLS_ROOT>/codex-usage-metrics/scripts/collect_usage_metrics.py \
  --output <TARGET_SKILL_PATH>/usage-metrics.txt
```

When context remains above the safe threshold, the agent continues the interview
without creating, overwriting, or refreshing `temp_prd.md`.

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

## Candidate Requirements

| ID | Candidate Requirement | Source Scenario Or Need | Rationale | Status |
|---|---|---|---|---|
| REQ-CAND-001 | The system should record each submitted request with requester, location, description, priority, status, and owner. | NEED-001, SCN-001 | Prevents unowned or untraceable requests. | candidate |
```

## Example Context Handoff

If `usage-metrics.txt` reports context left at `55%` or lower, the agent writes
`<TARGET_SKILL_PATH>/temp_prd.md` with:

- resume command,
- objective,
- situation classification,
- System Intent Profile,
- strategic-intent candidates, missing stakeholders, approval principal, conflicts, waiver and review state,
- stakeholders,
- boundary,
- as-is and to-be state,
- scenarios,
- candidate requirements,
- quality attributes,
- drivers,
- interfaces,
- V&V seeds,
- evidence,
- assumptions, risks, and constraints,
- open questions,
- last question and answer,
- recommended next branch,
- metrics snapshot,
- prior checkpoint integration.

The resume command is:

```text
/system-definition-interview-context-45 temp_prd
```

## Example PRD Handoff

When questioning is genuinely complete, the agent asks:

```text
Questioning is complete. Should I create a PRD with `/conversation-to-prd` using the current discussion and `temp_prd.md` if it exists?
```

If the user says yes, the agent routes the current discussion and any existing
`temp_prd.md` content into `/conversation-to-prd`. If the user says no, the
agent stops with a concise summary and logical next step.

## Validation

- The question is focused and decision-relevant.
- The user answer is captured before the metrics checkpoint.
- `temp_prd.md` is written only at the handoff threshold, on unavailable/unknown
  metrics, or on explicit user request.
- The handoff file contains enough context to resume without restarting the
  interview.
- Candidate requirements remain labeled as candidates.
- PRD creation requires explicit user confirmation.
