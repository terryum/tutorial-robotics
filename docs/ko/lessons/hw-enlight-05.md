<!-- pal:language:start -->
<p align="right">
  <a href="hw-enlight-05.md" lang="ko">한국어</a> | <a href="../../en/lessons/hw-enlight-05.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# hw-enlight-05 — Enlight 프로브 평면 힘 제어 준비

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `hardware / enlight` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight` |
| Prerequisites | `hw-enlight-04` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

[배포·실물 검증 개념](../concepts/deployment-hardware.md)과 [안전 규칙](../../07_SAFETY.md)을 읽습니다. 질문은 “평면에 가하는 힘의 방향·크기를 믿으려면 무엇이 먼저 확인되어야 하는가?”입니다. 이 단계는 `scaffolded`이며 장비·툴·힘 제어기의 증거가 없습니다.

[제어·접촉 개념](../concepts/control-contact.md)에서 접촉력과 좌표 변환의 선행 지식을 함께 확인합니다.

## Learning goals

프로브의 툴 좌표계·하중·허용력·평면 보정을 검토해야 합니다. 학습 정책 토크를 실물에 직접 보내지 않습니다. 검증한 별도 힘 제어기가 필요합니다.

## Preflight

선행 수업은 `hw-enlight-04`입니다. 읽기 전용으로 `pal course next --json`을 확인하고, 장비 식별·비활성/오류/E-stop·관절/힘 한계·타임아웃·상태 시각·stop 경로·격리 네트워크의 검증 기록을 검토합니다. 실제 장비 기록과 승인·보정값은 ignored `.local/`에만 보관합니다.

Enlight의 RDK 2.1 / v3E.1 기준과 공개 description v4의 호환성은 별도 검토 항목입니다. 프로브가 있다고 추정하지 말고 툴 장착·TCP·하중·힘 측정·평면 보정이 각각 검증되었는지 확인합니다. 이름이 WS1/WS2인 호스트도 이 증거를 대체하지 않습니다.

## Action

### 준비 기록만 읽기

장비 모델·프로브 TCP/질량/무게중심·작업 평면 좌표계·센서 영점/하중 보상·힘 제한·검증한 힘 제어기·timeout/stop 증거의 확인 여부를 기록합니다. 누락 항목은 미확인으로 둡니다.

현재 `pal lesson run hw-enlight-05`는 `NotImplementedError`의 `reader_test_required`로 거부됩니다. 정상 측정 run이나 run_dir가 생긴다고 기대하지 않습니다. 이 준비 수업을 위해 실행 명령·토크·힘 목표를 장비에 보내지 않습니다. 실물 접촉은 이 문서 밖의 검증된 실행 경로와 해당 실행에 대한 새로운 정확한 승인까지 필요합니다.

## Expected

정상적인 결과는 “준비 검토 중, 실물 증거 없음, 완료 차단”입니다. `summary.json`, `trace.csv`, 힘 응답 그래프를 실제 측정처럼 만들지 않습니다. 카탈로그의 `scaffolded`와 `reader_test_required`를 유지합니다.

### 어떤 증거를 관찰할 것인가

준비 표에는 각 항목의 근거 위치와 `confirmed`/`unverified`를 적습니다. 센서 힘과 평면 법선을 같은 좌표계로 표현하고 힘의 단위는 N, 단위 법선은 무차원임을 명시합니다. tool/payload 보정과 신선한 상태 시각을 함께 확인합니다. 이 목록은 실물 동작의 자동 허가가 아닙니다. 공개 [검증 기록](../../verification/robot-paths-2026-11-08.md)도 실제 Enlight·프로브 실행은 미검증으로 남겨 둡니다.

## How it works

### 힘과 평면을 같은 좌표계로 읽기

다음은 준비를 위한 기하 설명이며 구현된 힘 제어 법칙이 아닙니다. 세계 좌표계 W에서 평면 위 한 점을 $p_0\in\mathbb R^3$ (m), 프로브 끝 위치를 $p\in\mathbb R^3$ (m), 단위 법선을 $n\in\mathbb R^3$이라고 정합니다. 법선 방향은 문서에서 먼저 정해야 합니다.

$$
d=n^T(p-p_0),\qquad f_W=R_{WT}f_T,\qquad f_n=n^Tf_W.
$$

$d$는 부호 있는 평면 거리(m), $R_{WT}$는 툴 좌표 T의 벡터를 W로 회전시키는 3×3 무차원 행렬, $f_T,f_W$는 같은 힘 벡터의 좌표 표현(N), $f_n$은 법선 방향 힘(N)입니다. 여기서는 힘 벡터만 설명합니다. 센서 전체 wrench의 토크를 다른 기준점으로 옮길 때는 위치 오프셋 항도 필요합니다.

계산 예시(실행 측정값 아님): $n=[0,0,1]^T$, $f_W=[0,0,2]^T$ N이면 $f_n=2$ N입니다. 실제 힘 기록은 센서 부호·영점·툴 중력 보상과 기준점을 먼저 확인해야 이 식과 비교할 수 있습니다. 2 N는 승인한 목표나 허용력이 아닙니다.

### 위치 정책과 힘 제어기의 경계

도달 정책의 관절 목표나 좋은 시뮬레이션 보상은 접촉 중 힘 제한을 보장하지 않습니다. 별도로 검증한 힘/임피던스 제어기, 센서 지연과 포화 처리, 접촉 이탈·충돌·stop 검증이 필요합니다. 여기에 힘 제어 게인을 정하거나 접촉 동작을 수행하는 구현은 없습니다.

## Code connection

[`runner.py`](../../../src/pai_lab/lessons/runner.py)의 `implementation != "implemented"` 검사가 이 수업을 실행 전에 거부합니다. [`run_card.py`](../../../src/pai_lab/hardware/run_card.py)의 `execute`는 검증된 transport를 주입받는 별도 승인 게이트이고 자체 vendor 연결·토크 활성화 API가 없습니다.

현재 게이트가 지원하는 동작은 Enlight `small-joint-move`뿐입니다. 프로브 힘 제어가 구현되어 있거나 그 카드로 접촉을 승인할 수 있다고 해석하지 않습니다. 코드의 60초 이내 카드 수명·일회성 소비·1초 이하 timeout·0.02 rad 이하 증분 검사는 그 제한된 관절 동작의 조건이며 접촉 힘 기준이 아닙니다. 학습 체크포인트 코드는 이 수업의 실제 실행 경로가 아닙니다.

## Try it

### 오프라인 한 변수 계산 비교

위 계산의 법선만 $[0,0,1]^T$에서 $[0,\sin30^\circ,\cos30^\circ]^T$로 기울이고 $f_W=[0,0,2]^T$ N를 유지합니다. 그러면 $f_n=2\cos30^\circ\approx1.732$ N입니다. 힘 자체는 같은데 법선 성분은 달라집니다. 평면 방향 오차가 힘 해석을 바꾸는 이유를 설명하세요.

이는 종이 위 계산입니다. 실제 평면을 기울이거나 로봇을 움직이지 않습니다. `--variant` trial이나 `pal lesson finish`로 준비 검토를 측정·완료 증거로 바꾸지 않습니다.

## Recovery

장비·프로브·보정·제어기·호환성·안전 게이트 중 하나라도 미확인이면 차단 사유와 다음 확인 항목을 남깁니다. 실패·중단 기록을 보존하고 자동 재시도·동작 재개를 하지 않습니다. 실물 경로는 offline replay → command sink → read-only → live shadow → torque-disabled replay → 새 run card → 명시 승인한 한 동작의 순서를 따릅니다. 접촉은 별도의 검증과 새로운 실행 승인이 필요합니다.

## Checkpoint

### 이해 확인

1. 법선 방향이나 힘 좌표계를 잘못 해석하면 어떤 오류가 생기나요?
2. 왜 좋은 도달 정책·작은 관절 이동 승인으로 프로브 접촉까지 허가할 수 없나요?
3. 현재 runner와 run-card 코드가 각각 제공하는 기능과 제공하지 않는 기능은 무엇인가요?

준비 기록에는 확인한 근거, 미확인 툴·보정·호환성, 검증해야 할 제어기와 안전 경로를 적습니다. 실물 증거가 없는 이 단계는 미완료로 유지합니다. 다음 수업 탐색 링크가 있다고 실행 게이트가 충족되는 것은 아닙니다.

답의 기준: 좌표계·법선 부호 오류는 힘 방향과 성분을 왜곡합니다. 도달 성능은 접촉 중 힘 제한을 보장하지 않으며 관절 이동 카드는 접촉 승인이 아닙니다. runner는 이 수업을 차단하고 run-card는 별도로 검증한 transport의 제한된 관절 동작만 게이트합니다. 프로브 힘 제어·장비 증거는 여전히 없습니다.

<!-- pal:navigation:start -->
## Next lesson

[hw-enlight-06](./hw-enlight-06.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
