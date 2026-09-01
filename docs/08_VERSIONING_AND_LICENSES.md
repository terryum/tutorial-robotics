# Versioning, Reproducibility, and Licenses

## Pinning

For each external repository record:

- canonical URL
- selected branch/tag
- exact commit SHA
- retrieval date
- dirty state
- license file path
- expected asset paths

A branch name alone is not reproducible.

## Update policy

1. Audit new upstream in read-only mode.
2. Compare file paths, model counts, joint names, APIs, environment requirements, and licenses.
3. Create a new lock candidate.
4. Run asset and tutorial regression tests.
5. Promote only after comparison artifacts are saved.
6. Keep the previous lock and migration notes.

## Asset handling

- Do not copy vendor meshes into this repository unless the license permits redistribution.
- Prefer checked-out external repositories or local paths.
- Converted USD/MJCF files must record their source and conversion command.
- Generated assets are not automatically licensed more permissively than their source.

## Experiment provenance

Every run metadata should include:

- Git commit of this tutorial repository
- external model commits
- environment lock hash
- OS/architecture/GPU
- seed
- physics timestep and control decimation
- policy checkpoint hash when applicable
