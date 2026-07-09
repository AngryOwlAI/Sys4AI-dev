---
name: codex-usage-metrics
description: Capture Codex context, token, and rate-limit metrics into a refreshed local receipt without exporting conversation content.
adaptation_status: adapter_shell
source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
source_path: skills/codex-usage-metrics
---

# Codex Usage Metrics

## Purpose

Capture Codex app context, token, and rate-limit metrics into a refreshed local receipt without exporting conversation content.

This local adapter supports context-aware skills such as `system-definition-interview-context-45`. It is not an OpenAI API billing reporter, ChatGPT usage reporter, general telemetry collector, or transcript export tool.

## When to use

Use this skill when a `Sys4AI` project authority requires the `runtime_session_accounting` capability and the governing PRD or implementation plan authorizes skill use.

Use it when a long-session adapter needs to know whether current Codex context state is safe to continue or should fail closed into a resumable handoff.

## Inputs

- Current project authorization or authorized adapter procedure.
- Optional Codex rollout JSONL file via `--session-file`.
- Optional session id via `--session-id`.
- Optional Codex home directory via `--codex-home`.
- Optional receipt output path via `--output`.
- Optional context-45 skill directory via `--skill-dir` for the archive helper.

## Outputs

- A deterministic text receipt such as `usage-metrics.txt`.
- Context window, latest request context usage, estimated context left, rate-limit summary, and token totals when present in local Codex session events.
- A confirmed prior context-45 checkpoint archive such as `archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md`.
- Validation evidence from `--help` or the local `validate-metrics` command.

## Procedure

1. Confirm the project authority authorizes this skill.
2. Use the local script path:

   ```bash
   .venv/bin/python skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py \
     --output skills/core/system-definition-interview-context-45/usage-metrics.txt
   ```

3. Prefer `--session-file` or `--session-id` when a project authority names a specific Codex session.
4. Use the latest local session only when no more specific session selector is authorized.
5. Read only the metrics receipt needed by the calling adapter.
6. If the script fails, returns no context section, or cannot identify context left, the calling context-45 adapter must fail closed by writing `temp_prd.md` and stopping.
7. For context-45 stale checkpoint checks, use the local archive helper:

   ```bash
   .venv/bin/python skills/core/codex-usage-metrics/scripts/archive_temp_prd.py \
     --check --skill-dir skills/core/system-definition-interview-context-45
   ```

   Run the same helper with `--confirm-archive` only after explicit user
   confirmation. The archive path format is
   `archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md`.
8. Run validation before treating the metrics or archive-helper paths as operational.

## Local authority boundaries

- This adapter does not override PRDs, source registries, decision records, or validators.
- Metrics receipts are point-in-time evidence only.
- The collector intentionally excludes conversation transcript content.
- Do not export chat messages, secrets, tool arguments, reasoning content, or full session logs.
- Do not use this adapter for OpenAI API billing, ChatGPT usage reporting, or generic telemetry.
- Upstream skill text and behavior must be reviewed before this adapter is marked `adapted`.

## Validation

Run:

```bash
cd Sys4AI
make validate-metrics
.venv/bin/python skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py --help
.venv/bin/python skills/core/codex-usage-metrics/scripts/archive_temp_prd.py --help
```

## Known failure modes

- Using the skill without explicit project authority.
- Treating Codex app session metrics as OpenAI API billing or ChatGPT usage data.
- Continuing a context-45 workflow when metrics cannot be collected.
- Archiving or overwriting a context-45 `temp_prd.md` without explicit user confirmation.
- Including transcript content or sensitive local paths in a shared receipt.
- Marking the adapter as fully adapted before local review.

## Provenance

Adapted from `AngryOwlAI/ai-skills-for-sys/skills/codex-usage-metrics` as a local `Sys4AI` adapter. The local script remains scoped to Codex app rollout/session metrics.

## Adaptation work remaining

1. Review the upstream template and script for drift.
2. Add more structured receipt validation if the context-45 adapters require it.
3. Mark as `adapted` only after a skill-import review and validation receipt.
