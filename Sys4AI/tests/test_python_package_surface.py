from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import unittest

from sys_for_ai.cli import build_parser
from sys_for_ai.python_package_surface import validate_python_package_surface


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
REQUIREMENTS = ROOT / "requirements.txt"


class PythonPackageSurfaceTests(unittest.TestCase):
    def test_live_python_package_surface_passes(self) -> None:
        result = validate_python_package_surface(PYPROJECT, REQUIREMENTS)
        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("4/4" in message for message in result.messages))

    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-python-package-surface"])
        self.assertEqual("validate-python-package-surface", args.command)
        self.assertIn("validate-python-package-surface:", (ROOT / "Makefile").read_text(encoding="utf-8"))

    def test_heavy_or_unbounded_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._fixture(Path(temporary))
            path = root / "pyproject.toml"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    '  "jsonschema>=4.0,<5.0",',
                    '  "jsonschema>=4.0,<5.0",\n  "celery>=5",',
                ),
                encoding="utf-8",
            )
            result = validate_python_package_surface(
                path,
                root / "requirements.txt",
                run_interpreter_probes=False,
            )
        self.assertFalse(result.ok)
        self.assertTrue(any("exactly the three lightweight" in message for message in result.messages))

    def test_dependency_file_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._fixture(Path(temporary))
            (root / "requirements.txt").write_text("PyYAML>=6.0,<7.0\n", encoding="utf-8")
            result = validate_python_package_surface(
                root / "pyproject.toml",
                root / "requirements.txt",
                run_interpreter_probes=False,
            )
        self.assertFalse(result.ok)
        self.assertTrue(any("must match pyproject.toml" in message for message in result.messages))

    def test_missing_reference_surface_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._fixture(Path(temporary))
            (root / "sys_for_ai/validators.py").unlink()
            result = validate_python_package_surface(
                root / "pyproject.toml",
                root / "requirements.txt",
                run_interpreter_probes=False,
            )
        self.assertFalse(result.ok)
        self.assertTrue(any("required Python reference surface is missing" in message for message in result.messages))

    @staticmethod
    def _fixture(root: Path) -> Path:
        shutil.copytree(ROOT / "sys_for_ai", root / "sys_for_ai")
        for directory in ("configs", "control_records", "registries", "schemas/contracts"):
            (root / directory).mkdir(parents=True, exist_ok=True)
        shutil.copy2(PYPROJECT, root / "pyproject.toml")
        shutil.copy2(REQUIREMENTS, root / "requirements.txt")
        return root


if __name__ == "__main__":
    unittest.main()
