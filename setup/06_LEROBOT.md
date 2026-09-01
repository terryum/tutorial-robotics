# LeRobot Environment

## Scope

Dataset creation/visualization, behavioral cloning, ACT, ALOHA simulation, and lightweight VLA experiments.

## Separation

Use a separate Python 3.12 environment. Do not install LeRobot into `mac-core` or ROS 2.

## Installation policy

- pin a release or commit after reading the current official installation guide
- install only required extras: dataset/viz/training, then `aloha`, then `smolvla` when needed
- record PyTorch, torchvision, device, and video codec versions
- test both CPU and MPS execution for a tiny deterministic inference
- use CPU fallback when MPS produces unsupported operators or inconsistent results

## Mac expectations

The Mac is appropriate for dataset inspection, small BC/ACT smoke tests, and policy-client code. Large training belongs on the NVIDIA workstation.
