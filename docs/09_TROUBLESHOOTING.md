# Troubleshooting Protocol

## Do not guess blindly

For any failure:

1. Copy the exact command and complete traceback to `state/OPEN_ISSUES.md` or an error log.
2. Classify it: environment, asset path, model compile, rendering, physics, ROS middleware, training, or hardware.
3. Reduce to the smallest reproducible command.
4. Change one variable at a time.
5. Preserve the failed run directory.
6. Add a regression test when fixed.

## Frequent Mac issues

- wrong architecture or Rosetta shell
- GUI launched from non-interactive/sandboxed process
- OpenGL/offscreen rendering backend mismatch
- MPS numerical or unsupported-operator differences
- ROS 2 DDS multicast/firewall behavior
- binary package missing for `osx-arm64`

## Frequent model issues

- relative mesh paths broken after copying only the XML
- missing Git submodules
- duplicated body/joint/site names after composition
- freejoint/base assumption mismatched
- actuator count differs from controllable joint count
- invalid inertia or non-positive mass
- collision meshes too detailed or interpenetrating

## Frequent learning issues

- action normalization mismatch
- camera ordering mismatch
- episode boundary leakage
- incorrect control frequency or action chunk interpretation
- reward scale imbalance
- policy evaluated with different observation preprocessing

A tutorial remains `blocked-retry` until the original acceptance criteria pass.
