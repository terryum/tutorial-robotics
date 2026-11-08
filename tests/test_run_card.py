import json
import time

import pytest

from pai_lab.hardware.preflight import preflight
from pai_lab.hardware.run_card import digest, execute


class MockTransport:
    def __init__(self, path, **overrides):
        self.path = path
        self.moves = []
        self.stops = 0
        self.failure = None
        self.state = {
            "model": "flexiv-enlight-l",
            "robot_identity": "fixture-only",
            "timestamp": time.time(),
            "stale_after_s": 1.0,
            "network_ok": True,
            "enabled": False,
            "error": False,
            "estop_ready": True,
            "command_authority_count": 0,
            "positions_rad": [0.0] * 7,
            "position_limits_rad": [[-1.0, 1.0]] * 7,
            "joint_group": "arm",
        }
        self.state.update(overrides)

    def snapshot(self):
        self.path.write_text(json.dumps(self.state))
        return self.path

    def move(self, positions_rad, *, timeout_s):
        if self.failure:
            raise self.failure
        self.moves.append(positions_rad)
        return True

    def stop(self):
        self.stops += 1


def card():
    now = time.time()
    return {
        "robot": "enlight",
        "model": "flexiv-enlight-l",
        "robot_identity": "fixture-only",
        "action": "small-joint-move",
        "joint_group": "arm",
        "units": "rad",
        "created_at": now,
        "expires_at": now + 30,
        "timeout_s": 0.1,
        "max_delta_rad": 0.01,
        "positions_rad": [0.005] * 7,
        "model_compatibility_reviewed": True,
        "tool_payload_reviewed": True,
        "stop_tested": True,
    }


def test_read_only_never_moves_and_single_use_card_stops(tmp_path):
    t = MockTransport(tmp_path / "state.json")
    assert preflight("enlight", t.snapshot(), read_only=True)["ready"]
    assert t.moves == []
    c = card()
    with pytest.raises(PermissionError):
        execute(c, "", t, tmp_path / "ledger")
    assert not t.moves
    execute(c, "APPROVE " + digest(c), t, tmp_path / "ledger")
    assert len(t.moves) == 1 and t.stops == 1
    with pytest.raises(FileExistsError):
        execute(c, "APPROVE " + digest(c), t, tmp_path / "ledger")
    assert len(t.moves) == 1 and t.stops == 2


@pytest.mark.parametrize(
    "change",
    [
        {"created_at": time.time() - 90, "expires_at": time.time() - 30},
        {"model": "wrong"},
        {"positions_rad": [0.5] * 7},
        {"positions_rad": [float("nan")] * 7},
        {"joint_group": "gripper"},
        {"timeout_s": float("inf")},
        {"stop_tested": False},
    ],
)
def test_card_rejects_invalid_action_before_motion(tmp_path, change):
    c = card()
    c.update(change)
    t = MockTransport(tmp_path / "state.json")
    with pytest.raises((ValueError, PermissionError)):
        execute(c, "APPROVE " + digest(c), t, tmp_path / "ledger")
    assert not t.moves


@pytest.mark.parametrize(
    "state",
    [
        {"positions_rad": [], "position_limits_rad": []},
        {"positions_rad": [float("nan")] * 7},
        {"timestamp": time.time() + 10},
        {"timestamp": float("nan")},
        {"timestamp": time.time() - 5},
        {"previous_timestamp": float("inf")},
        {"joint_group": "all"},
        {"enabled": None},
        {"error": None},
        {"network_ok": False},
        {"stale_after_s": float("inf")},
    ],
)
def test_preflight_fails_closed_and_card_never_moves(tmp_path, state):
    t = MockTransport(tmp_path / "state.json", **state)
    assert not preflight("enlight", t.snapshot(), read_only=True)["ready"]
    c = card()
    with pytest.raises(ValueError):
        execute(c, "APPROVE " + digest(c), t, tmp_path / "ledger")
    assert not t.moves and t.stops == 1


@pytest.mark.parametrize(
    "failure", [TimeoutError("mock timeout"), ConnectionError("mock disconnect")]
)
def test_transport_failure_consumes_card_and_stops(tmp_path, failure):
    t = MockTransport(tmp_path / "state.json")
    t.failure = failure
    c = card()
    with pytest.raises(type(failure)):
        execute(c, "APPROVE " + digest(c), t, tmp_path / "ledger")
    assert t.stops == 1
    t.failure = None
    with pytest.raises(FileExistsError):
        execute(c, "APPROVE " + digest(c), t, tmp_path / "ledger")
