# Robot path implementation verification — 2026-11-08

Development evidence is separate from personal learner completion. All runs used isolated `PAL_LOCAL_DIR` state; no learner history was marked complete. No physical robot, enable API, firmware operation or motion command was used.

| Environment | Result | Limits |
|---|---|---|
| Mac / MuJoCo | Named-path CLI, numerical control/learning, rendering and artifact checks verified | Simulation evidence only |
| Isaac / PhysX | Code, manifests and capability blocking prepared; runtime unverified | Mac has no Isaac runtime. The WS2 alias did not resolve in this session. No substitute engine was used to claim success |
| Enlight hardware | Mock transport approval/read-only/failure gates verified | RDK 2.1 / v3E.1 versus description v4, site transport, tools, payload, stop/watchdog and real execution remain unverified |

## Measured simulation evidence

Baseline uses seed 7 and samples 64; comparison changes only variant from 1.0 to 0.8. Runs record the exact code, model pin, numeric files and render hashes. The integration harness bypasses prerequisite *completion* checks only in its isolated developer session, while retaining host/model checks and independent artifact validation. This is batch development evidence, not completion of a learner's path.

| Lesson | Baseline | Comparison | Interpretation |
|---|---:|---:|---|
| FR3 joint/TCP trajectory | TCP RMS 0.00679325 m | 0.00656127 m | Both below the simulation 20 mm tracking check |
| Enlight joint/TCP trajectory | TCP RMS 0.00519292 m | 0.00415416 m | Uses Enlight inertia-scaled PD and bias compensation; no FR3 joint transfer |
| FR3 BC independent reach | 20/20 | 11/20 | Baseline passes 16/20 gate; lower learning-rate short comparison fails it |
| Enlight BC independent reach | 20/20 | 20/20 | Separate Enlight demonstrations and weights |
| Enlight PPO short training | 0/20 | 0/20 | Optimizer execution is not policy performance; neither is a deployable candidate |
| Enlight independent FK | maximum 6.76071e-16 m | unchanged | Preserves the independent 1e-9 m criterion |

Shadow Hand verifies contacts specifically involving the named spherical object, rather than counting self contacts. Its derived scene preserves lighting and places the object at the pinned grasp site. Stretch 3 addresses named wheel, lift and tendon actuators separately from its free-base state. The coordinated introductory task reduces measured TCP target error, without claiming a trained mobile policy or millimetre accuracy (baseline 44.31 → 40.50 mm; comparison 44.30 → 40.52 mm).

Learning evaluates twenty independent targets and recomputes ten consecutive steps within 10 mm. This threshold is not a real-device tolerance. Episode-level train/validation/test splits are 20/5/5. Checkpoints retain optimizer, fixed normalization and RNG state. Tests compare interrupted/resumed BC and PPO with uninterrupted weights, exercise real SIGINT/SIGTERM at update boundaries, recover the newest intact checkpoint, reject changed data/configuration and detect tampered host transfers.

## Checks and handoff

Mac regression: 196 tests and eight subtests passed. Ruff, mypy, catalog, release, public source boundary and strict MkDocs checks passed. The numeric/render harness verified seventeen baseline/comparison runs, including FR3 PPO independent evaluation. Remote CI is checked after push.

Run these before publishing a changed revision:

```bash
.venv/bin/pytest
.venv/bin/ruff check .
.venv/bin/mypy src
.venv/bin/python scripts/validate_repository.py
.venv/bin/python scripts/validate_release.py
.venv/bin/python scripts/check_public_boundary.py
.venv/bin/python scripts/check_credentials.py --tracked
.venv/bin/mkdocs build --strict
```

The original 49 IDs/aliases have an explicit regression fixture; new lessons are append-only. Legacy private-provider compatibility is checked in the sibling overlay before updating its public pin. Personal progress uses the existing opt-in integration and raw artifacts/approvals remain local.

Next on the GPU host: fetch pinned model assets, verify Isaac installation/version and PhysX, then run each FR3/Enlight/Shadow/Stretch lesson. Verify joint/drive/coupling/free-base behavior, actual contact sensors, TCP frame/Jacobian, render, close and training resume. Imported equality constraints that lack verified mimic/tendon mapping deliberately block. Manufacturer Robotiq USD requires real Git LFS objects and the pinned PhysX variant; pointer files are rejected. No GPU lesson badge is promoted using Mac-only evidence.

Next on Enlight: review Elements and RDK 2.1 / v3E.1, establish model identity and description compatibility, validate offline replay/sink/read-only/shadow/torque-disabled replay, then approve a fresh exact-action card for one small movement. TCP path, calibrated probe plane force, and gripper pick/transfer/place each require their own validated tool, limits and per-run approval. Learned torques are not directly sent to hardware.

See [English path guide](../en/paths.md) and [한국어 경로 안내](../ko/paths.md).
