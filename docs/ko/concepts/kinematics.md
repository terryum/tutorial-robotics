<!-- pal:language:start -->
<p align="right">
  <a href="kinematics.md" lang="ko">한국어</a> | <a href="../../en/concepts/kinematics.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 기구학: 관절에서 점으로, 다시 관절로

## 위치에는 좌표계가 필요하다

관절 숫자 7개만으로는 그리퍼가 어디 있는지 알기 어렵다. 순기구학 $x=f(q)$는 rad 단위의 관절각 $q\in\mathbb R^7$을 m 단위의 도구점 $x\in\mathbb R^3$으로 바꾼다. 위치는 이름이 정해진 좌표계로 표현하며, 이 수업에서는 주로 월드 좌표계를 쓴다. 도구의 방향은 별도 양이다. 위치만 푸는 문제는 6차원 자세 문제를 해결하지 않는다.

강체 변환은 회전 $R$(3×3, 무차원)과 병진 $p$(3원소, m)를 묶는다.

$$
T=\begin{bmatrix}R&p\\0&1\end{bmatrix},\qquad
\begin{bmatrix}x_A\\1\end{bmatrix}=T_{AB}\begin{bmatrix}x_B\\1\end{bmatrix}.
$$

$T_{AB}$는 B 좌표를 A 좌표로 변환한다. 점의 마지막 동차 좌표는 1이다. 변위는 마지막 좌표가 0이어서 병진의 영향을 받지 않는다. 행렬 곱에는 순서가 있으므로 곱하기 전에 변환 방향부터 확인한다.

## 자코비안은 현재 자세의 국소적인 자다

한 자세 근처에서는 작은 관절 변화와 점의 변화가 대략 선형 관계를 가진다.

$$
\Delta x\approx J(q)\Delta q,\qquad J\in\mathbb R^{3\times7}.
$$

각 열은 관절 하나를 바꾸었을 때 그 점이 어떻게 움직이는지 나타낸다. 회전 관절이면 단위는 m/rad이다. 이는 국소 근사이며 큰 움직임까지 보장하지 않는다. [physics.py의 `jacobian`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/physics.py)은 MuJoCo에 사이트의 병진 자코비안을 요청한다. FR3 수업은 이를 중앙 유한차분과 비교한다.

$$
J_{:,j}\approx\frac{f(q+\epsilon e_j)-f(q-\epsilon e_j)}{2\epsilon}.
$$

$e_j$는 관절 $j$를 선택하며, 기준 $\epsilon$은 $10^{-6}$ rad이다. 위치를 바꾼 뒤에는 `mj_forward`로 기하 정보를 갱신해야 한다. `qpos`에 값을 대입하는 것만으로 사이트 위치가 갱신되지는 않는다.

## 역기구학은 작은 관절 갱신을 선택한다

위치 좌표 3개에 관절 변수 7개가 있으므로 일반적으로 해가 여러 개다. 특이점 근처에서는 직접 역행렬이 없거나 잡음을 증폭할 수 있다. 수업은 감쇠 최소제곱 갱신을 사용한다.

$$
\Delta q=J^T(JJ^T+\lambda I_3)^{-1}(x^*-x).
$$

m와 rad 좌표에서 코드의 수치 정규화 계수는 $\lambda=10^{-4}$이며, $JJ^T$ 원소와 같은 수치 스케일을 가진다. 각 갱신은 ±0.08 rad로 제한하고, 다시 모델의 관절 한도로 제한한다. 충돌 여유를 최적화하지는 않는다. 기구학적 해와 동역학으로 달성한 운동의 차이는 [제어와 접촉](control-contact.md)에서 설명한다.

**측정 결과가 아닌 계산 예제**: 한 국소 방향의 $J=[0.2]$ m/rad와 목표 변위 0.01 m에 $\lambda=10^{-4}$를 쓰면 한도 적용 전 $\Delta q=0.0498753$ rad이다. 다음은 같은 풀이를 3×7 설명용 자코비안에 적용한 것이다.

```python
import numpy as np
J = np.zeros((3, 7))
J[:3, :3] = np.diag([0.2, 0.3, 0.4])
error_m = np.array([0.01, 0.0, 0.0])
dq_rad = J.T @ np.linalg.solve(J @ J.T + 1e-4 * np.eye(3), error_m)
assert np.isclose(dq_rad[0], 0.04987531172069825)
```

## 근거를 따라 읽기

[core-fr3-04](../lessons/core-fr3-04.md)의 `experiment.json` → `payload`에는 각각 3×7인 `analytic`, `finite_difference`와 `jacobian_max_error`, `target_m`, `ik_errors_m`가 있다. 그래프 가로축은 시간이 아니라 **IK 반복 횟수**다. 검사는 자코비안 차이를 $10^{-6}$과, 최종 위치 잔차를 0.001 m와 비교한다. 작은 잔차는 이 모델 제약에서 이 점에 도달했음을 보일 뿐, 방향·토크 한도·실물 보정을 증명하지 않는다.

[Enlight 모델 변환](../lessons/core-enlight-02.md)은 독립적인 벤더 변환식과 컴파일된 MJCF 위치를 비교해 변환 일관성을 검사한다. 두 기하 모델이 일치해도 실제 관성은 식별되지 않는다. [FR3 궤적 추종](../lessons/core-fr3-09.md)은 연속 기구학 목표를 실제 시뮬레이션 동역학에 연결한다.

한 변수 비교에서는 자세와 목표를 유지하고 유한차분 $\epsilon$만 바꾼다고 생각한다. 큰 $\epsilon$은 절단 오차를 늘리고, 지나치게 작은 값은 뺄셈의 반올림 오차를 키운다. IK는 계속 해석적 자코비안을 쓰므로 별도의 IK 잔차는 같을 수 있다. 이 비교의 대상은 수치 검산이지 반드시 도달 성능 개선은 아니다.

## 이해 확인

1. 3×7 자코비안을 그대로 역행렬로 만들지 않는 이유는? 직사각 행렬이며 랭크가 부족할 수도 있기 때문이다.
2. `qpos`를 바꾼 뒤 `mj_forward`를 호출하는 이유는? 사이트 위치 등 파생량을 다시 계산해야 하기 때문이다.
3. 작은 위치 잔차가 도구 방향을 보장하는가? 아니다. 이 목적함수에는 방향이 없다.

선택형 [원격조작](../equipment-stages.md)은 장치 좌표계 → 보정 월드 좌표계 → 장착 손목·도구 좌표계라는 두 번째 변환 체인을 추가한다. `sim-teleop-02`는 합성 통합 입력으로 이를 가르치며 실제 Quest·MANUS·VIVE 검증은 별도다. 변환값과 함께 원시 좌표·시계 라벨을 보존해 그럴듯한 자세가 잘못된 규약을 숨기지 않게 한다.
