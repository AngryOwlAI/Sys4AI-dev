"""Memory preflight support placeholder.

Phase 4 adds receipt-writing behavior. Phase 3 keeps this module present so
the memory package shape is stable before preflight is wired into /continue.
"""

from __future__ import annotations


def preflight_not_implemented() -> dict[str, object]:
    return {"ok": False, "status": "BLOCKED", "reason": "memory_preflight_phase_4_not_implemented"}
