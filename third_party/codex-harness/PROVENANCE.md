# Codex Harness provenance and redistribution

Imported project-local skill, scripts, references and five role definitions from
[revfactory/codex-harness](https://github.com/revfactory/codex-harness), revision
`80f8217b5b6d3f220a31f05f9c0adaf09dac40f4`, using its provided installer.
The source checkout and user-wide configuration were not changed.

The imported material is Apache-2.0. The complete [license](LICENSE) and upstream
[NOTICE](NOTICE) are retained here, including original attribution to robin and
the upstream Harness revision. Apache-2.0 permits redistribution and modification
subject to its conditions; it does not grant trademark permission or endorsement.
Redistribution requirements were checked against the official
[Apache-2.0 Section 4](https://www.apache.org/licenses/LICENSE-2.0).
This redistribution retains notices, supplies the license, and identifies local
modifications. Individual robot/model assets remain under their own licenses.

Local integration: installer merged AGENTS.md and project configuration. Imported
Harness skill/scripts/roles remain unmodified unless listed below. Robotics book
skills, templates, glossary, book contract, specification tooling, curriculum
generator changes and book content are local additions under the repository's
Apache-2.0 license. Production run outputs and communications are ignored.

The current runtime exposes general native agents rather than named custom role
selection. Task packets explicitly supply the installed role definition and
record real native IDs separately from Harness ledger state. Static structure
validation is not evidence of native execution.
