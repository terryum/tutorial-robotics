"""Recompute key scientific checks from stored values, independently of pass flags."""

import json
from pathlib import Path
from typing import Any

import numpy as np


def pendulum_state_errors(
    run_dir: Path, trace: np.ndarray, experiment: dict[str, Any]
) -> list[str]:
    parameters = experiment["parameters"]
    payload = experiment["payload"]
    state = np.asarray(payload["state"], dtype=float)
    tips = np.asarray(payload["tip_positions_m"], dtype=float)
    pivot = np.asarray(payload["pivot_position_m"], dtype=float)
    gravity = np.asarray(payload["gravity_m_s2"], dtype=float)
    if (
        state.shape != (len(trace) + 1, 3)
        or tips.shape != state.shape
        or pivot.shape != (3,)
        or gravity.shape != (3,)
        or not all(np.isfinite(values).all() for values in (state, tips, pivot, gravity))
    ):
        return ["invalid pendulum replay coordinates"]

    times, angles, velocities = state.T
    timestep = parameters["timestep"]
    if (
        payload["dt_s"] != timestep
        or not np.allclose(times, np.arange(len(times)) * 10 * timestep, atol=1e-10, rtol=1e-9)
        or not np.array_equal(times[1:], trace[:, 0])
        or times[-1] != payload["observation_time_s"]
        or angles[0] != parameters["initial_angle_rad"]
        or angles[0] != payload["initial_angle_rad"]
        or velocities[0] != 0.0
        or velocities[0] != payload["initial_angular_velocity_rad_s"]
    ):
        return ["pendulum state disagrees with recorded experiment inputs or observation window"]

    offsets = tips - pivot
    if not (
        np.allclose(offsets[:, 0], -np.sin(angles), atol=1e-10)
        and np.allclose(offsets[:, 1], 0.0, atol=1e-10)
        and np.allclose(offsets[:, 2], -np.cos(angles), atol=1e-10)
    ):
        return ["pendulum site positions disagree with the one-meter hinge geometry"]

    with np.load(run_dir / "replay.npz", allow_pickle=False) as saved:
        if not (
            np.array_equal(saved["time_s"], times)
            and np.array_equal(saved["qpos"], angles[:, None])
            and np.array_equal(saved["qvel"], velocities[:, None])
        ):
            return ["pendulum replay disagrees with recorded state"]
    return []


def measurement_errors(
    identifier: str,
    run_dir: Path,
    trace: np.ndarray,
    experiment: dict[str, Any],
    *,
    legacy: bool = False,
) -> list[str]:
    payload = experiment["payload"]
    errors = []
    if identifier in {"core-fr3-09", "core-enlight-03"}:
        halfway = len(trace) // 2
        rmse = float(np.sqrt(np.mean(trace[halfway:, 2] ** 2)))
        if rmse >= 0.02 or not np.isclose(rmse, experiment["metric"]):
            errors.append("arm trajectory exceeds 20 mm or metric inconsistent")
        if len(payload["joint_names"]) != 7 or payload["frame"] != "world":
            errors.append("arm joint/frame contract mismatch")
    if identifier in {
        "core-fr3-10",
        "core-enlight-04",
        "core-enlight-05",
        "sim-fr3-02",
        "sim-fr3-03",
        "sim-enlight-04",
        "sim-enlight-05",
    }:
        evaluation = json.loads((run_dir / "evaluation.json").read_text())
        weights = np.load(run_dir / "policy.npz", allow_pickle=False)["weights"]
        if weights.shape != (18, 7) or not np.isfinite(weights).all():
            errors.append("invalid arm policy")
        successes = 0
        for episode in evaluation["episodes"]:
            hold, achieved = 0, False
            for distance in episode["errors_m"]:
                if not np.isfinite(distance) or distance < 0:
                    errors.append("invalid evaluation distance")
                hold = hold + 1 if distance <= 0.01 else 0
                achieved |= hold >= 10
            if achieved != episode["success"]:
                errors.append("reach success disagrees with consecutive hold")
            successes += achieved
        if (
            len(evaluation["episodes"]) != 20
            or successes != evaluation["successes"]
            or evaluation["performance_verified"] != (successes >= 16)
        ):
            errors.append("reach performance gate mismatch")
    if identifier == "core-01":
        drift = float(np.max(np.abs(trace[:, 2] - trace[:, 1])))
        if drift >= 1e-5 or not np.isclose(drift, experiment["metric"], atol=1e-14, rtol=1e-8):
            errors.append("pendulum energy drift inconsistent or exceeds tolerance")
        if not legacy:
            errors += pendulum_state_errors(run_dir, trace, experiment)
    if identifier == "core-02" and not legacy:
        from pai_lab.catalog import ROOT
        from pai_lab.lessons.physics import source_hash_comparison

        comparison = source_hash_comparison((ROOT / "assets/sources.json").read_bytes())
        if (
            payload["hash_comparison"] != comparison
            or json.loads((run_dir / "source-pins.json").read_text()) != payload
        ):
            errors.append("one-byte SHA-256 comparison disagrees with the public source manifest")
    if identifier == "core-03":
        inventory = json.loads((run_dir / "model-inventory.json").read_text())
        if inventory != payload or len(inventory) != len(trace):
            errors.append("model inventory disagrees with the recorded experiment")
        elif any(
            type(model[key]) is not int or model[key] < 0 or model[key] != model["source"][key]
            for model in inventory.values()
            for key in ("nq", "nv", "nu")
        ):
            errors.append("invalid MuJoCo configuration, velocity, or actuator counts")
    if identifier == "core-04" and not legacy:
        with np.load(run_dir / "replay.npz", allow_pickle=False) as saved:
            if (
                not np.array_equal(saved["time_s"], payload["time_s"])
                or not np.array_equal(saved["qpos"], payload["qpos"])
                or not np.array_equal(saved["qvel"], payload["qvel"])
                or not np.array_equal(saved["qpos"], trace[:, 2][None, :])
            ):
                errors.append("FR3 camera replay disagrees with the saved pose")
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
