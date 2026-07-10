from __future__ import annotations

import copy
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from sys_for_ai.host_profiles import validate_host_capability_profiles
from sys_for_ai.toml_io import load_toml
from sys_for_ai.validators import ValidationResult
from sys_for_ai.yaml_io import dump_yaml


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = PRODUCT_ROOT / "configs/host_profiles/codex_app_reference.toml"
SCHEMA_PATH = PRODUCT_ROOT / "schemas/contracts/host_capability_profile.schema.json"


class HostCapabilityProfileTests(unittest.TestCase):
    def test_current_codex_reference_profile_passes_structurally(self) -> None:
        result = validate_host_capability_profiles(PROFILE_PATH, SCHEMA_PATH)

        self.assertTrue(result.ok, result.messages)
        self.assertTrue(any("G-07 remains open" in message for message in result.messages))

    def test_missing_interface_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["interfaces"].pop()

        self._assert_mutation_fails(mutate, "missing required interface")

    def test_duplicate_interface_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["interfaces"].append(copy.deepcopy(data["interfaces"][0]))

        self._assert_mutation_fails(mutate, "duplicate interface")

    def test_invalid_capability_state_fails_schema_and_invariant(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["interfaces"][0]["capability_status"] = "assumed_available"

        self._assert_mutation_fails(mutate, "invalid capability_status")

    def test_invalid_json_schema_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            schema_path = Path(temp_dir) / "invalid.schema.json"
            schema_path.write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema","type":7}\n',
                encoding="utf-8",
            )

            result = validate_host_capability_profiles(PROFILE_PATH, schema_path)

        self.assertFalse(result.ok)
        self.assertTrue(any("invalid JSON Schema" in message for message in result.messages))

    def test_pending_g07_with_verified_state_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["interfaces"][0]["capability_status"] = "verified_available"

        self._assert_mutation_fails(mutate, "requires capability_status 'unknown'")

    def test_pending_profile_requires_pending_verification_decision(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["profile"]["verification_decision"] = "DDR-SFADEV-HOST-G07-001"

        self._assert_mutation_fails(
            mutate,
            "pending G-07 profile requires profile.verification_decision='pending_G_07'",
        )

    def test_unknown_capability_cannot_execute(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["interfaces"][0]["execution_allowed"] = True

        self._assert_mutation_fails(mutate, "must not allow execution")

    def test_verified_unavailable_capability_cannot_execute(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            interface = data["interfaces"][0]
            interface["capability_status"] = "verified_unavailable"
            interface["execution_allowed"] = True

        self._assert_mutation_fails(mutate, "must not allow execution")

    def test_missing_permission_source_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["interfaces"][0].pop("permission_source")

        self._assert_mutation_fails(mutate, "missing or empty permission_source")

    def test_missing_source_evidence_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["interfaces"][0].pop("source_evidence")

        self._assert_mutation_fails(mutate, "missing or empty source_evidence")

    def test_missing_degraded_behavior_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["interfaces"][0].pop("degraded_behavior")

        self._assert_mutation_fails(mutate, "missing or empty degraded_behavior")

    def test_missing_cancellation_behavior_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["interfaces"][0].pop("cancellation_behavior")

        self._assert_mutation_fails(mutate, "missing or empty cancellation_behavior")

    def test_stale_evidence_cannot_execute(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            interface = data["interfaces"][0]
            interface["evidence_status"] = "stale"
            interface["execution_allowed"] = True

        self._assert_mutation_fails(mutate, "evidence_status 'stale' must not allow execution")

    def test_permission_precedence_reordering_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            order = data["permission_precedence"]["order"]
            if isinstance(order, list):
                order[0], order[1] = order[1], order[0]
            else:
                data["permission_precedence"]["order"] = order.replace(
                    "platform and system constraints -> host permissions",
                    "host permissions -> platform and system constraints",
                )

        self._assert_mutation_fails(mutate, "permission precedence must be exactly")

    def test_secret_like_key_fails(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["profile"]["api_key"] = "not-a-real-secret"

        self._assert_mutation_fails(mutate, "secret-like key")

    def test_host_profile_cannot_supply_sys4ai_purpose(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["profile"]["purpose_authority"] = True

        self._assert_mutation_fails(mutate, "profile.purpose_authority must be false")

    def test_host_profile_cannot_supply_sys4ai_values(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["profile"]["values_authority"] = True

        self._assert_mutation_fails(mutate, "profile.values_authority must be false")

    def test_pending_tx09_contract_cannot_be_executable(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["profile"]["portable_execution_contract_executable"] = True

        self._assert_mutation_fails(mutate, "pending_TX_09 portable execution contract must not be executable")

    def test_verified_capability_requires_fresh_rfc3339_evidence(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            profile = data["profile"]
            profile["verification_state"] = "verified_G_07"
            profile["verified_at"] = "2026-07-10T00:00:00Z"
            profile["verified_by"] = "verification_engineer"
            profile["portable_execution_contract_version"] = "1.0.0"
            profile["portable_execution_contract_executable"] = True

            interface = data["interfaces"][0]
            interface["capability_status"] = "verified_available"
            interface["execution_allowed"] = True
            interface["evidence_status"] = "current"
            interface["evidence_checked_at"] = "2026-07-10T00:00:00Z"
            interface["evidence_fresh_until"] = "2026-07-10T00:00:01Z"
            interface["positive_probe"] = "EVIDENCE-G07-POSITIVE-001"
            interface["denial_or_absence_probe"] = "EVIDENCE-G07-DENIAL-001"
            interface["evidence_capture"] = "EVIDENCE-G07-CAPTURE-001"

        self._assert_mutation_fails(mutate, "verified capability evidence is stale")

    def test_verified_profile_rejects_pending_interfaces(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _set_verified_profile_metadata(data)

        self._assert_mutation_fails(
            mutate,
            "verified G-07 profile requires evidence_status 'current'",
        )

    def test_verified_profile_rejects_pending_verification_decision(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_verified_profile(data)
            data["profile"]["verification_decision"] = "pending_G_07"

        self._assert_mutation_fails(
            mutate,
            "verified G-07 profile requires a nonpending verification_decision",
        )

    def test_verified_profile_rejects_future_verification_timestamp(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            now = datetime.now(timezone.utc)
            _make_verified_profile(data, now)
            data["profile"]["verified_at"] = _rfc3339(now + timedelta(days=1))

        self._assert_mutation_fails(mutate, "profile.verified_at must not be in the future")

    def test_verified_profile_rejects_future_evidence_checked_timestamp(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            now = datetime.now(timezone.utc)
            _make_verified_profile(data, now)
            data["interfaces"][0]["evidence_checked_at"] = _rfc3339(now + timedelta(days=1))
            data["interfaces"][0]["evidence_fresh_until"] = _rfc3339(now + timedelta(days=2))

        self._assert_mutation_fails(
            mutate,
            "evidence_checked_at must not be in the future",
        )

    def test_executable_capability_rejects_pending_tx09_contract(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_verified_profile(data)
            profile = data["profile"]
            profile["portable_execution_contract_version"] = "pending_TX_09"
            profile["portable_execution_contract_executable"] = False
            interface = data["interfaces"][0]
            interface["capability_status"] = "verified_available"
            interface["execution_allowed"] = True

        self._assert_mutation_fails(
            mutate,
            "execution requires a nonpending portable execution contract version",
        )

    def test_executable_capability_requires_executable_contract(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            _make_verified_profile(data)
            data["profile"]["portable_execution_contract_executable"] = False
            interface = data["interfaces"][0]
            interface["capability_status"] = "verified_available"
            interface["execution_allowed"] = True

        self._assert_mutation_fails(
            mutate,
            "profile.portable_execution_contract_executable=true",
        )

    def test_verified_profile_with_current_evidence_rejects_unregistered_decision(self) -> None:
        data = copy.deepcopy(load_toml(PROFILE_PATH))
        _make_verified_profile(data)
        data["profile"]["verification_decision"] = "DDR-TEST-FAKE-G07-999"

        result = self._validate_data(data)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "requires exactly one director_decision_registry.csv row; found 0" in message
                for message in result.messages
            ),
            result.messages,
        )

    def test_verified_profile_accepts_complete_temporary_g07_authority_fixture(self) -> None:
        data = copy.deepcopy(load_toml(PROFILE_PATH))
        _make_verified_profile(data)
        decision_id = "DDR-TEST-G07-ACCEPTED-001"
        data["profile"]["verification_decision"] = decision_id

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry_path = root / "registries/director_decision_registry.csv"
            decision_path = root / f"control_records/director_decisions/{decision_id}.yaml"
            registry_path.parent.mkdir(parents=True)
            decision_path.parent.mkdir(parents=True)
            registry_path.write_text(
                "director_decision_id,path,status,task_id,selected_route,selected_agentjob_id,"
                "authority_status,supersedes,source_hash,last_validated_at,notes\n"
                f"{decision_id},control_records/director_decisions/{decision_id}.yaml,completed,"
                "TASK-TEST-G07,accept_G_07,,controlled,,pending,pending,temporary test fixture\n",
                encoding="utf-8",
            )
            dump_yaml(
                decision_path,
                {
                    "director_decision_id": decision_id,
                    "decision_status": "completed",
                    "human_authorization": {
                        "model_self_approval": False,
                        "approval_evidence": "Temporary unit-test evidence only; not repository authority.",
                    },
                    "decision_context": {"gate_id": "G-07"},
                    "authority_boundary": {"accepts_gate_G_07": True},
                },
            )

            result = self._validate_data(data, registry_path)

        self.assertTrue(result.ok, result.messages)

    def test_cli_and_make_surfaces_exist(self) -> None:
        cli_text = (PRODUCT_ROOT / "sys_for_ai/cli.py").read_text(encoding="utf-8")
        make_text = (PRODUCT_ROOT / "Makefile").read_text(encoding="utf-8")

        self.assertIn('"validate-host-capability-profiles"', cli_text)
        self.assertIn("validate-host-capability-profiles:", make_text)

    def _assert_mutation_fails(
        self,
        mutate: Callable[[dict[str, Any]], None],
        expected_message: str,
    ) -> None:
        data = copy.deepcopy(load_toml(PROFILE_PATH))
        mutate(data)
        result = self._validate_data(data)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(expected_message in message for message in result.messages),
            result.messages,
        )

    def _validate_data(
        self,
        data: dict[str, Any],
        director_decision_registry_path: Path | None = None,
    ) -> ValidationResult:
        with tempfile.TemporaryDirectory() as temp_dir:
            profile_path = Path(temp_dir) / "mutated.toml"
            profile_path.write_text(_render_profile_toml(data), encoding="utf-8")

            if director_decision_registry_path is None:
                result = validate_host_capability_profiles(profile_path, SCHEMA_PATH)
            else:
                result = validate_host_capability_profiles(
                    profile_path,
                    SCHEMA_PATH,
                    director_decision_registry_path,
                )
        return result


def _render_profile_toml(data: dict[str, Any]) -> str:
    lines: list[str] = []
    for table_name in ("profile", "permission_precedence"):
        table = data[table_name]
        lines.append(f"[{table_name}]")
        lines.extend(f"{key} = {_toml_value(value)}" for key, value in table.items())
        lines.append("")

    for interface in data["interfaces"]:
        lines.append("[[interfaces]]")
        lines.extend(f"{key} = {_toml_value(value)}" for key, value in interface.items())
        lines.append("")

    return "\n".join(lines)


def _set_verified_profile_metadata(
    data: dict[str, Any],
    now: datetime | None = None,
) -> None:
    current = now or datetime.now(timezone.utc)
    profile = data["profile"]
    profile["verification_state"] = "verified_G_07"
    profile["verification_scope"] = "observable_host_conformance"
    profile["verification_decision"] = "DDR-SFADEV-HOST-G07-001"
    profile["verified_at"] = _rfc3339(current - timedelta(minutes=10))
    profile["verified_by"] = "verification_engineer"
    profile["portable_execution_contract_version"] = "1.0.0"
    profile["portable_execution_contract_executable"] = True


def _make_verified_profile(
    data: dict[str, Any],
    now: datetime | None = None,
) -> None:
    current = now or datetime.now(timezone.utc)
    _set_verified_profile_metadata(data, current)
    for index, interface in enumerate(data["interfaces"], start=1):
        interface["capability_status"] = "unknown"
        interface["execution_allowed"] = False
        interface["source_evidence"] = [f"EVIDENCE-G07-SOURCE-{index:03d}"]
        interface["evidence_status"] = "current"
        interface["evidence_checked_at"] = _rfc3339(current - timedelta(minutes=5))
        interface["evidence_fresh_until"] = _rfc3339(current + timedelta(days=1))
        interface["positive_probe"] = f"EVIDENCE-G07-POSITIVE-{index:03d}"
        interface["denial_or_absence_probe"] = f"EVIDENCE-G07-DENIAL-{index:03d}"
        interface["evidence_capture"] = f"EVIDENCE-G07-CAPTURE-{index:03d}"


def _rfc3339(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(item) for item in value) + "]"
    if isinstance(value, int):
        return str(value)
    raise TypeError(f"Unsupported TOML test value: {value!r}")


if __name__ == "__main__":
    unittest.main()
