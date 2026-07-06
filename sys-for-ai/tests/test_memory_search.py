from __future__ import annotations

import unittest

from sys_for_ai.memory import search_memory


class MemorySearchTests(unittest.TestCase):
    def test_search_returns_deterministic_hits(self) -> None:
        payload = search_memory("source-first memory", limit=5)
        self.assertTrue(payload["ok"])
        hits = payload["hits"]
        self.assertIsInstance(hits, list)
        self.assertGreater(len(hits), 0)
        scores = [hit["score"] for hit in hits]
        self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main()
