# Self-Hosting Boundary Policy

**Status:** Controlled
**Scope:** `Sys4AI-dev` dogfooding `Sys4AI` Phase 1 bounded-execution concepts

**Authority note:** Registered as `SRC-SELFHOST-BOUNDARY-POLICY`. This policy
does not grant write, approval, permission, production, or operational
authority.

---

## Policy

`Sys4AI-dev` is allowed to use `Sys4AI` concepts while building `Sys4AI`, provided every operational record keeps these roles distinct:

- Framework system: `Sys4AI`
- Development system: `Sys4AI-dev`
- Target system: the system currently being changed

For this implementation, the target system is also `Sys4AI`, so `self_hosting_mode` is true and `reflection_depth` is 1.

## Boundary rules

1. PRDs define product requirements.
2. `Sys4AI/` is the product scaffold.
3. `.agents/skills/` is the active development runtime skill surface.
4. `.codex/skills/` is a compatibility surface.
5. `Sys4AI/docs/generated/` is a generated reader surface.
6. `Sys4AI/.local/` is local retrieval or receipt support.

## Anti-rules

- Do not treat a generated page as canonical by convenience.
- Do not let a local cache or chat summary authorize a code change.
- Do not collapse active development skills into product scaffold skills.
- Do not run multiple ExecutionTransactions through one `resume operation` invocation.
