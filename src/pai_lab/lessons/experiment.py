"""Measured results passed from an experiment to the recording layer."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np


@dataclass
class Experiment:
    rows: list[tuple[float, float, float]]
    metric: float
    payload: dict[str, Any]
    checks: dict[str, bool]
    model: Any = None
    data: Any = None
    files: list[str] = field(default_factory=list)


def plot_trace(
    path: Path, rows: list[tuple[float, float, float]], units: str, xlabel: str = "Time (s)"
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    values = np.asarray(rows)
    fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
    ax.plot(values[:, 0], values[:, 1], label="reference")
    ax.plot(values[:, 0], values[:, 2], label="measured")
    ax.set(xlabel=xlabel, ylabel=units)
    ax.grid(alpha=0.25)
    ax.legend()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def render(path: Path, model: Any, data: Any) -> dict[str, Any]:
    import mujoco
    from PIL import Image

    camera = mujoco.MjvCamera()
    mujoco.mjv_defaultFreeCamera(model, camera)
    camera.azimuth, camera.elevation = 135, -25
    camera.distance = max(float(model.stat.extent) * 1.6, 0.35)
    with mujoco.Renderer(model, height=360, width=480) as renderer:
        renderer.update_scene(data, camera=camera)
        pixels = renderer.render().copy()
    Image.fromarray(pixels).save(path)
    return {"shape": list(pixels.shape), "std": float(pixels.std()), "renderer": "MuJoCo"}
