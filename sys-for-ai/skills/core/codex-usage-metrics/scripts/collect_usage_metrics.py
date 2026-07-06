#!/usr/bin/env python3
"""Collect latest Codex usage metrics into a deterministic text receipt."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    skill_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description=(
            "Collect the latest Codex token_count metrics from a rollout JSONL "
            "file and write a refreshed text receipt."
        )
    )
    parser.add_argument(
        "--session-file",
        type=Path,
        help="Path to a Codex rollout JSONL file.",
    )
    parser.add_argument(
        "--session-id",
        help="Session id to search for under CODEX_HOME/sessions.",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path.home() / ".codex",
        help="Codex state directory. Defaults to ~/.codex.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=skill_root / "usage-metrics.txt",
        help="Output text file. Defaults to usage-metrics.txt in the skill folder.",
    )
    parser.add_argument(
        "--include-source-path",
        action="store_true",
        help="Include the full source session path in the receipt.",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def select_session_file(args: argparse.Namespace) -> Path:
    if args.session_file:
        session_file = args.session_file.expanduser().resolve()
        if not session_file.is_file():
            fail(f"session file not found: {session_file}")
        return session_file

    sessions_root = args.codex_home.expanduser().resolve() / "sessions"
    if not sessions_root.is_dir():
        fail(f"Codex sessions directory not found: {sessions_root}")

    if args.session_id:
        candidates = list(sessions_root.rglob(f"*{args.session_id}*.jsonl"))
    else:
        candidates = list(sessions_root.rglob("*.jsonl"))

    candidates = [candidate for candidate in candidates if candidate.is_file()]
    if not candidates:
        if args.session_id:
            fail(f"no rollout file found for session id: {args.session_id}")
        fail(f"no rollout JSONL files found under: {sessions_root}")

    return max(candidates, key=lambda candidate: candidate.stat().st_mtime)


def parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        return datetime.fromisoformat(normalized).astimezone()
    except ValueError:
        return None


def format_datetime(value: datetime | None) -> str:
    if value is None:
        return "unknown"
    return value.strftime("%Y-%m-%d %I:%M:%S %p %Z")


def format_epoch(value: Any) -> str:
    if value is None:
        return "unknown"
    try:
        return format_datetime(datetime.fromtimestamp(int(value)).astimezone())
    except (TypeError, ValueError, OSError, OverflowError):
        return "unknown"


def format_int(value: Any) -> str:
    if value is None:
        return "unknown"
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "unknown"


def format_percent(value: Any) -> str:
    if value is None:
        return "unknown"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "unknown"
    if number.is_integer():
        return f"{int(number)}%"
    return f"{number:.1f}%"


def percent_left(used_percent: Any) -> float | None:
    try:
        return max(0.0, 100.0 - float(used_percent))
    except (TypeError, ValueError):
        return None


def context_left_percent(context_used: Any, context_window: Any) -> float | None:
    try:
        used = float(context_used)
        window = float(context_window)
    except (TypeError, ValueError):
        return None
    if window <= 0:
        return None
    return max(0.0, (window - used) / window * 100.0)


def latest_metrics(session_file: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    session_meta: dict[str, Any] = {}
    latest_token_count: dict[str, Any] | None = None

    with session_file.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                fail(f"invalid JSON on line {line_number}: {exc}")

            if record.get("type") == "session_meta":
                payload = record.get("payload")
                if isinstance(payload, dict):
                    session_meta = payload
                continue

            if record.get("type") != "event_msg":
                continue

            payload = record.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "token_count":
                latest_token_count = record

    if latest_token_count is None:
        fail(f"no token_count event found in: {session_file}")

    return session_meta, latest_token_count


def source_label(session_file: Path, include_source_path: bool) -> str:
    if include_source_path:
        return str(session_file)
    return session_file.name


def build_receipt(
    session_file: Path,
    session_meta: dict[str, Any],
    token_record: dict[str, Any],
    include_source_path: bool,
) -> str:
    payload = token_record.get("payload", {})
    info = payload.get("info", {}) if isinstance(payload, dict) else {}
    rate_limits = payload.get("rate_limits", {}) if isinstance(payload, dict) else {}

    total = info.get("total_token_usage", {}) if isinstance(info, dict) else {}
    last = info.get("last_token_usage", {}) if isinstance(info, dict) else {}
    context_window = info.get("model_context_window") if isinstance(info, dict) else None
    context_used = last.get("input_tokens") if isinstance(last, dict) else None
    context_left = context_left_percent(context_used, context_window)

    primary = rate_limits.get("primary", {}) if isinstance(rate_limits, dict) else {}
    secondary = rate_limits.get("secondary", {}) if isinstance(rate_limits, dict) else {}
    primary_left = percent_left(primary.get("used_percent")) if isinstance(primary, dict) else None
    secondary_left = (
        percent_left(secondary.get("used_percent")) if isinstance(secondary, dict) else None
    )

    generated_at = format_datetime(datetime.now().astimezone())
    metrics_event = format_datetime(parse_iso_datetime(token_record.get("timestamp")))
    session_id = (
        session_meta.get("session_id")
        or session_meta.get("id")
        or session_meta.get("payload", {}).get("id")
        or "unknown"
    )

    lines = [
        "Codex Usage Metrics",
        f"Generated at: {generated_at}",
        f"Metrics event: {metrics_event}",
        f"Source session file: {source_label(session_file, include_source_path)}",
        f"Session: {session_id}",
        f"Title: {session_meta.get('thread_name') or session_meta.get('title') or 'unknown'}",
        f"CWD: {session_meta.get('cwd') or 'unknown'}",
        f"Model provider: {session_meta.get('model_provider') or 'unknown'}",
        f"Model: {session_meta.get('model') or 'unknown'}",
        "",
        "Context:",
        f"  Window: {format_int(context_window)} tokens",
        f"  Used: {format_int(context_used)} tokens",
        f"  Left: {format_percent(context_left)}",
        "",
        "Rate Limits:",
        (
            "  Primary "
            f"({format_int(primary.get('window_minutes') if isinstance(primary, dict) else None)} minutes): "
            f"{format_percent(primary_left)} left, "
            f"{format_percent(primary.get('used_percent') if isinstance(primary, dict) else None)} used, "
            f"resets {format_epoch(primary.get('resets_at') if isinstance(primary, dict) else None)}"
        ),
        (
            "  Secondary "
            f"({format_int(secondary.get('window_minutes') if isinstance(secondary, dict) else None)} minutes): "
            f"{format_percent(secondary_left)} left, "
            f"{format_percent(secondary.get('used_percent') if isinstance(secondary, dict) else None)} used, "
            f"resets {format_epoch(secondary.get('resets_at') if isinstance(secondary, dict) else None)}"
        ),
        f"  Plan type: {rate_limits.get('plan_type') if isinstance(rate_limits, dict) else 'unknown'}",
        (
            "  Rate limit reached: "
            f"{rate_limits.get('rate_limit_reached_type') or 'no' if isinstance(rate_limits, dict) else 'unknown'}"
        ),
        "",
        "Token Usage:",
        f"  Cumulative input: {format_int(total.get('input_tokens') if isinstance(total, dict) else None)} tokens",
        (
            "  Cumulative cached input: "
            f"{format_int(total.get('cached_input_tokens') if isinstance(total, dict) else None)} tokens"
        ),
        f"  Cumulative output: {format_int(total.get('output_tokens') if isinstance(total, dict) else None)} tokens",
        (
            "  Cumulative reasoning output: "
            f"{format_int(total.get('reasoning_output_tokens') if isinstance(total, dict) else None)} tokens"
        ),
        f"  Cumulative total: {format_int(total.get('total_tokens') if isinstance(total, dict) else None)} tokens",
        f"  Last request input: {format_int(last.get('input_tokens') if isinstance(last, dict) else None)} tokens",
        (
            "  Last request cached input: "
            f"{format_int(last.get('cached_input_tokens') if isinstance(last, dict) else None)} tokens"
        ),
        f"  Last request output: {format_int(last.get('output_tokens') if isinstance(last, dict) else None)} tokens",
        (
            "  Last request reasoning output: "
            f"{format_int(last.get('reasoning_output_tokens') if isinstance(last, dict) else None)} tokens"
        ),
        f"  Last request total: {format_int(last.get('total_tokens') if isinstance(last, dict) else None)} tokens",
        "",
        "Notes:",
        "  Context used is taken from latest last_token_usage.input_tokens.",
        "  This is a point-in-time receipt; later messages can change live usage.",
        "  The collector intentionally excludes conversation transcript content.",
        "",
    ]
    return "\n".join(lines)


def write_receipt(output: Path, text: str) -> None:
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    output.write_text(text, encoding="utf-8")


def main() -> None:
    args = parse_args()
    session_file = select_session_file(args)
    session_meta, token_record = latest_metrics(session_file)
    receipt = build_receipt(
        session_file=session_file,
        session_meta=session_meta,
        token_record=token_record,
        include_source_path=args.include_source_path,
    )
    write_receipt(args.output, receipt)
    print(f"Wrote usage metrics: {args.output.expanduser().resolve()}")


if __name__ == "__main__":
    main()
