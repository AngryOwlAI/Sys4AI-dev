from __future__ import annotations

import unittest

from sys_for_ai.control_loop import continue_status
from sys_for_ai.control_loop.state import load_program_state


class ProgramStateTests(unittest.TestCase):
    def test_program_state_loads(self) -> None:
        state = load_program_state()
        self.assertEqual(state.program_state_id, "SFA-PROGRAM-STATE-001")
        self.assertIsNone(state.active_director_decision_id)
        self.assertEqual(state.latest_handoff_id, "HANDOFF-P1-SELFHOST-ACCEPTANCE-001")

    def test_continue_status_reports_state(self) -> None:
        payload = continue_status()
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["packet_type"], "continue_status")


if __name__ == "__main__":
    unittest.main()
