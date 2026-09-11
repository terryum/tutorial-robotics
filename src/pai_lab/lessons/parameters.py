"""Named, bounded experiment inputs; legacy variant remains readable."""

from __future__ import annotations

import math

# name: (default, minimum exclusive, maximum inclusive, units)
PARAMETERS = {
    "core-04": {"camera_azimuth": (135.0, -360.0, 360.0, "degree")},
    "core-01": {"timestep": (0.002, 0.0, 0.01, "s")},
    "core-fr3-02": {
        "kp": (120.0, 0.0, 500.0, "Nm/rad"),
        "kd": (2 * math.sqrt(120), 0.0, 100.0, "Nm s/rad"),
    },
}


def parse_parameters(values: list[str]) -> dict[str, float]:
    result = {}
    for value in values:
        name, separator, raw = value.partition("=")
        if not separator or name in result:
            raise ValueError("use unique --param name=value inputs")
        number = float(raw)
        if not math.isfinite(number):
            raise ValueError("parameters must be finite")
        result[name] = number
    return result


def resolve_parameters(
    identifier: str, supplied: dict[str, float], variant: float
) -> dict[str, float]:
    contract = PARAMETERS.get(identifier, {})
    if set(supplied) - set(contract):
        raise ValueError(
            f"{identifier}: supported named parameters: {', '.join(contract) or 'none'}"
        )
    if supplied and variant != 1.0:
        raise ValueError("use either named parameters or legacy --variant")
    values = {name: spec[0] for name, spec in contract.items()}
    if identifier == "core-01":
        values["timestep"] *= variant
    elif identifier == "core-fr3-02":
        values["kp"] *= variant
        values["kd"] = 2 * math.sqrt(values["kp"])
    values.update(supplied)
    for name, value in values.items():
        if not math.isfinite(value) or not contract[name][1] < value <= contract[name][2]:
            raise ValueError(
                f"{name}: expected ({contract[name][1]}, {contract[name][2]}] {contract[name][3]}"
            )
    return values
