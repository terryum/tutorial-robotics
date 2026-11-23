<!-- pal:language:start -->
<p align="right">
  <a href="ros.md" lang="ko">한국어</a> | <a href="../../en/concepts/ros.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# ROS: 시뮬레이터를 둘러싼 통신 계약

## 메시지는 숫자 배열 이상의 뜻을 담는다

ROS 2는 독립 구성요소가 타입 있는 메시지를 교환하게 한다. 토픽은 스트림을 배포하고, 서비스는 제한된 요청·응답을 반환하며, 액션은 긴 목표를 관리하고, TF는 좌표계를 연결한다. 인터페이스가 있다고 메시지가 자동으로 제시간에 도착하거나 순서·실물 안전이 보장되지는 않는다.

[ROS 그래프·QoS](../lessons/sim-ros-01.md), [MuJoCo 브리지](../lessons/sim-ros-02.md), [bag 재생](../lessons/sim-ros-03.md), [공통 embodiment API](../lessons/sim-ros-04.md)는 실제로 source한 ROS 런타임을 사용한다. [Enlight fake hardware](../lessons/sim-enlight-01.md)는 생산용 Flexiv 드라이버 상태가 아닌 시뮬레이션 상태를 발행한다. ROS/DDS 역량이 없으면 unavailable이며, ROS 트래픽 대신 Python 목록을 쓰는 것은 성공 실행이 아니다.

`JointState`에는 관절 `name`, `position`, `velocity`, 타임스탬프가 있다. 이 수업의 회전 위치는 rad, 속도는 rad/s이다. 원소 $j$는 생산자·소비자에서 같은 이름의 관절이어야 한다. 자유 물체가 있으면 `nq`와 관절 이름 수가 다를 수 있으므로 모든 `qpos`가 이름 있는 모터 하나라고 가정하지 않는다. 실제 모델·메시지 계약을 확인한다. 교육 ROS 경로는 진자 또는 고정 베이스 Enlight 모델을 사용하며 스칼라 관절 원소가 대응한다.

## 시간과 좌표계도 계산의 일부다

ROS 타임스탬프는 다음 시간을 나타낸다.

$$
t=t_{sec}+10^{-9}t_{nanosec}.
$$

초와 나노초는 서로 다른 정수 필드다. 단위 변환이 틀리면 최신 측정이 오래된 것처럼 보일 수 있다. 교육 어댑터는 시뮬레이터 `data.time`을 사용하며 벽시계 수신 시간이 아니다. 일반적인 지연 $t_{receive}-t_{send}$은 시간 도메인과 동기화가 맞아야 의미가 있다.

**통신 지연 측정이 아닌 변환 예제**: 2초와 30,000,000나노초는 2.03 s이다.

```python
seconds = 2
nanoseconds = 30_000_000
time_s = seconds + nanoseconds * 1e-9
assert abs(time_s - 2.03) < 1e-12
```

TF는 `pal_world`와 `pal_base` 같은 좌표계 관계를 표현한다. 좌표 라벨은 장식이 아니다. 회전된 좌표의 벡터를 잘못 적용하면 다른 방향을 명령할 수 있다. 어댑터는 항등 정적 변환을 발행하고 수신을 확인한다. 이 단순 통신 경로를 검사하며 보정된 실물 전체 변환 트리를 검증하지는 않는다. 변환 방향은 [기구학](kinematics.md)을 참고한다.

## 어댑터가 실제로 검사하는 것

[ros.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/ros.py)는 `/pal_isolated` 네임스페이스, domain 217, localhost-only 모드의 격리 노드를 만든다. 발행자·구독자는 reliable QoS와 depth 10을 사용한다. Reliable은 통신 정책이며 엄격한 실시간 마감이 아니다. 코드는 discovery와 서비스 준비를 기다리고 수신 마감을 적용해 누락을 조용히 통과시키지 않는다.

물리 스텝 10회 뒤 관절 상태를 발행하고 수신을 기다린 다음 `trace.csv`에 첫 관절의 송신·수신값을 저장한다. `experiment.json` → `payload`에는 노드·토픽·서비스·`qos`·`domain`·`localhost_only`·출처가 있다. 검사는 `all_messages_received`, `service_roundtrip`, `tf_received`, `state_equal`을 포함한다. 액션 예제는 유한한 피보나치 결과 [0, 1, 1, 2, 3, 5, 8, 13]을 계산하며 로봇 궤적을 보내지 않는다.

bag 수업은 예전 operation 이름에 MCAP가 있어도 실제로 rosbag2 **sqlite3** 저장소를 쓴다. 시뮬레이션 나노초 타임스탬프로 직렬화한 `JointState`를 기록하고 다시 읽어 `bag_replay_exact`를 확인한다. 실제 `storage_id`, `messages_written`, `messages_replayed`를 읽는다. 메시지 재생은 직렬화 충실도를 증명하며, 동역학을 다시 실행하거나 실시간 제어기가 같은 궤적을 만든다고 증명하지 않는다.

## 한 변수 사고와 한계

모델·시드·샘플 수를 고정하면 문서의 `variant`는 시뮬레이션 사인 입력의 진폭을 바꾼다. 새 송수신 곡선과 최대 통신 오차를 비교한다. 상태가 달라져도 전송 일치는 정확할 수 있다. 좋은 브리지는 달라진 입력도 충실히 전달한다. QoS 변경은 생산자·소비자 호환성이 필요한 별도 통신 실험이며 문서의 입력 진폭 비교와 다르다.

[검증 보고서](../../verification/reader-experience.md)는 휴대형 모델 검사와 외부 ROS 런타임 검사를 구별한다. 단위 테스트나 소스 검토로 ROS 런타임 배지를 승격할 수 없다. 공통 reset/observe/act/close 용어도 시뮬레이터와 실물 전송체를 동등하게 만들지 않는다.

## 이해 확인

1. 배열에 관절 이름을 넣는 이유는? 모델·생산자마다 숫자 인덱스가 다를 수 있기 때문이다.
2. Reliable QoS가 안전한 제어 마감을 보장하는가? 아니다. 실제 시각·마감·오래된 상태 처리를 확인해야 한다.
3. bag 일치가 물리 재생을 증명하는가? 아니다. 저장 메시지 재현을 검증한다.

다른 물리 시뮬레이터는 [PhysX](physx.md), 다음 권한 경계는 [배포와 실물](deployment-hardware.md)로 이어진다.
