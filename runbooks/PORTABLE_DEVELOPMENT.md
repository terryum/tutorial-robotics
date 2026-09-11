> Current execution authority: [common workflow](../agent/workflow.md). Learner state is ignored `.local/`; historical host reports below never complete lessons or require automatic commits.

# Runbook — Portable Development on MacBook

MacBook is not a mandatory first phase. It is a portable `DEVELOPMENT` host.

## Typical capabilities

- MuJoCo local/offscreen
- robotics math and control
- small Gym/PPO/BC/ACT
- LeRobot dataset work and small VLA smoke
- optional RoboStack ROS 2
- Git/Codex/Jupyter and remote cockpit

## Selection rule

Run any pending tutorial whose `requires` are satisfied. CUDA, Isaac Sim, native Ubuntu vendor driver and large mjlab jobs are simply not local candidates.

## Continue command

```text
현재 MacBook capability로 실행 가능한 다음 eligible tutorial 하나만 실행해. GPU/Isaac/native-vendor tutorial의 shared status는 바꾸지 말고, completed code를 재사용해 test·visualization·한국어 report까지 완료해.
```

## Optional Mac-only checks

`setup/12_MACOS_PORTABILITY_CHECK.md` may be run to verify arm64, MPS, RoboStack, SSH/WebRTC and memory-constrained operation. It is not a curriculum gate.
