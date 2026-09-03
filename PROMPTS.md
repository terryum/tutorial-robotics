# Codex Prompt Library

## Universal next tutorial

```text
EXECUTION_MODEL.md, AGENTS.md, references/PUBLIC_CURRICULUM.md, local host capabilities, shared progress and tutorial index를 읽고 현재 host에서 실행 가능한 다음 eligible tutorial 하나만 실행해줘. preflight → code → test → actual run → persistent visualization → Korean report → shared state update를 완료하고 멈춰줘.
```

## WS2 as superset host

```text
이 컴퓨터는 WS2 DEVELOPMENT host다. portable/core curriculum을 다른 장비의 선행 단계로 취급하지 말고 core/portable와 CUDA/Isaac tutorial을 모두 capability에 따라 실행해. core lesson에서는 deterministic baseline을 먼저 만들고 GPU scale-up을 별도로 기록해.
```

## MacBook continuation

```text
이 컴퓨터는 MacBook DEVELOPMENT host다. Git에서 완료 상태를 이어받고 현재 capability로 실행 가능한 다음 tutorial 하나만 수행해. 지원하지 않는 GPU/Isaac/native-vendor tutorial의 shared 상태는 변경하지 마.
```

## Explain current lesson

```text
$explain-and-visualize를 사용해 방금 tutorial을 mental model → 수식/단위/frame → 코드·데이터 흐름 → 결과 시각화 → simulation 한계 → 공개 로봇 적용 순서로 설명해줘. 한 변수만 바꾼 비교 실험을 추가해.
```

## Cross-host verification

```text
<TUTORIAL_ID>는 globally done을 유지하고 이 host에서 portability verification으로 재실행해. canonical output을 덮어쓰지 말고 host-specific evidence만 추가해.
```

## Hardware safety

```text
$hardware-gate를 사용해 read-only 또는 command-sink dry-run까지만 수행해. 실제 motion/contact/system-identification excitation은 robot, subsystem, trajectory, payload, mode, limits, workspace, watchdog와 stop path가 포함된 이번 run card를 내가 명시적으로 승인하기 전 금지해.
```
