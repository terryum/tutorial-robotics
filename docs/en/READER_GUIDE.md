# Read on GitHub, execute in your terminal

This is the current execution guide. Dated host installation reports describe their historical revision. They do not establish current readiness. Lesson Action commands compute and exit; GUI replay is separate.

## First setup — macOS Terminal, zsh

Git retrieves pinned sources. Python runs the experiments. uv installs locked dependencies into `.venv`. MuJoCo provides dynamics and rendering; NumPy performs numerical calculations.

Use the repository root for all relative paths below. Adjust the first path if your checkout lives elsewhere.

```bash
cd ~/Codes/robotics/tutorial-robotics
```

```bash
sh bootstrap.sh --plan
```

This prints the OS, architecture, disk space, Python/uv status, environment path and proposed commands, then exits. If setup is needed, apply the minimal Core plan. Wait while dependencies download; preserve an error and reread the plan if installation fails.

```bash
sh bootstrap.sh --apply
```

```bash
source .venv/bin/activate
```

```bash
pal setup verify --profile core --json
```

Expect `ready: true`. Otherwise address missing_capabilities and rerun verify. CUDA, ROS and Isaac need their separately prepared lesson environments.

```bash
pal course init --json
```

```bash
pal course next --json
```

Select one eligible lesson. Initializing does not erase completed records.

## Resume in a new terminal

Run `cd` and `source .venv/bin/activate` in each new terminal. Installation is not repeated.

```bash
pal course status --json
```

```bash
pal feedback list --json
```

```bash
python -m json.tool .local/session.json
```

Read session.json after at least one execution. If it does not exist, start with `pal course next --json`. `pal: command not found` usually means activation is missing.

On another host, prepare locked sources and rerun verify there. Copying progress does not verify that environment. Preserve original evidence and use a fresh run directory.

## One lesson at a time

1. Read Expected and identify the first quantities and units to inspect.
2. Execute each Action command. `executed` is an experiment result, not learner completion.
3. Use `lesson inspect` to validate and summarize artifacts. Open PNGs with macOS `open` or a file manager. A text editor can read CSV files.
4. Calculate the worked example and locate corresponding values at the same timestamp in code and CSV.
5. Change the single input in Try it and use `lesson compare`. Environment and structure audits can be reviewed without an artificial numeric comparison.
6. Save questions, verify fixes, then review and finish. Stop before the next lesson.

If baseline-01 exists, choose baseline-02. Never overwrite earlier evidence. Keep failed run.json receipts. Press Ctrl-C in the terminal to interrupt a running process.

## Model replay and Mac controls

For a lesson with saved model state, substitute its actual ID and run path:

```bash
mjpython -m pai_lab.cli lesson view core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01
```

The window replays once and exits. Add `--speed 0.25` for slower playback. Left-drag rotates, right-drag translates and scrolling zooms. Enable secondary click on a trackpad or begin with a mouse. Shift-drag selects horizontal movement. Match displayed axes to model joint/frame names. Closing the window stops replay.

Replay assigns saved qpos/qvel and calls `mj_forward`. It does not integrate dynamics with `mj_step` or produce new force/contact experiment evidence. Without a GUI, render the final saved state:

```bash
pal lesson view core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01 --offscreen .local/pd-replay-01.png
```

Preserve older runs without replay files and create a fresh run. Binary replay models require the same MuJoCo version.

## Turn questions into teaching improvements

```bash
pal feedback add 'Original question; step: Observe; actual value; difference from expectation' --lesson core-fr3-02 --json
```

Resolve with `pal feedback resolve ID --evidence 'answer and cause; missing explanation; changed file; verification result; next starting point'`. Add reusable explanations to the lesson; keep personal execution data under `.local`. Developers select an independent session with `PAL_LOCAL_DIR` and never manufacture learner completion.

Math follows [GitHub mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions). Mac replay follows the [MuJoCo passive viewer](https://mujoco.readthedocs.io/en/stable/python.html#passive-viewer).
