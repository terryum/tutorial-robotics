<a id="start-here"></a>

# Start here / 여기서 시작

Codex 또는 Claude Code에 아래 요청을 붙여 넣어 시작합니다. 준비와 첫 수업 시작은 두 단계입니다. Use Codex or Claude Code; preparation and the first lesson start are separate steps.

## 한국어로 시작

**Codex 또는 Claude Code로 시작하는 것을 권장합니다.** 아래 한 문장을 대화창에 붙여 넣으세요. 터미널 명령을 먼저 외울 필요는 없습니다.

```text
https://github.com/terryum/tutorial-robotics 이 레포를 받아서 설치해주고 튜토리얼을 시작해줘
```

에이전트는 기존 체크아웃이 있으면 재사용하고, 없으면 저장소를 받습니다. 저장소 지침을 읽고 실제 OS·환경을 확인한 뒤 최소 Core 설치 계획을 보여 주고 필요한 준비만 적용·검증합니다. 기존 `.venv`, 잠금 파일과 `.local/` 진도를 보존합니다. 현재 호스트에서 준비 검증을 통과한 기존 환경은 재설치하지 않습니다. 지원하지 않는 환경이나 설치 실패는 차단 사유와 다음 행동을 설명하며 준비 완료로 표시하지 않습니다.

완료했거나 진행 중인 학습 수업이 없으면 에이전트는 준비 검증을 마치고 다음 안내를 한 뒤 **사용자의 응답을 기다립니다**. 환경 진단만 마친 경우에도 첫 진자 수업부터 시작합니다. 저장한 학습 상태가 있으면 에이전트가 마지막 수업과 단계를 알려 주고 이어갈지 묻습니다.

> 첫번째 튜토리얼을 띄울 준비가 되었습니다. 시작하시겠습니까?

이때 첫 수업 실행이나 수업 탭 열기는 아직 시작하지 않습니다. 시작할 준비가 되면 답하세요.

```text
네, 첫번째 튜토리얼을 시작해줘.
```

시작하겠다고 답하면 에이전트가 선택한 언어로 첫 수업 [진자 실험](docs/ko/lessons/core-01.md)을 엽니다. 학습자가 움직임을 예측하면 에이전트는 시작 각도만 바꿔 두 번 실행하고, 두 진자의 재생 화면과 각도 그래프를 별도 결과 창에 띄웁니다. 별도 창을 열 수 없으면 결과 탭을 쓰고, 화면을 제어할 수 없으면 지원되는 이미지와 측정값을 대화에 표시합니다. 에이전트는 이해 확인 질문에서 멈춥니다. 답을 함께 확인하거나 학습자가 완료를 요청하면 진도를 기록합니다.

환경 점검은 설치 중에 마칩니다. 나중에 점검만 필요하면 [환경 진단 `core-00` (`T00`)](docs/ko/lessons/core-00.md)을 직접 실행할 수 있습니다.

처음부터 특정 수업의 실행을 명시적으로 요청했다면 그 요청은 준비 후 해당 수업을 진행할 수 있는 별도 지시입니다. 일반적인 위 설치·시작 요청은 준비 후 시작 여부를 묻는 두 단계 흐름입니다.

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

[한국어 실행 안내](docs/ko/READER_GUIDE.md)는 대화 진행·재개와 필요할 때 펼쳐 보는 터미널 참고를 제공합니다.

## Start in English

**We recommend Codex or Claude Code.** Paste this sentence into the conversation; you do not need to learn terminal commands first.

```text
https://github.com/terryum/tutorial-robotics Clone this repository, install it, and help me start the tutorial.
```

The agent reuses an existing checkout or clones the repository when needed. It reads the repository instructions, checks the actual OS/environment, shows the smallest Core setup plan, and applies/verifies only the needed preparation. It preserves `.venv`, the lockfile and `.local/` progress. An existing environment that passes readiness verification on this host is reused without reinstalling. Unsupported environments or failed setup remain blocked with a concrete next action rather than a readiness claim.

After verifying readiness, the agent gives the following invitation and **waits for your reply** if you have no completed or active learning lessons. If you have only run the host diagnostic, start with the pendulum. With saved learning progress, the agent identifies the last lesson and phase and offers to resume.

> The first tutorial is ready to open. Would you like to start?

The first lesson and its browser tab have not started yet. When ready, reply:

```text
Yes, start the first tutorial.
```

When you reply to start, the agent opens the [first pendulum experiment](docs/en/lessons/core-01.md) in your selected language. After you predict the motion, it runs the experiment twice, changing only the release angle, and opens a separate results window with synchronized replay and an angle graph. If a separate window is unavailable, it uses a results tab. Without screen control, it shares supported images and measurements in chat. The agent stops at a comprehension question and records progress after confirming your answer or receiving your request to finish.

Setup includes host checks. You can run the [on-demand host diagnostic `core-00` (`T00`)](docs/en/lessons/core-00.md) whenever you need it.

An explicit request to run a particular lesson is separate authorization to proceed after readiness. The general install/start request above follows the two-step preparation and start invitation.

### Next lesson

```text
Run the next eligible lesson only.
```

### Resume in a new chat

```text
https://github.com/terryum/tutorial-robotics I cleared the previous chat. Continue in the same existing checkout. Reread the repository instructions, curriculum/catalog.json and agent/workflow.md, then inspect .local/progress.json, .local/session.json, feedback and existing run evidence. Resume the last interrupted phase for one lesson without reinstalling, recloning or resetting progress.
```

### Rerun this lesson

```text
Rerun the current lesson. Preserve existing evidence and use a fresh run directory.
```

### Check progress

```text
Show my progress: completed lessons, current phase, remaining prerequisites and the next action.
```

### Pause

```text
Pause here and save the current lesson, explanation/comparison phase, run paths and next starting point.
```

### Questions and feedback

```text
[개선점] Explain the graph axes and units more simply.
```

The [English reader guide](docs/en/READER_GUIDE.md) covers prompt-led learning, resume and optional terminal references.

## Optional manual and development routes

<details>
<summary>Direct terminal reference</summary>

Choose a scope, not a machine sequence.

```bash
pal host detect --json
pal setup plan --profile core --out .local/setup-plan.json --json
pal setup verify --profile core --json
pal course runnable --without-hardware --json
pal course init --through core --json
pal course next --json
```

Read the [English](docs/en/index.md) or [한국어](docs/ko/index.md) page for the returned lesson. Run its check, execute it headlessly, and inspect `summary.json`, `trace.csv`, and `lesson-report.md`.

For Simulation, initialize `--through sim` on Ubuntu and install only the capabilities needed by the selected track. For Hardware, select one or more `--robot` values, complete the common runtime lessons, and stop at read-only preflight until a fresh motion approval exists.

</details>

For the WS2 development handoff, say **“튜토리얼 업데이트 해줘”**. Follow the [WS2 update runbook](setup/WS2_TUTORIAL_UPDATE.md) for repository sync, real Isaac/PhysX verification, fixes and publication. This is separate from ordinary learner progress and hardware operation. An existing clone must first receive these instructions through its normal repository update.
