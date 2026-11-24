# WS2 한국어 오프라인 교재 검증

WS2에서 `main`을 동기화한 뒤 **“워크스테이션 부분의 튜토리얼 검증해줘”**라는 요청을 받으면 이 런북을 실행합니다. 범위는 공개 소프트웨어, 시뮬레이션, 고정 입력 추론입니다. 장비와 학습자 상태는 분리합니다. 드라이버, CUDA, Isaac Sim, 장치 SDK, 대형 체크포인트, 새 약관 동의 또는 재부팅이 필요한 단계는 차단 상태로 기록하고 실행 가능한 다른 단계를 계속합니다.

## 체크아웃과 네이티브 환경

1. 저장소의 `AGENTS.md`, `agent/workflow.md`, [기존 WS2 런북](WS2_TUTORIAL_UPDATE.md)과 해당 OS의 공개 설치 기록([Ubuntu](../docs/WS2_UBUNTU_INSTALLATION_STATUS.md), [Windows](../docs/WS2_WINDOWS_INSTALLATION_STATUS.md))을 읽습니다. `git status --short --branch`와 `git remote -v`로 기존 작업과 원격을 확인합니다. 가능한 경우 `git pull --ff-only`로 동기화한 뒤 갱신된 지침을 다시 읽습니다. 작업이 갈라져 있으면 양쪽 커밋을 확인하고 보존합니다.
2. `git rev-parse HEAD`, `uname -srm`, `cat /etc/os-release`, `nvidia-smi`로 소스 커밋, 네이티브 OS/아키텍처, GPU와 드라이버를 확인합니다. Windows 세션에서는 PowerShell의 `Get-CimInstance Win32_OperatingSystem`과 `nvidia-smi`를 사용합니다. 네이티브 Ubuntu 24.04 x86_64의 기존 Isaac 환경이 준비된 경우에만 카탈로그의 `sim-enlight-03/04/05`를 실행합니다. 다른 OS에서 실행 가능한 항목은 각각의 플랫폼과 런타임으로 확인합니다.
3. Core Python과 Isaac이 실제로 사용하는 Python의 경로 및 버전을 확인합니다. 해당 Python에서 `python -m pai_lab.cli host detect --json`과 `python -m pai_lab.cli setup verify --profile core --json` 또는 `--profile isaac`를 실행하고 준비 여부를 읽습니다. Isaac Sim·PhysX와 NVIDIA 추론 저장소의 버전 또는 Git 커밋, 사용한 GPU 모델과 드라이버, 모델 가중치·입력 데이터의 리비전 및 SHA-256을 기록합니다.
4. 기존 공개 캐시의 Enlight 리비전과 파일 SHA-256은 `assets/model-lock.json`에 대조합니다. `pai_lab.lessons.models.provenance("enlight")`가 성공해야 로봇 실습을 시작합니다. 설치가 준비된 Core 환경에서 가져올 수 있는 고정 공개 로봇 모델만 기존 `pal assets fetch flexiv-description` 경로로 준비한 뒤 다시 검사합니다. API 토큰, 장치 정보, 모델 캐시의 로컬 경로와 비공개 입력은 공개 요약에서 제외합니다.

로컬 기록은 ignored 경로에 둡니다. 한 검증 배치의 루트를 고정하고 배치 간에는 새 경로를 사용합니다. 아래 예의 `WS2_RUN`은 Bash 변수입니다. 각 명령의 Python은 위에서 검증한 해당 가상환경 또는 Isaac Python을 사용합니다.

```sh
export WS2_RUN="$PWD/outputs/robotics-ko/ws2-$(git rev-parse --short HEAD)"
export PAL_LOCAL_DIR="$WS2_RUN/state"
mkdir -p "$PAL_LOCAL_DIR"
```

## 1. MuJoCo 기준 재실행

```sh
python scripts/verify_robotics_ko.py lessons core-enlight-03 core-enlight-04 core-enlight-05 --seed 7 --samples 64 --output-dir "$WS2_RUN/mujoco"
python examples/robotics_ko/isaac_enlight_rgbd.py --engine mujoco --output-dir "$WS2_RUN/rgbd-mujoco"
```

`lessons.json`의 `status`와 `run_dir`을 읽습니다. `core-enlight-03`에서 7개 이름과 초기 각도, 월드 TCP 목표, 20 ms 제어 주기, 유한한 상태와 궤적을 확인합니다. TCP 추종 구간의 오차 RMSE는 20 mm 미만이고 첫 관절의 이동 범위는 0.01 rad를 넘어야 합니다. BC·PPO는 갱신 실행과 독립 평가 값을 각각 기록합니다. 초기 자세 RGB-D 기준선의 카메라 계약과 파일 해시도 보관합니다.

교육용 작업대 집기 예제 결과를 재생성할 때는 책의 해당 명령과 씨드를 사용합니다. 물체가 그리퍼에 닿아 들린 높이와 최종 영역 오차를 검증합니다. 암 도달 정책과 물체 집기 결과는 별도 과제 근거로 기록합니다.

## 2. Enlight PhysX 관절·TCP 추종과 RGB-D

```sh
python scripts/verify_robotics_ko.py lessons sim-enlight-03 --seed 7 --samples 64 --output-dir "$WS2_RUN/physx"
python examples/robotics_ko/isaac_enlight_rgbd.py --engine physx --output-dir "$WS2_RUN/rgbd-physx"
```

- `physx-observations.json`에서 실제 PhysX 실행임을 확인합니다. 모델 파일 지문, 관절 이름·순서, 기준 자세, 월드 좌표계, 제어 주기, 배열 길이와 시간별 목표를 MuJoCo와 대조합니다. 다른 값이 있으면 차이와 원인을 기록하고 동일 조건 비교를 보류합니다.
- `joint_errors_rad`의 앞 절반에서 관절 추종 오차를, 두 `trace.csv`의 뒤 절반에서 TCP 오차 RMSE를 계산합니다. 모든 오차는 유한해야 합니다. PhysX `probe_contact_forces_N`는 적어도 하나의 양의 센서 관측을 포함하고, 렌더링된 RGB에 공간 변화가 있어야 합니다. 추종 수업의 수치와 각 엔진의 차이를 보고합니다.
- 두 `rgbd.json`에서 고정 카메라 위치·축·시야각과 초기 관절각을 비교합니다. 각 `rgb.png`는 240×320×3, `depth.npy`는 240×320이며 깊이는 m 단위의 광축 거리입니다. 양수이면서 유한한 깊이 픽셀이 최소 100개, 유효 깊이 범위가 0.1 mm 이상이고 RGB의 공간 표준편차가 1을 넘어야 합니다. 기준 자세의 최대 관절각 오차 10⁻⁵ rad 이하, TCP 위치 오차 2 mm 이하를 요구합니다. 보고서에는 유효 픽셀 수, 깊이 최솟값·중앙값·최댓값과 파일 해시를 남깁니다. 해당 예제는 같은 카메라를 사용한 **기본 팔의 초기 자세** 비교입니다. 작업대 집기와 순차 카메라 기록은 별도 과제입니다.
- 호환성 수정이 필요하면 설치된 API와 카메라 샘플을 확인합니다. `sim-isaac-02`의 Wuji 카메라나 다른 엔진의 결과를 Enlight의 매칭 결과로 사용할 수 없습니다. [Replicator 카메라 관측 정의](https://docs.omniverse.nvidia.com/extensions/latest/ext_replicator/visualization.html)

## 3. PhysX 시연·BC·PPO와 독립 평가

```sh
python scripts/verify_robotics_ko.py lessons sim-enlight-04 sim-enlight-05 --seed 7 --samples 64 --output-dir "$WS2_RUN/physx"
```

1. `training-contract.json`의 엔진, 모델, 코드 지문과 학습 설정을 읽습니다. BC의 `demonstrations.json`은 자체 SHA-256을 남깁니다. 에피소드별 train/validation/test 할당이 겹치지 않으며 관측·행동의 형상과 수치가 유효해야 합니다. PPO는 PhysX rollout에서 얻은 보상과 갱신 기록을 확인합니다.
2. `physx-observations.json`의 가중치 L1 변화량이 양수이고 정책이 유한하며 재로딩 오차가 10⁻¹² 이하여야 짧은 학습 실행을 통과로 표시합니다. `evaluation.json`의 독립 평가 씨드 10007로 새 목표 20개를 검사합니다. 오차 10 mm 이하를 10 제어 단계 연속 유지한 목표가 16개 이상이면 과제 성능이 통과합니다. 짧은 학습이 실행됐어도 성능이 기준 미달이면 성공 수를 그대로 적습니다. 이 도달 평가에서 실물 또는 집기 성능을 추정하지 않습니다.

## 4. GR00T·Cosmos 추론

명령 예시는 [워크스테이션 교재](../book/robotics-ko/workstation.md)의 각 모델 절에 있습니다. 검증한 NVIDIA 체크아웃과 그 환경에서 실행합니다.

| 모델 | 고정 입력과 검증 기준 |
|---|---|
| GR00T N1.7 | 설치된 NVIDIA 체크아웃의 `scripts/deployment/standalone_inference_script.py`를 실행합니다. 공식 공개 DROID 샘플 및 호환 가중치와 `OXE_DROID_RELATIVE_EEF_RELATIVE_JOINT` 태그를 사용합니다. 예측 행동 키와 형상이 해당 embodiment 계약과 일치하고 데이터가 유한해야 합니다. 에피소드 ID, 행동 길이, 개방루프의 행동 비교 오차 및 추론 시간을 기록합니다. 캐시에 없거나 모델 접근이 필요한 경우에는 차단 사유로 남깁니다. [NVIDIA 실행 예제](https://github.com/NVIDIA/Isaac-GR00T#inference) |
| Cosmos-Predict2.5 | 설치된 가중치와 맞는 공식 Image2World 구성을 선택합니다. 같은 첫 영상 프레임, 텍스트, 씨드, 샘플러로 추론합니다. 영상이 디코딩되고 유효한 프레임이 여러 개 있으며 시간에 따른 변화가 있는지 확인합니다. 프레임 수, 해상도, FPS와 출력 영상 해시를 기록합니다. [NVIDIA 추론 가이드](https://github.com/nvidia-cosmos/cosmos-predict2.5/blob/main/docs/inference.md) |
| GR00T 2 | 연구 페이지의 코드 공개 여부와 설치된 하드웨어·소프트웨어 호환성을 다시 확인합니다. 공개되지 않았거나 호환 환경이 없으면 사유와 확인일을 기록합니다. 설치된 지원 환경이 있으면 공식 샘플의 영상·행동 결과를 개별 검증합니다. [NVIDIA 연구 페이지](https://research.nvidia.com/labs/gear/gr00t-2/) |

추론 결과는 오프라인 파일과 수치로 확인하며 장비 명령, 네트워크를 통한 외부 추론 요청 또는 실물 평가로 확장하지 않습니다.

## 실패 이후 재개와 공개 요약

검증 명령은 같은 출력 폴더의 `lessons.json`에서 설정과 검증이 일치한 통과 항목을 재사용합니다. 일부 항목이 차단·실패해도 같은 호출의 나머지 항목은 진행됩니다. 미검증 항목부터 다시 실행합니다. 같은 환경에서 특정 입력을 새로 검증하려면 해당 ID와 `--retry`를 지정합니다. 호스트, 드라이버, Python 또는 런타임 버전이 바뀌면 새 배치 경로를 사용합니다. RGB-D 예제를 재시험할 때는 개별 카메라 출력에 새 폴더를 사용합니다. 선행 항목이 실패한 상태에서 독립 실행은 계속하고, 같은 초기 조건·입력이 필요한 비교는 차단으로 남깁니다. 각 단계의 명령, 사용한 버전과 해시, 수치 또는 구체적인 차단 이유는 로컬 배치에 기록합니다.

공개 요약은 `book/robotics-ko/ws2-results.json`에 저장합니다. 아래 예는 필드를 설명하는 빈 보고서입니다.

```json
{
  "schema_version": 1,
  "source_commit": "실제로 검증한 40자리 Git 커밋 해시",
  "environment": "네이티브 OS와 Python·GPU·드라이버·Isaac Sim·모델 버전 요약",
  "checks": [
    {
      "id": "physx-rgbd",
      "title": "Enlight PhysX RGB-D",
      "status": "pending",
      "evidence": "아직 실행하지 않았습니다."
    }
  ]
}
```

항목 ID를 안정적으로 유지합니다. 예를 들어 `mujoco-tracking`, `mujoco-rgbd`, `physx-tracking`, `physx-rgbd`, `physx-bc-training`, `physx-bc-evaluation`, `physx-ppo-training`, `physx-ppo-evaluation`, `gr00t-n1-7`, `cosmos-predict2-5`, `gr00t-2`를 각각 사용합니다. 실행과 기준을 확인하면 `passed`, 실행했으나 검사 미달이면 `failed`, 실행 요건이나 필수 선행 결과가 없으면 `blocked`, 아직 선택하지 않은 항목은 `pending`입니다. `evidence`에 공개 가능한 수치, 단위, 버전, 검증한 입력과 산출물의 해시, 그리고 실패·차단 사유를 기록합니다.

Docs 의존성이 설치된 환경에서 `python scripts/build_robotics_ko.py`를 실행하고 `outputs/robotics-ko/index.html`을 열어 요약 값이 표시되는지 확인합니다. 현재 지침의 테스트와 공개 경계 검사를 실행하고 `gh context`에서 `terryum`과 소유자를 확인합니다. 검증한 수정과 공개 요약만 스테이징하여 `terry.t.um@gmail.com`으로 커밋하고 `origin/main`에 푸시합니다. 정확한 커밋의 CI 결과와 마지막 미검증 항목을 남깁니다. Mac에서는 `main` 동기화 뒤 저장소의 빌더를 다시 실행하면 같은 HTML에 WS2 근거가 반영됩니다.
