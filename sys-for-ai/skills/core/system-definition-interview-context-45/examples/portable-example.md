# Portable example for `system-definition-interview-context-45`

## Scenario

A system-definition interview spans multiple sessions. The agent captures user answers, checks context after each answer, and writes `temp_prd.md` when context used reaches 45 percent or metrics are unavailable.

## Minimal use

1. Confirm AgentJob authorization.
2. Resume from `temp_prd.md` if requested.
3. Ask one focused system-definition question.
4. Record the answer.
5. Run the metrics checkpoint.
6. Continue only if context left is known and greater than 55 percent.
7. Otherwise write `temp_prd.md` and stop.

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
