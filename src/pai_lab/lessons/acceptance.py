"""Recompute key scientific checks from stored values, independently of pass flags."""

import json
from pathlib import Path
from typing import Any

import numpy as np


def measurement_errors(
    identifier: str, run_dir: Path, trace: np.ndarray, experiment: dict[str, Any]
) -> list[str]:
    payload = experiment["payload"]
    errors = []
    if identifier == "core-01":
        drift = float(np.max(np.abs(trace[:, 2] - trace[:, 1])))
        if drift >= 1e-5 or not np.isclose(drift, experiment["metric"], atol=1e-14, rtol=1e-8):
            errors.append("pendulum energy drift inconsistent or exceeds tolerance")
    if identifier == "core-fr3-04":
        jac = np.array(payload["analytic"])
        finite = np.array(payload["finite_difference"])
        if jac.shape != (3, 7) or finite.shape != jac.shape or np.max(np.abs(jac - finite)) >= 1e-6:
            errors.append("Jacobian finite-difference check failed")
        if payload["ik_errors_m"][-1] >= 0.001:
            errors.append("IK residual exceeds 1 mm")
    if (
        identifier == "core-fr3-03"
        and payload["final_error"] >= payload["without_compensation_error"]
    ):
        errors.append("gravity compensation does not reduce tracking error")
    if identifier == "core-enlight-02" and max(payload["fk_error_m"]) >= 1e-9:
        errors.append("Enlight independent FK comparison failed")
    if identifier in {"core-fr3-06", "core-wuji-02", "sim-enlight-02"} and np.max(trace[:, 2]) <= 0:
        errors.append("no measured contact force")
    if identifier in {"core-rl-01", "core-fr3-08", "core-il-01"}:
        weights = np.load(run_dir / "policy.npz")["weights"]
        if not np.isfinite(weights).all() or np.linalg.norm(weights) <= 1e-8:
            errors.append("empty or non-finite trained policy")
        if identifier != "core-il-01" and payload["parameter_delta"] <= 1e-8:
            errors.append("PPO parameters did not change")
        if identifier == "core-il-01" and payload["heldout_mse"] >= 0.1:
            errors.append("BC held-out loss exceeds tolerance")
    if identifier == "core-data-01":
        rows = [json.loads(line) for line in (run_dir / "episode.jsonl").read_text().splitlines()]
        if len(rows) != payload["transitions"] or len({row["episode"] for row in rows}) != 8:
            errors.append("dataset transition/episode count mismatch")
        if not all(
            np.isfinite(row["observation"] + row["action"] + row["next_observation"]).all()
            for row in rows
        ):
            errors.append("dataset contains non-finite state/action")
    if identifier == "sim-deploy-01":
        from pai_lab.lessons.deployment import validate_candidate

        errors += validate_candidate(run_dir / "sample_candidate")
    if identifier == "hw-common-01":
        data = json.loads((run_dir / "inference.json").read_text())
        if (
            not data["actions"]
            or data["actions"] != data["replay"]
            or payload["emitted_command_count"] != 0
        ):
            errors.append("offline inference/replay/sink check failed")
    return errors
