# Portable example for `codex-usage-metrics`

## Scenario

A `sys-for-ai` implementation agent receives an AgentJob requiring `runtime_session_accounting` support.

## Minimal use

1. Read the AgentJob objective and allowed files.
2. Confirm the task needs Codex app session metrics, not API billing or generic telemetry.
3. Run `make validate-metrics`.
4. Run the metrics script with an authorized output path.
5. Treat the resulting receipt as point-in-time evidence.
6. If context left is unknown, route the caller to fail-closed handoff behavior.

## Example output shape

```text
Skill: codex-usage-metrics
Status: pass | repair | block
Sources used:
- local Codex rollout JSONL token_count events
Output:
- usage-metrics.txt
Validation:
- make validate-metrics
- collect_usage_metrics.py --help
```
