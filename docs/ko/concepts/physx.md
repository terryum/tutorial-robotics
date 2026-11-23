<!-- pal:language:start -->
<p align="right">
  <a href="physx.md" lang="ko">한국어</a> | <a href="../../en/concepts/physx.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# PhysX: 두 번째 엔진에는 별도 근거가 필요하다

## 가져오기는 비교의 시작이다

같은 로봇 그림 두 장 뒤에도 질량·관절·구동기·접촉 모델은 다를 수 있다. 두 번째 엔진 실험은 이 계약을 확인한 뒤 과제 동작이 유사한지 묻는다. MuJoCo 출력의 이름을 PhysX로 바꿔서는 답할 수 없다. [Isaac 자산 가져오기](../lessons/sim-isaac-01.md)와 [카메라 데이터](../lessons/sim-isaac-02.md)는 먼저 가져오기와 렌더링을 확인한다. [FR3 PhysX 제어](../lessons/sim-fr3-01.md)는 실제 물리 엔진을 사용하며, [FR3 동일 조건 비교](../lessons/sim-fr3-04.md)는 완료된 두 실행을 입력받는다.

어댑터는 배열 순서가 유지된다고 가정하지 않고 관절 이름으로 대응해야 한다. 엔진 A의 $q_A$가 $n$원소 벡터이고 $P$가 이름 대응 순열 행렬이면 $q_B^{aligned}=Pq_B$이다. 회전 관절은 rad, 직선 관절은 m이다. 자유 베이스의 위치·쿼터니언·속도는 일반적인 모터 명령 벡터가 아니다. 오차 해석 전에 축 부호·한도·베이스 고정·충돌·관성·드라이브 이득·결합 관계를 맞춘다. mimic·tendon 변환이 검증되지 않으면 진행을 막는 결함이다.

## 무엇을 비교하는지 먼저 정의한다

샘플 $i$에서 월드 목표에 대한 오차를 $e_i^A=\lVert x_i^*-x_i^A\rVert_2$, $e_i^B=\lVert x_i^*-x_i^B\rVert_2$라 하면 모두 m 단위다. FR3 비교는 다음을 보고한다.

$$
D=\sqrt{\frac1N\sum_{i=1}^N(e_i^A-e_i^B)^2}.
$$

$D$는 **오차 크기 차이**의 RMS이다. 두 TCP 궤적 사이의 벡터 거리 RMS가 아니다. 반대 방향으로 같은 크기의 오차가 나면 $D=0$일 수 있다. 이 스칼라의 일치를 동일 동역학의 증거로 표현하지 않는다.

**엔진 측정이 아닌 계산 예제**: 오차가 각각 [0.01, 0.02] m와 [0.012, 0.018] m이면 $D=0.002$ m이다.

```python
import numpy as np
error_a_m = np.array([0.01, 0.02])
error_b_m = np.array([0.012, 0.018])
difference_rmse_m = np.sqrt(np.mean((error_a_m - error_b_m)**2))
assert np.isclose(difference_rmse_m, 0.002)
```

[comparison.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/comparison.py)는 `previous_run`으로 완료된 `core-fr3-09`와 `sim-fr3-01`의 실제 근거를 읽는다. `frame`, `initial_q_rad`, `tcp_targets_m`, `control_dt_s` 또는 샘플 수가 다르면 거부한다. 비교 수업의 카탈로그 역량은 휴대형 환경의 분석을 허용하지만, PhysX 입력을 만들려면 별도로 설치·검증된 Isaac/GPU 환경이 필요하다. WS1·WS2라는 이름으로 그 역량이 생기지는 않는다.

## 출력에서 생산자로 거슬러 올라간다

`experiment.json`의 비교 payload에는 `engine_a`, `engine_b`, `tcp_error_difference_rmse_m`, `joint_errors_a_rad`, `joint_errors_b_rad`, `contacts_a_N`, `contacts_b_N`, `control_dt_s`, `hardware_tolerance=False`가 있다. 그래프 가로축은 초이며 두 곡선은 m 단위의 TCP 오차 크기다. 현재 생산자는 0.02 s 간격으로 비교 trace 시간 라벨을 만든다. 입력의 시간 계약은 여전히 같아야 하며, 시간 해석에는 원본 실행의 타임스탬프도 확인한다.

접촉 배열은 원본 실행에서 가져온다. MuJoCo 궤적 생산자의 `contact_force_norms_N`은 모든 접촉의 법선 성분 절댓값을 합한다. 필드 이름과 달리 6차원 접촉 렌치 전체의 노름이 아니다. 배열 이름만으로 물리적 접촉이 대응한다고 추론하지 말고, 접촉 물체 이름과 각 생산자의 힘 계산을 읽는다. 카메라 그림과 유한한 수치는 필요한 산출물이지만 그것만으로 드라이브가 정확하다고 증명하지 못한다.

한 변수 사고 비교에서는 두 입력 실행을 고정하고 비교 수업의 기존 `variant`만 바꾼다. 이 생산자는 `variant`를 사용하지 않으므로 결과가 같아야 한다. 제어 이득을 조사하려면 목표·좌표계·시간 계약을 유지한 채 이득 하나만 바꾼 새 대응 실행쌍을 만든다. 서로 다른 과제를 몰래 비교하면 안 된다.

## 검증 범위와 이해 확인

[공개 경로 검증 기록](../../verification/robot-paths-2026-11-08.md)은 Mac 시뮬레이션 검사와 실행하지 못한 Isaac 검증을 구별한다. 실제 근거가 없으면 `reader_test_required`를 유지한다. 문서 빌드나 어댑터 단위 테스트는 PhysX 실행이 아니다.

1. 휴대형 컴퓨터에서 기존 PhysX 근거를 분석할 수 있는가? 가능하지만 진짜 검증 입력이 필요하며 없는 실행을 만들어낼 수는 없다.
2. $D=0$이면 TCP 위치가 일치하는가? 아니다. 같은 크기의 오차가 다른 방향을 가리킬 수 있다.
3. 엔진이 일치하면 실물을 허가하는가? 아니다. [배포와 실물](deployment-hardware.md)의 독립 게이트가 필요하다.

## NVIDIA 도구의 연결

[NVIDIA 생태계 안내](../nvidia-ecosystem.md)에서 Isaac Sim의 장면·PhysX 검증, Isaac Lab의 과제·학습 인터페이스, Isaac 원격조작 입력·리타게팅, GR00T 데이터·모델 실험을 연결한다. 각각 별도 계약과 환경이므로 하나를 설치하거나 가져왔다고 나머지를 검증한 것은 아니다. GPU 시뮬레이션 뒤 선택형 수집을 거치고 실물 게이트를 요청한다.
