<!-- pal:language:start -->
<p align="right">
  <a href="../ko/nvidia-ecosystem.md" lang="ko">한국어</a> | <a href="nvidia-ecosystem.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# NVIDIA Physical AI experience workbook

Build one evidence chain: **scene → physics/sensors → demonstration → policy → independent evaluation → deployment candidate**. Start without a robot or headset. This workbook connects catalog lessons to additional official NVIDIA exercises; external exercises do not silently become catalog completion. Read the [equipment progression](equipment-stages.md) and [PhysX concepts](concepts/physx.md) first.

## Know which layer you are using

| Layer | What the learner changes | Evidence produced | Repository status |
|---|---|---|---|
| Isaac Sim / OpenUSD / PhysX | Assets, drives, contacts, camera and lighting | USD provenance, actual physics observations, images | Catalog import/control/sensor lessons; actual GPU execution required |
| Isaac Lab | Vectorized task, reward, reset and training/evaluation | Config, checkpoint, seed and held-out rollout | Separate pinned environment and official extension exercises; not every GPU lesson uses Lab |
| Isaac Teleop / Isaac Capture / CloudXR | Input, retargeting, session and recording | Tracking/reception clocks, transforms, replay | Catalog offers synthetic MuJoCo contracts; live device input remains unverified |
| GR00T / VLA | Dataset modality/action contract, model-specific adaptation | Dataset manifests, weight identity, inference/evaluation | Pinned GR00T profile; import smoke is not task performance |
| ROS 2 / Isaac ROS and deployment | Time-stamped messages, policy interface and runtime gate | Message/latency evidence, candidate hashes, offline sink | Ordinary ROS lessons exist; Isaac ROS accelerated packages and Jetson acceptance are separate |

Official sources: [Isaac Sim documentation](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html), [Isaac Lab](https://developer.nvidia.com/isaac/lab), [Isaac Capture](https://nvidia.github.io/IsaacCapture/main/), and [GR00T](https://developer.nvidia.com/isaac/gr00t). Current upstream documentation is a reference, not permission to replace installed environments.

## 0. Record a reproducible environment plan

From this repository's activated Core environment, inspect without installing:

```bash
pal stack plan --profile isaac-modern --json
pal stack plan --profile groot --json
pal stack plan --profile pi05 --json
```

Read [stack-lock.json](../../setup/stack-lock.json) and the [two-stack strategy](../../setup/08_ISAAC_STACKS.md). Keep vendor-compatible Isaac and modern Isaac Lab profiles isolated. Record native OS, GPU/driver/VRAM, Python, source revision, extensions and license acceptance separately. Do not apply an environment or download weights merely to read the book. Missing runtime remains unavailable.

The reviewed official [Teleop quick start](https://nvidia.github.io/IsaacCapture/main/teleop/quick_start.html) now uses `isaaccapture` and notes a rename from `isaacteleop`. Its package/import names and examples can differ from older installations. Pin a compatible checkout and package together in a separate environment before using new commands. The [Lab/Sim integration page](https://nvidia.github.io/IsaacCapture/main/integrations/isaac_lab_sim.html) is marked as being prepared; do not treat that page as a tested recipe for this repository.

## 1. Import a robot and audit physics

Use [sim-isaac-01](lessons/sim-isaac-01.md), then [sim-fr3-01](lessons/sim-fr3-01.md) or [sim-enlight-03](lessons/sim-enlight-03.md) on a ready host. Inspect the imported articulation's named joints, axes, limits, collision bodies, inertia, drive and tendon/mimic behavior. Save source hashes/import options and derived USD in the run directory. Execute the documented baseline and check its actual `physx-observations.json` and `isaac-frame.png`.

One-variable exercise: change one documented controller parameter or a single drive setting in a separately preserved official example, with pose/targets/timing fixed. Explain raw command versus measured joint/TCP state. A nonblank image proves neither joint mapping nor correct contact.

Checkpoint: identify three model properties that can make a visually correct import physically wrong. Answer: inertia, drive/actuator semantics and collision/coupling are examples.

## 2. Experience RTX cameras and synthetic observations

Follow [sim-isaac-02](lessons/sim-isaac-02.md). Save RGB and the available annotation/depth outputs with image size, camera intrinsics/extrinsics, units and capture timing. Inspect foreground framing and labels; do not substitute an unrelated preview image. Use the installed release's official sensor/randomization example when extending beyond the lesson.

Keep the scene/seed fixed and change only lighting or camera pose, never both in one trial. Compare visibility and label alignment, then describe which observation shift a policy would see. A rendered pixel change is not evidence of improved policy robustness. Record the exact extension/API version because upstream randomization APIs migrate.

## 3. Compare engines before scaling training

Run [core-fr3-09](lessons/core-fr3-09.md) and actual [sim-fr3-01](lessons/sim-fr3-01.md) under the documented matching contract, then [sim-fr3-04](lessons/sim-fr3-04.md). Inspect targets, initial pose, frame and period before the scalar error-difference metric. Equal error magnitudes can hide opposite position errors. Newton or MuJoCo-Warp is a distinct backend choice; do not relabel it as independent PhysX evidence.

## 4. Train and evaluate in Isaac Lab

After the isolated Lab environment passes its official basic example, use the installed release's task registry and official [Isaac Lab learning resources](https://developer.nvidia.com/isaac/lab). Begin with a small supported simulated task. Save task ID, observation/action shape, reward terms, reset/termination rules, number of environments, seed, configuration and checkpoint. Replay a policy in a separate evaluation run with held-out conditions.

One-variable experiment: increase only environment count while keeping the learning budget explicitly defined. Compare transitions/second, memory and evaluation return; wall-clock speed and sample efficiency are different. This external Lab exercise is not the existing MJLab-based G1/Wuji lesson and is not automatically a verified FR3/Enlight Lab task. A new robot/task needs its own mapping and acceptance evidence. Use catalog [PhysX PPO](lessons/sim-fr3-03.md) for the repository's implemented arm workflow.

## 5. Teleoperate a simulated target before owning XR gear

First complete the synthetic contract [core-teleop-01](lessons/core-teleop-01.md) and offline [sim-teleop-02](lessons/sim-teleop-02.md). Inspect SI units, xyzw quaternion order, left/right identity, calibration, receive time, clutch/deadman, stale input at 100 ms and explicit local rearm. The catalog's input is synthetic; software success is not a human-device test.

As an external NVIDIA exercise, the official quick start offers a desktop browser emulator and a terminal-only gripper retargeter. In a separately reviewed compatible Capture environment, with vendor setup/consent handled and no robot transport connected, the documented example is:

```bash
python -m isaaccapture_examples.teleop.gripper_retargeting_example_simple --duration 20
```

It prints binary open/close values; no physical gripper is needed. Hold other input fixed and compare trigger values immediately below/above its threshold. Explain why continuous trigger input can produce a binary output. Save software version and cleanup outcome. The example can start a CloudXR service and prompt for its EULA; it is an optional runtime action, never part of automatic book generation. A desktop emulator is not Quest acceptance.

## 6. Add Quest, MANUS and VIVE only when useful

Use [sim-teleop-01](lessons/sim-teleop-01.md) and [pinned Ubuntu VR setup](setup/vr-teleop.md). Begin read-only, one stream at a time, then combined input: headset/controllers, fingers and wrists are separate signals. Validate calibration transforms and freshness independently; SDK names and quaternion conventions are not interchangeable. Manufacturer/plugin support in the current [Capture ecosystem](https://nvidia.github.io/IsaacCapture/main/overview/ecosystem.html) does not validate this learner's hardware/firmware combination.

Record at least 60 seconds per stream and simultaneous input, rate/max gap, validity, occlusion, release, timeout and reconnection. Compare a stationary pose with one known motion. Do not enable haptic outputs or connect robot command transport. Preserve the existing Hub/SDK protocol boundary described in the repository setup; a current upstream plugin cannot erase a documented mismatch. The [public VR record](../verification/vr-teleop-2026-11-13.md) has no live human-input pass.

## 7. Collect, augment, learn and evaluate

Use [sim-enlight-06](lessons/sim-enlight-06.md) to understand simulated camera/state/action episodes. Inspect saved/discarded/aborted provenance, hashes and episode-level splits, then compare [BC](lessons/core-enlight-04.md). A three-episode synthetic example teaches a contract; it is not a sufficient real training dataset.

For an external Isaac Lab Mimic/Teleop exercise, follow the matching release's guide linked from the official quick start: record a simulated demonstration, validate reset/task success, generate augmented demonstrations, train and test on separate seeds/scenes. Keep source and generated episode provenance separate. Measure acceptance/rejection and held-out task success, not only the number of generated trajectories. An official sample for another robot is not an Enlight adapter.

For GR00T, follow the pinned [installation/data handoff](../../setup/LATEST_ROBOTICS_UPDATE.md) and [VLA concepts](concepts/vla.md). Check image/state/language modalities, action units and horizon, normalization, robot embodiment, weights/license and episode split. Compare only one adaptation or inference parameter under fixed evaluation conditions. Report latency, invalid responses, task success and failure cases separately. Catalog `core-vla-01` remains a mock; model import and compatible-shaped data do not establish GR00T pick-and-place performance. A two-finger gripper and UMI are [later task-specific options](equipment-stages.md), not required to start.

## 8. Finish with a candidate and an offline runtime

Connect policy/state/image time through [ROS lessons](lessons/sim-ros-01.md), [deployment candidate](lessons/sim-deploy-01.md) and [offline command sink](lessons/hw-common-01.md). An optional Isaac ROS or Jetson extension needs its own supported platform/package/license and latency validation; no Jetson purchase is a prerequisite for the earlier GPU experience. Freeze model/data/environment hashes and compare a replayed target to the saved action schema. Only then study real-robot readiness, with separate [hardware safety](../07_SAFETY.md) gates.

## Record experience honestly

For each exercise save: input/config revision, artifacts, numeric observation, one-variable comparison, interpretation, limitation and next step. Use `passed`, `failed` or `not_run`; distinguish planned, installed, software-tested, GPU-executed, human-input-validated and physical-robot-validated. This workbook has been authored and checked as documentation. It does not claim that these external NVIDIA runtimes were executed during book production.
