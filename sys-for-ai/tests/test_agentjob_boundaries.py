"""Tests for AgentJob boundary and Git diff validation."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from sys_for_ai.control_loop.boundaries import validate_agentjob_boundaries, validate_check_diff
from sys_for_ai.yaml_io import dump_yaml


class AgentJobBoundaryTests(unittest.TestCase):
    def test_allowed_path_passes_from_repo_root(self) -> None:
        payload = validate_agentjob_boundaries(
            "AJ-P1-BOUNDARY-VALIDATORS-001",
            root="..",
            changed_paths=["sys-for-ai/sys_for_ai/control_loop/boundaries.py"],
        )

        self.assertTrue(payload["ok"], payload)
        self.assertEqual(["sys-for-ai/sys_for_ai/control_loop/boundaries.py"], payload["allowed"])

    def test_allowed_path_passes_from_product_root(self) -> None:
        payload = validate_agentjob_boundaries(
            "AJ-P1-BOUNDARY-VALIDATORS-001",
            root=".",
            changed_paths=["sys_for_ai/control_loop/boundaries.py"],
        )

        self.assertTrue(payload["ok"], payload)
        self.assertEqual(["sys-for-ai/sys_for_ai/control_loop/boundaries.py"], payload["allowed"])

    def test_outside_allowed_write_fails(self) -> None:
        payload = validate_agentjob_boundaries(
            "AJ-P1-BOUNDARY-VALIDATORS-001",
            changed_paths=["README.md"],
        )

        self.assertFalse(payload["ok"])
        self.assertIn("outside_allowed_writes", _reasons(payload))

    def test_forbidden_path_fails(self) -> None:
        payload = validate_agentjob_boundaries(
            "AJ-P1-BOUNDARY-VALIDATORS-001",
            changed_paths=["LICENSE"],
        )

        self.assertFalse(payload["ok"])
        self.assertIn("forbidden_path", _reasons(payload))

    def test_generated_derivative_requires_generated_path_authorization(self) -> None:
        payload = validate_agentjob_boundaries(
            "AJ-P1-BOUNDARY-VALIDATORS-001",
            changed_paths=["sys-for-ai/docs/generated/configuration_control/index.md"],
        )

        self.assertFalse(payload["ok"])
        self.assertIn("generated_derivative_without_generated_path_authorization", _reasons(payload))

    def test_git_collection_includes_untracked_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            _write_temp_git_fixture(repo)
            (repo / "sys-for-ai/tmp").mkdir(parents=True)
            (repo / "sys-for-ai/tmp/new.txt").write_text("new\n", encoding="utf-8")

            payload = validate_agentjob_boundaries("AJ-TEMP-BOUNDARY-001", root=repo, use_git=True)

            self.assertTrue(payload["ok"], payload)
            self.assertIn("sys-for-ai/tmp/new.txt", payload["changed_paths"])

    def test_validate_check_diff_current_repo_has_no_boundary_violations(self) -> None:
        payload = validate_check_diff("AJ-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001")
        self.assertTrue(payload["ok"], payload)


def _reasons(payload: dict[str, object]) -> set[str]:
    violations = payload.get("violations", [])
    return {
        str(item.get("reason"))
        for item in violations
        if isinstance(item, dict)
    }


def _write_temp_git_fixture(repo: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    (repo / "sys-for-ai/registries").mkdir(parents=True)
    (repo / "sys-for-ai/control_records/agentjobs").mkdir(parents=True)
    (repo / "sys-for-ai/registries/agentjob_registry.csv").write_text(
        "agentjob_id,path,status,role_id,task_id,created_at,activated_at,completed_at,"
        "completion_receipt_id,handoff_id,authority_status,supersedes,source_hash,"
        "last_validated_at,notes\n"
        "AJ-TEMP-BOUNDARY-001,control_records/agentjobs/AJ-TEMP-BOUNDARY-001.yaml,pending,"
        "validator_engineer,TASK-TEMP,2026-07-06T00:00:00Z,,,,,controlled,,pending,pending,Temp job\n",
        encoding="utf-8",
    )
    dump_yaml(
        repo / "sys-for-ai/control_records/agentjobs/AJ-TEMP-BOUNDARY-001.yaml",
        {
            "agentjob_id": "AJ-TEMP-BOUNDARY-001",
            "schema_version": "0.2.0",
            "status": "pending",
            "role_binding": {"role_id": "validator_engineer"},
            "allowed_writes": [
                "sys-for-ai/control_records/agentjobs/**",
                "sys-for-ai/registries/**",
                "sys-for-ai/tmp/**",
            ],
            "generated_paths": [],
            "forbidden_paths": [".git/**"],
        },
    )


if __name__ == "__main__":
    unittest.main()
