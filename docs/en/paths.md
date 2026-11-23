<!-- pal:language:start -->
<p align="right">
  <a href="../ko/paths.md" lang="ko">한국어</a> | <a href="paths.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Robot learning paths

Choose a path by pasting one prompt into Codex or Claude Code after initial setup:

```text
Run the manipulator tutorial, one eligible lesson at a time, preserving my progress.
```

For the other paths, say “Run the dexterous-hand tutorial” or “Run the mobile-manipulator tutorial.” The agent reads the path and saved state, handles its reference commands below, and stops after one lesson. You do not need to type the `pal` commands yourself.

The append-only catalog preserves the original IDs and aliases. `curriculum/paths.json` defines three independent routes. A selected path includes all required stages: `--through` and elective filters continue to work for the legacy course without a path.

| Path | Start | Required progression | Follow-up |
|---|---|---|---|
| manipulator | FR3 | MuJoCo joint/TCP control → PhysX → PPO/BC → measured engine comparison → separately trained Enlight → device readiness | Probe plane force and gripper pick/transfer/place, each with separate tool review |
| dexterous-hand | Shadow Hand | MuJoCo joints/synergies/contact → PhysX | Wuji Hand 2 Beta 2, then Enlight integration |
| mobile-manipulator | Stretch 3 | MuJoCo base/arm/combined movement → PhysX | Private Friday provider; public groups remain base/arm/gripper |

```bash
pal course paths --json
pal course init --path manipulator --json
pal course next --json
pal course summary --json
pal course pause --json
pal course resume --json
pal lesson run core-fr3-09 --resume-from BASE --json
```

Say “매니퓰레이터 튜토리얼 실행해줘” or “Run the manipulator tutorial.” The agent selects this path while preserving completion history, inspects saved state, opens the current GitHub lesson in your selected language, runs one baseline and one comparison, explains the numerical results, checks and saves the review, then stops. Ask to continue for the next lesson. An unavailable required Isaac lesson blocks the path and reports the required host; it never completes the course by skipping it.

Pause preserves the explanation, run, parameters and comparison. Resume first reports the saved phase and next action; it sends no robot command. A short interrupted simulation restarts in a fresh directory. Saved complete artifacts can still be reviewed. Feedback and personal progress integration keep their existing boundaries.

## Training and host transfer

Run long learning separately from a short lesson. Start on the model you will evaluate; an FR3 policy is never an Enlight candidate. The bounded position-delta policy is for simulation. Contact control needs a separately validated controller.

```bash
pal train run --model fr3 --algorithm bc --epochs 64 --output-dir .local/train/fr3-bc --json
pal train run --model fr3 --algorithm bc --epochs 128 --resume-from .local/train/fr3-bc --output-dir .local/train/fr3-bc-resumed --json
pal train export --source .local/train/fr3-bc-resumed --destination .local/fr3-training.json --json
# Copy only this export to the other host, then:
pal train import --source .local/fr3-training.json --destination .local/imported-fr3 --json
```

Use `--algorithm ppo` for real arm rollouts. Checkpoints are atomic at epoch/update boundaries and include model, optimizer, fixed normalization, RNG and progress. SIGINT/SIGTERM request a stop at the next boundary. Forced termination preserves earlier checkpoints; directory resume chooses the newest intact checkpoint. Resume rejects changed source, model, data, engine, environment lock, seed or learning rate. Increasing the total epoch count is supported. Transfer includes only the training checkpoint and demonstration data with hashes; host/device settings and hardware approval receipts are excluded. Exact software lock and source must match on the target host. A training export supplies no personal completion or device authority.

BC splits complete episodes 20/5/5 for train/validation/test. A separate twenty-target rollout measures policy performance. At least sixteen targets must remain within 10 mm for ten consecutive control steps. Inspect `evaluation.json` even when optimizer checks pass. This gate is not a hardware tolerance. Short BC/PPO runs may fail it.

## Models, gripper and device gates

The FR3 source pin stays unchanged. Shadow Hand, Stretch 3 and Robotiq 2F-85 use a separate Menagerie commit with per-file hashes and model licenses. Isaac imports that pinned source into derived USD under the run directory and uses PhysX. Model import, joint names, actuator/coupling behavior, free base, contact, observations and rendering all require GPU verification. Missing coupling parity fails closed. No MuJoCo stepping substitutes for PhysX validation.

Robotiq 2F-85 is the gripper simulation baseline. The [manufacturer's Isaac assets](https://github.com/robotiq/isaacsim_assets) have a separate source manifest. Select the PhysX variant; Newton/MuJoCo-Warp is not an independent-engine comparison. A replacement gripper requires reusable model licensing, collision/inertia, mimic/closed-loop and width conversion, documented status/timeout/stop API, mounting, power, communications and payload compatibility. The public `Gripper` protocol isolates these properties. No purchase is included.

Enlight retains RDK 2.1 / v3E.1 as the hardware baseline. The public description's v4 compatibility remains unverified. Review Elements, then offline replay, command sink, read-only, live shadow and torque-disabled replay before a fresh exact-action card. Hardware lesson commands stay blocked. The injected run-card executor provides no vendor connection or enable API. A site adapter must separately validate watchdog, timeout, stop, identity, limits and tool/payload. Probe and gripper stages remain blocked without those tools and reviews. Read [hardware safety](../07_SAFETY.md).

On an installed Isaac host, use `pal train run --engine physx --model fr3 --algorithm bc --epochs 64 --output-dir .local/train/physx-fr3 --json`. Resume checkpoints only on the same engine. See [environment verification](../verification/robot-paths-2026-11-08.md).

## How to read a path

The five common foundations teach reproducibility, models, state and rendering. The manipulator route builds from joints/frames into control, learning and independent evaluation. The hand route connects joints/synergies to contact. The mobile route composes base and arm coordinates. Check prerequisite lessons and return to the relevant [concept chapter](index.md#eleven-common-concept-chapters) when a new idea appears.

Move from Mac to a capable WS at the first required PhysX, ROS or GPU lesson. Required Isaac work cannot be skipped to finish a path. Physical stages require separate tool/payload/safety review and fresh per-run approval. Read [equipment guidance](equipment.md) first.

Below is the required order from `curriculum/paths.json`, which can differ from global catalog order. Ask `pal course next --json` for actual selection.

### manipulator

[core-00](lessons/core-00.md) → [core-01](lessons/core-01.md) → [core-02](lessons/core-02.md) → [core-03](lessons/core-03.md) → [core-04](lessons/core-04.md) → [core-fr3-01](lessons/core-fr3-01.md) → [core-fr3-02](lessons/core-fr3-02.md) → [core-fr3-03](lessons/core-fr3-03.md) → [core-fr3-04](lessons/core-fr3-04.md) → [core-fr3-05](lessons/core-fr3-05.md) → [core-fr3-06](lessons/core-fr3-06.md) → [core-fr3-09](lessons/core-fr3-09.md) → [sim-fr3-01](lessons/sim-fr3-01.md) → [core-rl-01](lessons/core-rl-01.md) → [core-fr3-07](lessons/core-fr3-07.md) → [core-fr3-08](lessons/core-fr3-08.md) → [core-fr3-10](lessons/core-fr3-10.md) → [sim-fr3-02](lessons/sim-fr3-02.md) → [sim-fr3-03](lessons/sim-fr3-03.md) → [sim-fr3-04](lessons/sim-fr3-04.md) → [core-enlight-01](lessons/core-enlight-01.md) → [core-enlight-02](lessons/core-enlight-02.md) → [core-enlight-03](lessons/core-enlight-03.md) → [core-enlight-04](lessons/core-enlight-04.md) → [core-enlight-05](lessons/core-enlight-05.md) → [sim-enlight-03](lessons/sim-enlight-03.md) → [sim-enlight-04](lessons/sim-enlight-04.md) → [sim-enlight-05](lessons/sim-enlight-05.md) → [sim-deploy-01](lessons/sim-deploy-01.md) → [hw-common-01](lessons/hw-common-01.md) → [hw-common-02](lessons/hw-common-02.md) → [sim-ros-01](lessons/sim-ros-01.md) → [sim-enlight-01](lessons/sim-enlight-01.md) → [hw-enlight-01](lessons/hw-enlight-01.md) → [hw-enlight-02](lessons/hw-enlight-02.md) → [hw-enlight-04](lessons/hw-enlight-04.md) → [hw-enlight-05](lessons/hw-enlight-05.md) → [hw-enlight-06](lessons/hw-enlight-06.md)

### dexterous-hand

[core-00](lessons/core-00.md) → [core-01](lessons/core-01.md) → [core-02](lessons/core-02.md) → [core-03](lessons/core-03.md) → [core-04](lessons/core-04.md) → [core-shadow-01](lessons/core-shadow-01.md) → [sim-shadow-01](lessons/sim-shadow-01.md)

### mobile-manipulator

[core-00](lessons/core-00.md) → [core-01](lessons/core-01.md) → [core-02](lessons/core-02.md) → [core-03](lessons/core-03.md) → [core-04](lessons/core-04.md) → [core-stretch3-01](lessons/core-stretch3-01.md) → [sim-stretch3-01](lessons/sim-stretch3-01.md)


## Progress from minimal equipment

Follow [laptop → GPU → optional collection equipment → real robots last](equipment-stages.md). The [NVIDIA experience workbook](nvidia-ecosystem.md) connects Isaac Sim, Lab, Teleop/Capture, GR00T and ROS/deployment through exercises and evidence. Consider XR, a gripper or UMI only for the later tasks that need them.
