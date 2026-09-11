> Current execution authority: [common workflow](../agent/workflow.md). Learner state is ignored `.local/`; historical host reports below never complete lessons or require automatic commits.

# Runbook — WS2 Simulation and Training

## 역할

WS2 is the primary GPU research machine. Use Ubuntu 24.04.x/Jazzy-compatible cells for vendor stacks and separate locked environments for Isaac, mjlab and LeRobot/VLA.

## First command

## Sequence

```text
T26  G1 staged PPO/motion imitation
T27  Wuji in-hand PPO
 ACT scale-up
T32C SmolVLA fine-tuning/server
T32D optional π₀/GR00T inference
T33  Isaac asset import
T34  synthetic camera data
T35  MuJoCo–Isaac validation
T35A generic deployment bundle
//T42A target-specific manufacturing candidates
```

## Repetition

```text
현재 profile은 WS2_SIM_TRAIN이다. 다음 eligible WS2 tutorial 하나만 실행해줘. vendor-compatible/modern Isaac/mjlab/LeRobot 환경을 분리하고 GPU·VRAM·throughput·locks·outputs·report·state를 기록해. 실물 command는 금지해.
```

## Promotion

T35A never packages only a checkpoint. It includes processor/config, normalization, camera/joint/state/action order, units/rates/horizon, asset/calibration revisions, dataset manifest, source commit, environment lock/container digest, test vectors, tolerance and rollback.

## Hardware-mode transition

Before connecting a robot, stop every training/Isaac batch process, deactivate ML environments, verify a dedicated wired NIC and switch to `WS2_ROBOT_INTEGRATION`. Do not automatically start hardware commands.
