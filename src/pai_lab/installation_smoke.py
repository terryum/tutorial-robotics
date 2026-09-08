"""Deterministic MuJoCo installation check; not tutorial completion.

SI units: s, rad, rad/s, N m. Right-handed world, +Z up, hinge about +Y.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mujoco
import numpy as np

XML = """
<mujoco model="installation_pendulum">
  <option timestep="0.002" gravity="0 0 -9.81"/>
  <worldbody>
    <light pos="0 -2 3"/>
    <geom type="plane" size="2 2 .1" rgba=".8 .8 .8 1"/>
    <body pos="0 0 1.5">
      <joint name="hinge" axis="0 1 0" damping=".05" range="-120 120"/>
      <geom type="capsule" fromto="0 0 0 0 0 -.8" size=".06" mass="1" rgba=".1 .4 .9 1"/>
    </body>
  </worldbody>
  <actuator><motor joint="hinge" ctrllimited="true" ctrlrange="-2 2"/></actuator>
</mujoco>
"""


def simulate(
    seed: int, timestep: float, torque: float = 0.0
) -> tuple[mujoco.MjModel, mujoco.MjData, np.ndarray]:
    if not np.isfinite(timestep) or timestep <= 0:
        raise ValueError("timestep must be positive and finite")
    if not np.isfinite(torque) or abs(torque) > 2:
        raise ValueError("torque must be finite and within [-2, 2] N m")
    model = mujoco.MjModel.from_xml_string(XML)
    model.opt.timestep = timestep
    data = mujoco.MjData(model)
    data.qpos[0] = np.random.default_rng(seed).uniform(0.7, 0.9)
    data.ctrl[0] = torque
    mujoco.mj_forward(model, data)
    rows = []
    for _ in range(round(2.0 / timestep)):
        mujoco.mj_step(model, data)
        rows.append((data.time, data.qpos[0], data.qvel[0], data.ctrl[0]))
    values = np.asarray(rows)
    if not np.isfinite(values).all():
        raise AssertionError("nonfinite simulation state")
    return model, data, values


def render(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    destination: Path,
    *,
    lookat: tuple[float, float, float] = (0.0, 0.0, 0.8),
    distance: float = 3.0,
) -> None:
    from PIL import Image

    camera = mujoco.MjvCamera()
    camera.lookat[:] = lookat
    camera.distance = distance
    camera.azimuth = 135
    camera.elevation = -20
    with mujoco.Renderer(model, height=480, width=640) as renderer:
        renderer.update_scene(data, camera=camera)
        pixels = renderer.render()
        if float(pixels.std()) < 5:
            raise AssertionError("render is blank")
        Image.fromarray(pixels).save(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--headless", action="store_true", help="Offscreen rendering (default)."
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    model, data, baseline = simulate(args.seed, 0.002)
    _, _, repeated = simulate(args.seed, 0.002)
    _, _, finer = simulate(args.seed, 0.001)
    _, _, driven = simulate(args.seed, 0.002, torque=0.5)
    np.testing.assert_array_equal(baseline, repeated)
    delta = float(np.max(np.abs(baseline[:, 1] - finer[1::2, 1])))
    if delta >= 0.02 or np.allclose(baseline[:, 1], driven[:, 1]):
        raise AssertionError("timestep convergence or motor response failed")
    rejected = 0
    for timestep, torque in [(0.0, 0.0), (0.002, float("nan")), (0.002, 3.0)]:
        try:
            simulate(args.seed, timestep, torque)
        except ValueError:
            rejected += 1
    assert rejected == 3
    np.savetxt(
        args.output_dir / "pendulum.csv",
        baseline,
        delimiter=",",
        header="time_s,angle_rad,velocity_rad_s,torque_nm",
        comments="",
    )
    render(model, data, args.output_dir / "pendulum.png")
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    figure, ax = plt.subplots(figsize=(8, 4))
    for label, values in [
        ("dt=2 ms", baseline),
        ("dt=1 ms", finer),
        ("torque=0.5 N m", driven),
    ]:
        ax.plot(values[:, 0], values[:, 1], label=label)
    ax.set(xlabel="Time [s]", ylabel="Hinge angle [rad]")
    ax.legend()
    figure.tight_layout()
    figure.savefig(args.output_dir / "comparison.png")
    plt.close(figure)
    summary = {
        "mujoco": mujoco.__version__,
        "seed": args.seed,
        "samples": len(baseline),
        "repeat_max_abs_error": float(np.max(np.abs(baseline - repeated))),
        "timestep_angle_max_abs_error_rad": delta,
        "invalid_inputs_rejected": rejected,
        "final_time_s": float(data.time),
        "finite": True,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
