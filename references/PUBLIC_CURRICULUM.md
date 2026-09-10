# Public curriculum baseline

The versioned [catalog](../curriculum/catalog.json) defines 49 public lessons: 25 Core, 15 Simulation, and 9 Hardware.

FR3 teaches manipulator control; Unitree G1 teaches floating-base motion and imitation; Wuji Hand 2 Beta 2 and Sharpa Wave teach dexterity and retargeting; ALOHA teaches bimanual imitation; Flexiv Enlight teaches a second public manipulator and read-only-first hardware integration. Shared task, observation, action, dataset, evaluator, and deployment contracts transfer between robots. Gains, dynamics, calibration, and policies do not transfer by assumption.

Every external repository or model is pinned in `assets/sources.json`. Vendor checkouts are read-only, fetched on demand, and excluded from Git. If redistribution permission is unknown, only the source URL, version, license status, checksum or Git revision, and adapter contract may be published.

English and Korean pages share the same code and command sequence. Each page states Action, Expected result, Recovery, Try it, Checkpoint, artifacts, safety level, and a truthful `ci-checked`, `maintainer-checked`, or `reader_test_required` badge.
