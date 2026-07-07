# Portable Example

User:

```text
/init brownfield
```

Expected agent behavior:

1. Inspect repository evidence in read-only mode.
2. Classify the situation as brownfield, partially built, or documentation recovery.
3. Identify the system-of-interest, subject layer, lifecycle intent, available evidence, and missing evidence.
4. Summarize the current-state baseline in chat.
5. Ask before writing a Current-State Baseline or Requirements Discovery Record.
6. Ask again before creating a Product Requirements Document, implementation plan, AgentJob, or scaffold.

Required approval prompt:

```text
I have enough evidence to create a draft Requirements Discovery Record. Should I write it to the controlled discovery area? This will not modify source code or install scaffolding.
```

