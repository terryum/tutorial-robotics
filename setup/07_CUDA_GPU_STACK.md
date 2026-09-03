# CUDA GPU Development Stacks

A full GPU host such as WS2 must still use separate locked environments.

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
