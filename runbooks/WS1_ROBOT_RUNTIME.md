# Runbook — WS1 before hardware connection

WS1 uses one Ubuntu/NVIDIA workstation for the full hardware-free curriculum. A
MacBook is optional and supports only the Core profile. Machine names never grant
runtime or hardware capability.

## 1. Clean checkout and Core

```bash
pal host detect --json
pal setup plan --profile core --out .local/setup-core.json --json
pal setup verify --profile core --json
pal course runnable --without-hardware --json
pal course init --through core --json
```

Run the 25 Core lessons in catalog order. Inspect each semantic artifact in
addition to `summary.json`; process exit alone is not completion evidence.

## 2. Optional, isolated software profiles

Create and verify only the profile needed by the next lesson:

```bash
pal setup plan --profile ros --out .local/setup-ros.json --json
pal setup plan --profile gpu --out .local/setup-gpu.json --json
pal setup plan --profile isaac --out .local/setup-isaac.json --json
```

The ROS profile covers `sim-ros-01` through `sim-ros-04`, including live graph,
QoS, TF and MCAP checks. GPU, Isaac and VLA stacks stay in separate environments
and require explicit installation approval. Do not install drivers, CUDA, ROS or
Isaac automatically.

## 3. Candidate bundle and offline runtime

`sim-deploy-01` creates and validates the candidate contract. Before any device
is connected, verify target-runtime parity and run only `hw-common-01`:

```bash
pal setup plan --profile runtime-offline --out .local/setup-runtime.json --json
pal setup verify --profile runtime-offline --json
pal lesson check hw-common-01 --json
pal lesson run hw-common-01 --headless --json
```

The result must contain the exact candidate hash, deterministic vector result,
rollback declaration, an enabled command sink and `emitted_command_count = 0`.
There is no robot command publisher in this scope.

## 4. Explicit stop point

Do not run `hw-common-02`, `hw-fr3-01`, `hw-wuji-01`, `hw-wuji-02`,
`hw-enlight-01`, `hw-enlight-02`, `hw-enlight-03`, or
`hw-enlight-wuji-01` before device discovery and a fresh read-only gate. Those
lessons remain `scaffolded`/`reader_test_required`.

Private robot models, teleoperation data, and hardware integrations belong only
in their private overlay and follow its own reader-gated stop point.

## 5. Evidence boundary

Store run output, inventory, bags, calibration and host facts under `.local/`.
Commit only version/pin/checksum information and a non-secret summary. Never
record device serials, accounts, license keys, private addresses or raw datasets.

Hardware progression, after a separate request, remains:

```text
offline replay → command sink → read-only → live shadow → torque-disabled replay
→ fresh run card → one explicitly approved action
```
