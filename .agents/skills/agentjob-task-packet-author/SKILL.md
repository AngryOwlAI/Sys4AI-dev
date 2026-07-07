---
name: agentjob-task-packet-author
description: Convert implementation plans into bounded AgentJobs and task packets.
---

# AgentJob Task Packet Author

Use this skill when a plan, handoff, or Director decision needs to become one executable bounded AgentJob.

## Procedure

1. Identify the authoritative source plan, handoff, or Director decision.
2. Define exactly one objective, role, subject system, and layer.
3. Declare allowed reads, allowed writes, forbidden actions, validators, and stop conditions.
4. Check that the packet cannot execute multiple independent jobs.
5. Validate and record the AgentJob boundary before execution.

## Boundary

This skill authors task boundaries. It does not authorize execution without the required Director decision and program-state route.
