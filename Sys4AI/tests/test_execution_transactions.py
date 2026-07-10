from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any, Callable

from sys_for_ai.jsonschema_io import check_schema, load_json, validate_instance
from sys_for_ai.yaml_io import load_yaml


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PRODUCT_ROOT / "schemas/contracts/execution_transaction.schema.json"
TEMPLATE_PATH = PRODUCT_ROOT / "templates/project/execution-transaction-template.yaml"


class ExecutionTransactionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        cls.template = load_yaml(TEMPLATE_PATH)

    def test_schema_is_valid_draft_2020_12(self) -> None:
        self.assertEqual([], check_schema(self.schema))

    def test_proposed_template_passes(self) -> None:
        self.assertEqual([], validate_instance(self.template, self.schema))

    def test_contract_has_every_tx09_required_surface(self) -> None:
        required = set(self.schema["required"])
        self.assertTrue(
            {
                "execution_transaction_id",
                "contract_version",
                "objective",
                "source_requirement_ids",
                "source_decision_ids",
                "subject_system",
                "subject_layer",
                "runtime_actor",
                "approval_principal",
                "permission_envelope",
                "allowed_reads",
                "allowed_writes",
                "allowed_tools",
                "allowed_external_actions",
                "forbidden_actions",
                "inputs",
                "expected_outputs",
                "validators",
                "stop_conditions",
                "cancellation",
                "escalation",
                "state",
                "resume_evidence",
                "closeout_evidence",
                "rollback",
                "supersession",
            }.issubset(required)
        )

    def test_contract_has_exact_execution_states(self) -> None:
        states = self.schema["properties"]["state"]["properties"]["status"]["enum"]
        self.assertEqual(
            [
                "proposed",
                "authorized",
                "active",
                "blocked",
                "cancelled",
                "completed",
                "accepted",
                "superseded",
            ],
            states,
        )

    def test_contract_version_is_pinned_to_schema_version(self) -> None:
        self._assert_mutation_fails(lambda data: data.__setitem__("contract_version", "2.0.0"))

    def test_contract_is_harness_neutral_and_omits_legacy_execution_keys(self) -> None:
        combined = json.dumps(self.schema) + json.dumps(self.template)
        self.assertNotIn("Codex", combined)
        self.assertNotIn("AgentJob", combined)
        self.assertNotIn("agentjob", combined)
        self.assertNotIn("/continue", combined)

    def test_unknown_top_level_field_fails(self) -> None:
        self._assert_mutation_fails(lambda data: data.__setitem__("implicit_authority", True))

    def test_missing_permission_envelope_fails(self) -> None:
        self._assert_mutation_fails(lambda data: data.pop("permission_envelope"))

    def test_missing_stop_conditions_fails(self) -> None:
        self._assert_mutation_fails(lambda data: data.pop("stop_conditions"))

    def test_missing_cancellation_contract_fails(self) -> None:
        self._assert_mutation_fails(lambda data: data.pop("cancellation"))

    def test_missing_closeout_contract_fails(self) -> None:
        self._assert_mutation_fails(lambda data: data.pop("closeout_evidence"))

    def test_model_self_approval_fails(self) -> None:
        self._assert_mutation_fails(
            lambda data: data["approval_principal"].__setitem__("model_self_approval", True)
        )

    def test_execution_self_authorization_fails(self) -> None:
        self._assert_mutation_fails(
            lambda data: data["execution_authorization"].__setitem__("self_authorized", True)
        )

    def test_permission_expansion_fails(self) -> None:
        self._assert_mutation_fails(
            lambda data: data["permission_envelope"].__setitem__(
                "permission_expansion_allowed", True
            )
        )

    def test_external_action_requires_explicit_side_effect_permission(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["allowed_external_actions"] = ["Create one external change"]

        self._assert_mutation_fails(mutate)

    def test_delegation_requires_explicit_expiry(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["permission_envelope"]["delegation_allowed"] = True

        self._assert_mutation_fails(mutate)

    def test_current_permission_requires_bounded_time_window(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_authorized(data)
            data["permission_envelope"]["expires_at"] = "pending_permission"

        self._assert_mutation_fails(mutate)

    def test_secret_access_requires_sensitive_data_permission(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["permission_envelope"]["secrets_allowed"] = True

        self._assert_mutation_fails(mutate)

    def test_empty_requirement_trace_fails(self) -> None:
        self._assert_mutation_fails(lambda data: data.__setitem__("source_requirement_ids", []))

    def test_duplicate_allowed_read_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["allowed_reads"].append(data["allowed_reads"][0])

        self._assert_mutation_fails(mutate)

    def test_invalid_subject_layer_fails(self) -> None:
        self._assert_mutation_fails(lambda data: data.__setitem__("subject_layer", "meta_layer"))

    def test_authorized_state_requires_human_authorization_evidence(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_authorized(data)
            data["approval_principal"]["authorization_evidence_ids"] = []

        self._assert_mutation_fails(mutate)

    def test_proposed_state_rejects_premature_authorization(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            authorization = data["execution_authorization"]
            authorization["status"] = "authorized"
            authorization["authorized_at"] = "2026-07-10T12:00:00Z"
            authorization["expires_at"] = "2026-07-11T12:00:00Z"
            authorization["authority_evidence_ids"] = ["EVID-HUMAN-AUTH-001"]

        self._assert_mutation_fails(mutate)

    def test_active_state_with_verified_capabilities_passes(self) -> None:
        data = copy.deepcopy(self.template)
        _make_active(data)
        self.assertEqual([], validate_instance(data, self.schema))

    def test_active_state_rejects_unknown_required_capability(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_active(data)
            data["host_capability_requirements"]["overall_status"] = "unknown"

        self._assert_mutation_fails(mutate)

    def test_active_state_rejects_pending_host_profile(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_active(data)
            data["host_capability_requirements"]["execution_profile_id"] = "pending_host_profile"

        self._assert_mutation_fails(mutate)

    def test_active_state_rejects_pending_runtime_actor(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_active(data)
            data["runtime_actor"]["actor_id"] = "pending_runtime_actor"

        self._assert_mutation_fails(mutate)

    def test_active_state_rejects_pending_approval_principal(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_active(data)
            data["approval_principal"]["principal_id"] = "pending_accountable_human"

        self._assert_mutation_fails(mutate)

    def test_active_state_requires_capability_evidence(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_active(data)
            data["host_capability_requirements"]["evidence_ids"] = []

        self._assert_mutation_fails(mutate)

    def test_blocked_state_requires_blocked_continuation_and_transition_evidence(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["state"]["status"] = "blocked"
            data["state"]["continuation_state"] = "not_ready"

        self._assert_mutation_fails(mutate)

    def test_cancelled_state_requires_cancellation_evidence(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["state"]["status"] = "cancelled"
            data["state"]["state_transition_evidence_ids"] = ["EVID-CANCEL-TRANSITION-001"]
            data["cancellation"]["state"] = "safe_stop"

        self._assert_mutation_fails(mutate)

    def test_completed_state_requires_validation_closeout_evidence(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_completed(data)
            data["closeout_evidence"]["validation_evidence_ids"] = []

        self._assert_mutation_fails(mutate)

    def test_completed_state_with_retained_execution_evidence_passes(self) -> None:
        data = copy.deepcopy(self.template)
        _make_completed(data)

        self.assertEqual([], validate_instance(data, self.schema))

    def test_completed_state_requires_retained_capability_evidence(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_completed(data)
            data["host_capability_requirements"]["evidence_ids"] = []

        self._assert_mutation_fails(mutate)

    def test_accepted_state_requires_acceptance_evidence(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_completed(data)
            data["state"]["status"] = "accepted"
            data["closeout_evidence"]["status"] = "accepted"

        self._assert_mutation_fails(mutate)

    def test_superseded_state_requires_supersession_evidence(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["state"]["status"] = "superseded"
            data["state"]["state_transition_evidence_ids"] = ["EVID-SUPERSESSION-001"]
            data["supersession"]["status"] = "superseded"
            data["supersession"]["superseded_by"] = "TX-REPLACEMENT-001"

        self._assert_mutation_fails(mutate)

    def _assert_mutation_fails(self, mutate: Callable[[dict[str, Any]], None]) -> None:
        data = copy.deepcopy(self.template)
        mutate(data)
        errors = validate_instance(data, self.schema)
        self.assertTrue(errors, "mutated execution transaction unexpectedly passed")


def _make_authorized(data: dict[str, Any]) -> None:
    data["subject_system"]["system_id"] = "sys4ai"
    data["runtime_actor"]["actor_id"] = "sys4ai_meta_agent_runtime"
    data["approval_principal"]["principal_id"] = "accountable_human_owner"
    data["approval_principal"]["authorization_evidence_ids"] = ["EVID-HUMAN-AUTH-001"]
    authorization = data["execution_authorization"]
    authorization["status"] = "authorized"
    authorization["authorized_at"] = "2026-07-10T12:00:00Z"
    authorization["expires_at"] = "2026-07-11T12:00:00Z"
    authorization["authority_evidence_ids"] = ["EVID-HUMAN-AUTH-001"]
    permission = data["permission_envelope"]
    permission["status"] = "current"
    permission["valid_from"] = "2026-07-10T12:00:00Z"
    permission["expires_at"] = "2026-07-11T12:00:00Z"
    data["state"]["status"] = "authorized"
    data["state"]["state_transition_evidence_ids"] = ["EVID-AUTH-TRANSITION-001"]


def _make_active(data: dict[str, Any]) -> None:
    _make_authorized(data)
    _make_capability_verified(data)
    data["state"]["status"] = "active"
    data["state"]["state_transition_evidence_ids"] = ["EVID-ACTIVE-TRANSITION-001"]


def _make_capability_verified(data: dict[str, Any]) -> None:
    capabilities = data["host_capability_requirements"]
    capabilities["execution_profile_id"] = "verified_reference_profile"
    capabilities["overall_status"] = "verified_available"
    capabilities["evidence_ids"] = ["EVID-HOST-CAPABILITY-001"]
    capabilities["checked_at"] = "2026-07-10T12:05:00Z"


def _make_completed(data: dict[str, Any]) -> None:
    _make_authorized(data)
    _make_capability_verified(data)
    data["state"]["status"] = "completed"
    data["state"]["continuation_state"] = "consumed"
    data["state"]["state_transition_evidence_ids"] = ["EVID-COMPLETE-TRANSITION-001"]
    closeout = data["closeout_evidence"]
    closeout["status"] = "complete"
    closeout["evidence_ids"] = ["EVID-CLOSEOUT-001"]
    closeout["validation_evidence_ids"] = ["EVID-VALIDATION-001"]


if __name__ == "__main__":
    unittest.main()
