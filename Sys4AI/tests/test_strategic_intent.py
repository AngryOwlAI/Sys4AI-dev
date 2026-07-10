from __future__ import annotations

from datetime import date
from pathlib import Path
import shutil
import tempfile
import unittest

from sys_for_ai.cli import build_parser
from sys_for_ai.strategic_intent import STRUCTURAL_LIMITATION, validate_strategic_intent


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = PRODUCT_ROOT / "examples/strategic_intent"


class StrategicIntentTests(unittest.TestCase):
    def test_registered_templates_and_examples_pass(self) -> None:
        result = validate_strategic_intent()
        self.assertTrue(result.ok, result.messages)
        self.assertIn(STRUCTURAL_LIMITATION, result.messages)

    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-strategic-intent"])
        self.assertEqual("validate-strategic-intent", args.command)
        makefile = (PRODUCT_ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("validate-strategic-intent:", makefile)

    def test_missing_vision_file_fails_pair_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copy2(EXAMPLES / "greenfield/core-values.md", root / "core-values.md")
            result = validate_strategic_intent(root)
        self.assertFalse(result.ok)
        self.assertTrue(any("missing pair artifact" in item for item in result.messages))

    def test_missing_core_values_file_fails_pair_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copy2(EXAMPLES / "greenfield/vision-statement.md", root / "vision-statement.md")
            result = validate_strategic_intent(root)
        self.assertFalse(result.ok)
        self.assertTrue(any("missing pair artifact" in item for item in result.messages))

    def test_duplicate_vision_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("a", "b"):
                target = root / name
                target.mkdir()
                shutil.copy2(EXAMPLES / "greenfield/vision-statement.md", target / "vision-statement.md")
                shutil.copy2(EXAMPLES / "greenfield/core-values.md", target / "core-values.md")
            result = validate_strategic_intent(root)
        self.assertFalse(result.ok)
        self.assertTrue(any("duplicate strategic-intent ID 'VISION-GREENFIELD-001'" in item for item in result.messages))

    def test_approved_candidate_id_fails(self) -> None:
        result = self._mutated_vision("vision_id: VISION-GREENFIELD-001", "vision_id: VISION-CAND-GREENFIELD-001")
        self.assertFalse(result.ok)
        self.assertTrue(any("VISION-(?!CAND-)" in item for item in result.messages))

    def test_model_self_approval_fails(self) -> None:
        result = self._mutated_vision("approved_by: Example Product Owner", "approved_by: model")
        self.assertFalse(result.ok)
        self.assertTrue(any("accountable non-model principal" in item for item in result.messages))

    def test_candidate_cannot_be_marked_approved_without_evidence(self) -> None:
        result = self._mutated_file(
            "brownfield/vision-statement.md",
            "content_approval_state: stakeholder_review",
            "content_approval_state: approved",
        )
        self.assertFalse(result.ok)
        self.assertTrue(any("approval" in item and "approved" in item for item in result.messages))

    def test_invalid_approval_date_fails(self) -> None:
        result = self._mutated_vision('approved_at: "2026-07-09"', 'approved_at: "not-a-date"')
        self.assertFalse(result.ok)
        self.assertTrue(any("valid approval date" in item for item in result.messages))

    def test_missing_source_evidence_heading_fails(self) -> None:
        result = self._mutated_vision(
            "## Source Evidence And RDR Candidates",
            "## Source Notes",
        )
        self.assertFalse(result.ok)
        self.assertTrue(any("Source Evidence And RDR Candidates" in item for item in result.messages))

    def test_stale_hash_fails(self) -> None:
        result = self._mutated_vision("Every maintenance request", "Each maintenance request")
        self.assertFalse(result.ok)
        self.assertTrue(any("stale source_hash" in item for item in result.messages))

    def test_superseded_document_cannot_remain_active(self) -> None:
        result = self._mutated_vision("superseded_by: null", "superseded_by: VISION-GREENFIELD-002")
        self.assertFalse(result.ok)
        self.assertTrue(any("cannot remain active" in item for item in result.messages))

    def test_expired_waiver_fails(self) -> None:
        replacement = """waiver:
  waiver_id: WAIVER-EXAMPLE-001
  accountable_authority: Example Product Owner
  missing_artifact_or_approval: stakeholder evidence
  reason: fixture
  risk: fixture
  scope: fixture
  downstream_handling: blocked
  expiry: \"2026-01-01\"
  revisit_trigger: evidence arrives
  affected_requirements_and_decisions:
    - SFA-CORE-VISION-001
  status: active"""
        result = self._mutated_vision("waiver:\n  status: none", replacement, today=date(2026, 7, 10))
        self.assertFalse(result.ok)
        self.assertTrue(any("waiver expired" in item for item in result.messages))

    def test_values_require_decision_tests(self) -> None:
        result = self._mutated_values("## Decision Tests", "## Missing Decision Tests")
        self.assertFalse(result.ok)
        self.assertTrue(any("Decision Tests" in item for item in result.messages))

    def test_duplicate_value_id_fails(self) -> None:
        result = self._mutated_values("  - VALUE-GREENFIELD-002", "  - VALUE-GREENFIELD-001")
        self.assertFalse(result.ok)
        self.assertTrue(any("non-unique elements" in item or "duplicate strategic-intent ID" in item for item in result.messages))

    def test_values_cannot_expand_permissions(self) -> None:
        result = self._mutated_values(
            "Law, platform policy, safety, security, privacy, source authority, permissions, and required human approval outrank these values.",
            "These values control every other concern.",
        )
        self.assertFalse(result.ok)
        self.assertTrue(any("permission expansion" in item for item in result.messages))

    def test_target_value_cannot_override_safety(self) -> None:
        result = self._mutated_values(
            "Law, platform policy, safety, security, privacy, source authority, permissions, and required human approval outrank these values.",
            "Target values outrank safety, security, privacy, permissions, law, and human approval.",
        )
        self.assertFalse(result.ok)
        self.assertTrue(any("permission expansion" in item for item in result.messages))

    def _mutated_vision(self, old: str, new: str, *, today: date | None = None):
        return self._mutated_file("greenfield/vision-statement.md", old, new, today=today)

    def _mutated_values(self, old: str, new: str):
        return self._mutated_file("greenfield/core-values.md", old, new)

    def _mutated_file(self, relative: str, old: str, new: str, *, today: date | None = None):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / Path(relative).name
            text = (EXAMPLES / relative).read_text(encoding="utf-8")
            self.assertIn(old, text)
            target.write_text(text.replace(old, new, 1), encoding="utf-8")
            return validate_strategic_intent(target, today=today)


if __name__ == "__main__":
    unittest.main()
