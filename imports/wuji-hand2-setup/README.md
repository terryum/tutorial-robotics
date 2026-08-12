# Wuji Hand 2 Setup

Public, simulation-only setup for the Wuji Hand 2 Beta 1 model in MuJoCo and
ROS 2 Jazzy. Both left and right hands use the native position actuators from
the official model. No physical-hand connection is included.

## MuJoCo

```bash
git submodule update --init --recursive
uv sync --group dev
uv run wuji-hand2-inspect --side right
uv run mjpython sim/scripts/joint_sweep.py --side right
uv run pytest
```

The official model is pinned at `wuji-description` v2026.8.3. It is loaded
directly; vendor files are never rewritten or copied into generated history.

## ROS 2

```bash
cd ros2_ws
pixi install
pixi run build
pixi run test-backend
pixi run mujoco-right
```

In another terminal, run `pixi run command-right` or
`pixi run mujoco-rviz-right`. Left-hand tasks use the corresponding `left`
name. `pixi run dual-mujoco` starts both simulation nodes.

The simulation interfaces intentionally match the Wuji ROS convention:

- `/left_hand/joint_commands`, `/right_hand/joint_commands`
- `/left_hand/joint_states`, `/right_hand/joint_states`
- `/left_hand/mujoco_reset`, `/right_hand/mujoco_reset`

Commands and states use `sensor_msgs/msg/JointState` with the 20 anatomical
joint names from the pinned model.

## Limits

Wuji Hand 2 remains a Beta prototype. The published actuator gains are
preliminary, and the fingertip soft pads are not attached to the collision
model. This repository is suitable for model, ROS, control-interface, and
learning experiments, not for validating real contact forces or hardware
safety.
