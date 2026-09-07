# Runbook — Full GPU Development Host

WS2 normally uses this runbook in `DEVELOPMENT` mode. It is a superset of portable development.

## Typical capabilities

- every core MuJoCo/control/data tutorial
- native Ubuntu 24.04 + ROS 2 Jazzy vendor simulation
- NVIDIA CUDA
- MuJoCo Warp/mjlab
- Isaac Sim/Lab vendor and modern stacks
- ACT/SmolVLA/π₀/GR00T experiments
- synthetic data and candidate bundle creation

## First command

```text
이 컴퓨터는 full GPU DEVELOPMENT host다. git pull 이후 state/HOST_STATUS.md와 state/PROGRESS.md를 읽고 $bootstrap-host로 capability를 등록해. shared progress에서 다음 eligible tutorial 하나를 실행하되 core tutorial도 생략하지 말고 deterministic baseline 후 GPU scale-up을 분리해 기록해. 결과를 push할 때 이 OS layer의 host 행도 같은 commit에서 갱신해.
```

## Safety boundary

No real robot command in development mode. To attach hardware, stop all training/Isaac/policy-server batch work and switch through `runbooks/ROBOT_RUNTIME.md`.
