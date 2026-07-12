from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from sys_for_ai.cli import build_parser
from sys_for_ai.cross_version_ci import validate_cross_version_ci


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/cross-version-python.yml"


class CrossVersionCITests(unittest.TestCase):
    def test_live_workflow_passes(self) -> None:
        result = validate_cross_version_ci(WORKFLOW)
        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("5/5" in message for message in result.messages))

    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-cross-version-ci"])
        self.assertEqual("validate-cross-version-ci", args.command)
        makefile = (ROOT / "Sys4AI/Makefile").read_text(encoding="utf-8")
        self.assertIn("validate-cross-version-ci:", makefile)

    def test_missing_supported_minor_fails(self) -> None:
        result = self._mutated('\n          - "3.14"', "")
        self.assertFalse(result.ok)
        self.assertTrue(any("matrix must be exactly" in message for message in result.messages))

    def test_write_permission_fails(self) -> None:
        result = self._mutated("contents: read", "contents: write")
        self.assertFalse(result.ok)
        self.assertTrue(any("permissions must be exactly" in message for message in result.messages))

    def test_partial_validation_command_fails(self) -> None:
        result = self._mutated("make validate PY=python", "cd Sys4AI && make validate-python-package-surface")
        self.assertFalse(result.ok)
        self.assertTrue(any("required command is missing" in message for message in result.messages))

    @staticmethod
    def _mutated(before: str, after: str):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "workflow.yml"
            path.write_text(WORKFLOW.read_text(encoding="utf-8").replace(before, after), encoding="utf-8")
            return validate_cross_version_ci(path)


if __name__ == "__main__":
    unittest.main()
