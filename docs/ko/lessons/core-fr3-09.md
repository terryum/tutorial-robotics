<!-- pal:language:start -->
<p align="right">
  <a href="core-fr3-09.md" lang="ko">한국어</a> | <a href="../../en/lessons/core-fr3-09.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-fr3-09 — FR3 관절·TCP 궤적 추종

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / fr3` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-fr3-06` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

실제 MuJoCo 팔 상태에서 관절·TCP 오차를 측정합니다. 학습 수업은 팔의 시연 또는 rollout을 사용하고 독립 목표 20개를 평가합니다.

선행 [개념 장](../concepts/control-contact.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 관절 궤적 오차와 TCP 궤적 오차는 어떻게 다른가?

## Learning goals

관절 궤적과 직교 좌표 궤적은 다른 질문이다.

관절 궤적 오차와 TCP 궤적 오차는 어떻게 다른가?

## Preflight

선행 수업: core-fr3-06. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run core-fr3-09 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-09/baseline-01 --json
```

## Expected

`trajectory.json`, `trace.csv`, `plot.png`, `experiment.json`을 확인합니다. `evaluation.json`의 performance_verified는 학습 성능만 나타냅니다.

## Observe

축·단위·첫/마지막 오차·최댓값을 읽습니다. 렌더링에서 모델과 움직임을 확인하고, payload의 관절 이름·그룹·접촉을 수치와 대조합니다.

### 산출물 읽기

`experiment.json` → `payload`의 `joint_targets_rad`, `joint_errors_rad`, `tcp_targets_m`, `tcp_rmse_m`, `time_s`, `initial_q_rad`, `frame`, `control_dt_s`, 접촉 배열을 읽는다. `tcp_rmse_m`는 후반부만 평균하지만 그래프 오차는 두 단계를 포함한다. 기준 개수는 max(160,64×4)=256이며 제어 명령마다 물리 10스텝을 진행한다. MuJoCo 접촉 필드는 norm 같은 이름이지만 모든 접촉 법선력 절댓값의 합이다.

## How it works

### 직관

관절 궤적과 직교 좌표 궤적은 다른 질문이다. 전반부는 FR3 첫 관절을 사인파로 움직이고 후반부는 TCP에 월드 x/y 평면의 원을 추종하게 한다. 다른 팔의 관절 배열을 옮기지 않고 FR3 모델을 사용한다. FR3 위치 구동기에 관절 목표를 보낸다.

### 계산과 단위

$$
x^*(\theta)=x_0+0.012v[\sin\theta,1-\cos\theta,0]^T,\qquad e_i=\|x_i^*-x_i\|_2
$$

x는 월드 m 단위 3원소, 관절 목표는 rad 단위 7각도, v는 무차원 `variant`다. 원의 반지름은 0.012v m이고 x0에서 중심이 이동해 θ=π에서 y 변위는 0.024v m이다. 전반부 관절 진폭은 0.06v rad다. 측정 실행이 아닌 계산으로 v=0.8이면 반지름 0.0096 m, 관절 진폭 0.048 rad이다.

```python
import numpy as np
v = 0.8
assert np.isclose(0.012 * v, 0.0096)
assert np.isclose(0.06 * v, 0.048)
```

### 경로의 중간도 확인해야 하는 이유

[2관절 평면 팔의 경로 계산](../concepts/kinematics.md#configuration-and-clearance)에서 둘째 관절을 0 rad에 두고 첫째 관절을 $-\pi/4$ rad에서 $+\pi/4$ rad까지 움직입니다. 두 끝에서는 링크와 원판 사이에 약 0.254 m의 여유가 있지만, 첫째 관절이 0 rad를 지나는 중간 자세에서는 첫 링크가 원판 중심을 지나므로 충돌 여유가 $-0.10$ m입니다.

FR3의 `tcp_rmse_m`은 후반부 원 추종 단계에서 월드 좌표계 TCP 위치 오차의 제곱을 평균한 뒤 제곱근을 취한 값입니다. 이 값은 목표점들의 추종 품질을 m 단위로 요약합니다. 경로의 충돌 여유를 구하려면 경로를 따라 링크 형상과 주변 장애물까지의 거리를 별도로 확인해야 합니다. `contact_counts`와 `contact_force_norms_N`은 기록된 표본에서 감지한 접촉과 법선력 합을 읽는 데 씁니다. 표본 사이를 포함한 경로 전체의 최소 여유는 별도로 검증해야 합니다.

## Code connection

### 소스 추적

[`src/pai_lab/lessons/arm.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py)

`examples/core-fr3-09/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[공개 경로 검증](../../verification/robot-paths-2026-11-08.md)은 기존 시뮬레이션 근거와 미검증 외부·장치 실행을 구별한다.

## Try it

### 통제된 비교

샘플 수·시드를 고정하고 `variant`만 1→0.8로 바꾼다. CLI 변수 하나가 관절 파형과 TCP 반지름을 함께 바꾸므로 두 물리 변화를 명시한다. 이득만 바꾸는 실험은 아니다. 단계별 오차·극값을 비교한다. 경로가 작아 오차가 줄어도 제어기 자체가 개선된 것은 아니다.

```bash
pal lesson run core-fr3-09 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/core-fr3-09/comparison-01 --json
pal lesson check core-fr3-09 --run-dir .local/runs/core-fr3-09/baseline-01 --json
pal lesson check core-fr3-09 --run-dir .local/runs/core-fr3-09/comparison-01 --json
pal lesson compare core-fr3-09 --run-dir .local/runs/core-fr3-09/baseline-01 --comparison-run-dir .local/runs/core-fr3-09/comparison-01 --output-dir .local/comparisons/core-fr3-09/comparison-01 --json
```

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run core-fr3-09 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [실행 안내](../READER_GUIDE.md#학습-중단재개와-호스트-이동)를 따릅니다.

## Checkpoint

### 이해 확인

기록에서 관절 오차와 TCP 위치 오차의 단위는 각각 무엇인가요? 관절 오차는 rad, TCP 위치 오차는 m입니다.

두 실행에서 `tcp_rmse_m`이 더 작은 쪽을 고릅니다. 이 값으로 어느 실행의 원 추종이 더 정확했는지, 그리고 어느 경로에 충돌 여유가 더 큰지 각각 판단할 수 있나요? `tcp_rmse_m`은 후반부 TCP 위치 오차를 비교할 근거입니다. 평면 팔 예제에서 경로 양 끝의 여유가 중간 자세의 충돌을 알려 주지 못했듯, FR3 경로의 최소 여유를 알려면 경로 전체에서 링크와 장애물 사이의 거리를 따로 확인해야 합니다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review core-fr3-09 --run-dir .local/runs/core-fr3-09/baseline-01 --comparison-run-dir .local/runs/core-fr3-09/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-fr3-09 --run-dir .local/runs/core-fr3-09/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-10](./core-fr3-10.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
