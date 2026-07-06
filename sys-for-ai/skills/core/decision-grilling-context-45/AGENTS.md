# Maintenance rules for `decision-grilling-context-45`

- Preserve provenance to `skills/decision-grilling-context-45`.
- Do not remove authority-boundary language.
- Do not mark this skill as `adapted` without a skill-import AgentJob and validation receipt.
- Keep examples portable and free of private project assumptions.
- Do not create, overwrite, or refresh `temp_prd.md` after each question when context is still safe.
- Preserve the normal-invocation archive preflight and the `temp_prd` resume bypass.
- Do not archive or overwrite an existing `temp_prd.md` without explicit user confirmation.
- Keep the end-of-questioning `/conversation-to-prd` prompt synchronized across `SKILL.md`, `README.md`, examples, and manifests.
- Do not create a PRD automatically; require explicit user confirmation.
- If the upstream template changes, record the review date and adaptation decision.
