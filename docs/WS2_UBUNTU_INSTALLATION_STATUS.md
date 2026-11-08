# WS2 Ubuntu installation status

Verified: 2026-09-10 (Asia/Seoul). OS layer: native Ubuntu. Mode: `DEVELOPMENT`.

This report records installation and software-only verification. It does not
complete T00 or any later tutorial, grant robot command authority, or claim a
physical VR/robot connection.

## Host capability

| Component | Verified state |
|---|---|
| OS | Ubuntu 24.04.5 LTS, x86_64, native boot |
| CPU / memory | Intel Core Ultra 9 285K, 24 logical CPUs, 125 GiB RAM |
| GPU | NVIDIA GeForce RTX 5090, 32,607 MiB VRAM |
| Driver | NVIDIA 595.84 |
| Display | X11 and MuJoCo EGL verified |
| Storage after provisioning | root 366 GiB total / 242 GiB available; `/data` about 1.3 TiB available |

Machine-local hostname, address, interface, environment paths, and credentials
remain under ignored `.local/` and are not stored in this report.

## Installed environments and tools

- uv 0.12.10 with separate locked public and shared-core environments.
- Native ROS 2 Jazzy Desktop, CycloneDDS, RViz, colcon, and rosbag2 MCAP.
- Docker Engine 29.8.0, Docker Compose 5.5.1, and NVIDIA Container Toolkit 1.19.1.
- A locked learning environment with PyTorch 2.13.0+cu130 and Stable-Baselines3 2.9.0.
- A separate `gpu-lerobot` environment with LeRobot 0.5.1 and CUDA-enabled PyTorch.
- A separate `gpu-mjlab` environment with mjlab 1.6.0, MuJoCo 3.11.0,
  MuJoCo Warp 3.11.0, and CUDA-enabled PyTorch.
- A separate `gpu-isaac-modern` environment with Isaac Sim 6.0.1.0 and the
  official Isaac Lab `v3.0.0-beta2.patch1` source release.
- The official `nvcr.io/nvidia/isaac-sim:6.0.1` container, pinned to digest
  `sha256:783444c706538aa76cf5126e911ddc5e618779e6105305ad4af4260362a30aa9`.
- OpenSSH server, CMake 3.28.3, GCC/G++ 13.3, Git LFS 3.4.1, and FFmpeg 6.1.1.

The Python roles remain isolated. System Python was not modified with pip, and
vendor/modern Isaac, mjlab, LeRobot, and small-learning environments were not
merged.

## Software-only verification

- public doctor passed; public tests: 15 passed.
- shared-core tests: 8 passed.
- MuJoCo deterministic pendulum and EGL rendering passed.
- Native Jazzy C++ publisher to Python subscriber passed.
- ROS TF, RViz, MCAP record/replay, disconnect detection, invalid-record
  rejection, and command-free replay passed.
- PyTorch CUDA tensor checks passed in the learning, LeRobot, mjlab, and Isaac environments.
- Docker `hello-world` and the official CUDA 12.8 container GPU check passed.
- mjlab dependency check, Warp CUDA discovery, and Unitree environment registry passed.
- Isaac Sim's official compatibility checker returned `PASSED` for the RTX 5090 host.

## Known limitations and user-gated work

- Isaac Sim's first application launch was not performed because the user must
  review and accept NVIDIA's EULA. Run one official Isaac Lab example after that step.
- The current Isaac Sim/Lab beta package metadata contains mutually incompatible
  exact pins for some full extras. The documented Isaac Lab Torch 2.10+cu128
  override is installed; final runtime acceptance remains pending the official example.
- `gpu-isaac-vendor` is not guessed. Create it only after a selected upstream
  robot example provides its exact simulator/Lab pair.
- Robot model/source selection remains T02 work; policy checkpoints and large datasets were not fetched.
- Docker group membership takes effect in a new login session.
- VR pairing, calibration, live streams, physical robots, isolated robot networking,
  and all hardware motion remain unverified and unauthorized.

## Progress boundary

- This is pre-v1 host evidence; learner progress now remains local and publication evidence lives in `state/PUBLISHING.md`.
- Next prerequisite-eligible tutorial remains **T00**.
- This installation makes the host capable of later GPU tutorials; it is not
  evidence that their learning or acceptance contracts were completed.

## Native Ubuntu maintenance — 2026-11-09

The sections above retain the historical 2026-09-10 snapshot. Current checks used
public work base `ea066c2`, core `f3723f9`, Ubuntu 24.04.5, Python 3.12.3,
RTX 5090 and driver **595.99.02**. Locked base/development dependencies were
synchronized with `uv sync --locked --inexact`, preserving existing extras.
Required native ROS packages were already installed; no system-package, driver,
CUDA or simulator upgrade was needed.
Both native ROS virtualenvs were also synchronized with their existing locks.
The public ROS environment's editable project metadata was updated from
`pai-lab 0.1.0` to `1.0.0.dev0`; both dependency checks passed.

- Public tests: **195 passed, one optional vendor-cache skip**, eight subtests.
  Core: nine passed. Ruff, mypy, repository/release/public-boundary/credential
  checks and strict MkDocs passed.
- MuJoCo 3.12 deterministic pendulum: 1,000 samples, repeat error **0**,
  finite states and nonblank EGL rendering.
- Native Jazzy/CycloneDDS communication, TF, RViz on a virtual display and MCAP
  record/replay passed. Replay matched exactly and emitted no commands.
- Existing learning, LeRobot, mjlab and default Isaac environments passed
  dependency checks and CUDA matrix multiplication. Additional smoke checks
  passed: a 16-step PPO update, synthetic ACT GPU inference without downloading
  weights, and ten MuJoCo-Warp GPU physics steps.
- Existing default Isaac **6.1.0.0** / Teleop **1.3.131** passed headless PhysX
  and RTX rendering: 182 physics steps, cube height approximately **0.100 m**,
  nonblank **320 x 240 RGBA** image and clean process exit. Existing Isaac terms
  consent was reused. These results supersede the historical first-launch
  pending item above; they do not verify new robot-path lessons or live VR.

The retained `gpu-isaac-modern` recovery environment still passes CUDA arithmetic
but has **11 dependency incompatibilities**. Its Sim/Lab beta stack contains
contradictory requirements, including coverage 7.4.4 versus 7.6.1, packaging 26.0
versus <24, and websockets 12.0 versus >=13.1. It is preserved and is **not a
dependency-clean supported execution environment**. Use the verified default
Isaac environment for its documented workflow; new Lab-specific work needs a
separately validated compatible stack.

Learner history was preserved. This maintenance created no lesson completion,
hardware authority, driver/firmware changes, remote-access changes or reboot.
