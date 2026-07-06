# System Definition Interview Context 45

## Status

Adapter shell for the core `sys-for-ai` skill `system-definition-interview-context-45`.

## Source

- Repository: `https://github.com/AngryOwlAI/ai-skills-for-sys`
- Path: `skills/system-definition-interview-context-45`

## Purpose

Support long-session system-definition interviews with a 45 percent context-used checkpoint and resumable `temp_prd.md` handoff.

This adapter checks context metrics after each user answer, but it writes
`temp_prd.md` only at the handoff threshold, on unavailable/unknown metrics, or
on explicit user request.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe.

## Local authority

This adapter is governed by `sys-for-ai` AgentJobs, canonical PRDs, source registries, decision records, and validation commands.

The `temp_prd.md` file is resumable context, not canonical authority. Candidate requirements remain candidates until promoted through an authorized source-authority workflow.

## Metrics policy

Use `skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py` for local Codex app context metrics. If the script is missing, fails, cannot report usable context-left data, or context left is at most 55 percent, write `temp_prd.md` and stop.

## Adaptation work remaining

1. Compare this adapter shell with the current upstream template.
2. Replace generic placeholders with local paths, validators, and authority boundaries.
3. Add stronger validation for `temp_prd.md` once a discovery-record validator exists.
4. Update `skills/core_skill_manifest.yaml` and `registries/skill_registry.csv` if status changes.
5. Mark status as `adapted` only after review and validation evidence.
