# CUDA GPU Development Stacks

A GPU-capable WS1 or WS2 in DEVELOPMENT must use separate locked environments.
Inspect and reuse installed stacks before adding anything. Follow the
[Ubuntu remote development guide](../docs/en/setup/remote-development/ubuntu.md)
for incremental setup and synthetic GPU/checkpoint verification; that smoke test
does not validate the robotics stacks below or complete their lessons.

```text
gpu-mjlab
├─ MuJoCo Warp / mjlab / rsl-rl
├─ Unitree G1 PPO
└─ Wuji in-hand PPO

gpu-isaac-vendor
├─ vendor-tested Isaac Sim/Lab pair
└─ Unitree/Sharpa/Wuji reproduction

gpu-isaac-modern
├─ current custom Isaac stack
└─ custom public-robot USD and synthetic data

gpu-lerobot
├─ ACT scale-up
├─ SmolVLA
└─ optional π₀/GR00T
```

Do not merge these environments or upgrade a vendor reproduction environment in place. Record GPU model, driver, CUDA, VRAM, package lock and container digest.
