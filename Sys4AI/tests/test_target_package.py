from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from sys_for_ai.target_package import validate_target_package
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

    def test_missing_required_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            (package / "product-requirements.md").unlink()

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertIn("product-requirements.md", payload["missing_files"])

    def test_canonical_authority_claim_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = _copy_package(Path(temp_dir))
            manifest_path = package / "target-system-manifest.yaml"
            manifest = load_yaml(manifest_path)
            manifest["source_authority_status"] = "canonical"
            dump_yaml(manifest_path, manifest)

            payload = validate_target_package(package)

            self.assertFalse(payload["ok"])
            self.assertIn(
                "target-system-manifest.yaml: source_authority_status must remain derivative or scaffold authority",
                payload["trace_gaps"],
            )


def _copy_package(temp_root: Path) -> Path:
    target = temp_root / "repo_steward_agent_package"
    shutil.copytree(PACKAGE_ROOT, target)
    return target


if __name__ == "__main__":
    unittest.main()
