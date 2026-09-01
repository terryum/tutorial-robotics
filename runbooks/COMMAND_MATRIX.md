# Commands by Machine

## MacBook — first

```text
이 컴퓨터는 MACBOOK이다. MACHINE_SEQUENCE.md, references/00_USER_BASELINE_2026-08-31.md, docs/11_SOURCE_CURRICULUM_ALIGNMENT.md, runbooks/MACBOOK.md를 읽고 $bootstrap-machine으로 MACBOOK_FOUNDATION을 등록해줘. T00 하나만 실행하고 코드·test·시각화·한국어 report·state까지 완료한 뒤 멈춰줘.
```

## MacBook — repeat

```text
현재 profile은 MACBOOK_FOUNDATION이다. 사용자 baseline에 대응되는 다음 eligible tutorial 하나만 실행해줘. 다른 host 단계는 pending-host로 두고 완료 후 멈춰줘.
```

## WS2 — first/repeat

```text
이 컴퓨터는 WS2다. MACHINE_SEQUENCE.md, 사용자 baseline, runbooks/WS2_SIM_TRAIN.md를 읽고 WS2_SIM_TRAIN을 등록해줘. Mac handoff를 검증하고 다음 eligible WS2 tutorial 하나만 실행해. 실물 command는 금지해.
```

## WS2 → robot integration

```text
WS2_ROBOT_INTEGRATION 전환 audit을 실행해. training/Isaac job 종료, robot-runtime environment와 NIC 분리를 검증하고 T35B offline/no-motion shadow까지만 수행해. 움직이지 마.
```


```text
 pre-motion dry-run과 run card까지만 실행해.
 system-identification 계획과 각 excitation별 run card를 만들되 승인 전 움직이지 마.
는 offline/shadow까지만 실행하고 contact는 별도 승인으로 남겨.
```

## Wuji

```text
T36 --robot wuji_hand2_beta2_right read-only만 실행해.
T38 tactile baseline과 named-pose dry-run까지만 실행해.
T42B는 offline/shadow까지만 실행하고 grasp/contact는 별도 승인으로 남겨.
```


```text
이 컴퓨터는 WS1이다. WS1_ROBOT_RUNTIME을 등록하고 bundle/hash를 검증해 T35B offline/no-motion shadow까지만 수행해.
 subsystem dry-run과 run card까지만 실행해.
 carton task는 shadow까지만 실행하고 실제 한 episode는 별도 승인으로 남겨.
```
