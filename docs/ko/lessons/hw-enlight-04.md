<!-- pal:language:start -->
<p align="right">
  <a href="hw-enlight-04.md" lang="ko">한국어</a> | <a href="../../en/lessons/hw-enlight-04.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# hw-enlight-04 — Enlight 자유공간 관절·TCP 실행 카드

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `hardware / enlight` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight` |
| Prerequisites | `hw-enlight-02, sim-enlight-05` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

이 단계는 장비 증거가 없어 대기 상태입니다. 일반 수업 명령은 실물 명령을 보내지 않습니다.

## Learning goals

Elements 문서 검토 → 읽기 전용 조회 → 오프라인 재생 → command sink → 새 실행 카드 순서로 준비합니다. 작은 관절 동작부터 검증하고 TCP 제어는 별도 승인합니다.

## Preflight

선행 수업: hw-enlight-02, sim-enlight-05. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

## Action

실물 명령을 실행하지 마세요. 준비 기록과 미확인 게이트를 검토합니다. 실행 카드는 정확한 장비·작업·관절·한계·60초 이내 만료·일회성 승인에 묶입니다.

```bash
pal lesson run hw-enlight-04 --samples 64 --json
```

JSON의 run_dir를 BASE로 기록하세요. 실행은 완료 처리가 아닙니다.

## Expected

`reader_test_required`로 차단됩니다. 장비 증거 없이 완료하지 않습니다.

## How it works

Elements 문서 검토 → 읽기 전용 조회 → 오프라인 재생 → command sink → 새 실행 카드 순서로 준비합니다. 작은 관절 동작부터 검증하고 TCP 제어는 별도 승인합니다.

## Code connection

[`hardware.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/run_card.py)

`pai_lab.training`이 체크포인트·독립 평가를 기록합니다.

## Try it

variant 하나만 바꾸고 나머지 조건을 유지합니다.

```bash
pal lesson run hw-enlight-04 --samples 64 --variant 0.8 --json
pal lesson check hw-enlight-04 --run-dir BASE --json
pal lesson review hw-enlight-04 --run-dir BASE --comparison-run-dir COMPARISON --notes "측정값과 비교 해석"
pal lesson finish hw-enlight-04 --run-dir BASE --json
```

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run hw-enlight-04 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [경로 안내](../paths.md)를 따릅니다.

## Checkpoint

설명·기준 실행·비교 실행·다음 행동을 저장한 뒤 한 수업에서 멈춥니다. 도구 또는 모델 호환성이 미확인이면 대기합니다.

<!-- pal:navigation:start -->
## Next lesson

[hw-enlight-05](./hw-enlight-05.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
