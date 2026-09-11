> Current execution authority: [common workflow](../agent/workflow.md). Learner state is ignored `.local/`; historical host reports below never complete lessons or require automatic commits.

# Runbook — WS2 Robot Integration Mode

## 목적


## 강제 조건

- `CANDIDATE_DEPLOYMENT_BUNDLE_READY` gate for the selected robot/task
- 모든 GPU training/Isaac batch job 종료
- `ws2-robot-runtime` 환경만 활성화
- robot 전용 유선 NIC
- 인터넷/default route와 robot subnet 충돌 없음
- hardware-gate
- 한 번에 한 로봇

## profile 전환 명령

```text
이 컴퓨터는 WS2 Ubuntu이며 지금부터 ROBOT_RUNTIME mode로만 사용한다. git pull 이후 state/HOST_STATUS.md와 .local/progress.json, runbooks/WS2_ROBOT_INTEGRATION.md와 docs/07_SAFETY.md를 읽고 실행 중인 training/Isaac process를 audit해 종료 여부를 확인해. ignored `.local/` state를 전환하고 T35B의 offline replay와 no-motion shadow dry-run만 실행해줘. 결과를 push할 때 WS2_UBUNTU 행을 갱신하고 실제 로봇 motion command는 실행하지 마.
```

## read-only 명령

```text
```

## 저위험 motion 명령

```text
$hardware-gate를 사용해 <|T38|>의 승인 전 checklist와 dry-run을 먼저 완료해줘. 실제 motion은 내가 이 실행에서 명시적으로 승인한 단일 저속 동작만 허용하고, workspace·speed·force/current limit·watchdog·stop path를 run card에 고정해. 승인 범위를 넘어가지 말고 완료 후 멈춰줘.
```

## 권장 robot 배치

- Wuji: `hw-common-02` → `hw-wuji-01` → `hw-wuji-02`
- Enlight: `hw-common-02` → `hw-enlight-01` and only then its selected follow-up
- FR3: `hw-common-02` → `hw-fr3-01`

## SIM_TRAIN 복귀

```text
로봇 연결을 종료하고 WS2_SIM_TRAIN profile로 복귀하기 위한 shutdown audit을 실행해줘. torque/control disable, driver 종료, robot NIC 상태, 기록 파일 flush와 hash, runtime environment deactivate를 검증해. 실제 장치가 안전 상태임을 확인한 뒤에만 profile을 바꾸고, training을 자동 시작하지는 마.
```
