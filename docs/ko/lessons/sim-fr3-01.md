<!-- pal:language:start -->
<p align="right">
  <a href="sim-fr3-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-fr3-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-fr3-01 — FR3 PhysX 관절·TCP 제어

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / fr3` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda` |
| Prerequisites | `core-fr3-09` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

PhysX에서 제어·관측·렌더링을 수행하는 코드입니다. Mac에서 실행 검증하지 않았습니다. import 성공만으로 수업을 통과하지 않습니다.

선행 [개념 장](../concepts/physx.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 가져온 PhysX 관절은 같은 관절·TCP 목표를 어떻게 추종하는가?필요한 경우 [NVIDIA 생태계 실습](../nvidia-ecosystem.md)을 참고하되, 이 수업이 쓰는 실제 엔진·프레임워크는 아래 생산자로 구별한다.

## Learning goals

관절 궤적과 직교 좌표 궤적은 다른 질문이다.

가져온 PhysX 관절은 같은 관절·TCP 목표를 어떻게 추종하는가?

## Preflight

선행 수업: core-fr3-09. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

Ubuntu NVIDIA GPU와 설치된 Isaac Sim이 필요합니다. `pal setup verify --profile isaac --json`으로 점검합니다. 누락 시 capability-unavailable이며 다른 물리 엔진으로 대체하지 않습니다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run sim-fr3-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-fr3-01/baseline-01 --json
```

## Expected

`physx-control.json`, `trace.csv`, `plot.png`, `experiment.json`을 확인합니다. `evaluation.json`의 performance_verified는 학습 성능만 나타냅니다.

## Observe

축·단위·첫/마지막 오차·최댓값을 읽습니다. 렌더링에서 모델과 움직임을 확인하고, payload의 관절 이름·그룹·접촉을 수치와 대조합니다.

### 산출물 읽기

`physx-observations.json`과 `experiment.json` → `payload`의 `tcp_targets_m`, `tcp_errors_m`, `joint_errors_rad`, `initial_q_rad`, `frame`, `control_dt_s`, `joint_reaction_forces`, `contact_force_norms_N`, 별도의 `probe_contact_forces_N`를 읽는다. 반력에는 중력이 포함되며 접촉 센서가 아니다. 궤적 뒤 별도 충돌 프로브 실험에서 양의 유한 PhysX 힘이 나와야 한다. 렌더링이나 USD 가져오기만으로 동역학·접촉 요구를 만족할 수 없다. 실제 GPU 실행은 별도 검증 게이트다.

## How it works

### 직관

관절 궤적과 직교 좌표 궤적은 다른 질문이다. 전반부는 FR3 첫 관절을 사인파로 움직이고 후반부는 TCP에 월드 x/y 평면의 원을 추종하게 한다. 다른 팔의 관절 배열을 옮기지 않고 FR3 모델을 사용한다. 이름 있는 PhysX 관절에 위치 드라이브 목표를 보낸다. TCP 운동·자코비안·관측 상태는 PhysX에서 얻으며 MuJoCo는 고정 소스 메타데이터·내보내기에만 쓴다.

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

## Code connection

### 소스 추적

[`src/pai_lab/lessons/isaac_tasks.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac_tasks.py)

`examples/sim-fr3-01/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[공개 경로 검증](../../verification/robot-paths-2026-11-08.md)은 기존 시뮬레이션 근거와 미검증 외부·장치 실행을 구별한다.

## Try it

### 통제된 비교

샘플 수·시드를 고정하고 `variant`만 1→0.8로 바꾼다. CLI 변수 하나가 관절 파형과 TCP 반지름을 함께 바꾸므로 두 물리 변화를 명시한다. 이득만 바꾸는 실험은 아니다. 단계별 오차·극값을 비교한다. 경로가 작아 오차가 줄어도 제어기 자체가 개선된 것은 아니다.

```bash
pal lesson run sim-fr3-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-fr3-01/comparison-01 --json
pal lesson check sim-fr3-01 --run-dir .local/runs/sim-fr3-01/baseline-01 --json
pal lesson check sim-fr3-01 --run-dir .local/runs/sim-fr3-01/comparison-01 --json
pal lesson compare sim-fr3-01 --run-dir .local/runs/sim-fr3-01/baseline-01 --comparison-run-dir .local/runs/sim-fr3-01/comparison-01 --output-dir .local/comparisons/sim-fr3-01/comparison-01 --json
```

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run sim-fr3-01 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [실행 안내](../READER_GUIDE.md#학습-중단재개와-호스트-이동)를 따릅니다.

## Checkpoint

### 이해 확인

rad와 m인 양은 각각 무엇인가? 관절 오차와 TCP 위치 오차다. FR3 원 추종이 다른 팔·실물 전이를 보장하는가? 아니다. 이 모델·엔진의 궤적 동작만 확인한다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review sim-fr3-01 --run-dir .local/runs/sim-fr3-01/baseline-01 --comparison-run-dir .local/runs/sim-fr3-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-fr3-01 --run-dir .local/runs/sim-fr3-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-fr3-02](./sim-fr3-02.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
