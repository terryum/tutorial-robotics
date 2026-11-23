<!-- pal:language:start -->
<p align="right">
  <a href="sim-teleop-02.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-teleop-02.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-teleop-02 — 공간 정합과 command sink

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / common` |
| Legacy alias | `None` |
| Platforms | `linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-teleop-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

공간 정합은 명시적인 변환 체인이며 자세 배열 복사가 아니다. Integrated 모드의 `InputMux`는 VIVE 손목·MANUS 손가락·Quest 스위치를 선택하며 quest-only는 별도 명시 모드다. 수업의 `integrated_frame`은 합성 샘플과 알려진 0.05 m 좌표 병진으로 출처 선택·변환 산술을 검사하며 실제 보정을 주장하지 않는다.

선행 [개념 장](../concepts/kinematics.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 보정된 SE3 변환과 오래된 입력 차단 수신기는 리타게팅을 어떻게 제한하는가?

## Learning goals

공간 정합은 명시적인 변환 체인이며 자세 배열 복사가 아니다.

보정된 SE3 변환과 오래된 입력 차단 수신기는 리타게팅을 어떻게 제한하는가?

## Preflight

카탈로그 플랫폼·역량에 맞는 호스트를 사용하며 컴퓨터 이름이 준비를 허가하지 않는다. `core-teleop-01`은 macOS arm64·Linux x86_64를 지원하고 이후 선택 입력·수집 수업은 Linux x86_64다. [VR 준비](../setup/vr-teleop.md), [장비 단계](../equipment-stages.md), [검증 기록](../../verification/vr-teleop-2026-11-13.md)의 합성·실제 구별을 읽는다. 장치·보정·원시 에피소드는 무시되는 `.local/`에 두며 벤더 자동 설치·장치 동의를 뜻하지 않는다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run sim-teleop-02 --headless --seed 7 --samples 16 --output-dir .local/runs/sim-teleop-02/baseline-01 --json
```

## Expected

실제 장치 검증 보고서가 아니라 합성 재생·수집 근거를 기대한다. 카탈로그 산출물·`experiment.json`·`trace.csv`·`plot.png`·에피소드 매니페스트를 확인한다. 저장 3에피소드와 폐기·중단 기록으로 생명주기·출처를 보존한다. 실제 60초 장치 속도·추적·가림·재연결 검증은 별도 실제 입력 게이트다.

## Observe

기록한 입력과 적용 목표를 따로 확인합니다. 합성 timestamp는 테스트용으로 생성한 시각입니다.

### 산출물 읽기

저장 프레임의 원시 `devices`, Quest 스위치, `mode`와 변환된 좌우 `pose_source`, `finger_source`, 좌표·보정 ID·수신 시각을 함께 읽는다. 결합 최신 여부는 선택한 수신 시각 중 가장 오래된 값을 쓰므로 최신 손목이 오래된 손가락·스위치를 숨길 수 없다. 에피소드 매니페스트·`live_input_verified=False`가 중요하며 장치 시계는 호스트 간 뺄셈 없이 보존한다.

## How it works

### 직관

공간 정합은 명시적인 변환 체인이며 자세 배열 복사가 아니다. Integrated 모드의 `InputMux`는 VIVE 손목·MANUS 손가락·Quest 스위치를 선택하며 quest-only는 별도 명시 모드다. 수업의 `integrated_frame`은 합성 샘플과 알려진 0.05 m 좌표 병진으로 출처 선택·변환 산술을 검사하며 실제 보정을 주장하지 않는다.

### 계산과 단위

$$
T_{world,wrist}=T_{world,device}T_{device,tracker}T_{tracker,wrist}
$$

각 T는 유한한 오른손 4×4 강체 변환이다. 병진은 m, 회전은 무차원이며 출력 자세는 xyz+xyzw다. 곱 순서가 중요하며 손목 장착 오프셋은 추적 방향에 따라 회전한다. 보정 측정이 아닌 계산으로 항등 회전·장치 x=0.3 m·월드 병진 +0.05 m이면 월드 x=0.35 m이다.

```python
import numpy as np
world_from_device = np.eye(4)
world_from_device[0, 3] = 0.05
point = np.array([0.3, 0.0, 0.0, 1.0])
assert np.isclose((world_from_device @ point)[0], 0.35)
```

## Code connection

### 소스 추적

[`src/pai_lab/teleop_sources.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_sources.py)

`examples/sim-teleop-02/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[`teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop.py), [`teleop_recording.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_recording.py), [VR 검증 기록](../../verification/vr-teleop-2026-11-13.md)도 읽는다.

## Try it

### 통제된 비교

합성 입력 변위 `variant`만 1→0.8로 바꾸고 월드·장착 행렬·출처 모드·샘플 수·스위치를 유지한다. 자세가 달라도 수용 프레임 수는 같을 수 있다. 종이 변환 민감도는 장착 병진 하나를 별도로 바꾸며 같은 입력 변위 실험이라고 부르지 않는다.

```bash
pal lesson run sim-teleop-02 --headless --seed 7 --samples 16 --variant 0.8 --output-dir .local/runs/sim-teleop-02/comparison-01 --json
pal lesson check sim-teleop-02 --run-dir .local/runs/sim-teleop-02/baseline-01 --json
pal lesson check sim-teleop-02 --run-dir .local/runs/sim-teleop-02/comparison-01 --json
pal lesson compare sim-teleop-02 --run-dir .local/runs/sim-teleop-02/baseline-01 --comparison-run-dir .local/runs/sim-teleop-02/comparison-01 --output-dir .local/comparisons/sim-teleop-02/comparison-01 --json
```

## Recovery

중단된 에피소드를 보존하고 저장·폐기·중단 상태를 구분합니다. 기존 에피소드를 덮어쓰지 않고 재연결 후에는 로컬 재무장 전 조작을 재개하지 않습니다.

## Checkpoint

### 이해 확인

가장 오래된 수신 시각을 택하는 이유는? 선택 출처가 모두 최신이어야 하기 때문이다. 정확한 합성 4×4 변환이 실물 장착을 인증하는가? 아니다. 실제 보정·스트림 근거는 별도다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review sim-teleop-02 --run-dir .local/runs/sim-teleop-02/baseline-01 --comparison-run-dir .local/runs/sim-teleop-02/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-teleop-02 --run-dir .local/runs/sim-teleop-02/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-enlight-06](./sim-enlight-06.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
