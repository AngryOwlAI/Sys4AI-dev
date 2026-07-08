from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sys_for_ai.walking_skeleton import expected_walking_skeleton_report_markdown, validate_walking_skeleton_flow
from sys_for_ai.yaml_io import dump_yaml


class WalkingSkeletonTests(unittest.TestCase):
    def test_current_walking_skeleton_flow_passes(self) -> None:
        payload = validate_walking_skeleton_flow()
        self.assertTrue(payload["ok"], payload)
        self.assertEqual(payload["result"], "pass")
        self.assertEqual(payload["missing_artifacts"], [])

    def test_missing_required_artifact_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = _write_fixture(Path(temp_dir))
            (root.parent / "PRDs/Sys4AI_phase-2_walking_skeleton_prd.md").unlink()

            payload = validate_walking_skeleton_flow(root)

            self.assertFalse(payload["ok"])
            self.assertIn("PRDs/Sys4AI_phase-2_walking_skeleton_prd.md", payload["missing_artifacts"])

    def test_report_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = _write_fixture(Path(temp_dir))
            (root / "docs/generated/governance/walking-skeleton-flow.md").write_text("drift\n", encoding="utf-8")

            payload = validate_walking_skeleton_flow(root)

            self.assertFalse(payload["ok"])
            self.assertIn(
                "Sys4AI/docs/generated/governance/walking-skeleton-flow.md: generated report drift",
                payload["trace_gaps"],
            )


def _write_fixture(temp_root: Path) -> Path:
    product = temp_root / "Sys4AI"
    (product / "registries").mkdir(parents=True)
    (product / "control_records/agentjobs").mkdir(parents=True)
    (product / "control_records/completions").mkdir(parents=True)
    (product / "control_records/handoffs").mkdir(parents=True)
    (product / "control_records/system_definition").mkdir(parents=True)
    (product / "docs/generated/governance").mkdir(parents=True)
    (temp_root / "PRDs").mkdir()
    (temp_root / "implementation_plans").mkdir()

    for path in (
        product / "control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md",
        product / "control_records/completions/RECEIPT-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml",
    ):
        path.write_text("fixture\n", encoding="utf-8")

    (temp_root / "PRDs/Sys4AI_phase-2_walking_skeleton_prd.md").write_text(
        "\n".join(
            [
                "fixture PRD",
                "SFA-P2-WS-FLOW-001",
                "SFA-P2-WS-FLOW-002",
                "SFA-P2-WS-RDR-001",
                "SFA-P2-WS-PRD-001",
                "SFA-P2-WS-PLAN-001",
                "SFA-P2-WS-AJ-001",
                "SFA-P2-WS-PACKAGE-001",
                "SFA-P2-WS-TRACE-001",
                "SFA-P2-WS-VAL-001",
                "SFA-P2-WS-NFR-001",
                "SFA-P2-WS-NFR-002",
            ]
        ),
        encoding="utf-8",
    )
    (temp_root / "implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md").write_text(
        "\n".join(
            [
                "fixture plan",
                "SFA-P2-WS-FLOW-001",
                "SFA-P2-WS-FLOW-002",
                "SFA-P2-WS-RDR-001",
                "SFA-P2-WS-PRD-001",
                "SFA-P2-WS-PLAN-001",
                "SFA-P2-WS-AJ-001",
                "SFA-P2-WS-PACKAGE-001",
                "SFA-P2-WS-TRACE-001",
                "SFA-P2-WS-VAL-001",
                "SFA-P2-WS-NFR-001",
                "SFA-P2-WS-NFR-002",
                "AJ-SFADEV-20-WALKING-SKELETON-FLOW-001",
                "AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001",
                "AJ-SFADEV-22-WALKING-SKELETON-DEMO-001",
            ]
        ),
        encoding="utf-8",
    )

    dump_yaml(
        product / "control_records/handoffs/HANDOFF-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml",
        {"control_loop_notes": {"next_agentjob_id": "AJ-SFADEV-20-WALKING-SKELETON-FLOW-001"}},
    )
    _write_agentjob(product / "control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml")
    _write_agentjob(
        product / "control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml",
        ["Sys4AI/examples/target_systems/repo_steward_agent_package/**"],
    )
    _write_agentjob(
        product / "control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml",
        ["Sys4AI/control_records/completions/RECEIPT-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml"],
    )

    (product / "registries/source_registry.csv").write_text(
        "source_id,path,source_type,authority_status,owner,last_reviewed,notes\n"
        "SRC-RDR-PHASE2-WALKING-SKELETON-001,Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md,requirements_discovery_record,controlled,test,2026-07-08,fixture\n"
        "SRC-PRD-P2-WALKING-SKELETON,PRDs/Sys4AI_phase-2_walking_skeleton_prd.md,prd,controlled,test,2026-07-08,fixture\n"
        "SRC-P2-WALKING-SKELETON-IMPLEMENTATION-PLAN,implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md,implementation_plan,controlled,test,2026-07-08,fixture\n"
        "SRC-AJ-WALKING-SKELETON-FLOW-001,Sys4AI/control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml,agentjob,controlled,test,2026-07-08,fixture\n"
        "SRC-AJ-TARGET-PACKAGE-SMOKE-001,Sys4AI/control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml,agentjob,controlled,test,2026-07-08,fixture\n"
        "SRC-AJ-WALKING-SKELETON-DEMO-001,Sys4AI/control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml,agentjob,controlled,test,2026-07-08,fixture\n"
        "SRC-COMPLETION-PHASE2-WALKING-SKELETON-PLAN-001,Sys4AI/control_records/completions/RECEIPT-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml,completion_receipt,controlled,test,2026-07-08,fixture\n"
        "SRC-HANDOFF-PHASE2-WALKING-SKELETON-PLAN-001,Sys4AI/control_records/handoffs/HANDOFF-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml,handoff,controlled,test,2026-07-08,fixture\n",
        encoding="utf-8",
    )
    (product / "registries/derivative_registry.csv").write_text(
        "derivative_id,path,derivative_type,source_ids,generation_method,last_generated,status,notes\n"
        "der_walking_skeleton_flow,docs/generated/governance/walking-skeleton-flow.md,walking_skeleton_flow_report,SRC-RDR-PHASE2-WALKING-SKELETON-001;SRC-PRD-P2-WALKING-SKELETON;SRC-P2-WALKING-SKELETON-IMPLEMENTATION-PLAN,sys_for_ai.walking_skeleton:0.1.0,2026-07-08T21:41:39Z,generated_derivative,fixture\n",
        encoding="utf-8",
    )
    (product / "docs/generated/governance/walking-skeleton-flow.md").write_text(
        expected_walking_skeleton_report_markdown(product),
        encoding="utf-8",
    )
    return product


def _write_agentjob(path: Path, allowed_writes: list[str] | None = None) -> None:
    dump_yaml(
        path,
        {
            "agentjob_id": path.stem,
            "schema_version": "0.2.0",
            "status": "pending",
            "allowed_writes": allowed_writes or [],
        },
    )


if __name__ == "__main__":
    unittest.main()
