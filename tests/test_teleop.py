import json
import socket
import struct
from dataclasses import replace

import numpy as np
import pytest

from pai_lab.lessons.teleop import sample
from pai_lab.teleop import BimanualFrame, CommandSink, transform_pose
from pai_lab.teleop_recording import Episode, replay, split_episodes
from pai_lab.teleop_sources import DeviceSample, InputMux
from pai_lab.vive_ipc import HEADER, POSE, HubClient, HubDecoder


def armed():
    gate = CommandSink("synthetic-calibration")
    gate.accept(sample(0, 0, pressed=False), 0)
    assert gate.rearm_local(0)
    assert gate.accept(sample(1, 1), 1)
    return gate


def test_watchdog_exact_expiry_reconnect_and_local_rearm():
    gate = armed()
    assert gate.poll(100_000_000)
    assert not gate.poll(100_000_001)
    assert not gate.accept(sample(2, 100_000_002), 100_000_002)
    assert not gate.rearm_local(100_000_002)
    gate.accept(sample(3, 100_000_003, pressed=False), 100_000_003)
    assert gate.rearm_local(100_000_003)
    assert gate.accept(sample(4, 100_000_004), 100_000_004)
    assert not gate.accept(replace(sample(0, 100_000_005), session="new"), 100_000_005)


@pytest.mark.parametrize(
    "change",
    [
        {"units": "mm"},
        {"quaternion_order": "wxyz"},
        {"calibration_id": "wrong"},
        {"sequence": 0},
        {"receive_time_ns": -1},
        {"left": replace(sample(2, 2).left, side="right")},
        {"left": replace(sample(2, 2).left, tracked=False)},
        {"left": replace(sample(2, 2).left, pose=(float("nan"), 0, 0, 0, 0, 0, 1))},
        {"left": replace(sample(2, 2).left, pose=(0, 0, 0, 0, 0, 0, 0))},
    ],
)
def test_bad_input_latches_hold(change):
    gate = armed()
    assert not gate.accept(replace(sample(2, 2), **change), 2)
    assert not gate.accept(sample(3, 3), 3)


def test_contract_roundtrip_and_transform():
    frame = sample(1, 1)
    assert BimanualFrame.from_dict(json.loads(json.dumps(frame.to_dict()))) == frame
    world = np.eye(4)
    world[:3, 3] = [1, 0, 0]
    mount = np.eye(4)
    mount[:3, 3] = [0, 0.1, 0]
    assert np.allclose(transform_pose(frame.left.pose, world, mount), [1.3, 0.3, 0.5, 0, 0, 0, 1])
    world[0, 0] = -1
    with pytest.raises(ValueError):
        transform_pose(frame.left.pose, world, mount)


def test_explicit_source_selection_and_stale_fingers():
    samples = [
        DeviceSample(
            src,
            side,
            1,
            9,
            "device",
            "device-space",
            True,
            sample(1, 1).left.pose,
            ("index",),
            (0.1,),
        )
        for src in ("quest", "vive", "manus")
        for side in ("left", "right")
    ]
    mux = InputMux(
        mode="integrated",
        calibration_id="cal",
        transforms={"device-space": np.eye(4)},
        mounts={s: np.eye(4) for s in ("left", "right")},
    )
    kwargs = {
        "quest_switches": {"receive_time_ns": 1, "clutch": True, "deadman": True},
        "session": "s",
        "sequence": 1,
        "now_ns": 1,
    }
    frame = mux.combine(samples, **kwargs)
    assert frame.left.pose_source == "vive" and frame.right.finger_source == "manus"
    with pytest.raises(ValueError):
        mux.combine(samples, **(kwargs | {"now_ns": 100_000_001}))


def test_episode_no_overwrite_corruption_and_lifecycle(tmp_path):
    paths = []
    for i in range(3):
        ep = Episode(tmp_path, str(i), provenance="synthetic")
        ep.append(
            sample(1, 1),
            target={"q": 0.1},
            state={"q": 0},
            state_time_ns=1,
            cameras={"sim": {"time_ns": 1, "data": [[[1, 2, 3]]]}},
        )
        ep.finish()
        paths.append(ep.path)
        assert replay(ep.path)[0]["target"]["q"] == 0.1
        with pytest.raises(FileExistsError):
            Episode(tmp_path, str(i), provenance="synthetic")
    assert {k: len(v) for k, v in split_episodes(paths).items()} == {
        "train": 1,
        "validation": 1,
        "test": 1,
    }
    (paths[0] / "frames.jsonl").write_text("corrupt")
    with pytest.raises(ValueError):
        replay(paths[0])
    for status in ("discarded", "aborted"):
        ep = Episode(tmp_path, status, provenance="synthetic")
        ep.finish(status)
        with pytest.raises(ValueError):
            replay(ep.path)


def packet(kind, payload, request=0):
    return HEADER.pack(kind, 1, 0, request, len(payload)) + payload


def test_hub_fragmented_packets_and_status_gate():
    decoder = HubDecoder()
    ack = packet(2, struct.pack("<HHIQ", 1, 0, 42, 0), 1)
    status = packet(0x31, struct.pack("<IIIIQ", 1, 2, 0, 0, 1))
    pose = packet(
        0x30, POSE.pack(1, 0, 1, *([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0] + [0.0] * 6), b"synthetic")
    )
    events = []
    for byte in ack + status + pose:
        events.extend(decoder.feed(bytes([byte])))
    assert events[-1]["tracked"] and events[-1]["pose"][-1] == 1
    with pytest.raises(ValueError):
        HubDecoder().feed(packet(0x30, pose))
    with pytest.raises(ValueError):
        HubDecoder().feed(HEADER.pack(2, 1, 0, 0, 65537))


def test_partial_receive_and_server_stop_do_not_block_watchdog():
    a, b = socket.socketpair()
    client = HubClient(a)
    gate = armed()
    b.send(b"\x02")
    ticks = []

    def watchdog():
        ticks.append(1)
        gate.poll(100_000_001)

    assert client.poll(watchdog) == []
    assert not gate.armed and len(ticks) == 2
    b.close()
    assert client.poll(watchdog) == [{"kind": "disconnected"}]
    assert client.closed


@pytest.mark.parametrize("identifier", ["core-teleop-01", "sim-teleop-02", "sim-enlight-06"])
def test_synthetic_lessons_numeric_artifacts(identifier, tmp_path, monkeypatch):
    # Development integration bypasses learner prerequisite history only. This
    # executes synthetic, command-free lessons and never records a completion.
    from pai_lab.lessons import runner
    from pai_lab.lessons.evidence import validate_run

    monkeypatch.setattr(runner, "gaps", lambda lesson: [])
    output = tmp_path / identifier
    result = runner.run_lesson(identifier, output_dir=output, samples=8)
    assert validate_run(identifier, output) == []
    assert result.status == "executed"
    assert len(list((output / "episodes").glob("episode-*"))) == 3


def test_external_demonstrations_model_dimensions_and_episode_leakage(tmp_path):
    from pai_lab.teleop_learning import load_demonstrations

    rows = [
        {"episode": i, "split": split, "observation": [0.0] * 17, "action": [0.0] * 7}
        for i, split in enumerate(("train", "validation", "test"))
    ]
    path = tmp_path / "data.json"
    payload = {"schema_version": 1, "model": "enlight", "rows": rows}
    path.write_text(json.dumps(payload))
    assert len(load_demonstrations(path, "enlight")) == 3
    with pytest.raises(ValueError):
        load_demonstrations(path, "fr3")
    payload["rows"][1]["episode"] = 0
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError):
        load_demonstrations(path, "enlight")
