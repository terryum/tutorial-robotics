# Learner progress moved to `.local/`

Shared per-learner completion is no longer committed. Run `pal course init`, `pal course status`, and `pal course next`; the CLI stores progress in ignored `.local/progress.json` and evidence under `.local/runs/`.

Repository maintainers track implementation and publication evidence in [PUBLISHING.md](PUBLISHING.md).

Use `pal course list --json` to see completed and pending lessons;
`pal course status --json` lists only remaining or review-needed lessons.
See [Your local progress](../README.md#your-local-progress) for returning to the
same checkout. A fresh clone starts independently with no completed lessons.
