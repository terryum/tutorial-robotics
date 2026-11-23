<!-- pal:language:start -->
<p align="right">
  <a href="robot-hands.md" lang="ko">한국어</a> | <a href="../../en/concepts/robot-hands.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 로봇 손: 기하, 시너지, 접촉 관측

## 손끝이 비슷해도 관절은 다르다

팔은 도구를 위치시키고, 손은 물체 주변에서 많은 관절을 조정한다. 손 비교는 같은 길이 배열만으로 할 수 없다. 관절 축·범위·구동기 수·결합·tendon 동작·손끝 좌표계가 다르다. [Wuji 자세](../lessons/core-wuji-01.md), [가상 촉각](../lessons/core-wuji-02.md), [Wuji–Sharpa 비교](../lessons/core-dexterity-01.md), [리타게팅](../lessons/core-dexterity-02.md), [Shadow Hand 입문](../lessons/core-shadow-01.md)에서 이를 관찰한다.

시너지는 많은 관절 좌표를 소수 제어로 줄인다. Wuji의 단일 진폭 예제는 다음과 같다.

$$
q=\operatorname{clip}(\alpha s,q_{min},q_{max}).
$$

$q,s\in\mathbb R^{20}$은 rad 단위이고 진폭 $\alpha$는 무차원이다. [hands.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/hands.py)는 이름에 abduction이 있는 관절에 0.3, 나머지에 0.6의 시너지 값을 준다. `variant` 배율 전에 진폭 0, 0.5, 1이 열림·반쯤·닫힘 자세다. 지정한 모델 자세이며 학습된 파지 전략이나 검증된 파지 안정성이 아니다.

**손 측정이 아닌 계산 예제**: 관절 하나의 $s_j=0.6$ rad, $\alpha=0.5$이면 포화 전 목표는 0.3 rad이다.

```python
import numpy as np
synergy_rad = np.array([0.3, 0.6])  # 설명용 관절 두 개
amplitude = 0.5
q_rad = np.clip(amplitude * synergy_rad, [-0.2, 0.0], [0.5, 0.8])
assert np.allclose(q_rad, [0.15, 0.30])
```

`experiment.json` → `payload` → `poses`에는 각 `qpos`와 월드 손끝 위치의 5×3 배열 `tips_m`가 있다. 전체 관절 벡터의 노름은 rad 단위지만 특정 손가락 하나의 각도는 아니다. 진폭을 키워도 관절이 범위 끝에 도달하면 더 변하지 않을 수 있다.

## 관절 번호 대신 변위를 대응한다

리타게팅은 다른 손에 기하 관계를 재현하도록 요청한다. 수업의 풀이기는 먼저 SVD로 구한 적절한 회전으로 휴지 자세 손끝 점군을 정렬한다. 원본 손끝 **변위**를 대상의 월드 좌표로 바꾼 뒤, 손끝 잔차와 작은 관절 정규화가 포함된 한도 있는 최소제곱 문제를 푼다.

$$
r(q)=\begin{bmatrix}\operatorname{vec}(p_{tips}(q)-p^*)\\0.002(q-q_0)\end{bmatrix}.
$$

손끝 5개가 각각 3차원이므로 첫 잔차는 m 단위 15원소다. 관절 차이는 rad이며 수치 계수 0.002가 이를 목적함수의 m에 대응하는 잔차 스케일로 맞춘다. 보고 필드 `tip_error_m`는 **결합 잔차**의 노름이며 순수한 평균 손끝 거리가 아니다. 코드와 해석에서 이를 구별한다. `retargeted-motion.npz`는 대상 손 자세를 저장하지만 무충돌이나 실물 운동을 인증하지 않는다.

## 접촉력은 촉각 보정값이 아니다

MuJoCo는 시뮬레이션 기하와 제약으로 접촉력을 계산한다. `mj_contactForce`는 접촉 좌표계 성분 6개를 반환한다. 힘 성분은 N, 토크 성분은 N m이다. Wuji 가상 촉각 실험은 자극 구를 넣고 그 구와 관련된 접촉만 골라 법선력 절댓값을 합한다. `payload.contacts`의 `position_world_m`와 `force_contact_N`를 읽는다. 뒤 필드는 반환값 6개를 담으므로 이름만 보고 전부 힘 단위로 해석하면 안 된다.

문서의 비교처럼 자극 구 반지름만 바꾸면 침투와 법선력 trace가 달라질 수 있다. 물리 taxel 감도를 바꾸는 실험은 아니다. Shadow Hand 입문 검사는 이름이 정해진 `contact_object`의 접촉을 세어 자기 접촉과 구별한다. 접촉 수, 접촉력 크기, 파지 성공은 서로 다른 관측이다.

[공개 검증 보고서](../../verification/reader-experience.md)에 Wuji·Sharpa 측정 예제가 있다. GPU 손안 조작 PPO 수업에는 실제 준비 런타임과 평가가 필요하며, 휴대형 자세 수업이 학습된 정교 조작 정책을 증명하지 않는다. 실물 Wuji 보정·승인 평가는 별도의 하드웨어 단계다.

## 이해 확인

1. Wuji 관절 0을 Sharpa에 그대로 복사하지 않는 이유는? 이름·축·범위·제어 의미가 다를 수 있기 때문이다.
2. 시너지 하나가 모든 관절만큼 표현력이 있는가? 아니다. 낮은 차원의 자세 집합으로 제한해 과제를 단순하게 하지만 표현력을 줄인다.
3. 가상 힘 샘플은 보정된 촉각 센서 측정인가? 아니다. 기하와 풀이기 가정에서 생성된다.

좌표계는 [기구학](kinematics.md), 힘 해석은 [제어와 접촉](control-contact.md)을 참고한다.

Wuji 가상 촉각 스칼라는 시점별 법선력 절댓값 합을 시간에 대해 평균하며 개별 접촉의 평균은 아니다. 선택형 손 입력 수집은 [장비 단계](../equipment-stages.md)를 따른다. MANUS 손가락 이름과 VIVE 손목 좌표계에는 명시적 보정·대응이 필요하며 합성 출처 라벨은 실제 장갑·트래커 검증이 아니다.
