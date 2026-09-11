# Host Rollout

## MacBook

Create the Python 3.12 environment, run the doctor and foundation tutorials,
and record learner progress only under ignored `.local/`. Keep global Python unchanged.

## WS2

Use Ubuntu 24.04 and ROS 2 Jazzy for the verified robotics stack. Keep Isaac,
MuJoCo/MJX, ROS 2, LeRobot, and VLA environments separate. Reuse the verified
MacBook commit and produce checksummed deployment candidates.

## WS1

Use the exact promoted source commit and bundle. Verify offline replay and
read-only state before any hardware-specific operation.

Partitioning, bootloader, NVIDIA driver, Secure Boot, and filesystem changes
always require a separately reviewed phase and rollback plan.

