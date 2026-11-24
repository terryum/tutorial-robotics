# 로봇 시뮬레이션 · 매니퓰레이션

Flexiv Enlight-L의 공개 기구학·관성·관절 한계에서 출발합니다. 관절 목표를 추종한 뒤 말단 제어점(TCP)의 월드 좌표 오차를 읽고, 물체를 집을 때에는 접촉력과 물체 위치를 따로 확인합니다. 같은 작업대에서 물체 위치를 아는 경우와 카메라로 추정하는 경우를 비교합니다. FR3를 선택하면 별도 모델로 기구학과 추종을 검산할 수 있습니다.

## 관절 목표와 TCP 궤적

**예측.** 같은 관절각 오차가 팔을 접은 자세와 뻗은 자세에서 같은 TCP 오차를 만들까요? 자코비안 J(q)가 자세에 따라 달라지므로 같은 관절 오차라도 TCP에 미치는 영향은 다릅니다.

**코드와 입력.** `arm.py`의 `trajectory()`는 앞 절반에서 첫 관절을 진폭 0.06 rad인 사인파로 움직이고, 뒤 절반에서 월드 XY 평면의 반지름 0.012 m 원을 추종합니다. 후반의 위치 오차 e는 목표 위치 x*와 현재 위치 x의 차 x* − x입니다. 코드는 3×7 병진 자코비안으로 관절 증분 Δq = Jᵀ(JJᵀ + λI)⁻¹e를 계산합니다. `Arm.command()`는 관절 위치 및 속도 오차를 가속도 명령으로 만들고, 관성행렬을 곱한 뒤 편향 토크를 더해 모델의 구동기 한계 안에서 적용합니다. 물리 간격은 0.002 s, 제어 명령 간격은 물리 10스텝에 해당하는 0.020 s입니다. [관절·TCP 추종 구현](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py)

```bash
pal assets fetch flexiv-description
python scripts/verify_robotics_ko.py lessons core-enlight-02 core-enlight-03 --output-dir outputs/robotics-ko/track
```

**결과.** Mac 기준 실행에서 독립 순기구학의 최대 차이는 6.76 × 10⁻¹⁶ m였고, 후반 TCP 추종 RMSE는 **5.19 mm**였습니다. `experiment.json`의 `payload`에서 `joint_errors_rad`, `tcp_targets_m`, `tcp_rmse_m`을 확인합니다. TCP RMSE는 후반 원 궤적만 집계합니다. 접촉 배열의 법선력 합에는 지정 물체 이외의 접촉도 들어갈 수 있으므로 파지 단계에서는 아래와 같이 접촉쌍을 지정합니다.

**한 가지 변경.** 모델·시드·샘플 수를 고정하고 `--variant 0.8`을 새 출력 폴더에서 실행합니다. 이 계수 하나가 첫 관절의 명령 진폭과 원 반지름을 각각 80%로 줄입니다. 후반 RMSE와 전반 관절 오차를 나누어 비교합니다. 작은 입력에서 줄어든 오차에는 목표 궤적 크기의 변화가 반영됩니다.

<details>
<summary>선택 경로 · FR3에서 검산하기</summary>
<p><code>pal assets fetch mujoco-menagerie</code>로 고정된 FR3 자산을 준비합니다. 이어 <code>python scripts/verify_robotics_ko.py lessons core-fr3-04 core-fr3-05 core-fr3-09 --output-dir outputs/robotics-ko/fr3</code>를 실행합니다. 역기구학 잔차, 작업공간 힘을 관절 토크로 옮긴 결과, 궤적 오차를 차례로 읽습니다. 각 로봇의 관절 이름과 자체 초기 상태를 적용합니다.</p>
</details>

## 위치를 알고 집고 옮기고 놓기

**예측.** 두 손가락이 물체를 누르는 동안 물체가 몇 mm 움직였다는 사실만으로 들어 올렸다고 판단할 수 있을까요? 양쪽 접촉을 확인하고 물체 중심이 작업대 위에서 충분히 높아진 동안 두 접촉이 유지됐는지 확인합니다. 마지막에는 물체가 목표 원 안에서 작업대에 지지되어야 합니다.

**코드와 입력.** `pick.py`는 고정 버전의 Enlight 변환 모델에 교육용 평행 그리퍼, 작업대, 한 변이 36 mm인 자유 물체를 추가합니다. 첫 시험의 목표는 정해진 초기 위치 (0.432, 0.087, 0.043) m입니다. 위치는 월드 좌표로 표현하고 그리퍼 방향은 아래로 고정합니다. `wanted_joints()`는 별도 역기구학 상태에서 TCP 위치와 방향을 만족하는 관절 목표를 찾습니다. `simulate()`의 `advance()`는 목표 간 관절각을 부드럽게 보간하고 모터 토크와 손가락 구동기를 적용합니다. 물체의 자유관절은 초기화 뒤 접촉과 중력에 따라 `mj_step()`에서 움직입니다. 접근 → 하강 → 닫기 → 들기 → 이동 → 놓기 → 열기 → 후퇴를 순서대로 실행합니다. [집기 소스](https://github.com/terryum/tutorial-robotics/blob/main/examples/robotics_ko/pick.py)

```bash
python examples/robotics_ko/pick.py --output-dir outputs/robotics-ko/pick
```

**결과.** Mac의 `pick.json`에서 `known_pose`와 `rgbd`를 비교합니다. 이 표는 마찰 계수 1.3에서 측정한 값입니다.

| 제어에 쓴 물체 위치 | 최대 상승 | 최종 XY 오차 | 공중에서 양쪽 접촉을 유지한 물리 스텝 | 최종 작업대 지지력 |
| --- | ---: | ---: | ---: | ---: |
| 고정된 초기 위치 | 82.26 mm | 0.235 mm | 1007 | 0.441 N |
| RGB-D에서 추정 | 82.26 mm | 0.677 mm | 1007 | 0.441 N |

양쪽 접촉은 들기·이동 구간에서 물체 중심이 초기 이론 높이보다 30 mm 넘게 올라간 상태에서 손가락과 물체 사이의 두 법선력 합이 각각 0.1 N 이상인 스텝을 셉니다. 통과하려면 그런 스텝이 25회 이상, 최대 상승이 65 mm 이상이어야 합니다. 후퇴 후 XY 오차 25 mm 미만, 높이 오차 5 mm 미만, 속력 15 mm/s 미만, 작업대 지지력 0.2 N 이상, 지정 파지쌍 외 로봇 접촉 0회도 확인합니다. `pick-trace.csv`에서 높이가 증가하는 순간의 `left_N`, `right_N`과 `cube_z_m`을 대조합니다.

**한 가지 변경.** 나머지 조건을 고정하고 패드의 미끄럼 마찰 계수만 1.3에서 0.02로 바꿉니다. 코드가 의도적으로 파지 실패를 보고할 수 있으므로 실패해도 출력 JSON을 확인합니다.

```bash
python examples/robotics_ko/pick.py --output-dir outputs/robotics-ko/pick-low-friction --pad-friction 0.02
```

이 조건에서 RGB-D의 위치 추정 오차는 그대로였지만 양쪽으로 지지한 공중 스텝은 **0**, 최대 상승은 **1.99 mm**였습니다. 시각으로 목표 위치를 맞춰도 들어 올리려면 중력을 지탱할 접선력이 필요합니다.

## RGB 분할과 깊이 영상에서 물체 위치 구하기

**예측.** 빨간 픽셀의 좌표로 카메라에서 물체 방향을 알아낼 수 있습니다. 물체까지의 거리를 얻으려면 무엇이 더 필요할까요? 이 실습은 같은 픽셀의 깊이 Z를 읽고 픽셀을 카메라의 3D 점으로 역투영합니다.

**코드와 입력.** `rgbd_frame()`은 위에서 내려다보는 고정 핀홀 카메라의 320×240 픽셀마다 MuJoCo에서 가장 가까운 표면과 광선의 교점을 구합니다. CPU에서 표면색과 광축 방향 깊이(Z)를 짝지어 생성합니다. 보정값에는 38° 수직 시야각에서 얻은 초점거리 348.51 px, 주점 (159.5, 119.5) px, 카메라 중심 (0.505, 0.095, 0.900) m 및 카메라 좌표를 월드 좌표로 변환하는 회전이 들어갑니다. 카메라의 +X는 오른쪽, +Y는 아래쪽, +Z는 보는 방향입니다. 정사각 픽셀이고 렌즈 왜곡은 0으로 둡니다.

`estimate()`는 빨강이 강하고 초록·파랑이 약한 픽셀만 선택한 뒤, 알려진 보정값으로 `camera_points`를 만듭니다. 픽셀 좌표를 (u, v), 주점을 (cₓ, cᵧ), 초점거리를 f, 깊이를 Z m라 하면, 카메라 좌표계의 점은 다음과 같습니다.

<math display="block"><mrow><msub><mi>P</mi><mi>c</mi></msub><mo>=</mo><mo>(</mo><mfrac><mrow><mo>(</mo><mi>u</mi><mo>−</mo><msub><mi>c</mi><mi>x</mi></msub><mo>)</mo><mi>Z</mi></mrow><mi>f</mi></mfrac><mo>,</mo><mfrac><mrow><mo>(</mo><mi>v</mi><mo>−</mo><msub><mi>c</mi><mi>y</mi></msub><mo>)</mo><mi>Z</mi></mrow><mi>f</mi></mfrac><mo>,</mo><mi>Z</mi><mo>)</mo></mrow></math>

월드 점은 P𝑤 = RP𝑐 + t로 변환합니다. 높이가 가장 높은 면의 점들 중 최솟값과 최댓값의 중점을 구한 뒤 알려진 반높이 18 mm를 빼면 정육면체 중심입니다. RGB-D 시험은 이 위치만 제어에 넘깁니다. 물체가 수평이고 방향을 알고 있다는 조건은 두 시험에서 같습니다.

**결과.** 앞의 `pick.py` 명령이 이 시험도 실행합니다. `pick-rgb.png`와 `pick-mask.png`로 원본과 분할을 확인합니다. `pick-camera.npz`는 높이×너비 배열 `depth_m`과 N×3 배열 `points_world_m`을 담습니다. Mac 실행에서는 240 픽셀을 분할했고 그중 225 픽셀을 윗면에 사용했습니다. `pick.json`의 `perception`에서 물체 중심 오차는 **0.606 mm**, 재투영 RMSE는 표시 정밀도에서 **0 px**였습니다. 재투영 오차는 좌표 변환의 왕복 일관성을 확인합니다. 깊이의 단위와 축은 별도로 알려진 작업대 높이와 비교했으며, 중심 오차는 시뮬레이터의 실제 물체 위치로 평가했습니다.

**한 가지 변경.** 깊이 스케일만 2배로 바꾼 별도 계산을 `monocular_scale_comparison`에서 읽습니다. 가령 약 0.839 m에 해당하는 중앙 깊이는 약 1.678 m가 됩니다. (X, Y, Z)를 모두 2배로 하면 핀홀 투영에 쓰는 X/Z, Y/Z와 픽셀 위치는 같습니다. 단안 모델이나 원근 단서가 상대적 깊이를 주더라도, 절대 미터값을 얻으려면 알려진 물체 크기나 카메라 높이 등 스케일을 정할 기준이 필요합니다. 이 비교는 투영 식 자체의 성질을 검산합니다.

<details>
<summary>카메라 보정을 실제 센서로 옮길 때</summary>
<p>가로·세로 초점거리와 주점은 보정 표적을 여러 자세에서 촬영해 추정하고 왜곡 계수도 함께 얻습니다. 같은 해상도와 캡처 설정에서 보정값을 적용합니다. 카메라와 월드 사이 회전·위치는 별도의 외부 보정으로 구합니다. RGB와 깊이 센서가 서로 다른 카메라에 있으면 각자의 보정값과 두 카메라의 상대 자세를 사용해 깊이를 RGB 픽셀에 정렬합니다.</p>
</details>

## 모델 기반 시연에서 BC와 PPO로

**예측.** 전문가의 행동을 더 잘 맞히면 새 목표에 더 자주 도달할까요? 시연과 비슷한 상태에서는 행동 오차가 작아도, 정책의 작은 실수가 누적되어 시연에 없었던 자세에 갈 수 있습니다.

**코드와 입력.** 집기 과제의 단계 제어 뒤에 같은 팔의 **TCP 도달 동작**을 학습합니다. `Arm.expert()`는 현재 위치 오차와 자코비안으로 전문가의 관절 증분을 계산합니다. 이를 상태·행동 쌍으로 기록하고 행동 복제(BC)가 예측 행동의 제곱 오차를 줄입니다. 30 시연 에피소드는 학습 20개, 검증 5개, 테스트 5개로 나눕니다. PPO는 초기 자세에서 자신의 행동을 적용한 시뮬레이션 기록으로 갱신합니다. 각 스텝의 보상은 TCP 거리의 음수에서 0.001 × 행동 제곱합을 추가로 뺀 값입니다. 정책의 관측 17개는 기준 자세 대비 관절각 7개, 스케일을 적용한 관절 속도 7개, 월드 TCP 목표 오차 3개입니다. 행동 7개는 환경에서 0.03 × tanh(a) rad만큼의 관절 증분으로 변환됩니다. [도달 환경과 전문가](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py) · [학습 코드](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/training.py)

```bash
python scripts/verify_robotics_ko.py lessons core-enlight-04 core-enlight-05 --output-dir outputs/robotics-ko/learning
```

**결과.** `training-contract.json`과 `experiment.json`은 학습 조건과 갱신 횟수를 기록합니다. `evaluation.json`은 시드 10007의 독립 목표 20개에서 TCP 오차 10 mm 이내를 연속 10 제어 스텝 유지했는지 기록합니다. 통과 기준은 16/20입니다. Mac에서 같은 설정으로 각 16회 갱신했고, **BC는 20/20**, **PPO는 0/20**이었습니다. 두 학습 모두 가중치가 갱신되고 재로딩 검사를 통과했습니다. 집기와 배치는 앞 장의 접촉 실습에서 별도로 검증합니다.

**한 가지 변경.** 시드, 모델, 독립 목표, 갱신 횟수를 동일하게 유지한 채 `--variant 0.8`을 지정하면 학습률이 0.010에서 0.008로 바뀝니다. 예를 들어 다음과 같이 BC에서 먼저 비교합니다. `trace.csv`의 관측 열 또는 `plot.png`에서 BC의 학습 행동 MSE를 읽고, `evaluation.json`에서 독립 목표의 성공 수를 확인합니다.

```bash
python scripts/verify_robotics_ko.py lessons core-enlight-04 --variant 0.8 --output-dir outputs/robotics-ko/learning-low-rate
```

### 시연을 어떻게 나누느냐에 따라 달라지는 검증

**예측.** 연속한 두 프레임은 관측과 전문가 행동이 서로 비슷합니다. 각 프레임을 독립 표본처럼 섞으면, 검증 프레임에 바로 이웃한 학습 프레임이 몇 개의 시연에서 나올지 예상해 보세요.

**코드와 입력.** 위 `lessons` 명령이 만든 `outputs/robotics-ko/learning/lessons.json`에서 `core-enlight-04`의 `run_dir`을 읽어 실행 폴더를 찾습니다. `bc_split.py`는 해당 실행의 `demonstrations.json`에서 `episode`와 `split`을 읽습니다. 원래 학습·검증용 시연의 프레임만 모아 시드 7로 무작위로 섞은 뒤, 원래와 같은 프레임 수로 나눕니다. 두 방식 각각에서 학습·검증 에피소드 ID의 교집합 크기를 셉니다. 테스트 시연 5개는 두 방식 모두 이 비교에서 빼 둡니다. [분할 검산 코드](https://github.com/terryum/tutorial-robotics/blob/main/examples/robotics_ko/bc_split.py)

```bash
book_run=outputs/robotics-ko/learning
bc_run=$(python -c 'import json, sys; print(json.load(open(sys.argv[1]))["lessons"]["core-enlight-04"]["run_dir"])' "$book_run/lessons.json")
python examples/robotics_ko/bc_split.py --run-dir "$book_run/$bc_run"
```

**결과.** Mac 실행에서 학습 532프레임과 검증 134프레임을 유지했습니다. 프레임 단위 분할은 시연 25개를 양쪽에 포함했습니다. 기존 에피소드 단위 분할은 학습 시연 20개와 검증 시연 5개가 겹치지 않았습니다. 행동 복제 정책의 기존 `evaluation.json`에서 `validation_mse`는 **0.04854**, `test_mse`는 **0.06400**이었습니다. 이 값은 관절 증분으로 변환하기 전 7개 행동 성분의 제곱 오차를 프레임과 성분에 걸쳐 평균한 값입니다. 같은 파일의 독립 목표 평가에서는 **20/20**에 도달했습니다. 분할 검산은 중복만 세므로 프레임 단위로 다시 학습했을 때 MSE가 얼마나 달라질지는 별도 실험이 필요합니다.

**이해 확인.** 검증 MSE가 작더라도 폐루프 성공률을 따로 읽는 이유는 무엇일까요? MSE는 주어진 시연 상태에서 행동을 비교합니다. 폐루프 평가는 정책이 만든 다음 상태를 다시 관측하므로 여러 단계에 걸쳐 누적된 오차까지 반영합니다.

### 읽기 사례 · 시연의 시간표와 실행 제약

Moon 등의 사전 공개 논문은 시연 경로를 따라 실행 속도의 분포를 학습하고, 선택한 분위수로 경로를 언제 지날지 정합니다. 이렇게 시간을 조정한 시연으로 시각·언어·행동 정책을 미세조정합니다. 실행 중에는 정책이 낸 행동 묶음과 속도를 최적 제어기가 받아 로봇 한계 안에서 현재 계획에 이어 붙입니다. 논문 그림 2를 읽으며 정책이 제안하는 것과 제어기가 지켜야 하는 조건을 적어 보세요. 앞에서 다룬 진자 LQR은 모델과 비용에서 이득을 구했고, 이 사례의 실행 제어기는 여러 시점의 경로와 제약을 함께 다룹니다. [Retiming Robot Demonstrations with a Learned Speed Prior](https://arxiv.org/abs/2610.32676)

## Isaac Sim에서 같은 초기 상태로 비교하기

**현장 확인 대기.** 워크스테이션에서 Enlight의 같은 초기 관절 자세, 월드 TCP 목표, 제어 간격을 사용해 PhysX에서 추종을 재실행합니다. 양쪽에서 이름이 같은 관절을 대응시키고, TCP 오차와 카메라 RGB·깊이 배열의 해상도, 좌표계, 무효 픽셀, 깊이 단위를 함께 확인합니다. 조명·재질과 깊이의 정의가 다른 경우 차이를 먼저 기록해야 영상이나 점군의 차이를 해석할 수 있습니다. Isaac의 결과를 기록하는 순서와 통과 기준은 워크스테이션 실습에서 이어집니다. 시뮬레이션 간 비교의 다음 질문은 목표 자세, 마찰, 카메라 보정값을 각각 독립적으로 바꿨을 때 어느 지표가 가장 민감하게 반응하는지입니다.
