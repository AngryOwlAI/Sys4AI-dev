from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import unittest

from sys_for_ai.cli import build_parser
from sys_for_ai.prd_semantics import STRUCTURAL_LIMITATION, validate_prd_semantics


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PRODUCT_ROOT.parent
PHASE0 = REPOSITORY_ROOT / "PRDs/Sys4AI_phase-0_product_system_design_prd.md"
PHASE1 = REPOSITORY_ROOT / "PRDs/Sys4AI_phase-1_implementation_initialization_prd.md"
MANIFEST = PRODUCT_ROOT / "configs/capability_migration.toml"


class PrdSemanticTests(unittest.TestCase):
    def test_current_canonical_prds_pass(self) -> None:
        result = validate_prd_semantics()
        self.assertTrue(result.ok, result.messages)
        self.assertIn(STRUCTURAL_LIMITATION, result.messages)

    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-prd-semantics"])
        self.assertEqual("validate-prd-semantics", args.command)
        self.assertIn("validate-prd-semantics:", (PRODUCT_ROOT / "Makefile").read_text(encoding="utf-8"))

    def test_missing_composite_identity_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._fixture_root(Path(temporary))
            path = root / "PRDs/Sys4AI_phase-0_product_system_design_prd.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace("Meta-Agentic AI Framework System", "Removed identity"), encoding="utf-8")
            result = self._validate_fixture(root)
        self.assertFalse(result.ok)
        self.assertTrue(any("Meta-Agentic AI Framework System" in item for item in result.messages))

    def test_active_removed_reference_without_classification_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._fixture_root(Path(temporary))
            path = root / "PRDs/Sys4AI_phase-0_product_system_design_prd.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nActive AgentJob route.\n", encoding="utf-8")
            result = self._validate_fixture(root)
        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "active removed command reference is not classified" in item
                or "legacy reference classification 'active_but_stale' is not allowed" in item
                for item in result.messages
            )
        )

    def test_derivative_module_cannot_claim_unclassified_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            modules = root / "modules"
            modules.mkdir()
            (modules / "bad.md").write_text("# Draft\n", encoding="utf-8")
            result = validate_prd_semantics(modules_root=modules)
        self.assertFalse(result.ok)
        self.assertTrue(any("derivative_draft authority status" in item for item in result.messages))

    def _fixture_root(self, root: Path) -> Path:
        (root / "PRDs").mkdir(parents=True)
        (root / "Sys4AI/configs").mkdir(parents=True)
        shutil.copy2(PHASE0, root / "PRDs/Sys4AI_phase-0_product_system_design_prd.md")
        shutil.copy2(PHASE1, root / "PRDs/Sys4AI_phase-1_implementation_initialization_prd.md")
        shutil.copy2(MANIFEST, root / "Sys4AI/configs/capability_migration.toml")
        return root

    def _validate_fixture(self, root: Path):
        return validate_prd_semantics(
            root / "PRDs/Sys4AI_phase-0_product_system_design_prd.md",
            root / "PRDs/Sys4AI_phase-1_implementation_initialization_prd.md",
            capability_manifest=root / "Sys4AI/configs/capability_migration.toml",
            modules_root=root / "missing-modules",
            repository_root=root,
        )


if __name__ == "__main__":
    unittest.main()
