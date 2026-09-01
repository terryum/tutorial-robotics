---
id: T00
title: "Repository bootstrap and host audit"
phase: "Foundation"
host: "registered-profile"
prerequisites: []
gpu: "none"
hardware: "none"
---

# T00 — Repository bootstrap and host audit

## Objective

현재 컴퓨터의 실제 capability를 기록하고, Codex가 이후 튜토리얼을 안정적으로 생성할 저장소 골격과 상태 추적 CLI를 만든다.

## Prerequisites

- Tutorial status: none
- Host profile: explicit `MACBOOK_FOUNDATION`, `WS2_SIM_TRAIN`, `WS2_ROBOT_INTEGRATION`, or `WS1_ROBOT_RUNTIME`
- GPU: `none`
- Hardware access: `none`
- Read first: `MACHINE_SEQUENCE.md`, matching runbook, `setup/00_HOST_AUDIT.md`, `setup/01_REPO_BOOTSTRAP.md`, `setup/11_MACHINE_LOCAL_STATE.md`

## Concepts to explain

- Codex AGENTS/skill routing
- host capability detection
- src-layout와 격리 환경
- 완료 상태의 기계적 추적

## Required implementation targets

- `src/pai_lab/cli.py`
- `src/pai_lab/doctor.py`
- `tests/T00/test_doctor.py`
- `.local/HOST_PROFILE.md` and `.local/CAPABILITIES.md`
- shared non-secret environment summary in `state/ENVIRONMENTS.md`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. `$bootstrap-machine`으로 등록된 logical host/profile을 확인한다
2. read-only host audit를 수행한다
3. Git 상태를 확인하고 필요한 디렉터리와 `.local/` ignore 규칙을 만든다
4. `pal doctor`, `pal tutorial list`, `pal tutorial status`를 구현한다
5. 현재 `state/PROGRESS.md`, phase gate와 machine profile을 파싱하는 테스트를 만든다

## Commands that must exist or be replaced by documented equivalents

- `pal doctor`
- `pal tutorial list`
- `pytest tests/T00 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- 호스트 capability 표를 Markdown과 JSON으로 저장한다

Persist outputs under `outputs/T00/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] global Python을 변경하지 않는다
- [ ] `pal doctor`가 logical host/profile과 실제 OS/architecture를 정확히 보고한다
- [ ] profile/gate/state를 읽고 이 machine에서 다음 eligible tutorial을 표시한다
- [ ] `.local/`이 Git에서 제외된다
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
