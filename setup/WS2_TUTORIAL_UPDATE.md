# WS2: “튜토리얼 업데이트 해줘” 실행 인계

기록: 2026-11-09, MacBook. 이 문서는 다음 WS2 세션의 실행 지침이며,
WS2에서 새 Isaac 검증을 수행했다는 증거가 아니다.

## 시작 문장과 범위

WS2의 robotics 작업 공간 또는 `tutorial-robotics` / 비공개 overlay에서
사용자가 **“튜토리얼 업데이트 해줘”**라고 요청하면 다음 작업을 이어간다.
긴 프롬프트를 다시 요구하지 않는다. 이 문구를 문서에 기록하거나 인용하는
작업 자체는 WS2 실행 요청으로 해석하지 않는다.

이 요청은 저장소 동기화만이 아니라 **새 로봇 학습 경로의 실제 Isaac/PhysX
개발 검증 배치**, 발견한 범위 내 코드/API 호환성 수정, 재검증, 문서·호스트
기록 갱신, 검증된 변경의 커밋·푸시·CI 확인까지 포함한다. 일반 학습의
“한 수업 후 멈춤” 규칙은 이 개발 배치에 적용하지 않는다.
실제 로봇·VR 장치·펌웨어·드라이버 설치나 조작은 이 요청에 포함하지 않는다.

## 먼저 읽을 내용

1. 현재 저장소와 상위 `AGENTS.md`, public `agent/workflow.md`.
2. [구현·환경별 검증 기록](../docs/verification/robot-paths-2026-11-08.md),
   [한글 학습 경로](../docs/ko/paths.md), `curriculum/catalog.json`,
   `curriculum/paths.json`과 실행할 수업 문서.
3. public `state/HOST_STATUS.md`와 해당 네이티브 OS 설치 기록:
   [Ubuntu](../docs/WS2_UBUNTU_INSTALLATION_STATUS.md) /
   [Windows](../docs/WS2_WINDOWS_INSTALLATION_STATUS.md).
4. overlay가 있으면 그 저장소의 `AGENTS.md`, `PUBLIC_BASE.lock`, 호스트 기록.
   공개 작업은 public 저장소에서 수행하며 비공개 구현을 복사하지 않는다.
5. ignored 로컬 검증 receipt·run·체크포인트가 있으면 먼저 읽고 마지막
   실패/미검증 단계에서 재개한다. 과거 설치 성공은 새 수업 성공이 아니다.

## 저장소와 환경 점검

- 로컬 변경, 브랜치, 원격, 진행 중인 작업을 확인하고 보존한다. 개인 계정
  `terryum` / `terry.t.um@gmail.com`을 사용하며 GitHub 쓰기 전에 `gh context`를
  확인한다. `gh auth switch`, 강제 push/reset, vendor pin의 임의 갱신은 하지 않는다.
- 관련 저장소의 원격을 조회하고 가능한 경우 `git pull --ff-only`로 동기화한다.
  pull 후 **갱신된 AGENTS·workflow·이 문서를 다시 읽는다**. 분기/충돌은 로컬
  작업을 보존하며 해결하고, 해결이 불가능한 경우에만 정확한 차단 사유를 남긴다.
- 실제 native OS, Python, GPU·드라이버, 설치된 Isaac 버전과 사용 중인 Python
  실행 환경을 확인한다. 현재 새 Isaac 수업의 지원 경로는 **네이티브 Ubuntu
  24.04 + NVIDIA GPU + 설치된 Isaac Sim**이다. 호스트 이름만으로 준비를 가정하지 않는다.
- Windows라면 읽기 전용 환경·저장소 점검과 적용 가능한 수정/문서화까지 진행하고,
  현재 Ubuntu 수업 실행은 차단 상태로 남긴다. 플랫폼 필터를 바꾸거나 Windows의
  기존 Hello World 기록을 새 수업 검증으로 대신하지 않는다. OS 전환·재부팅은 하지 않는다.
- 정상인 설치와 vendor 캐시는 재사용한다. 기존 locked Core 환경만 필요한 범위에서
  동기화하고, GPU 드라이버·CUDA·Isaac·ROS·시스템 패키지·대형 모델을 자동 설치하지 않는다.
  설치나 약관 동의가 필요하면 이미 유효한 승인이 있는지 먼저 확인하고, 없다면
  정확한 부족 항목과 필요한 다음 행동을 남긴다. 약관 동의를 대신 생성하지 않는다.
- 설치된 Isaac Python 문맥에서 `pal host detect --json` 및
  `pal setup verify --profile isaac --json`을 확인한다. 일반 `.venv`에서 Isaac을
  찾지 못하는 것과 설치된 Isaac 자체가 없는 것을 구분한다.

## 실제 실행 순서

개발 상태는 새 ignored 경로로 분리한다. 예를 들어 public 저장소에서:

```bash
export PAL_LOCAL_DIR="$PWD/.local/verification/ws2-isaac-update"
pal host detect --json
pal setup verify --profile isaac --json
```

overlay 검사 시에도 별도의 ignored `PAL_PRIVATE_LOCAL_DIR`을 설정한다.
기존 개인 진도·피드백·브라우저·동기화 설정과 완료 기록을 변경하지 않는다.
필요한 공개 자산만 manifest의 고정 커밋·파일 해시·라이선스로 검증/준비한다.

| 순서 | 수업 | 확인할 것 |
|---|---|---|
| 1 | `core-fr3-09` 기준 실행 → `sim-fr3-01` | 동일 FR3·초기 자세·월드 TCP 목표·제어 주기, 관절 구동·IK·궤적·프로브 접촉·관측·렌더링·종료 |
| 2 | `sim-fr3-02`, `sim-fr3-03` | 실제 PhysX 시연/rollout으로 BC·PPO, 독립 평가, 학습 체크포인트 |
| 3 | `sim-fr3-04` | 실제 MuJoCo·PhysX 증거의 조건 일치와 관절/TCP 오차·주기·접촉 비교 |
| 4 | `sim-enlight-03`, `sim-enlight-04`, `sim-enlight-05` | Enlight 자체 관절·좌표계·시연·학습·평가. FR3 배열/가중치를 재사용하지 않음 |
| 5 | `sim-shadow-01` | 개별 관절·열기/쥐기 시너지·물체 접촉·동적 연동 관계 |
| 6 | `sim-stretch3-01` | 바퀴 속도·팔 위치 그룹, 자유 베이스·연동·접촉·베이스/팔 협응 도달 |

먼저 FR3 실제 실행 하나를 안정화한 뒤 범위를 넓힌다. 각 행에서 필요한
MuJoCo 기준 실행과 입력 산출물도 실제로 생성·검증한다.

개인 선행 수업 이력이 없어서 일반 `pal lesson run`이 막힐 때는 완료 기록을
만들거나 learner용 readiness를 약화하지 않는다. 분리된 개발 검증 하네스에서
**학습 이력 요건만** 분리하여 실행한다. 플랫폼·의존성·모델 해시·실제 입력
산출물·물리/수치 검사는 유지하고 사용한 하네스와 예외 범위를 기록한다.

## 통과 기준과 수정

- 프로세스 종료 코드나 모델 import만으로 성공 처리하지 않는다. 실제 구동기
  반응, 관절 이름/주소·단위·좌표계·TCP/Jacobian, mimic/텐던·폐루프 관계,
  자유 베이스와 물체별 접촉 센서, 수치 trace와 렌더 이미지를 확인한다.
- **PhysX**를 사용한다. MuJoCo stepping이나 Newton/MuJoCo-Warp로 Isaac의
  독립 엔진 실행 성공을 대체하지 않는다. 연동이나 프레임이 잘못되면 수정 후 재검증한다.
- BC 데이터는 에피소드 단위 train/validation/test를 유지한다. 도달 정책은 독립
  목표 20회 중 최소 16회에서 10 mm 이내를 연속 10 제어 단계 유지해야 성능 통과다.
  optimizer 검사 통과와 과제 성능을 분리한다. 이는 실물 허용 오차가 아니다.
  짧은 학습의 실패를 숨기거나 임의로 성능 문턱을 낮추지 않는다.
- BC/PPO의 정상 중단·SIGINT/SIGTERM·마지막 정상 체크포인트 재개, 소스/모델/
  데이터/환경 불일치 거부를 실제 Isaac 실행에서 확인한다. transfer export/import의
  해시도 검증한다. 이 과정에 장비 설정·자격증명·실물 승인 receipt를 포함하지 않는다.
- 문제를 발견하면 해당 공개 코드와 한영 수업을 범위 내에서 수정하고 영향받은
  검사를 반복한다. 필요한 환경이 없으면 `capability-unavailable`로 남기고
  가능한 독립 작업은 계속한다. 정책 성능 미달과 환경 차단을 구분한다.

## 저장·커밋·종료

- ignored 검증 상태에 실제 실행 명령, 버전/코드/모델·입력 해시, 단계,
  기준/비교 run, 관측 결과, 실패 사유, 다음 행동과 재개 명령을 원자적으로 남긴다.
  재실행은 새 run 디렉터리를 사용하고 원본 증거를 보존한다.
- 공개 보고서에는 수치 요약·검증 범위·차단 사유만 담는다. 원시 로그, 데이터,
  체크포인트, 주소, 일련번호, 인증·현장 설정은 커밋하지 않는다.
- 전체 회귀 테스트, Ruff·mypy, repository/release/public-boundary/credential
  검사와 strict 문서 빌드를 수행한다. GPU 검증 배지는 실제 증거가 있는 수업만 갱신한다.
- **실제로 작업한 WS2 native OS 행만** 호스트 ledger에서 갱신한다. 다른 호스트의
  기록을 덮지 않는다. Mac에서 준비한 이 문서만으로 WS2 행을 완료 처리하지 않는다.
- 검증된 public 변경을 커밋하고, overlay가 있으면 새 public/core pin에 필요한
  호환성 검사·exact-pin doctor·비공개 증거 갱신을 수행한다. 비공개 구현은 수정하지 않는다.
  CI/문서만 바뀌어 runtime이 동일하면 그 근거와 재검증 범위를 명시한다.
- 이 shortcut 요청은 위 범위의 검증된 코드/문서/pin의 **커밋·푸시**도 포함한다.
  기존 권한과 환경 승인이 충분하면 같은 승인을 다시 묻지 않는다. 개인 계정과
  공개/비공개 경계를 확인한 뒤 푸시하고 원격 커밋·CI·작업 트리 동기화를 확인한다.
- 통과 시 검증된 수업·성능·커밋·CI를 보고한다. 차단 시 준비된 내용과 미검증 내용을
  구분하고, 다음에 같은 문장을 말하면 마지막 미완료 단계에서 이어가도록 기록한다.
  모든 단계가 이미 현재 소스로 검증되었다면 차이만 점검하며 무조건 재학습하지 않는다.

## 이번 인계의 시작 상태

2026-11-08 Mac 구현 기준으로 공개 수업은 68개이며 기존 49개 ID/별칭을 보존한다.
Mac MuJoCo 수치·렌더링 검증과 공개/비공개/코어 회귀 검사는 수행했다.
WS2 검증용 SSH 연결은 시간 초과였으므로 **새 Isaac/PhysX 수업은 실행 미검증**이다.
실제 로봇 검증도 미완료이며 이 shortcut으로 로봇을 연결하거나 움직이지 않는다.
다음 세션에서는 이 과거 스냅샷보다 최신 저장소와 실제 로컬 증거를 우선한다.
