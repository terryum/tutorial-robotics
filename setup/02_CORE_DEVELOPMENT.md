# Core Development Environment

Create a semantic `core-dev` environment on either macOS arm64 or Ubuntu x86_64.

Contents:

- Python 3.12 where supported
- MuJoCo, NumPy, SciPy, Gymnasium
- JAX/MJX when supported
- PyTorch CPU/MPS/CUDA appropriate to the host
- pytest, ruff, mypy

Rules:

- never modify system Python
- keep OS/architecture-specific lock output but one shared environment purpose
- do not hard-code home paths
- run the same deterministic smoke vectors on MacBook and WS2 when both are used

## Minimal Ubuntu installation

Follow [Ubuntu offline setup](13_UBUNTU_OFFLINE.md). Install the existing lock without the `learning` extra first. PyTorch, JAX/MJX, CUDA and Isaac are later, separately verified environment roles.
