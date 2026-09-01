---
id: T02
title: "Download and pin the public robot sources"
phase: "Assets"
host: "either"
prerequisites: [T00]
gpu: "none"
hardware: "none"
---

# T02 — Download and pin the public robot sources

## Objective

공식 외부 저장소를 다운로드하고 commit SHA, license, 모델 경로를 고정한 registry를 만든다.

## Prerequisites

- Tutorial status: T00
- Host: `either`
- GPU: `none`
- Hardware access: `none`
- Read first: `setup/03_MODEL_DOWNLOAD.md`, `docs/08_VERSIONING_AND_LICENSES.md`

## Concepts to explain

- native asset immutability
- commit pinning
- license provenance
- model path discovery

## Required implementation targets

- `configs/models.yaml`
- `configs/upstreams.lock.yaml`
- `src/pai_lab/assets/registry.py`
- `tests/T02/test_registry.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 공식 source 목록을 검증한다
2. `external/`에 필요한 저장소를 clone/fetch한다
3. commit·license·asset path를 자동 탐색한다
4. FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, ALOHA와 watchlist를 registry에 기록한다

## Commands that must exist or be replaced by documented equivalents

- `pal model sync --audit`
- `pal model list`
- `pytest tests/T02 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- model_registry.md 표
- source graph Mermaid diagram

Persist outputs under `outputs/T02/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 다섯 public robot ecosystem entry 존재
- [ ] 각 Git source에 SHA와 license path 존재
- [ ] vendor working tree clean
- [ ] 존재하지 않는 path를 registry가 거부
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
