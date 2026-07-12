"""Fail-closed contract checks for the supported-Python GitHub Actions matrix."""

from __future__ import annotations

from pathlib import Path

import yaml

from .registry_io import resolve_registered_path
from .validators import ValidationResult


EXPECTED_PYTHON_VERSIONS = ("3.10", "3.11", "3.12", "3.13", "3.14")
EXPECTED_TRIGGERS = {"push", "pull_request", "workflow_dispatch"}


def validate_cross_version_ci(
    workflow: str | Path = "../.github/workflows/cross-version-python.yml",
) -> ValidationResult:
    """Validate the exact read-only matrix and full-validation execution contract."""

    workflow_path = resolve_registered_path(str(workflow))
    messages: list[str] = []
    try:
        document = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return ValidationResult(False, [f"Cannot load cross-version CI workflow {workflow_path}: {exc}"])

    if not isinstance(document, dict):
        return ValidationResult(False, [f"{workflow_path}: workflow must be a mapping"])

    triggers = document.get("on")
    if not isinstance(triggers, dict) or set(triggers) != EXPECTED_TRIGGERS:
        messages.append(f"{workflow_path}: triggers must be exactly push, pull_request, and workflow_dispatch")
    else:
        push = triggers.get("push")
        branches = push.get("branches") if isinstance(push, dict) else None
        if branches != ["main"]:
            messages.append(f"{workflow_path}: push trigger must be restricted to main")

    permissions = document.get("permissions")
    if permissions != {"contents": "read"}:
        messages.append(f"{workflow_path}: workflow permissions must be exactly contents: read")

    jobs = document.get("jobs")
    validate_job = jobs.get("validate") if isinstance(jobs, dict) else None
    if not isinstance(validate_job, dict):
        messages.append(f"{workflow_path}: jobs.validate is required")
    else:
        if validate_job.get("runs-on") != "ubuntu-latest":
            messages.append(f"{workflow_path}: validation job must use ubuntu-latest")
        if validate_job.get("timeout-minutes") != 30:
            messages.append(f"{workflow_path}: validation job timeout must be 30 minutes")
        strategy = validate_job.get("strategy")
        matrix = strategy.get("matrix") if isinstance(strategy, dict) else None
        versions = matrix.get("python-version") if isinstance(matrix, dict) else None
        if tuple(versions or ()) != EXPECTED_PYTHON_VERSIONS:
            messages.append(
                f"{workflow_path}: Python matrix must be exactly {', '.join(EXPECTED_PYTHON_VERSIONS)}"
            )
        if not isinstance(strategy, dict) or strategy.get("fail-fast") is not False:
            messages.append(f"{workflow_path}: matrix fail-fast must be false so every version yields evidence")
        _validate_steps(workflow_path, validate_job.get("steps"), messages)

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            "Cross-version CI contract: 5/5 supported stable Python minors declared.",
            "The workflow is read-only, bounded to 30 minutes per job, and runs the full root validation on Python 3.10 through 3.14.",
        ],
    )


def _validate_steps(workflow_path: Path, steps: object, messages: list[str]) -> None:
    if not isinstance(steps, list):
        messages.append(f"{workflow_path}: validation job steps are required")
        return
    uses = [step.get("uses") for step in steps if isinstance(step, dict) and "uses" in step]
    if uses != ["actions/checkout@v6", "actions/setup-python@v6"]:
        messages.append(f"{workflow_path}: action dependencies must be exactly checkout@v6 and setup-python@v6")
    setup = next(
        (step for step in steps if isinstance(step, dict) and step.get("uses") == "actions/setup-python@v6"),
        None,
    )
    setup_with = setup.get("with") if isinstance(setup, dict) else None
    if not isinstance(setup_with, dict) or setup_with.get("python-version") != "${{ matrix.python-version }}":
        messages.append(f"{workflow_path}: setup-python must consume the declared matrix version")
    runs = [step.get("run", "") for step in steps if isinstance(step, dict) and "run" in step]
    combined = "\n".join(str(run) for run in runs)
    required_commands = (
        "python -m venv Sys4AI/.venv",
        "Sys4AI/.venv/bin/python -m pip install -r Sys4AI/requirements.txt",
        "make validate PY=python",
    )
    for command in required_commands:
        if command not in combined:
            messages.append(f"{workflow_path}: required command is missing: {command}")
    forbidden_markers = ("secrets.", "permissions: write", "sudo ", "deploy", "gh ")
    workflow_text = workflow_path.read_text(encoding="utf-8")
    for marker in forbidden_markers:
        if marker in workflow_text:
            messages.append(f"{workflow_path}: forbidden external-authority marker present: {marker}")
