<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/ros.md" lang="ko">한국어</a> | <a href="ros.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# ROS: communication contracts around a simulator

## A message carries meaning beyond its numeric array

ROS 2 lets independent components exchange typed messages. A topic distributes a stream, a service returns a bounded request/response, an action manages a longer goal, and TF relates coordinate frames. These interfaces do not automatically make messages timely, correctly ordered or safe for a physical robot.

[ROS graph and QoS](../lessons/sim-ros-01.md), [MuJoCo bridge](../lessons/sim-ros-02.md), [bag replay](../lessons/sim-ros-03.md) and [common embodiment API](../lessons/sim-ros-04.md) use an actual sourced ROS runtime. The [Enlight fake-hardware lesson](../lessons/sim-enlight-01.md) publishes simulated state, not production Flexiv driver state. Missing ROS/DDS capability remains unavailable; a Python list standing in for ROS traffic is not a successful run.

A `JointState` message contains joint `name`, `position`, `velocity` and a timestamp. Here revolute positions use rad and velocities rad/s. Array element $j$ must mean the same named joint across producer and consumer. If a model includes a free body, `nq` need not equal joint-name count, so inspect the actual model/message contract rather than assuming every `qpos` entry is one named motor. The teaching ROS path uses the pendulum, or the fixed-base Enlight model, with matching scalar joint entries.

## Timestamps and frames are part of the calculation

A ROS timestamp represents

$$
t=t_{sec}+10^{-9}t_{nanosec}.
$$

Seconds and nanoseconds are different integer fields; a unit conversion error can make a fresh measurement look ancient. In this teaching adapter, timestamps come from simulator time `data.time`. They are not wall-clock receipt time. A general latency estimate $t_{receive}-t_{send}$ is meaningful only with compatible clock domains and synchronization.

Worked conversion, **not measured communication latency**: 2 seconds plus 30,000,000 nanoseconds is 2.03 s.

```python
seconds = 2
nanoseconds = 30_000_000
time_s = seconds + nanoseconds * 1e-9
assert abs(time_s - 2.03) < 1e-12
```

TF expresses a relation such as `pal_world` to `pal_base`. A frame label is not decoration: applying a vector expressed in a rotated frame can command the wrong direction. The adapter publishes an identity static transform and checks its reception. This verifies that simple communication path, not a calibrated real robot's entire transform tree. See [kinematics](kinematics.md) for transform direction.

## What the adapter actually tests

[ros.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/ros.py) creates an isolated node in `/pal_isolated`, domain 217 and localhost-only mode. Publisher and subscription use reliable QoS with depth 10. Reliable delivery is a communication policy, not a hard real-time deadline. The code waits for discovery, checks service availability, and enforces receive deadlines rather than silently accepting missing samples.

After ten physics steps it publishes simulated joint state, waits for a receive, and saves sent/received first-joint values in `trace.csv`. `experiment.json` → `payload` records nodes, topics, services, `qos`, `domain`, `localhost_only`, and source. Checks include `all_messages_received`, `service_roundtrip`, `tf_received` and `state_equal`. The action example calculates the bounded Fibonacci result [0, 1, 1, 2, 3, 5, 8, 13]; it sends no robot trajectory.

The bag lesson explicitly uses rosbag2 **sqlite3** storage, despite a legacy operation label mentioning MCAP. It writes serialized `JointState` messages with simulated nanosecond timestamps, reads them back and verifies `bag_replay_exact`. Read actual `storage_id`, `messages_written` and `messages_replayed` fields. Replaying saved message values proves serialization fidelity; it does not rerun dynamics or prove that a live controller would reproduce the trajectory.

## One-variable reasoning and limits

With a fixed source model, seed and sample count, the documented `variant` scales the simulated sinusoidal input amplitude. Compare the new sent/received curves and maximum communication discrepancy. The simulator state may change while transport equality remains exact: a good bridge preserves a different input just as faithfully. Changing QoS would be a separate communication experiment requiring both publisher and subscriber compatibility; it is not the documented input-amplitude comparison.

The [verification report](../../verification/reader-experience.md) distinguishes portable model checks from external ROS runtime checks. A unit test or source review cannot promote a ROS runtime badge. The common reset/observe/act/close vocabulary also does not equate the simulator with a physical transport.

## Check your understanding

1. Why include joint names with arrays? Numeric indices can differ across models or producers.
2. Does reliable QoS guarantee a safe control deadline? No; inspect actual timestamps, deadlines and stale-state behavior.
3. Does bag equality prove physics replay? No. It establishes saved-message reproduction.

Continue to [PhysX](physx.md) for a second physical simulator or [deployment and hardware](deployment-hardware.md) for the next authority boundary.
