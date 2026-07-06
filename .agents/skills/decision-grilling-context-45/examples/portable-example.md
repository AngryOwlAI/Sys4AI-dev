# Portable Example: Clarifying Dashboard Decisions With Context Guard

## Scenario

A source analysis found that a release readiness dashboard is feasible, but the
team has not decided whether warning-level test failures should block release.
The grilling session may continue long enough to need a context handoff.

## Skill Role In The Chain

Use `decision-grilling-context-45` after initial analysis and before final PRD
writing when one unresolved decision could change scope, acceptance criteria, or
risk, and the interview may need to continue across multiple discussions.

## Example Inputs

- Plan under review: "Build a release readiness dashboard."
- Evidence: source analysis showing CI status, incidents, and release owner are
  existing source inputs.
- Decision criteria: avoid false release confidence and keep the first version
  small.
- Optional resume parameter: `/decision-grilling-context-45 temp_prd`.

## Example Interaction

```text
Analysis:
The highest-leverage unresolved decision is whether warning-level test failures
should block the dashboard's release-ready state.

Question:
Should the dashboard treat warning-level test failures as release-blocking?

Recommendation:
No. Treat warnings as "attention required" in version 1 unless the release
policy explicitly defines them as blockers. This preserves source authority and
avoids inventing stricter governance than the project currently documents.
```

After the user answers, the agent records the answer and runs:

```sh
python3 <SKILLS_ROOT>/codex-usage-metrics/scripts/collect_usage_metrics.py \
  --output <TARGET_SKILL_PATH>/usage-metrics.txt
```

When context remains above the safe threshold, the agent continues the interview
without creating, overwriting, or refreshing `temp_prd.md`.

## Example Resolved Decision

```md
## Resolved Decision

Warning-level test failures will not mark a release as blocked in version 1.
They will appear in an "attention required" section with source links and owner
labels.
```

## Example Context Handoff

If `usage-metrics.txt` reports context left at `55%` or lower, the agent writes
`<TARGET_SKILL_PATH>/temp_prd.md` with the gathered requirements, confirmed
decisions, unresolved questions, last question, user answer, metrics snapshot,
and this resume command:

```text
/decision-grilling-context-45 temp_prd
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

- The question is singular and decision-relevant.
- The recommendation is tied to evidence and risk.
- The resolved decision can be carried into the PRD.
- The context check happens after the user answer.
- `temp_prd.md` is written only at the handoff threshold, on unavailable/unknown
  metrics, or on explicit user request.
- The handoff file contains enough context to resume without restarting the
  interview.
- PRD creation requires explicit user confirmation.

## Adaptation Notes

In a regulated or safety-critical target project, the recommended default may
change. Preserve the one-question-at-a-time method, then adapt the risk
tolerance from target-project authority. Preserve the context checkpoint unless
the target project explicitly chooses a different threshold.
