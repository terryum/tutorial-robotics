# Model Validation

Every model needs an asset test before a controller, dataset generator, or policy uses it. A mesh that renders is not a validated robot model.

## 1. Mandatory ten checks

1. The model loads/compiles without unresolved files; warnings are captured and classified.
2. Body/link/joint/actuator/sensor/camera inventory matches the registry.
3. Joint names are unique and lower/upper limits, units and axes are valid.
4. The default/named pose has no severe unintended self-collision or environment penetration.
5. A deterministic 10-second passive/held simulation has no NaN, Inf or numerical explosion.
6. Every rigid body has finite positive mass/inertia and total mass is within an expected range.
7. Actuator order, control dimension and actuator-to-joint mapping match the registry.
8. Left/right hand or bilateral groups have documented sign, mirror and naming conventions.
9. URDF and MJCF forward kinematics agree at at least three deterministic poses within a declared tolerance.
10. When USD exists, Isaac USD and MJCF end-effector/fingertip poses agree at the same deterministic poses within a declared tolerance.

## 2. Additional format-specific checks

- mesh resolution and scale
- fixed/free/mobile base semantics
- collision group/mask behavior
- contact and friction defaults
- drive/actuator stiffness, damping, force/control range
- sensor frame, unit and sample-rate metadata
- keyframes, mimic/tendon/coupling semantics
- importer options for every generated asset

## 3. Cross-format policy

When two or more formats exist:

- compare joint/frame names, axes and limits
- compare total mass and center-of-mass summaries
- compare deterministic FK
- record differences rather than forcing numerical equality
- do not assume equal friction numbers produce equal contact behavior across MuJoCo and PhysX

## 4. Output

Each model receives:

```text
reports/models/<model-id>.md
outputs/T03/<run-id>/<model-id>_validation.json
outputs/T03/<run-id>/<model-id>_fk_comparison.csv
```

A generated USD/MJCF must record source commit, conversion command/options and checksum. Native vendor files remain immutable.
