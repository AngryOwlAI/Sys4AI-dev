# Portable example for `system-definition-interview`

## Scenario

A root AI agent receives a bounded project authorization to define a target agentic system for coordinating maintenance requests. Stakeholders know pain points but have not established vision, values, authority, boundary, scenarios, candidate requirements, or V&V seeds.

## Minimal use

1. Confirm the bounded project authorization or Director decision.
2. Read canonical sources first.
3. Classify the situation as new, existing, partially built, or documentation recovery.
4. Ask one focused question about the success criterion.
5. Record the answer in a discovery record.
6. Extract `NEED-*`, `STK-*`, `SCN-*`, `VISION-CAND-*`, `VALUE-CAND-*`, `REQ-CAND-*`, and `VVE-*` entries; record missing approval authority and conflicts.
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
- VISION-CAND-001
- VALUE-CAND-001
- REQ-CAND-001
- VVE-001
Validation:
- make validate-skills
- validate-discovery-record, if available
```
