<!-- pal:language:start -->
<p align="right">
  <a href="vla.md" lang="ko">한국어</a> | <a href="../../en/concepts/vla.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# VLA: 프로토콜, 모델, 런타임

## 세 단어 뒤에는 여러 계약이 있다

VLA 정책은 시각 정보·언어·로봇 상태를 조건으로 행동을 만든다. 이 설명만으로는 카메라 종류·픽셀 전처리·상태 순서·행동 단위·시간 지평·가중치·오래된 관측의 거부 방식을 알 수 없다. 네트워크 응답에 숫자가 있다고 이 질문에 답한 것은 아니다.

[휴대형 프로토콜 수업](../lessons/core-vla-01.md)은 mock이다. [로컬 SmolVLA 미세조정](../lessons/sim-vla-01.md)은 준비된 고정 체크포인트·데이터를 CUDA에서 사용한다. [선택형 원격 추론](../lessons/sim-vla-02.md)은 설정한 전송을 검사한다. 세 주장은 다르며 서로 다른 근거가 필요하다. 어느 경로도 실물 명령을 허가하지 않는다.

정책을 다음처럼 생각할 수 있다.

$$
A=\pi_\theta(I,s,\ell),\qquad A\in\mathbb R^{H\times d_a}.
$$

$I$는 영상, $s$는 상태, $\ell$은 언어 지시, $H$는 행동 지평, $d_a$는 행동 차원이다. 이는 인터페이스 계열을 설명한다. 실제 모델은 영상을 `(batch, channels, height, width)`로 전처리하고 청크 전체 대신 선택한 행동 하나를 노출할 수도 있다. 형태는 의미가 아니다. 출력 7개는 각도·변화량·속도·정규화 제어일 수 있다. 단위와 이름 있는 행동 순서를 별도로 기록해야 한다.

## 휴대형 mock이 가르치는 것

[learning.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/learning.py)는 `instruction`, 0인 관측 7개, fixture 영상 다이제스트, `timestamp_s`, `timeout_s=0.1`을 가진 version-1 요청을 직렬화한다. 다시 읽어 행동 한 행을 반환하며 `mock=True`, `command_sink=True`, 단위 rad를 표시한다. JSON 왕복과 제한된 응답을 검사하지만 비전 인코더를 불러오거나 언어를 이해하거나 학습 VLA 정책을 실행하지 않는다. 이 로컬 fixture의 timeout은 스키마 필드이며 실제 네트워크 timeout 시행의 근거는 아니다.

**모델 결과가 아닌 형태 계산**: 행동 7개의 행 하나는 (1, 7)이다. 0 일곱 개에 0.8을 곱해도 0이므로 mock의 `variant`만 바꾸면 불변이 예상된다.

```python
import json
import numpy as np
request = {"observation": [0.0] * 7}
decoded = json.loads(json.dumps(request))
actions = np.asarray([[0.8 * x for x in decoded["observation"]]])
assert actions.shape == (1, 7)
assert np.array_equal(actions, np.zeros((1, 7)))
```

`experiment.json` → `payload` → `request`, `response`와 `checks`의 `schema_roundtrip`, `bounded_actions`, `sink_only`를 읽는다. 여기서 0인 그래프는 올바른 fixture 동작이며 정책의 실패·성공을 뜻하지 않는다.

## 실제 미세조정과 전송이 추가하는 것

[vla.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/vla.py)는 고정 LeRobot 체크아웃, 기존 로컬 사전학습 체크포인트, `meta/info.json`이 있는 데이터셋을 요구한다. 오프라인 모델 로딩 플래그를 설정하고 데이터별 전후처리기를 만든 뒤 AdamW 갱신을 수행하고 정책과 처리기를 저장한다. 배치 크기는 2이며 행동 시각은 데이터 FPS와 청크 크기에 따른다. 이를 보편적인 카메라 크기나 로봇 행동 차원으로 대체하지 않는다.

손실 trace, `parameter_delta`, 저장한 `policy/`, `training-observation.png`, `server-response.json`은 짧은 학습·재로딩·loopback 추론 동작을 확인한다. 코드는 `performance_verified=False`를 명시한다. 기울기 갱신 몇 회와 유한한 추론은 독립 로봇 과제를 평가하지 않는다. 학습 관측 영상도 전처리에 의존하며 원본 보정 카메라 측정이라고 단정할 수 없다.

원격 추론은 HTTPS 또는 loopback HTTP를 요구한다. 어댑터는 준비 요청의 해시를 만들고 5 s 전송 timeout, 제한된 응답 크기, 설정 행동 차원의 2차원 배열, 유한 값·행동 한도를 검사한다. 제공되면 `model_identity`를 기록한다. 식별 문자열 수신이 배포 가중치의 암호학적 증명은 아니다. 측정 스칼라는 초 단위 왕복 시간이고 그래프 값은 설정 단위의 행동이므로 행동 축을 지연으로 표시하면 안 된다.

## 올바른 계층에서 한 변수를 비교한다

mock에서는 요청·시드를 유지하고 `variant`만 바꾼다. 0 행동은 유지된다. 준비된 로컬 학습의 학습률 배율 비교에서는 체크포인트·데이터·전처리·시드·갱신 예산을 고정한다. 유한 손실과 파라미터 변화를 확인하되 과제 성능 개선을 주장하지 않는다. 원격 응답은 서버가 정한다. 로컬 배율을 사용하지 않으면 불변 출력이 예상되며, 네트워크·서버 변동을 기록하고 결정론적 개선을 만들어내지 않는다.

[공개 검증 보고서](../../verification/reader-experience.md)는 외부 VLA 검사와 휴대형 mock 검증을 구별한다. 가중치·데이터·CUDA가 없으면 명시적으로 준비할 역량이며 mock 출력을 실제 추론으로 바꿔 부를 이유가 아니다.

## 이해 확인

1. JSON 스키마 성공이 언어 이해인가? 아니다. 휴대형 fixture는 VLA 모델을 실행하지 않는다.
2. 처리기를 정책과 함께 저장하는 이유는? 스케일·특성 순서·영상 전처리가 가중치의 뜻을 정하기 때문이다.
3. 유한한 원격 행동을 실물에 바로 보낼 수 있는가? 아니다. [배포와 실물](deployment-hardware.md)의 검토된 전체 계약과 새 실행 권한이 필요하다.

[NVIDIA 생태계 안내](../nvidia-ecosystem.md)는 데이터에서 정책으로 이어지는 질문을 GR00T로 확장한다. 모델 설치·데이터 변환·유한 추론·미세조정·독립 로봇 성능 평가는 별도 이정표이며 SmolVLA나 mock 근거가 GR00T 실행을 대신하지 못한다.
