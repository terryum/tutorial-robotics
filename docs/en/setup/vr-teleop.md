<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/setup/vr-teleop.md" lang="ko">한국어</a> | <a href="vr-teleop.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Ubuntu VR teleoperation setup

WS2 Ubuntu runs Quest 3 display/controllers, MANUS fingers and VIVE wrists, simulation, collection and learning. Mac supports contracts, transforms, replay and small MuJoCo examples. Windows is optional for vendor recovery; no permanent Windows input server is required. Existing VR-free lessons and installed Isaac/CloudXR/MANUS environments remain usable.

## VIVE Linux beta

Use the official [Hub v1.0.3 beta release](https://github.com/ViveRoboticsSoftware/vivehub-linux/releases/tag/v1.0.3).
The x86_64 archive SHA256 is `4bd87a7d7cb7d580a8dce0a5b2b5d4c32c1bd44822fec4a7bbf5971da277bc07`.
Download the matching `.sha256` file and verify before extracting under ignored
`.local/vendor/vivehub-1.0.3/`. Read LICENSE.txt and ThirdPartyLicenses.txt.
HTC EULA consent is separate from prior NVIDIA consent. Do not run Hub, its SDK,
udev installation, pairing, map setup or device initialization before that review.
The current development archive is checksum-verified and extracted only; no HTC
EULA acceptance or live device success has been recorded.

The [official Hub architecture](https://github.com/ViveRoboticsSoftware/vivehub-linux)
requires launching `run-vivehub.sh`; Hub owns the tracker_server. Never start a
second server from the collector. Hub supports mapping/pairing on Linux and does
not provide Quest HMD support. Its included SDK uses **/tmp/vut.sock**, protocol 1,
12-byte `<BBHII` header, HELLO/ACK, and READY=2. Poses are meters and xyzw in HTC/OpenVR
right-handed space. The collector only sends HELLO with pose/status subscription;
it exposes no pairing, power, reset or setup commands. Serial numbers remain local.

The candidate standalone SDK revision
`8685112780734c2513c66d53b9eb104db47afcf9` in the
[official SDK repository](https://github.com/ViveRoboticsSoftware/vive-ultimate-tracker-sdk)
uses **/tmp/vive_tracker.sock**, a 16-byte `<IBB10s` header and READY=8.
This is **not wire-compatible** with the Hub v1.0.3 included SDK. Do not substitute
that Python reference client or launch its standalone server alongside Hub.
`pai_lab.vive_ipc` implements the included Hub framing with a bounded nonblocking
receive buffer; it never waits for the rest of a fragmented packet. Software
socketpair tests do not establish IPC compatibility against a running vendor daemon.

## Input and calibration / 입력·보정

1. Quest: preserve current CloudXR/Isaac environment; verify head view and controllers
   read-only, including timestamped clutch/deadman release. Quest-only is an explicit
   alternative mode, never an automatic fallback from integrated mode.
2. MANUS: confirm actual glove model, firmware, Linux SDK compatibility and Integrated
   entitlement first. Use the official printer/plugin read-only stream. Map joint
   names explicitly and preserve raw device timestamps, clock domain and tracking.
3. VIVE: after separate EULA review, apply only missing USB permissions/dependencies.
   Use Hub to pair and build a Linux map. Assign left/right tracker identities locally.
   Validate tracker_from_wrist mounting transforms and world_from_device alignment
   with the Quest space using stationary poses and known movements. Do not reuse
   Windows calibration without independent Ubuntu verification.
4. `InputMux` consumes read-only DeviceSample envelopes. Supply calibrated SE3 matrices
   and an explicit calibration ID. Device clocks remain raw evidence; freshness uses
   each source's local monotonic reception time. Reconnection requires a new session.
   Device adapters must not restamp cached samples as fresh. Quest switches, both
   MANUS finger streams and both VIVE wrists must all be fresh in integrated mode.

## Acceptance / 검증

For EACH stream and then simultaneous input, record at least 60 seconds of rate,
maximum gap and tracking validity (`pai_lab.teleop_sources.rate_report`). Check
stationary/moving input, occlusion, switch release and reconnect. Poll the sink
independently of receive callbacks; last valid input expires at exactly 100 ms.
A separate local rearm after releasing both switches is required. Hardware runtimes
must enforce their own watchdog if the collector process fails.

Check three saved episodes plus discarded and aborted cases. Raw input, applied
named target, actual state and camera data must have clock labels and timestamps.
Use exclusive episode IDs; preserve partial recording after interruption. Reload,
check hashes, then split entire episodes. Synthetic data is never human device
validation. Installation, software tests, live input, simulation performance and
physical robot operation are separate acceptance levels.

## Route / 수업 순서

[core-teleop-01](../lessons/core-teleop-01.md) →
[sim-teleop-01](../lessons/sim-teleop-01.md) →
[sim-teleop-02](../lessons/sim-teleop-02.md) →
[sim-enlight-06](../lessons/sim-enlight-06.md).
The alignment lesson's offline mode can run while physical calibration is pending;
this does not complete sim-teleop-01. Enlight uses its own model, six-axis wrist IK,
joint limits and arm-only BC data. No gripper pick/transfer until verified.

## Current verification / 현재 상태

Native Ubuntu WS2: archive verified and isolated, protocol mismatch identified,
no Quest/MANUS/VIVE USB devices observed. HTC review, Hub daemon negotiation,
MANUS firmware/entitlement, Linux map and transforms, live 60-second evidence and
human demonstrations remain pending. Isaac extension follows MuJoCo validation in
the preserved environment; Lab lessons require a separate compatible environment.
No learner completion or physical robot authority is created by development tests.

## Read-only IPC capture after HTC review

```bash
python -m pai_lab.vive_ipc --htc-eula-reviewed --duration 61 --output-dir .local/vive-input-unique
```

The flag is an explicit operator assertion; development setup never passes it automatically. Hub must already own the daemon. Raw device evidence stays local.
