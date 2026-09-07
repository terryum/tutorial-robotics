# Runbook — WS1 Shared Robot Runtime

## 역할


WS1은 연구용 대규모 training 장비가 아니다. package와 driver는 pin하고, WS2에서 넘어온 bundle을 target runtime에서 재검증한다.

## 최초 Codex 명령

```text
이 컴퓨터는 WS1 Ubuntu이며 ROBOT_RUNTIME mode다. git pull 이후 EXECUTION_MODEL.md, AGENTS.md, state/HOST_STATUS.md와 state/PROGRESS.md를 읽고 $bootstrap-host로 실제 capability를 등록해줘. candidate bundle manifest/hash를 확인하고 이 target runtime에서 dependencies를 재구축한 뒤 T35B offline replay와 no-motion shadow dry-run까지만 실행해. 결과를 push할 때 WS1_UBUNTU 행을 non-secret summary로 갱신하고 retraining과 실제 motion command는 실행하지 마.
```

## T36 read-only

```text
$hardware-gate를 사용해 `pal tutorial run T36 --robot <robot-id>`에 해당하는 read-only integration만 실행해줘. 실제 로봇을 움직이지 말고 serial/revision/firmware, joint/order/unit, timestamp/rate, safety/E-stop, command watchdog의 읽기 경로를 검증해. simulation registry와 차이를 보고하고 완료 후 멈춰줘.
```

## robot별 저위험 검증


```text
로 fake/real schema와 단일 free-space motion을 검증한 뒤, 별도 run card로  system identification을 수행해. 제조 task는  bundle을 받아 에서 shadow→free-space→separate contact approval 순서로 평가해.
```

### Wuji

```text
T38로 Beta 2 hardware/tactile calibration과 named pose를 검증한다. 제조 dexterity task는 T42A bundle을 받아 T42B에서 shadow→named pose→separate contact/grasp approval 순서로 평가해.
```


```text
와 T38이 각각 완료된 경우에만 를 실행해. adapter/TCP/payload/inertia와 arm-hand-tactile timestamp를 먼저 검증하고, arm motion·hand motion·contact task는 각각 별도 승인으로 분리해줘.
```


```text
을 실행하되 full-body 동시 구동을 금지해. read-only inventory → command dry-run → base 또는 한 팔의 단일 저속 subsystem test 순서를 지키고, 양팔은 별도 승인으로 남겨줘.
```

## capstone 배포

```text
에서 생성된 candidate bundle을 검증하고 를 실행해줘. offline replay → read-only → live no-command shadow → torque-off replay → gated low-speed → 승인된 carton task 순서를 지키고, 성공률·cycle time·retry·failure gallery·stop event를 기록해. automatic promotion to production은 금지하고 결과만 보고해줘.
```

## WS2로 되돌릴 데이터

- raw/corrected episode manifest
- calibration version
- failure clips and labels
- latency/timestamp report
- task outcome and retry
- safety/stop events
- exact deployed bundle hash

실물 데이터를 WS1에서 직접 재학습하지 않고 WS2로 전달한다.
