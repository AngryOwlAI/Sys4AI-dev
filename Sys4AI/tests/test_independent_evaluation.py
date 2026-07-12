from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest

from sys_for_ai.cli import build_parser
from sys_for_ai.independent_evaluation import validate_independent_evaluation_protocol
from sys_for_ai.yaml_io import dump_yaml, load_yaml


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = PRODUCT_ROOT / "assurance/independent_evaluation_protocol_tx37.yaml"
SCHEMA = PRODUCT_ROOT / "schemas/contracts/independent_evaluation_protocol.schema.json"


class IndependentEvaluationProtocolTests(unittest.TestCase):
    def test_current_protocol_passes_at_readiness_boundary(self) -> None:
        result = validate_independent_evaluation_protocol(PROTOCOL, SCHEMA)

        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("evidence is not executed" in item for item in result.messages))
        self.assertTrue(any("pending 4 prerequisites" in item for item in result.messages))

    def test_runtime_or_accountable_principal_cannot_be_external_evaluator(self) -> None:
        protocol = load_yaml(PROTOCOL)
        protocol["independence"]["prohibited_evaluator_ids"] = ["codex_meta_agent_runtime"]

        result = self._validate(protocol)

        self.assertFalse(result.ok)
        self.assertTrue(any("prohibited evaluator identities" in item for item in result.messages))

    def test_nonconfidential_or_repository_stored_holdouts_fail(self) -> None:
        protocol = load_yaml(PROTOCOL)
        protocol["holdout_protection"]["contents_confidential_before_execution"] = False
        protocol["holdout_protection"]["repository_storage_prohibited"] = False

        result = self._validate(protocol)

        self.assertFalse(result.ok)
        self.assertTrue(any("confidential before execution" in item for item in result.messages))
        self.assertTrue(any("must not be stored" in item for item in result.messages))

    def test_relaxed_threshold_or_unexpected_acceptance_tolerance_fails(self) -> None:
        protocol = load_yaml(PROTOCOL)
        protocol["rubric"]["required_pass_fraction"] = 0.95
        protocol["rubric"]["maximum_unexpected_accepts"] = 1

        result = self._validate(protocol)

        self.assertFalse(result.ok)
        self.assertTrue(any("pass fraction must remain 1.0" in item for item in result.messages))
        self.assertTrue(any("unexpected accepts must remain zero" in item for item in result.messages))

    def test_readiness_cannot_claim_execution_or_external_permission(self) -> None:
        protocol = load_yaml(PROTOCOL)
        protocol["evidence_status"] = "executed"
        protocol["permissions"]["TX_37_external_execution_authorized"] = True

        result = self._validate(protocol)

        self.assertFalse(result.ok)
        self.assertTrue(any("cannot claim executed" in item for item in result.messages))
        self.assertTrue(any("external_execution_authorized" in item for item in result.messages))

    def test_bound_public_artifact_hash_drift_fails(self) -> None:
        protocol = load_yaml(PROTOCOL)
        protocol["baseline"]["safety_evaluator_sha256"] = "0" * 64

        result = self._validate(protocol)

        self.assertFalse(result.ok)
        self.assertTrue(any("safety evaluator hash mismatch" in item for item in result.messages))

    def test_cli_and_make_expose_direct_and_aggregate_validation(self) -> None:
        args = build_parser().parse_args(
            ["validate-independent-evaluation", "--protocol", str(PROTOCOL), "--schema", str(SCHEMA)]
        )
        makefile = (PRODUCT_ROOT / "Makefile").read_text(encoding="utf-8")

        self.assertEqual("validate-independent-evaluation", args.command)
        self.assertIn("validate-independent-evaluation:", makefile)
        self.assertIn("validate-safety-evaluation validate-independent-evaluation", makefile)

    def _validate(self, protocol: dict[str, object]):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "protocol.yaml"
            dump_yaml(path, copy.deepcopy(protocol))
            return validate_independent_evaluation_protocol(path, SCHEMA)


if __name__ == "__main__":
    unittest.main()
