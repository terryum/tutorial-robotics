# Host Audit

This step is read-only and runs after the logical host/profile has been explicitly registered through `$bootstrap-machine`.

## Detect

- logical host ID and profile from `.local/HOST_PROFILE.md`
- OS version, kernel and architecture
- hostname and shell; Rosetta status on macOS
- CPU, memory and free disk
- Python, Git, compiler and CMake
- display session and GUI capability
- actual NVIDIA device, driver and CUDA on Linux
- existing uv, pixi, conda, ROS and Docker
- network interfaces and routes without storing secrets
- restrictions, proxy and filesystem characteristics

## Required local output

Create:

```text
.local/HOST_PROFILE.md
.local/CAPABILITIES.md
.local/ENVIRONMENTS.md
.local/MODELS.md
.local/NETWORK.md
```

Capability summary:

```text
logical_host: MACBOOK | WS2 | WS1
profile: MACBOOK_FOUNDATION | WS2_SIM_TRAIN | WS2_ROBOT_INTEGRATION | WS1_ROBOT_RUNTIME
mujoco_local: yes/no
ros2_local: yes/no
lerobot_local: yes/no
isaac_local: yes/no
nvidia_training: yes/no
real_robot_runtime: yes/no
interactive_gui: yes/no
```

Also save a non-secret JSON/Markdown snapshot under `outputs/T00/<run-id>/` and update shared `state/ENVIRONMENTS.md` only with validated version summaries.

Do not infer an NVIDIA GPU from an installed CUDA package. Query the actual device. Do not infer WS1 versus WS2 from matching workstation specifications.
