# Portable Example

Input:

```text
/init greenfield
```

Expected behavior:

1. Ask what system the user wants to develop if it is not already clear.
2. Identify the likely subject layer and lifecycle goal.
3. Route to `system-definition-interview-context-45` when discovery may be long.
4. Ask before writing a Requirements Discovery Record.
5. Ask before creating a Product Requirements Document, system requirements, implementation plan, AgentJob, or scaffold.

Input:

```text
/init brownfield
```

Expected behavior:

1. Inspect the repository in read-only mode.
2. Summarize existing evidence, risks, missing authority, and likely Sys4AI adoption route.
3. Ask before writing a Current-State Baseline or Requirements Discovery Record.
4. Ask before creating an implementation plan or AgentJob for governance adoption.

