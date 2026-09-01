---
id: T30
title: "ALOHA simulation and ACT"
phase: "Imitation Learning"
host: "mac/either"
prerequisites: [T28, T29]
gpu: "optional"
hardware: "none"
---

# T30 — ALOHA simulation and ACT

## Objective

LeRobot/gym-aloha로 양팔 dataset과 ACT action chunking을 재현한다.

## Prerequisites

- Tutorial status: T28, T29
- Host: `mac/either`
- GPU: `optional`
- Hardware access: `none`
- Read first: `setup/06_LEROBOT.md`

## Concepts to explain

- bimanual state/action
- action chunk
- temporal aggregation
- CVAE/transformer policy
- demonstration efficiency

## Required implementation targets

- `examples/T30/aloha_act_workflow.md`
- `configs/il/aloha_act.yaml`
- `tests/T30/test_aloha_smoke.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 공식 ALOHA environment를 설치·검증한다
2. 작은 dataset 또는 공식 sample을 시각화한다
3. tiny ACT training/inference를 실행한다
4. chunk size 한 항을 비교한다

## Commands that must exist or be replaced by documented equivalents

- `LeRobot official ALOHA dataset/env command`
- `LeRobot ACT train/eval command with a tiny config`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- action_chunks.png
- aloha_act_loss.png
- aloha_rollout.mp4

Persist outputs under `outputs/T30/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 환경 reset/step 성공
- [ ] ACT checkpoint 생성 또는 공식 checkpoint inference
- [ ] Mac 한계와 workstation 명령 구분
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
