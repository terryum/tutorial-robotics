# Wuji Hand 2 Motion Baselines

Public simulation baselines for the left and right Wuji Hand 2 Beta 1 models.
The repository includes deterministic gestures, a 20-DoF joint-reaching PPO
lesson, and a contact-based cube yaw-reorientation PPO lesson.

```bash
git submodule update --init --recursive
uv sync --group dev
uv run pytest
```

## Gestures

```bash
uv run mjpython -m wuji_hand2_motion.scripts.replay_gestures \
  --side right --sequence open,relaxed,fist,pinch,point,spread
```

The six semantic poses are connected with 1.5-second, 50 Hz minimum-jerk
transitions and validated against the pinned model limits.

## Joint reach PPO

```bash
uv run python -m wuji_hand2_motion.scripts.train \
  --task joint-reach --side right --timesteps 20000
uv run mjpython -m wuji_hand2_motion.scripts.replay \
  --task joint-reach --side right
```

## Cube yaw PPO

```bash
uv run python -m wuji_hand2_motion.scripts.train \
  --task cube-yaw --side right --timesteps 500000
uv run mjpython -m wuji_hand2_motion.scripts.replay \
  --task cube-yaw --side right
```

The cube task uses a runtime-generated MuJoCo scene: a 40 mm, 50 g primitive
cube is placed in a nominal pre-grasp and rotated about the palm-normal axis.
It is intentionally smaller than the official first-generation Wuji MJLab
full-SO(3) task and has no hardware deployment path.

## Safety and fidelity

The official Hand 2 actuator gains are preliminary, and the fingertip soft
pads are not attached to collision geometry. These baselines establish
software, observation/action, contact, training, and evaluation contracts;
they do not establish physical-force accuracy or safe real-hand behavior.
