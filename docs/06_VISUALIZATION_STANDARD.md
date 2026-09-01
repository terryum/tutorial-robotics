# Visualization and Result Standard

## Minimum persistent outputs

For a dynamic tutorial, create:

```text
outputs/Txx/<run-id>/
├── command.txt
├── environment.json
├── summary.json
├── metrics.csv
├── trajectory.png
├── rollout.mp4        # or frames/*.png if encoding is unavailable
└── stdout.log
```

## Verification modes

1. **Interactive verified:** viewer opened and the agent had a supported way to inspect it.
2. **Offscreen verified:** frames/video were rendered and inspected; numeric sanity checks passed.
3. **Command-only:** GUI command was provided but not verified. This does not satisfy completion for tutorials requiring visualization unless an offscreen fallback also exists.

## Plot conventions

- one figure per chart; no subplot grids unless the tutorial explicitly requires synchronized comparison
- default Matplotlib colors and style
- axes labels include units
- title includes model ID and run ID
- target and actual trajectories are unambiguous
- do not crop failure regions

## Rollout conventions

- fixed seed and initial state for comparisons
- visible simulation time or frame index
- camera pose recorded in metadata
- no accelerated playback without recording the speed factor
- frame rate and physics timestep recorded separately

## Required summary metrics

Depending on task:

- RMS/max tracking error
- success rate and success definition
- completion time
- contact count and peak force
- energy/effort proxy
- number of retries
- termination reason
- NaN/constraint violations
