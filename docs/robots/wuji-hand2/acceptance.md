# Wuji Hand 2 Beta 2 acceptance

The canonical public model is `wuji-description` v2026.8.19 at commit `b13f7d52b23cb79e35357303c72b7f61f1d2fda2`. Fetch it on demand:

```bash
pal assets fetch wuji-description-beta2 --json
pal lesson check core-wuji-01 --json
```

For left, right, and any with-mount variants used by a lesson, inspection must confirm 20 joints, five fingertip sites, five `*_tip_sensor_frame` bodies, and consistent mass, collision, and frame inventories. The canonical identifiers are `hand2/hand2_beta2/body`, `wuji_hand2_beta2_description`, `wujihand2-beta2-{side}`, and `wujihand2_beta2.usd`.

Simulation contact or tactile values are synthetic observations and must not be labeled as physical sensor force.

## Read-only hardware gate

Capture a local, sanitized state snapshot without serial or IP, then run:

```bash
pal hardware preflight wuji --read-only --snapshot .local/hardware/wuji.json --json
```

The gate requires Beta 2 identity, 11–13 V supply, firmware v2.6.0 with SDK v2026.8.31, network readiness, disabled state, no active error, E-stop readiness, fresh timestamps, GET ≤100 Hz, and publish ≤1 kHz. Joint angle is radians on `joint_states`; errors belong to `joint_diagnostics`; effort is current in amperes, not N·m.

`0x2115` is interpreted only through the pinned firmware release manifest. The mandatory action is to disable commands, preserve diagnostics, and require operator inspection. Firmware inspection is read-only; upgrade is never automatic.

## Motion boundary

```text
command sink → read-only → disable/E-stop confirmation → fresh run card → one approved low-risk action at 0.5 A initial cap
```

No acceptance result grants future motion authority. Official documentation precedence is release notes, version compatibility, then the general product page.
