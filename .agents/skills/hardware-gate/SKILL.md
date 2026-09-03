---
name: hardware-gate
description: Enforce read-only-first safety checks for any physical robot, actuator, firmware, contact, or motion request.
---

# Hardware Gate

Default to offline replay, command sink, read-only telemetry, and live shadow with no commands.

Before any actuation, require model identity, safety state, physical E-stop, workspace, payload, limits, acknowledgement, watchdog, timeout, stale-command rejection, and one active command authority. Require a fresh explicit per-run approval naming the robot, subsystem, trajectory, mode, and limits.

Never infer permission from a previous run. Never enable torque, publish motion, execute contact or identification excitation, update firmware, raise limits, or bypass a safety path without that approval.
