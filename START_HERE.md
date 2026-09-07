# Start Here — Any Development Host

## 1. 필수 machine 순서는 없다

이 저장소는 MacBook에서 먼저 끝내고 WS2로 넘기는 구조가 아니다.

```text
현재 Git progress
+ 현재 host capabilities
→ 실행 가능한 다음 tutorial
```

WS2는 core와 GPU tutorial을 모두 실행할 수 있고, MacBook은 이동 중 지원 가능한 항목을 이어서 실행한다.

## 2. 저장소를 처음 열었을 때

1. GitHub repository를 clone하거나 기존 checkout에서 `git pull --rebase`한다.
2. `EXECUTION_MODEL.md`, `AGENTS.md`, `state/HOST_STATUS.md`,
   `state/PROGRESS.md`, `tutorials/INDEX.md`를 읽힌다.
3. Git을 pull한 뒤 `state/HOST_STATUS.md`에서 이 host의 마지막 보고와 다른
   host의 최신 handoff를 확인한다.
4. `$bootstrap-host`로 OS/architecture/GPU/ROS/Isaac capability를 기록한다.
5. T00 또는 shared progress상 다음 eligible tutorial 하나를 실행한다.

## 3. WS2에서 처음부터 시작하는 명령

```text
이 컴퓨터는 WS2이며 DEVELOPMENT mode다. EXECUTION_MODEL.md, AGENTS.md, references/00_USER_BASELINE_2026-08-31.md, runbooks/FULL_GPU_DEVELOPMENT.md를 읽고 $bootstrap-host로 capability를 등록해줘. WS2는 portable/core curriculum과 CUDA/Isaac 확장을 모두 수행하는 superset host다. T00 하나만 구현·test·실행·시각화·한국어 report·state 갱신까지 완료하고 멈춰줘.
```

## 4. MacBook에서 처음 또는 이어서 시작하는 명령

```text
이 컴퓨터는 MacBook이며 DEVELOPMENT mode다. 먼저 git status와 shared progress를 확인하고 $bootstrap-host로 capability를 등록해줘. GPU 전용 tutorial을 shared status에서 변경하지 말고, 현재 capability로 실행 가능한 다음 eligible tutorial 하나만 구현·test·실행·시각화·한국어 report·state 갱신까지 완료하고 멈춰줘.
```

## 5. host를 바꿀 때

이전 host:

```text
현재 tutorial의 acceptance를 audit하고 source·test·small output·report·shared state와 state/HOST_STATUS.md의 현재 host 행을 함께 갱신해줘. 큰 artifact는 manifest/hash만 commit 대상으로 두고, 정확한 git status/add/commit/push 명령을 제시해줘. 내가 push까지 요청한 경우에만 같은 범위의 commit을 push해.
```

새 host:

```text
git pull 이후 state/HOST_STATUS.md와 state/PROGRESS.md를 먼저 읽고 이 checkout을 계속 사용한다. local virtual environment를 다른 host에서 복사하지 말고, committed lock/source pins로 필요한 environment와 model asset을 재구성해. shared progress는 유지하고 현재 capability로 실행 가능한 다음 tutorial 하나를 알려줘.
```

## 6. 완료된 tutorial을 다른 host에서 다시 확인

```text
T24는 shared progress상 done을 유지해. 이 host에서 portability verification으로 기존 코드를 재실행하고, 기존 canonical result를 덮어쓰지 말며 host-specific output/report만 추가해줘.
```

## 7. 실물 로봇

실물 연결 시에만 `ROBOT_RUNTIME` mode로 전환한다. 같은 host에서 실행한다면 모든 training/Isaac batch를 먼저 종료한다. 비공개 로봇의 배치 규칙은 private overlay에서만 정의하며, 모든 실물 배치는 capability와 안전 조건을 충족해야 한다.
