from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest

import yaml

from sys_for_ai.cli import build_parser
from sys_for_ai.strategic_metrics import validate_strategic_vision_measurement


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT = PRODUCT_ROOT / "assurance/strategic_vision_measurement_tx35.yaml"
SCHEMA = PRODUCT_ROOT / "schemas/contracts/strategic_vision_measurement.schema.json"
ACCEPTANCE_DECISION = PRODUCT_ROOT / (
    "control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-013.yaml"
)


class StrategicMetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = yaml.safe_load(MEASUREMENT.read_text(encoding="utf-8"))

    def test_live_measurement_reproduces_four_results(self) -> None:
        result = validate_strategic_vision_measurement(MEASUREMENT, SCHEMA, PRODUCT_ROOT)
        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("4/4" in message for message in result.messages))
        self.assertTrue(any("accepted by the accountable human" in message for message in result.messages))

    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-strategic-metrics"])
        self.assertEqual("validate-strategic-metrics", args.command)
        makefile = (PRODUCT_ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("validate-strategic-metrics:", makefile)

    def test_inflated_result_fails(self) -> None:
        data = copy.deepcopy(self.document)
        data["metrics"][0]["result"]["numerator"] = 12
        result = self._validate(data)
        self.assertFalse(result.ok)
        self.assertTrue(any("does not match recomputed" in message for message in result.messages))

    def test_relaxed_threshold_fails(self) -> None:
        data = copy.deepcopy(self.document)
        data["metrics"][0]["threshold"]["value"] = 0.9
        result = self._validate(data)
        self.assertFalse(result.ok)
        self.assertTrue(any("1.0 was expected" in message for message in result.messages))

    def test_model_self_approval_fails(self) -> None:
        data = copy.deepcopy(self.document)
        data["acceptance"]["model_self_approval"] = True
        result = self._validate(data)
        self.assertFalse(result.ok)
        self.assertTrue(any("False was expected" in message for message in result.messages))

    def test_pending_status_fails_after_accountable_acceptance(self) -> None:
        data = copy.deepcopy(self.document)
        data["acceptance"]["result_status"] = "pending_human_acceptance"
        result = self._validate(data)
        self.assertFalse(result.ok)
        self.assertTrue(any("accepted_by_accountable_human" in message for message in result.messages))

    def test_missing_human_acceptance_evidence_fails(self) -> None:
        data = copy.deepcopy(self.document)
        data["acceptance"]["acceptance_evidence_ids"] = []
        result = self._validate(data)
        self.assertFalse(result.ok)
        self.assertTrue(any("too short" in message for message in result.messages))

    def test_counterfeit_human_acceptance_decision_fails(self) -> None:
        decision = yaml.safe_load(ACCEPTANCE_DECISION.read_text(encoding="utf-8"))
        decision["human_authorization"]["model_self_approval"] = True
        with tempfile.TemporaryDirectory() as temporary:
            decision_path = Path(temporary) / "decision.yaml"
            decision_path.write_text(yaml.safe_dump(decision, sort_keys=False), encoding="utf-8")
            result = validate_strategic_vision_measurement(
                MEASUREMENT,
                SCHEMA,
                PRODUCT_ROOT,
                decision_path,
            )
        self.assertFalse(result.ok)
        self.assertTrue(any("lacks exact accountable human decision evidence" in message for message in result.messages))

    @staticmethod
    def _validate(data: dict):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "measurement.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            return validate_strategic_vision_measurement(path, SCHEMA, PRODUCT_ROOT)


if __name__ == "__main__":
    unittest.main()
