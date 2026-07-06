# Portable example for `system-definition-interview`

## Scenario

A root AI agent receives an AgentJob to define a target agentic system for coordinating maintenance requests. Stakeholders know pain points but have not established boundary, scenarios, candidate requirements, or V&V seeds.

## Minimal use

1. Confirm AgentJob authorization.
2. Read canonical sources first.
3. Classify the situation as new, existing, partially built, or documentation recovery.
4. Ask one focused question about the success criterion.
5. Record the answer in a discovery record.
6. Extract `NEED-*`, `STK-*`, `SCN-*`, `REQ-CAND-*`, and `VVE-*` entries.
7. Route unresolved decisions to decision grilling.

## Example output shape

```text
Skill: system-definition-interview
Status: pass | repair | block
Discovery record: control_records/system_definition/requirements-discovery-record.md
Candidate IDs created:
- NEED-001
- STK-001
- SCN-001
- REQ-CAND-001
- VVE-001
Validation:
- make validate-skills
- validate-discovery-record, if available
```
