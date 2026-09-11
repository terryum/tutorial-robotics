"""Read measured evidence and replay saved states without integrating dynamics."""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

from pai_lab.lessons.experiment import Experiment


def save_replay(output: Path, experiment: Experiment) -> None:
    if experiment.model is None:
        return
    import mujoco

    model, data, payload = experiment.model, experiment.data, experiment.payload
    mujoco.mj_saveModel(model, str(output / "replay.mjb"))
    qpos = np.asarray(payload.get("qpos", [data.qpos.tolist()]))
    qvel = np.asarray(payload.get("qvel", np.zeros((len(qpos), model.nv))))
    times = np.asarray(payload.get("time_s", np.arange(len(qpos)) * 0.02))
    if "state" in payload and model.nq == 1:
        values = np.asarray(payload["state"])
        times, qpos, qvel = values[:, 0], values[:, 1:2], values[:, 2:3]
    if qpos.ndim != 2 or qpos.shape[1] != model.nq or qvel.shape != (len(qpos), model.nv):
        raise ValueError("invalid replay state dimensions")
    np.savez_compressed(output / "replay.npz", time_s=times, qpos=qpos, qvel=qvel)
    if "control_rows" in payload:
        with (output / "control.csv").open("w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(
                [
                    "time_s",
                    "joint",
                    "target_rad",
                    "q_rad",
                    "velocity_rad_s",
                    "requested_nm",
                    "applied_nm",
                ]
            )
            writer.writerows(payload.pop("control_rows"))


def inspect_run(identifier: str, run_dir: Path) -> dict[str, Any]:
    from pai_lab.lessons.evidence import validate_run

    errors = validate_run(identifier, run_dir)
    if errors:
        raise ValueError("; ".join(errors))
    summary = json.loads((run_dir / "summary.json").read_text())
    experiment = json.loads((run_dir / "experiment.json").read_text())
    values = np.loadtxt(run_dir / "trace.csv", delimiter=",", skiprows=1, ndmin=2)
    return {
        "lesson": summary["lesson_id"],
        "metric": summary["metric_name"],
        "value": summary["metric_value"],
        "units": summary["units"],
        "parameters": experiment.get("parameters", {}),
        "checks": experiment["checks"],
        "observed_first": float(values[0, 2]),
        "observed_last": float(values[-1, 2]),
        "observed_range": [float(values[:, 2].min()), float(values[:, 2].max())],
        "files": sorted(p.name for p in run_dir.iterdir()),
        "completion": "execution only",
    }


def compare_runs(
    identifier: str, baseline: Path, comparison: Path, output: Path | None = None
) -> dict[str, Any]:
    from pai_lab.lessons.evidence import comparison_errors

    errors = comparison_errors(identifier, baseline, comparison)
    if errors:
        raise ValueError("; ".join(errors))
    a, b = inspect_run(identifier, baseline), inspect_run(identifier, comparison)
    report = {
        "lesson": a["lesson"],
        "baseline": a,
        "comparison": b,
        "metric_delta": b["value"] - a["value"],
        "unchanged": b["value"] == a["value"],
    }
    if output is not None:
        if output.exists() and any(output.iterdir()):
            raise ValueError("comparison output must be empty; preserve earlier evidence")
        output.mkdir(parents=True, exist_ok=True)
        import matplotlib

        matplotlib.use("Agg")
        from matplotlib import pyplot as plt

        fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
        for path, label in ((baseline, "baseline"), (comparison, "comparison")):
            values = np.loadtxt(path / "trace.csv", delimiter=",", skiprows=1, ndmin=2)
            ax.plot(values[:, 0], values[:, 2], label=label)
        header = (baseline / "trace.csv").read_text().splitlines()[0].split(",")[0]
        ax.set(xlabel=header, ylabel=f"{a['metric']} ({a['units']})")
        ax.legend()
        ax.grid(alpha=0.25)
        fig.savefig(output / "comparison.png", dpi=120)
        plt.close(fig)
        (output / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def replay(run_dir: Path, *, offscreen: Path | None = None, speed: float = 1.0) -> None:
    import mujoco

    from pai_lab.lessons.experiment import render

    if not np.isfinite(speed) or speed <= 0:
        raise ValueError("replay speed must be finite and positive")
    if not (run_dir / "replay.mjb").is_file():
        raise ValueError(
            "this run has no saved model state; inspect its plot and semantic artifact"
        )
    model = mujoco.MjModel.from_binary_path(str(run_dir / "replay.mjb"))
    data = mujoco.MjData(model)
    experiment = json.loads((run_dir / "experiment.json").read_text())
    azimuth = float(experiment.get("parameters", {}).get("camera_azimuth", 135.0))
    with np.load(run_dir / "replay.npz", allow_pickle=False) as saved:
        qpos, qvel, times = saved["qpos"], saved["qvel"], saved["time_s"]
    if (
        qpos.shape != (len(times), model.nq)
        or qvel.shape != (len(times), model.nv)
        or not all(np.isfinite(v).all() for v in (qpos, qvel, times))
        or len(times) == 0
    ):
        raise ValueError("invalid recorded state")

    def frame(index: int) -> None:
        data.qpos[:], data.qvel[:], data.time = qpos[index], qvel[index], times[index]
        mujoco.mj_forward(model, data)

    if offscreen is not None:
        if offscreen.exists():
            raise ValueError("choose a new image path")
        frame(len(times) - 1)
        offscreen.parent.mkdir(parents=True, exist_ok=True)
        render(offscreen, model, data, azimuth=azimuth)
        return
    if sys.platform == "darwin" and not __import__("os").environ.get("MJPYTHON_BIN"):
        # mjpython configures this launcher variable in current MuJoCo releases.
        if "mjpython" not in sys.executable.lower():
            raise RuntimeError(
                "macOS replay: mjpython -m pai_lab.cli lesson view ID --run-dir PATH"
            )
    import mujoco.viewer

    frame(0)
    with mujoco.viewer.launch_passive(model, data) as viewer:
        viewer.cam.azimuth = azimuth
        for index in range(len(times)):
            if not viewer.is_running():
                break
            with viewer.lock():
                frame(index)
            viewer.sync()
            if index + 1 < len(times):
                time.sleep(min(max(float(times[index + 1] - times[index]) / speed, 0), 1))
