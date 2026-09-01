# Mac Core Environment

## Scope

MuJoCo, numerical robotics, plotting, Gymnasium, tests, and small RL experiments.

## Rules

- native Apple Silicon shell only; do not use Rosetta Python
- use a project-local environment and lock file
- prefer an existing `uv`; otherwise install it only with user-visible approval under Codex sandbox rules
- start with Python 3.12
- start with MuJoCo 3.12.x and record the exact resolved version
- use `mujoco.Renderer` for offscreen rendering and the native viewer for interactive inspection

## Initial dependencies

- mujoco
- numpy
- scipy
- matplotlib
- imageio and an MP4 encoder path
- gymnasium
- typer
- pydantic or dataclasses-based schemas
- pyyaml
- pytest, ruff, mypy

LeRobot and ROS 2 are deliberately excluded from this environment.

## Acceptance

- Python reports arm64
- `import mujoco` succeeds
- a minimal XML compiles
- one RGB frame is rendered to disk
- an interactive viewer command is provided and, when GUI access exists, launched
