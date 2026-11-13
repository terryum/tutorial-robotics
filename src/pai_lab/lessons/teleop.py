"""Synthetic input teaching path, independent of live VR capabilities."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from pai_lab.lessons.experiment import Experiment
from pai_lab.teleop import BimanualFrame, CommandSink, HandInput
from pai_lab.teleop_recording import Episode, replay, split_episodes


def sample(sequence: int, timestamp: int, *, pressed: bool = True) -> BimanualFrame:
    hands = [
        HandInput(
            side,
            (0.3, y, 0.5, 0.0, 0.0, 0.0, 1.0),
            ("index_flexion",),
            (0.2,),
            True,
            "synthetic",
            "synthetic",
        )
        for side, y in (("left", 0.2), ("right", -0.2))
    ]
    return BimanualFrame(
        sequence,
        "synthetic-session",
        timestamp,
        "synthetic-calibration",
        hands[0],
        hands[1],
        {
            "source": "synthetic",
            "device_time": timestamp,
            "device_clock": "synthetic",
            "frame_id": "world",
        },
        pressed,
        pressed,
    )


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    del seed
    if identifier == "sim-enlight-06":
        return collect_enlight(output, samples, variant)
    if identifier == "sim-teleop-01":
        raise FileNotFoundError(
            "capability-unavailable: live Quest/MANUS/VIVE and calibration required"
        )
    gate = CommandSink("synthetic-calibration")
    rows = []
    for episode_id in range(3):
        episode = Episode(output / "episodes", f"episode-{episode_id}", provenance="synthetic")
        start = (episode_id + 1) * (samples + 20) * 10_000_000
        release = sample(episode_id * (samples + 1), start, pressed=False)
        if identifier == "sim-teleop-02":
            release = integrated_frame(release)
        gate.accept(release, start)
        assert gate.rearm_local(start)
        for step in range(samples):
            now = start + (step + 1) * 10_000_000
            frame = sample(episode_id * (samples + 1) + step + 1, now)
            frame = replace(
                frame,
                left=replace(
                    frame.left, pose=(0.3 + step * 0.0001 * variant,) + frame.left.pose[1:]
                ),
            )
            if identifier == "sim-teleop-02":
                frame = integrated_frame(frame)
            accepted = gate.accept(frame, now)
            target = {"preview_x": frame.left.pose[0]}
            episode.append(
                frame,
                target=target,
                state=target,
                cameras={"synthetic": {"time_ns": now, "data": [[[step % 255, 0, 0]]]}},
                state_time_ns=now,
            )
            rows.append((now / 1e9, 1.0, float(accepted)))
        episode.finish()
        assert len(replay(episode.path)) == samples
        assert not gate.poll(now + 100_000_000)
    for status in ("discarded", "aborted"):
        episode = Episode(output / "episodes", status, provenance="synthetic")
        episode.finish(status)
    splits = split_episodes(sorted((output / "episodes").glob("episode-*")))
    payload: dict[str, Any] = {
        "schema_version": 2,
        "provenance": "synthetic",
        "saved_episodes": 3,
        "discarded_episodes": 1,
        "aborted_episodes": 1,
        "splits": {k: [p.name for p in v] for k, v in splits.items()},
        "command_publishers": 0,
        "live_input_verified": False,
        "watchdog_ns": 100_000_000,
    }
    return Experiment(
        rows,
        float(sum(r[2] for r in rows)),
        payload,
        {"three_reloaded_episodes": True, "timeout_hold": not gate.poll(now + 100_000_001)},
    )


def collect_enlight(output: Path, samples: int, variant: float) -> Experiment:
    import mujoco
    import numpy as np
    from scipy.spatial.transform import Rotation

    from pai_lab.lessons.arm import Arm
    from pai_lab.local import write_json
    from pai_lab.teleop_enlight import wrist_target

    arm = Arm("enlight", output)
    gate = CommandSink("synthetic-calibration")
    rows = []
    demonstrations = []
    for ep in range(3):
        arm.reset()
        start = (ep + 1) * (samples + 20) * 20_000_000
        gate.accept(sample(ep * (samples + 1), start, pressed=False), start)
        assert gate.rearm_local(start)
        episode = Episode(
            output / "episodes", f"episode-{ep}", provenance="synthetic-mujoco-enlight-arm"
        )
        origin = arm.tcp()
        orientation = tuple(
            Rotation.from_matrix(arm.data.site_xmat[arm.site].reshape(3, 3)).as_quat()
        )
        for step in range(samples):
            now = start + (step + 1) * 20_000_000
            frame = sample(ep * (samples + 1) + step + 1, now)
            desired = origin + [0.005 * np.sin(step / samples * np.pi) * variant, 0, 0]
            frame = replace(frame, left=replace(frame.left, pose=tuple(desired) + orientation))
            if not gate.accept(frame, now):
                raise ValueError("command sink rejected input")
            arm.target = desired
            observation = arm.observation().tolist()
            target_values = wrist_target(arm, frame.left.pose)
            action = np.arctanh(
                np.clip((target_values - arm.data.qpos[arm.qadr]) / 0.03, -0.999, 0.999)
            )
            with mujoco.Renderer(arm.model, height=64, width=64) as renderer:
                renderer.update_scene(arm.data)
                image = renderer.render().tolist()
            names = [f"joint{i}" for i in range(1, 8)]
            state = dict(zip(names, arm.data.qpos[arm.qadr].tolist()))
            target = dict(zip(names, target_values.tolist()))
            arm.step(action)
            episode.append(
                frame,
                target=target,
                state=state,
                cameras={"sim": {"time_ns": now, "data": image}},
                state_time_ns=now,
            )
            demonstrations.append(
                {
                    "episode": ep,
                    "split": ("train", "validation", "test")[ep],
                    "observation": observation,
                    "action": action.tolist(),
                }
            )
            rows.append((now / 1e9, float(desired[0]), float(arm.tcp()[0])))
        episode.finish()
        replay(episode.path)
    for status in ("discarded", "aborted"):
        Episode(output / "episodes", status, provenance="synthetic-mujoco-enlight-arm").finish(
            status
        )
    write_json(
        output / "collected-demonstrations.json",
        {
            "schema_version": 1,
            "model": "enlight",
            "provenance": "synthetic",
            "rows": demonstrations,
        },
    )
    return Experiment(
        rows,
        float(max(abs(r[1] - r[2]) for r in rows)),
        {
            "provenance": "synthetic-mujoco-enlight-arm",
            "saved_episodes": 3,
            "human_demonstration": False,
            "gripper_verified": False,
            "orientation_control": True,
            "command_publishers": 0,
        },
        {"finite_states": bool(np.isfinite(rows).all()), "three_reloads": True},
        arm.model,
        arm.data,
    )


def integrated_frame(frame: BimanualFrame) -> BimanualFrame:
    import numpy as np

    from pai_lab.teleop_sources import DeviceSample, InputMux

    world = np.eye(4)
    world[:3, 3] = [0.05, 0, 0]
    mux = InputMux(
        mode="integrated",
        calibration_id=frame.calibration_id,
        transforms={"synthetic-space": world},
        mounts={side: np.eye(4) for side in ("left", "right")},
    )
    devices = [
        DeviceSample(
            src,
            side,
            frame.receive_time_ns,
            frame.receive_time_ns,
            "synthetic",
            "synthetic-space",
            True,
            getattr(frame, side).pose,
            ("index_flexion",),
            (0.2,),
        )
        for src in ("vive", "manus")
        for side in ("left", "right")
    ]
    return mux.combine(
        devices,
        quest_switches={
            "receive_time_ns": frame.receive_time_ns,
            "clutch": frame.clutch,
            "deadman": frame.deadman,
        },
        session=frame.session,
        sequence=frame.sequence,
        now_ns=frame.receive_time_ns,
    )
