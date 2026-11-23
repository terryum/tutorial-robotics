<!-- pal:language:start -->
<p align="right">
  <a href="reinforcement-learning.md" lang="ko">한국어</a> | <a href="../../en/concepts/reinforcement-learning.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 강화학습: 학습 실행과 쓸 수 있는 정책

## 행동의 결과로 배운다

피드백 제어에서는 행동 규칙을 직접 쓴다. 강화학습에서는 행동의 결과로 정책을 조정한다. 시간 $t$의 관측 $o_t$를 정책 $\pi_\theta$에 넣고, 행동 $a_t$로 시뮬레이션 상태를 바꾼 뒤 보상 $r_t$로 전이를 평가한다. 환경은 과제가 종료되었는지, 시간 한도로 잘렸는지도 반환한다. 시드는 소프트웨어와 모델이 고정된 환경에서 난수를 재현하도록 돕지만 일반화의 증거는 아니다.

[최소 PPO](../lessons/core-rl-01.md)는 진자 관측 2개와 행동 1개를 사용한다. [FR3 도달](../lessons/core-fr3-07.md)은 관측 17개를 사용한다. 홈 대비 관절 변위 7개(rad), 관절 속도에 0.1을 곱한 값 7개, 월드 목표 오차에 10을 곱한 값 3개다. 고정 수치 스케일은 정책 입력의 크기를 조절하며 물리 단위 자체를 없애지는 않는다. 편향 특성을 추가하면 입력은 18원소, FR3 가중치는 18×7이다.

[learning.py의 `Reach.step`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/learning.py)은 제한 없는 7원소 행동 $a$를 관절 위치 목표로 바꾼다.

$$
q_{target}=\operatorname{clip}(q+0.03\tanh(a),q_{min},q_{max}),\qquad
r=-\lVert x^*-x\rVert_2-0.001\sum_j a_j^2.
$$

관절 변화량은 rad, 거리는 m이다. 보상은 선택한 수치 가중치로 설계한 점수이며 물리적 에너지가 아니다. 벌점은 변환 전 행동 $a$로 계산하고 로봇에는 제한된 변화량이 전달된다. 제어 전이 한 번마다 시뮬레이터가 10스텝 진행한다. `Reach`는 64전이 후 시간 종료되지만, 뒤의 `arm.py` 명명 관절 환경은 160전이를 허용한다. 에피소드 길이를 비교하기 전에 실제 환경을 읽는다.

## PPO가 정책 갱신을 제한하는 이유

가우스 정책은 평균 주변에서 행동을 샘플링한다. 한 배치 뒤 정책이 너무 크게 바뀌면 기존 샘플이 새 정책의 행동을 잘 대표하지 못한다. PPO는 가능도 비율 $\rho_t=\pi_\theta(a_t|o_t)/\pi_{old}(a_t|o_t)$을 사용하고 갱신 유인을 제한한다.

$$
L=\mathbb E\left[\min(\rho_t A_t,\operatorname{clip}(\rho_t,0.8,1.2)A_t)\right].
$$

$A_t$는 해당 행동이 기대보다 얼마나 나았는지의 추정값이다. 이 목적함수는 갱신을 위한 것이며 과제 성공률이 아니다. 구현은 어드밴티지를 정규화하고, 롤아웃마다 정책 갱신을 4회 수행하며 기울기 노름을 제한한다. 학습 중 평균 보상은 오르내릴 수 있다.

어드밴티지 재귀식은 실제 과제 종료와 수집 경계를 구별한다.

$$
\delta_t=r_t+\gamma V(o_{t+1})(1-d_t)-V(o_t),\qquad
A_t=\delta_t+\gamma\lambda(1-b_t)A_{t+1}.
$$

$d_t$는 과제 종료, $b_t$는 종료 **또는** 시간 한도를 뜻하며 $\gamma=0.99$, $\lambda=0.95$이다. 시간 한도에서는 다음 상태 가치를 사용할 수 있지만 리셋된 다음 에피소드의 어드밴티지를 이어받으면 안 된다. **측정 실행이 아닌 계산 예제**: 보상 1, 다음 가치 2, 현재 가치 0, 설명용 $\gamma=0.5$이면 시간 한도의 값은 2, 실제 종료의 값은 1이다.

```python
import numpy as np
from pai_lab.lessons.learning import generalized_advantage
adv = generalized_advantage(
    np.array([1., 1.]), np.array([0., 0.]), np.array([2., 2.]),
    np.array([False, True]), np.array([True, True]), gamma=0.5,
)
assert np.allclose(adv, [2., 1.])
```

## 저장된 근거에서 세 주장을 구별한다

[core-fr3-08](../lessons/core-fr3-08.md)은 `policy.npz`, `policy-contract.json`, `experiment.json`, `evaluation.json`을 저장한다. 먼저 `parameter_delta`와 `reload_max_error`를 확인한다. 이는 최적화 갱신과 정확한 다시 불러오기를 검증한다. 다음으로 학습 보상 그래프를 평가로 취급하지 말고 독립 평가를 확인한다.

[arm.py의 `evaluate`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py)는 시드 10007로 목표 에피소드 20개를 평가한다. 0.01 m 안에서 연속 10 제어 스텝을 유지하면 성공이며, 16개 이상 성공해야 `performance_verified`가 참이다. 이는 시뮬레이션 과제 기준이며 `hardware_tolerance=False`로 명시한다. 유한한 값으로 갱신된 정책도 모든 목표에서 실패할 수 있다. [공개 경로 보고서](../../verification/robot-paths-2026-11-08.md)의 짧은 Enlight PPO가 이런 사례이며, 과제를 해결했다고 보고하지 않는다.

한 변수 비교에서는 시드·모델·롤아웃 수·평가 목표를 유지하고 문서의 학습률 배율만 바꾼다. 최적화 진단과 독립 성공 수를 함께 비교한다. 큰 학습률은 결과를 개선할 수도 망칠 수도 있으므로 유리한 보상 한 점으로 결론을 선택하지 않는다. [데이터와 모방학습](data-imitation.md)은 지도학습 기준선을, [배포](deployment-hardware.md)는 추가 게이트를 소개한다.

## 이해 확인

1. 가중치가 바뀌면 유용한 정책인가? 학습 코드 실행은 증명하지만 유용성은 독립 과제 평가가 필요하다.
2. 시간 한도에서 다음 가치를 유지하는 이유는? 수집이 끝났어도 과제 자체가 끝난 것은 아닐 수 있기 때문이다.
3. 16/20 통과로 실물 팔이 준비되는가? 아니다. 기준은 이 시뮬레이션 과제에 한정된다.

GPU 벤더 수업에서 `samples`는 학습 반복 수와 평가 지평을 함께 바꿀 수 있다. 샘플 수 비교는 예산·지평의 결합 변경으로 해석하고 두 효과를 명시한다. 최적화만 생각하려면 둘을 고정하고 지원하는 학습률 입력만 바꾼다. [NVIDIA 생태계](../nvidia-ecosystem.md)는 Isaac Lab 학습, Sim 엔진 검사, GR00T 모델 실험을 구별한다.
