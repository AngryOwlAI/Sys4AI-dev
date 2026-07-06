"""Tests for runtime, shim, and product scaffold skill surfaces."""

from __future__ import annotations

import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


class SkillSurfaceTests(unittest.TestCase):
    def test_active_runtime_continue_skill_exists(self) -> None:
        text = _read(".agents/skills/continue/SKILL.md")

        self.assertIn("name: continue", text)
        self.assertIn("advance at most one authorized AgentJob", text)
        self.assertIn("Write a completion receipt and handoff", text)

    def test_active_runtime_source_first_memory_skill_exists(self) -> None:
        text = _read(".agents/skills/source-first-memory/SKILL.md")

        self.assertIn("name: source-first-memory", text)
        self.assertIn("Memory lookup finds likely sources. It does not decide truth or permission.", text)
        self.assertIn("Inspect the canonical source path or registry row", text)

    def test_codex_shims_point_to_agents_runtime_skills(self) -> None:
        continue_text = _read(".codex/skills/continue/SKILL.md")
        memory_text = _read(".codex/skills/source-first-memory/SKILL.md")

        self.assertIn(".agents/skills/continue/SKILL.md", continue_text)
        self.assertIn("compatibility shim", continue_text)
        self.assertIn(".agents/skills/source-first-memory/SKILL.md", memory_text)
        self.assertIn("compatibility shim", memory_text)

    def test_product_scaffold_skills_are_generic(self) -> None:
        for relative in [
            "sys-for-ai/skills/core/continue/SKILL.md",
            "sys-for-ai/skills/core/continue/README.md",
            "sys-for-ai/skills/core/continue/AGENTS.md",
            "sys-for-ai/skills/core/continue/examples/portable-example.md",
            "sys-for-ai/skills/core/source-first-memory/SKILL.md",
            "sys-for-ai/skills/core/source-first-memory/README.md",
            "sys-for-ai/skills/core/source-first-memory/AGENTS.md",
            "sys-for-ai/skills/core/source-first-memory/examples/portable-example.md",
        ]:
            text = _read(relative)
            self.assertNotIn("Codex", text, relative)
            self.assertRegex(text, r"target[ -]system", relative)

    def test_context_45_temp_prd_is_threshold_only(self) -> None:
        rule = "Do not create, overwrite, or refresh `temp_prd.md` after each question when context is still safe."
        failure = "metrics are unavailable"

        for skill in [
            "decision-grilling-context-45",
            "domain-grilling-with-docs-context-45",
            "system-definition-interview-context-45",
        ]:
            for relative in [
                f".agents/skills/{skill}/SKILL.md",
                f"sys-for-ai/skills/core/{skill}/SKILL.md",
            ]:
                text = _read(relative)
                normalized = " ".join(text.split())
                self.assertIn(rule, normalized, relative)
                self.assertRegex(text, r"context left is (at most 55 percent|55 percent or lower|`<= 55%`)", relative)
                self.assertIn(failure, text, relative)

        policy = _read("sys-for-ai/docs/skill_integration_policy.md")
        normalized_policy = " ".join(policy.split())
        self.assertIn(rule, normalized_policy)
        self.assertIn("not the normal per-question state file", policy)


def _read(relative: str) -> str:
    return (WORKSPACE_ROOT / relative).read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
