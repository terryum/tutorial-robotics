from __future__ import annotations

import copy
import hashlib
import socket
import subprocess
import sys

import pytest

from pai_lab.manual_examples import DEVICES, ROOT, check, fixture, g1_ids, inspect_hands


@pytest.mark.parametrize("device", DEVICES)
def test_reordering_and_contract_failures(device):
    expected = fixture(device)
    packet = copy.deepcopy(expected)
    packet["joints"].reverse()
    result = check(packet, expected)
    assert result["ordered_positions"] == [j["position"] for j in expected["joints"]]
    assert not result["hardware_evidence"]
    for field, bad in [
        ("position_unit", "deg"),
        ("effort_unit", "unknown"),
        ("model_revision", "wrong"),
        ("sdk_revision", "wrong"),
        ("frame_id", "wrong"),
        ("received_at_s", 9.0),
        ("received_at_s", float("nan")),
        ("received_at_s", 11.0),
    ]:
        packet = copy.deepcopy(expected)
        packet[field] = bad
        with pytest.raises(ValueError):
            check(packet, expected)
    for operation in ["missing", "duplicate", "unknown", "nan"]:
        packet = copy.deepcopy(expected)
        if operation == "missing":
            packet["joints"].pop()
        elif operation == "duplicate":
            packet["joints"].append(packet["joints"][0])
        elif operation == "unknown":
            packet["joints"][0]["nid"] = 999
        else:
            packet["joints"][0]["position"] = float("nan")
        with pytest.raises(ValueError):
            check(packet, expected)


def test_wuji_missing_id_never_shifted_or_filled_with_zero():
    expected = fixture("wuji")
    packet = copy.deepcopy(expected)
    packet["joints"] = list(reversed(packet["joints"][1:]))
    result = check(packet, expected, allow_partial=True)
    assert not result["complete"]
    assert result["missing_ids"] == [0]
    assert result["ordered_positions"][:3] == [None, 0.01, 0.02]
    assert result["effort_unit"] == "A"
    assert packet["tactile"] == expected["tactile"]


@pytest.mark.parametrize(
    "key,bad",
    [
        ("point_unit", "N"),
        ("aggregate_unit", "normalized"),
        ("format_version", 2),
        ("digest", "wrong"),
        ("temperature_unit", "K"),
        ("positions", []),
    ],
)
def test_wuji_metadata_rejected(key, bad):
    expected = fixture("wuji")
    packet = copy.deepcopy(expected)
    packet["tactile"][key] = bad
    with pytest.raises(ValueError):
        check(packet, expected)


@pytest.mark.parametrize(
    "dof,locked,count", [(23, True, 23), (23, False, 23), (29, True, 27), (29, False, 29)]
)
def test_g1_array_slots(dof, locked, count):
    expected = fixture("g1", dof=dof, waist_locked=locked)
    assert len(g1_ids(dof, locked)) == count
    assert check(expected, expected)["complete"]
    packet = copy.deepcopy(expected)
    packet["motor_state"] = list(reversed(packet["motor_state"]))
    with pytest.raises(ValueError):
        check(packet, expected)
    packet = copy.deepcopy(expected)
    packet["waist_locked"] = not locked
    with pytest.raises(ValueError):
        check(packet, expected)


@pytest.mark.parametrize("device", ["enlight", "fr3"])
def test_arm_arrays_units_and_pose(device):
    expected = fixture(device)
    for field, bad in [
        ("parent", "unknown"),
        ("translation_unit", "mm"),
        ("quaternion", [0.0] * 4),
    ]:
        packet = copy.deepcopy(expected)
        packet["pose"][field] = bad
        with pytest.raises(ValueError):
            check(packet, expected)
    packet = copy.deepcopy(expected)
    packet["sdk_state"]["q"].reverse()
    with pytest.raises(ValueError):
        check(packet, expected)


@pytest.mark.parametrize(
    "fault",
    ["dimension", "row-count", "camera-time", "camera-missing", "version", "gripper", "time-order"],
)
def test_episode_failures(fault):
    expected = fixture("aloha")
    packet = copy.deepcopy(expected)
    e = packet["episode"]
    if fault == "dimension":
        e["qpos"][0].pop()
    elif fault == "row-count":
        e["action"].pop()
    elif fault == "camera-time":
        e["cameras"]["cam_high"][0] -= 0.1
    elif fault == "camera-missing":
        del e["cameras"]["cam_high"]
    elif fault == "version":
        e["format"] = "hdf5-assumed"
    elif fault == "gripper":
        e["action"][0][6] = 2
    else:
        e["timestamp_s"].reverse()
    with pytest.raises(ValueError):
        check(packet, expected)


def test_example_does_not_connect_or_write_state(monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        raise AssertionError("Network not permitted")

    monkeypatch.setattr(socket, "socket", forbidden)
    for device in DEVICES:
        expected = fixture(device)
        check(expected, expected)
    local = ROOT / ".local"
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in local.glob("*.json")}
    result = subprocess.run(
        [sys.executable, "-m", "pai_lab.manual_examples", "all"],
        cwd=tmp_path,
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert list(tmp_path.iterdir()) == []
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in local.glob("*.json")}
    assert after == before


def test_pinned_hand_inventory_when_available():
    if not (ROOT / ".cache/assets/mujoco-menagerie/sharpa_wave/scene_left.xml").exists():
        pytest.skip("Optional pinned vendor cache unavailable")
    result = inspect_hands()
    assert not result["sdk_axis_mapping_verified"]
    assert len(result["models"]["sharpa"][0]["joints"]) == 22
    assert len(result["models"]["wuji"][1]["joints"]) == 20
