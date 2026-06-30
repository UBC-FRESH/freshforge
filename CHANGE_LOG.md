# Change Log

Newest entries last. Keep this file synchronized with roadmap phase/task
completion and GitHub issue comments.

## 2026-06-29

- Created the Phase 0 bootstrap lane for FreshForge on
  `feature/p0-bootstrap-scaffold`, with parent issue #1 and child task issues
  #2 through #5 for governance, package skeleton, docs/automation, and closeout.
- Began scaffolding FreshForge as a package-backed FRESH project for
  workflow-as-code in open forest resources and ecosystem services modelling.
- Completed the Phase 0 scaffold with strict FRESH governance docs, roadmap,
  changelog, planning note, contribution and public-repo hygiene files, minimal
  `freshforge` package and Typer CLI, Sphinx RTD-theme docs, CI/docs/release
  workflows, and focused import/CLI/docs tests.
- Verified Phase 0 locally with editable install, `ruff check`, `pytest`,
  warning-clean Sphinx HTML build, package build, and `twine check` for both
  generated artifacts.
- Merged Phase 0 to `main` through PR #6 at `99b20a5` and closed the Phase 0
  parent issue #1 after the child issues had been completed.
- Opened Phase 1 on `feature/p1-architecture-contracts` with parent issue #7
  and child issues #8 through #12 for workflow-pattern survey, vocabulary/schema
  direction, provider boundary, CLI/API boundary, and closeout.
- Recorded the Phase 1 architecture contracts in `planning/`, defining YAML as
  the first authoring direction, naming the initial workflow vocabulary, keeping
  FreshForge core independent of FEMIC/FHOPS/ws3/Modelwright/Nemora imports, and
  deferring parser, validator, provider, planning, and execution code to later
  phases.
- Verified Phase 1 locally with `ruff check`, `pytest`, warning-clean Sphinx
  HTML build, package build, and `twine check` for the generated artifacts.
