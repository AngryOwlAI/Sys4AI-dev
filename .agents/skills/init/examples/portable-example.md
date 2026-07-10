# Portable Example

User:

```text
/init brownfield
```

Expected agent behavior:

1. Inspect repository evidence in read-only mode.
2. Classify the situation as brownfield, partially built, or documentation recovery.
3. Identify the system-of-interest, subject layer, lifecycle intent, available evidence, and missing evidence.
4. Identify mission-versus-vision, candidate values and anti-values, missing stakeholders, approval principal, inherited constraints, conflicts, waiver state, and review cadence without implying approval.
5. Summarize the current-state baseline in chat.
6. Ask before writing a Current-State Baseline or Requirements Discovery Record.
7. Ask again before creating a Product Requirements Document, implementation plan, or scaffold.

Required approval prompt:

```text
I have enough evidence to create a draft Requirements Discovery Record. Should I write it to the controlled discovery area? This will not modify source code or install scaffolding.
```
