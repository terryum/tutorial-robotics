---
id: T35A
title: "WS2 candidate deployment bundle and promotion gate"
phase: "Handoff"
mode: "development"
requires: [dev_core, ubuntu_24_04_x86_64, nvidia_cuda]
preferred_execution: "full-gpu-linux-host"
prerequisites: [T26, T27, T32C, T34, T35]
gpu: "required-for-validation"
hardware: "none"
---

# T35A — WS2 candidate deployment bundle and promotion gate

## Objective

WS2 핵심 학습·simulation 결과를 audit하고, 실제 robot runtime이 재현 가능한 candidate deployment bundle과 phase gate를 만든다.

## Prerequisites

- Tutorial status: , T26, T27, T32C, T34, T35
- Host profile: `WS2_SIM_TRAIN`
- Gate: `MACBOOK_FOUNDATION_COMPLETE`
- Hardware access: none
- Read first: `MACHINE_SEQUENCE.md`, `runbooks/HANDOFF_AND_SYNC.md`

## Required implementation targets

- `deployment_bundles/<bundle-id>/MANIFEST.md`
- `deployment_bundles/<bundle-id>/test_vectors/`
- `reports/T35A_promotion_audit.md`
- updates to `state/PHASE_GATES.md`

## Execution procedure

1. required tutorial artifacts와 acceptance criteria를 audit한다
2. 한 target task/policy/robot candidate를 선택한다
3. `$promote-deployment-bundle`을 실행한다
4. checkpoint, config, normalization, camera/joint/state/action order, units, rates, horizon, pre/post-process, assets, calibration, dataset manifest, Git commit, lock/container digest, sim reports, test vectors, rollback을 manifest에 기록한다
5. deployment-compatible environment에서 deterministic load/inference test를 수행한다
6. 성공 시 `WS2_SIM_TRAIN_COMPLETE`와 `WS2_DEPLOYMENT_BUNDLE_READY` gate를 갱신한다

## Acceptance criteria

- [ ] checkpoint-only handoff가 아니다
- [ ] 모든 artifact의 hash 또는 immutable reference가 있다
- [ ] deterministic test vector와 expected tolerance가 있다
- [ ] rollback candidate가 있다
- [ ] hardware command를 실행하지 않는다
- [ ] WS1/WS2 integration 최초 명령을 report에 포함한다
