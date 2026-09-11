# GitHub에서 읽고 직접 실행하기

이 문서는 현재 실행 안내입니다. 날짜가 붙은 호스트 설치 보고서는 당시 환경의 기록이며 현재 실행 성공을 보장하지 않습니다. 수업의 Action은 계산하고 종료합니다. GUI 재생은 별도 명령입니다.

## 처음 준비 — Mac Terminal, zsh

Git은 고정 소스 버전을 받고, Python은 실험을 실행하며, uv는 잠긴 의존성을 `.venv`에 설치합니다. MuJoCo는 동역학과 렌더링, NumPy는 수치 계산을 담당합니다. GUI용 프로그램을 따로 설치할 필요는 없습니다.

저장소를 처음 받았다면 아래 폴더로 이동합니다. 다른 곳에 복제했다면 첫 경로를 바꿉니다. 이 안내의 상대 경로는 모두 저장소 루트 기준입니다.

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

```bash
pal course init --json
```

```bash
pal course next --json
```

선수 조건을 충족하는 수업을 하나 선택합니다. 기존 completed 기록은 init으로 지워지지 않습니다.

## 새 터미널에서 재개

새 터미널마다 `cd`와 `source .venv/bin/activate`를 다시 실행합니다. 설치를 반복할 필요는 없습니다.

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

## 한 수업의 작업 순서

1. Expected에서 먼저 볼 값과 단위를 읽습니다.
2. Action 명령을 한 줄씩 실행합니다. `executed`는 실험 실행이며 학습 완료가 아닙니다.
3. `lesson inspect`로 artifact 무결성과 수치를 확인합니다. PNG는 Mac `open` 또는 파일 관리자에서 엽니다. CSV는 텍스트 편집기에서도 열립니다.
4. 이론의 예시를 직접 계산하고 코드와 CSV의 같은 시각을 찾습니다.
5. Try it의 한 가지 입력만 바꾸고 `lesson compare`로 비교합니다. 구조·설치 조사 수업은 별도 수치 실험 없이 review할 수 있습니다.
6. 질문을 저장하고 해결 내용을 검증한 뒤 review·finish를 실행합니다. 다음 수업은 여기서 자동으로 시작하지 않습니다.

`baseline-01`이 이미 있으면 `baseline-02`처럼 새 이름을 씁니다. 기존 폴더를 덮어쓰지 않습니다. 실패한 `run.json`도 원인 기록으로 남깁니다. 프로세스가 계속 실행 중이고 중단하려면 Terminal에서 Ctrl-C를 누릅니다.

## 모델 재생과 Mac 조작

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

## 질문을 교재 개선으로 연결

```bash
pal feedback add '질문 원문; 단계: Observe; 값: 실제 관측값; 기대와 다른 점' --lesson core-fr3-02 --json
```

수정 후 `pal feedback resolve ID --evidence '답변·원인; 교재 누락; 수정 파일; 재검증 결과; 다음 시작점'`으로 연결합니다. 일반화된 설명은 교재에 반영하고 개인 실행 자료는 `.local`에 둡니다. 개발자는 `PAL_LOCAL_DIR`로 별도 세션을 선택하며 사용자 완료 기록을 대신 만들지 않습니다.

수식 표기는 [GitHub 수식 문법](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions), Mac 재생 경로는 [MuJoCo passive viewer](https://mujoco.readthedocs.io/en/stable/python.html#passive-viewer)를 따릅니다.
