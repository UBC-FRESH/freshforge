# FreshForge Roadmap

This roadmap is the current project plan and issue tracker map. Keep it
synchronized with GitHub issues, planning notes, pull requests, and
`CHANGE_LOG.md`.

## Issue Tracker Map

| Phase | Parent issue | Branch | Status |
| --- | --- | --- | --- |
| P0 Bootstrap scaffold | #1 | `feature/p0-bootstrap-scaffold` | Complete |
| P1 Architecture and workflow-language research | #7 | `feature/p1-architecture-contracts` | Complete |
| P2 Core workflow records and validation contracts | #14 | `feature/p2-core-workflow-records` | Complete |
| P3 Node provider API and execution-planning prototype | #21 | `feature/p3-provider-api-planning` | Active |

## Phase 0: Bootstrap Scaffold

Parent issue: #1

Branch: `feature/p0-bootstrap-scaffold`

Goal: establish FreshForge as a public package-backed FRESH project with strict
governance, planning, docs, CI, release-artifact checks, and a minimal
importable Python package.

- [x] P0.1 Governance and planning scaffold (#2)
  - [x] Add public governance files.
  - [x] Add roadmap and changelog with Phase 0 issue references.
  - [x] Add cleaned bootstrap rationale planning note.
  - [x] Document strict issue and roadmap workflow in `AGENTS.md`.
- [x] P0.2 Python package and CLI skeleton (#3)
  - [x] Add package metadata and dependency extras.
  - [x] Add minimal package module and CLI.
  - [x] Add focused tests.
  - [x] Keep runtime dependencies limited to `typer` and `rich`.
- [x] P0.3 Docs, CI, Pages, and release-artifact scaffold (#4)
  - [x] Add Sphinx configuration and docs pages.
  - [x] Add CI workflow for Python 3.11 and 3.12.
  - [x] Add docs Pages workflow.
  - [x] Add release artifact workflow.
  - [x] Add tests for docs configuration import sanity.
- [x] P0.4 Phase closeout and verification (#5)
  - [x] Run local acceptance commands.
  - [x] Update roadmap and changelog closeout notes.
  - [x] Comment on child issues and parent issue with verification result.
  - [x] Commit and push branch.
  - [x] Open PR to `main`.

Phase 0 local verification passed with:

- `python -m pip install -e .[dev]`
- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`

## Phase 1: Architecture And Workflow-Language Research

Parent issue: #7

Branch: `feature/p1-architecture-contracts`

Status: complete

Goal: define the first durable FreshForge architecture contracts without
over-specifying the implementation before evidence exists.

- [x] P1.1 Workflow-as-code pattern survey (#8)
  - [x] Record relevant workflow patterns.
  - [x] Identify accepted FreshForge principles.
  - [x] Identify anti-patterns and deferred features.
  - [x] Tie findings to Phase 2 implementation needs.
- [x] P1.2 Minimum workflow vocabulary and schema direction (#9)
  - [x] Define the core vocabulary.
  - [x] Record schema-format direction.
  - [x] Record minimum Phase 2 implementation target.
  - [x] Record explicit non-goals.
- [x] P1.3 Provider boundary and ecosystem dependency contract (#10)
  - [x] Record dependency direction.
  - [x] Define core vs domain responsibilities.
  - [x] Define adapter packaging options.
  - [x] Record Phase 2/3 implications.
- [x] P1.4 CLI and Python API boundary contract (#11)
  - [x] Define future command groups.
  - [x] Define Python API layering principles.
  - [x] Record IO and output-format principles.
  - [x] Record Phase 2/3 implementation implications.
- [x] P1.5 Docs, roadmap, changelog, and verification closeout (#12)
  - [x] Update docs with Phase 1 decisions.
  - [x] Update roadmap and changelog.
  - [x] Run local acceptance commands.
  - [x] Commit and push branch.
  - [x] Open PR to `main`.

Phase 1 local verification passed with:

- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`

## Phase 2: Core Workflow Records And Validation Contracts

Parent issue: #14

Branch: `feature/p2-core-workflow-records`

Status: complete

Goal: implement the smallest useful set of typed records for workflow
definitions, nodes, inputs, outputs, dependencies, diagnostics, and provenance.

- [x] P2.1 Workflow record dataclasses and serialization helpers (#15)
  - [x] Add record dataclasses and severity enum.
  - [x] Add serialization helpers.
  - [x] Export public record types from the package.
  - [x] Add unit tests for construction and serialization.
- [x] P2.2 YAML/JSON loading and validation diagnostics (#16)
  - [x] Add YAML/JSON loader.
  - [x] Add validation diagnostics.
  - [x] Add tests for valid, malformed, unsupported, missing, duplicate, unknown
        dependency, cycle, and invalid field-shape cases.
- [x] P2.3 Non-executing run planning and CLI commands (#17)
  - [x] Add planning API.
  - [x] Add validate CLI command.
  - [x] Add plan CLI command.
  - [x] Add CLI and planning tests.
- [x] P2.4 Example workflow, docs, and tests (#18)
  - [x] Add public-safe example workflow.
  - [x] Add or update docs for workflow records and CLI examples.
  - [x] Add tests using the tracked example.
  - [x] Keep docs warning-clean.
- [x] P2.5 Phase closeout and verification (#19)
  - [x] Run local acceptance commands.
  - [x] Update roadmap and changelog closeout notes.
  - [x] Comment on child issues and parent issue with verification result.
  - [x] Commit and push branch.
  - [x] Open PR to `main`.
  - [x] Merge after green CI and verify live docs.

Phase 2 local verification passed with:

- `python -m pip install -e .[dev]`
- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`

## Phase 3: Node Provider API And Execution-Planning Prototype

Parent issue: #21

Branch: `feature/p3-provider-api-planning`

Status: active

Goal: create a provider API and planner that can validate a workflow graph and
explain what would run without executing domain tools.

- [x] P3.1 Provider protocol, metadata, and registry (#22)
  - [x] Define provider and node-type metadata records.
  - [x] Define provider reference parsing for provider namespace plus node type.
  - [x] Add explicit registry registration and lookup behavior.
  - [x] Add default built-in example provider registry.
- [x] P3.2 Provider-aware validation and planning records (#23)
  - [x] Preserve structural validation APIs.
  - [x] Add registry-backed provider diagnostics.
  - [x] Extend planned nodes with provider id, node type, and availability.
  - [x] Keep planning deterministic and non-executing.
- [x] P3.3 Providers and inspect CLI surfaces (#24)
  - [x] Add `freshforge providers [--json]`.
  - [x] Add `freshforge inspect PATH [--json]`.
  - [x] Keep `freshforge validate` and `freshforge plan` deterministic and
        provider-aware.
  - [x] Do not add `freshforge run`.
- [x] P3.4 Docs, examples, and tests (#25)
  - [x] Update public docs and README status.
  - [x] Add public planning note for explicit-registry-first design.
  - [x] Keep example workflow resolving against the built-in example provider.
  - [x] Add provider, validation, planning, and CLI test coverage.
- [ ] P3.5 Phase closeout and verification (#26)
  - [x] Run local acceptance commands.
  - [x] Update roadmap and changelog closeout notes.
  - [ ] Comment on child issues and parent issue with verification result.
  - [ ] Open PR to `main`.
  - [ ] Merge after green CI and verify live docs.

Phase 3 local verification passed with:

- `python -m pip install -e .[dev]`
- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`

## Phase 4: Ecosystem Adapter Prototypes

Status: backlog

Goal: prove FreshForge can compose a small public-safe workflow using adapters
from one or more FRESH ecosystem tools without turning FreshForge into a
domain-package dependency hub.

## Phase 5: Documentation, Examples, And Public Alpha Hardening

Status: backlog

Goal: harden docs, examples, tests, CI, and release workflows enough to support
the first public alpha release.

## Current Next Steps

Phase 3 provider API, provider-aware validation/planning, providers CLI,
workflow inspection, docs, examples, and tests are implemented and locally
verified on `feature/p3-provider-api-planning`. The next bounded lane is P3.5
GitHub closeout: reconcile issue comments, open a PR, merge after green CI/docs,
and verify live docs.
