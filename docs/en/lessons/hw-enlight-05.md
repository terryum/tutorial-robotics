<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/hw-enlight-05.md" lang="ko">한국어</a> | <a href="hw-enlight-05.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# hw-enlight-05 — Enlight probe plane-force preparation

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

Read the [deployment and hardware chapter](../concepts/deployment-hardware.md) and [safety rules](../../07_SAFETY.md). Ask: “What must be checked before trusting the direction and magnitude of force against a plane?” This stage is `scaffolded`, without device, tool or force-controller evidence.

Also read the [control and contact chapter](../concepts/control-contact.md) for contact force and coordinate-transform prerequisites.

## Learning goals

Review probe TCP, payload, force limits and plane calibration. A separately validated force controller is required; policy torque is not sent directly to hardware.

## Preflight

The prerequisite is `hw-enlight-04`. Inspect `pal course next --json` read-only and review evidence of device identity, disabled/error/E-stop state, joint/force limits, timeout, state timestamps, stop path and isolated networking. Real device records, approvals and calibration belong only in ignored `.local/`.

Compatibility between the Enlight RDK 2.1 / v3E.1 baseline and public description v4 needs separate review. Do not assume a probe exists: verify mounting, TCP, payload, force sensing and plane calibration individually. A host named WS1 or WS2 does not supply this evidence.

## Action

### Read preparation records only

Record evidence status for model identity, probe TCP/mass/center of mass, plane frame, sensor zero/payload compensation, force limits, validated force controller and timeout/stop tests. Leave missing items unverified.

Currently `pal lesson run hw-enlight-05` is rejected with `NotImplementedError` carrying `reader_test_required`. Do not expect a normal measurement run or returned run_dir. Do not send device execution commands, torques or force targets for this preparation lesson. Physical contact requires a separately validated execution route and new exact approval for that run.

## Expected

The expected outcome is “preparation under review, no physical evidence, completion blocked.” Do not create `summary.json`, `trace.csv` or force-response plots and describe them as measurements. Keep `scaffolded` and `reader_test_required`.

### Evidence to inspect

For each readiness item, record its source and `confirmed`/`unverified` status. Express force and plane normal in the same frame; declare force in N and the normal dimensionless. Check tool/payload compensation and fresh state timestamps. This list does not automatically authorize physical action. The public [verification record](../../verification/robot-paths-2026-11-08.md) also leaves real Enlight/probe execution unverified.

## How it works

### Express force and plane in the same frame

This is preparation geometry, not an implemented force-control law. In world frame W, let $p_0\in\mathbb R^3$ be a point on the plane(m), $p\in\mathbb R^3$ the probe tip(m), and $n\in\mathbb R^3$ a unit normal. Define the normal's direction before interpreting signs.

$$
d=n^T(p-p_0),\qquad f_W=R_{WT}f_T,\qquad f_n=n^Tf_W.
$$

$d$ is signed plane distance(m); $R_{WT}$ is a dimensionless 3×3 rotation mapping tool-frame T vectors into W; $f_T,f_W$ express the same force(N); and $f_n$ is normal force(N). This describes the force vector only. Transforming a full sensor wrench's torque to another reference point also requires a position-offset term.

Worked calculation, not a measurement: $n=[0,0,1]^T$ and $f_W=[0,0,2]^T$ N give $f_n=2$ N. Actual force records require checked sensor signs, zero, tool-gravity compensation and reference point before comparison with this equation. 2 N is not an approved target or force limit.

### Position policy versus force controller

Reach-policy joint targets and good simulation rewards do not ensure bounded contact force. A separately validated force/impedance controller, sensor delay/saturation handling, contact-loss/collision behavior and stop tests are required. This lesson implements neither force gains nor contact execution.

## Code connection

The `implementation != "implemented"` check in [`runner.py`](../../../src/pai_lab/lessons/runner.py) rejects this lesson before execution. `execute` in [`run_card.py`](../../../src/pai_lab/hardware/run_card.py) is a separate approval gate with an injected validated transport; it provides no vendor connection or torque-enable API.

The current gate supports only Enlight `small-joint-move`. It does not implement probe force control or authorize contact. Its card lifetime of at most 60 seconds, single-use consumption, timeout at most 1 second and increment at most 0.02 rad apply to that limited joint action; they are not contact-force criteria. Training checkpoint code is not this lesson's execution path.

## Try it

### Offline one-variable calculation

Tilt only the example's normal from $[0,0,1]^T$ to $[0,\sin30^\circ,\cos30^\circ]^T$, keeping $f_W=[0,0,2]^T$ N fixed. Then $f_n=2\cos30^\circ\approx1.732$ N. The force itself is unchanged while its normal component changes. Explain why an error in plane direction changes force interpretation.

This is a paper calculation. Do not tilt a real surface or move a robot. A `--variant` trial or `pal lesson finish` cannot turn preparation review into measurement or completion evidence.

## Recovery

If device, probe, calibration, controller, compatibility or a safety gate is unverified, record the blocker and next evidence needed. Preserve failed/interrupted records without automatic retry or motion resume. Physical progression is offline replay → command sink → read-only → live shadow → torque-disabled replay → fresh run card → one explicitly approved action. Contact needs separate validation and new per-run approval.

## Checkpoint

### Check your understanding

1. What errors follow from misreading the normal direction or force frame?
2. Why do a good reach policy and a small-joint-move approval not authorize probe contact?
3. What do the current runner and run-card code each provide, and what remains absent?

Record inspected evidence, unverified tools/calibration/compatibility, the controller to validate and the safety route. Keep this stage incomplete without physical evidence. A navigation link to another lesson does not satisfy execution gates.

Answer guide: Frame and normal-sign errors distort force direction and components. Reach performance does not bound contact force, and a joint-move card does not approve contact. The runner blocks this lesson; the run-card gates only a limited joint action through a separately validated transport. Probe force control and device evidence remain absent.

<!-- pal:navigation:start -->
## Next lesson

[hw-enlight-06](./hw-enlight-06.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
