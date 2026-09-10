"""Deployment candidate manifest validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "schema_version",
    "lesson_id",
    "candidate_id",
    "policy",
    "processor",
    "normalization",
    "observation_order",
    "action_order",
    "units",
    "frame",
    "rates_hz",
    "horizon",
    "assets",
    "calibration",
    "source_commit",
    "lock_sha256",
    "simulation_result",
    "deterministic_vector",
    "tolerances",
    "rollback",
}


def validate_bundle(path: Path) -> list[str]:
    """Validate completeness, policy hash, and deterministic sample output."""

    errors: list[str] = []
    manifest: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    for field in sorted(REQUIRED_FIELDS - set(manifest)):
        errors.append(f"missing field: {field}")
    policy = manifest.get("policy", {})
    policy_path = path.parent / str(policy.get("path", ""))
    if not policy_path.is_file():
        errors.append("missing policy file")
        return errors
    digest = hashlib.sha256(policy_path.read_bytes()).hexdigest()
    if digest != policy.get("sha256"):
        errors.append("policy checksum mismatch")
    weights = json.loads(policy_path.read_text(encoding="utf-8"))
    vector = manifest.get("deterministic_vector", {})
    inputs = [float(item) for item in vector.get("input", [])]
    expected = [float(item) for item in vector.get("expected_action", [])]
    actual = [
        sum(float(weight) * item for weight, item in zip(row, inputs, strict=True))
        + float(bias)
        for row, bias in zip(weights.get("weights", []), weights.get("bias", []), strict=True)
    ]
    tolerance = float(manifest.get("tolerances", {}).get("absolute", 0.0))
    if len(actual) != len(expected) or any(
        abs(left - right) > tolerance for left, right in zip(actual, expected, strict=True)
    ):
        errors.append("deterministic vector mismatch")
    return errors
