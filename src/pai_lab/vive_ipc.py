"""Read-only VIVE Hub v1.0.3 VUT protocol client; no server/device commands.

Protocol described by the bundled sdk/include/vut/vut_types.h. The standalone
8685112 SDK uses a different socket/header and MUST NOT be substituted here.
"""

from __future__ import annotations

import socket
import struct
from collections.abc import Callable
from typing import Any

HEADER = struct.Struct("<BBHII")
POSE = struct.Struct("<IIQ13f32s")


class HubDecoder:
    def __init__(self) -> None:
        self.buffer = bytearray()
        self.ready = False
        self.states: dict[int, int] = {}

    def feed(self, data: bytes) -> list[dict[str, Any]]:
        self.buffer.extend(data)
        if len(self.buffer) > 131072:
            raise ValueError("IPC buffer exceeded")
        events = []
        while len(self.buffer) >= HEADER.size:
            kind, version, flags, request, size = HEADER.unpack_from(self.buffer)
            if version != 1 or flags != 0 or size > 65536:
                raise ValueError("incompatible VUT protocol")
            if len(self.buffer) < HEADER.size + size:
                break
            payload = bytes(self.buffer[HEADER.size : HEADER.size + size])
            del self.buffer[: HEADER.size + size]
            if kind == 2:
                if len(payload) != 16 or struct.unpack_from("<H", payload)[0] != 1 or request != 1:
                    raise ValueError("incompatible hello acknowledgement")
                self.ready = True
            elif kind == 0x31:
                if not self.ready or len(payload) != 24:
                    raise ValueError("invalid status event")
                device, state, error, _, timestamp = struct.unpack("<IIIIQ", payload)
                self.states[device] = state if error == 0 else -1
                events.append(
                    {
                        "kind": "status",
                        "device_id": device,
                        "state": state,
                        "error": error,
                        "timestamp_ns": timestamp,
                    }
                )
            elif kind == 0x30:
                if not self.ready or len(payload) != POSE.size:
                    raise ValueError("invalid pose event")
                values = POSE.unpack(payload)
                events.append(
                    {
                        "kind": "pose",
                        "device_id": values[0],
                        "flags": values[1],
                        "timestamp_ns": values[2],
                        "pose": values[3:10],
                        "velocity": values[10:13],
                        "angular_velocity": values[13:16],
                        "tracked": self.states.get(values[0]) == 2,
                        "serial": values[16].split(b"\0")[0].decode("utf-8", "replace"),
                    }
                )
            else:
                raise ValueError("unexpected IPC event")
        return events


class HubClient:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.sock.setblocking(False)
        self.decoder = HubDecoder()
        payload = struct.pack("<HHI32s", 1, 0, 3, b"pai-readonly")
        self.pending = HEADER.pack(1, 1, 0, 1, len(payload)) + payload
        self.closed = False

    def poll(self, watchdog: Callable[[], object]) -> list[dict[str, Any]]:
        """Bounded work per tick; partial header/payload never causes blocking."""
        watchdog()
        if self.closed:
            return []
        try:
            if self.pending:
                sent = self.sock.send(self.pending)
                self.pending = self.pending[sent:]
            data = self.sock.recv(65536)
            if not data:
                self.close()
                return [{"kind": "disconnected"}]
            return self.decoder.feed(data)
        except BlockingIOError:
            return []
        except (OSError, ValueError):
            self.close()
            return [{"kind": "disconnected"}]
        finally:
            watchdog()

    def close(self) -> None:
        self.closed = True
        self.decoder = HubDecoder()
        self.sock.close()


def main() -> None:
    """Opt-in read-only device evidence; never called by synthetic lessons."""
    import argparse
    import json
    import time
    from itertools import pairwise
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--socket", default="/tmp/vut.sock")
    parser.add_argument("--duration", type=float, default=61.0)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--htc-eula-reviewed", action="store_true")
    args = parser.parse_args()
    if not args.htc_eula_reviewed:
        parser.error("review HTC LICENSE.txt/EULA and third-party terms before live IPC use")
    if not 0 < args.duration <= 3600:
        parser.error("duration must be (0,3600] seconds")
    args.output_dir.mkdir(parents=True, exist_ok=False)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(0.05)
    try:
        sock.connect(args.socket)
    except OSError:
        sock.close()
        raise
    client = HubClient(sock)
    start = time.monotonic_ns()
    last_tick = start
    max_tick_gap = 0
    streams: dict[int, list[tuple[int, bool]]] = {}

    def watchdog() -> None:
        nonlocal last_tick, max_tick_gap
        now = time.monotonic_ns()
        max_tick_gap = max(max_tick_gap, now - last_tick)
        last_tick = now

    status = "completed"
    try:
        with (args.output_dir / "raw.jsonl").open("x") as output:
            while time.monotonic_ns() - start < args.duration * 1e9:
                for event in client.poll(watchdog):
                    now = time.monotonic_ns()
                    output.write(
                        json.dumps(
                            {"receive_time_ns": now, "receive_clock": "monotonic", "raw": event},
                            allow_nan=False,
                        )
                        + "\n"
                    )
                    if event["kind"] == "pose":
                        streams.setdefault(event["device_id"], []).append((now, event["tracked"]))
                if client.closed:
                    status = "server-disconnected"
                    break
                time.sleep(0.001)
    except KeyboardInterrupt:
        status = "aborted"
    finally:
        client.close()
    reports = []
    for device, rows in streams.items():
        elapsed = rows[-1][0] - rows[0][0]
        reports.append(
            {
                "device_id": device,
                "samples": len(rows),
                "duration_ns": elapsed,
                "full_60s": elapsed >= 60_000_000_000,
                "rate_hz": (len(rows) - 1) * 1e9 / elapsed if elapsed else 0,
                "maximum_gap_ns": max((b[0] - a[0] for a, b in pairwise(rows)), default=0),
                "tracking_valid_ratio": sum(r[1] for r in rows) / len(rows),
            }
        )
    report = {
        "status": status,
        "streams": reports,
        "maximum_poll_gap_ns": max_tick_gap,
        "command_publishers": 0,
        "calibration_verified": False,
        "live_input_verified": False,
        "note": "rate evidence only; occlusion, release, reconnect and calibration still require review",
    }
    (args.output_dir / "device-input.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report))


if __name__ == "__main__":
    main()
