from __future__ import annotations

import csv
from pathlib import Path
import tempfile
import unittest

from sys_for_ai.cli import build_parser
from sys_for_ai.derivatives.validation_contracts_catalog import (
    expected_validation_contracts_catalog_pages,
)
from sys_for_ai.generated_reader_surface import validate_generated_reader_surface


ROOT = Path(__file__).resolve().parents[1]


class GeneratedReaderSurfaceTests(unittest.TestCase):
    def test_live_generated_reader_surface_passes(self) -> None:
        result = validate_generated_reader_surface(product_root=ROOT)
        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("14/14" in message for message in result.messages))

    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-generated-reader-surface"])
        self.assertEqual("validate-generated-reader-surface", args.command)
        self.assertIn(
            "validate-generated-reader-surface:",
            (ROOT / "Makefile").read_text(encoding="utf-8"),
        )

    def test_missing_required_format_profile_fails(self) -> None:
        with self._mutated_registry(
            "format_profile_registry.csv",
            "format_id",
            "fmt_yaml_control",
            "format_id",
            "fmt_yaml_missing",
        ) as path:
            result = validate_generated_reader_surface(format_profiles=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("missing required format profile fmt_yaml_control" in item for item in result.messages))

    def test_missing_canonical_source_fails(self) -> None:
        with self._mutated_registry(
            "config_source_registry.csv",
            "config_id",
            "cfg_pyproject",
            "path",
            "configs/missing.toml",
        ) as path:
            result = validate_generated_reader_surface(config_sources=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("canonical source path does not exist" in item for item in result.messages))

    def test_unknown_declared_contract_fails(self) -> None:
        with self._mutated_registry(
            "config_source_registry.csv",
            "config_id",
            "cfg_pyproject",
            "validation_contract_id",
            "contract_missing",
        ) as path:
            result = validate_generated_reader_surface(config_sources=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("unknown validation contract contract_missing" in item for item in result.messages))

    def test_canonical_derivative_registration_fails(self) -> None:
        with self._mutated_registry(
            "derivative_registry.csv",
            "derivative_id",
            "der_configuration_control_index",
            "status",
            "canonical",
        ) as path:
            result = validate_generated_reader_surface(derivatives=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("status must be 'generated_derivative'" in item for item in result.messages))

    def test_obsidian_mirror_outside_generated_root_fails(self) -> None:
        with self._mutated_registry(
            "derivative_registry.csv",
            "derivative_id",
            "der_configuration_control_index",
            "path",
            "obsidian/configuration-control.md",
        ) as path:
            result = validate_generated_reader_surface(derivatives=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("must remain under docs/generated" in item for item in result.messages))

    def test_standalone_json_wiki_registration_fails(self) -> None:
        with self._mutated_registry(
            "derivative_registry.csv",
            "derivative_id",
            "der_validation_contracts_index",
            "derivative_type",
            "json_wiki_page",
        ) as path:
            result = validate_generated_reader_surface(derivatives=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("standalone JSON wiki" in item for item in result.messages))

    def test_unlinked_declaring_artifact_row_fails(self) -> None:
        with self._mutated_registry(
            "artifact_contract_registry.csv",
            "artifact_contract_id",
            "artifact_handoff",
            "artifact_contract_id",
            "artifact_handoff_unlinked",
        ) as path:
            result = validate_generated_reader_surface(artifact_contracts=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("omits declaration trace artifact_handoff_unlinked" in item for item in result.messages))

    def test_missing_mirror_policy_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "wiki-policy.md"
            text = (ROOT / "docs/configuration_control_wiki_policy.md").read_text(encoding="utf-8")
            path.write_text(text.replace("Obsidian mirrors are optional derivatives", "Mirrors may exist"), encoding="utf-8")
            result = validate_generated_reader_surface(wiki_policy=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("missing generated-reader policy term" in item for item in result.messages))

    def test_catalog_generator_is_registry_driven_for_future_contract_formats(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "registries").mkdir()
            for name in (
                "validation_contract_registry.csv",
                "artifact_contract_registry.csv",
                "config_source_registry.csv",
                "control_record_registry.csv",
                "derivative_registry.csv",
            ):
                source = ROOT / "registries" / name
                (root / "registries" / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            contract_path = root / "registries/validation_contract_registry.csv"
            with contract_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            future = dict(rows[0])
            future.update(
                contract_id="contract_future_validation_format",
                path="schemas/contracts/future.contract",
                dialect="future-1",
                target_format="future",
                target_artifact_type="future_artifact",
                target_glob="future/**/*",
                supersedes="",
            )
            with contract_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
                writer.writeheader()
                writer.writerows([*rows, future])
            pages = expected_validation_contracts_catalog_pages(root)
        self.assertTrue(all("contract_future_validation_format" in text for text in pages.values()))
        self.assertTrue(all("future-1" in text for text in pages.values()))

    @staticmethod
    def _mutated_registry(filename: str, id_field: str, row_id: str, field: str, value: str):
        temporary = tempfile.TemporaryDirectory()
        path = Path(temporary.name) / filename
        with (ROOT / "registries" / filename).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            if row[id_field] == row_id:
                row[field] = value
                break
        else:
            temporary.cleanup()
            raise AssertionError(f"missing fixture row {row_id}")
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

        class TemporaryRegistry:
            def __enter__(self):
                return path

            def __exit__(self, exc_type, exc, traceback):
                temporary.cleanup()

        return TemporaryRegistry()


if __name__ == "__main__":
    unittest.main()
