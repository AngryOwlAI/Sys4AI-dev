from __future__ import annotations

import csv
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from sys_for_ai.cli import build_parser
from sys_for_ai.format_governance_surface import validate_format_governance_surface


ROOT = Path(__file__).resolve().parents[1]


class FormatGovernanceSurfaceTests(unittest.TestCase):
    def test_live_format_governance_surface_passes(self) -> None:
        result = validate_format_governance_surface()
        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("10/10" in message for message in result.messages))

    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-format-governance-surface"])
        self.assertEqual("validate-format-governance-surface", args.command)
        self.assertIn("validate-format-governance-surface:", (ROOT / "Makefile").read_text(encoding="utf-8"))

    def test_missing_profile_axis_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            registry = Path(temporary) / "format_profile_registry.csv"
            shutil.copy2(ROOT / "registries/format_profile_registry.csv", registry)
            rows = self._read_rows(registry)
            rows[0]["canonical_roots"] = ""
            self._write_rows(registry, rows)
            result = validate_format_governance_surface(registry)
        self.assertFalse(result.ok)
        self.assertTrue(any("canonical_roots must be populated" in message for message in result.messages))

    def test_authority_inversion_policy_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            policy = Path(temporary) / "format_profile_policy.md"
            text = (ROOT / "docs/format_profile_policy.md").read_text(encoding="utf-8")
            policy.write_text(
                text.replace(
                    "Generated derivatives, local vault notes, semantic caches, and summaries do not become canonical",
                    "Generated pages may become canonical",
                ),
                encoding="utf-8",
            )
            result = validate_format_governance_surface(policy=policy)
        self.assertFalse(result.ok)
        self.assertTrue(any("do not become canonical" in message for message in result.messages))

    def test_uncontrolled_project_extension_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            policy = Path(temporary) / "format_profile_policy.md"
            text = (ROOT / "docs/format_profile_policy.md").read_text(encoding="utf-8")
            policy.write_text(
                text.replace("shall not weaken the core authority hierarchy", "may override core authority"),
                encoding="utf-8",
            )
            result = validate_format_governance_surface(policy=policy)
        self.assertFalse(result.ok)
        self.assertTrue(any("shall not weaken" in message for message in result.messages))

    def test_missing_memory_freshness_field_fails(self) -> None:
        real_lookup = __import__("sys_for_ai.memory", fromlist=["lookup_memory"]).lookup_memory

        def lookup_without_freshness(object_id: str, root: str | Path = "."):
            payload = real_lookup(object_id, root)
            result = payload.get("result")
            if object_id == "SRC-PRD-P0" and isinstance(result, dict):
                result.pop("derivative_freshness", None)
            return payload

        with patch("sys_for_ai.format_governance_surface.lookup_memory", side_effect=lookup_without_freshness):
            result = validate_format_governance_surface()
        self.assertFalse(result.ok)
        self.assertTrue(any("missing inspectability fields derivative_freshness" in message for message in result.messages))

    @staticmethod
    def _read_rows(path: Path) -> list[dict[str, str]]:
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    @staticmethod
    def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
