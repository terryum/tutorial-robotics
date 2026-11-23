<!-- pal:language:start -->
<p align="right">
  <a href="mobile-motion.md" lang="ko">한국어</a> | <a href="../../en/concepts/mobile-motion.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 이동 로봇과 모션: 재생, 동역학, 협응 도달

## 움직임을 보는 것과 제어하는 것은 다르다

모션 파일은 관절 위치를 지정할 수 있지만 이를 만드는 힘·균형·접촉까지 설명하지는 않는다. [G1 재생](../lessons/core-g1-01.md)은 이 경계를 가르친다. [G1 GPU 학습](../lessons/sim-g1-01.md)에는 별도 런타임·최적화·독립 평가가 필요하다. [Stretch 3 입문](../lessons/core-stretch3-01.md)은 이름이 정해진 바퀴·리프트·팔 구동기로 시뮬레이션 동역학을 진행한다.

자유 베이스는 관절 상태에 전역 위치와 방향을 추가하며 모터 배열이 아니다. MuJoCo의 자유 관절은 위치 좌표 7개(위치 3, 쿼터니언 4)와 속도 좌표 6개를 가진다. `jnt_qposadr`, `jnt_dofadr`, 구동기 이름으로 배열을 올바르게 다룬다. 자유 베이스 상태 7개를 바퀴 제어에 넣으면 상태 표현과 행동 의미를 혼동하게 된다.

## 제한된 주기는 데이터 예제다

G1 교육 궤적은 힌지 좌표에 사인파를 더한다.

$$
q_j(\phi)=q_{home,j}+0.08\,v\sin\phi,\qquad \phi\in[0,2\pi].
$$

$q_j$와 진폭 0.08의 단위는 rad, $v$는 무차원 `variant`, $\phi$는 무차원 위상이다. 구현은 관절 한도를 적용하고 `mj_forward`를 호출한다. 보행 제어기를 풀거나 토크 기반 보행을 적분하지 않는다. `motion.npz`에는 `(samples, nq)` 형태의 `qpos`, `dt=0.02` s, 관절 이름이 있다. 같은 좌표 재생은 물리적으로 균형이 안 맞아도 정확할 수 있다.

**보행 측정이 아닌 계산 예제**: $\phi=\pi/2$, $v=1$이면 변위 0.08 rad, $v=0.8$이면 0.064 rad이다.

```python
import numpy as np
phase = np.pi / 2
baseline_rad = 0.08 * np.sin(phase)
comparison_rad = 0.08 * 0.8 * np.sin(phase)
assert np.isclose(comparison_rad, 0.064)
assert comparison_rad < baseline_rad
```

[손·모션 구현](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/hands.py)은 `replay_max_error`, `loop_error`를 보고한다. 재생 오차 0은 저장 상태를 정확히 재생했음을 뜻한다. 시작과 끝 위상은 닫힌 주기를 만들지만, 어느 관측도 균형·발 여유·전력·학습 보행 성능을 증명하지 않는다.

## 베이스와 팔의 역할을 구별하며 협응한다

이동형 매니퓰레이터는 베이스를 움직여 팔의 도달 범위를 개선할 수 있다. [embodiments.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/embodiments.py)는 Stretch 제어를 `left_wheel_vel`, `right_wheel_vel`, `lift`, `arm`, 손목 구동기, `gripper`로 구별한다. 바퀴는 속도 명령이며 팔·리프트는 각 모델 구동기의 의미를 따른다. 베이스는 동역학·접촉의 영향을 받는 자유 상태다.

직관을 위한 이상적 차동 구동식은 다음과 같다.

$$
v_{body}=\frac r2(\omega_R+\omega_L),\qquad
\dot\psi=\frac rL(\omega_R-\omega_L).
$$

$r$는 바퀴 반지름(m), $L$은 바퀴 간격(m), $\omega$는 바퀴 각속도(rad/s), $v_{body}$는 전진 속도(m/s), $\dot\psi$는 yaw 속도(rad/s)다. 미끄럼 없는 이상 모델로 같은 부호의 진행과 반대 부호의 회전을 설명한다. 수업에서 이 식으로 $r$, $L$을 추정하지는 않는다.

마지막 단계에서는 시뮬레이션 그리퍼 위치와 베이스 전방 축에서 월드 목표를 만든다. 바퀴로 평면 오차를, 리프트로 수직 오차를 수정한다. `experiment.json`의 `groups`, `free_base`, `actuator_names`, `commands`, `tcp_positions_m`, `reach_target_m`, `reach_errors_m`를 읽는다. 그래프는 도달 목표가 생기기 전에는 TCP 높이, 이후에는 도달 오차를 표시하므로 전체 trace를 하나의 고정 목표 오차 곡선으로 부르면 안 된다.

## 비교와 근거 범위

G1에서는 샘플 수·시드·모델을 유지하고 `variant`만 바꿔 진폭을 줄인다. 힌지 변위는 작아져도 정확한 재생은 유지될 수 있으며 이것이 의도된 불변이다. Stretch에서는 `variant`가 지정 일정 일부와 결과 상태를 바꾸므로, 단일 제어 이득 시험이 아니라 문서의 일정 실험으로 해석한다. [공개 보고서](../../verification/robot-paths-2026-11-08.md)는 작은 도달 오차 감소를 설명하며 mm 정확도나 학습된 이동 정책을 주장하지 않는다.

1. 정확한 재생이 동역학적 가능성을 증명하는가? 아니다. 순기구학은 균형 제어기 없이 지정 상태를 보여줄 수 있다.
2. 구동기 이름을 사용하는 이유는? 자유 베이스·관절 상태 배열과 제어 배열이 다르기 때문이다.
3. 시뮬레이션 오차 감소가 실물 베이스 이동을 허가하는가? 아니다. [실물 게이트](deployment-hardware.md)가 별도로 필요하다.
