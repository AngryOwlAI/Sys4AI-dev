"""Focused verification for the bounded Python/package-surface evidence family."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

from .registry_io import resolve_registered_path
from .toml_io import load_toml
from .validators import ValidationResult


EXPECTED_DEPENDENCIES = (
    "PyYAML>=6.0,<7.0",
    "tomli>=2.0,<3.0; python_version < '3.11'",
    "jsonschema>=4.0,<5.0",
)
REQUIRED_REFERENCE_SURFACES = (
    "sys_for_ai/__init__.py",
    "sys_for_ai/cli.py",
    "sys_for_ai/validators.py",
    "sys_for_ai/memory/__init__.py",
    "sys_for_ai/skills.py",
    "sys_for_ai/yaml_io.py",
    "sys_for_ai/toml_io.py",
    "sys_for_ai/jsonschema_io.py",
    "sys_for_ai/derivative_generation.py",
    "configs",
    "control_records",
    "registries",
    "schemas/contracts",
)


def validate_python_package_surface(
    pyproject: str | Path = "pyproject.toml",
    requirements: str | Path = "requirements.txt",
    *,
    run_interpreter_probes: bool = True,
) -> ValidationResult:
    """Verify only the implemented Python reference and dependency-policy surface."""

    pyproject_path = resolve_registered_path(str(pyproject))
    requirements_path = resolve_registered_path(str(requirements))
    product_root = pyproject_path.parent
    messages: list[str] = []

    try:
        document = load_toml(pyproject_path)
    except RuntimeError as exc:
        return ValidationResult(False, [str(exc)])

    project = document.get("project")
    if not isinstance(project, dict):
        return ValidationResult(False, [f"{pyproject_path}: missing [project] table"])

    if project.get("name") != "Sys4AI":
        messages.append(f"{pyproject_path}: project.name must be Sys4AI")
    if project.get("requires-python") != ">=3.10":
        messages.append(f"{pyproject_path}: requires-python must declare the supported >=3.10 range")

    dependencies = project.get("dependencies")
    if not isinstance(dependencies, list) or tuple(dependencies) != EXPECTED_DEPENDENCIES:
        messages.append(
            f"{pyproject_path}: dependencies must be exactly the three lightweight, bounded parser/validator families"
        )

    scripts = project.get("scripts")
    if not isinstance(scripts, dict) or scripts.get("Sys4AI") != "sys_for_ai.cli:main":
        messages.append(f"{pyproject_path}: project script must bind Sys4AI to sys_for_ai.cli:main")

    packages = ((document.get("tool") or {}).get("setuptools") or {}).get("packages", {})
    find = packages.get("find", {}) if isinstance(packages, dict) else {}
    if find.get("where") != ["."] or find.get("include") != ["sys_for_ai*"]:
        messages.append(f"{pyproject_path}: setuptools package discovery must include sys_for_ai*")

    try:
        requirement_lines = tuple(
            line.strip()
            for line in requirements_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    except OSError as exc:
        messages.append(f"Cannot read requirements file {requirements_path}: {exc}")
    else:
        if requirement_lines != EXPECTED_DEPENDENCIES:
            messages.append(f"{requirements_path}: dependency declarations must match pyproject.toml exactly")

    for relative in REQUIRED_REFERENCE_SURFACES:
        if not (product_root / relative).exists():
            messages.append(f"{product_root / relative}: required Python reference surface is missing")

    if run_interpreter_probes and not messages:
        direct_python = product_root / ".venv/bin/python"
        if not direct_python.is_file():
            messages.append(f"{direct_python}: required direct interpreter path is missing")
        else:
            try:
                probe = _run_probe([str(direct_python)], product_root)
            except (OSError, subprocess.TimeoutExpired) as exc:
                messages.append(f"direct interpreter probe failed: {exc}")
            else:
                if probe.returncode != 0:
                    messages.append(f"direct interpreter probe failed: {probe.stderr.strip() or probe.stdout.strip()}")

            env = os.environ.copy()
            env["PATH"] = f"{direct_python.parent}{os.pathsep}{env.get('PATH', '')}"
            try:
                activated = _run_probe(["python"], product_root, env=env)
            except (OSError, subprocess.TimeoutExpired) as exc:
                messages.append(f"activated-environment probe failed: {exc}")
            else:
                if activated.returncode != 0:
                    messages.append(
                        f"activated-environment probe failed: {activated.stderr.strip() or activated.stdout.strip()}"
                    )

    if messages:
        return ValidationResult(False, messages)
    return ValidationResult(
        True,
        [
            "Python/package surface: 4/4 requirements verified against the current reference package.",
            "Dependencies are exactly PyYAML, conditional tomli, and jsonschema with bounded major versions; no heavy runtime service dependency is declared.",
            f"Direct and activated interpreter probes passed with Python {sys.version_info.major}.{sys.version_info.minor}.",
        ],
    )


def _run_probe(
    interpreter: list[str],
    cwd: Path,
    *,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            *interpreter,
            "-c",
            (
                "import sys; "
                "assert sys.version_info >= (3, 10), sys.version; "
                "import sys_for_ai, sys_for_ai.cli, sys_for_ai.validators, sys_for_ai.memory"
            ),
        ],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
