# LeRobot Environment

## Scope

Dataset creation/visualization, behavioral cloning, ACT, ALOHA simulation, and lightweight VLA experiments.

## Separation

Use a separate Python 3.12 environment. Do not install LeRobot into `mac-core` or ROS 2.

## Installation policy

- pin a release or commit after reading the current official installation guide
- install only required extras: dataset/viz/training, then `aloha`, then `smolvla` when needed
- record PyTorch, torchvision, device, and video codec versions
- always test a tiny deterministic CPU inference
- on Apple Silicon, additionally test MPS and keep CPU fallback for unsupported or inconsistent operators
- on an NVIDIA host, additionally test CUDA and record GPU/VRAM/package versions

## Host expectations

MacBook is appropriate for dataset inspection, small BC/ACT smoke tests, and policy-client code. A CUDA host such as WS2 can perform all of those tasks and also scale training. Device-specific results must be stored under distinct run IDs.
