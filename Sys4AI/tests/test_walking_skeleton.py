from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sys_for_ai.target_package import DEFAULT_PACKAGE_ROOT, PRODUCT_ROOT
from sys_for_ai.walking_skeleton import (
    PHASE2_ADDENDUM_REQUIREMENT_IDS,
    expected_walking_skeleton_report_markdown,
    validate_walking_skeleton_flow,
)


PACKAGE_ROOT = PRODUCT_ROOT / DEFAULT_PACKAGE_ROOT


class WalkingSkeletonTests(unittest.TestCase):
    def test_current_strategic_walking_skeleton_passes(self) -> None:
        payload = validate_walking_skeleton_flow()

        self.assertTrue(payload["ok"], payload)
        self.assertEqual("pass", payload["result"])
        self.assertEqual([], payload["missing_artifacts"])
        self.assertEqual([], payload["trace_gaps"])
        self.assertEqual("repo_steward_agent_sample", payload["target_system_id"])

    def test_active_graph_contains_revised_artifacts_and_no_retired_packet_nodes(self) -> None:
        payload = validate_walking_skeleton_flow()
        active = payload["artifacts"]
        active_types = {artifact["artifact_type"] for artifact in active}

        self.assertIn("target_vision", active_types)
        self.assertIn("target_core_values", active_types)
        self.assertIn("approval_or_waiver_evidence", active_types)
        self.assertIn("agentic_system_pattern_decision", active_types)
        self.assertIn("host_capability_evidence", active_types)
        self.assertIn("test_and_evaluation_evidence", active_types)
        self.assertIn("strategic_trace", active_types)
        self.assertIn("portable_execution_transaction", active_types)
        for artifact in active:
            active_text = " ".join(
                (
                    artifact["artifact_id"],
                    artifact["artifact_type"],
                    artifact["path"],
                )
            ).lower()
            self.assertNotIn("agentjob", active_text)
            self.assertNotIn("/continue", active_text)

    def test_historical_packet_flow_remains_available_only_as_history(self) -> None:
        payload = validate_walking_skeleton_flow()
        historical = payload["historical_artifacts"]

        self.assertGreaterEqual(len(historical), 7)
        self.assertTrue(any(item["artifact_type"] == "agentjob" for item in historical))
        self.assertTrue(all(item["authority_status"] == "historical" for item in historical))
        self.assertTrue(all(item["validation_status"] == "historical_preserved" for item in historical))

    def test_lifecycle_stages_are_complete_and_ordered(self) -> None:
        payload = validate_walking_skeleton_flow()
        stages = payload["lifecycle_stages"]

        self.assertEqual(["Design", "Develop", "Implement", "Test"], [stage["stage"] for stage in stages])
        required_fields = {
            "inputs",
            "responsible_role",
            "approving_role",
            "permissions",
            "activities",
            "outputs",
            "entry_criteria",
            "exit_criteria",
            "failure_behavior",
            "rollback_or_return",
            "evidence",
        }
        for stage in stages:
            self.assertTrue(all(stage[field].strip() for field in required_fields), stage)

    def test_manifest_driven_flow_accepts_an_alternate_package_location(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = Path(temp_dir) / "package"
            shutil.copytree(PACKAGE_ROOT, package)

            payload = validate_walking_skeleton_flow(package_root=package, check_report=False)

        self.assertTrue(payload["ok"], payload)
        self.assertEqual("repo_steward_agent_sample", payload["target_system_id"])
        self.assertEqual(str(package.resolve()), payload["package_root"])

    def test_missing_target_vision_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = Path(temp_dir) / "package"
            shutil.copytree(PACKAGE_ROOT, package)
            (package / "governance/vision-statement.md").unlink()

            payload = validate_walking_skeleton_flow(package_root=package, check_report=False)

        self.assertFalse(payload["ok"])
        self.assertTrue(
            any("vision-statement.md" in item for item in payload["missing_artifacts"]),
            payload,
        )

    def test_missing_approval_evidence_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = Path(temp_dir) / "package"
            shutil.copytree(PACKAGE_ROOT, package)
            (package / "governance/approval-evidence.yaml").unlink()

            payload = validate_walking_skeleton_flow(package_root=package, check_report=False)

        self.assertFalse(payload["ok"])
        self.assertTrue(
            any("approval-evidence.yaml" in item for item in payload["missing_artifacts"]),
            payload,
        )

    def test_target_package_validation_failure_is_part_of_flow_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = Path(temp_dir) / "package"
            shutil.copytree(PACKAGE_ROOT, package)
            manifest = package / "target-system-manifest.yaml"
            manifest.write_text(manifest.read_text(encoding="utf-8").replace("validated_prototype", "production"), encoding="utf-8")

            payload = validate_walking_skeleton_flow(package_root=package, check_report=False)

        self.assertFalse(payload["ok"])
        self.assertTrue(any(item.startswith("target-package:") for item in payload["trace_gaps"]), payload)

    def test_report_drift_fails(self) -> None:
        with patch("sys_for_ai.walking_skeleton.expected_walking_skeleton_report_markdown", return_value="drift\n"):
            payload = validate_walking_skeleton_flow()

        self.assertFalse(payload["ok"])
        self.assertIn(
            "Sys4AI/docs/generated/governance/walking-skeleton-flow.md: generated report drift",
            payload["trace_gaps"],
        )

    def test_generated_report_separates_active_flow_history_and_open_gates(self) -> None:
        report = expected_walking_skeleton_report_markdown()
        active_section, historical_section = report.split("## Historical Evidence Appendix", maxsplit=1)

        self.assertIn("## Active Revised Artifact Flow", active_section)
        self.assertNotIn("agentjob", active_section.lower())
        self.assertIn("agentjob", historical_section.lower())
        self.assertIn("G-07 host verification remains open", report)
        self.assertIn("G-08 framework strategic approval is accepted", report)
        self.assertNotIn("G-08 strategic approval remains open", report)
        self.assertIn("Production readiness, operational authority, stakeholder consensus, and domain acceptance remain open", report)

    def test_every_addendum_requirement_is_in_the_framework_trace(self) -> None:
        payload = validate_walking_skeleton_flow()
        self.assertEqual(13, len(PHASE2_ADDENDUM_REQUIREMENT_IDS))
        self.assertFalse(
            any("framework trace missing" in item for item in payload["trace_gaps"]),
            payload,
        )


if __name__ == "__main__":
    unittest.main()
