from __future__ import annotations

from collections import Counter
import copy
import csv
import hashlib
from pathlib import Path
import tempfile
import unittest

from sys_for_ai.cli import build_parser
from sys_for_ai.safety_evaluation import (
    EXPECTED_ASSURANCE_ARTIFACTS,
    EXPECTED_VALUE_IDS,
    evaluate_candidate,
    validate_safety_evaluation,
)
from sys_for_ai.yaml_io import dump_yaml, load_yaml


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
PACKET = PRODUCT_ROOT / "assurance/meta_agent_self_change_safety_evaluation.yaml"
HOLDOUTS = PRODUCT_ROOT / "assurance/holdouts/meta_agent_self_change_holdouts.yaml"
PACKET_SCHEMA = PRODUCT_ROOT / "schemas/contracts/self_change_safety_evaluation.schema.json"
HOLDOUT_SCHEMA = PRODUCT_ROOT / "schemas/contracts/self_change_holdout_suite.schema.json"


class SafetyEvaluationTests(unittest.TestCase):
    def test_current_packet_and_protected_holdouts_pass(self) -> None:
        result = validate_safety_evaluation(PACKET, PACKET_SCHEMA, HOLDOUTS, HOLDOUT_SCHEMA)

        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("scenarios=24 positive=3 negative=17 conflict=4" in item for item in result.messages))
        self.assertTrue(
            any(
                "TX-17 snapshot" in item
                and "TX-18" in item
                and "current G-08 status" in item
                and "G-07" in item
                and "current G-07 status" in item
                for item in result.messages
            )
        )

    def test_all_seven_assurance_artifacts_have_exact_ids(self) -> None:
        packet = load_yaml(PACKET)

        self.assertEqual(
            EXPECTED_ASSURANCE_ARTIFACTS,
            {key: packet[key]["artifact_id"] for key in EXPECTED_ASSURANCE_ARTIFACTS},
        )

    def test_holdout_classes_cover_every_candidate_value(self) -> None:
        holdouts = load_yaml(HOLDOUTS)

        for classification in ("positive", "negative", "conflict"):
            covered = {
                value_id
                for scenario in holdouts["scenarios"]
                if scenario["classification"] == classification
                for value_id in scenario["value_ids"]
            }
            self.assertEqual(EXPECTED_VALUE_IDS, covered)

    def test_cli_exposes_direct_safety_validator(self) -> None:
        args = build_parser().parse_args(
            [
                "validate-safety-evaluation",
                str(PACKET),
                "--schema",
                str(PACKET_SCHEMA),
                "--holdouts",
                str(HOLDOUTS),
                "--holdout-schema",
                str(HOLDOUT_SCHEMA),
                "--json",
            ]
        )

        self.assertEqual("validate-safety-evaluation", args.command)
        self.assertTrue(args.json)

    def test_make_target_is_direct_and_aggregate(self) -> None:
        makefile = (PRODUCT_ROOT / "Makefile").read_text(encoding="utf-8")

        self.assertIn("validate-safety-evaluation:", makefile)
        self.assertIn("validate-lifecycle-and-patterns validate-safety-evaluation validate-prd-semantics", makefile)

    def test_role_bindings_make_evaluation_and_assurance_duties_explicit(self) -> None:
        roles = _rows(PRODUCT_ROOT / "registries/role_registry.csv", "role_id")
        bindings = _rows(PRODUCT_ROOT / "registries/role_execution_binding_registry.csv", "role_id")

        verifier = roles["verification_engineer"]
        self.assertIn("evaluation-harness-designer", verifier["required_skills"])
        self.assertIn("holdout-evaluation", verifier["primary_outputs"])
        self.assertIn("framework_product", roles["runtime_maintenance_planner"]["system_layer_scope"])
        for role_id in (
            "security_safety_privacy_compliance_reviewer",
            "verification_engineer",
            "runtime_maintenance_planner",
            "svc_documentation_surface_architect",
        ):
            self.assertIn(role_id, bindings)

    def test_missing_permission_envelope_blocks(self) -> None:
        actual = self._evaluate(permission_envelope_present=False)

        self.assertEqual("block", actual["evaluation_outcome"])
        self.assertEqual(["MISSING_PERMISSION_ENVELOPE"], actual["reason_codes"])

    def test_noncurrent_permission_envelope_blocks(self) -> None:
        actual = self._evaluate(permission_envelope_current=False)

        self.assertEqual(["STALE_OR_INVALID_PERMISSION_ENVELOPE"], actual["reason_codes"])

    def test_values_cannot_expand_permission(self) -> None:
        actual = self._evaluate(values_used_to_expand_permission=True)

        self.assertEqual(["VALUES_CANNOT_EXPAND_PERMISSION"], actual["reason_codes"])

    def test_model_self_approval_blocks(self) -> None:
        actual = self._evaluate(
            approval_principal_id="codex_meta_agent_runtime",
            approval_principal_type="meta_agent_runtime",
        )

        self.assertEqual(["MODEL_SELF_APPROVAL"], actual["reason_codes"])

    def test_proposer_cannot_be_evaluator(self) -> None:
        actual = self._evaluate(evaluator_actor_id="codex_meta_agent_runtime")

        self.assertEqual(["EVALUATOR_NOT_INDEPENDENT"], actual["reason_codes"])

    def test_material_change_requires_distinct_acceptance(self) -> None:
        actual = self._evaluate(acceptance_principal_id="codex_meta_agent_runtime")

        self.assertEqual(["ACCEPTANCE_NOT_INDEPENDENT"], actual["reason_codes"])

    def test_material_change_requires_human_typed_acceptance_principal(self) -> None:
        actual = self._evaluate(acceptance_principal_type="meta_agent_runtime")

        self.assertEqual(["ACCOUNTABLE_HUMAN_ACCEPTANCE_REQUIRED"], actual["reason_codes"])

    def test_proposer_cannot_modify_evaluation_standard(self) -> None:
        actual = self._evaluate(evaluation_standard_modified_by_proposer=True)

        self.assertEqual(["PROPOSER_CONTROLS_EVALUATION_STANDARD"], actual["reason_codes"])

    def test_reflection_expansion_without_complete_control_set_blocks(self) -> None:
        actual = self._evaluate(change_scope="reflection_expansion", reflection_depth=2)

        self.assertEqual(["REFLECTION_EXPANSION_UNAUTHORIZED"], actual["reason_codes"])

    def test_unbounded_recursion_blocks(self) -> None:
        actual = self._evaluate(unbounded_recursion_requested=True)

        self.assertEqual(["UNBOUNDED_RECURSION_PROHIBITED"], actual["reason_codes"])

    def test_cross_layer_write_without_authority_blocks(self) -> None:
        actual = self._evaluate(
            change_scope="target_system_improvement",
            cross_layer_write_requested=True,
        )

        self.assertEqual(["CROSS_LAYER_AUTHORITY_REQUIRED"], actual["reason_codes"])

    def test_unmitigated_hostile_input_blocks(self) -> None:
        actual = self._evaluate(hostile_input_detected=True)

        self.assertEqual(["HOSTILE_INPUT_UNMITIGATED"], actual["reason_codes"])

    def test_unverified_source_authority_blocks(self) -> None:
        actual = self._evaluate(source_authority_verified=False)

        self.assertEqual(["SOURCE_AUTHORITY_UNVERIFIED"], actual["reason_codes"])

    def test_cross_target_access_without_recorded_authority_blocks(self) -> None:
        actual = self._evaluate(cross_target_data_access_requested=True)

        self.assertEqual(["CROSS_TARGET_ACCESS_UNAUTHORIZED"], actual["reason_codes"])

    def test_production_urgency_does_not_override_evidence_or_approval(self) -> None:
        actual = self._evaluate(
            change_scope="production_promotion",
            production_promotion_requested=True,
        )

        self.assertEqual(
            ["PRODUCTION_APPROVAL_REQUIRED", "PRODUCTION_EVIDENCE_INCOMPLETE"],
            actual["reason_codes"],
        )

    def test_threshold_mutation_fails_closed(self) -> None:
        result = self._mutated_validation(
            holdout_mutation=lambda data: data["acceptance_thresholds"].update(
                required_pass_fraction=0.5
            )
        )

        self.assertFalse(result.ok)
        self.assertTrue(any("pass fraction must be 1.0" in item for item in result.messages))

    def test_holdout_digest_drift_fails_closed(self) -> None:
        result = self._mutated_validation(
            holdout_mutation=lambda data: data["scenarios"][0].update(
                target_risk="changed without baseline approval"
            ),
            refresh_digest=False,
        )

        self.assertFalse(result.ok)
        self.assertTrue(any("protected holdout digest mismatch" in item for item in result.messages))

    def test_missing_threat_family_fails(self) -> None:
        result = self._mutated_validation(
            packet_mutation=lambda data: data["threat_model"]["threats"].pop()
        )

        self.assertFalse(result.ok)
        self.assertTrue(any("threat model category coverage is incomplete" in item for item in result.messages))

    def test_protected_phase2_hash_drift_fails(self) -> None:
        def mutate(packet):
            packet["baseline_and_rollback_record"]["protected_artifacts"][0]["sha256"] = "0" * 64

        result = self._mutated_validation(packet_mutation=mutate)

        self.assertFalse(result.ok)
        self.assertTrue(any("protected baseline hash mismatch" in item for item in result.messages))

    def test_preserved_trace_gap_count_drift_fails(self) -> None:
        def mutate(packet):
            packet["baseline_and_rollback_record"]["preserved_trace_state"]["planned_verification"] = 199

        result = self._mutated_validation(packet_mutation=mutate)

        self.assertFalse(result.ok)
        self.assertTrue(any("planned_verification expected 199, found 157" in item for item in result.messages))

    def test_human_acceptance_and_production_claims_remain_gaps(self) -> None:
        packet = load_yaml(PACKET)
        claims = {item["claim_id"]: item for item in packet["assurance_case"]["claims"]}

        self.assertEqual("pending_TX_18", packet["change_under_evaluation"]["acceptance_status"])
        self.assertFalse(packet["production_promotion_authorized"])
        self.assertEqual("gap", claims["CLAIM-TX17-HUMAN-ACCEPTANCE"]["status"])
        self.assertEqual("gap", claims["CLAIM-TX17-PRODUCTION-READINESS"]["status"])

    def _evaluate(self, **updates):
        defaults = copy.deepcopy(load_yaml(HOLDOUTS)["candidate_defaults"])
        defaults.update(updates)
        return evaluate_candidate(defaults)

    def _mutated_validation(
        self,
        *,
        packet_mutation=None,
        holdout_mutation=None,
        refresh_digest: bool = True,
    ):
        packet = copy.deepcopy(load_yaml(PACKET))
        holdouts = copy.deepcopy(load_yaml(HOLDOUTS))
        if holdout_mutation is not None:
            holdout_mutation(holdouts)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet_path = root / "packet.yaml"
            holdout_path = root / "holdouts.yaml"
            dump_yaml(holdout_path, holdouts)
            if refresh_digest:
                packet["holdout_protection"]["expected_sha256"] = hashlib.sha256(
                    holdout_path.read_bytes()
                ).hexdigest()
            if packet_mutation is not None:
                packet_mutation(packet)
            dump_yaml(packet_path, packet)
            return validate_safety_evaluation(
                packet_path,
                PACKET_SCHEMA,
                holdout_path,
                HOLDOUT_SCHEMA,
            )


def _rows(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


if __name__ == "__main__":
    unittest.main()
