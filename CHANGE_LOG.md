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
- Merged Phase 1 to `main` through PR #13 at `146753c` after CI passed on Python
  3.11 and 3.12, then closed the Phase 1 parent issue #7.
- Enabled GitHub Pages workflow deployments for the new FreshForge repository,
  reran the docs workflow successfully on `main`, and verified the public docs
  root returned `200` with FreshForge and Phase 1 content.
- Reconciled the Phase 1 roadmap closeout checklist so P1.5 reflects the merged
  PR and pushed closeout commits on `main`.
- Reconciled the Phase 1 current-next-step note after the final closeout commits
  on `main`.
- Opened Phase 2 on `feature/p2-core-workflow-records` with parent issue #14
  and child issues #15 through #19 for workflow records, loading/validation,
  non-executing planning and CLI, examples/docs/tests, and closeout.
- Implemented Phase 2 core workflow records using stdlib dataclasses and enums,
  YAML/JSON loading with `PyYAML`, structured validation diagnostics,
  deterministic non-executing run planning, and user-facing `freshforge validate`
  / `freshforge plan` commands with human-readable and JSON output.
- Added the public-safe `examples/stand_treatment_workflow.yaml`, Phase 2
  workflow-record documentation, and tests for records, loading, validation,
  planning, CLI behavior, and JSON output.
- Verified Phase 2 locally with editable install, `ruff check`, `pytest`,
  warning-clean Sphinx HTML build, package build, and `twine check` for the
  generated artifacts.
- Merged Phase 2 to `main` through PR #20 at `42200b6` after CI passed on Python
  3.11 and 3.12.
- Completed Phase 2 closeout by reconciling roadmap and issue state after merge;
  final GitHub Actions and live-docs verification were performed on `main`.
