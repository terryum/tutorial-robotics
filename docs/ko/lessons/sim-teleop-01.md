<!-- pal:language:start -->
<p align="right">
  <a href="sim-teleop-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-teleop-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-teleop-01 — Ubuntu VR 설치와 읽기 전용 입력

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / common` |
| Legacy alias | `None` |
| Platforms | `linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-teleop-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

기존 VR 없는 기초 수업을 유지하는 선택 경로입니다. 합성 재생은 synthetic으로 표시하며 실제 입력 검증으로 인정하지 않습니다. 새 실행 폴더에 기록합니다. 장치 원시 시각, m/rad 단위 xyz+xyzw, 명시적인 좌우, 보정 ID, clutch와 deadman을 확인합니다. 유효 입력 없이 100 ms가 지나면 hold로 잠깁니다. 두 스위치를 해제하고 로컬 재무장한 다음 다시 누릅니다. 재연결·추적 손실에도 같은 절차가 필요합니다.

Quest → MANUS → VIVE 개별 읽기 전용 검사와 동시 60초 수신 검증 전에는 capability-unavailable입니다. 아래 설치 안내를 따릅니다. 장치 증거를 합성하지 않으며 실제 입력 수업은 reader test 전까지 scaffolded입니다.

## Learning goals

입력 소스 선택·보정 좌표·로컬 hold·에피소드 무결성을 이해합니다.

## Preflight

`pal setup verify --profile core --json`을 실행하고 [Ubuntu VR 설치](../setup/vr-teleop.md)를 읽습니다. Mac은 계약·변환·재생·소형 MuJoCo 예제, WS2 Ubuntu는 입력·시뮬레이션·학습 환경입니다. WS1 Ubuntu 실물 적용은 별도 승인 단계입니다. Windows는 제조사 복구용 선택 경로입니다. 보정값·데이터는 ignored `.local/`에 둡니다.

## Action

```bash
pal lesson run sim-teleop-01 --samples 16 --json
```

## Expected

Inspect `device-input.json`, `experiment.json`, `trace.csv` and episode manifests when available. 실제 입력은 60초 수신율·최대 간격·추적 유효율·가림·해제·재연결·100 ms timeout 증거를 요구합니다.

## How it works

공통 계약은 수신 호스트 monotonic 시각과 명시적 소스 식별자를 사용합니다. 장치 원시 시각을 보존하고 호스트 사이 시각을 빼지 않습니다.

## Code connection

`pai_lab.teleop`, `teleop_sources`, `teleop_recording` and `lessons.teleop`.

## Try it

```bash
pal lesson run sim-teleop-01 --samples 16 --variant 0.8 --json
pal lesson check sim-teleop-01 --run-dir BASE --json
```

## Recovery

중단된 에피소드를 보존하고 저장·폐기·중단 상태를 구분합니다. 기존 에피소드를 덮어쓰지 않고 재연결 후에는 로컬 재무장 전 조작을 재개하지 않습니다.

## Checkpoint

검토 전에 수치 산출물과 재생을 비교합니다. 개발 테스트는 개인 수업 완료를 만들지 않습니다. 실물 텔레오퍼레이션은 시뮬레이션 완료와 별도 안전 검토·실행별 승인이 필요합니다.

<!-- pal:navigation:start -->
## Next lesson

[sim-teleop-02](./sim-teleop-02.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
