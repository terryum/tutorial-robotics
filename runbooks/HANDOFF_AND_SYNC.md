# Runbook — Repository Sync and Model Promotion

## 1. 개별 Markdown 파일을 전달하지 않는다

Codex가 올바른 prerequisite와 progress를 판단하려면 다음이 함께 있어야 한다.

- `AGENTS.md`
- `MACHINE_SEQUENCE.md`
- `tutorials/`
- `docs/`, `setup/`, `runbooks/`
- `state/`
- 실제 생성된 `src/`, `configs/`, `tests/`, `reports/`
- Git history

따라서 각 컴퓨터에는 **저장소 전체**를 clone/pull하거나 rsync한다.

## 2. Git에 포함할 것

- source code
- Markdown instructions/reports
- configs and schemas
- lockfiles
- small deterministic test vectors
- model/dataset/checkpoint manifest and hashes
- phase gates

## 3. Git에 포함하지 않을 것

- virtual environments
- CUDA/Isaac cache
- `.local/HOST_PROFILE.md`
- large model checkpoints
- raw dataset blobs
- generated video collections
- vendor source trees that can be re-cloned

대용량 artifact는 경로와 hash를 manifest에 기록하고 별도 NAS/object storage/rsync로 이동한다.

## 4. MacBook → WS2 handoff

```text
Mac reports/state/configs
+ exact source pins
+ small test vectors
+ unresolved issue list
```

WS2는 Mac environment를 복사하지 않고 같은 lock/spec으로 새 환경을 만든다.

## 5. WS2 → WS1 handoff

반드시 다음 bundle을 생성한다.

```text
checkpoint
model config
normalization statistics
camera set and order
joint/state/action order
units
policy rate
control rate
action horizon/chunk size
pre/post-processing
URDF/MJCF/USD revisions
calibration version
dataset manifest
Git commit
Python lockfile
container image/digest
simulation and sim-to-sim report
deterministic test vectors
rollback model
```

## 6. promotion state

```text
EXPERIMENTAL
→ SIM_VALIDATED
→ CANDIDATE_BUNDLE
→ RUNTIME_OFFLINE_VALIDATED
→ READ_ONLY_VALIDATED
→ SHADOW
→ GATED
→ PRODUCTION_CANDIDATE
```

Codex는 한 요청에서 둘 이상의 safety promotion을 자동으로 넘지 않는다.
