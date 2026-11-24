<!-- pal:language:start -->
<p align="right">
  <a href="sim-stretch3-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-stretch3-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-stretch3-01 — Stretch 3 PhysX 입문

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / stretch3` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda` |
| Prerequisites | `core-stretch3-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

PhysX에서 제어·관측·렌더링을 수행하는 코드입니다. Mac에서 실행 검증하지 않았습니다. import 성공만으로 수업을 통과하지 않습니다.

선행 [개념 장](../concepts/physx.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: PhysX로 가져온 Stretch의 베이스·팔 동작을 어떻게 검증하는가?필요한 경우 [NVIDIA 생태계 실습](../nvidia-ecosystem.md)을 참고하되, 이 수업이 쓰는 실제 엔진·프레임워크는 아래 생산자로 구별한다.

## Learning goals

PhysX 가져오기 뒤 Stretch는 자유 베이스와 이름 있는 바퀴·리프트·신축 관절 제어를 보존해야 한다.

PhysX로 가져온 Stretch의 베이스·팔 동작을 어떻게 검증하는가?

## Preflight

선행 수업: core-stretch3-01. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

Ubuntu NVIDIA GPU와 설치된 Isaac Sim이 필요합니다. `pal setup verify --profile isaac --json`으로 점검합니다. 누락 시 capability-unavailable이며 다른 물리 엔진으로 대체하지 않습니다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run sim-stretch3-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-stretch3-01/baseline-01 --json
```

## Expected

`stretch-physx.json`, `trace.csv`, `plot.png`, `experiment.json`을 확인합니다. `evaluation.json`의 performance_verified는 학습 성능만 나타냅니다.

## Observe

축·단위·첫/마지막 오차·최댓값을 읽습니다. 렌더링에서 모델과 움직임을 확인하고, payload의 관절 이름·그룹·접촉을 수치와 대조합니다.

### 산출물 읽기

`base_positions_m`, `joint_states`, `free_base_required`, `couplings_required`, 엔진·소스를 읽는다. 베이스 이동 0.005 m 초과·관절 이동 0.01 초과 및 필요한 동적 결합 검사를 요구한다. `commands`의 일반 목표 배열은 별도 바퀴·리프트 명령을 담지 않으므로 전체 재생 로그로 보기 전에 이름 있는 소스 명령을 읽는다.

## How it works

### 직관

PhysX 가져오기 뒤 Stretch는 자유 베이스와 이름 있는 바퀴·리프트·신축 관절 제어를 보존해야 한다. 바퀴 속도와 팔 위치 명령은 다른 구동기 의미다. 현재 PhysX 일정은 전진·회전·팔 운동을 보이며 MuJoCo 입문의 마지막 피드백 도달 제어기를 구현하지 않는다. 가져오기만으로 같은 도달 오차 개선을 약속하면 안 된다.

### 계산과 단위

$$
v=\frac r2(\omega_R+\omega_L),\qquad \dot\psi=\frac rL(\omega_R-\omega_L)
$$

이 이상적 무미끄럼 차동식은 방향을 설명하며 피팅된 시뮬레이터 모델이 아니다. 반지름 r·간격 L은 m, 바퀴 각속도는 rad/s, 몸체 속도 m/s, yaw 속도 rad/s이다. Stretch 기하 측정이 아닌 예제로 r=0.1 m, L=0.4 m, 양 바퀴 0.2 rad/s이면 v=0.02 m/s, 회전은 0이다.

```python
import numpy as np
r_m, separation_m = 0.1, 0.4
left_rad_s = right_rad_s = 0.2
assert np.isclose(r_m * (left_rad_s + right_rad_s) / 2, 0.02)
assert r_m * (right_rad_s - left_rad_s) / separation_m == 0
```

## Code connection

### 소스 추적

[`src/pai_lab/lessons/isaac_tasks.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac_tasks.py)

`examples/sim-stretch3-01/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

## Try it

### 통제된 비교

시드·샘플·소스를 유지하고 `variant`만 바꾼다. 바퀴 일정과 팔 신장 일부가 함께 변하므로 단일 바퀴 이득 실험이 아니라 여러 물리 효과의 일정 배율로 설명한다. 자유 베이스·접촉 설정을 보존하고 요청 명령만 아니라 실제 베이스·TCP 상태를 비교한다.

```bash
pal lesson run sim-stretch3-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-stretch3-01/comparison-01 --json
pal lesson check sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/baseline-01 --json
pal lesson check sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/comparison-01 --json
pal lesson compare sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/baseline-01 --comparison-run-dir .local/runs/sim-stretch3-01/comparison-01 --output-dir .local/comparisons/sim-stretch3-01/comparison-01 --json
```

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run sim-stretch3-01 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [실행 안내](../READER_GUIDE.md#학습-중단재개와-호스트-이동)를 따릅니다.

## Checkpoint

### 이해 확인

자유 베이스 쿼터니언을 구동기 제어에 쓰지 않는 이유는? 상태 표현이며 바퀴·팔 행동이 아니기 때문이다. 베이스 이동이 내비게이션을 증명하는가? 아니다. 작은 지정 시뮬레이션 일정이다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/baseline-01 --comparison-run-dir .local/runs/sim-stretch3-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[hw-enlight-04](./hw-enlight-04.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
