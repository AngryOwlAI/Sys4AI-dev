from __future__ import annotations

import csv
from pathlib import Path
import tempfile
import unittest

from sys_for_ai.evidence_closure import (
    LEDGER_FIELDS,
    expected_evidence_closure_rows,
    validate_evidence_closure_plan,
    validate_local_evidence_execution,
    write_evidence_closure_ledger,
)


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "registries/requirement_trace_registry.csv"
LEDGER = ROOT / "registries/evidence_closure_plan_registry.csv"
EXECUTION = ROOT / "registries/local_evidence_execution_registry.csv"


class EvidenceClosureTests(unittest.TestCase):
    def test_live_tx23_ledger_is_frozen_and_tx24_closures_validate(self) -> None:
        before = TRACE.read_bytes()
        result = validate_evidence_closure_plan(TRACE, LEDGER)
        self.assertTrue(result.ok, result.messages)
        self.assertEqual(before, TRACE.read_bytes())

        rows = self._read(LEDGER)
        self.assertEqual(484, len(rows))
        self.assertEqual(74, sum(row["closure_route"] == "locally_executable_evidence" for row in rows))
        self.assertEqual(410, sum(row["closure_route"] == "plan_supersession_candidate" for row in rows))
        self.assertTrue(all(row["status"] == "planned" for row in rows))
        execution = self._read(EXECUTION)
        self.assertEqual(7, len(execution))
        self.assertTrue(all(row["status"] == "accepted" for row in execution))
        self.assertTrue(validate_local_evidence_execution(TRACE, LEDGER, EXECUTION).ok)

    def test_missing_obligation_fails(self) -> None:
        rows = self._read(LEDGER)[1:]
        result = self._validate_rows(rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("activated TX-23 ledger bytes changed" in item for item in result.messages))

    def test_bulk_promotion_fails(self) -> None:
        rows = self._read(LEDGER)
        rows[0]["status"] = "complete"
        result = self._validate_rows(rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("must remain planned" in item or "activated TX-23 ledger bytes changed" in item for item in result.messages))

    def test_current_open_builder_excludes_accepted_semantic_closures(self) -> None:
        expected = expected_evidence_closure_rows(self._read(TRACE))
        self.assertEqual(477, len(expected))
        self.assertEqual(200, sum(row["gap_dimension"] == "verification" for row in expected))
        self.assertEqual(142, sum(row["gap_dimension"] == "capability" for row in expected))
        self.assertEqual(135, sum(row["gap_dimension"] == "coverage" for row in expected))
        self.assertEqual(0, sum(row["gap_dimension"] == "semantic_review" for row in expected))

    def test_frozen_ledger_generator_refuses_rewrite(self) -> None:
        result = write_evidence_closure_ledger(TRACE, LEDGER)
        self.assertFalse(result.ok)
        self.assertTrue(any("frozen after local evidence execution" in item for item in result.messages))

    def test_unexpected_local_closure_fails(self) -> None:
        rows = self._read(EXECUTION)[:-1]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "local.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            result = validate_local_evidence_execution(TRACE, LEDGER, path)
        self.assertFalse(result.ok)
        self.assertTrue(any("exactly the seven authorized" in item for item in result.messages))

    def _validate_rows(self, rows: list[dict[str, str]]):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "ledger.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            return validate_evidence_closure_plan(TRACE, path)

    @staticmethod
    def _read(path: Path) -> list[dict[str, str]]:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
