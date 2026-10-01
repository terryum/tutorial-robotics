# Host Rollout

Use the [remote robotics development guide](en/setup/remote-development/index.md)
([한국어](ko/setup/remote-development/index.md)) for per-machine execution prompts,
incremental installation and recovery. Existing installation reports are history;
inspect each host before deciding what is missing. Hosts can start independently.

## MacBook

Preserve the existing Python 3.12 Core environment and add SSH/VS Code client
tools only as needed. Local Core learning remains available; keep global Python
unchanged. Installation does not run or complete lessons automatically.

## WS1 and WS2 — DEVELOPMENT

Use Ubuntu 24.04 and ROS 2 Jazzy for the verified robotics stack. Keep Isaac,
MuJoCo/MJX, ROS 2, LeRobot, and VLA environments separate. Reuse each host's
installed stacks and locks. Both WS1 and WS2 may develop/train with verified
capabilities; a MacBook run is not a prerequisite. Synthetic GPU smoke is not
Isaac/ROS acceptance or learned-policy validation.

## WS1 or WS2 — ROBOT_RUNTIME

Use the exact promoted source commit and bundle. Do not run training concurrently.
Verify offline replay and read-only state before any hardware-specific operation;
network and physical-action approvals remain separate from remote access.

Partitioning, bootloader, NVIDIA driver, Secure Boot, and filesystem changes
always require a separately reviewed phase and rollback plan.
