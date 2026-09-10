import json
import time

from pai_lab.hardware.preflight import preflight


def _snapshot(**overrides):
    value = {
        "model": "wujihand2-beta2-right",
        "voltage_v": 12.0,
        "firmware": "v2.6.0",
        "sdk": "v2026.8.31",
        "network_ok": True,
        "enabled": False,
        "error": False,
        "estop_ready": True,
        "get_rate_hz": 100,
        "publish_rate_hz": 1000,
        "timestamp": time.time(),
        "stale_after_s": 1.0,
        "command_authority_count": 0,
        "positions_rad": [0.0, 0.2],
        "position_limits_rad": [[-1.0, 1.0], [-1.0, 1.0]],
        "serial": "must-not-be-copied",
    }
    value.update(overrides)
    return value


def test_wuji_preflight_is_read_only_and_sanitized(tmp_path) -> None:
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(_snapshot()), encoding="utf-8")
    result = preflight("wuji", path, read_only=True)
    assert result["ready"] is True
    assert result["serial_stored"] is False
    assert "serial" not in result


def test_wuji_preflight_rejects_wrong_model_limits_fault_and_stale_state(tmp_path) -> None:
    path = tmp_path / "snapshot.json"
    path.write_text(
        json.dumps(
            _snapshot(
                model="wujihand2-beta1-right",
                voltage_v=14.0,
                enabled=True,
                error=True,
                estop_ready=False,
                get_rate_hz=101,
                publish_rate_hz=1001,
                timestamp=0,
            )
        ),
        encoding="utf-8",
    )
    result = preflight("wuji", path, read_only=True)
    assert result["ready"] is False
    assert {
        "wrong-model: expected wuji",
        "power-out-of-range",
        "device-must-be-disabled",
        "device-error",
        "estop-not-ready",
        "get-rate-limit",
        "publish-rate-limit",
        "stale-state",
    } <= set(result["errors"])


def test_public_robot_preflights_fail_closed_on_transport_and_limits(tmp_path) -> None:
    for robot, model in (("fr3", "fr3"), ("enlight", "flexiv-enlight-l")):
        path = tmp_path / f"{robot}.json"
        path.write_text(
            json.dumps(
                _snapshot(
                    model=model,
                    network_ok=False,
                    estop_ready=False,
                    command_authority_count=1,
                    positions_rad=[2.0],
                    position_limits_rad=[[-1.0, 1.0]],
                )
            ),
            encoding="utf-8",
        )
        result = preflight(robot, path, read_only=True)
        assert result["ready"] is False
        assert {
            "disconnected-device",
            "estop-not-ready",
            "command-authority-active",
            "limit-violation",
        } <= set(result["errors"])
