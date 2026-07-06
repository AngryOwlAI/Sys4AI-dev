from __future__ import annotations

import unittest

from sys_for_ai.memory import lookup_memory, memory_status


class MemoryLookupTests(unittest.TestCase):
    def test_lookup_known_prd_source(self) -> None:
        payload = lookup_memory("SRC-PRD-P0")
        self.assertTrue(payload["ok"])
        result = payload["result"]
        self.assertIsInstance(result, dict)
        self.assertEqual(result["path"], "PRDs/sys-for-ai_phase-0_product_system_design_prd.md")
        self.assertEqual(result["required_next_action"], "inspect_canonical_source")

    def test_memory_status_reports_objects(self) -> None:
        payload = memory_status()
        self.assertTrue(payload["ok"])
        self.assertGreater(payload["objects_count"], 0)


if __name__ == "__main__":
    unittest.main()
