"""Shared templates for generated derivative pages."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from ..registry_io import read_registry_rows
from ..validators import ValidationResult

GENERATED_AT = "2026-07-06T00:00:00Z"
NOTICE = (
    "> **Generated derivative notice**\n"
    ">\n"
    "> This page is a generated reader surface. It is not canonical. "
    "Canonical authority remains with the linked source files, registry rows, "
    "and validation contracts. Do not hand-edit this page as source authority.\n"
)
PROMOTION_PATH = (
    "Promotion requires an explicit source-authority decision, registry update, "
    "and validation evidence. This generated page is not promoted by generation."
)
STRUCTURAL_WARNING = (
    "Validation contracts prove structural conformance only. They do not prove "
    "semantic truth, product correctness, or implementation completeness."
)


def product_root(root: str | Path = ".") -> Path:
    """Resolve either repository root or product root to the product root."""

    base = Path(root).resolve()
    if (base / "registries").exists():
        return base
    if (base / "sys-for-ai/registries").exists():
        return base / "sys-for-ai"
    return base


def render_metadata(
    *,
    derivative_id: str,
    derivative_type: str,
    source_registries: list[str],
    validation_contracts: list[str],
    generator: str,
    source_hashes: Iterable[str] = ("pending",),
) -> str:
    """Render a deterministic page metadata YAML block."""

    lines = [
        "```yaml",
        "page_metadata:",
        f"  derivative_id: {derivative_id}",
        "  authority_status: generated_noncanonical",
        f"  derivative_type: {derivative_type}",
        "  source_registries:",
    ]
    lines.extend(f"    - {item}" for item in source_registries)
    lines.append("  validation_contracts:")
    lines.extend(f"    - {item}" for item in validation_contracts)
    lines.extend(
        [
            f"  generated_at: {GENERATED_AT}",
            f"  generator: {generator}",
            "  stale_or_orphan_status: current",
            "  source_hashes:",
        ]
    )
    lines.extend(f"    - {item}" for item in sorted(set(source_hashes)) if item)
    lines.append("```")
    return "\n".join(lines)


def render_page(
    *,
    title: str,
    derivative_id: str,
    derivative_type: str,
    source_registries: list[str],
    validation_contracts: list[str],
    generator: str,
    body: str,
    source_hashes: Iterable[str] = ("pending",),
) -> str:
    """Render a full generated derivative Markdown page."""

    return "\n\n".join(
        [
            NOTICE.rstrip(),
            render_metadata(
                derivative_id=derivative_id,
                derivative_type=derivative_type,
                source_registries=source_registries,
                validation_contracts=validation_contracts,
                generator=generator,
                source_hashes=source_hashes,
            ),
            f"# {title}",
            body.rstrip(),
        ]
    ) + "\n"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a Markdown table with escaped cell content."""

    if not rows:
        rows = [["No registered rows" for _ in headers]]
    header = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(_cell(value) for value in row) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def registry_trace_table(root: Path, derivative_ids: list[str]) -> str:
    """Render derivative registry trace rows."""

    rows_by_id = {
        row.get("derivative_id", ""): row
        for row in read_registry_rows(root / "registries/derivative_registry.csv")
    }
    rows: list[list[str]] = []
    for derivative_id in derivative_ids:
        row = rows_by_id.get(derivative_id, {})
        rows.append(
            [
                derivative_id,
                row.get("path", ""),
                row.get("source_ids", ""),
                row.get("generation_method", ""),
                row.get("status", ""),
            ]
        )
    return markdown_table(
        ["derivative_id", "path", "source_ids", "generation_method", "status"],
        rows,
    )


def check_or_write_pages(pages: dict[Path, str], *, write: bool, label: str) -> ValidationResult:
    """Check or write deterministic generated pages."""

    messages: list[str] = []
    ok = True
    for path, expected in sorted(pages.items()):
        if write:
            path.parent.mkdir(parents=True, exist_ok=True)
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current != expected:
                path.write_text(expected, encoding="utf-8")
                messages.append(f"{path}: wrote generated derivative")
            else:
                messages.append(f"{path}: generated derivative already current")
            continue
        if not path.exists():
            ok = False
            messages.append(f"{path}: missing generated derivative; run {label} --write")
            continue
        current = path.read_text(encoding="utf-8")
        if current != expected:
            ok = False
            messages.append(f"{path}: generated derivative differs; run {label} --write")
        else:
            messages.append(f"{path}: generated derivative current")
    return ValidationResult(ok, messages)


def source_hashes_from_rows(rows: list[dict[str, str]]) -> list[str]:
    """Collect source_hash values or pending markers from registry rows."""

    hashes = [row.get("source_hash", "pending") or "pending" for row in rows]
    return hashes or ["pending"]


def _cell(value: object) -> str:
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    return text if text else "pending"
