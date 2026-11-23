<!-- pal:language:start -->
<p align="right">
  <a href="deployment-hardware.md" lang="ko">한국어</a> | <a href="../../en/concepts/deployment-hardware.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 배포와 실물: 단계마다 근거와 권한이 달라진다

## 정책 파일은 계약의 일부다

정책 배포는 숫자의 뜻을 보존하는 일이다. 모델 식별, 관측 순서, 스케일, 행동 단위, 좌표계, 시간, 의존성 버전, 롤백 동작이 필요하다. 계약 없이 숫자 7개의 출력은 모호하다. 두 팔 모두 7관절이라고 FR3 관절 벡터가 Enlight 벡터가 되지는 않는다.

[후보 패키징](../lessons/sim-deploy-01.md)은 학습 정책 바이트와 결정론적 테스트 벡터를 기록한다. [오프라인 런타임과 sink](../lessons/hw-common-01.md)는 명령을 내보내지 않고 추론을 반복한다. 이는 휴대형 환경에서 가능한 소프트웨어 활동이다. 이후의 [읽기 전용 게이트](../lessons/hw-common-02.md)와 [Enlight 프로브 준비](../lessons/hw-enlight-05.md)는 독립 실물 근거가 필요하며, 근거가 없으면 scaffolded 상태를 유지한다.

휴대형 후보에서 $o$는 고정 스케일을 적용한 17원소 관측, $\tilde o=[\operatorname{clip}(o,-5,5),1]$는 편향을 추가한 18원소 특성, $W$는 18×7 가중치다. 추론은 다음과 같다.

$$
a=\tanh(\tilde oW),\qquad \Delta q=0.03a.
$$

$a$는 제한된 무차원 값이며 시뮬레이터는 $\Delta q$를 rad로 해석한다. 위치 변화량이 제한되었다고 속도·토크·접촉력이 모두 제한되지는 않는다. 매니페스트의 `rate_hz=50`은 계약을 설명한다. 오프라인 테스트 벡터 반복은 실시간 스케줄링 시험이 아니다.

**로봇 측정이나 명령이 아닌 계산 예제**: 변환 전 값이 0.5이면 $a=0.462117$, $\Delta q\approx0.0138635$ rad이다.

```python
import numpy as np
pre_transform = np.array([0.5])
normalized_delta = np.tanh(pre_transform)
sim_delta_rad = 0.03 * normalized_delta
assert np.allclose(sim_delta_rad, [0.013863514717800292])
```

## 휴대형 소프트웨어 근거를 따라 읽기

[deployment.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/deployment.py)는 `sample_candidate/manifest.json`을 만든다. `policy.sha256`, `files`, `test_vectors`, `observation_order`, `action_order`, `frame`, `units`, `normalization`, `rollback`, `promotion`, `performance_verified`를 읽는다. 과정의 후보는 `candidate-only`이며 이 패키징 경로는 `performance_verified=False`, 롤백은 `command-sink`로 명시한다. 실물로 승격하는 과정이 아니다.

`validate_candidate`는 해시, 경로 포함 관계, 수치 테스트 벡터 일치를 검사한다. 바이트 재현성과 인터페이스 동작을 검증하지만 신뢰할 출처나 과제 안전을 증명하지는 않는다. sink 수업은 `inference.json`을 저장하며 payload에 `emitted_command_count=0`, `inference_count`, `replay_exact`, 매니페스트 해시를 기록한다. 의도적으로 publisher·소켓·벤더 SDK·실행 콜백이 없다. 테스트 벡터 관측 하나를 바꾸는 사고 비교에서는 추론이 달라질 수 있다. 기존 `variant`를 바꾸어도 없는 전송 경로가 생기지 않는다.

## 실물 준비는 별도의 단계다

실물 작업 전에 [안전 계약](../../07_SAFETY.md)을 읽는다.

```text
오프라인 재생 → 명령 sink → 읽기 전용 → 실시간 shadow
→ 토크 비활성 재생 → 새 정확한 행동 카드 → 승인된 행동 한 번
```

각 단계에서 정확한 모델·장치 식별, 비활성·오류·E-stop 상태, 관절·좌표 의미, 한도, watchdog, timeout, 오래된 상태 거부, 도구·페이로드, 격리 네트워크를 확인한다. 실시간 shadow는 관찰하고 계산할 수 있지만 구동을 허가하지 않는다. 시뮬레이션 배지는 이 사실들을 대신하지 못한다.

[run_card.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/run_card.py)는 **별도 검증된 주입형 전송체**의 정확한 행동을 게이트한다. 벤더 연결·토크 활성·제어기 API는 제공하지 않는다. 구현된 카드는 Enlight의 작은 관절 이동 한 번을 지원한다. 유한한 rad 목표 7개, arm 그룹, 변화량 최대 0.02 rad, timeout 최대 1 s, 유효기간 최대 60 s, 정확한 승인, 일회 소비가 필요하다. 이는 이 소프트웨어 게이트의 제약이며 보편적인 안전 운동 한도가 아니다. 최신 일치 preflight, 호환성·도구 검토, 시험된 stop 경로가 필수다. 전송 전에 승인이 소비되므로 불확실하거나 실패한 호출은 자동 재시도 대신 상태를 확인해야 한다.

## 실행을 가장하지 않는 접촉 준비

프로브 평면 힘 제어 준비에는 검토된 TCP 변환, 보정된 평면 법선, 페이로드, 별도 검증된 힘 제어기가 필요하다. 좌표 오차는 원하는 힘의 방향을 바꾼다. 도구 좌표를 월드로 바꾸는 회전이 $R$이면 $f_{world}=Rf_{tool}$이며 두 벡터는 N 단위의 3원소다. 종이 위에서 각도 하나를 바꾸며 방향을 계산할 수 있지만 표면 접촉의 허가는 아니다. 그리퍼에는 장착·폭 변환·상태·timeout·stop·하중 검토도 필요하다. description v4와 Enlight RDK 2.1/v3E.1의 호환성은 실물 근거로 해소하기 전까지 미검증이다.

## 이해 확인

1. 정확한 해시는 무엇을 증명하는가? 바이트가 예상 다이제스트와 같다는 뜻이며 안전한 제어기라는 뜻은 아니다.
2. 명령 0개는 실물 준비를 뜻하는가? sink의 소프트웨어 경계만 보여준다.
3. 종이 계산 뒤 scaffolded 수업을 완료해도 되는가? 안 된다. 준비와 없는 근거를 기록하고 차단 상태를 유지한다.

선택형 [XR·장갑·트래커·UMI 수집](../equipment-stages.md)은 실물 로봇 권한 이전 단계다. 원격조작 모듈의 `CommandSink`와 배포 수업의 추론 sink는 별도 구현이며 둘 다 실물 publisher를 두지 않는다. teleop 게이트는 입력이 정확히 100 ms 오래되면 래치되고, 새 release·로컬 rearm·새 press를 요구한다. 합성 watchdog 테스트는 실물 stop 경로 검증이 아니다.
