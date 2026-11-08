"""Single-use, exact-action approval gate for an injected, independently validated transport.

No vendor connection, enable, or torque API is provided by this module.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import time
from pathlib import Path
from typing import Any, Protocol

from pai_lab.hardware.preflight import preflight


class Transport(Protocol):
    def snapshot(self) -> Path: ...
    def move(self, positions_rad: list[float], *, timeout_s: float) -> bool: ...
    def stop(self) -> None: ...


def digest(card: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(card, sort_keys=True, allow_nan=False).encode()).hexdigest()


def execute(
    card: dict[str, Any],
    approval: str,
    transport: Transport,
    ledger: Path,
) -> None:
    """Consume exact approval before sending one bounded joint command. Failures stop."""
    if approval != f"APPROVE {digest(card)}":
        raise PermissionError("exact run-card approval required")
    now = time.time()
    try:
        created, expires = float(card["created_at"]), float(card["expires_at"])
        if not all(math.isfinite(x) for x in (created, expires)):
            raise ValueError("invalid card time")
        if not created <= now < expires or not 0 < expires - created <= 60:
            raise ValueError("expired or future run card")
        if card["robot"] != "enlight" or card["action"] != "small-joint-move":
            raise ValueError("unsupported robot/action")
        if card["joint_group"] != "arm" or card["units"] != "rad":
            raise ValueError("invalid joint group/units")
        timeout = float(card["timeout_s"])
        delta = float(card["max_delta_rad"])
        target = [float(x) for x in card["positions_rad"]]
        if (
            len(target) != 7
            or not all(math.isfinite(x) for x in target)
            or not 0 < timeout <= 1
            or not 0 < delta <= 0.02
        ):
            raise ValueError("invalid limits")
        # Compatibility, tool, and site reviews are deliberately mandatory.
        for gate in ("model_compatibility_reviewed", "tool_payload_reviewed", "stop_tested"):
            if card.get(gate) is not True:
                raise ValueError(f"unverified {gate}")
        snapshot = transport.snapshot()
        readiness = preflight("enlight", snapshot, read_only=True)
        state = json.loads(snapshot.read_text())
        if not readiness["ready"] or card["model"] != state["model"]:
            raise ValueError("device readiness/model mismatch")
        if state.get("robot_identity") != card.get("robot_identity") or not card.get(
            "robot_identity"
        ):
            raise ValueError("exact device identity required")
        for q, current, bounds in zip(
            target, state["positions_rad"], state["position_limits_rad"], strict=True
        ):
            if abs(q - current) > delta or not bounds[0] <= q <= bounds[1]:
                raise ValueError("command exceeds limits")
        ledger.mkdir(parents=True, exist_ok=True)
        receipt = ledger / (digest(card) + ".consumed")
        # Exclusive creation makes replay fail, including after a transport failure.
        descriptor = os.open(receipt, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(descriptor, "w") as stream:
            stream.write(str(now))
            stream.flush()
            os.fsync(stream.fileno())
        started = time.monotonic()
        acknowledged = transport.move(target, timeout_s=timeout)
        if time.monotonic() - started > timeout or time.time() >= expires:
            raise TimeoutError("command acknowledgement deadline exceeded")
        if acknowledged is not True:
            raise RuntimeError("command not acknowledged")
    except BaseException:
        transport.stop()
        raise
    transport.stop()
