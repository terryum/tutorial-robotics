<!-- pal:language:start -->
<p align="right">
  <a href="../ko/lessons.md" lang="ko">한국어</a> | <a href="lessons.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Complete 72-lesson guide

Goal summaries come from each lesson's first `Learning goals` paragraph. Environments, prerequisite lessons and implementation status come from the catalog. Verification badges appear on the [learning map](index.md). `implemented` does not assert execution on this host or a policy performance pass. `scaffolded` lessons teach preparation and remain blocked without device evidence.

[Equipment](equipment.md) · [Learning paths](paths.md) · [Concept chapters](index.md#eleven-common-concept-chapters)

<!-- pal:goals:start -->
| Lesson | Learning goal | Prerequisites | Platforms / capabilities | Implementation |
|---|---|---|---|---|
| [core-00](lessons/core-00.md) | Separate host readiness, local runs, and course completion. | — | macos-arm64, linux-x86_64; python-3.12 | `implemented` |
| [core-01](lessons/core-01.md) | Measure pendulum state and numerical energy drift. | core-00 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-02](lessons/core-02.md) | Verify immutable source revisions and model bytes. | core-00 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-03](lessons/core-03.md) | Load six robot models and inspect their actual dimensions. | core-01, core-02 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-04](lessons/core-04.md) | Render the actual FR3 scene and inspect the camera result. | core-03 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-teleop-01](lessons/core-teleop-01.md) | Learn a bimanual data contract without buying a headset. | core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-01](lessons/core-fr3-01.md) | Map FR3 joints, bodies, actuators and the tool site. | core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-02](lessons/core-fr3-02.md) | Apply bounded joint PD torque on the FR3 dynamics. | core-fr3-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-03](lessons/core-fr3-03.md) | Measure how gravity feedforward changes tracking error. | core-fr3-02 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-04](lessons/core-fr3-04.md) | Check a geometric Jacobian and solve a small IK displacement. | core-fr3-03 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-05](lessons/core-fr3-05.md) | Control a world-frame tool position using operational inertia. | core-fr3-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-06](lessons/core-fr3-06.md) | Measure probe/table contact force and vary friction. | core-fr3-05 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-rl-01](lessons/core-rl-01.md) | Follow a complete minimal continuous-action PPO update. | core-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-07](lessons/core-fr3-07.md) | Use reset, observation, action, reward and episode boundaries for FR3 reach. | core-fr3-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-08](lessons/core-fr3-08.md) | Train, save and reload PPO on the actual FR3 reach environment. | core-fr3-07, core-rl-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-01](lessons/core-enlight-01.md) | Build Enlight-L frames from the public vendor parameters. | core-02 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-02](lessons/core-enlight-02.md) | Compare independent vendor forward kinematics against compiled MJCF. | core-enlight-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-wuji-01](lessons/core-wuji-01.md) | Create bounded open, half and closed poses using a hand synergy. | core-02, core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-wuji-02](lessons/core-wuji-02.md) | Read virtual contact forces at a Wuji fingertip. | core-wuji-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-dexterity-01](lessons/core-dexterity-01.md) | Compare Wuji and Sharpa using measured model properties. | core-wuji-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-data-01](lessons/core-data-01.md) | Record real MuJoCo state/action/next-state transitions. | core-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-dexterity-02](lessons/core-dexterity-02.md) | Retarget observed fingertip displacement and record the result. | core-dexterity-01, core-data-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-g1-01](lessons/core-g1-01.md) | Record and replay a bounded G1 joint-motion cycle. | core-03, core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-il-01](lessons/core-il-01.md) | Fit behavioral cloning to the completed episode dataset. | core-data-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-aloha-01](lessons/core-aloha-01.md) | Run the dual-arm ALOHA model and build an ACT-shaped batch. | core-data-01, core-il-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-vla-01](lessons/core-vla-01.md) | Round-trip the explicitly mocked VLA protocol without a device. | core-data-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-ros-01](lessons/sim-ros-01.md) | Exchange real ROS topics, service calls, actions and TF in an isolated domain. | core-00, core-02 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-ros-02](lessons/sim-ros-02.md) | Bridge measured MuJoCo state into ROS JointState messages. | core-04, sim-ros-01 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-ros-03](lessons/sim-ros-03.md) | Record actual ROS messages and replay a rosbag2 database. | sim-ros-02 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-ros-04](lessons/sim-ros-04.md) | Inspect a common reset/observe/act/close interface over simulation and ROS. | sim-ros-02 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-g1-01](lessons/sim-g1-01.md) | Train a G1 motion-imitation PPO task and evaluate its saved checkpoint. | core-g1-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-wuji-01](lessons/sim-wuji-01.md) | Train and evaluate the pinned Wuji MJLab reorientation task. | core-wuji-02, core-rl-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-vla-01](lessons/sim-vla-01.md) | Fine-tune prepared SmolVLA weights on real local data and serve inference. | core-vla-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-vla-02](lessons/sim-vla-02.md) | Validate an explicitly configured optional remote policy response. | sim-vla-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-isaac-01](lessons/sim-isaac-01.md) | Import the pinned public Wuji URDF into an actual Isaac articulation. | core-04 | ubuntu-24.04-x86_64; isaac-sim | `implemented` |
| [sim-isaac-02](lessons/sim-isaac-02.md) | Measure RGB and depth observations while changing light intensity. | sim-isaac-01 | ubuntu-24.04-x86_64; isaac-sim | `implemented` |
| [sim-cross-01](lessons/sim-cross-01.md) | Compare two actual engines using matched initial state and the same applied effort. | core-fr3-08, sim-isaac-01 | ubuntu-24.04-x86_64; isaac-sim | `implemented` |
| [sim-deploy-01](lessons/sim-deploy-01.md) | Packaging preserves the meaning of learned numbers across a process boundary. | core-fr3-08 | macos-arm64, linux-x86_64; python-3.12 | `implemented` |
| [sim-enlight-01](lessons/sim-enlight-01.md) | Fake hardware separates communication from physical authority. | core-enlight-01, sim-ros-01 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-enlight-02](lessons/sim-enlight-02.md) | This candidate is a known controller, not a learned policy. | core-enlight-02, sim-deploy-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-wuji-02](lessons/sim-wuji-02.md) | The dexterity candidate consumes an actual completed `sim-wuji-01` checkpoint, loads it into the same pinned registered vendor task in play mode, evaluates it, then copies exact policy bytes. | sim-wuji-01, sim-deploy-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [hw-common-01](lessons/hw-common-01.md) | An inference sink exercises a policy while making the output boundary visible. | sim-deploy-01 | macos-arm64, linux-x86_64; python-3.12 | `implemented` |
| [hw-common-02](lessons/hw-common-02.md) | A read-only snapshot answers whether observed state is coherent, fresh and disabled. | hw-common-01 | ubuntu-24.04-x86_64; robot-runtime, isolated-network | `scaffolded` |
| [hw-fr3-01](lessons/hw-fr3-01.md) | FR3 simulation and offline replay establish software behavior; read-only device state must separately confirm the real arm's joint order, signs, units and stop boundary. | hw-common-02, core-fr3-06 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, fr3-hardware, read-only-preflight-fr3 | `scaffolded` |
| [hw-wuji-01](lessons/hw-wuji-01.md) | A real tactile stream needs sensor identity and calibration, not only contact-shaped numbers. | hw-common-02, core-wuji-02 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, wuji-hardware, read-only-preflight-wuji | `scaffolded` |
| [hw-wuji-02](lessons/hw-wuji-02.md) | A dexterity checkpoint evaluated on a vendor simulation task is a candidate. | hw-wuji-01, sim-wuji-02 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, wuji-hardware, read-only-preflight-wuji | `scaffolded` |
| [hw-enlight-01](lessons/hw-enlight-01.md) | Read-only Enlight readiness starts from the physical controller identity, not an MJCF model label. | hw-common-02, sim-enlight-01 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-02](lessons/hw-enlight-02.md) | System identification asks which model parameters explain measured motion and effort. | hw-enlight-01, core-enlight-02 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-03](lessons/hw-enlight-03.md) | Contact-task shadow compares a candidate's interpretation with read-only device observations while retaining no actuation authority. | hw-enlight-01, sim-enlight-02 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-wuji-01](lessons/hw-enlight-wuji-01.md) | Combining arm and hand adds synchronization and stop-boundary questions; two independent green badges do not establish an integrated system. | hw-enlight-01, hw-wuji-01 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight, wuji-hardware, read-only-preflight-wuji | `scaffolded` |
| [core-fr3-09](lessons/core-fr3-09.md) | A joint-space trajectory and a Cartesian trajectory ask different questions. | core-fr3-06 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-10](lessons/core-fr3-10.md) | Behavioral cloning learns FR3's observation-to-action mapping from demonstrations generated on its own MuJoCo environment. | core-fr3-09 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-fr3-01](lessons/sim-fr3-01.md) | A joint-space trajectory and a Cartesian trajectory ask different questions. | core-fr3-09 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-fr3-02](lessons/sim-fr3-02.md) | Behavioral cloning learns FR3's observation-to-action mapping from demonstrations generated on its own PhysX environment. | sim-fr3-01, core-fr3-10 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-fr3-03](lessons/sim-fr3-03.md) | PPO adjusts a FR3 policy using actual PhysX rollouts, not prerecorded reward numbers. | sim-fr3-02, core-fr3-08 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-fr3-04](lessons/sim-fr3-04.md) | Match target arrays, initial pose, world frame and control period in two completed runs. Compare TCP error RMS difference, joint errors and measured contact forces. Investigate import, drive and engine differences without inferring hardware safety. | sim-fr3-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-03](lessons/core-enlight-03.md) | A joint-space trajectory and a Cartesian trajectory ask different questions. | core-enlight-02 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-04](lessons/core-enlight-04.md) | Behavioral cloning learns Enlight's observation-to-action mapping from demonstrations generated on its own MuJoCo environment. | core-enlight-03 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-05](lessons/core-enlight-05.md) | PPO adjusts a Enlight policy using actual MuJoCo rollouts, not prerecorded reward numbers. | core-enlight-04, core-rl-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-enlight-03](lessons/sim-enlight-03.md) | A joint-space trajectory and a Cartesian trajectory ask different questions. | core-enlight-03 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-enlight-04](lessons/sim-enlight-04.md) | Behavioral cloning learns Enlight's observation-to-action mapping from demonstrations generated on its own PhysX environment. | sim-enlight-03, core-enlight-04 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-enlight-05](lessons/sim-enlight-05.md) | PPO adjusts a Enlight policy using actual PhysX rollouts, not prerecorded reward numbers. | sim-enlight-04, core-enlight-05 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [core-shadow-01](lessons/core-shadow-01.md) | The introduction holds the wrist, exercises one finger, then closes/opens a shared finger synergy. | core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-shadow-01](lessons/sim-shadow-01.md) | The PhysX introduction must preserve Shadow named joints, drive semantics, coupling and real object contacts after import. | core-shadow-01 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [core-stretch3-01](lessons/core-stretch3-01.md) | A mobile manipulator can use both base and arm to reduce tool error. | core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-stretch3-01](lessons/sim-stretch3-01.md) | After PhysX import, Stretch must retain a free base and named wheel, lift and telescoping-joint controls. | core-stretch3-01 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [hw-enlight-04](lessons/hw-enlight-04.md) | An exact-action card binds one reviewed device and one action to fresh state, limits and a single-use approval. | hw-enlight-02, sim-enlight-05 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-05](lessons/hw-enlight-05.md) | Review probe TCP, payload, force limits and plane calibration. A separately validated force controller is required; policy torque is not sent directly to hardware. | hw-enlight-04 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-06](lessons/hw-enlight-06.md) | Pick-transfer-place needs a width-based gripper contract, verified mount/tool/payload and task-specific stop/recovery behavior. | hw-enlight-04 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [sim-teleop-01](lessons/sim-teleop-01.md) | Read-only input acceptance needs actual Quest, MANUS and VIVE identities, firmware/SDK compatibility, calibration and simultaneous stream measurements. | core-teleop-01 | linux-x86_64; python-3.12, numpy, mujoco | `scaffolded` |
| [sim-teleop-02](lessons/sim-teleop-02.md) | Spatial alignment is an explicit transform chain, not a pose-array copy. | core-teleop-01 | linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-enlight-06](lessons/sim-enlight-06.md) | Collection closes a data loop in simulation: synthetic wrist pose → Enlight-only IK → bounded arm action → camera/state/target episode → model-bound BC input. | core-enlight-05, sim-teleop-02 | linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
<!-- pal:goals:end -->
