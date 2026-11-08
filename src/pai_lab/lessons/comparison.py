"""Compare genuine measured runs with matching target/frame/timing contracts."""

import json
from pathlib import Path

import numpy as np

from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.learning import previous_run


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    a = previous_run("core-fr3-09")
    b = previous_run("sim-fr3-01")
    first = json.loads((a / "experiment.json").read_text())["payload"]
    second = json.loads((b / "experiment.json").read_text())["payload"]
    for field in ("frame", "initial_q_rad", "tcp_targets_m", "control_dt_s"):
        if first.get(field) != second.get(field) or field not in first:
            raise ValueError(
                f"engine comparison requires matched {field}; rerun both with equal parameters"
            )
    errors_a = np.loadtxt(a / "trace.csv", delimiter=",", skiprows=1, ndmin=2)[:, 2]
    errors_b = np.asarray(second["tcp_errors_m"])
    if len(errors_a) != len(errors_b):
        raise ValueError("engine comparison sample mismatch")
    rows = [
        (i * 0.02, float(x), float(y))
        for i, (x, y) in enumerate(zip(errors_a, errors_b, strict=True))
    ]
    delta = float(np.sqrt(np.mean((errors_a - errors_b) ** 2)))
    return Experiment(
        rows,
        delta,
        {
            "engine_a": "MuJoCo",
            "engine_b": "PhysX",
            "tcp_error_difference_rmse_m": delta,
            "joint_errors_a_rad": first["joint_errors_rad"],
            "joint_errors_b_rad": second["joint_errors_rad"],
            "contacts_a_N": first["contact_force_norms_N"],
            "contacts_b_N": second["contact_force_norms_N"],
            "control_dt_s": first["control_dt_s"],
            "hardware_tolerance": False,
        },
        {"matched_real_runs": True, "finite": bool(np.isfinite(rows).all())},
    )
