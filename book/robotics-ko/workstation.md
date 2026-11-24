# 워크스테이션 실습

Mac에서 검증한 Enlight 실습은 워크스테이션에서 엔진을 바꿨을 때 읽을 기준선을 제공합니다. 먼저 같은 관절과 TCP(도구 중심점)의 움직임을 확인합니다. 다음으로 동작을 만들어 낸 제어기를 시연 수집에 사용하고, BC와 PPO로 학습한 정책을 새 목표에 평가합니다. 마지막으로 카메라 영상이 행동 또는 미래 영상으로 이어지는 두 가지 모델 입출력을 살펴봅니다.

## 같은 시작 자세에서 엔진 비교

**현장 확인 대기 · Enlight PhysX**　**Mac 직접 실행 · MuJoCo 초기 자세 RGB-D**

**예측.** 두 엔진에 같은 관절각을 넣으면 로봇의 첫 TCP 위치는 얼마나 가까울까요? 다음으로 같은 TCP 원 궤적을 입력했을 때 추종 오차도 같을지 생각해 보세요. 첫 번째 질문은 모델 변환과 좌표계를 확인합니다. 두 번째는 제어기와 물리 엔진을 함께 비교합니다.

두 추종 수업은 고정된 Enlight 모델, 월드 좌표계, 2 ms 물리 스텝과 20 ms 제어 주기, 같은 기본 궤적을 씁니다. 앞 절반에는 첫 관절의 목표각을 바꾸고, 뒤 절반에는 월드 XY 평면에서 반지름 12 mm인 원을 그립니다. TCP 위치 오차는 `e = p_target − p_TCP`이며 단위는 m입니다. `arm.trajectory()`와 `IsaacArm.expert()`에서 자코비안과 감쇠 최소제곱을 사용해 관절 증분을 구합니다. 각 엔진에서 제어기와 구동기가 증분을 적용하는 방식도 결과에 영향을 줍니다.

```sh
python scripts/verify_robotics_ko.py lessons core-enlight-03 --output-dir outputs/robotics-ko/ws-baseline
python scripts/verify_robotics_ko.py lessons sim-enlight-03 --output-dir outputs/robotics-ko/ws-physx
```

`lessons.json`에 기록된 실행 폴더에서 `initial_q_rad`, `joint_names`, `control_dt_s`, `tcp_targets_m`을 대조하세요. `trace.csv`에서 두 엔진 모두 TCP를 추종한 **뒤 절반**의 행을 골라 오차의 제곱 평균 제곱근(RMSE)을 구합니다. 앞 절반에는 첫 관절의 `joint_errors_rad`를 비교합니다. PhysX의 별도 프로브 구간은 센서가 평면 접촉력을 감지하는지 확인합니다.

```sh
python examples/robotics_ko/isaac_enlight_rgbd.py --engine mujoco --output-dir outputs/robotics-ko/rgbd-mujoco
python examples/robotics_ko/isaac_enlight_rgbd.py --engine physx --output-dir outputs/robotics-ko/rgbd-physx
```

별도 RGB-D 예제는 두 엔진에서 고정 카메라로 **동일한 기본 팔의 초기 자세**를 관측합니다. 카메라를 월드 `(0.505, 0.095, 0.9)` m에 놓고 월드 −Z 방향을 보게 합니다. 해상도는 320×240 px, 수직 시야각은 38°입니다. `depth.npy`의 값은 카메라 전방 축을 따른 깊이(m)입니다. `rgbd.json`에서 자세와 TCP 오차, 카메라 설정, 영상 배열 크기, 유한한 양의 깊이 픽셀 수와 깊이 범위를 확인합니다. Mac의 MuJoCo 초기 프레임에서는 양수이면서 유한한 깊이 픽셀 76,800개와 깊이 중앙값 0.900 m를 관찰했습니다. 이 픽셀에는 카메라에서 0.9 m 아래에 있는 바닥도 포함됩니다. 두 엔진의 무효 깊이 표기를 먼저 대조하세요. 추종 수업의 렌더링 결과와 이 측정을 함께 보면 움직임과 관측을 각각 검증할 수 있습니다. 앞 장의 집기 작업대와 그리퍼는 별도 장면에서 사용합니다.

**한 변수.** 추종 계산에서 궤적의 진폭만 늘린다고 가정하세요. 자코비안이 자세에 따라 달라지고 관절 증분이 포화될 수 있습니다. 같은 제어 주기라도 오차가 커지는 구간이 생기는 이유를 이 두 조건으로 설명해 보세요.

<details>
<summary>깊이의 정의와 출처</summary>
<p>픽셀을 카메라 좌표로 역투영할 때 축 깊이 z를 사용하면 X = (u − cₓ)z/fₓ, Y = (v − cᵧ)z/fᵧ입니다. 카메라 중심까지의 거리는 광축에서 벗어날수록 z보다 큽니다. Isaac 예제는 <code>distance_to_image_plane</code>을 고릅니다.</p>
<p><a href="https://docs.omniverse.nvidia.com/extensions/latest/ext_replicator/visualization.html">NVIDIA Omniverse Replicator 센서 정의</a></p>
</details>

## 시연 수집과 BC·PPO 평가

**현장 확인 대기 · PhysX BC·PPO**

**예측.** BC의 훈련 데이터 행동 오차가 줄면 새 목표에서도 바로 성공할까요? 같은 훈련 횟수로 PPO를 실행한 뒤 목표를 향해 이동하는 것과 그 위치를 유지하는 것을 각각 예측해 보세요.

`IsaacArm.observation()`은 기준 자세와의 관절각 차이 7개, 스케일을 적용한 관절 속도 7개, 월드 TCP 목표 오차 3개를 잇습니다. `training.train()`에는 상수 항이 붙은 18개 입력에서 관절별 행동 7개를 만드는 가중치가 있습니다. BC는 PhysX에서 감쇠 최소제곱 제어기의 행동을 수집하고 에피소드 단위로 훈련·검증·테스트를 나눕니다. PPO는 PhysX를 직접 스텝하며 얻은 오차와 행동 크기에서 보상을 계산하고 행동 확률비를 제한해 갱신합니다. 로봇에는 `q_next = clip(q + 0.03 tanh(a), q_min, q_max)`에 따라 계산한 관절 위치가 전달됩니다. `a`는 7차원 정책 출력이며 위치 증분 한계는 관절별 0.03 rad입니다.

```sh
python scripts/verify_robotics_ko.py lessons sim-enlight-04 sim-enlight-05 --output-dir outputs/robotics-ko/ws-physx-learn
```

`demonstrations.json`에서 에피소드 분할과 이름을 읽고, `training-contract.json`에서 모델과 엔진을 확인합니다. `physx-observations.json`의 `parameter_l1_change`, `finite_policy`, `reload_error`는 최적화와 저장 상태를 설명합니다. 독립 과제 성능은 `evaluation.json`에 있습니다. TCP 오차가 10 mm 이내로 10 제어 단계 연속 유지되는 새 목표가 20개 중 16개 이상이면 현 과제 기준을 통과합니다. 학습 실행과 이 성능 기준을 각각 표시합니다. 이 정책의 과제는 자유공간 도달입니다. 물체를 들고 나르는 정책을 검증하려면 집기 물리와 관측·행동·종료 조건을 포함한 별도 평가가 필요합니다.

**한 변수.** 씨드, 모델, 목표 범위, 독립 평가 기준을 고정하고 학습 횟수만 바꿔 보세요. BC의 검증 MSE와 독립 성공 횟수가 함께 변하는지 확인하세요. PPO의 평균 보상과 성공 횟수도 각각 해석하세요. 기준 표본 수 64에서 갱신은 16회이며, 아래 명령의 표본 수 32에서는 8회입니다.

```sh
python scripts/verify_robotics_ko.py lessons sim-enlight-04 sim-enlight-05 --samples 32 --output-dir outputs/robotics-ko/ws-physx-learn-8
```

## 영상에서 행동으로 · GR00T N1.7

**현장 확인 대기 · NVIDIA 공개 예제 추론**

**예측.** 같은 RGB 영상과 로봇 상태를 주고 언어 지시만 바꾸면 행동 청크가 어느 시점부터 달라질까요? `π(video, state, language) → action[0:H]`에서 `H`는 한 번에 예측한 미래 행동 단계 수입니다. 추론에서 예측한 청크 길이와 실행기가 다음 관측 전까지 소비하는 행동 수를 구분합니다.

지정된 NVIDIA 체크아웃의 `standalone_inference_script.py`를 사용해 호환되는 DROID 공개 에피소드에서 개방루프 예측을 수행합니다. `--embodiment-tag`가 관측·행동 키와 단위를 정합니다. 프로그램은 공개 에피소드의 관측을 읽고 예측 행동과 기록된 행동을 비교합니다. 출력 키별 배열 모양, 유한 여부, 처리 시간과 에피소드 ID를 기록하세요. 같은 입력에서 행동 길이만 바꿀 때는 실행 설정과 결과의 비교 구간을 같이 기록합니다. Enlight에 적용하려면 별도의 모델 입력·출력 매핑, 좌표계, 제한 및 평가가 필요합니다. [NVIDIA Isaac GR00T 추론 안내](https://github.com/NVIDIA/Isaac-GR00T#inference)

기존 NVIDIA 추론 환경에서 아래 명령을 실행합니다. `GR00T_MODEL_DIR`에는 미리 검증한 N1.7 체크포인트 경로를 지정합니다. 준비된 백본과 가중치가 필요합니다.

```sh
HF_HUB_OFFLINE=1 python scripts/deployment/standalone_inference_script.py \
  --model-path "$GR00T_MODEL_DIR" --dataset-path demo_data/droid_sample \
  --embodiment-tag OXE_DROID_RELATIVE_EEF_RELATIVE_JOINT \
  --traj-ids 1 2 --inference-mode pytorch --execution-horizon 8
```

## 영상에서 미래 영상으로 · Cosmos-Predict2.5와 GR00T 2

**현장 확인 대기 · Cosmos 추론 및 GR00T 2 공개 상태**

**예측.** 로봇 팔과 컵이 담긴 첫 화면이 같아도 “멈춘다”와 “컵에 접근한다”는 문장은 다른 미래를 만들 수 있습니다. Cosmos-Predict2.5의 Image2World는 입력 영상 한 장과 텍스트 조건에서 미래 영상을 생성합니다. `V_future = f(I₀, text, seed)`에서 `I₀`는 고정 초기 프레임입니다. 설치된 체크포인트에 맞는 공식 Image2World 예제를 선택합니다. 디코딩 가능한 영상인지 확인하고 프레임 수, 크기, 프레임 속도, 씨드와 입력 해시를 남깁니다. 첫 프레임과 씨드를 고정하고 텍스트만 바꾼 두 결과에서 물체의 가림, 이동과 자세 변화를 비교하세요. 영상에서 그럴듯하게 보이는 접촉은 시뮬레이터가 계산한 접촉력이나 독립 성공 횟수와 별도로 해석합니다. [Cosmos-Predict2.5 공식 추론 예제](https://github.com/nvidia-cosmos/cosmos-predict2.5/blob/main/docs/inference.md)

기존 Cosmos 환경에서 공식 예제의 기준 영상을 생성합니다. 체크포인트와 샘플 입력은 미리 검증한 파일을 사용합니다.

```sh
HF_HUB_OFFLINE=1 python examples/inference.py -i assets/base/robot_welding.json \
  -o outputs/robotics-ko-image2world --inference-type=image2world --model=2B/post-trained
```

GR00T 2는 미래 영상과 로봇 행동을 함께 예측하는 월드 액션 모델입니다. 같은 장면에서 영상 속 물체의 변화와 로봇 행동이 시간상 어떻게 대응하는지 살펴볼 수 있습니다. 2026년 11월 24일 확인한 NVIDIA 연구 페이지는 코드 공개 시점을 12월로 안내했습니다. WS2에서는 공개 여부와 현재 설치 환경의 호환성을 확인한 뒤 상태와 근거를 기록합니다. [NVIDIA GR00T 2 연구 페이지](https://research.nvidia.com/labs/gear/gr00t-2/)
