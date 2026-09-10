# Large artifact publishing

GitHub is the source of truth for code, catalog, documentation, tests, and small fixtures. Large public outputs belong in:

- `terryum/tutorial-robotics-datasets`
- `terryum/tutorial-robotics-models`
- `terryum/tutorial-robotics-media` only when media size requires it

An upload is eligible only when its dataset/model card records the generating lesson ID, source Git commit, upstream revisions, license, SHA-256, feature/action ordering, units, and verification status. Restricted vendor files, serials, private IPs, site calibration, raw bags, and credentials are never uploaded. `reader_test_required` artifacts must retain that label until authoritative execution evidence exists.
