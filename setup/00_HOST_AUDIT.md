# Host Capability Audit

This is read-only before installation or execution.

## Detect

- logical host label supplied by the user: MacBook, WS2, WS1, or other
- execution mode: `DEVELOPMENT` or `ROBOT_RUNTIME`
- OS, version, kernel, architecture and hostname
- CPU, memory, free disk and display/offscreen support
- Python, Git, compiler, CMake, uv/Pixi/Conda
- actual NVIDIA GPU, driver and CUDA; never infer from packages alone
- ROS 2 support and installed distro/RMW
- Isaac Sim/Lab support
- network interfaces/routes without storing secrets
- connected robot identity only in runtime mode

## Required local files

```text
.local/HOST_CAPABILITIES.md
.local/ENVIRONMENTS.md
.local/MODELS.md
.local/NETWORK.md
```

Example capability keys:

```text
mode: DEVELOPMENT | ROBOT_RUNTIME
dev_core: yes/no
internet: yes/no
mujoco_supported: yes/no
rendering_supported: yes/no
small_ml_supported: yes/no
lerobot_supported: yes/no
ros2_core_supported: yes/no
ubuntu_24_04_x86_64: yes/no
ros2_jazzy_native: yes/no
nvidia_cuda: yes/no
mjlab_supported: yes/no
lerobot_gpu_supported: yes/no
policy_gpu_supported: yes/no
isaac_sim_supported: yes/no
robot_runtime_supported: yes/no
isolated_robot_network: yes/no
wuji_hardware: yes/no
public_robot_hardware: yes/no
```

Capability means supported or safely provisionable on this host under the environment plan. Actual environment readiness is recorded separately. Do not infer WS1 versus WS2 from similar hardware.
