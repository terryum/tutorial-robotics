<!-- pal:language:start -->
<p align="right">
  <a href="core-enlight-03.md" lang="ko">한국어</a> | <a href="../../en/lessons/core-enlight-03.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-enlight-03 — Enlight 관절·TCP 궤적 추종

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / enlight` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-enlight-02` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

실제 MuJoCo 팔 상태에서 관절·TCP 오차를 측정합니다. 학습 수업은 팔의 시연 또는 rollout을 사용하고 독립 목표 20개를 평가합니다.

## Learning goals

FR3의 관절 배열을 복사하지 않고 Enlight의 joint1…joint7을 이름으로 찾습니다. Enlight 모델의 중력 보상·PD 토크를 시뮬레이션에서만 적용합니다.

## Preflight

선행 수업: core-enlight-02. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

## Action

```bash
pal lesson run core-enlight-03 --samples 64 --json
```

JSON의 run_dir를 BASE로 기록하세요. 실행은 완료 처리가 아닙니다.

## Expected

`enlight-trajectory.json`, `trace.csv`, `plot.png`, `experiment.json`을 확인합니다. `evaluation.json`의 performance_verified는 학습 성능만 나타냅니다.

## Observe

축·단위·첫/마지막 오차·최댓값을 읽습니다. 렌더링에서 모델과 움직임을 확인하고, payload의 관절 이름·그룹·접촉을 수치와 대조합니다.

## How it works

FR3의 관절 배열을 복사하지 않고 Enlight의 joint1…joint7을 이름으로 찾습니다. Enlight 모델의 중력 보상·PD 토크를 시뮬레이션에서만 적용합니다.

## Code connection

[`arm.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py)

`pai_lab.training`이 체크포인트·독립 평가를 기록합니다.

## Try it

variant 하나만 바꾸고 나머지 조건을 유지합니다.

```bash
pal lesson run core-enlight-03 --samples 64 --variant 0.8 --json
pal lesson check core-enlight-03 --run-dir BASE --json
pal lesson review core-enlight-03 --run-dir BASE --comparison-run-dir COMPARISON --notes "측정값과 비교 해석"
pal lesson finish core-enlight-03 --run-dir BASE --json
```

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run core-enlight-03 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [경로 안내](../paths.md)를 따릅니다.

## Checkpoint

설명·기준 실행·비교 실행·다음 행동을 저장한 뒤 한 수업에서 멈춥니다. 도구 또는 모델 호환성이 미확인이면 대기합니다.

<!-- pal:navigation:start -->
## Next lesson

[core-enlight-04](./core-enlight-04.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
