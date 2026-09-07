# Runbook — MacBook Foundation

## 역할

MacBook은 학습과 운영의 cockpit이다. MuJoCo, robotics math/control, ROS 2 concepts, small PPO/BC/ACT, offline hand retargeting and VLA protocol/small smoke를 담당한다. Isaac Sim 본체와 실물 low-level runtime은 설치하지 않는다.

## 최초 명령

```text
이 컴퓨터는 MACBOOK이며 DEVELOPMENT mode다. git pull 이후 EXECUTION_MODEL.md, AGENTS.md, state/HOST_STATUS.md와 state/PROGRESS.md를 읽고 $bootstrap-host로 실제 capability를 등록해줘. 현재 capability로 실행 가능한 tutorial 하나만 test/output/report/state까지 완료하고, 결과를 push할 때 MACBOOK 행도 같은 commit에서 갱신해줘.
```

## 반복 명령

```text
현재 profile은 MACBOOK_FOUNDATION이다. source-alignment에 맞는 다음 eligible tutorial 하나만 실행해줘. 코드를 직접 실행하고 시각화와 한국어 설명을 남긴 뒤 멈춰줘.
```

## Canonical sequence

```text
T00 T01 T02 T03 T04
T05 T06 T07 T08  T09 T10 
  
T14 T15 T16
T17 T19 T20 T21
T22 T23 T24 T25
T28 T29 T30  T16A T32A
```

## Learning boundaries

- local: all model loading/inspection possible on macOS, small deterministic simulation, FK/IK/control, small learning jobs
- remote only: Isaac, thousands of environments, full G1/Wuji PPO, ACT/VLA scale-up
- real robot: no vendor driver or motion command
- RViz is optional; MuJoCo/offscreen and numeric TF verification are mandatory fallbacks

## Phase completion

```text
MacBook phase를 baseline mapping과 acceptance 기준으로 audit하고 MACBOOK_FOUNDATION_COMPLETE와 WS2_HANDOFF.md를 만들어줘. Git commands만 제시하고 자동 push하지 마.
```
