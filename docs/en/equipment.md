<!-- pal:language:start -->
<p align="right">
  <a href="../ko/equipment.md" lang="ko">한국어</a> | <a href="equipment.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Equipment and execution environments

Choose execution hosts by verified capabilities. Names such as WS1 and WS2 do not establish Ubuntu, ROS, CUDA, Isaac or robot-runtime readiness. Any workstation with the required capabilities can start at the first lesson.

## Independent MacBook scope

The macOS arm64 execution scope is 33 Core lessons plus `sim-deploy-01` and the offline command sink `hw-common-01`: 35 lessons. Actual Python 3.12, NumPy, MuJoCo, pinned public models and each lesson's other requirements must be available. Core learning can require additional dependencies. Keep learner state and run evidence in ignored `.local/`.

`sim-fr3-04` can analyze evidence on macOS, but is not independent execution. First produce genuine PhysX evidence on a capable host, then compare it to MuJoCo evidence with matched targets, initial pose, world frame and control period. MuJoCo output cannot substitute for PhysX output.

## When to move to a remote workstation

| Work | Required actual capabilities | Evidence to inspect |
|---|---|---|
| Foundations and Core control/learning | Python 3.12, lesson libraries and pinned models | Numeric artifacts and local check |
| ROS lessons | Supported Ubuntu/ROS environment and message/service runtime | Topics, timing, QoS and replay records |
| GPU PPO and VLA | Lesson-specific CUDA, mjlab/training or policy server | Actual execution and evaluation artifacts |
| Isaac/PhysX | Supported Ubuntu, NVIDIA CUDA, compatible Isaac Sim/model | Genuine PhysX observations, renderings and coupling checks |
| Physical preparation | Isolated network, device identity and read-only preflight | Model, tool, payload, limits, stop and run-card evidence |

The [MacBook → WS remote-development guide](setup/remote-development/index.md) explains connection and resume. Recreate the locked environment per host; do not copy virtual environments. Missing GPU or device evidence remains `capability-unavailable` or `reader_test_required`. Publication badges and evidence from this host are separate.

## Deployment and physical boundaries

The 72 lessons comprise 33 Core, 27 Sim and 12 Hardware lessons. One Hardware lesson is an offline sink; the other 11 are `scaffolded`. Documentation, simulation and policy evaluation do not authorize physical actions. Begin read-only and obtain separate approval for each fresh exact action. Read [safety](../07_SAFETY.md) and [deployment/physical concepts](concepts/deployment-hardware.md).

[Platforms, capabilities and status per lesson](lessons.md) · [Public verification report](../verification/robot-paths-2026-11-08.md)

## Progress from minimal equipment

Follow [laptop → GPU → optional collection equipment → real robots last](equipment-stages.md). The [NVIDIA experience workbook](nvidia-ecosystem.md) connects Isaac Sim, Lab, Teleop/Capture, GR00T and ROS/deployment through exercises and evidence. Consider XR, a gripper or UMI only for the later tasks that need them.
