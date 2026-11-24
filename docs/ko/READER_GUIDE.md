<!-- pal:language:start -->
<p align="right">
  <a href="READER_GUIDE.md" lang="ko">한국어</a> | <a href="../en/READER_GUIDE.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

<a id="github에서-읽고-직접-실행하기"></a>

# AI와 대화하며 수업 진행하기

이 안내는 Codex 또는 Claude Code에 요청을 붙여 넣고 한 수업씩 배우는 흐름을 설명합니다. 명령은 에이전트가 실행하며, 독자는 이론·측정값·그래프를 함께 읽습니다. 아래 터미널 참고는 직접 실행하거나 오류를 확인하려는 경우에만 펼쳐 보세요. 날짜가 붙은 과거 설치 보고가 현재 준비 상태를 대신하지는 않습니다.

## Codex 또는 Claude Code에서 시작

**Codex 또는 Claude Code로 시작하는 것을 권장합니다.** 아래 한 문장을 대화창에 붙여 넣으세요. 터미널 명령을 먼저 외울 필요는 없습니다.

```text
https://github.com/terryum/tutorial-robotics 이 레포를 받아서 설치해주고 튜토리얼을 시작해줘
```

에이전트는 기존 체크아웃이 있으면 재사용하고, 없으면 저장소를 받습니다. 저장소 지침을 읽고 실제 OS·환경을 확인한 뒤 최소 Core 설치 계획을 보여 주고 필요한 준비만 적용·검증합니다. 기존 `.venv`, 잠금 파일과 `.local/` 진도를 보존합니다. 현재 호스트에서 준비 검증을 통과한 기존 환경은 재설치하지 않습니다. 지원하지 않는 환경이나 설치 실패는 차단 사유와 다음 행동을 설명하며 준비 완료로 표시하지 않습니다.

완료했거나 진행 중인 학습 수업이 없으면 에이전트는 준비 검증을 마치고 다음 안내를 한 뒤 **실제 사용자 응답을 기다립니다**. 환경 진단만 마친 경우에도 첫 진자 수업부터 시작합니다. 저장한 학습 상태가 있으면 에이전트가 마지막 수업과 단계를 알려 주고 이어갈지 묻습니다.

> 첫번째 튜토리얼을 띄울 준비가 되었습니다. 시작하시겠습니까?

이때 첫 수업 실행이나 수업 탭 열기는 아직 시작하지 않습니다. 시작할 준비가 되면 답하세요.

```text
네, 첫번째 튜토리얼을 시작해줘.
```

답을 받으면 에이전트가 [첫 진자 수업 `core-01`](lessons/core-01.md)의 GitHub 페이지를 현재 언어로 엽니다. 두 가지 시작 각도를 비교한 뒤 결과를 보여 주고 이해 확인 질문을 합니다. 브라우저를 제어할 수 없는 환경에서는 교재 링크를 안내합니다.

특정 수업의 실행을 명시적으로 요청하면 에이전트는 준비를 확인한 뒤 그 수업을 실행합니다. 설치 환경을 따로 점검하려면 [`core-00`(`T00`) 진단](lessons/core-00.md)을 요청하세요. 예전 `T00` 기록은 보존하며, 진단 실행은 학습 진도에서 제외합니다.

## 대화로 진행하는 요청

### 다음 수업

```text
다음 단계 실행해줘.
```

### 새 대화에서 이어서

```text
https://github.com/terryum/tutorial-robotics 이전 대화를 지웠으니 같은 기존 체크아웃에서 이어서 진행해줘. 저장소 지침과 curriculum/catalog.json, agent/workflow.md를 다시 읽고 .local/progress.json, .local/session.json, 피드백과 기존 실행 근거를 확인해줘. 재설치·재복제·진도 초기화 없이 마지막 중단 단계부터 이어서 한 수업만 진행해줘.
```

### 현재 수업 다시 실행

```text
다시 실행해줘. 기존 실행 근거를 보존하고 새 실행 폴더를 사용해줘.
```

### 진도 확인

```text
진도 확인해줘. 완료한 수업, 현재 단계, 남은 선행 조건과 다음에 할 일을 알려줘.
```

### 잠시 멈추기

```text
여기서 멈추고 현재 수업과 설명·비교 단계, 실행 경로와 다음 시작점을 저장해줘.
```

### 질문·개선점

```text
[개선점] 그래프의 축과 단위를 더 쉽게 설명해줘.
```

<a id="manual-setup"></a>

## 처음 준비 — Mac Terminal, zsh

<details markdown="1">
<summary>수동 준비와 브라우저 동작 참고</summary>

시작 언어는 Codex/Claude Code의 대화 언어를 따릅니다. 모든 교재 페이지 본문 상단 오른쪽의 **한국어 | ENGLISH**를 누르면 같은 챕터의 다른 언어로 이동합니다. 페이지 아래의 다음 수업 링크도 그 언어를 유지합니다. 에이전트에게 다음 수업을 요청하면 현재 교재 탭의 언어를 확인해 같은 언어의 교재와 설명을 이어갑니다. 중간에 다시 언어 링크를 누르거나 대화에서 언어 변경을 명시하면 새 선택을 따릅니다. 탭을 닫았을 때는 에이전트가 마지막으로 확인한 언어를 복원합니다.

첫 수업을 시작하겠다고 답하면 에이전트가 [진자 실험 한국어 GitHub 교재](https://github.com/terryum/tutorial-robotics/blob/main/docs/ko/lessons/core-01.md)를 브라우저에 엽니다. 교재 탭이 없으면 새 탭을 하나 만들고, 다음 수업이나 재실행에서는 같은 교재 탭을 해당 수업으로 이동합니다. 다른 작업의 탭은 그대로 둡니다. 브라우저 연결이 없으면 에이전트가 그 사실과 링크를 안내하므로 직접 열어도 됩니다.

한쪽에는 Codex/Claude Code 대화와 터미널, 다른 쪽에는 GitHub 교재를 두고 진행합니다. 에이전트가 짚어주는 Expected·Observe·How it works를 읽으며 실제 결과와 이론을 연결합니다. 공통 기초 실험에서는 별도 창이나 결과 탭에 로컬 결과 페이지를 엽니다. 교재를 여는 것만으로 시뮬레이션이 실행되지는 않습니다.

Git은 고정 소스 버전을 받고, Python은 실험을 실행하며, uv는 잠긴 의존성을 `.venv`에 설치합니다. MuJoCo는 동역학과 렌더링, NumPy는 수치 계산을 담당합니다. GUI용 프로그램을 따로 설치할 필요는 없습니다.

아직 체크아웃이 없다면 `git clone https://github.com/terryum/tutorial-robotics.git`으로 받은 뒤 그 폴더를 사용합니다. 기존 체크아웃이 있으면 새로 복제하지 않습니다. 아래는 기존 폴더로 이동하는 예입니다. 다른 곳에 복제했다면 첫 경로를 바꿉니다. 이 안내의 상대 경로는 모두 저장소 루트 기준입니다.

```bash
cd ~/Codes/robotics/tutorial-robotics
```

```bash
sh bootstrap.sh --plan
```

OS·architecture·디스크·Python·uv·환경 위치와 설치 명령을 출력하고 종료합니다. 준비가 필요한 경우 다음 명령으로 최소 Core 환경을 설치합니다. 다운로드가 진행되는 동안 기다립니다. 실패하면 오류 원문을 보존하고 plan을 다시 읽습니다.

```bash
sh bootstrap.sh --apply
```

```bash
source .venv/bin/activate
```

```bash
pal setup verify --profile core --json
```

`ready: true`를 확인합니다. `false`면 missing_capabilities를 해결한 뒤 같은 verify 명령을 반복합니다. CUDA·ROS·Isaac은 해당 수업의 외부 환경에서 별도 준비합니다.

수동으로 첫 수업을 시작하기로 결정한 뒤에만 아래 과정 선택으로 넘어갑니다. 에이전트 준비 단계에서는 init/next를 자동 실행하지 않습니다.

```bash
pal course init --json
```

```bash
pal course next --json
```

선행 조건을 충족한 수업을 하나 선택합니다. 처음 시작하거나 환경 진단만 마쳤다면 `core-01`로 시작합니다. `init`을 실행해도 기존 `completed` 기록은 남습니다.

</details>

## 새 터미널에서 재개

대화를 지우거나 새 채팅을 열어도 같은 체크아웃의 기록은 남아 있습니다. 다음 요청을 붙여 넣으세요.

```text
https://github.com/terryum/tutorial-robotics 이전 대화를 지웠으니 같은 기존 체크아웃에서 이어서 진행해줘. 저장소 지침과 curriculum/catalog.json, agent/workflow.md를 다시 읽고 .local/progress.json, .local/session.json, 피드백과 기존 실행 근거를 확인해줘. 재설치·재복제·진도 초기화 없이 마지막 중단 단계부터 이어서 한 수업만 진행해줘.
```

에이전트가 현재 파일에서 마지막 수업과 단계를 읽고 저장된 근거에서 이어갑니다. 이해 확인을 기다리는 중이면 같은 결과를 열고 저장된 질문을 다시 합니다. 체크아웃이 여러 개라 구분할 수 없다면 사용할 기존 경로만 확인합니다. 다른 호스트의 준비 상태를 진도 파일로 대신하지 않습니다.

<details markdown="1">
<summary>새 터미널의 직접 조회 명령</summary>

새 터미널마다 `cd`와 `source .venv/bin/activate`를 다시 실행합니다. 설치를 반복할 필요는 없습니다.

진도는 현재 클론의 `.local/progress.json`에 완료 시각과 함께 저장됩니다.
마지막 수업과 단계는 `.local/session.json`, 피드백은 `.local/feedback.json`,
실행·복습 증거는 `.local/runs/`에 남습니다. 터미널을 닫아도 유지되며,
`.local/`은 Git에서 제외되므로 다른 사용자에게 공유되지 않습니다.
다시 이어가려면 같은 클론과 `.local/`을 보존하세요. 새 클론은 완료 수업 없이 시작합니다.

```bash
pal course list --json
pal course next --json
```

`list`는 완료·미완료 학습 수업을, `next`는 다음으로 실행할 수업을 보여 줍니다.
아래 `status`는 남은 수업과 재검토가 필요한 수업만 보여줍니다.
`pal course init`을 다시 실행해도 기존 완료 기록은 유지됩니다.

```bash
pal course status --json
```

```bash
pal feedback list --json
```

```bash
python -m json.tool .local/session.json
```

마지막 명령은 한 번 이상 실행한 세션에서 사용합니다. session.json이 없으면 `pal course next --json`부터 시작합니다. `pal: command not found`는 대개 활성화가 빠졌다는 뜻입니다.

다른 컴퓨터에서는 잠금 파일과 모델 소스를 준비하고 그 호스트에서 verify를 다시 합니다. 진도 파일을 복사해 환경 검증을 대체하지 않습니다. 원본 실행 자료는 보존하고 새 실행 폴더를 사용합니다.

</details>

## 한 수업의 작업 순서

위의 시작 또는 다음 수업 요청을 받으면 에이전트가 아래 절차를 맡습니다. 독자는 실제 결과를 보며 설명을 확인하고 질문합니다. 한 수업을 마쳤다고 다음 수업을 자동 시작하지 않습니다.

1. 배울 내용과 이유를 읽고, 입력을 바꾸면 어떤 결과가 나올지 예측합니다.
2. 에이전트가 바꿀 입력과 고정할 조건을 코드에서 짚고 Action 명령으로 기준 실험을 실행합니다.
3. 에이전트가 `lesson inspect`로 산출물과 수치를 확인합니다. 결과에서 예측을 확인할 축과 단위를 찾습니다.
4. Try it에서 한 가지 입력만 바꾸고 어떤 차이가 생겼는지 읽습니다. 해시와 모델 차원 수업은 한 번의 실행에 비교 결과를 함께 기록합니다.
5. 공통 기초 수업에서 에이전트가 `pal lesson present`로 검증한 실행 기록을 결과 페이지에 담고 교재와 별도 창에 직접 엽니다. 별도 창이 어려우면 결과 탭을 엽니다. 페이지에 결과가 표시되는지 확인한 뒤 사용자가 창을 닫거나 다음 수업에서 에이전트가 자신이 연 창임을 확인하고 교체할 때까지 열어 둡니다. 화면을 제어할 수 없는 환경에서는 실제 수치와 채팅에서 지원하는 이미지를 보여 줍니다. PNG는 Mac의 `open`이나 파일 관리자에서 직접 열 수 있고, CSV는 텍스트 편집기로 읽을 수 있습니다.
6. 에이전트는 결과와 질문을 이해 확인 대기 상태로 저장합니다. 답을 함께 확인하거나 독자가 완료를 요청한 뒤 `lesson review`와 `lesson finish`로 진도를 기록합니다. 다음 수업은 요청을 받으면 시작합니다.

`baseline-01`이 이미 있으면 `baseline-02`처럼 새 이름을 씁니다. 기존 폴더를 덮어쓰지 않습니다. 실패한 `run.json`도 원인 기록으로 남깁니다. 프로세스가 계속 실행 중이고 중단하려면 Terminal에서 Ctrl-C를 누릅니다.

## 모델 재생과 Mac 조작

```text
방금 수업의 저장된 모델 상태를 재생해서 보여주고, 그래프와 같은 시점의 관절·좌표계를 설명해줘.
```

저장 상태 재생은 새로운 동역학 실험이 아닙니다. 에이전트가 실제 저장 근거가 있는지 확인하고 적절한 viewer 또는 그림을 사용합니다.

<details markdown="1">
<summary>직접 재생하는 명령과 Mac 조작</summary>

모델 상태가 저장된 수업에서, ID와 경로를 실제 실행으로 바꿉니다.

```bash
mjpython -m pai_lab.cli lesson view core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01
```

재생 창은 저장 상태를 한 번 재생하고 종료합니다. `--speed 0.25`로 느리게 봅니다. 마우스 왼쪽 드래그는 회전, 오른쪽 드래그는 이동, 스크롤은 확대입니다. 트랙패드의 보조 클릭을 오른쪽 클릭으로 사용하고 조작이 불편하면 마우스로 시작합니다. Shift를 누른 드래그는 수평 조작입니다. 화면의 축·모델 joint/frame 이름을 맞춰 읽습니다. 창 닫기로 종료할 수 있습니다.

이 명령은 저장한 qpos/qvel을 대입하고 `mj_forward`로 표시합니다. `mj_step`으로 동역학을 재실행하지 않으므로 접촉·힘에 대한 새 실험 증거를 만들지 않습니다. GUI가 없는 호스트에서는 마지막 상태의 그림을 만듭니다.

```bash
pal lesson view core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01 --offscreen .local/pd-replay-01.png
```

이전 실행에 replay 파일이 없으면 그대로 보존하고 새 실행을 만듭니다. 바이너리 모델 재생에는 같은 MuJoCo 버전을 사용합니다.

</details>

## 학습 중단·재개와 호스트 이동

긴 학습은 짧은 수업과 별도로 실행합니다. FR3 가중치를 Enlight 후보로 쓰지 말고 해당 모델에서 다시 학습·평가하세요. 위치 증분 정책은 시뮬레이션용이며 접촉은 별도 검증 제어기가 필요합니다.

```bash
pal train run --model fr3 --algorithm bc --epochs 64 --output-dir .local/train/fr3-bc --json
pal train run --model fr3 --algorithm bc --epochs 128 --resume-from .local/train/fr3-bc --output-dir .local/train/fr3-bc-resumed --json
pal train export --source .local/train/fr3-bc-resumed --destination .local/fr3-training.json --json
# 이 파일만 다른 호스트로 옮긴 뒤:
pal train import --source .local/fr3-training.json --destination .local/imported-fr3 --json
```

`--algorithm ppo`는 실제 팔 rollout을 사용합니다. 업데이트/에포크 경계마다 모델·optimizer·고정 정규화·RNG·진도를 원자적으로 저장합니다. SIGINT/SIGTERM은 다음 경계에서 중단합니다. 강제 종료 후 디렉터리 재개는 마지막 정상 체크포인트를 찾습니다. 코드·모델·데이터·엔진·환경 lock·seed·학습률이 바뀌면 재개를 거부하며 총 에포크 증가는 허용합니다. export는 해시가 있는 학습 상태·시연 데이터만 포함하고 장비 설정·자격증명·실물 승인·개인 진도는 포함하지 않습니다. 대상 호스트도 같은 소스와 소프트웨어 lock을 사용해야 합니다.

BC는 에피소드 단위로 20/5/5를 학습/검증/평가로 분리합니다. 별도 목표 20개에서 16개 이상이 10 mm 이내를 연속 10 제어 단계 유지해야 성능 게이트를 통과합니다. optimizer 검사가 통과해도 `evaluation.json`을 확인하세요. 짧은 BC/PPO는 이 게이트에 실패할 수 있습니다. 실물 허용 오차로 사용하지 않습니다.

## 모델·그리퍼·실물 게이트

FR3의 기존 pin은 유지합니다. Shadow Hand·Stretch 3·Robotiq 2F-85는 별도 Menagerie 커밋·파일 해시·모델 라이선스로 고정합니다. Isaac은 고정 소스를 실행 폴더의 USD로 변환하고 PhysX를 사용합니다. 관절·구동기·연동·자유 베이스·접촉·관측·렌더링을 실제 GPU에서 검증해야 합니다. 연동 관계가 확인되지 않으면 차단합니다. MuJoCo 계산으로 PhysX 검증을 대체하지 않습니다.

그리퍼 시뮬레이션 기준은 Robotiq 2F-85입니다. [제조사 Isaac 자산](https://github.com/robotiq/isaacsim_assets)은 별도 manifest에 고정합니다. PhysX variant를 사용하며 Newton/MuJoCo-Warp를 두 엔진 비교로 쓰지 않습니다. 교체 제품은 재사용 라이선스, 충돌·관성, mimic·폐루프·개폐 폭 변환, 상태·timeout·정지 API, 플랜지·전원·통신·하중 호환성을 확인해야 합니다. 공개 `Gripper` protocol로 인터페이스를 분리하며 구매는 포함하지 않습니다.

Enlight 실물 기준은 RDK 2.1 / v3E.1입니다. description의 v4 표기와 실물 호환성은 미확인 게이트입니다. Elements 검토 → 오프라인 재생 → sink → 읽기 전용 → live shadow → torque-disabled replay → 정확한 일회성 실행 카드 순으로 진행합니다. 일반 수업은 실물 명령을 보내지 않습니다. run-card executor에는 제조사 연결·enable API가 없으며 현장 어댑터에서 watchdog·timeout·정지·장비 식별·한계·툴 하중을 검증해야 합니다. 프로브·그리퍼가 없거나 검토되지 않으면 해당 실습은 대기합니다. [안전 지침](../07_SAFETY.md)을 따릅니다.

설치된 Isaac 호스트에서는 `pal train run --engine physx --model fr3 --algorithm bc --epochs 64 --output-dir .local/train/physx-fr3 --json`을 사용합니다. 동일 엔진에서만 체크포인트를 재개합니다. [환경별 검증 결과](../verification/robot-paths-2026-11-08.md)를 확인하세요.

## 질문을 교재 개선으로 연결

```text
[개선점] 그래프의 축과 단위를 더 쉽게 설명해줘.
```

에이전트가 질문 원문·현재 수업·실제 관측값을 저장하고 원인·교재 보완·재검증을 연결합니다. 지금 수정하려면 다음과 같이 요청합니다.

```text
[개선점] 지금 바로 고쳐줘. 그래프 단위 설명이 빠져 있어.
```

<details markdown="1">
<summary>직접 피드백을 조회·기록하는 명령</summary>

```bash
pal feedback add '질문 원문; 단계: Observe; 값: 실제 관측값; 기대와 다른 점' --lesson core-fr3-02 --json
```

수정 후 `pal feedback resolve ID --evidence '답변·원인; 교재 누락; 수정 파일; 재검증 결과; 다음 시작점'`으로 연결합니다. 일반화된 설명은 교재에 반영하고 개인 실행 자료는 `.local`에 둡니다. 개발자는 `PAL_LOCAL_DIR`로 별도 세션을 선택하며 사용자 완료 기록을 대신 만들지 않습니다.

수식 표기는 [GitHub 수식 문법](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions), Mac 재생 경로는 [MuJoCo passive viewer](https://mujoco.readthedocs.io/en/stable/python.html#passive-viewer)를 따릅니다.

</details>

### 공개 교재 피드백

한국어 HTML 교재의 페이지 하단에서 ‘튜토리얼 의견 보내기’를 눌러 양식을 펼치면 GitHub 로그인 없이 개선점을 보낼 수 있습니다. Codex나 Claude Code에 아래처럼 요청해도 공개 GitHub 이슈로 등록할 수 있습니다.

```text
이 피드백을 만든 사람에게 알려줘.
core-01에서 각도 그래프의 0 rad가 어떤 자세인지 그림 옆에도 표시하면 좋겠어.
공개해도 되는 내용으로 terryum/tutorial-robotics에 GitHub 이슈를 등록하고 링크를 알려줘.
```

Codex에서 GitHub에 연결할 수 없으면 [GitHub에서 직접 이슈를 작성](https://github.com/terryum/tutorial-robotics/issues/new)할 수 있습니다.
