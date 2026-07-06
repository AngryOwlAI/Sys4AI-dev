# Portable example for `system-definition-interview-context-45`

## Scenario

A system-definition interview spans multiple sessions. The agent captures user answers, checks context after each answer, and writes `temp_prd.md` only when context used reaches 45 percent, context left is 55 percent or lower, metrics are unavailable or unknown, or the user explicitly requests a handoff.

## Minimal use

1. Confirm AgentJob authorization.
2. Resume from `temp_prd.md` if requested.
3. Ask one focused system-definition question.
4. Record the answer.
5. Run the metrics checkpoint.
6. Continue only if context left is known and greater than 55 percent.
7. Do not create, overwrite, or refresh `temp_prd.md` after each question when context is still safe.
8. Otherwise write `temp_prd.md` and stop.

## Example resume command

```text
/system-definition-interview-context-45 temp_prd
```

## Example output shape

```text
Skill: system-definition-interview-context-45
Status: pass | repair | block
Discovery record: control_records/system_definition/requirements-discovery-record.md
Checkpoint file: skills/core/system-definition-interview-context-45/temp_prd.md
Validation:
- make validate-skills
- collect_usage_metrics.py --help, if operational
```
