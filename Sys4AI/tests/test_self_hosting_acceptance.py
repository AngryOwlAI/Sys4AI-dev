"""Acceptance wiring tests for retained self-hosting memory evidence."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

from sys_for_ai.yaml_io import load_yaml


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PRODUCT_ROOT.parent


class SelfHostingAcceptanceTests(unittest.TestCase):
    def test_program_state_uses_portable_current_execution_fields(self) -> None:
        state = load_yaml(PRODUCT_ROOT / "control_records/program_state.yaml")

        self.assertEqual("active", state["state_status"])
        self.assertIsNone(state["active_execution_transaction_id"])
        self.assertIsNone(state["active_director_decision_id"])
        self.assertEqual(
            "RECEIPT-SFADEV-STRATEGIC-BASELINE-TX20-001",
            state["latest_closeout_evidence_id"],
        )
        self.assertEqual(
            "HANDOFF-SFADEV-STRATEGIC-BASELINE-TX20-001",
            state["latest_handoff_evidence_id"],
        )
        self.assertEqual("ready", state["continuation_state"])
        self.assertEqual("not_requested", state["cancellation_state"])
        self.assertEqual("not_required", state["escalation_state"])
        self.assertFalse(state["human_gate_required"])
        self.assertEqual("implemented", state["capability_status_summary"]["safety_evaluation_controls"])
        self.assertEqual("accepted_G_08", state["capability_status_summary"]["strategic_approval"])
        self.assertEqual("complete_G_09", state["capability_status_summary"]["derivative_regeneration"])

        handoff_rows = _rows(PRODUCT_ROOT / "registries/handoff_registry.csv", "handoff_id")
        completion_rows = _rows(PRODUCT_ROOT / "registries/completion_receipt_registry.csv", "completion_receipt_id")
        self.assertIn(state["latest_closeout_evidence_id"], completion_rows)
        self.assertIn(state["latest_handoff_evidence_id"], handoff_rows)
        self.assertIn("RECEIPT-SFADEV-STRATEGIC-BASELINE-TX17-001", completion_rows)
        self.assertIn("HANDOFF-SFADEV-STRATEGIC-BASELINE-TX17-001", handoff_rows)
        self.assertIn("RECEIPT-SFADEV-STRATEGIC-BASELINE-TX18-001", completion_rows)
        self.assertIn("HANDOFF-SFADEV-STRATEGIC-BASELINE-TX18-001", handoff_rows)
        self.assertIn("RECEIPT-SFADEV-STRATEGIC-BASELINE-TX19-001", completion_rows)
        self.assertIn("HANDOFF-SFADEV-STRATEGIC-BASELINE-TX19-001", handoff_rows)
        self.assertIn("RECEIPT-SFADEV-STRATEGIC-BASELINE-TX20-001", completion_rows)
        self.assertIn("HANDOFF-SFADEV-STRATEGIC-BASELINE-TX20-001", handoff_rows)
        self.assertIn("RECEIPT-P1-SELFHOST-ACCEPTANCE-001", completion_rows)
        self.assertIn("RECEIPT-SYS4AI-DEV-NAME-MIGRATION-001", completion_rows)
        self.assertIn("RECEIPT-SFADEV-20-WALKING-SKELETON-FLOW-001", completion_rows)
        self.assertIn("RECEIPT-SFADEV-21-TARGET-PACKAGE-SMOKE-001", completion_rows)
        self.assertIn("RECEIPT-SFADEV-22-WALKING-SKELETON-DEMO-001", completion_rows)
        self.assertIn("RECEIPT-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001", completion_rows)
        self.assertIn("RECEIPT-SFADEV-24-SUBPRD-DRAFTS-001", completion_rows)
        self.assertIn("RECEIPT-SFADEV-25-SUBPRD-PROMOTION-001", completion_rows)
        self.assertIn("RECEIPT-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001", completion_rows)
        self.assertIn("HANDOFF-P1-SELFHOST-ACCEPTANCE-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-05-RUNTIME-SKILL-RECONCILIATION-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-01-PRD-INTEGRATION-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-03-DISCOVERY-GATE-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-04-ROLE-GOVERNANCE-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-06-SKILL-LIFECYCLE-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-08-CORE-SKILLS-BATCH-2-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-09-GENERATED-DOCS-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-10-END-TO-END-ACCEPTANCE-001", handoff_rows)
        self.assertIn("HANDOFF-SYS4AI-DEV-NAME-MIGRATION-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-20-WALKING-SKELETON-FLOW-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-21-TARGET-PACKAGE-SMOKE-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-22-WALKING-SKELETON-DEMO-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-24-SUBPRD-DRAFTS-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-25-SUBPRD-PROMOTION-001", handoff_rows)
        self.assertIn("HANDOFF-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001", handoff_rows)

    def test_acceptance_receipt_and_handoff_are_registered(self) -> None:
        receipt = load_yaml(PRODUCT_ROOT / "control_records/completions/RECEIPT-P1-SELFHOST-ACCEPTANCE-001.yaml")
        handoff = load_yaml(PRODUCT_ROOT / "control_records/handoffs/HANDOFF-P1-SELFHOST-ACCEPTANCE-001.yaml")
        completion_rows = _rows(PRODUCT_ROOT / "registries/completion_receipt_registry.csv", "completion_receipt_id")
        handoff_rows = _rows(PRODUCT_ROOT / "registries/handoff_registry.csv", "handoff_id")

        self.assertEqual("AJ-P1-SELFHOST-ACCEPTANCE-001", receipt["agentjob_id"])
        self.assertEqual("PASS", receipt["result"])
        self.assertEqual("HANDOFF-P1-SELFHOST-ACCEPTANCE-001", receipt["next_handoff_id"])
        self.assertEqual("RECEIPT-P1-SELFHOST-ACCEPTANCE-001", handoff["traceability"]["completion_receipt_id"])
        self.assertIn("RECEIPT-P1-SELFHOST-ACCEPTANCE-001", completion_rows)
        self.assertIn("HANDOFF-P1-SELFHOST-ACCEPTANCE-001", handoff_rows)

    def test_initial_director_decision_is_closed(self) -> None:
        decision = load_yaml(PRODUCT_ROOT / "control_records/director_decisions/DDR-P1-SELFHOST-001.yaml")
        rows = _rows(PRODUCT_ROOT / "registries/director_decision_registry.csv", "director_decision_id")

        self.assertEqual("completed", decision["decision_status"])
        self.assertEqual("completed", rows["DDR-P1-SELFHOST-001"]["status"])

    def test_trace_registry_contains_acceptance_evidence(self) -> None:
        rows = _rows(PRODUCT_ROOT / "registries/requirement_trace_registry.csv", "trace_id")
        for trace_id in [
            "TRACE-SFA-CORE-CONT-001",
            "TRACE-SFA-CORE-CONT-002",
            "TRACE-SFA-P0-FR-019",
            "TRACE-SFA-P0-NFR-010",
            "TRACE-SFA-CORE-DOC-007",
            "TRACE-SFA-CORE-MEM-009",
        ]:
            row = rows[trace_id]
            self.assertIn("implementation_plans/self_hosting_memory_continue_acceptance_report.md", row["evidence_paths"])
            self.assertEqual("sufficient", row["semantic_review_verdict"])

    def test_acceptance_report_covers_twenty_criteria(self) -> None:
        report = (WORKSPACE_ROOT / "implementation_plans/self_hosting_memory_continue_acceptance_report.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("# Self-Hosting Memory and Continue Acceptance Report", report)
        self.assertEqual(20, report.count("| SFA-ACCEPT-"))
        self.assertIn("SFA-ACCEPT-020", report)
        self.assertIn("Conclusion: Accepted", report)

    def test_makefile_exposes_sync_check_target(self) -> None:
        makefile = (PRODUCT_ROOT / "Makefile").read_text(encoding="utf-8")

        self.assertIn("SYNC_REMOTE ?= origin", makefile)
        self.assertIn("SYNC_BRANCH ?= main", makefile)
        self.assertIn("SYNC_CHECK_HASHES ?= 0", makefile)
        self.assertIn("sync-check:", makefile)
        self.assertIn("git fetch", makefile)
        self.assertIn("HEAD does not match", makefile)
        self.assertIn("memory status --json", makefile)
        self.assertIn("memory validate-hashes --json", makefile)


def _rows(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


if __name__ == "__main__":
    unittest.main()
