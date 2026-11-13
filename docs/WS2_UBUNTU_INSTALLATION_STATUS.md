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

<a id="enlight-ws2-20261113"></a>

## Enlight and native verification — 2026-11-13

Native Ubuntu 24.04.5 / RTX 5090 / driver 595.99.02. Existing locked Core/dev
environments were synchronized without removing extras. Working GPU environments
were reused; the recovery-only Isaac Lab beta still has 11 dependency conflicts.
No new Lab environment was required by this installation task.

- MuJoCo: 1,000 samples, repeat error 0, finite states and inspected EGL image.
- Native ROS: communication/TF and exact MCAP replay; RViz launched and stopped.
- Learning/LeRobot/mjlab/default Isaac: dependency and CUDA checks passed;
  16-step PPO update, synthetic ACT CUDA output `(1, 4)` and ten Warp physics steps.
- Default Isaac 6.1: PhysX 182 steps, cube height 0.099999964 m, inspected
  320 × 240 RGBA image, RGB standard deviation 15.66696, process exit 0.
- Isolated Python 3.12 SDK: `flexivrdk==2.1.0`, `numpy==2.5.4`; imports and
  dependency check passed. Reproduction uses
  `setup/requirements/enlight-rdk-2.1-linux-py312.txt` with wheel SHA256 hashes.
- Operational sources: RDK `bfab04f4e385ca335ee3025bfefe70249b015578`, ROS
  `a165e88a2b41cb7e09b46aa1bfb842718ee783b1`, description
  `54593cda75bac0251567a13db3d6862da7fe7cfb`. Educational source pins unchanged.
- C++ RDK built against isolated Zenoh C/C++ 1.9.0, SpaceVecAlg 1.2.8 and
  RBDyn 1.9.3, reusing installed Eigen/spdlog/Boost/tinyxml2/yaml-cpp. Official
  Zenoh C GNU x86_64 standalone archive SHA256:
  `29f6a0dedc7ada0be007058e706df64ff26e62ae56f6efc2b098132c431c263d`.
- Jazzy control packages and xacro were missing and installed. Nine driver
  packages built without vendor edits. Build with `colcon build --base-paths src`,
  system `Python3_EXECUTABLE` and `Python_EXECUTABLE`, isolated
  `CMAKE_PREFIX_PATH`, and `CMAKE_CXX_FLAGS=-I<prefix>/include`: upstream
  gpio_controller omits RDK include propagation. Exclude dependency source trees
  from colcon discovery rather than changing vendor source.
- Official fake hardware: confirmed GenericSystem in generated URDF before
  launch; seven joint names, 0.01 rad trajectory and error below 1e-5 rad passed.
  No real SDK connection or hardware commands. Separate synthetic offline replay
  and sink: 64 frames, seven joints, exact match, sockets forbidden.
- Fixed the teaching ROS adapter to spin a dedicated executor on its own context.
  Native regression runs service/action and bag paths twice; Enlight DDS received
  all 64 samples with zero state error, reset and TF passed.

Quest/MANUS/VIVE were absent from USB inventory. Existing CloudXR/client and
MANUS plugin/printer libraries were retained; live input, firmware and SDK
entitlement remain pending. No matching Elements Studio installer was available
in the existing setup caches: request the Ubuntu 24.04 x86_64 package compatible
with Enlight-L / v3E.1 / RDK Professional, its checksum, license and matching
Elements/Orion/Aegis manuals through Flexiv Hub/support. Description v4 versus
v3E.1 remains a physical-use gate. No robot motion, firmware/driver change,
reboot, learner completion or remote push occurred.
