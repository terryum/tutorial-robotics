---
id: T16A
title: "Wuji/Sharpa hand retargeting and demonstration recording"
phase: "Dexterous Data"
mode: "development"
requires: [dev_core, mujoco_supported, small_ml_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T14, T16, T28, T30]
gpu: "optional"
hardware: "none"
---

# T16A — Wuji/Sharpa hand retargeting and demonstration recording

## Objective

recorded/synthetic human hand landmarks 또는 glove-like joint streams를 Wuji Hand 2와 Sharpa Wave에 retarget하고, 동일한 episode schema로 demonstration을 저장·재생한다. 실제 Manus/Wuji Glove 연결 전 offline pipeline을 완성한다.

## Concepts to explain

- human-to-robot morphology mismatch
- fingertip versus joint-angle retargeting
- optimization objective, joint limits and temporal smoothing
- left/right convention and calibration pose
- retargeting error versus task success
- demonstration timestamps and episode boundaries

## Required implementation targets

- `src/pai_lab/retargeting/hand_retargeter.py`
- `src/pai_lab/data/hand_demo_recorder.py`
- `examples/T16A/offline_hand_retargeting.py`
- `tests/T16A/`

## Execution procedure

1. Use a deterministic synthetic or recorded human-hand sequence.
2. Retarget it separately to Wuji and Sharpa using pinned model revisions.
3. Enforce joint limits, smoothness and collision checks.
4. Save raw human input, robot targets and residuals in the common episode schema.
5. Replay both hands and compare fingertip/task-space error.
6. Document the later live Manus/Wuji Glove adapter boundary without pretending hardware is connected.

## Commands

- `pal retarget hand --robot wuji_hand2_beta2_right --input <sequence>`
- `pal retarget hand --robot sharpa_wave_right --input <sequence>`
- `pal dataset inspect <episode-id>`

## Visualization contract

- `human_wuji_sharpa_fingertip_error.png`
- `retargeting_joint_limits.png`
- `wuji_retargeted_demo.mp4`
- `sharpa_retargeted_demo.mp4`

## Acceptance criteria

- [ ] raw input and both robot outputs share timestamps and provenance
- [ ] left/right, units and calibration pose are explicit
- [ ] joint-limit and smoothing behavior are tested
- [ ] demonstration can be replayed deterministically
- [ ] live glove use is clearly deferred to robot/device integration
