---
name: role-catalog-governance
description: Govern role catalogs, role-to-skill crosswalks, and role execution bindings.
---

# Role Catalog Governance

Use this skill when an explicit project authority requires creating, reviewing, validating, or repairing controlled role definitions, role-to-skill crosswalk rows, or role execution bindings.

## Procedure

1. Identify the subject system layer and the role registry rows in scope.
2. Confirm every role has a mission, allowed artifact classes, authority limits, and validation obligations.
3. Check required, optional, conditional, and forbidden skill bindings against active or proposed skill registries.
4. Verify temporary role bindings declare expiry and do not outlive their explicit authority.
5. Run the role validator and record any residual risk in the completion receipt.

## Boundary

Do not add project-specific domain authority to a core role. Route project-specific role needs through a project or domain pack.
