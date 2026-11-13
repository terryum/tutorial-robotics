"""Exclusive episode storage: raw input, applied target, state and camera clocks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from pai_lab.teleop import BimanualFrame


def encode(value: Any) -> str:
    return json.dumps(value, allow_nan=False, sort_keys=True)


class Episode:
    def __init__(self, root: Path, episode_id: str, *, provenance: str):
        if not episode_id or Path(episode_id).name != episode_id or episode_id in {".", ".."}:
            raise ValueError("single component episode id required")
        self.path = root / episode_id
        self.path.mkdir(parents=True, exist_ok=False)
        self.rows: list[dict[str, Any]] = []
        self.closed = False
        self.provenance = provenance
        self._manifest("recording")

    def _manifest(self, status: str) -> None:
        payload = {
            "schema_version": 2,
            "status": status,
            "provenance": self.provenance,
            "count": len(self.rows),
        }
        if status != "recording":
            payload["sha256"] = hashlib.sha256(
                (self.path / "frames.jsonl").read_bytes()
            ).hexdigest()
        temp = self.path / "manifest.tmp"
        temp.write_text(encode(payload))
        temp.replace(self.path / "manifest.json")

    def append(
        self,
        frame: BimanualFrame,
        *,
        target: dict[str, float],
        state: dict[str, float],
        cameras: dict[str, Any],
        state_time_ns: int,
        mode: str = "preview",
    ) -> None:
        if self.closed:
            raise ValueError("episode closed")
        if not target or set(target) != set(state) or not cameras:
            raise ValueError("aligned named target/state and camera evidence required")
        if state_time_ns < 0:
            raise ValueError("state clock required")
        for camera in cameras.values():
            if camera["time_ns"] < 0 or not camera["data"]:
                raise ValueError("timestamped camera data required")
        row = {
            "input": frame.to_dict(),
            "target": target,
            "state": state,
            "state_time_ns": state_time_ns,
            "state_clock": "collector-monotonic",
            "mode": mode,
            "cameras": {
                name: {"clock": "collector-monotonic", **camera} for name, camera in cameras.items()
            },
        }
        validate_row(row)
        if self.rows:
            previous = self.rows[-1]["input"]
            if (
                frame.session != previous["session"]
                or frame.calibration_id != previous["calibration_id"]
                or frame.sequence <= previous["sequence"]
                or frame.receive_time_ns <= previous["receive_time_ns"]
            ):
                raise ValueError(
                    "episode session/calibration/order changed; abort and start new episode"
                )
        with (self.path / "frames.jsonl").open("a") as stream:
            stream.write(encode(row) + "\n")
        self.rows.append(row)

    def finish(self, status: str = "saved") -> None:
        if self.closed or status not in {"saved", "discarded", "aborted"}:
            raise ValueError("invalid episode transition")
        if status == "saved" and not self.rows:
            raise ValueError("cannot save empty episode")
        (self.path / "frames.jsonl").touch(exist_ok=True)
        self._manifest(status)
        self.closed = True


def replay(path: Path) -> list[dict[str, Any]]:
    metadata = json.loads((path / "manifest.json").read_text())
    content = (path / "frames.jsonl").read_bytes()
    if metadata["status"] != "saved" or hashlib.sha256(content).hexdigest() != metadata["sha256"]:
        raise ValueError("episode is unsaved or corrupted")
    rows = [json.loads(line) for line in content.splitlines()]
    if len(rows) != metadata["count"] or not rows:
        raise ValueError("episode count mismatch")
    previous = None
    for row in rows:
        validate_row(row)
        current = row["input"]
        if previous is not None and (
            current["session"] != previous["session"]
            or current["calibration_id"] != previous["calibration_id"]
            or current["sequence"] <= previous["sequence"]
            or current["receive_time_ns"] <= previous["receive_time_ns"]
        ):
            raise ValueError("episode sequence/session/calibration mismatch")
        previous = current
    return rows


def split_episodes(paths: list[Path]) -> dict[str, list[Path]]:
    if len(paths) < 3 or len({p.resolve() for p in paths}) != len(paths):
        raise ValueError("at least three distinct saved episodes required")
    for path in paths:
        replay(path)
    return {"train": paths[:-2], "validation": paths[-2:-1], "test": paths[-1:]}


def validate_row(row: dict[str, Any]) -> None:
    import math

    BimanualFrame.from_dict(row["input"])
    encode(row)
    if (
        not row["target"]
        or set(row["target"]) != set(row["state"])
        or row["mode"] not in {"preview", "hold"}
        or row["state_clock"] != "collector-monotonic"
    ):
        raise ValueError("named target/state, mode and collector clock required")
    if not all(
        isinstance(x, (int, float)) and math.isfinite(x)
        for values in (row["target"], row["state"])
        for x in values.values()
    ):
        raise ValueError("finite numeric state/target required")
    timestamp = row["state_time_ns"]
    if timestamp < 0 or not row["cameras"]:
        raise ValueError("state timestamp and cameras required")
    for camera in row["cameras"].values():
        if (
            camera["clock"] != row["state_clock"]
            or not camera["data"]
            or camera["time_ns"] < 0
            or abs(camera["time_ns"] - timestamp) >= 100_000_000
        ):
            raise ValueError("camera/state clocks or alignment invalid")
