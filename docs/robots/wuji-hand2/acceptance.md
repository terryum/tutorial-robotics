# Wuji Hand 2 테스트 가이드

이 문서는 Wuji Hand 2 관련 세 저장소를 다음 순서로 검증하기 위한 체크리스트다.

1. `mujoco-ros2-core`: 공통 MuJoCo backend
2. `wuji-hand2-setup`: Wuji Hand 2 모델과 ROS 2 연동
3. `wuji-hand2-motion-baselines`: 제스처와 PPO baseline

실제 Wuji Hand 2 하드웨어는 연결하지 않는다. 이 문서의 테스트 범위는 MuJoCo와 ROS 2 시뮬레이션까지다.

## 테스트 전 준비

작업 폴더를 확인한다.

```bash
cd ~/Codes/robotics
pwd
```

각 저장소에서 아래 명령을 실행해 현재 branch와 변경 사항을 확인한다.

```bash
git status -sb
```

테스트가 생성하는 `.venv`, `.cache`, `runs`, `checkpoints` 파일은 Git 추적 대상이 아니다.

## 1. mujoco-ros2-core

### 1.1 설치 및 단위 테스트

```bash
cd ~/Codes/robotics/mujoco-ros2-core
uv sync --group dev
uv run pytest
```

정상 판정:

- `7 passed`가 출력된다.
- traceback이나 test failure가 없다.
- 이 단계에서는 GUI 창이 열리지 않는 것이 정상이다.

체크:

- [ ] dependency 설치 완료
- [ ] 전체 테스트 7개 통과

### Codex에 맡길 때

저장소 폴더에서 Codex를 실행한 뒤 다음과 같이 요청한다.

> 이 저장소는 수정하지 말고 `uv sync --group dev`와 전체 테스트를 실행해줘. 실패하면 먼저 원인을 진단하고 결과를 설명해줘.

## 2. wuji-hand2-setup

### 2.1 submodule, Python 환경 및 모델 검사

```bash
cd ~/Codes/robotics/wuji-hand2-setup
git submodule update --init --recursive
uv sync --group dev
uv run wuji-hand2-inspect --side right
uv run wuji-hand2-inspect --side left
uv run pytest
```

정상 판정:

- 왼손과 오른손 각각 20 joints, 20 actuators, 5 fingertip sites가 확인된다.
- Python 테스트가 `6 passed`로 끝난다.

체크:

- [ ] vendor model submodule 준비 완료
- [ ] `mujoco-ros2-core` submodule 준비 완료
- [ ] 오른손 모델 검사 통과
- [ ] 왼손 모델 검사 통과
- [ ] Python 테스트 6개 통과

### 2.2 MuJoCo 단독 joint sweep

오른손부터 실행한다.

```bash
cd ~/Codes/robotics/wuji-hand2-setup
uv run mjpython sim/scripts/joint_sweep.py --side right
```

종료한 뒤 왼손을 실행한다.

```bash
uv run mjpython sim/scripts/joint_sweep.py --side left
```

정상 판정:

- MuJoCo viewer 창이 열린다.
- 손가락 관절이 순서대로 움직인다.
- 관절이 갑자기 크게 튀거나 모델이 사라지지 않는다.
- terminal에 NaN, fatal error 또는 traceback이 없다.

체크:

- [ ] 오른손 viewer와 joint sweep 정상
- [ ] 왼손 viewer와 joint sweep 정상

### 2.3 ROS 2 workspace 설치 및 빌드

```bash
cd ~/Codes/robotics/wuji-hand2-setup/ros2_ws
pixi install
pixi run build
pixi run test-backend
```

`pixi install`에서 TLS 또는 인증서 오류가 발생하면 다음 명령을 사용한다.

```bash
pixi install --tls-root-certs system
```

정상 판정:

- ROS 2 package 2개가 빌드된다.
- backend test가 `1 passed`로 끝난다.

체크:

- [ ] Pixi 환경 설치 완료
- [ ] ROS 2 build 성공
- [ ] ROS backend test 1개 통과

### 2.4 오른손 ROS 2 명령 테스트

Terminal A에서 simulator를 실행하고 계속 켜둔다.

```bash
cd ~/Codes/robotics/wuji-hand2-setup/ros2_ws
pixi run mujoco-right
```

Terminal B를 새로 열어 verification command를 전송한다.

```bash
cd ~/Codes/robotics/wuji-hand2-setup/ros2_ws
pixi run command-right
```

정상 판정:

- Terminal A에서 MuJoCo 오른손 창이 열린다.
- `command-right` 실행 후 손가락 관절이 움직인다.
- simulator node가 비정상 종료하지 않는다.

체크:

- [ ] 오른손 simulator node 실행
- [ ] 오른손 command 수신 및 움직임 확인

### 2.5 ROS topic과 reset service 확인

Simulator가 실행 중인 상태에서 별도 terminal로 확인한다.

```bash
cd ~/Codes/robotics/wuji-hand2-setup/ros2_ws

pixi run bash -c \
  'source install/setup.bash && ros2 topic list'
```

적어도 다음 topic이 보여야 한다.

```text
/right_hand/joint_commands
/right_hand/joint_states
```

Joint state 한 건을 확인한다.

```bash
pixi run bash -c \
  'source install/setup.bash && ros2 topic echo --once /right_hand/joint_states'
```

Reset service를 호출한다.

```bash
pixi run bash -c \
  'source install/setup.bash && ros2 service call /right_hand/mujoco_reset std_srvs/srv/Trigger "{}"'
```

정상 판정:

- command/state topic이 모두 발견된다.
- `joint_states`에 20개 관절 이름과 position이 들어 있다.
- reset 응답의 `success`가 `true`다.
- reset 후 손이 초기 자세로 돌아간다.

체크:

- [ ] command/state topic 확인
- [ ] 20개 joint state 확인
- [ ] reset service 성공

### 2.6 왼손과 양손 테스트

오른손 프로세스를 `Ctrl-C`로 종료한 뒤 왼손을 확인한다.

Terminal A:

```bash
cd ~/Codes/robotics/wuji-hand2-setup/ros2_ws
pixi run mujoco-left
```

Terminal B:

```bash
cd ~/Codes/robotics/wuji-hand2-setup/ros2_ws
pixi run command-left
```

양손 simulator는 다음 명령으로 실행한다.

```bash
pixi run dual-mujoco
```

정상 판정:

- 왼손 command가 왼손에만 적용된다.
- 양손 실행 시 left/right node가 모두 유지된다.
- left/right command 및 state topic이 서로 분리되어 있다.

체크:

- [ ] 왼손 command 정상
- [ ] 양손 simulator 동시 실행 정상
- [ ] left/right topic 분리 확인

### 2.7 RViz 확인

기존 simulator를 `Ctrl-C`로 종료한 뒤 실행한다.

```bash
cd ~/Codes/robotics/wuji-hand2-setup/ros2_ws
pixi run mujoco-rviz-right
```

왼손은 다음과 같다.

```bash
pixi run mujoco-rviz-left
```

정상 판정:

- MuJoCo viewer와 RViz가 실행된다.
- RViz의 robot state가 MuJoCo 관절 움직임을 따른다.

체크:

- [ ] 오른손 RViz 표시 정상
- [ ] 필요 시 왼손 RViz 표시 정상

### Codex에 맡길 때

> 이 저장소를 수정하지 말고 오른손 ROS 2 acceptance test를 진행해줘. 모델 검사와 pytest, ROS build와 backend test를 먼저 실행하고, `mujoco-right`를 background session으로 유지한 뒤 `command-right`, joint state, reset service를 확인해줘. GUI 실행에 승인이 필요하면 요청해줘. 각 단계의 정상 여부를 표로 정리해줘.

## 3. wuji-hand2-motion-baselines

### 3.1 설치 및 단위 테스트

```bash
cd ~/Codes/robotics/wuji-hand2-motion-baselines
git submodule update --init --recursive
uv sync --group dev
uv run pytest
```

정상 판정:

- `6 passed`가 출력된다.
- 왼손과 오른손 cube contact test가 통과한다.

체크:

- [ ] submodule 준비 완료
- [ ] dependency 설치 완료
- [ ] 전체 테스트 6개 통과

### 3.2 제스처 재생

오른손 여섯 제스처를 재생한다.

```bash
uv run mjpython -m wuji_hand2_motion.scripts.replay_gestures \
  --side right \
  --sequence open,relaxed,fist,pinch,point,spread
```

왼손도 확인하려면 다음 명령을 사용한다.

```bash
uv run mjpython -m wuji_hand2_motion.scripts.replay_gestures \
  --side left \
  --sequence open,relaxed,fist,pinch,point,spread
```

정상 판정:

- `open`, `relaxed`, `fist`, `pinch`, `point`, `spread`가 순서대로 표현된다.
- 자세 사이가 부드럽게 전환된다.
- joint limit을 벗어나거나 손 모델이 불안정해지지 않는다.

체크:

- [ ] 오른손 여섯 제스처 정상
- [ ] 필요 시 왼손 여섯 제스처 정상

### 3.3 Joint-reach PPO smoke test

전체 학습 전에 짧은 실행 경로를 검증한다.

```bash
uv run python -m wuji_hand2_motion.scripts.train \
  --task joint-reach \
  --side right \
  --timesteps 64 \
  --eval-episodes 1
```

PPO rollout 설정으로 인해 실제 수집량은 최소 512 simulation steps가 된다.

학습 결과를 재생한다.

```bash
uv run mjpython -m wuji_hand2_motion.scripts.replay \
  --task joint-reach \
  --side right \
  --duration 30
```

정상 판정:

- training이 traceback 없이 끝난다.
- 평가 metrics JSON이 terminal에 출력된다.
- `checkpoints/wuji_hand2_right_joint_reach_ppo.zip`이 생성된다.
- replay viewer에서 손이 target joint pose를 향해 움직인다.

체크:

- [ ] joint-reach smoke training 완료
- [ ] checkpoint와 metrics 생성
- [ ] joint-reach replay 정상

더 긴 baseline 학습은 다음과 같다.

```bash
uv run python -m wuji_hand2_motion.scripts.train \
  --task joint-reach \
  --side right \
  --timesteps 20000
```

### 3.4 Cube-yaw contact PPO smoke test

```bash
uv run python -m wuji_hand2_motion.scripts.train \
  --task cube-yaw \
  --side right \
  --timesteps 64 \
  --eval-episodes 1
```

이 과제의 최소 PPO rollout은 2,048 simulation steps다.

학습 결과를 재생한다.

```bash
uv run mjpython -m wuji_hand2_motion.scripts.replay \
  --task cube-yaw \
  --side right \
  --duration 30
```

정상 판정:

- 손 안에 40 mm 주황색 cube가 나타난다.
- cube가 손과 접촉한 상태에서 episode가 시작된다.
- training과 평가가 traceback 없이 끝난다.
- `checkpoints/wuji_hand2_right_cube_yaw_ppo.zip`이 생성된다.
- replay에서 cube와 손의 접촉이 관찰된다.
- 짧은 smoke test는 학습 경로 확인용이므로 매번 성공적인 회전을 보장하지 않는다.

체크:

- [ ] cube-yaw smoke training 완료
- [ ] checkpoint와 metrics 생성
- [ ] cube 접촉 확인
- [ ] cube-yaw replay 정상

본격적인 baseline 학습은 다음과 같다.

```bash
uv run python -m wuji_hand2_motion.scripts.train \
  --task cube-yaw \
  --side right \
  --timesteps 500000
```

### Codex에 맡길 때

> 이 저장소를 수정하지 말고 pytest, 오른손 gesture viewer, joint-reach PPO smoke training과 replay, cube-yaw PPO smoke training과 replay를 순서대로 검증해줘. GUI는 각각 30초 동안 확인할 수 있게 유지해줘. checkpoint와 metrics 생성 여부 및 실패 원인을 정리해줘.

## 권장 최소 테스트 순서

시간이 부족하면 다음 항목만 먼저 확인한다.

1. `mujoco-ros2-core`의 `uv run pytest`
2. `wuji-hand2-setup`의 오른손 `joint_sweep`
3. `wuji-hand2-setup/ros2_ws`의 `build`, `test-backend`, `mujoco-right`, `command-right`
4. `wuji-hand2-motion-baselines`의 `uv run pytest`
5. 오른손 gesture replay
6. cube-yaw smoke training과 replay

## GUI 창이 열리지 않을 때

MuJoCo GUI는 일반 `python` 대신 `mjpython`으로 실행한다.

```bash
uv run mjpython ...
```

Codex 또는 sandbox 안에서 GUI 실행 권한이 막히면 다음 중 하나를 사용한다.

1. Codex가 표시하는 GUI 실행 승인 요청을 허용한다.
2. 같은 명령을 macOS Terminal에서 직접 실행한다.

이미 떠 있는 viewer와 ROS node가 포트를 점유할 수 있으므로, 다른 테스트로 넘어가기 전에 기존 프로세스를 `Ctrl-C`로 종료한다.

ROS topic이 보이지 않을 때는 다음을 확인한다.

- simulator node가 아직 실행 중인지
- 모든 terminal이 `ros2_ws`에서 Pixi task로 실행됐는지
- `ROS_DOMAIN_ID=72`와 local discovery 설정이 동일하게 적용됐는지
- build 이후 `install/setup.bash`가 source됐는지

## 최종 결과 기록

테스트 날짜: `YYYY-MM-DD`

환경:

- macOS/Linux:
- CPU/GPU:
- Python:
- MuJoCo:
- ROS 2:

결과:

- [ ] core tests
- [ ] left/right model inspection
- [ ] left/right joint sweep
- [ ] ROS build/backend test
- [ ] ROS right command/state/reset
- [ ] ROS left command/state/reset
- [ ] dual-hand ROS simulation
- [ ] RViz
- [ ] gestures
- [ ] joint-reach PPO smoke/replay
- [ ] cube-yaw PPO smoke/replay

발견한 문제와 재현 명령:

```text
여기에 기록
```
