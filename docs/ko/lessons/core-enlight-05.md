<!-- pal:language:start -->
<p align="right">
  <a href="core-enlight-05.md" lang="ko">한국어</a> | <a href="../../en/lessons/core-enlight-05.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-enlight-05 — Enlight PPO 후보와 독립 평가

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / enlight` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-enlight-04, core-rl-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

실제 MuJoCo 팔 상태에서 관절·TCP 오차를 측정합니다. 학습 수업은 팔의 시연 또는 rollout을 사용하고 독립 목표 20개를 평가합니다.

선행 [개념 장](../concepts/reinforcement-learning.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: Enlight PPO 후보는 어떤 독립 기준을 통과하지 못할 수 있는가?

## Learning goals

PPO는 미리 만든 보상 숫자가 아니라 실제 MuJoCo 롤아웃으로 Enlight 정책을 조정한다.

Enlight PPO 후보는 어떤 독립 기준을 통과하지 못할 수 있는가?

## Preflight

선행 수업: core-enlight-04, core-rl-01. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run core-enlight-05 --headless --seed 7 --samples 64 --output-dir .local/runs/core-enlight-05/baseline-01 --json
```

## Expected

`enlight-ppo.json`, `trace.csv`, `plot.png`, `experiment.json`을 확인합니다. `evaluation.json`의 performance_verified는 학습 성능만 나타냅니다.

## Observe

축·단위·첫/마지막 오차·최댓값을 읽습니다. 렌더링에서 모델과 움직임을 확인하고, payload의 관절 이름·그룹·접촉을 수치와 대조합니다.

### 산출물 읽기

`policy.npz`, `training-contract.json`, `evaluation.json`, epoch 체크포인트를 본다. 학습 식별은 모델·소스·엔진·정규화·RNG·최적화·데이터를 연결한다. `evaluation.json`에는 시드 10007의 독립 목표 20에피소드, 개별 `errors_m`, 성공이 있다. 0.01 m 안에서 연속 10스텝을 유지해야 성공이며 16/20 이상이 `performance_verified`다. 실물 허용 오차가 아니다. 유한한 갱신 가중치·정확한 재로딩에도 0/20일 수 있다. 갱신 그래프는 평균 롤아웃 보상이며 유리한 한 점이나 손실 감소로 과제 성능을 인증하지 않는다. `candidate.json`은 실물 호환성을 거짓으로 유지하고 모델 간 전이를 금지한다.

## How it works

### 직관

PPO는 미리 만든 보상 숫자가 아니라 실제 MuJoCo 롤아웃으로 Enlight 정책을 조정한다. 정책 갱신과 독립 성능 통과는 다른 주장이다. 과제는 작은 월드 TCP 거리에 보상하고 변환 전 큰 행동에 벌점을 준다. 모델별 동역학·구동기 의미도 환경의 일부다.

### 계산과 단위

$$
L=\mathbb E[\min(\rho A,\operatorname{clip}(\rho,0.8,1.2)A)],\qquad r=-\|x^*-x\|_2-0.001\sum_j a_j^2
$$

가능도 비율 ρ와 제한 구간은 무차원이며 어드밴티지 A는 보상 점수 스케일이다. 관측 17개와 행동 7개를 사용하며 0.03 tanh(a)가 rad로 변환한다. 보상은 설계 점수이며 J가 아니다. 롤아웃 데이터가 아닌 계산으로 거리 0.02 m, 행동 제곱합 2이면 보상 −0.022다.

```python
import numpy as np
reward = -0.02 - 0.001 * 2
assert np.isclose(reward, -0.022)
```

## Code connection

### 소스 추적

[`src/pai_lab/training.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/training.py)

`examples/core-enlight-05/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[공개 경로 검증](../../verification/robot-paths-2026-11-08.md)은 기존 시뮬레이션 근거와 미검증 외부·장치 실행을 구별한다.

## Try it

### 통제된 비교

모델·시드·샘플 수·독립 목표 집합을 고정하고 `variant`만 1→0.8로 바꿔 학습률 0.01→0.008을 만든다. 학습 진단과 보류 롤아웃 성공을 별도로 비교한다. 이전 체크포인트를 보존한다. 재개는 같은 엔진·데이터·소스·설정을 요구하며 전체 epoch 목표 증가는 별도의 명시 작업이다.

```bash
pal lesson run core-enlight-05 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/core-enlight-05/comparison-01 --json
pal lesson check core-enlight-05 --run-dir .local/runs/core-enlight-05/baseline-01 --json
pal lesson check core-enlight-05 --run-dir .local/runs/core-enlight-05/comparison-01 --json
pal lesson compare core-enlight-05 --run-dir .local/runs/core-enlight-05/baseline-01 --comparison-run-dir .local/runs/core-enlight-05/comparison-01 --output-dir .local/comparisons/core-enlight-05/comparison-01 --json
```

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run core-enlight-05 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [실행 안내](../READER_GUIDE.md#학습-중단재개와-호스트-이동)를 따릅니다.

## Checkpoint

### 이해 확인

최적화 검사 뒤 새로운 목표를 평가하는 이유는? 가중치 갱신은 실행을 증명하며 과제 성공은 독립 측정해야 하기 때문이다. 16/20이 실물 검증 기준인가? 아니다. 이 시뮬레이션 도달 과제의 게이트다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review core-enlight-05 --run-dir .local/runs/core-enlight-05/baseline-01 --comparison-run-dir .local/runs/core-enlight-05/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-enlight-05 --run-dir .local/runs/core-enlight-05/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-enlight-03](./sim-enlight-03.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
