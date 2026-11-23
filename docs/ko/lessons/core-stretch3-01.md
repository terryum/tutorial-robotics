<!-- pal:language:start -->
<p align="right">
  <a href="core-stretch3-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/core-stretch3-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-stretch3-01 — Stretch 3 베이스·팔·협응 도달

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / stretch3` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-04` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

고정한 모델의 관절·구동기 이름과 주소를 검사하고 실제 움직임·접촉을 기록합니다.

선행 [개념 장](../concepts/mobile-motion.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 베이스와 팔 동작은 도달 목표에서 어떻게 합쳐지는가?

## Learning goals

이동형 매니퓰레이터는 베이스와 팔을 함께 써 도구 오차를 줄일 수 있다.

베이스와 팔 동작은 도달 목표에서 어떻게 합쳐지는가?

## Preflight

선행 수업: core-04. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run core-stretch3-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-stretch3-01/baseline-01 --json
```

## Expected

`stretch-introduction.json`, `trace.csv`, `plot.png`, `experiment.json`을 확인합니다. `evaluation.json`의 performance_verified는 학습 성능만 나타냅니다.

## Observe

축·단위·첫/마지막 오차·최댓값을 읽습니다. 렌더링에서 모델과 움직임을 확인하고, payload의 관절 이름·그룹·접촉을 수치와 대조합니다.

### 산출물 읽기

`groups`, `free_base`, `actuator_names`, `commands`, `tcp_positions_m`, `reach_target_m`, `reach_errors_m`, `qpos`, `qvel`을 읽는다. 초기 trace는 TCP 높이, 목표 생성 뒤에는 도달 오차이며 둘 다 m지만 뜻이 다르다. 검사는 최종 도달 오차 감소·실제 접촉을 요구하며 학습 정책·mm 정확도를 뜻하지 않는다.

## How it works

### 직관

이동형 매니퓰레이터는 베이스와 팔을 함께 써 도구 오차를 줄일 수 있다. 입문 일정은 전진·회전·리프트/팔 운동 뒤 생성한 월드 목표에 대해 평면 바퀴·수직 리프트 피드백을 협응한다. 이름 있는 구동기로 바퀴·신축 팔·손목·그리퍼와 자유 베이스 상태를 구별한다. 지정 시뮬레이션 제어기이며 학습 내비게이션 정책이 아니다.

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

[`src/pai_lab/lessons/embodiments.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/embodiments.py)

`examples/core-stretch3-01/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[공개 경로 검증](../../verification/robot-paths-2026-11-08.md)은 기존 시뮬레이션 근거와 미검증 외부·장치 실행을 구별한다.

## Try it

### 통제된 비교

시드·샘플·소스를 유지하고 `variant`만 바꾼다. 바퀴 일정과 팔 신장 일부가 함께 변하므로 단일 바퀴 이득 실험이 아니라 여러 물리 효과의 일정 배율로 설명한다. 자유 베이스·접촉 설정을 보존하고 요청 명령만 아니라 실제 베이스·TCP 상태를 비교한다.

```bash
pal lesson run core-stretch3-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/core-stretch3-01/comparison-01 --json
pal lesson check core-stretch3-01 --run-dir .local/runs/core-stretch3-01/baseline-01 --json
pal lesson check core-stretch3-01 --run-dir .local/runs/core-stretch3-01/comparison-01 --json
pal lesson compare core-stretch3-01 --run-dir .local/runs/core-stretch3-01/baseline-01 --comparison-run-dir .local/runs/core-stretch3-01/comparison-01 --output-dir .local/comparisons/core-stretch3-01/comparison-01 --json
```

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run core-stretch3-01 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [경로 안내](../paths.md)를 따릅니다.

## Checkpoint

### 이해 확인

자유 베이스 쿼터니언을 구동기 제어에 쓰지 않는 이유는? 상태 표현이며 바퀴·팔 행동이 아니기 때문이다. 베이스 이동이 내비게이션을 증명하는가? 아니다. 작은 지정 시뮬레이션 일정이다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review core-stretch3-01 --run-dir .local/runs/core-stretch3-01/baseline-01 --comparison-run-dir .local/runs/core-stretch3-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-stretch3-01 --run-dir .local/runs/core-stretch3-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-stretch3-01](./sim-stretch3-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
