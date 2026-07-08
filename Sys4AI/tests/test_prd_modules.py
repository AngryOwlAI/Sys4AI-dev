from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

from sys_for_ai.prd_modules import validate_prd_modules

PRODUCT_ROOT = Path(__file__).resolve().parents[1]

HEADER = (
    "prd_module_id,path,title,status,subject_layer,authority_scope,owns_requirement_prefixes,"
    "references_source_prds,supersedes,source_authority_status,owner_role,validation_status,"
    "source_hash,last_validated_at,notes\n"
)


class PrdModuleTests(unittest.TestCase):
    def test_current_prd_module_registry_passes(self) -> None:
        result = validate_prd_modules("registries/prd_module_registry.csv")

        self.assertTrue(result.ok, result.messages)

    def test_planned_modules_may_reference_future_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registry = _write_fixture(Path(temp_dir), status="planned", validation_status="planned")

            with _working_directory(registry.parents[1]):
                result = validate_prd_modules("registries/prd_module_registry.csv")

            self.assertTrue(result.ok, result.messages)

    def test_duplicate_canonical_requirement_ownership_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registry = _write_fixture(
                Path(temp_dir),
                status="canonical",
                validation_status="validated",
                source_authority_status="canonical",
                duplicate_canonical=True,
            )

            with _working_directory(registry.parents[1]):
                result = validate_prd_modules("registries/prd_module_registry.csv")

            self.assertFalse(result.ok)
            self.assertTrue(
                any("multiple canonical owners" in message for message in result.messages),
                result.messages,
            )

    def test_draft_cannot_claim_canonical_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registry = _write_fixture(
                Path(temp_dir),
                status="draft",
                validation_status="pending",
                source_authority_status="canonical",
                write_module=True,
            )

            with _working_directory(registry.parents[1]):
                result = validate_prd_modules("registries/prd_module_registry.csv")

            self.assertFalse(result.ok)
            self.assertTrue(
                any("draft module cannot claim canonical authority" in message for message in result.messages),
                result.messages,
            )


def _write_fixture(
    temp_root: Path,
    *,
    status: str,
    validation_status: str,
    source_authority_status: str = "derivative_draft",
    duplicate_canonical: bool = False,
    write_module: bool = False,
) -> Path:
    product = temp_root / "Sys4AI"
    registries = product / "registries"
    registries.mkdir(parents=True)
    (product / "schemas/contracts").mkdir(parents=True)
    shutil.copyfile(
        PRODUCT_ROOT / "schemas/contracts/prd_module_registry_row.schema.json",
        product / "schemas/contracts/prd_module_registry_row.schema.json",
    )
    prds = temp_root / "PRDs"
    prds.mkdir()
    source_prd = prds / "source.md"
    source_prd.write_text("# Source\n", encoding="utf-8")

    (registries / "system_layer_registry.csv").write_text(
        "layer_id,layer_name,layer_type,canonical_roots,mutable_roots,derivative_roots,authority_notes,requires_director_decision_for_mutation,default_validators,owner,source_hash,last_validated_at,notes\n"
        "framework_product,Framework product,framework,PRDs,PRDs/modules,,fixture,false,,test,pending,pending,fixture\n",
        encoding="utf-8",
    )
    (registries / "role_registry.csv").write_text(
        "role_id,role_name,role_class,system_layer_scope,primary_mission,required_skills,optional_skills,forbidden_skills,primary_outputs,allowed_artifact_classes,may_create_agentjobs,requires_director_decision,authority_status,owner,supersedes,source_hash,last_validated_at,notes\n"
        "requirements_manager,Requirements Manager,governance,framework_product,fixture,,,,,prd,true,false,controlled,test,,pending,pending,fixture\n",
        encoding="utf-8",
    )
    (registries / "requirement_trace_registry.csv").write_text(
        "trace_id,phase0_selector,phase0_source,coverage_status,trace_class,semantic_justification,semantic_review_verdict,phase1_selectors,evidence_paths,notes\n"
        "TRACE-PRD-MOD-ONE,SFA-CORE-ONE,PRD-MOD-ONE,covered,implemented,fixture,sufficient,PRD-MOD-ONE,PRD-MOD-ONE,fixture\n"
        "TRACE-PRD-MOD-TWO,SFA-CORE-ONE,PRD-MOD-TWO,covered,implemented,fixture,sufficient,PRD-MOD-TWO,PRD-MOD-TWO,fixture\n",
        encoding="utf-8",
    )

    module_path = prds / "module.md"
    if write_module or status != "planned":
        module_path.write_text(
            "# Module\n\n"
            "> Authority notice: fixture.\n\n"
            "**Source PRDs:** source.md\n"
            "**Subject layer:** framework_product\n"
            f"**Source authority status:** {source_authority_status}\n",
            encoding="utf-8",
        )

    rows = [
        _row("PRD-MOD-ONE", module_path, source_prd, status, source_authority_status, validation_status),
    ]
    if duplicate_canonical:
        second_module = prds / "module_two.md"
        second_module.write_text(module_path.read_text(encoding="utf-8"), encoding="utf-8")
        rows.append(_row("PRD-MOD-TWO", second_module, source_prd, status, source_authority_status, validation_status))

    registry = registries / "prd_module_registry.csv"
    registry.write_text(HEADER + "".join(rows), encoding="utf-8")
    return registry


def _row(
    module_id: str,
    module_path: Path,
    source_prd: Path,
    status: str,
    source_authority_status: str,
    validation_status: str,
) -> str:
    module_registry_path = f"PRDs/{module_path.name}"
    source_registry_path = f"PRDs/{source_prd.name}"
    return (
        f"{module_id},{module_registry_path},Fixture Module,{status},framework_product,fixture_scope,"
        f"SFA-CORE-ONE,{source_registry_path},,{source_authority_status},requirements_manager,"
        f"{validation_status},pending,2026-07-08T22:26:00Z,fixture\n"
    )


@contextmanager
def _working_directory(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
