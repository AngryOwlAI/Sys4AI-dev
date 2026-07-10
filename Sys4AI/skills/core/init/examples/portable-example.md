# Portable Example

Input:

```text
/init greenfield
```

Expected behavior:

1. Ask what system the user wants to develop if it is not already clear.
2. Identify the likely subject layer and lifecycle goal.
3. Identify candidate vision and value evidence, anti-values, missing stakeholders, approval principal, conflicts, waiver state, and review cadence.
4. Route to `system-definition-interview-context-45` when discovery may be long.
5. Ask before writing a Requirements Discovery Record.
6. Ask before creating a Product Requirements Document, system requirements, implementation plan, or scaffold.

Input:

```text
/init brownfield
```

Expected behavior:

1. Inspect the repository in read-only mode.
2. Summarize existing evidence, risks, missing authority, and likely Sys4AI adoption route.
3. Ask before writing a Current-State Baseline or Requirements Discovery Record.
4. Ask before creating an implementation plan for governance adoption.
