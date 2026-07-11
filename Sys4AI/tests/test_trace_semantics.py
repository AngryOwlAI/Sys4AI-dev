from __future__ import annotations

import csv
from pathlib import Path
import shutil
import tempfile
import unittest

from sys_for_ai.trace_validation import STRUCTURAL_LIMITATION, validate_generalized_trace_semantics
from sys_for_ai.validators import validate_requirement_trace
from sys_for_ai.yaml_io import dump_yaml, load_yaml


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
TRACE = PRODUCT_ROOT / "registries/requirement_trace_registry.csv"
PROGRAM_STATE = PRODUCT_ROOT / "control_records/program_state.yaml"
SOURCES = PRODUCT_ROOT / "registries/source_registry.csv"
DERIVATIVES = PRODUCT_ROOT / "registries/derivative_registry.csv"
POLICY = PRODUCT_ROOT / "configs/capability_migration.toml"
PHASE0 = PRODUCT_ROOT.parent / "PRDs/Sys4AI_phase-0_product_system_design_prd.md"
PHASE1 = PRODUCT_ROOT.parent / "PRDs/Sys4AI_phase-1_implementation_initialization_prd.md"


class TraceSemanticTests(unittest.TestCase):
    def test_live_semantics_pass_with_tx24_review_evidence(self) -> None:
        result = validate_generalized_trace_semantics(TRACE, policy_path=POLICY)
        self.assertTrue(result.ok, result.messages)
        self.assertIn(STRUCTURAL_LIMITATION, result.messages)
        rows = self._read_rows(TRACE)
        self.assertEqual(0, sum(row["semantic_review_verdict"] == "needs_evidence" for row in rows))
        self.assertEqual(227, sum(row["semantic_review_verdict"] == "sufficient" for row in rows))
        self.assertEqual(196, sum(row["verification_status"] == "planned" for row in rows))

    def test_implemented_capability_with_missing_path_fails(self) -> None:
        result = self._mutated_trace(
            lambda rows: rows[self._implemented_index(rows)].update(
                implementation_artifacts="Sys4AI/missing-implementation.py"
            )
        )
        self.assertFalse(result.ok)
        self.assertTrue(any("missing implementation_artifacts path" in item for item in result.messages))

    def test_optional_profile_without_profile_boundary_fails(self) -> None:
        def mutate(rows):
            row = rows[0]
            row["applicability_status"] = "optional_profile"
            row["implementation_artifacts"] = "PRDs/Sys4AI_phase-0_product_system_design_prd.md"
            row["evidence_paths"] = "PRDs/Sys4AI_phase-0_product_system_design_prd.md"
            row["semantic_justification"] = "bounded fixture"
            row["notes"] = "bounded fixture"

        result = self._mutated_trace(mutate)
        self.assertFalse(result.ok)
        self.assertTrue(any("optional_profile row must identify" in item for item in result.messages))

    def test_program_state_misalignment_fails(self) -> None:
        result = self._mutated_trace(lambda rows: None, state_mutation=lambda state: state.update(current_phase="unknown"))
        self.assertFalse(result.ok)
        self.assertTrue(any("unsupported strategic-baseline program phase" in item for item in result.messages))

    def test_post_tx20_state_requires_exact_tx21_route(self) -> None:
        def mutate_state(state):
            self._as_post_tx20(state)
            state["allowed_next_actions"] = [
                item
                for item in state["allowed_next_actions"]
                if item != "execute_TX_21_FINAL_ACCEPTANCE_only_after_TX_20_shared_baseline"
            ]

        result = self._mutated_trace(lambda rows: None, state_mutation=mutate_state)
        self.assertFalse(result.ok)
        self.assertTrue(any("exact TX-21 final-acceptance route" in item for item in result.messages))

    def test_post_tx20_state_requires_g09_completion(self) -> None:
        def mutate_state(state):
            self._as_post_tx20(state)
            state["capability_status_summary"].pop("derivative_regeneration")

        result = self._mutated_trace(lambda rows: None, state_mutation=mutate_state)
        self.assertFalse(result.ok)
        self.assertTrue(any("derivative_regeneration complete_G_09" in item for item in result.messages))

    def test_post_g07_state_blocks_unsupported_g10(self) -> None:
        def mutate_state(state):
            self._as_post_g07(state)
            state["blocked_actions"] = [
                item
                for item in state["blocked_actions"]
                if item != "claim_G_10_after_TX_21_audit_without_G_07_and_evidence_closure"
            ]

        result = self._mutated_trace(lambda rows: None, state_mutation=mutate_state)
        self.assertFalse(result.ok)
        self.assertTrue(any("block unsupported G-10 acceptance" in item for item in result.messages))

    def test_post_g07_state_requires_exact_tx23_planning_route(self) -> None:
        def mutate_state(state):
            self._as_post_g07(state)
            state["allowed_next_actions"] = [
                item
                for item in state["allowed_next_actions"]
                if item != "execute_TX_23_EVIDENCE_CLOSURE_PLAN_only"
            ]

        result = self._mutated_trace(lambda rows: None, state_mutation=mutate_state)
        self.assertFalse(result.ok)
        self.assertTrue(any("bounded TX-23 evidence-closure planning route" in item for item in result.messages))

    def test_post_g07_state_blocks_host_authority_expansion(self) -> None:
        def mutate_state(state):
            self._as_post_g07(state)
            state["blocked_actions"] = [
                item
                for item in state["blocked_actions"]
                if item != "treat_G_07_as_production_operational_target_runtime_or_permission_authority"
            ]

        result = self._mutated_trace(lambda rows: None, state_mutation=mutate_state)
        self.assertFalse(result.ok)
        self.assertTrue(any("block host-verification authority expansion" in item for item in result.messages))

    def test_current_evidence_freshness_fails_against_controlled_state_date(self) -> None:
        def mutate_state(state):
            state["validation_status"]["last_validated_at"] = "2026-09-20T00:00:00Z"

        result = self._mutated_trace(lambda rows: None, state_mutation=mutate_state)
        self.assertFalse(result.ok)
        self.assertTrue(any("current evidence is stale" in item for item in result.messages))

    def test_generated_derivative_cannot_be_sole_implementation_authority(self) -> None:
        def mutate(rows):
            row = rows[self._implemented_index(rows)]
            row["implementation_artifacts"] = "Sys4AI/docs/generated/configuration_control/index.md"

        result = self._mutated_trace(mutate)
        self.assertFalse(result.ok)
        self.assertTrue(any("sole implementation authority" in item for item in result.messages))

    def test_operational_capability_without_operational_evidence_fails(self) -> None:
        def mutate(rows):
            row = rows[self._implemented_index(rows)]
            row["capability_status"] = "operational"
            row["verification_status"] = "planned"
            row["validation_evidence"] = ""

        result = self._mutated_trace(mutate)
        self.assertFalse(result.ok)
        self.assertTrue(any("operational capability requires" in item for item in result.messages))

    def test_coverage_is_not_treated_as_verification(self) -> None:
        rows = self._read_rows(TRACE)
        self.assertTrue(
            any(row["coverage_status"] == "covered" and row["verification_status"] == "planned" for row in rows)
        )
        self.assertTrue(validate_generalized_trace_semantics(TRACE, policy_path=POLICY).ok)

    def test_post_tx23_state_requires_accountable_scope_gate(self) -> None:
        def mutate_state(state):
            self._as_post_tx23(state)
            state["allowed_next_actions"].remove("seek_accountable_G_11_EVIDENCE_SCOPE_decision")

        result = self._mutated_trace(lambda rows: None, state_mutation=mutate_state)
        self.assertFalse(result.ok)
        self.assertTrue(any("accountable G-11 evidence-scope gate" in item for item in result.messages))

    def test_post_tx23_state_blocks_classification_as_evidence(self) -> None:
        def mutate_state(state):
            self._as_post_tx23(state)
            state["blocked_actions"].remove("treat_TX_23_classification_as_executed_evidence")

        result = self._mutated_trace(lambda rows: None, state_mutation=mutate_state)
        self.assertFalse(result.ok)
        self.assertTrue(any("treat_TX_23_classification_as_executed_evidence" in item for item in result.messages))

    def test_post_tx26_state_requires_separate_next_family_authorization(self) -> None:
        def mutate_state(state):
            state["allowed_next_actions"].remove(
                "seek_separate_authorization_for_remaining_63_local_verification_obligations"
            )

        result = self._mutated_trace(lambda rows: None, state_mutation=mutate_state)
        self.assertFalse(result.ok)
        self.assertTrue(any("controlled next route" in item for item in result.messages))

    @staticmethod
    def _as_post_tx20(state):
        state["current_phase"] = "strategic_baseline_migration_after_TX_20"
        state["state_status"] = "active"
        state["human_gate_required"] = False
        state["latest_closeout_evidence_id"] = "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX20-001"
        state["latest_handoff_evidence_id"] = "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX20-001"
        state["allowed_next_actions"].append("execute_TX_21_FINAL_ACCEPTANCE_only_after_TX_20_shared_baseline")

    @staticmethod
    def _as_post_g07(state):
        state["current_phase"] = "strategic_baseline_migration_G_07_accepted_evidence_closure_ready"
        state["state_status"] = "active"
        state["human_gate_required"] = False
        state["continuation_state"] = "ready"
        state["escalation_state"] = "not_required"
        state["latest_closeout_evidence_id"] = "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX22-001"
        state["latest_handoff_evidence_id"] = "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX22-001"
        if "execute_TX_23_EVIDENCE_CLOSURE_PLAN_only" not in state["allowed_next_actions"]:
            state["allowed_next_actions"].append("execute_TX_23_EVIDENCE_CLOSURE_PLAN_only")

    @staticmethod
    def _as_post_tx23(state):
        state["current_phase"] = "strategic_baseline_migration_TX_23_evidence_closure_planned"
        state["state_status"] = "human_gated"
        state["human_gate_required"] = True
        state["continuation_state"] = "blocked"
        state["escalation_state"] = "pending"
        state["latest_closeout_evidence_id"] = "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX23-001"
        state["latest_handoff_evidence_id"] = "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX23-001"
        if "seek_accountable_G_11_EVIDENCE_SCOPE_decision" not in state["allowed_next_actions"]:
            state["allowed_next_actions"].append("seek_accountable_G_11_EVIDENCE_SCOPE_decision")

    def test_derivative_requirement_source_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._fixture_root(Path(temporary))
            rows = self._read_rows(root / "source_registry.csv")
            source = next(row for row in rows if row["source_id"] == "SRC-PRD-P0")
            source["authority_status"] = "derivative_draft"
            self._write_rows(root / "source_registry.csv", rows)
            result = self._validate_fixture(root)
        self.assertFalse(result.ok)
        self.assertTrue(any("requirement source cannot be" in item for item in result.messages))

    def test_additive_requirement_id_must_exist_in_registered_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._fixture_root(Path(temporary))
            rows = self._read_rows(root / "trace.csv")
            row = next(
                item for item in rows
                if item["requirement_source_id"] == "SRC-PRD-P2-STRATEGIC-BASELINE-ADDENDUM"
            )
            row["requirement_id"] = "SFA-P2-ADD-NOT-DECLARED-001"
            self._write_rows(root / "trace.csv", rows)
            result = validate_requirement_trace(
                root / "trace.csv",
                PHASE0,
                PHASE1,
                source_registry=root / "source_registry.csv",
            )
        self.assertFalse(result.ok)
        self.assertTrue(any("is not declared by registered source" in item for item in result.messages))

    def test_policy_detects_silent_planned_gap_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._fixture_root(Path(temporary))
            policy = root / "policy.toml"
            policy.write_text(
                "[trace_validation]\n"
                f'trace_registry_path = "{(root / "trace.csv").as_posix()}"\n'
                "max_current_evidence_age_days = 30\n"
                "expected_needs_evidence = 0\n"
                "expected_planned_verification = 196\n"
                "expected_operational_capability = 0\n",
                encoding="utf-8",
            )
            rows = self._read_rows(root / "trace.csv")
            row = next(item for item in rows if item["verification_status"] == "planned")
            row["verification_status"] = "pass"
            row["validation_evidence"] = "Sys4AI/tests/test_trace_semantics.py"
            self._write_rows(root / "trace.csv", rows)
            result = self._validate_fixture(root, policy=policy)
        self.assertFalse(result.ok)
        self.assertTrue(any("expected planned=196, found 195" in item for item in result.messages))

    def _mutated_trace(self, mutation, *, state_mutation=None):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._fixture_root(Path(temporary))
            rows = self._read_rows(root / "trace.csv")
            mutation(rows)
            self._write_rows(root / "trace.csv", rows)
            if state_mutation is not None:
                state = load_yaml(root / "program_state.yaml")
                state_mutation(state)
                dump_yaml(root / "program_state.yaml", state)
            return self._validate_fixture(root)

    def _fixture_root(self, root: Path) -> Path:
        shutil.copy2(TRACE, root / "trace.csv")
        shutil.copy2(PROGRAM_STATE, root / "program_state.yaml")
        shutil.copy2(SOURCES, root / "source_registry.csv")
        shutil.copy2(DERIVATIVES, root / "derivative_registry.csv")
        return root

    def _validate_fixture(self, root: Path, *, policy: Path | None = None):
        return validate_generalized_trace_semantics(
            root / "trace.csv",
            program_state=root / "program_state.yaml",
            source_registry=root / "source_registry.csv",
            derivative_registry=root / "derivative_registry.csv",
            policy_path=policy or root / "missing-policy.toml",
        )

    @staticmethod
    def _read_rows(path: Path):
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    @staticmethod
    def _write_rows(path: Path, rows):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def _implemented_index(rows):
        return next(index for index, row in enumerate(rows) if row["capability_status"] == "implemented")


if __name__ == "__main__":
    unittest.main()
