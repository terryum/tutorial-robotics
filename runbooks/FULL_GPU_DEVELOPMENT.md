> Current execution authority: [common workflow](../agent/workflow.md). Learner state is ignored `.local/`; historical host reports below never complete lessons or require automatic commits.

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

## Safety boundary

No real robot command in development mode. To attach hardware, stop all training/Isaac/policy-server batch work and switch through `runbooks/ROBOT_RUNTIME.md`.
