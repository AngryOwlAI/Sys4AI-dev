# Maintenance rules for `codex-usage-metrics`

- Preserve provenance to `skills/codex-usage-metrics`.
- Do not remove authority-boundary language.
- Do not mark this skill as `adapted` without a skill-import AgentJob and validation receipt.
- Keep examples portable and free of private project assumptions.
- If the upstream template changes, record the review date and adaptation decision.
- Keep this adapter scoped to Codex app rollout/session metrics.
- Do not represent these receipts as OpenAI API billing, ChatGPT usage reporting, or generic telemetry.
- Do not export chat messages, secrets, tool arguments, reasoning content, or full session logs.
- Preserve context-45 fail-closed behavior when metrics are unavailable or incomplete.
