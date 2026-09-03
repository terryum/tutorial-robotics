---
id: T26
title: "Unitree G1 PPO and motion imitation on NVIDIA workstation"
phase: "Humanoid"
mode: "development"
requires: [dev_core, ubuntu_24_04_x86_64, nvidia_cuda, mjlab_supported]
preferred_execution: "full-gpu-linux-host"
prerequisites: [T25]
gpu: "required"
hardware: "none"
---

# T26 — Unitree G1 PPO and motion imitation on NVIDIA workstation

## Objective

공식 Unitree RL MJLab 또는 Isaac Lab 경로 중 하나를 pin해 velocity tracking 또는 motion imitation을 재현한다.

## Prerequisites

- Tutorial status: T25
- Host profile: `WS2_SIM_TRAIN`
- GPU: `required`
- Hardware access: `none`
- Gate: `MACBOOK_FOUNDATION_COMPLETE`
- Read first: `setup/07_WORKSTATION.md`, `runbooks/WS2_SIM_TRAIN.md`

## Concepts to explain

- parallel environments
- RSL-RL/PPO config
- motion tracking rewards
- train→play→sim2sim

## Required implementation targets

- `workstation/T26/`
- `reports/T26_g1_training.md`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. vendor-compatible stack을 선택하고 이유를 기록한다
2. 공식 task list와 pretrained play를 먼저 실행한다
3. pose hold 또는 stand task에서 작은 env-count smoke training을 실행한다
4. velocity tracking을 재현한다
5. 가능한 경우 push-recovery evaluation을 수행한다
6. reference motion imitation을 재현한다
7. 정상 동작 후 scale-up 명령을 별도로 제공한다

## Commands that must exist or be replaced by documented equivalents

- `vendor task-list command`
- `vendor play command`
- `vendor train command with small num-envs`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- training_curve.png
- g1_policy.mp4
- throughput.json

Persist outputs under `outputs/T26/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] pose hold/stand → velocity tracking → push-recovery evaluation → motion imitation의 단계가 report에 구분됨
- [ ] 공식 example 재현
- [ ] GPU/VRAM/throughput 기록
- [ ] sim2sim 전에 real deployment 금지
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
