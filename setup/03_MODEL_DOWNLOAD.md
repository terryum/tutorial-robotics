# Model Download and Pinning

## Directory

Clone external repositories under `external/`. Do not copy only one XML if it relies on relative meshes.

## Required sources

- `wuji-technology/wuji-hand-description`
- `google-deepmind/mujoco_menagerie`
- `unitreerobotics/unitree_mujoco`
- `unitreerobotics/unitree_rl_mjlab`
- `unitreerobotics/unitree_rl_lab`
- `sharpa-robotics/sharpa-urdf-usd-xml`
- `huggingface/lerobot` only when entering LeRobot setup

Additional Wuji/Sharpa examples are downloaded only when the relevant tutorial begins.

## Pinning workflow

1. Clone or fetch the official repository.
2. Record default/selected branch.
3. Resolve current commit SHA.
4. Inspect license.
5. Discover expected model file paths.
6. Run a minimal compile/load test.
7. Write the result to machine-readable registry and `state/MODELS.md`.

Do not recursively clone every large model repository unless its submodules are required. Use `git submodule update --init --recursive` only for repos that declare them.
