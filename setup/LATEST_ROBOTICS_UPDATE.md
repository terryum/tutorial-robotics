# Latest robotics installation handoff — 2026-11-13

Trigger: **레포를 살펴보고 최신 버전으로 설치를 진행해줘**.
This request authorizes scoped software installation, required system packages and
necessary GPU driver/CUDA updates, compatibility fixes, commits/pushes and CI checks.
It does not authorize reboot, new license acceptance, physical devices or motion.
Installation runs short acceptance only; start 24-hour training explicitly.

## Agent procedure

1. Read workspace/public/private AGENTS, current host ledgers and private NEXT_SESSION.
   Audit actual native OS, GPU/VRAM, driver, disk, repositories and ignored receipts.
   Preserve local changes and learner history. On WS1 Windows preserve existing crash
   evidence before updates; Windows is audit-only in this workflow.
2. Verify `gh context`: personal terryum. Synchronize public, private and core without
   resetting local work; reread fetched instructions. Configure existing credential
   hooks without replacing custom hooks. Never modify vendor sources.
3. Mac is development/client only. Native Ubuntu x86_64 is the GPU installation path.
   Bootstrap Core first, then run `pal stack plan --profile PROFILE --json`.
4. Run `pal stack discover --profile PROFILE --json` for each selected profile.
   Discovery reports upstream HEAD, **not a verified release**. Inspect official
   releases and select stable compatible revisions. Create candidate registry/lock
   changes in an isolated worktree, install and verify there. Never promote merely
   because a commit is newer. Reconcile private exact pins after public/core tests.
5. Audit the official dependency lock and installation instructions at each pinned
   revision. Use `pal stack apply --profile PROFILE --json` for frozen uv projects.
   Missing lock/extras/wheels or required upstream setup steps are blockers to fix
   in the adapter, never reasons to retry with unfrozen resolution. Source trees
   must remain clean. Existing Sim 6.1/Teleop/CloudXR and vendor environments stay intact.
6. For Isaac, verify existing consent applies to the selected terms before adding
   `--accept-eula`. Never use that flag to invent consent. Check kernel/driver support
   and actual sm_120 CUDA kernels before updating system CUDA or NVIDIA drivers.
   Show concrete commands and rollback first; the trigger authorizes necessary
   changes. If reboot is needed, preserve a checkpoint and request that action.
7. Run `pal stack verify --profile PROFILE --json` and inspect results. Isaac smoke
   launches SimulationApp; it does not prove custom FR3 contact or model performance.
   `pal stack download --profile pi05|groot --json` fetches revision-pinned weights.
   A download receipt does not establish usable inference. Gated access stays blocked
   until the user completes the official flow; never export authentication.
8. Launch real policy inference and the relevant PhysX task under isolated evidence.
   Check identity, camera/state mappings, units, finite bounded actions, actual contact,
   task success, server timeout and reset. Only then promote candidate defaults.
9. Run full public/core/private tests, validators, Ruff/mypy, strict docs, credential
   scans and exact-pin doctor. Update only the current host row; commit scoped changes,
   push under terryum and inspect remote CI. Preserve failed receipts and resume there.

## Profiles and limits

`setup/stack-lock.json` records immutable code and weight revisions. Environments
live in ignored `.local/stacks/PROFILE/REVISION/env`; vendor source is a detached
checkout. `UV_LINK_MODE=copy` isolates any installed-library patch from shared uv caches.
GPU framework dependencies never enter the Core lock. No automatic cleanup.

- isaac-modern: Lab 3.0.0 / Sim 6.2 target, Python 3.12, official CUDA 13.0 stack.
- groot: N1.7, separate official dGPU CUDA 12.8 stack. >=40 GB recommended for training;
  local 32 GB training needs a real microbatch-1 memory trial before a full run.
- pi05: LeRobot PyTorch, separate environment, BF16/checkpointing/expert-only baseline.
- openpi-reference: official JAX/LoRA reference, separate Python 3.11 environment;
  actual Blackwell JAX kernels must pass. Do not patch immutable upstream sources.

Managed artifacts budget: 300 GB per machine, including models/data/runs; training
budget: 24 hours per model. The installer checks storage before/after synchronization;
operators must also budget download/cache temporary peaks and data before each job.
The installer does not yet enforce a hard filesystem quota. Do not delete user data.

## Remaining GPU acceptance and FR3 implementation

The portable stack manager is prepared, not GPU-validated on Mac. Before claiming
end-to-end completion, implement and verify the following on an available GPU host:

- Compose the existing pinned FR3 and Robotiq 2F-85 assets without editing vendor bytes;
  validate flange/TCP, limits, mimic coupling, contact and two-camera capture.
- Generate 200 successful block-pick-and-place demonstrations using real simulation;
  split complete episodes 160/20/20. Fit normalization on train only. Preserve timestamps,
  RGB, q/qvel, gripper aperture, language, control rate and absolute/relative actions.
- Export LeRobot and GR00T v2 + modality metadata; validate conversions and hash manifests.
  DROID/Panda checkpoint mappings are not automatically valid FR3 adapters.
- Train pi05 expert-only and optional official openpi LoRA; train N1.7 only after a
  memory trial. Use native optimizer/RNG checkpoints, immutable input identities and
  safe-tensor formats. Save/reload/resume in fresh runs; reject mismatched identities.
- Evaluate base and fine-tuned models on the same 50 unseen initial conditions.
  Success: object released within target, stable for one second; target 40/50.
  Budget exhaustion and sub-threshold performance are explicit failed results.
- Transfer candidate hashes to WS1 and independently evaluate there. Add bilingual
  catalog lessons and deterministic artifact checks after the real task exists.
  Installation evidence never grants learner completion.

These are pending implementation/acceptance, not commands already supplied by `pal`.

## Release watch and optional tools

- GR00T 2: https://research.nvidia.com/labs/gear/gr00t-2/ — code announced for December.
  Check code, weights, terms and real WAM interface before implementing a new provider.
- ASPIRE: https://github.com/NVlabs/ASPIRE — simulation-only optional skill loop;
  no new paid APIs. Not a neural fine-tuning replacement.
- SimFoundry: https://github.com/NVlabs/SimFoundry — optional scene reconstruction,
  ~250 GB full install plus gated models/Gemini; excluded from default installation.
- Flora: https://github.com/NVlabs/Flora — optional research/evaluation annotation;
  validated upstream on H100 80 GB. CPU validate-only first; 32 GB execution unverified.
- Human-1M: https://huggingface.co/datasets/nvidia/PhysicalAI-Human-1M-100K — pinned
  samples/metadata only; CC BY 4.0 attribution. Human video is not robot action ground truth.
- Hardware: https://research.nvidia.com/labs/gear/hardware-prototypes/ — document
  UMI/DexUMI/Neck sources and licenses; no purchases, fabrication or actuation.
