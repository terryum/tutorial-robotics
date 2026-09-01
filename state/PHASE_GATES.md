# Phase Gates

## Current status

| Gate | Status | Evidence / bundle ID | Last verified |
|---|---|---|---|
| `MACBOOK_FOUNDATION_COMPLETE` | pending | — | — |
| `WS2_SIM_TRAIN_COMPLETE` | pending | — | — |
| `WS2_DEPLOYMENT_BUNDLE_READY` | pending | — | — |
| `CARTON_CANDIDATE_BUNDLE_READY` | pending | — | — |
| `WUJI_COSMETICS_CANDIDATE_READY` | pending | — | — |
| `RUNTIME_OFFLINE_VALIDATED` | pending | — | — |
| `ROBOT_READ_ONLY_VALIDATED_WUJI` | pending | — | — |
| `WUJI_LOW_RISK_VALIDATED` | pending | — | — |

Motion/contact approval is never a persistent done-state. It is a dated per-run card.

## `MACBOOK_FOUNDATION_COMPLETE`

Required:

```text
T00–T08, , T09–T17
T19–T25
T28–, T16A
T32A
```

Evidence includes environment locks, source/model pins, four-model smoke outputs, cross-format tests, Korean reports and a WS2 handoff manifest.

## `WS2_SIM_TRAIN_COMPLETE`

Required:

```text
, T26, T27, , T32C, T33, T34, T35
```

T32D is optional. Target-specific //T42A are run when that robot/task is being promoted.

## `WS2_DEPLOYMENT_BUNDLE_READY`

T35A creates a bundle for one explicit robot/task/policy. A bare checkpoint is invalid. Include processor/config, normalization, camera/joint/state/action order, units/frame/rates/horizon, assets/calibration, dataset manifest, Git commit, lock/container digest, sim results, deterministic vectors, tolerances and rollback.

## Target-specific candidate gates

- `CARTON_CANDIDATE_BUNDLE_READY` — 
- `WUJI_COSMETICS_CANDIDATE_READY` — T42A

## `RUNTIME_OFFLINE_VALIDATED`

T35B verifies bundle/hash, runtime rebuild, deterministic parity, recorded-episode replay, no-motion command-sink shadow and rollback. It authorizes read-only only.

## Robot-specific read-only gates

```text
T36 --robot wuji_hand2_beta2_right → ROBOT_READ_ONLY_VALIDATED_WUJI
```

## Motion/contact progression

- Wuji: T38 named-pose/calibration approvals → T42B separate grasp/regrasp approval.

No gate in this file is production approval.
