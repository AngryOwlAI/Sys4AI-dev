"""Tests for completion receipt and finalization chains."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sys_for_ai.control_loop.finalization import finalize_agentjob
from sys_for_ai.validators import validate_completion_receipts, validate_state_snapshots
from sys_for_ai.yaml_io import dump_yaml, load_yaml


class CompletionChainTests(unittest.TestCase):
    def test_completion_receipt_examples_validate(self) -> None:
        result = validate_completion_receipts("control_records/completions")
        self.assertTrue(result.ok, result.messages)

    def test_state_snapshot_examples_validate(self) -> None:
        result = validate_state_snapshots("control_records/state_snapshots")
        self.assertTrue(result.ok, result.messages)

    def test_finalize_updates_program_state_in_temp_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _write_temp_finalization_fixture(root)

            payload = finalize_agentjob(
                root / "control_records/completions/completion.yaml",
                root=root,
            )

            self.assertTrue(payload["ok"], payload)
            state = load_yaml(root / "control_records/program_state.yaml")
            self.assertEqual("RECEIPT-TEMP-001", state["latest_completion_receipt_id"])
            self.assertEqual("HANDOFF-TEMP-001", state["latest_handoff_id"])
            self.assertEqual("MEMPREFLIGHT-TEMP-001", state["latest_memory_preflight_receipt_id"])
            self.assertEqual("active", state["state_status"])
            self.assertIsNone(state["active_agentjob_id"])
            snapshot = root / "control_records/state_snapshots/state_snapshot.example.v0_2.yaml"
            self.assertTrue(snapshot.exists())


def _write_temp_finalization_fixture(root: Path) -> None:
    for rel in (
        "registries",
        "control_records/agentjobs",
        "control_records/completions",
        "control_records/handoffs",
        "control_records/state_snapshots",
    ):
        (root / rel).mkdir(parents=True, exist_ok=True)

    (root / "registries/agentjob_registry.csv").write_text(
        "agentjob_id,path,status,role_id,task_id,created_at,activated_at,completed_at,"
        "completion_receipt_id,handoff_id,authority_status,supersedes,source_hash,"
        "last_validated_at,notes\n"
        "AJ-TEMP-001,control_records/agentjobs/AJ-TEMP-001.yaml,pending,"
        "control_loop_engineer,TASK-TEMP,2026-07-06T00:00:00Z,,,,,controlled,,pending,pending,Temp job\n",
        encoding="utf-8",
    )
    (root / "registries/completion_receipt_registry.csv").write_text(
        "completion_receipt_id,path,agentjob_id,result,validation_status,changed_artifacts_count,"
        "next_handoff_id,source_hash,last_validated_at,notes\n",
        encoding="utf-8",
    )
    (root / "registries/handoff_registry.csv").write_text(
        "handoff_id,path,status,producing_agentjob_id,next_recommended_role,next_agentjob_id,"
        "source_ids,supersedes,source_hash,last_validated_at,notes\n"
        "HANDOFF-TEMP-001,control_records/handoffs/HANDOFF-TEMP-001.yaml,completed,"
        "AJ-TEMP-001,validator_engineer,AJ-TEMP-NEXT,SRC-TEMP,,pending,pending,Temp handoff\n",
        encoding="utf-8",
    )
    (root / "registries/control_record_registry.csv").write_text(
        "control_record_id,path,record_type,authority_status,owner,validation_contract_id,"
        "allowed_writers,allowed_readers,related_agentjob_id,supersedes,source_hash,"
        "last_validated_at,notes\n",
        encoding="utf-8",
    )

    dump_yaml(
        root / "control_records/agentjobs/AJ-TEMP-001.yaml",
        {
            "agentjob_id": "AJ-TEMP-001",
            "schema_version": "0.2.0",
            "status": "pending",
            "role_binding": {"role_id": "control_loop_engineer"},
            "allowed_writes": ["sys-for-ai/sys_for_ai/control_loop/**"],
            "generated_paths": [],
            "forbidden_paths": [".git/**"],
            "validators": ["cd sys-for-ai && make validate-control-loop"],
        },
    )
    dump_yaml(
        root / "control_records/completions/completion.yaml",
        {
            "completion_receipt_id": "RECEIPT-TEMP-001",
            "schema_version": "0.2.0",
            "agentjob_id": "AJ-TEMP-001",
            "role": "control_loop_engineer",
            "result": "PASS",
            "summary": "Temp finalization receipt.",
            "changed_artifacts": [
                {
                    "path": "sys-for-ai/sys_for_ai/control_loop/finalization.py",
                    "change_type": "added",
                    "authority_status": "controlled",
                }
            ],
            "validation_evidence": {
                "commands_run": [
                    {
                        "command": "cd sys-for-ai && make validate-control-loop",
                        "result": "pass",
                        "output_path": ".local/receipts/temp.txt",
                    }
                ]
            },
            "memory_preflight_receipt_id": "MEMPREFLIGHT-TEMP-001",
            "format_profile_changes": {"added": [], "modified": [], "generated_derivatives": []},
            "authority_changes": {"promoted": [], "not_promoted": []},
            "unresolved_issues": [],
            "next_recommendation": "Continue with validator work.",
            "next_handoff_id": "HANDOFF-TEMP-001",
            "state_snapshot_path": "control_records/state_snapshots/state_snapshot.example.v0_2.yaml",
            "completed_at": "2026-07-06T00:00:00Z",
        },
    )
    dump_yaml(
        root / "control_records/handoffs/HANDOFF-TEMP-001.yaml",
        {
            "handoff_id": "HANDOFF-TEMP-001",
            "schema_version": "0.2.0",
            "framework_name": "sys-for-ai",
            "target_agentic_system": "temp",
            "artifact_name": "Temp handoff",
            "artifact_type": "operational_handoff",
            "artifact_version": "0.2.0",
            "producing_role": "control_loop_engineer",
            "artifact_status": "completed",
            "summary": "Temp handoff.",
            "source_artifacts": [],
            "traceability": {},
            "control_loop_notes": {"next_agentjob_id": "AJ-TEMP-NEXT"},
            "memory_preflight": {},
            "format_profile_evidence": {},
            "source_authority_evidence": {},
            "derivative_surface_evidence": {},
            "security_evidence": {},
            "recommended_next_role": "validator_engineer",
            "phase_boundary_notes": "Temp boundary.",
            "stop_conditions": [],
        },
    )
    dump_yaml(
        root / "control_records/program_state.yaml",
        {
            "program_state_id": "SFA-PROGRAM-STATE-TEMP",
            "schema_version": "0.1.0",
            "system_context": {
                "framework_system": "sys-for-ai",
                "development_system": "sys-for-ai-dev",
                "target_system": "sys-for-ai",
                "self_hosting_mode": True,
                "reflection_depth": 1,
            },
            "current_phase": "implementation_initialization",
            "lifecycle_stage": "develop",
            "active_task_id": "TASK-TEMP",
            "active_director_decision_id": None,
            "active_agentjob_id": "AJ-TEMP-001",
            "latest_completion_receipt_id": None,
            "latest_handoff_id": None,
            "latest_memory_preflight_receipt_id": None,
            "state_status": "active",
            "blocked_reason": None,
            "human_gate_required": False,
            "allowed_next_actions": ["run_memory_preflight"],
            "blocked_actions": [
                "execute_multiple_agentjobs",
                "use_chat_memory_as_authority",
                "treat_generated_derivative_as_canonical",
                "mutate_activated_control_record_without_supersession",
            ],
            "validation_status": {"last_validated_at": "pending", "validators": []},
        },
    )


if __name__ == "__main__":
    unittest.main()
