"""Tests for deterministic generated derivatives."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sys_for_ai.derivative_generation import (
    expected_governance_generated_docs,
    validate_generated_derivatives,
)
from sys_for_ai.derivatives import (
    check_config_control_wiki,
    check_validation_contracts_catalog,
    write_config_control_wiki,
    write_validation_contracts_catalog,
)


class GeneratedDerivativeTests(unittest.TestCase):
    def test_current_generated_derivatives_validate(self) -> None:
        result = validate_generated_derivatives("docs/generated", "registries/derivative_registry.csv")
        self.assertTrue(result.ok, result.messages)

    def test_strategic_governance_readers_are_generated_and_noncanonical(self) -> None:
        pages = expected_governance_generated_docs()
        names = {path.name for path in pages if path.parent.name == "governance"}
        self.assertEqual(
            {
                "capability-migration-status.md",
                "host-capability-profile.md",
                "lifecycle-and-patterns.md",
                "strategic-intent-contracts.md",
                "strategic-intent-evidence-graph.md",
            },
            names,
        )
        for path, text in pages.items():
            if path.parent.name != "governance":
                continue
            self.assertIn("authority_status: generated_noncanonical", text)
            self.assertIn("stale_or_orphan_status: current", text)
            self.assertNotIn("authority_status: canonical", text)

    def test_strategic_readers_preserve_gate_and_permission_boundaries(self) -> None:
        pages = expected_governance_generated_docs()
        combined = "\n".join(text for path, text in pages.items() if path.parent.name == "governance")
        self.assertIn("G-08 approves only the exact framework vision and values", combined)
        self.assertIn("G-07 remains open", combined)
        self.assertIn("Values do not grant permission", combined)
        self.assertNotIn("G-08 strategic approval remains open", combined)

    def test_config_control_check_fails_on_drift_and_write_repairs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _write_generated_fixture(root)

            write_result = write_config_control_wiki(root)
            self.assertTrue(write_result.ok, write_result.messages)
            target = root / "docs/generated/configuration_control/index.md"
            target.write_text("drift\n", encoding="utf-8")

            check_result = check_config_control_wiki(root)
            self.assertFalse(check_result.ok)

            rewrite_result = write_config_control_wiki(root)
            self.assertTrue(rewrite_result.ok, rewrite_result.messages)
            self.assertTrue(check_config_control_wiki(root).ok)
            text = target.read_text(encoding="utf-8")
            self.assertIn("authority_status: generated_noncanonical", text)
            self.assertNotIn("authority_status: canonical", text)

    def test_validation_contract_catalog_check_fails_on_drift_and_write_repairs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _write_generated_fixture(root)

            write_result = write_validation_contracts_catalog(root)
            self.assertTrue(write_result.ok, write_result.messages)
            target = root / "docs/generated/validation_contracts/index.md"
            target.write_text("drift\n", encoding="utf-8")

            check_result = check_validation_contracts_catalog(root)
            self.assertFalse(check_result.ok)

            rewrite_result = write_validation_contracts_catalog(root)
            self.assertTrue(rewrite_result.ok, rewrite_result.messages)
            self.assertTrue(check_validation_contracts_catalog(root).ok)
            text = target.read_text(encoding="utf-8")
            self.assertIn("Validation contracts prove structural conformance only.", text)
            self.assertNotIn("authority_status: canonical", text)


def _write_generated_fixture(root: Path) -> None:
    (root / "registries").mkdir(parents=True)
    (root / "docs/generated/configuration_control").mkdir(parents=True)
    (root / "docs/generated/validation_contracts").mkdir(parents=True)
    (root / "registries/format_profile_registry.csv").write_text(
        "format_id,extension,format_family,primary_role,canonical_roots,derivative_surfaces,"
        "registry_required,validator_required,default_authority_class,promotion_rule,secrets_allowed,notes\n"
        "fmt_yaml_control,.yaml,yaml,control,control_records,docs/generated,true,true,controlled,decision,false,fixture\n",
        encoding="utf-8",
    )
    (root / "registries/config_source_registry.csv").write_text(
        "config_id,path,format,config_domain,authority_status,owner,parser,validation_contract_id,"
        "consumers,secrets_allowed,environment_scope,supersedes,source_hash,last_validated_at,notes\n"
        "cfg_fixture,configs/example.toml,toml,fixture,controlled,test,tomllib,contract_toml,"
        "tests,false,local,,pending,pending,fixture\n",
        encoding="utf-8",
    )
    (root / "registries/control_record_registry.csv").write_text(
        "control_record_id,path,record_type,authority_status,owner,validation_contract_id,"
        "allowed_writers,allowed_readers,related_agentjob_id,supersedes,source_hash,last_validated_at,notes\n"
        "ctrl_fixture,control_records/example.yaml,agentjob,controlled,test,contract_agentjob,"
        "tester,all,AJ-FIXTURE,,pending,pending,fixture\n",
        encoding="utf-8",
    )
    (root / "registries/validation_contract_registry.csv").write_text(
        "contract_id,path,dialect,target_format,target_artifact_type,target_glob,authority_status,"
        "owner,validator_command,supersedes,source_hash,last_validated_at,notes\n"
        "contract_agentjob,schemas/contracts/agentjob.schema.json,2020-12,yaml,agentjob,"
        "control_records/**/*.yaml,controlled,test,validate-control-records,,pending,pending,fixture\n"
        "contract_toml,schemas/contracts/toml.schema.json,2020-12,toml,config,"
        "configs/**/*.toml,controlled,test,validate-toml,,pending,pending,fixture\n",
        encoding="utf-8",
    )
    (root / "registries/derivative_registry.csv").write_text(
        "derivative_id,path,derivative_type,source_ids,generation_method,last_generated,status,notes\n"
        "der_configuration_control_index,docs/generated/configuration_control/index.md,"
        "configuration_control_wiki_page,SRC-REG-FORMAT-PROFILES,deterministic,pending,generated_derivative,fixture\n"
        "der_configuration_control_yaml,docs/generated/configuration_control/yaml-control-records.md,"
        "configuration_control_wiki_page,SRC-REG-CONTROL-RECORDS,deterministic,pending,generated_derivative,fixture\n"
        "der_configuration_control_toml,docs/generated/configuration_control/toml-configuration-sources.md,"
        "configuration_control_wiki_page,SRC-REG-CONFIG-SOURCES,deterministic,pending,generated_derivative,fixture\n"
        "der_validation_contracts_index,docs/generated/validation_contracts/index.md,"
        "validation_contracts_catalog_page,SRC-REG-VALIDATION-CONTRACTS,deterministic,pending,generated_derivative,fixture\n"
        "der_validation_contracts_by_target,docs/generated/validation_contracts/contracts-by-target.md,"
        "validation_contracts_catalog_page,SRC-REG-VALIDATION-CONTRACTS,deterministic,pending,generated_derivative,fixture\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
