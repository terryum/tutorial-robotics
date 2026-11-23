<!-- pal:language:start -->
<p align="right">
  <a href="data-imitation.md" lang="ko">한국어</a> | <a href="../../en/concepts/data-imitation.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 데이터와 모방학습: 대응을 배우고 결과를 시험한다

## 시연은 시간이 있는 상태 전이다

모방학습은 예시 행동에 정책을 맞춘다. 결과의 유용성은 각 행의 뜻에 달려 있다. 행동 전 관측, 행동 단위, 스텝 이후 관측, 에피소드 경계, 시간과 출처가 필요하다. 임의 관절 숫자 표는 과제 시연을 대신하지 못한다.

[에피소드 기록](../lessons/core-data-01.md)은 실제 시뮬레이션 진자를 `episode.jsonl`에 저장한다. 행마다 `episode`, `step`, `time_s`, `observation`, `action`, `next_observation`, `terminated`, `truncated`가 있다. 관측 크기는 (2,), 단위는 [rad, rad/s]이며 행동은 (1,), N m이다. [learning.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/learning.py)에서는 제어 전에 관측을 읽고 물리 스텝 10회 뒤의 상태 시각을 `time_s`로 기록한다. 로그 정렬 시 이 시간 규칙을 기억한다.

8에피소드에 각각 `samples` 전이가 있으므로 $N=8\times samples$이다. 64샘플이면 예상 개수는 512다. 이는 계약 계산이며 새 측정이 아니다. 에피소드마다 시드로 정한 초기각을 사용하며 한 에피소드의 인접 행은 강하게 관련된다.

## 행동 복제는 지도 회귀다

진자 관측 2개에 상수 1을 붙이면 관측 행렬은 $X\in\mathbb R^{N\times3}$이다. 목표 $Y\in\mathbb R^{N\times1}$은 시연 토크다. [BC 기준선](../lessons/core-il-01.md)은 $W\in\mathbb R^{3\times1}$을 다음 식으로 학습한다.

$$
\hat Y=XW,\qquad L=\frac1N\sum_{i=1}^N(\hat Y_i-Y_i)^2,\qquad
\nabla_W L=\frac2N X^T(XW-Y).
$$

손실 단위는 (N m)²이며 가중치 단위는 대응 특성에 따라 달라진다. 스칼라 손실 감소는 물리 변위 개선이 아니다. **학습 측정이 아닌 계산 예제**: 예측 [0.2, 0.4] N m, 목표 [0.1, 0.6] N m이면 MSE는 0.025 (N m)²이다.

```python
import numpy as np
predicted_nm = np.array([0.2, 0.4])
target_nm = np.array([0.1, 0.6])
mse_nm2 = np.mean((predicted_nm - target_nm)**2)
assert np.isclose(mse_nm2, 0.025)
```

진자 수업은 에피소드 0–5로 학습하고 6–7을 보류한다. 같은 에피소드의 인접 스텝을 무작위로 양쪽에 섞고 독립 에피소드 평가라고 부르면 안 된다. `experiment.json`에서 `training_rows`, `heldout_rows`, `heldout_mse`, `weights`, `source_sha256`, `reload_max_error`를 확인한다. `policy.npz`에는 실제 학습 행렬이 있다. 작은 보류 행동 오차는 해당 데이터 분포를 근사했음을 보일 뿐이다. 정책 실행 시 낯선 상태로 갈 수 있으므로 별도 롤아웃 평가가 필요하다.

## 팔의 계약과 청크 계약을 구별한다

[FR3 시연·BC](../lessons/core-fr3-10.md)와 [Enlight 시연·BC](../lessons/core-enlight-04.md)는 모델별 독립 데이터를 사용한다. [arm.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py)는 30에피소드를 학습 20, 검증 5, 테스트 5로 표시한다. 관측은 17원소이고 행동 7개는 제한된 관절 변화량으로 바뀐다. [training.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/training.py)는 정확한 계약 재개를 위해 식별·고정 정규화·최적화 상태·RNG·데이터 다이제스트를 저장한다. 별도의 20목표 평가가 과제 성공을 검사하며 `performance_verified`를 BC 손실로 추론하지 않는다.

[ALOHA와 ACT 계약](../lessons/core-aloha-01.md)은 `(samples, 16, 14)` 형태의 행동 텐서를 만든다. 각 축은 샘플·청크 지평·양팔 구동기다. 코드는 지정된 청크를 만들고 각 청크의 첫 행동만 적용한다. `contract_only=True`, `ACT_trained=False`가 핵심이다. 저장·인터페이스 형태를 배우며 이 수업에서 ACT 네트워크는 학습하지 않는다.

한 변수 비교에서는 입력 데이터·분할·시드·스텝 예산을 고정하고 BC 학습률 배율만 바꾼다. 학습 손실·보류 MSE·다시 불러오기 일치를 비교하고, 팔에서는 독립 롤아웃 성공도 확인한다. 청크 지평 변경은 다른 계약을 바꾸는 일이므로 같은 BC 학습률 실험으로 설명하지 않는다.

## 이해 확인

1. 에피소드별로 나누는 이유는? 인접 스텝이 궤적을 공유하므로 행 단위 혼합은 거의 같은 상태를 평가로 누출할 수 있다.
2. 작은 행동 MSE가 폐루프 성공을 보장하는가? 아니다. 시연 분포에 없는 상태로 이탈할 수 있다.
3. ACT 형태의 배치면 ACT를 학습했는가? 아니다. 계약 수업은 학습하지 않았음을 명시한다.

상호작용 학습은 [강화학습](reinforcement-learning.md), 다중모달 정책 인터페이스는 [VLA](vla.md)로 이어진다.

## 실제 장치 검증을 가장하지 않는 선택형 수집

노트북·GPU 단계 뒤 [선택형 수집](../equipment-stages.md)에서 실제 역량이 있는 경우 Quest 3·MANUS·VIVE·UMI 경로를 다룬다. `core-teleop-01`은 합성 에피소드를 만들고, `sim-teleop-02`는 합성 VIVE 손목·MANUS 손가락·Quest 스위치를 보정 변환으로 결합하며, `sim-enlight-06`은 합성 Enlight MuJoCo 영상·상태·행동을 기록한다. `provenance`, 에피소드 상태, 분할 필드를 보존해야 한다. [VR 검증 기록](../../verification/vr-teleop-2026-11-13.md)은 소프트웨어 시험과 합성 데이터를 보고하며, 실제 USB 장치가 없었고 사람 수집을 검증하지 않았다. 합성 에피소드 3개 분할은 소프트웨어 계약 예제이며 충분한 사람 시연 데이터가 아니다. 외부 BC는 모델·행동·관측 호환성과 에피소드 분리를 요구하며 별도 평가에서 실패할 수 있다. GR00T 실험 전에 처리기·데이터 의미를 [NVIDIA 생태계](../nvidia-ecosystem.md)에 연결한다. 형태가 맞는 내보내기만으로 모델 성능을 입증하지 못한다.
