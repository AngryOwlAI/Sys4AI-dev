from __future__ import annotations

import copy
import csv
import hashlib
import io
import tempfile
import unittest
from pathlib import Path

from sys_for_ai.jsonschema_io import check_schema, load_json, validate_instance
from sys_for_ai.trace_migration import (
    GENERALIZED_HEADER,
    LEGACY_HEADER,
    TX11_LEGACY_SHA256,
    TX12_REVIEW_DATE,
    TX12_REVIEW_OWNER,
    migrate_legacy_trace_row,
    migrate_requirement_trace_registry,
    reverse_generalized_trace_row,
    row_uses_legacy_runtime_evidence,
    validate_requirement_trace_migration,
)


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PRODUCT_ROOT / "schemas/contracts/requirement_trace_registry_row.schema.json"
TRACE_PATH = PRODUCT_ROOT / "registries/requirement_trace_registry.csv"


class TraceSchemaMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        with TRACE_PATH.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            cls.live_header = tuple(reader.fieldnames or ())
            cls.live_rows = list(reader)
        if cls.live_header == GENERALIZED_HEADER:
            cls.tx12_rows = [
                row for row in cls.live_rows
                if row["requirement_source_id"] == "SRC-PRD-P0"
            ]
            cls.additive_rows = [
                row for row in cls.live_rows
                if row["requirement_source_id"] != "SRC-PRD-P0"
            ]
            cls.legacy_rows = [reverse_generalized_trace_row(row) for row in cls.tx12_rows]
            cls.generalized = next(
                row for row in cls.tx12_rows
                if not row["implementation_artifacts"] and not row["validation_evidence"]
            )
        else:
            cls.legacy_rows = cls.live_rows
            cls.tx12_rows = []
            cls.additive_rows = []
            cls.generalized = migrate_legacy_trace_row(cls.legacy_rows[0])

    def test_schema_is_valid_draft_2020_12(self) -> None:
        self.assertEqual([], check_schema(self.schema))

    def test_reconstructed_legacy_row_remains_valid_during_transition(self) -> None:
        self.assertEqual([], validate_instance(self.legacy_rows[0], self.schema))

    def test_generalized_row_passes(self) -> None:
        self.assertEqual([], validate_instance(self.generalized, self.schema))
        self.assertEqual(GENERALIZED_HEADER, tuple(self.generalized))

    def test_generalized_row_is_exactly_reversible(self) -> None:
        legacy = next(row for row in self.legacy_rows if row["trace_id"] == self.generalized["trace_id"])
        expected = {field: legacy[field] for field in LEGACY_HEADER}
        self.assertEqual(expected, reverse_generalized_trace_row(self.generalized))

    def test_covered_does_not_imply_implemented(self) -> None:
        data = copy.deepcopy(self.generalized)
        data["coverage_status"] = "covered"
        data["capability_status"] = "absent"
        self.assertEqual([], validate_instance(data, self.schema))

    def test_optional_profile_is_independent_of_coverage_and_capability(self) -> None:
        data = copy.deepcopy(self.generalized)
        data["requirement_id"] = "SFA-P1-INIT-EVID-002"
        data["applicability_status"] = "optional_profile"
        data["coverage_status"] = "covered"
        data["capability_status"] = "absent"
        self.assertEqual([], validate_instance(data, self.schema))

    def test_implemented_requires_implementation_artifact(self) -> None:
        self._assert_mutation_fails(
            lambda data: data.__setitem__("capability_status", "implemented")
        )

    def test_operational_requires_current_passing_evidence(self) -> None:
        data = copy.deepcopy(self.generalized)
        data["capability_status"] = "operational"
        data["implementation_artifacts"] = "Sys4AI/sys_for_ai/trace_migration.py"
        self.assertNotEqual([], validate_instance(data, self.schema))
        data["verification_status"] = "pass"
        data["evidence_status"] = "current"
        data["validation_evidence"] = "Sys4AI/tests/test_trace_schema_migration.py"
        self.assertEqual([], validate_instance(data, self.schema))

    def test_removed_rejects_active_implementation_path(self) -> None:
        data = copy.deepcopy(self.generalized)
        data["capability_status"] = "removed"
        data["evidence_status"] = "historical"
        data["implementation_artifacts"] = "Sys4AI/sys_for_ai/removed_runtime.py"
        self.assertNotEqual([], validate_instance(data, self.schema))

    def test_pass_requires_validation_evidence(self) -> None:
        self._assert_mutation_fails(
            lambda data: data.__setitem__("verification_status", "pass")
        )

    def test_waiver_requires_waiver_id(self) -> None:
        self._assert_mutation_fails(
            lambda data: data.__setitem__("verification_status", "waived")
        )

    def test_nonwaived_row_rejects_waiver_id(self) -> None:
        self._assert_mutation_fails(
            lambda data: data.__setitem__("verification_waiver_id", "WAIVER-001")
        )

    def test_reviewed_row_requires_review_date(self) -> None:
        self._assert_mutation_fails(
            lambda data: data.__setitem__("semantic_review_date", "")
        )

    def test_not_reviewed_row_rejects_review_date(self) -> None:
        self._assert_mutation_fails(
            lambda data: data.__setitem__("semantic_review_verdict", "not_reviewed")
        )

    def test_live_registry_preserves_tx12_and_accepts_additive_rows(self) -> None:
        before = TRACE_PATH.read_bytes()
        result = validate_requirement_trace_migration(TRACE_PATH, SCHEMA_PATH)
        self.assertTrue(result.ok, result.messages)
        self.assertIn(
            "rows=227 tx12_rows=214 additive_rows=13 trace_ids=227 requirement_ids=227",
            result.messages,
        )
        self.assertEqual(before, TRACE_PATH.read_bytes())
        self.assertEqual(GENERALIZED_HEADER, self.live_header)

    def test_live_registry_reconstructs_exact_tx11_baseline(self) -> None:
        buffer = io.StringIO(newline="")
        writer = csv.DictWriter(buffer, fieldnames=LEGACY_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(self.legacy_rows)
        digest = hashlib.sha256(buffer.getvalue().encode("utf-8")).hexdigest()
        self.assertEqual(TX11_LEGACY_SHA256, digest)

    def test_all_214_rows_have_accountable_nonprovisional_review(self) -> None:
        self.assertEqual(214, len(self.tx12_rows))
        for row in self.tx12_rows:
            self.assertEqual("active", row["requirement_lifecycle"])
            self.assertEqual("required", row["applicability_status"])
            self.assertNotEqual("not_run", row["verification_status"])
            self.assertNotEqual("missing", row["evidence_status"])
            self.assertEqual(TX12_REVIEW_OWNER, row["semantic_review_owner"])
            self.assertIn(row["semantic_review_date"], {TX12_REVIEW_DATE, "2026-07-11"})
            self.assertNotEqual("not_reviewed", row["semantic_review_verdict"])

    def test_reviewed_dimension_counts_are_stable(self) -> None:
        def counts(field: str) -> dict[str, int]:
            values = [row[field] for row in self.tx12_rows]
            return {value: values.count(value) for value in sorted(set(values))}

        self.assertEqual({"covered": 79, "partial": 135}, counts("coverage_status"))
        self.assertEqual(
            {"absent": 5, "implemented": 72, "scaffolded": 137},
            counts("capability_status"),
        )
        self.assertEqual({"pass": 18, "planned": 196}, counts("verification_status"))
        self.assertEqual(
            {"sufficient": 214},
            counts("semantic_review_verdict"),
        )

    def test_legacy_runtime_evidence_never_implies_operational_capability(self) -> None:
        affected = [row for row in self.tx12_rows if row_uses_legacy_runtime_evidence(row)]
        self.assertEqual(32, len(affected))
        self.assertTrue(all(row["capability_status"] != "operational" for row in affected))

    def test_additive_phase2_rows_record_exact_tx16_walking_skeleton_evidence(self) -> None:
        self.assertEqual(13, len(self.additive_rows))
        self.assertTrue(
            all(row["requirement_source_id"] == "SRC-PRD-P2-STRATEGIC-BASELINE-ADDENDUM" for row in self.additive_rows)
        )
        self.assertTrue(all(row["semantic_review_owner"] == "requirements_manager" for row in self.additive_rows))
        self.assertTrue(all(row["coverage_status"] == "covered" for row in self.additive_rows))
        self.assertTrue(all(row["capability_status"] == "implemented" for row in self.additive_rows))
        self.assertTrue(all(row["verification_status"] == "pass" for row in self.additive_rows))
        self.assertTrue(all(row["implementation_artifacts"] for row in self.additive_rows))
        self.assertTrue(all("tests/test_walking_skeleton.py" in row["validation_evidence"] for row in self.additive_rows))
        self.assertTrue(all("TX-16" in row["semantic_justification"] for row in self.additive_rows))

    def test_atomic_writer_migrates_exact_legacy_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "requirement_trace_registry.csv"
            self._write_legacy_rows(path, self.legacy_rows)
            result = migrate_requirement_trace_registry(path, SCHEMA_PATH)
            self.assertTrue(result.ok, result.messages)
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(GENERALIZED_HEADER, tuple(reader.fieldnames or ()))
                self.assertEqual(214, len(list(reader)))

    def test_atomic_writer_rejects_uncontrolled_review_date_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "requirement_trace_registry.csv"
            self._write_legacy_rows(path, self.legacy_rows)
            before = path.read_bytes()
            result = migrate_requirement_trace_registry(path, SCHEMA_PATH, "2026-07-11")
            self.assertFalse(result.ok)
            self.assertEqual(before, path.read_bytes())

    def test_duplicate_trace_id_fails_dry_run(self) -> None:
        rows = [copy.deepcopy(self.legacy_rows[0]), copy.deepcopy(self.legacy_rows[1])]
        rows[1]["trace_id"] = rows[0]["trace_id"]
        result = self._validate_temp_rows(rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("duplicate trace ID" in message for message in result.messages))

    def test_header_drift_fails_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "requirement_trace_registry.csv"
            path.write_text("trace_id,coverage_status\nTRACE-X,covered\n", encoding="utf-8")
            result = validate_requirement_trace_migration(path, SCHEMA_PATH)
        self.assertFalse(result.ok)
        self.assertTrue(any("exact legacy or generalized header" in message for message in result.messages))

    def test_extra_csv_value_fails_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "requirement_trace_registry.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(LEGACY_HEADER)
                writer.writerow([self.legacy_rows[0][field] for field in LEGACY_HEADER] + ["extra"])
            result = validate_requirement_trace_migration(path, SCHEMA_PATH)
        self.assertFalse(result.ok)
        self.assertTrue(any("unexpected extra CSV values" in message for message in result.messages))

    def _assert_mutation_fails(self, mutate) -> None:
        data = copy.deepcopy(self.generalized)
        mutate(data)
        self.assertNotEqual([], validate_instance(data, self.schema))

    def _validate_temp_rows(self, rows: list[dict[str, str]]):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "requirement_trace_registry.csv"
            self._write_legacy_rows(path, rows)
            return validate_requirement_trace_migration(path, SCHEMA_PATH)

    @staticmethod
    def _write_legacy_rows(path: Path, rows: list[dict[str, str]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=LEGACY_HEADER, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
