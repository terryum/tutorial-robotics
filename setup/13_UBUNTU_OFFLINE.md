# Ubuntu 24.04 오프라인 개발 환경

WS1과 WS2의 네이티브 Ubuntu에서 공통으로 사용하는 설치 경로다. 호스트 이름과
실행 mode는 별개다. WS1도 실물 연결 이전의 이 checkout에서는 `DEVELOPMENT`로
MuJoCo·ROS를 검증한다. WSL이나 Mac Pixi 환경과 빌드 디렉터리를 공유하지 않는다.

## 설치

저장소 root에서 시작한다. Python은 `/usr/bin/python3`의 3.12를 유지한다.
uv 0.12.10 공식 installer는 사용자 도구만 설치하며 shell profile은 변경하지 않는다.

```bash
curl -fsSL https://astral.sh/uv/0.12.10/install.sh -o /tmp/robotics-uv-install.sh
UV_NO_MODIFY_PATH=1 sh /tmp/robotics-uv-install.sh
export PATH="$HOME/.local/bin:$PATH"
uv sync --locked --python /usr/bin/python3
uv pip check --python .venv/bin/python
uv run --locked pal doctor
uv run --locked pytest
uv run --locked pytest ../mujoco-ros2-core/tests
```

`uv.lock`을 갱신하지 않는다. MuJoCo는 현재 lock의 3.12.0이다. `learning` extra,
CUDA toolkit, Isaac, 드라이버 교체는 기본 설치에 포함하지 않는다.

관리자 설치 내용을 [스크립트](../scripts/install_ubuntu_jazzy.sh)에서 확인한 뒤 실행한다.
ROS 공식 `ros2-apt-source` 1.2.0 배포 파일은 SHA-256을 검사한다. 빌드 도구,
ROS Jazzy desktop/RViz, colcon, CycloneDDS, rosbag2 MCAP을 설치한다.
시스템 전체 upgrade·패키지 제거는 수행하지 않는다.

```bash
sudo bash scripts/install_ubuntu_jazzy.sh
# GUI 관리자 인증을 사용하는 경우:
# pkexec /bin/bash "$PWD/scripts/install_ubuntu_jazzy.sh"
```

APT 의존성의 최종 버전은 설치 시점 저장소에 따라 달라진다. `dpkg-query -W`를
호스트의 `.local/`에 저장하고 다른 장비에서도 실제 검증한다. APT snapshot까지
고정된 배포 이미지라는 의미는 아니다.

## 작은 MuJoCo 실행

```bash
MUJOCO_GL=egl uv run --locked python -m pai_lab.installation_smoke \
  --seed 7 --headless --output-dir .local/installation/pendulum
```

진자의 `qpos`는 각도(rad), `qvel`은 각속도(rad/s), `ctrl`은 motor torque(N m),
`data.time`은 시뮬레이션 시간(s)이다. +Z가 위이며 +Y 축으로 회전한다.
`mj_step` 한 번이 2ms를 전진시킨다. 같은 seed의 1,000개 상태를 두 번 비교하고,
시간 간격만 1ms로 바꾼 결과와 torque만 0.5N m로 바꾼 결과를 비교한다.
0ms·NaN·범위 밖 torque를 거부한다. CSV, 렌더링 PNG, 비교 그래프와 JSON을 검사한다.

## ROS localhost 점검

새 Bash 터미널마다 아래를 실행한다. CycloneDDS의 실제 통신 interface도 `lo`로
제한한다. domain 81은 이 오프라인 실습용이며 이미 사용 중이면 먼저 실습을 종료한다.

```bash
source /opt/ros/jazzy/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export ROS_DOMAIN_ID=81
unset ROS_STATIC_PEERS ROS_LOCALHOST_ONLY
export CYCLONEDDS_URI="file://$PWD/setup/cyclonedds_localhost.xml"
ros2 run demo_nodes_cpp talker
# 같은 설정을 적용한 두 번째 터미널:
# ros2 run demo_nodes_py listener
```

네이티브 ROS와 PyPI 의존성을 함께 쓰는 브리지는 `/usr/bin/python3`로 별도 venv를
만든다. `--system-site-packages`를 사용하면 APT의 colcon·setuptools도 보인다.
MuJoCo 등 프로젝트 의존성은 기존 lock으로 그 venv에 설치한다. ROS Python ABI와
실제 `sys.base_prefix == '/usr'`를 확인한다. Mac의 Pixi lock을 Ubuntu에 복사하지 않는다.

## WS1 실측 결과: 2026-09-08

Ubuntu 24.04.5, Python 3.12.3, RTX 5090, NVIDIA 595.84를 확인했다. 설치 후에도
드라이버는 595.84다. uv 0.12.10, MuJoCo 3.12.0, NumPy 2.5.2를 사용했다.
public 테스트 3 passed/12 skipped, core 테스트 8 passed. Wuji vendor asset 미수신으로
12개를 skip했으며 해당 모델 검증을 완료했다고 보지 않는다.

진자 상태 1,000개 모두 유한, 반복 오차 0, 2ms/1ms 최대 각도 차이
0.0015375537rad. EGL 렌더링과 [비교 그래프](../docs/evidence/ws1-ubuntu/comparison.png)를
눈으로 확인했다. [수치 증거](../docs/evidence/ws1-ubuntu/pendulum-summary.json)를 보존한다.
ROS Jazzy의 C++→Python localhost 메시지, RViz와 MCAP 기능도 현재 호스트에서 검증했다.

`pal doctor`는 저장소·Python 버전·튜토리얼 graph를 검사한다. 실제 GPU 연산,
ROS, 모델, 표시 장치, lock 설치 일치, capability/mode와 다음 튜토리얼 선택을
보증하지 않는다. `pal tutorial next`도 현재 prerequisite만 확인한다.
T00에서 capability/mode·선택 로직을 보완하고 정식 acceptance를 수행해야 한다.
이번 작업은 설치 검증이며 **공개 진척은 0/40, T00 pending**이다.

공식 근거: [ROS Jazzy Ubuntu 설치](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html),
[ROS Python 환경](https://docs.ros.org/en/jazzy/How-To-Guides/Using-Python-Packages.html),
[uv 설치](https://docs.astral.sh/uv/getting-started/installation/).
