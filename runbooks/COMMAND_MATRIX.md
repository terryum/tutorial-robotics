> Current execution authority: [common workflow](../agent/workflow.md). Learner state is ignored `.local/`; historical host reports below never complete lessons or require automatic commits.

# Codex Commands — Capability-First

## WS2: first tutorial

```text
이 컴퓨터는 WS2이며 DEVELOPMENT mode다. EXECUTION_MODEL.md와 AGENTS.md를 읽고 $bootstrap-host를 실행해. WS2를 MacBook 이후 phase로 제한하지 말고 portable/core curriculum과 CUDA/Isaac curriculum을 모두 실행 가능한 superset host로 등록해. T00 하나만 완료하고 멈춰줘.
```

## MacBook: first or resumed tutorial

```text
이 컴퓨터는 MacBook이며 DEVELOPMENT mode다. git status와 local learner progress를 확인하고 $bootstrap-host를 실행해. 현재 capability로 실행 가능한 다음 eligible tutorial 하나만 완료해. 지원하지 않는 GPU/Isaac tutorial은 shared status를 변경하지 마.
```

## Any development host: next

```text
현재 host capabilities, tutorial prerequisites와 local learner progress를 기준으로 다음 eligible tutorial 하나만 실행해줘. 작은 deterministic baseline부터 실제 실행한 뒤 test·시각화·한국어 report·state를 갱신하고 멈춰줘.
```

## Switch host

```text
이전 host의 virtual environment와 cache를 복사하지 않는다. committed lock/source pins로 local environment를 재구성하고, shared done 상태를 존중해 현재 host에서 가능한 다음 tutorial을 선택해줘.
```

## Verify a completed tutorial on another host

```text
<TUTORIAL_ID>의 shared status는 done으로 유지하고 local portability verification만 수행해. canonical output을 덮어쓰지 말고 host ID가 포함된 새 output과 report를 생성해줘.
```

## WS2: switch from development to robot runtime

```text
WS2를 ROBOT_RUNTIME mode로 전환할 준비를 audit해. GPU training, Isaac, Jupyter, policy server batch를 모두 종료했는지 확인하고 robot-runtime environment, dedicated NIC와 single command authority를 검증해. 아직 hardware command는 보내지 마.
```

## WS1: robot runtime

```text
이 컴퓨터는 WS1이며 ROBOT_RUNTIME mode다. $bootstrap-host로 runtime capability를 등록하고 candidate bundle/hash를 검증해. T35B의 offline replay와 command-sink dry-run까지만 수행하고 실제 motion은 금지해.
```
