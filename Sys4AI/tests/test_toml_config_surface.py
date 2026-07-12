from __future__ import annotations

import csv
from pathlib import Path
import tempfile
import unittest

from sys_for_ai.cli import build_parser
from sys_for_ai.toml_config_surface import validate_toml_config_surface


ROOT = Path(__file__).resolve().parents[1]


class TomlConfigSurfaceTests(unittest.TestCase):
    def test_live_toml_config_surface_passes(self) -> None:
        result = validate_toml_config_surface(product_root=ROOT)
        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("9/9" in message for message in result.messages))

    def test_cli_and_make_surfaces_exist(self) -> None:
        args = build_parser().parse_args(["validate-toml-config-surface"])
        self.assertEqual("validate-toml-config-surface", args.command)
        self.assertIn("validate-toml-config-surface:", (ROOT / "Makefile").read_text(encoding="utf-8"))

    def test_toml_profile_assignment_drift_fails(self) -> None:
        with self._mutated_registry(
            "format_profile_registry.csv", "format_id", "fmt_toml_config", "primary_role", "document"
        ) as path:
            result = validate_toml_config_surface(format_profiles=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("fmt_toml_config primary_role" in message for message in result.messages))

    def test_missing_config_owner_fails(self) -> None:
        with self._mutated_registry(
            "config_source_registry.csv", "config_id", "cfg_sys4ai_example", "owner", ""
        ) as path:
            result = validate_toml_config_surface(config_sources=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("owner must be populated" in message for message in result.messages))

    def test_wrong_parser_fails(self) -> None:
        with self._mutated_registry(
            "config_source_registry.csv", "config_id", "cfg_sys4ai_example", "parser", "other"
        ) as path:
            result = validate_toml_config_surface(config_sources=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("parser must be 'tomllib_or_tomli'" in message for message in result.messages))

    def test_secret_policy_expansion_fails(self) -> None:
        with self._mutated_registry(
            "config_source_registry.csv", "config_id", "cfg_sys4ai_example", "secrets_allowed", "true"
        ) as path:
            result = validate_toml_config_surface(config_sources=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("secrets_allowed must be 'false'" in message for message in result.messages))

    def test_secret_like_toml_value_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            secret_path = Path(temporary) / "secret.toml"
            secret_path.write_text(
                (ROOT / "configs/examples/sys4ai.example.toml").read_text(encoding="utf-8")
                + '\napi_key = "redacted-fixture"\n',
                encoding="utf-8",
            )
            with self._mutated_registry(
                "config_source_registry.csv",
                "config_id",
                "cfg_sys4ai_example",
                "path",
                str(secret_path),
            ) as path:
                result = validate_toml_config_surface(config_sources=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("secret-like key" in message for message in result.messages))

    def test_contract_target_drift_fails(self) -> None:
        with self._mutated_registry(
            "validation_contract_registry.csv",
            "contract_id",
            "contract_sys4ai_config",
            "target_format",
            "yaml",
        ) as path:
            result = validate_toml_config_surface(validation_contracts=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("must target TOML" in message for message in result.messages))

    def test_stale_generated_toml_index_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "toml-configuration-sources.md"
            path.write_text("> generated reader surface. It is not canonical\n", encoding="utf-8")
            result = validate_toml_config_surface(generated_toml_page=path, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("stale generated TOML index" in message for message in result.messages))

    def test_toml_writer_api_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "toml_io.py"
            source.write_text(
                (ROOT / "sys_for_ai/toml_io.py").read_text(encoding="utf-8")
                + "\n\ndef dump_toml(path, data):\n    path.write_text(str(data))\n",
                encoding="utf-8",
            )
            result = validate_toml_config_surface(toml_io_source=source, product_root=ROOT)
        self.assertFalse(result.ok)
        self.assertTrue(any("parse-only" in message or "writing call" in message for message in result.messages))

    @staticmethod
    def _mutated_registry(
        filename: str,
        id_field: str,
        row_id: str,
        field: str,
        value: str,
    ):
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
