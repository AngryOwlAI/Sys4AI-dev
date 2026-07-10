# Strategic-Intent Contract Examples

These examples exercise the target vision and core-values contracts without becoming target-system authority.

- `greenfield/` shows a candidate that received stakeholder review, rejected one value candidate, resolved a value conflict, and reached accountable human approval.
- `brownfield/` extracts implied intent from observed behavior, labels the inference, rejects one unsafe value candidate, and remains blocked in stakeholder review because affected operators and the accountable approver have not confirmed it.

The examples are `derivative_draft` evidence. Names, dates, evidence IDs, and hashes are illustrative and grant no real approval or permission.

## Greenfield State Sequence

1. `VISION-CAND-GREENFIELD-001` and candidate value IDs were drafted from example stakeholder evidence.
2. Stakeholder review rejected `VALUE-CAND-GREENFIELD-003` because unqualified delivery speed conflicted with reliability and human override.
3. The retained candidates were revised with a precedence rule.
4. The example product owner approved the resulting stable `VISION-GREENFIELD-001`, `VALUE-GREENFIELD-001`, and `VALUE-GREENFIELD-002` records.

## Brownfield Blocking Sequence

1. Existing runbooks and incident records imply a continuity mission and two candidate values.
2. The examples label those statements as inference rather than stakeholder intent.
3. `VALUE-CAND-BROWNFIELD-003` is rejected because hiding degraded behavior would conflict with operator awareness and evidence integrity.
4. Approval remains blocked until operators, affected users, and the accountable product owner confirm or revise the candidates.

## Source-Hash Convention

The example hash is SHA-256 over LF-normalized UTF-8 Markdown after replacing the `source_hash` front-matter value with `pending`. This avoids self-referential hashing while keeping the algorithm deterministic.
