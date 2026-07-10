from __future__ import annotations

from collections import Counter
from pathlib import Path
import shutil
import tempfile
import unittest

from sys_for_ai.capability_migration import (
    capability_inventory_digest,
    validate_capability_migration,
)
from sys_for_ai.cli import build_parser


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PRODUCT_ROOT.parent
SCHEMA_SOURCE = PRODUCT_ROOT / "schemas/contracts/capability_migration.schema.json"


class CapabilityMigrationTests(unittest.TestCase):
    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-capability-migration"])
        self.assertEqual(args.command, "validate-capability-migration")
        makefile = (PRODUCT_ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("validate-capability-migration:", makefile)
        self.assertIn("validate: ", makefile)

    def test_repository_g05_manifest_passes(self) -> None:
        result = validate_capability_migration(
            PRODUCT_ROOT / "configs/capability_migration.toml",
            REPOSITORY_ROOT,
        )
        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("G-05 boundary inventory passed" in item for item in result.messages))

    def test_unclassified_active_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self._write_fixture_manifest(root, active_text="")
            (root / "unclassified.txt").write_text("AgentJob", encoding="utf-8")

            result = validate_capability_migration(manifest, root)

        self.assertFalse(result.ok)
        self.assertTrue(any("unclassified" in item for item in result.messages))

    def test_inventory_change_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self._write_fixture_manifest(root, active_text="AgentJob")
            (root / "active.txt").write_text("AgentJob AgentJob", encoding="utf-8")

            result = validate_capability_migration(manifest, root)

        self.assertFalse(result.ok)
        self.assertTrue(any("inventory fingerprint mismatch" in item for item in result.messages))

    def test_restored_runtime_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self._write_fixture_manifest(root, active_text="")
            (root / "removed/runtime").mkdir(parents=True)

            result = validate_capability_migration(manifest, root)

        self.assertFalse(result.ok)
        self.assertTrue(any("has been restored" in item for item in result.messages))

    def test_post_tx10_rejects_remaining_active_stale_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self._write_fixture_manifest(
                root,
                active_text="AgentJob",
                mode="post_tx10",
                state="active_but_stale",
                allowed_modes='["pre_tx10"]',
            )

            result = validate_capability_migration(manifest, root)

        self.assertFalse(result.ok)
        self.assertTrue(any("not allowed in mode 'post_tx10'" in item for item in result.messages))

    def _write_fixture_manifest(
        self,
        root: Path,
        *,
        active_text: str,
        mode: str = "pre_tx10",
        state: str = "active_valid",
        allowed_modes: str = '["pre_tx10", "post_tx10"]',
    ) -> Path:
        schema_target = root / "Sys4AI/schemas/contracts/capability_migration.schema.json"
        schema_target.parent.mkdir(parents=True)
        shutil.copy2(SCHEMA_SOURCE, schema_target)
        (root / "active.txt").write_text(active_text, encoding="utf-8")

        references = active_text.lower().count("agentjob")
        entries = (
            {"active.txt": Counter({"agentjob": references})}
            if references
            else {}
        )
        digest = capability_inventory_digest(entries)
        manifest = root / "manifest.toml"
        manifest.write_text(
            f'''[manifest]
manifest_id = "capability_migration_g05"
manifest_version = "1.0.0"
schema_path = "Sys4AI/schemas/contracts/capability_migration.schema.json"
gate_id = "G-05"
mode = "{mode}"
reviewed_head_commit = "0000000000000000000000000000000000000000"
owner = "baseline_change_manager"
replacement_capability = "ExecutionTransaction"
legacy_terms = ["AgentJob"]
scan_roots = ["."]
text_extensions = [".txt"]
excluded_paths = ["manifest.toml"]
removed_paths = ["removed/runtime"]
review_triggers = ["inventory change"]
limitation = "Structural classification only."

[[classifications]]
classification_id = "fixture"
priority = 10
state = "{state}"
paths = ["active.txt"]
path_globs = []
disposition = "fixture"
owner = "baseline_change_manager"
replacement_capability = "ExecutionTransaction"
blocking_transaction = "none"
allowed_modes = {allowed_modes}
expected_files = {1 if references else 0}
expected_references = {references}
expected_inventory_sha256 = "{digest}"
''',
            encoding="utf-8",
        )
        return manifest


if __name__ == "__main__":
    unittest.main()
