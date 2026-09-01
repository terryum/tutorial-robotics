# Isaac Sim and Isaac Lab Stacks

## Two-stack strategy

### Vendor-compatible

Use the exact Isaac Sim/Lab combination targeted by the selected Unitree, Sharpa, or Wuji example. Reproduction comes before modernization.

### Modern research

Use a separate environment for Isaac Sim 6.0.1 and Isaac Lab 3.0 Beta 2 or its later stable successor. Never upgrade the vendor-compatible environment in place.

## Installation requirements

- use only a supported Linux/Windows host; Mac is a client
- pin exact release/tag
- run official installation smoke test
- run one official example before importing custom robots
- record driver, GPU, VRAM, Python and extension versions

## Asset import

Import URDF/MJCF to USD into `generated_assets/`. Record source commit, importer options, and validation results. Do not overwrite native assets.
