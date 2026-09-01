# Machine Sequence

## MacBook foundation

Use MuJoCo, public model inspection, control, ROS 2 concepts, small RL/IL,
dataset tooling, and deterministic visualization. Do not attempt workstation-
only Isaac or large training jobs.

## WS2 simulation and training

Continue from the verified MacBook commit. Use isolated environments for ROS 2,
MuJoCo/MJX, Isaac, LeRobot/ACT, and VLA work. Produce checksummed candidate
bundles; do not send hardware commands from a training environment.

## WS1 runtime

Consume only a verified candidate bundle. Begin with offline replay, command
sink dry-run, read-only connection, and live no-command shadow. Motion remains
gated by the run-specific safety contract.

Machine-local identity, paths, GPUs, robot networks, and credentials belong in
`.local/` and are never committed.
