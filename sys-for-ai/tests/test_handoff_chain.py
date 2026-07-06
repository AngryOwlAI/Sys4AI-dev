"""Tests for operational handoff chains."""

from __future__ import annotations

import unittest

from sys_for_ai.control_loop.handoff import load_handoff_by_id, next_agentjob_from_handoff
from sys_for_ai.validators import validate_handoffs


class HandoffChainTests(unittest.TestCase):
    def test_handoff_examples_validate(self) -> None:
        result = validate_handoffs("control_records/handoffs")
        self.assertTrue(result.ok, result.messages)

    def test_handoff_next_agentjob_is_extractable(self) -> None:
        handoff = load_handoff_by_id("HANDOFF-P1-SELFHOST-CONTINUE-KERNEL-001")
        self.assertIsNotNone(handoff)
        self.assertEqual("AJ-P1-BOUNDARY-VALIDATORS-001", next_agentjob_from_handoff(handoff))


if __name__ == "__main__":
    unittest.main()
