# Future Windows MANUS/VIVE handoff

This phase is intentionally deferred until the devices and Wuji Hand 2 arrive.
Windows owns MANUS Core, VIVE Hub, SteamVR, device calibration, and raw capture.
The ROS 2/MuJoCo side owns retargeting, limits, simulation, and recording.

```text
MANUS Metagloves Pro Haptic skeleton   VIVE Ultimate wrist pose
                 \                     /
                  Windows input gateway
                          |
             timestamp + confidence + side
                          |
                  retargeting/safety gate
                          |
       /left_hand/joint_commands or /right_hand/joint_commands
                          |
            MuJoCo now; hardware adapter later
```

The future gateway must preserve monotonic timestamps, sequence, handedness,
calibration identity, confidence, stale/dropout state, wrist pose, named hand
skeleton, and deadman/clutch state. Wrist poses become `PoseStamped`; retargeted
hand positions become named `JointState` messages. Tracking older than 100 ms,
sequence reversal, invalid confidence, or released deadman must hold/stop before
any physical command.

VIVE Ultimate Tracker is an inside-out tracker and must be validated through
the then-current VIVE Hub/SteamVR path; lighthouse-only examples are not an
assumed fallback. Haptic/tactile feedback is a separate acceptance phase.
