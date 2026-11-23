<!-- pal:language:start -->
<p align="right">
  <a href="control-contact.md" lang="ko">한국어</a> | <a href="../../en/concepts/control-contact.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 제어와 접촉: 오차, 힘, 제약

## 로봇 팔에 피드백이 필요한 이유

목표는 도달 요청이며, 필요한 힘까지 정해주지는 않는다. 목표에서 벗어난 관절을 스프링으로 생각하면 오차가 클수록 복원 토크가 커진다. 댐퍼는 속도를 억제해 진동을 줄인다. 목표가 정지해 있어도 중력과 접촉은 힘을 만든다. 이 장은 [관절 PD](../lessons/core-fr3-02.md), [중력 보상](../lessons/core-fr3-03.md), [작업 공간 제어](../lessons/core-fr3-05.md), [접촉](../lessons/core-fr3-06.md)을 연결한다.

관절 위치 $q$와 목표 $q^*$는 각각 7원소 벡터이며 단위는 rad이다. 관절 속도 $\dot q$는 rad/s이다. 정지 목표를 가정한 제어식은 다음과 같다.

$$
\tau_{raw}=K_p(q^*-q)-K_d\dot q,\qquad
\tau=\operatorname{clip}(\tau_{raw},\tau_{min},\tau_{max}).
$$

토크의 단위는 N m, $K_p$는 N m/rad, $K_d$는 N m s/rad이다. 첫 실험에서는 같은 스칼라 이득을 각 관절에 적용한다. 포화는 원소별로 작동한다. 모델 한도 안으로 명령을 제한하지만 안정성이나 실물 안전을 증명하지는 않는다. 오차의 미분을 사용하려면 목표 속도도 필요하지만, 이 구현은 측정 속도를 감쇠한다.

관성 $I$인 독립 관절의 이상적 임계 감쇠는 $K_d=2\sqrt{I K_p}$이다. 코드의 수치 규칙 $2\sqrt{K_p}$는 기준 관성 1 kg m²를 사용한다. 결합된 7관절 팔의 관성은 자세에 따라 달라지므로, 이 규칙은 교육용 선택이며 일반적인 로봇 튜닝 법칙은 아니다.

## 코드까지 따라가는 계산 예제

**측정 결과가 아닌 계산 예제**: 오차 0.18 rad, 속도 0, $K_p=120$이면 원시 토크는 $120\times0.18=21.6$ N m이다. $K_d=21.9089$, 속도 0.1 rad/s이면 19.40911 N m이다. 실제 적용값은 포화로 더 작아질 수 있다.

```python
import numpy as np
error_rad = np.array([0.18])
velocity_rad_s = np.array([0.1])
raw_nm = 120.0 * error_rad - 21.9089 * velocity_rad_s
applied_nm = np.clip(raw_nm, -15.0, 15.0)  # 설명용 한도
assert np.allclose(applied_nm, [15.0])
```

위의 15 N m는 계산 설명용이며 FR3의 실제 한도가 아니다. [physics.py의 `arm_control`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/physics.py)은 `model.jnt_actfrcrange`에서 실제 포화 범위를 읽고 모델 구동기를 비활성화한 뒤 `qfrc_applied`에 쓴다. 제어기가 이중으로 작동하지 않게 하기 위해서다. `control.csv`의 목표·위치·속도·원시 토크·적용 토크는 각 적분 스텝 **이전** 값이다. 그래프의 전체 팔 오차는 25스텝 묶음 뒤에 기록한다. 스텝 이후 위치와 이전 토크를 섞어 식을 검산하면 안 된다.

## 중력, 좌표계와 접촉

정지 상태에서도 스프링 토크가 중력과 균형을 이루면 PD 오차가 남는다. 중력 보상 수업은 MuJoCo의 편향 힘 항인 `data.qfrc_bias`를 더한다. 이 항에는 중력뿐 아니라 속도에 따른 효과도 포함된다. 실물 중력 보정값을 측정한 것은 아니다. 월드 좌표계의 힘 $f$는 병진 자코비안으로 $\tau=J^T f$처럼 관절 토크로 변환한다. $J$는 3×7이고 단위는 m/rad, $f$는 N 단위의 3원소 벡터다. 작업 공간 제어에는 질량 행렬도 사용하므로, 관절 PD의 스칼라 식을 그대로 위치에 적용한 것과 다르다.

접촉에서는 침투와 상대 운동에 제약력이 생긴다. 설명에 유용한 건조 마찰 모델은 $\lVert f_t\rVert\leq\mu f_n$이다. $f_n\geq0$은 법선력, $f_t$는 접선력이며 단위는 N, 마찰계수 $\mu$는 무차원이다. 이는 개념적 경계이며 모든 시뮬레이터가 같은 마찰 풀이기를 쓴다는 뜻은 아니다. MuJoCo 접촉력은 접촉 좌표계로 표현되며 `mj_contactForce`의 첫 성분이 법선력이다. 수업은 이름으로 구분한 프로브·테이블 접촉쌍의 법선 성분 절댓값만 합한다. `normal_force_N`은 시뮬레이션 출력이며 보정된 힘 센서 측정값이 아니다.

## 관찰과 한 변수 비교

`experiment.json`의 `payload`에서 `gain`, `kd`, `target_qpos`, `qpos`, `torque_nm`, `commanded_joint_error`를 확인한다. `checks`는 `payload` 내부가 아니라 `experiment.json` 최상위의 형제 필드로 따로 읽는다. 명령한 첫 관절 오차와 전체 팔 오차 노름은 서로 다른 질문에 답한다. 기존 공개 측정값은 [검증 보고서](../../verification/reader-experience.md)에 있으며, 자신의 근거는 다시 실행해 얻어야 한다.

문서의 PD 비교에서는 `kp`만 120에서 180으로 바꾸고 `kd=21.9089`, 시드, 샘플 수를 유지한다. 복원 명령은 강해지지만 포화와 중력이 관여하면 오차가 비례해서 줄어든다고 단정할 수 없다. 기존 `variant`는 두 이득을 함께 바꾸므로 다른 비교다. 접촉 실험에서는 미끄럼 마찰의 영향이 작으면 마찰계수를 바꿔도 법선력이 거의 같을 수 있다. 불변도 올바른 결과다.

## 이해 확인

1. 속도가 0인데 위치 오차가 남을 수 있는 이유는? 비례 토크가 중력과 균형을 이룰 수 있기 때문이다.
2. 원시 토크와 적용 토크를 함께 보는 이유는? 포화가 피드백 계산값보다 작은 명령을 적용할 수 있기 때문이다.
3. 접촉 오차가 작으면 실물 프로브를 사용할 수 있는가? 아니다. [배포와 실물](deployment-hardware.md)의 도구·좌표계·제어기·실행별 게이트가 별도로 필요하다.
