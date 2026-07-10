from __future__ import annotations

import hashlib
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from sys_for_ai.target_package import validate_target_package
from sys_for_ai.validation_semantics import STRUCTURAL_LIMITATION
from sys_for_ai.yaml_io import dump_yaml, load_yaml


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PRODUCT_ROOT / "examples/target_systems/repo_steward_agent_package"


class TargetPackageTests(unittest.TestCase):
    def test_current_target_package_passes(self) -> None:
        payload = validate_target_package(PACKAGE_ROOT)

        self.assertTrue(payload["ok"], payload)
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["target_system_id"], "repo_steward_agent_sample")
        self.assertEqual(payload["missing_files"], [])
        self.assertEqual(payload["trace_gaps"], [])
        self.assertEqual(payload["limitation"], STRUCTURAL_LIMITATION)

    def test_generic_target_system_id_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            manifest_path = package / "target-system-manifest.yaml"
            manifest = load_yaml(manifest_path)
            manifest["target_system_id"] = "alternate_repo_steward"
            dump_yaml(manifest_path, manifest)
            for relative in ("governance/vision-statement.md", "governance/core-values.md"):
                _update_front_matter(package / relative, {"target_system_id": "alternate_repo_steward"})
            for relative in (
                "governance/approval-evidence.yaml",
                "governance/agentic-system-pattern-decision.yaml",
            ):
                path = package / relative
                data = load_yaml(path)
                data["target_system_id"] = "alternate_repo_steward"
                dump_yaml(path, data)
            _refresh_manifest_hashes(package)

            payload = validate_target_package(package)

            self.assertTrue(payload["ok"], payload)
            self.assertEqual(payload["target_system_id"], "alternate_repo_steward")

    def test_active_scoped_waiver_package_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            vision_path = package / "governance/vision-statement.md"
            values_path = package / "governance/core-values.md"
            replacements = {
                "VISION-REPO-STEWARD-DEMO-001": "VISION-CAND-REPO-STEWARD-DEMO-001",
                "VALUES-REPO-STEWARD-DEMO-001": "VALUES-CAND-REPO-STEWARD-DEMO-001",
                "VALUE-REPO-STEWARD-DEMO-001": "VALUE-CAND-REPO-STEWARD-DEMO-001",
                "VALUE-REPO-STEWARD-DEMO-002": "VALUE-CAND-REPO-STEWARD-DEMO-002",
            }
            _replace_text(vision_path, replacements)
            _replace_text(values_path, replacements)
            waiver = {
                "waiver_id": "WAIVER-REPO-STEWARD-DEMO-001",
                "accountable_authority": "Example Product Owner",
                "missing_artifact_or_approval": "Real stakeholder approval",
                "reason": "Exercise the package waiver route in a non-production fixture.",
                "risk": "The content remains unapproved and cannot support release.",
                "scope": "Derivative smoke package validation only.",
                "downstream_handling": "Block production and retain candidate labels.",
                "expiry": "2027-07-10",
                "revisit_trigger": "Any real target-system use.",
                "affected_requirements_and_decisions": ["RSS-FR-004", "RSS-FR-005"],
                "status": "active",
            }
            not_approved = {
                "status": "not_approved",
                "approved_by": None,
                "principal_role": None,
                "approved_at": None,
                "approval_evidence": None,
            }
            _update_front_matter(
                vision_path,
                {
                    "vision_id": replacements["VISION-REPO-STEWARD-DEMO-001"],
                    "content_approval_state": "candidate",
                    "approval": not_approved,
                    "waiver": waiver,
                },
            )
            _update_front_matter(
                values_path,
                {
                    "core_values_set_id": replacements["VALUES-REPO-STEWARD-DEMO-001"],
                    "value_ids": [
                        replacements["VALUE-REPO-STEWARD-DEMO-001"],
                        replacements["VALUE-REPO-STEWARD-DEMO-002"],
                    ],
                    "content_approval_state": "candidate",
                    "approval": not_approved,
                    "waiver": waiver,
                },
            )
            waiver_path = package / "governance/approval-evidence.yaml"
            dump_yaml(
                waiver_path,
                {
                    "schema_version": "1.0.0",
                    "waiver_evidence_id": "WAIVER-REPO-STEWARD-DEMO-001",
                    "target_system_id": "repo_steward_agent_sample",
                    "status": "active",
                    "accountable_authority": "Example Product Owner",
                    "model_self_approval": False,
                    "permission_expansion_allowed": False,
                    "expiry": "2027-07-10",
                },
            )
            manifest_path = package / "target-system-manifest.yaml"
            manifest = load_yaml(manifest_path)
            manifest["vision_id"] = replacements["VISION-REPO-STEWARD-DEMO-001"]
            manifest["core_values_set_id"] = replacements["VALUES-REPO-STEWARD-DEMO-001"]
            manifest["core_value_ids"] = [
                replacements["VALUE-REPO-STEWARD-DEMO-001"],
                replacements["VALUE-REPO-STEWARD-DEMO-002"],
            ]
            manifest["content_approval_status"] = "waived"
            manifest["approval_evidence"] = None
            manifest["waiver_id"] = "WAIVER-REPO-STEWARD-DEMO-001"
            dump_yaml(manifest_path, manifest)
            _refresh_manifest_hashes(package)

            payload = validate_target_package(package)

            self.assertTrue(payload["ok"], payload)

    def test_missing_manifest_declared_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            (package / "product-requirements.md").unlink()

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertIn("product-requirements.md", payload["missing_files"])

    def test_smoke_canonical_authority_claim_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            manifest_path = package / "target-system-manifest.yaml"
            manifest = load_yaml(manifest_path)
            manifest["source_authority_status"] = "canonical"
            dump_yaml(manifest_path, manifest)

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertTrue(
                any("smoke examples must remain derivative" in item for item in payload["trace_gaps"]),
                payload,
            )

    def test_model_self_approval_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            approval_path = package / "governance/approval-evidence.yaml"
            approval = load_yaml(approval_path)
            approval["approved_by"] = "model"
            approval["model_self_approval"] = True
            dump_yaml(approval_path, approval)

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertTrue(
                any("approval requires an accountable non-model principal" in item for item in payload["trace_gaps"]),
                payload,
            )

    def test_duplicate_strategic_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            manifest_path = package / "target-system-manifest.yaml"
            manifest = load_yaml(manifest_path)
            manifest["core_value_ids"] = [
                "VALUE-REPO-STEWARD-DEMO-001",
                "VALUE-REPO-STEWARD-DEMO-001",
            ]
            dump_yaml(manifest_path, manifest)

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertTrue(any("duplicate strategic-intent IDs" in item for item in payload["trace_gaps"]), payload)

    def test_stale_hash_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            path = package / "product-requirements.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nStale mutation.\n", encoding="utf-8")

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertTrue(any("stale hash for product-requirements.md" in item for item in payload["trace_gaps"]), payload)

    def test_stale_active_version_pointer_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            manifest_path = package / "target-system-manifest.yaml"
            manifest = load_yaml(manifest_path)
            manifest["vision_version"] = "2.0.0"
            dump_yaml(manifest_path, manifest)

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertTrue(any("active version does not match manifest" in item for item in payload["trace_gaps"]), payload)

    def test_unapproved_state_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            manifest_path = package / "target-system-manifest.yaml"
            manifest = load_yaml(manifest_path)
            manifest["content_approval_status"] = "candidate"
            dump_yaml(manifest_path, manifest)

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertTrue(any("content approval state does not match manifest" in item for item in payload["trace_gaps"]), payload)

    def test_retired_active_packet_wording_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            path = package / "execution-transactions/TX-001-read-only-repo-inspection.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nAgentJob active packet.\n", encoding="utf-8")

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertTrue(any("active packet uses retired term 'agentjob'" in item for item in payload["trace_gaps"]), payload)

    def test_smoke_production_maturity_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            manifest_path = package / "target-system-manifest.yaml"
            manifest = load_yaml(manifest_path)
            manifest["operational_maturity"] = "production_approved"
            dump_yaml(manifest_path, manifest)

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertTrue(any("cannot exceed validated_prototype" in item for item in payload["trace_gaps"]), payload)

    def test_path_escape_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            manifest_path = package / "target-system-manifest.yaml"
            manifest = load_yaml(manifest_path)
            manifest["contents"]["prd"] = "../outside.md"
            dump_yaml(manifest_path, manifest)

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertTrue(any("escapes the package root" in item for item in payload["trace_gaps"]), payload)


def _copy_package(temp_root: Path) -> Path:
    target = temp_root / "repo_steward_agent_package"
    shutil.copytree(PACKAGE_ROOT, target)
    return target


def _update_front_matter(path: Path, updates: dict[str, object]) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(?P<metadata>.*?)\n---\n(?P<body>.*)$", text, re.DOTALL)
    if match is None:
        raise AssertionError(f"missing front matter in {path}")
    metadata = yaml.safe_load(match.group("metadata"))
    metadata.update(updates)
    metadata["source_hash"] = "pending"
    body = match.group("body")
    pending = f"---\n{yaml.safe_dump(metadata, sort_keys=False)}---\n{body}"
    digest = hashlib.sha256(pending.encode("utf-8")).hexdigest()
    metadata["source_hash"] = f"sha256:{digest}"
    path.write_text(f"---\n{yaml.safe_dump(metadata, sort_keys=False)}---\n{body}", encoding="utf-8")


def _replace_text(path: Path, replacements: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    for source, target in replacements.items():
        text = text.replace(source, target)
    path.write_text(text, encoding="utf-8")


def _refresh_manifest_hashes(package: Path) -> None:
    path = package / "target-system-manifest.yaml"
    manifest = load_yaml(path)
    for entry in manifest["hashes"]:
        entry["sha256"] = hashlib.sha256((package / entry["path"]).read_bytes()).hexdigest()
    dump_yaml(path, manifest)


if __name__ == "__main__":
    unittest.main()
