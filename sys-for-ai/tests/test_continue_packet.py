from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sys_for_ai.control_loop import continue_packet, continue_select
from sys_for_ai.control_loop.state import load_program_state
from sys_for_ai.control_loop.job_selection import select_or_reuse_one_agentjob
from sys_for_ai.yaml_io import dump_yaml


class ContinuePacketTests(unittest.TestCase):
    def test_continue_packet_reports_terminal_missing_route(self) -> None:
        payload = continue_packet()
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["packet_type"], "director_decision_required")
        self.assertEqual(payload["status"], "BLOCKED")

    def test_missing_director_decision_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "control_records").mkdir()
            (root / "registries").mkdir()
            dump_yaml(
                root / "control_records/program_state.yaml",
                {
                    "program_state_id": "TEST-STATE",
                    "active_agentjob_id": None,
                    "active_director_decision_id": None,
                    "latest_handoff_id": None,
                    "state_status": "active",
                    "human_gate_required": False,
                },
            )
            (root / "registries/agentjob_registry.csv").write_text(
                "agentjob_id,path,status,role_id,task_id,created_at,activated_at,completed_at,completion_receipt_id,handoff_id,authority_status,supersedes,source_hash,last_validated_at,notes\n",
                encoding="utf-8",
            )
            (root / "registries/director_decision_registry.csv").write_text(
                "director_decision_id,path,status,task_id,selected_route,selected_agentjob_id,authority_status,supersedes,source_hash,last_validated_at,notes\n",
                encoding="utf-8",
            )
            (root / "registries/handoff_registry.csv").write_text(
                "handoff_id,path,status,producing_agentjob_id,next_recommended_role,next_agentjob_id,source_ids,supersedes,source_hash,last_validated_at,notes\n",
                encoding="utf-8",
            )
            payload = continue_select(root)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["packet_type"], "director_decision_required")

    def test_multiple_active_agentjobs_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "control_records/agentjobs").mkdir(parents=True)
            (root / "registries").mkdir()
            dump_yaml(
                root / "control_records/program_state.yaml",
                {
                    "program_state_id": "TEST-STATE",
                    "active_agentjob_id": None,
                    "active_director_decision_id": None,
                    "latest_handoff_id": None,
                    "state_status": "active",
                    "human_gate_required": False,
                },
            )
            for job_id in ("AJ-ONE", "AJ-TWO"):
                dump_yaml(
                    root / f"control_records/agentjobs/{job_id}.yaml",
                    {
                        "agentjob_id": job_id,
                        "schema_version": "0.2.0",
                        "status": "active",
                        "objective": "test",
                        "lifecycle_stage": "test",
                        "role_binding": {
                            "role_id": "tester",
                            "binding_type": "one_job_provisional_role",
                            "authority_scope": "test",
                            "expires_with_agentjob": True,
                        },
                        "required_inputs": [],
                        "allowed_reads": [],
                        "allowed_writes": [],
                        "forbidden_actions": [],
                        "expected_outputs": [],
                        "validators": [],
                        "completion_evidence_required": [],
                        "memory_preflight": {"required": False},
                        "authority_boundary": {},
                        "handoff_policy": {},
                        "stop_conditions": [],
                    },
                )
            (root / "registries/agentjob_registry.csv").write_text(
                "agentjob_id,path,status,role_id,task_id,created_at,activated_at,completed_at,completion_receipt_id,handoff_id,authority_status,supersedes,source_hash,last_validated_at,notes\n"
                "AJ-ONE,control_records/agentjobs/AJ-ONE.yaml,active,tester,TASK,,,,,,controlled,,pending,pending,test\n"
                "AJ-TWO,control_records/agentjobs/AJ-TWO.yaml,active,tester,TASK,,,,,,controlled,,pending,pending,test\n",
                encoding="utf-8",
            )
            state = load_program_state(root)
            selection = select_or_reuse_one_agentjob(state, root)
            self.assertEqual(selection.kind, "conflict")
            self.assertEqual(selection.reason, "multiple_active_agentjobs")


if __name__ == "__main__":
    unittest.main()
