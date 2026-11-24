<!-- pal:language:start -->
<p align="right">
  <a href="../ko/equipment-stages.md" lang="ko">한국어</a> | <a href="equipment-stages.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Learn with the least equipment first

The reading order increases equipment requirements. Catalog order remains stable for compatibility; the named routes and this guide provide teaching order. You can learn arm, hand and mobile-robot concepts without owning those robots. [Equipment capabilities](equipment.md) determine execution, and [all lesson goals](lessons.md) show exact prerequisites.

| Phase | Minimum equipment | Experience and evidence | Transition |
|---|---|---|---|
| 1. Foundations | MacBook or a Windows/Linux laptop | Python, state, models and plots: core-01–core-04 | Explain units, coordinates and reproducibility |
| 2. Local robotics | A supported Core environment; no robot/XR gear | FR3 control/IK, Enlight models, Shadow/Wuji, Stretch, short PPO/BC, offline input | Inspect artifacts and distinguish execution from performance |
| 3. GPU simulation | A verified remote or local NVIDIA workstation | Isaac Sim imports, PhysX, cameras, matched-engine comparison and learning | Genuine engine artifacts and independent evaluation |
| 4. Optional human data | Workstation plus selected Quest 3, MANUS glove and/or VIVE tracker input | Read-only input → alignment → sink → simulated episodes | Live input validation distinct from synthetic replay |
| 5. Data-to-policy | Verified GPU plus recorded data; optional UMI collection rig | Episode splits, BC/VLA and Isaac Lab/Teleop workflows | Independent held-out simulation evaluation |
| 6. Real robot, last | Reviewed FR3 or Flexiv Enlight; Wuji only for the hand branch | Offline replay → sink → read-only → shadow → torque-disabled replay → fresh exact-action approval | Physical evidence, tool/payload/stop checks and per-run approval |

## Laptop entry: Windows does not mean native Core acceptance

The catalog supports macOS arm64 and Linux x86_64 for portable Core. A Windows laptop can read the entire book, connect to a supported remote host, or use a separately checked Linux environment. [Microsoft WSL](https://learn.microsoft.com/en-us/windows/wsl/install) provides Linux on Windows; that feature alone does not certify this curriculum, graphics or GPU stack. Verify the distribution, architecture, Python, MuJoCo rendering and artifacts before claiming local success. Do not infer Ubuntu/Isaac acceptance from a Windows hostname. [Remote laptop setup](setup/remote-development/laptops.md) supplies the alternative.

## A manipulator route without an early robot purchase

1. Laptop: common foundations → FR3 anatomy, PD, gravity, Jacobian/IK, task-space control, contact and trajectories. A simulated FR3 is enough.
2. Laptop learning: reach environment → short PPO → demonstrations/BC → independent evaluation. Train Enlight on its own model; an FR3 policy is not an Enlight candidate.
3. GPU: actual PhysX control and learning → matched MuJoCo/PhysX evidence → Isaac cameras and synthetic data. Use the [NVIDIA experience workbook](nvidia-ecosystem.md).
4. Optional collection: `core-teleop-01` → `sim-teleop-01` → `sim-teleop-02` → `sim-enlight-06`. Offline alignment can be studied while live input is blocked; it does not complete the device-input lesson.
5. Simulation deployment candidate and offline runtime sink; finally read-only robot readiness. Probe contact and pick-transfer-place remain separate final branches with their own tools/controllers.

The [named manipulator path](paths.md) retains its exact prerequisites. The optional collection branch supplements that path and does not make XR equipment a prerequisite for ordinary control or learning.

## Reuse input equipment deliberately

| Device or option | Educational role | What remains to verify locally |
|---|---|---|
| Meta Quest 3 | Viewpoint, controllers, clutch/deadman; optional hand input | Tracking, local receive timing, release/reconnect, selected pipeline/version |
| MANUS haptic glove | Finger configuration and hand retargeting | Exact model, firmware, SDK/entitlement, calibration and timestamp semantics |
| HTC VIVE Ultimate Tracker | Wrist/body pose independent of finger angles | Exact tracker model, Hub/SDK protocol, mounting/world transforms, tracking validity |
| Wuji Hand 2 Beta 2 | Simulated dexterous hand; real read-only branch last | Joint names, limits, tactile calibration and separate physical gates |
| UMI-style collector | Robot-free demonstration data for a parallel-jaw task | Camera/pose/width synchronization, calibration and target-robot feasibility |

The product name intended here is **HTC VIVE Ultimate Tracker**; confirm the actual label before selecting a driver. MANUS Pro Haptic, MANUS Metagloves Pro and older Haptic variants are not interchangeable SDK identities. [MANUS documentation](https://docs.manus-meta.com/latest/Products/Metagloves%20Pro%20Haptic/) is a model-specific starting point. Haptic feedback is an output/actuation path; reading finger poses does not authorize enabling it.

For Ubuntu, use the repository's [pinned VR setup](setup/vr-teleop.md) and [actual verification record](../verification/vr-teleop-2026-11-13.md). A Linux Hub archive and software socket tests are not evidence of live devices. The separate [HTC product page](https://www.vive.com/us/accessory/vive-ultimate-tracker/) describes the consumer PC-VR route; its Windows requirements do not establish Linux beta or Quest integration. Preserve existing VR environments. The book does not publish a learner's inventory, device IDs or private robot integration.

## What, if anything, to buy later

No additional robot, headset, glove or tracker is required for the opening chapters. For a VLA pick-and-place capstone, plan a compatible **two-finger parallel gripper**, wrist/scene RGB camera coverage, known mounting/tool/payload and a calibrated workspace. The repository uses Robotiq 2F-85 as a simulation baseline; that is not a purchase commitment or proven Enlight compatibility. Check aperture, force/speed range, mass, mounting, electrical/interface support, stop/status API, latency and simulation coupling before choosing a model. A camera or mount may be the missing part even when the arm is already available.

Consider a UMI kit only when the goal is robot-free demonstration collection for that action representation. [The original UMI project](https://umi-gripper.github.io/) uses hand-held parallel-jaw grippers and cameras; it is not a glove replacement or a ready-made adapter for every robot. Match visual observations, width and relative pose to the policy/robot schema before procurement. Start with a small validated collection exercise; do not buy a new humanoid or Jetson merely to begin the NVIDIA chapters. No shopping or installation is performed by this guide.

## Equipment grows; authority does not

Synthetic input, real human input, simulated policy performance and physical operation are four separate claims. Finish each with its own evidence. An unavailable phase stays blocked and preserves all earlier learning. The final physical phase follows [hardware safety](../07_SAFETY.md); no earlier phase authorizes motion.
