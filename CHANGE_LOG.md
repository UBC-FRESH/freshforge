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
- Added a Phase 2 status signal to the docs index so the public docs root
  clearly advertises the workflow-records milestone.
- Opened Phase 3 on `feature/p3-provider-api-planning` with parent issue #21
  and child issues #22 through #26 for provider metadata/registry,
  provider-aware validation/planning, CLI surfaces, docs/tests, and closeout.
- Implemented the Phase 3 provider API with stdlib metadata records, provider
  reference parsing, an explicit in-process registry, a public-safe built-in
  example provider, provider-aware diagnostics, provider-aware run-plan records,
  and user-facing `freshforge providers` / `freshforge inspect` commands.
- Updated `freshforge validate` and `freshforge plan` to use provider-aware
  diagnostics through the default registry while keeping workflow planning
  non-executing and deferring `freshforge run`, entry-point discovery, provider
  auto-import, caching, checkpoints, run records, artifact materialization, and
  ecosystem adapters.
- Added Phase 3 provider documentation, an explicit-registry-first planning
  note, README status updates, and tests for provider metadata, registry lookup,
  provider-aware validation, provider-aware planning, and CLI JSON output.
- Verified Phase 3 locally with editable install, `ruff check`, `pytest`,
  warning-clean Sphinx HTML build, package build, and `twine check` for the
  generated artifacts.
- Merged Phase 3 to `main` through PR #27 at `230dd45` after CI passed on
  Python 3.11 and 3.12; the Docs workflow deployed successfully, and live docs
  verification returned `200` for both the docs root and providers page with
  Phase 3 provider content present.
- Opened Phase 4 on `feature/p4-ecosystem-adapter-prototype` with parent issue
  #28 and child issues #29 through #33 for entry-point discovery, fixture
  adapter, multi-provider CLI behavior, docs/tests, and closeout.
- Implemented Python entry-point provider discovery through the
  `freshforge.providers` group, with provider-factory loading, explicit registry
  preservation, and diagnostics for load failures, factory failures, invalid
  provider objects, invalid metadata, and duplicate provider IDs.
- Added the public-safe `freshforge.fixture` adapter as a FreshForge-shipped
  entry-point provider, plus `examples/ecosystem_adapter_workflow.yaml` to prove
  a multi-provider graph using both built-in and discovered providers without
  execution or real FRESH ecosystem imports.
- Updated CLI/default registry behavior so `freshforge providers`,
  `freshforge validate`, `freshforge inspect`, and `freshforge plan` use
  entry-point discovery by default while keeping explicit registration available
  for tests and controlled applications.
- Added adapter discovery documentation, updated README/architecture/provider
  docs, recorded the Phase 4 entry-point discovery planning note, and expanded
  tests for discovery diagnostics, fixture metadata, fixture validation,
  multi-provider validation, inspection, and planning.
- Verified Phase 4 locally with editable install, `ruff check`, `pytest`,
  warning-clean Sphinx HTML build, package build, and `twine check` for the
  generated artifacts. Also inspected the sdist entry-point metadata and smoke
  tested installed CLI provider listing and multi-provider planning.
- Merged Phase 4 to `main` through PR #34 at `8d049ef` after CI passed on
  Python 3.11 and 3.12; the Docs workflow deployed successfully, and live docs
  verification returned `200` for both the docs root and adapter discovery page
  with Phase 4 adapter content present.
- Opened Phase 5 on `feature/p5-public-alpha-hardening` with parent issue #35
  and child issues #36 through #40 for docs/API polish, examples, CI and
  release-artifact hardening, release notes, and closeout.
- Hardened public alpha status docs for `0.1.0a1`, replacing stale scaffold-only
  wording with the implemented Phase 0-4 scope and explicit limits: no workflow
  execution, no stable workflow DSL, no real ecosystem adapters, and no PyPI
  publication.
- Added examples documentation for the single-provider and multi-provider
  public-safe workflow specs, plus release-checklist documentation for the
  GitHub prerelease, tag target, artifact checks, and deferred PyPI publication.
- Updated `RELEASE_NOTES.md` for the implemented `0.1.0a1` alpha scope and added
  release-contract tests covering version synchronization, manifest example
  inclusion, fixture provider entry-point metadata, and documented alpha
  boundaries.
