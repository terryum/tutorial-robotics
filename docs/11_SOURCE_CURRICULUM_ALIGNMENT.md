# Source Curriculum Alignment

## 1. Authority

The conceptual baseline is [`../references/00_USER_BASELINE_2026-08-31.md`](../references/00_USER_BASELINE_2026-08-31.md). This document maps every major baseline requirement to the executable tutorial system. It exists to prevent later Codex sessions from drifting toward a generic robotics curriculum.

`MACHINE_SEQUENCE.md` may change **where** a lesson runs for compatibility and safety, but it must not silently remove **what** the baseline says to learn.

## 2. Model portfolio mapping

| Baseline role | Model | Tutorial coverage | End target |
|---|---|---|---|
| real target | Wuji Hand 2 Beta 2 | T02–T04, T14–T16A, T21, T27, T33–T35, T38, , T42A–T42B | dexterity, tactile, retargeting, regrasp |
| reference | Franka Research 3 v2 | T05–T10, T22–T24 | 7-DoF control and manipulation textbook |
| reference | Unitree G1 29-DoF | T25–T26 | whole-body PPO and motion imitation textbook |
| reference | Sharpa Wave | T16, T16A; optional vendor examples during T33 | tactile/dexterous comparison, not a Wuji replacement |
| watchlist | Unitree H2 Plus | registry only | add only after public ecosystem audit |

## 3. Explicit baseline requirements and coverage

| Baseline requirement | Coverage | Status in v3 |
|---|---|---|
| FR3 control principles before Enlight deployment | T05–T10 | explicit |
| Mac inspection of Enlight URDF and kinematics |  | added in v3 |
| Enlight URDF→MJCF draft, clearly not dynamics truth |  | added in v3 |
| Enlight real system identification |  | added in v3 |
| Wuji before Sharpa | T14–T15 before T16 | explicit |
| official minimal Wuji MuJoCo example on Mac | T14 before custom synergy code | explicit in v3 refinement |
| Wuji offline retargeting and demonstration recording | T16A | added in v3 |
| Wuji full PPO only on NVIDIA workstation | T27 | explicit |
| G1 before H2 Plus | T25–T26; H2 watchlist | explicit |
| G1 staged learning: pose hold→stand→velocity→push recovery→imitation | T26 | expanded in v3 |
| Mac small BC/ACT and VLA protocol/client | T29–T32A | explicit |
| Actual GPU SmolVLA training on WS2 | T32C | explicit |
| Optional π₀ or GR00T remote inference | T32D | added in v3 |
| ROS 2 node/topic/QoS/service/action/parameter/launch/tf2/URDF/JointState/rosbag/lifecycle | T17, T19, T20 | expanded in v3 |
| one monorepo, multiple locked environments | architecture/environment docs and T00 | explicit |
| native URDF/MJCF/USD remain immutable | T02 and model-format policy | explicit |
| ten model asset checks including cross-format FK | setup/04 and T03 | expanded in v3 |
| common RobotBackend and canonical observation/action schemas | T21 and common-interface doc | explicit |
| policy loop separated from high-rate vendor servo | common-interface doc, T21//T32 | explicit |

## 4. Baseline 16-week learning map

The week labels are planning estimates, not automatic deadlines.

| Baseline stage | Approx. weeks | Mac tutorial work | WS2/runtime continuation |
|---|---:|---|---|
| 0. environment and registry | 1 | T00–T04 | local source reconstruction on WS2 |
| 1. MuJoCo grammar/state | 1–2 | T01, T03–T05, , T14 | — |
| 2. kinematics/control | 3–4 | T06–T10, ,  |  real identification later |
| 3. ROS 2 and bridge | 5–6 | T17, T19–T21 |  fake hardware; runtime adapters later |
| 4. Gymnasium/evaluation | 7 | T22 | reusable evaluators feed capstones |
| 5. PPO | 8–9 | T23–T25 | T26 G1, T27 Wuji |
| 6. IL/ACT | 10–11 | T28– |  scale-up |
| 7. dexterous/retargeting | 12–13 | early model/contact: T14–T16; after generic ACT: T16A | T27, T38, T42A/B |
| 8. language/VLA | 14–15 | T32A | T32C; optional T32D |
| 9. real deployment/capstone | 16+ | cockpit/review | T35A/B, T36–T42B |

## 5. Recommended attention allocation

Use this as a curriculum weighting, not as rigid clock accounting.

| Area | Share |
|---|---:|
| manipulator control and contact | 40% |
| Wuji dexterity and tactile | 20% |
| IL/VLA data pipeline | 10% |
| G1 locomotion/whole-body RL | 5% |

## 6. Ordering interpretation

The baseline uses two different notions of order and both are preserved:

- **Detailed pedagogy:** minimal PPO is taught before BC/ACT; advanced hand retargeting/dexterity follows the generic IL/ACT foundation.

Therefore early Wuji model/synergy/contact lessons occur before ALOHA, while advanced offline retargeting T16A occurs after T30/ in canonical execution. G1 remains only about 5% of attention even though minimal PPO concepts precede ACT.

## 7. Baseline code-build sequence mapping

| Baseline build item | Tutorial implementation |
|---|---|
| repository scaffold | T00 |
| robot registry | T02 |
| MuJoCo model inspector | T03 |
| multi-robot viewer | T04 |
| joint-position controller | T06 |
| FR3 FK/Jacobian/IK | T08 |
| Wuji finger/synergy control | T14–T15 |
| ROS 2–MuJoCo bridge | T17, T19 |
| rosbag episode recorder | T20 |
| FR3 Reach Gym environment | T22 |
| minimal continuous PPO | T23–T24 |
| LeRobot dataset adapter | T28 |
| ALOHA ACT training | T29–T30 |
| Wuji retargeting | T16A |
| SmolVLA policy server | T32A–T32C |
| real-robot adapters | T35B– |

## 8. Deployment sequence interpretation

The baseline hardware sequence is preserved as:

```text
simulation → sim-to-sim
→ read-only hardware connection
→ live no-command shadow
→ torque-disabled state replay
→ approved low-speed command
→ workspace-limited task
→ normal operation only after evidence
```

T35B adds an earlier **no-hardware command-sink dry-run** before read-only access. This is an additional safety check, not a replacement for the baseline's post-connection live shadow stage.

## 9. Non-transfer rules

Reference models transfer methods, not hidden physical truth. Never copy these without target-specific identification:

- gains, friction, damping, armature and actuator strength
- torque/current/velocity limits
- link inertia or payload model
- frame and joint order
- command semantics and latency
- tactile scale and contact solver parameters
- trained policy weights unless an explicit embodiment adaptation experiment validates them
