<!-- pal:language:start -->
<p align="right">
  <a href="sim-enlight-06.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-enlight-06.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-enlight-06 — Enlight 팔 텔레오퍼레이션과 수집

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / enlight` |
| Legacy alias | `None` |
| Platforms | `linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-enlight-05, sim-teleop-02` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

수집은 시뮬레이션 데이터 루프를 잇는다. 합성 손목 자세 → Enlight 전용 IK → 제한 팔 행동 → 영상/상태/목표 에피소드 → 모델 지정 BC 입력 순서다. 헤드셋·실물 팔은 연결하지 않는다. 합성 3에피소드를 저장해 분할마다 전체 에피소드 하나를 둔다. 그리퍼는 unavailable이며 사람 시연을 주장하지 않는다.

선행 [개념 장](../concepts/data-imitation.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 물리 동작 승인 없이 시뮬레이션 Enlight 에피소드를 어떻게 시점 정보와 함께 수집하는가?

## Learning goals

수집은 시뮬레이션 데이터 루프를 잇는다.

물리 동작 승인 없이 시뮬레이션 Enlight 에피소드를 어떻게 시점 정보와 함께 수집하는가?

## Preflight

카탈로그 플랫폼·역량에 맞는 호스트를 사용하며 컴퓨터 이름이 준비를 허가하지 않는다. `core-teleop-01`은 macOS arm64·Linux x86_64를 지원하고 이후 선택 입력·수집 수업은 Linux x86_64다. [VR 준비](../setup/vr-teleop.md), [장비 단계](../equipment-stages.md), [검증 기록](../../verification/vr-teleop-2026-11-13.md)의 합성·실제 구별을 읽는다. 장치·보정·원시 에피소드는 무시되는 `.local/`에 두며 벤더 자동 설치·장치 동의를 뜻하지 않는다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run sim-enlight-06 --headless --seed 7 --samples 16 --output-dir .local/runs/sim-enlight-06/baseline-01 --json
```

## Expected

실제 장치 검증 보고서가 아니라 합성 재생·수집 근거를 기대한다. 카탈로그 산출물·`experiment.json`·`trace.csv`·`plot.png`·에피소드 매니페스트를 확인한다. 저장 3에피소드와 폐기·중단 기록으로 생명주기·출처를 보존한다. 실제 60초 장치 속도·추적·가림·재연결 검증은 별도 실제 입력 게이트다.

## Observe

기록한 입력과 적용 목표를 따로 확인합니다. 합성 timestamp는 테스트용으로 생성한 시각입니다.

### 산출물 읽기

`collected-demonstrations.json`은 model=enlight·provenance=synthetic·17원소 관측·변환 전 행동 7개·에피소드 분할을 기록한다. `episodes/*/frames.jsonl`은 이름 있는 행동 전 상태/목표와 64×64 RGB 영상을 저장하며 상태·카메라·합성 입력 시계를 명시한다. 적용 행동 뒤 TCP x를 그래프로 기록한다. 요약 지표는 전체 3D 자세 오차가 아니라 최대 x 절대 오차다. `human_demonstration=False`, `gripper_verified=False`, `command_publishers=0`을 보존한다.

## How it works

### 직관

수집은 시뮬레이션 데이터 루프를 잇는다. 합성 손목 자세 → Enlight 전용 IK → 제한 팔 행동 → 영상/상태/목표 에피소드 → 모델 지정 BC 입력 순서다. 헤드셋·실물 팔은 연결하지 않는다. 합성 3에피소드를 저장해 분할마다 전체 에피소드 하나를 둔다. 그리퍼는 unavailable이며 사람 시연을 주장하지 않는다.

### 계산과 단위

$$
\Delta q=J^T(JJ^T+0.001I_6)^{-1}e,\qquad a=\operatorname{arctanh}(\operatorname{clip}((q^*-q)/0.03,-0.999,0.999))
$$

쌓은 J는 6×7이다. 위치 행은 관절 rad를 월드 m로, 회전 행은 회전벡터 rad로 대응한다. e는 위치·방향을 합치므로 혼합 스케일은 교육 수치 선택이며 물리적으로 균일한 노름이 아니다. IK 증분은 ±0.02 rad·모델 한도로 제한한다. 장치 데이터가 아닌 계산으로 목표 변화 0.003 rad이면 변환 전 행동 arctanh(0.1)≈0.100335다.

```python
import numpy as np
a = np.arctanh(0.003 / 0.03)
assert np.isclose(0.03 * np.tanh(a), 0.003)
```

## Code connection

### 소스 추적

[`src/pai_lab/lessons/teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/teleop.py)

`examples/sim-enlight-06/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[`teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop.py), [`teleop_recording.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_recording.py), [VR 검증 기록](../../verification/vr-teleop-2026-11-13.md)도 읽는다.

## Try it

### 통제된 비교

`variant`만 1→0.8로 바꾸면 합성 손목 x 사인 진폭이 0.005→0.004 m가 되며 방향·샘플·20 ms 일정은 같다. 목표·스텝 뒤 x와 에피소드를 비교한다. 이후 선택 BC는 명시 시연 파일을 사용한 새 학습이며 독립 평가를 따로 읽는다. 공개 짧은 수집 BC 예제는 0/20이며 배포 가능 성능이 아니다.

```bash
pal lesson run sim-enlight-06 --headless --seed 7 --samples 16 --variant 0.8 --output-dir .local/runs/sim-enlight-06/comparison-01 --json
pal lesson check sim-enlight-06 --run-dir .local/runs/sim-enlight-06/baseline-01 --json
pal lesson check sim-enlight-06 --run-dir .local/runs/sim-enlight-06/comparison-01 --json
pal lesson compare sim-enlight-06 --run-dir .local/runs/sim-enlight-06/baseline-01 --comparison-run-dir .local/runs/sim-enlight-06/comparison-01 --output-dir .local/comparisons/sim-enlight-06/comparison-01 --json
```

## Recovery

중단된 에피소드를 보존하고 저장·폐기·중단 상태를 구분합니다. 기존 에피소드를 덮어쓰지 않고 재연결 후에는 로컬 재무장 전 조작을 재개하지 않습니다.

## Checkpoint

### 이해 확인

에피소드를 분리하는 이유는? 인접 수집 상태가 보류 데이터로 누출될 수 있기 때문이다. 작은 수집 x 오차가 BC의 새 목표 도달을 보장하는가? 아니다. 수집과 정책 평가는 다른 질문이다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review sim-enlight-06 --run-dir .local/runs/sim-enlight-06/baseline-01 --comparison-run-dir .local/runs/sim-enlight-06/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-enlight-06 --run-dir .local/runs/sim-enlight-06/baseline-01 --json
```

수집을 확인한 뒤 선택 후속 학습을 할 수 있다. 별도 학습 산출물이며 다른 수업 완료는 아니다:

```bash
pal train run --model enlight --algorithm bc --epochs 4 --demonstrations .local/runs/sim-enlight-06/baseline-01/collected-demonstrations.json --output-dir .local/teleop-bc-unique --json
```

<!-- pal:navigation:start -->
## Next lesson

과정 끝

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
