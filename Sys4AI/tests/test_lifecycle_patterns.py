from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from sys_for_ai.cli import build_parser
from sys_for_ai.lifecycle_patterns import (
    PATTERN_DECISION_FIELDS,
    STRUCTURAL_LIMITATION,
    validate_lifecycle_and_patterns,
    validate_pattern_decision,
    validate_transition,
)


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
PHASE0 = PRODUCT_ROOT.parent / "PRDs/Sys4AI_phase-0_product_system_design_prd.md"


class LifecyclePatternTests(unittest.TestCase):
    def test_current_lifecycle_and_pattern_baseline_passes(self) -> None:
        result = validate_lifecycle_and_patterns(PHASE0)
        self.assertTrue(result.ok, result.messages)
        self.assertIn(STRUCTURAL_LIMITATION, result.messages)

    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-lifecycle-and-patterns"])
        self.assertEqual("validate-lifecycle-and-patterns", args.command)
        self.assertIn(
            "validate-lifecycle-and-patterns:",
            (PRODUCT_ROOT / "Makefile").read_text(encoding="utf-8"),
        )

    def test_missing_lifecycle_stage_fails(self) -> None:
        result = self._mutated_prd("##### Retire", "##### Removed")
        self.assertFalse(result.ok)
        self.assertTrue(any("missing lifecycle stage Retire" in item for item in result.messages))

    def test_missing_stage_contract_field_fails(self) -> None:
        result = self._mutated_prd("| Permission requirements |", "| Missing permission field |")
        self.assertFalse(result.ok)
        self.assertTrue(any("missing contract field 'Permission requirements'" in item for item in result.messages))

    def test_invalid_transition_fails(self) -> None:
        result = validate_transition(
            "Design",
            "Run",
            {"authority": "A", "verification": "V", "rollback": "R", "next_state_owner": "O"},
        )
        self.assertFalse(result.ok)
        self.assertTrue(any("invalid lifecycle transition" in item for item in result.messages))

    def test_run_transition_requires_human_approval(self) -> None:
        result = validate_transition(
            "Test",
            "Run",
            {"authority": "A", "verification": "V", "rollback": "R", "next_state_owner": "O"},
        )
        self.assertFalse(result.ok)
        self.assertTrue(any("human approval" in item for item in result.messages))

    def test_complete_prototype_pattern_decision_passes(self) -> None:
        decision = {field: f"evidence-{field}" for field in PATTERN_DECISION_FIELDS}
        decision["coordination_pattern"] = "role_based_multi_agent"
        decision["operational_maturity"] = "prototype"
        result = validate_pattern_decision(decision)
        self.assertTrue(result.ok, result.messages)

    def test_missing_pattern_decision_fails(self) -> None:
        result = validate_pattern_decision({})
        self.assertFalse(result.ok)
        self.assertTrue(any("pattern decision missing" in item for item in result.messages))

    def test_production_promotion_without_evidence_fails(self) -> None:
        decision = {field: f"evidence-{field}" for field in PATTERN_DECISION_FIELDS}
        decision["coordination_pattern"] = "production_orchestration"
        decision["operational_maturity"] = "production_approved"
        result = validate_pattern_decision(decision)
        self.assertFalse(result.ok)
        self.assertTrue(any("production maturity requires evaluation evidence" in item for item in result.messages))

    def _mutated_prd(self, old: str, new: str):
        text = PHASE0.read_text(encoding="utf-8")
        self.assertIn(old, text)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "phase0.md"
            path.write_text(text.replace(old, new, 1), encoding="utf-8")
            return validate_lifecycle_and_patterns(path)


if __name__ == "__main__":
    unittest.main()
