"""Replay small synthetic Quest-style arm/hand poses through the offline command sink."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import replace
from pathlib import Path

import numpy as np

from pai_lab.local import write_json
from pai_lab.teleop import STALE_AFTER_NS, BimanualFrame, CommandSink
from pai_lab.teleop_sources import DeviceSample, InputMux

SESSION = "synthetic-xr-replay"
CALIBRATION = "synthetic-table-frame"
TICK_NS = 20_000_000
FINGERS = ("thumb", "index", "middle", "ring", "little")


def finger_nodes(
    wrist: tuple[float, float, float], side_sign: int, bends: tuple[float, ...]
) -> dict[str, list[tuple[float, float, float]]]:
    """Arrange the named finger links in a toy skeleton rooted at the wrist."""
    nodes = {}
    for index, (name, bend) in enumerate(zip(FINGERS, bends, strict=True)):
        x, y, z = wrist
        x += 0.043
        y += side_sign * (index - 2) * 0.013
        chain = [(x, y, z)]
        for link, length in enumerate((0.032, 0.022, 0.015), start=1):
            x += length * math.cos(link * bend)
            z -= length * math.sin(link * bend)
            chain.append((x, y, z))
        nodes[name] = chain
    return nodes


def synthesize_frame(sequence: int, *, pressed: bool, mode: str = "quest-only") -> BimanualFrame:
    """Use synthetic SI coordinates and bends, not a vendor SDK or capture format."""
    timestamp = sequence * TICK_NS
    identities = {"synthetic-local": np.eye(4)}
    mounts = dict.fromkeys(("left", "right"), np.eye(4))
    mux = InputMux(mode=mode, calibration_id=CALIBRATION, transforms=identities, mounts=mounts)
    samples = []
    skeletons = {}
    for side, sign in (("left", 1), ("right", -1)):
        shoulder = (0.0, sign * 0.22, 1.35)
        elbow = (0.18, sign * 0.26, 1.14)
        wrist = (0.36 + sequence * 0.008, sign * 0.24, 1.10)
        joints = tuple(0.12 + 0.025 * finger + sequence * 0.015 for finger in range(len(FINGERS)))
        pose = (*wrist, 0.0, 0.0, 0.0, 1.0)
        base = DeviceSample(
            "quest",
            side,
            timestamp,
            sequence,
            "synthetic-device",
            "synthetic-local",
            True,
            pose,
            FINGERS,
            joints,
        )
        skeletons[side] = {
            "shoulder_m": shoulder,
            "elbow_m": elbow,
            "wrist_m": wrist,
            "finger_nodes_m": finger_nodes(wrist, sign, joints),
        }
        if mode == "integrated":
            samples.extend(
                [
                    replace(base, source="vive", joint_names=(), joints=()),
                    replace(base, source="manus"),
                ]
            )
        else:
            samples.append(base)
    switches = {"receive_time_ns": timestamp, "clutch": pressed, "deadman": pressed}
    normalized = mux.combine(
        samples,
        quest_switches=switches,
        session=SESSION,
        sequence=sequence,
        now_ns=timestamp,
    )
    return replace(normalized, raw={**normalized.raw, "arm_skeletons": skeletons})


def replay_record() -> list[BimanualFrame]:
    frames = [synthesize_frame(index, pressed=index not in (0, 5)) for index in range(7)]
    # Round-trip the input format readers can examine in xr.json.
    serialized = json.dumps([frame.to_dict() for frame in frames], allow_nan=False)
    return [BimanualFrame.from_dict(raw) for raw in json.loads(serialized)]


def check_replay() -> dict:
    frames = replay_record()

    def new_sink() -> tuple[CommandSink, dict]:
        sink = CommandSink(CALIBRATION)
        early = sink.accept(frames[0], 0)
        armed = sink.rearm_local(0)
        moving = emit(sink, frames[1], TICK_NS)
        if early or not armed or moving["command_norm_m"] <= 0:
            raise RuntimeError("positive control did not reach a nonzero offline command")
        return sink, moving

    def emit(
        sink: CommandSink, frame: BimanualFrame, now_ns: int, *, poll_only: bool = False
    ) -> dict:
        # The demonstration sink exposes a boolean permission. The only output here
        # is a hypothetical translation vector written to an offline result file.
        permitted = sink.poll(now_ns) if poll_only else sink.accept(frame, now_ns)
        reference_x = frames[0].right.pose[0]
        requested = (round(frame.right.pose[0] - reference_x, 9), 0.0, 0.0)
        command = requested if permitted else (0.0, 0.0, 0.0)
        return {
            "permitted": permitted,
            "sink_reason": sink.reason if not permitted else "accepted",
            "sequence": frame.sequence,
            "input_age_ms": (now_ns - frame.receive_time_ns) / 1e6,
            "requested_delta_m": requested,
            "command_delta_m": command,
            "command_norm_m": math.hypot(*command),
        }

    fault_frame = frames[2]
    lost = replace(fault_frame, right=replace(fault_frame.right, tracked=False))
    clutch_released = replace(fault_frame, clutch=False)
    cases = {
        "tracking_loss": (lost, lost.receive_time_ns, False, "tracking-loss"),
        "stale_frame": (
            fault_frame,
            fault_frame.receive_time_ns + STALE_AFTER_NS,
            False,
            "stale",
        ),
        "stale_poll": (
            frames[1],
            frames[1].receive_time_ns + STALE_AFTER_NS,
            True,
            "stale",
        ),
        "clutch_released": (
            clutch_released,
            clutch_released.receive_time_ns,
            False,
            "switch-released",
        ),
    }
    results = {}
    for name, (frame, now_ns, poll_only, expected_reason) in cases.items():
        sink, moving = new_sink()
        blocked = emit(sink, frame, now_ns, poll_only=poll_only)
        # A current pressed sample alone must not clear the fault latch.
        after = align(frames[4], now_ns + TICK_NS)
        pressed_again = emit(sink, after, after.receive_time_ns)
        released = align(frames[5], after.receive_time_ns + TICK_NS)
        sink.accept(released, released.receive_time_ns)
        rearmed = sink.rearm_local(released.receive_time_ns)
        restarted = align(frames[6], released.receive_time_ns + TICK_NS)
        recovered = emit(sink, restarted, restarted.receive_time_ns)
        passed = (
            blocked["sink_reason"] == expected_reason
            and not blocked["permitted"]
            and blocked["requested_delta_m"][0] > 0.0
            and blocked["command_delta_m"] == (0.0, 0.0, 0.0)
            and pressed_again["command_delta_m"] == (0.0, 0.0, 0.0)
            and rearmed
            and recovered["command_norm_m"] > 0
        )
        results[name] = {
            "passed": passed,
            "moving": moving,
            "blocked": blocked,
            "pressed_again": pressed_again,
            "rearmed": rearmed,
            "recovered": recovered,
        }
    combined = synthesize_frame(1, pressed=True, mode="integrated")
    sources = {
        side: {"wrist": hand.pose_source, "fingers": hand.finger_source}
        for side, hand in (("left", combined.left), ("right", combined.right))
    }
    source_selection_passed = all(
        role == {"wrist": "vive", "fingers": "manus"} for role in sources.values()
    )
    return {
        "evidence": "synthetic-input-replay",
        "schema_version": 1,
        "stale_after_ms": STALE_AFTER_NS / 1e6,
        "frame_period_ms": TICK_NS / 1e6,
        "checks_passed": source_selection_passed
        and all(case["passed"] for case in results.values()),
        "cases": results,
        "integrated_sources": sources,
        "frames": [frame.to_dict() for frame in frames],
    }


def align(frame: BimanualFrame, timestamp: int) -> BimanualFrame:
    """Rebase a recovery sample to the scenario clock using its same fixed cadence."""
    raw = {
        **frame.raw,
        "devices": [{**sample, "receive_time_ns": timestamp} for sample in frame.raw["devices"]],
        "quest": {**frame.raw["quest"], "receive_time_ns": timestamp},
    }
    return replace(frame, receive_time_ns=timestamp, raw=raw)


def plot(result: dict, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = ["Track loss", "Old frame", "No new frame", "Clutch off"]
    phases = ("moving", "blocked", "pressed_again", "recovered")
    captions = ("Before fault", "Fault", "Press only", "After rearm")
    colors = ("#386fa4", "#b94c3c", "#b58123", "#287a64")
    fig, ax = plt.subplots(figsize=(8.3, 3.3), layout="constrained")
    cases = result["cases"]
    names = ("tracking_loss", "stale_frame", "stale_poll", "clutch_released")
    for i, (phase, caption, color) in enumerate(zip(phases, captions, colors, strict=True)):
        values = [cases[name][phase]["command_norm_m"] * 1000 for name in names]
        ax.bar(
            np.arange(len(names)) + (i - 1.5) * 0.18, values, width=0.16, label=caption, color=color
        )
        for x, value in enumerate(values):
            ax.annotate(
                f"{value:g}",
                (x + (i - 1.5) * 0.18, value),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color=color,
            )
    ax.set(
        xticks=np.arange(len(names)),
        xticklabels=labels,
        ylabel="Offline command norm (mm)",
        ylim=(0, 60),
    )
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = check_replay()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "xr.json", result)
    plot(result, args.output_dir / "xr.png")
    print(
        json.dumps({"output": str(args.output_dir / "xr.json"), "passed": result["checks_passed"]})
    )
    return 0 if result["checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
