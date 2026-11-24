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

<a id="gravity-and-bias" name="gravity-and-bias"></a>

### 정지 토크에서 운동방정식으로

팔을 공중에서 정지시키면 $\dot q=\ddot q=0$입니다. 접촉과 수동 토크를 무시하면 모터가 그 자세에서의 중력항 $g(q)$만큼 토크를 공급해야 합니다. 위 PD 계산처럼 오차가 비례 토크를 만들기 때문에, PD만으로 중력과 균형을 이루면 위치 오차가 남을 수 있습니다. 팔이 움직이거나 외부에서 힘을 받으면 관절 운동방정식에 항을 추가합니다.

$$
M(q)\ddot q+c(q,\dot q)+g(q)=\tau+\tau_{\mathrm{other}}.
$$

$M(q)$는 현재 자세에서의 7×7 관절 공간 관성 행렬 (kg·m²)입니다. $\ddot q$ (rad/s²)를 곱하면 관절 가속에 필요한 토크가 나옵니다. 비대각 성분은 한 관절의 가속이 다른 관절에 필요한 토크에도 영향을 줄 수 있음을 나타냅니다. $c$는 코리올리 및 원심 효과, $g$는 중력의 기여분입니다. $\tau$는 제어 토크이고, $\tau_{\mathrm{other}}$에는 접촉과 그 밖의 외력이 만드는 관절 토크, 수동 토크가 들어갑니다. 운동방정식의 각 벡터 항은 N·m입니다. [MuJoCo 운동방정식](https://mujoco.readthedocs.io/en/stable/computation/index.html#general-framework)

중력 보상 수업은 $c+g$를 담은 `data.qfrc_bias`를 PD 요청값에 더하고 관절별 한계를 적용합니다. 위 계산처럼 어떤 관절에서 속도가 0이고 오차가 0.18 rad일 때, PD 토크 21.6 N·m에 편향력 4 N·m를 더하면 한계를 적용하기 전 25.6 N·m입니다. 같은 설명용 한계 ±15 N·m 안에서 두 경우의 적용값은 모두 15 N·m입니다. 이 계산은 포화 때문에 보상 항을 추가해도 실제로 적용한 토크가 그대로일 수 있음을 보여 줍니다.

<a id="jacobian-power" name="jacobian-power"></a>

### 자코비안과 일률

병진 자코비안 $J$ (3×7, m/rad)는 관절 속도 $\dot q$ (rad/s)를 말단 사이트의 병진 속도 $v=J\dot q$ (m/s)로 바꿉니다. 같은 사이트에 작용하고 같은 좌표계로 표현한 힘 $f$ (N)는 $f^\top v$ (W)의 일률을 냅니다. 관절 쪽의 일률 $\tau_f^\top\dot q$와 같아야 하므로, 모든 $\dot q$에 대해 $f^\top J\dot q=\tau_f^\top\dot q$이고 토크 기여분은 $\tau_f=J^\top f$입니다. 수업의 작업 공간 제어기는 현재 자세에서의 $M(q)$와 $J$를 사용해 병진 가속도 요청에 해당하는 힘을 계산합니다.

회전까지 다룰 때는 힘 $f$와 같은 점에 대한 모멘트 $m$ (N·m)를 렌치라는 6원소 벡터에 담습니다. 같은 점의 병진 속도 $v$와 각속도 $\omega$ (rad/s)를 같은 좌표계로 표현하면 일률은 $f^\top v+m^\top\omega$입니다. 6행 자코비안으로 두 속도를 함께 계산할 때는 자코비안의 행과 렌치 성분의 순서를 맞춥니다. 좌표축 방향을 유지하면서 모멘트의 기준점을 옮기려면, 새 기준점에서 기존 기준점까지의 벡터 $r$과 힘의 외적 $r\times f$를 기존 모멘트에 더합니다. [Modern Robotics의 자코비안과 렌치](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-2-statics-of-open-chains/)

<a id="contact-force-and-friction" name="contact-force-and-friction"></a>

### 접촉력과 마찰

접촉면에 수직인 압축 법선력을 $f_n\geq0$, 접촉면을 따라 작용하는 접선력을 $f_t$라고 합니다. 둘 다 N 단위이며, 이상적인 쿨롱 모델에서 정지 마찰의 범위는 $\lVert f_t\rVert\leq\mu f_n$입니다. 마찰계수 $\mu$는 무차원입니다. 미끄러짐을 막는 데 이 범위를 넘는 힘이 필요하면 미끄럼이 일어납니다. 이때 단일 마찰계수를 쓰는 모델에서는 접선력 크기가 $\mu f_n$이며 상대 미끄럼 속도의 반대 방향으로 작용합니다. 파지에 이 식을 적용하려면 각 접촉점에서 허용되는 힘을 물체의 공통 기준점에서 모멘트로도 환산해, 외부 힘과 모멘트에 맞설 수 있는지 확인합니다. [Modern Robotics의 마찰 원뿔](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-1-friction/)

MuJoCo는 접촉 모델에 따라 제약력을 풉니다. `mj_contactForce`가 반환하는 접촉 좌표계의 첫 성분은 법선력입니다. 프로브 수업의 `normal_force_N`은 지정한 프로브·테이블 접촉쌍의 법선 성분 절댓값을 합한 시뮬레이션 출력입니다. [MuJoCo 접촉력 API](https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html#mj-contactforce)

## 관찰과 한 변수 비교

`experiment.json`의 `payload`에서 `gain`, `kd`, `target_qpos`, `qpos`, `torque_nm`, `commanded_joint_error`를 확인한다. `checks`는 `payload` 내부가 아니라 `experiment.json` 최상위의 형제 필드로 따로 읽는다. 명령한 첫 관절 오차와 전체 팔 오차 노름은 서로 다른 질문에 답한다. 기존 공개 측정값은 [검증 보고서](../../verification/reader-experience.md)에 있으며, 자신의 근거는 다시 실행해 얻어야 한다.

문서의 PD 비교에서는 `kp`만 120에서 180으로 바꾸고 `kd=21.9089`, 시드, 샘플 수를 유지한다. 복원 명령은 강해지지만 포화와 중력이 관여하면 오차가 비례해서 줄어든다고 단정할 수 없다. 기존 `variant`는 두 이득을 함께 바꾸므로 다른 비교다. 접촉 실험에서는 미끄럼 마찰의 영향이 작으면 마찰계수를 바꿔도 법선력이 거의 같을 수 있다. 불변도 올바른 결과다.

## 이해 확인

1. 속도가 0인데 위치 오차가 남을 수 있는 이유는? 비례 토크가 중력과 균형을 이룰 수 있기 때문이다.
2. 원시 토크와 적용 토크를 함께 보는 이유는? 포화가 피드백 계산값보다 작은 명령을 적용할 수 있기 때문이다.
3. 접촉 오차가 작으면 실물 프로브를 사용할 수 있는가? 아니다. [배포와 실물](deployment-hardware.md)의 도구·좌표계·제어기·실행별 게이트가 별도로 필요하다.
