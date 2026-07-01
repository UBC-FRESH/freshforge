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
| P3 Node provider API and execution-planning prototype | #21 | `feature/p3-provider-api-planning` | Complete |
| P4 Ecosystem adapter prototype | #28 | `feature/p4-ecosystem-adapter-prototype` | Complete |
| P5 Documentation, examples, and public alpha hardening | #35 | `feature/p5-public-alpha-hardening` | Complete |
| P6 Local workflow run runtime | #48 | `feature/p6-workflow-run-runtime` | Complete |

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

Status: complete

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
- [x] P3.5 Phase closeout and verification (#26)
  - [x] Run local acceptance commands.
  - [x] Update roadmap and changelog closeout notes.
  - [x] Comment on child issues and parent issue with verification result.
  - [x] Open PR to `main`.
  - [x] Merge after green CI and verify live docs.

Phase 3 local verification passed with:

- `python -m pip install -e .[dev]`
- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`

Phase 3 merged to `main` through PR #27 at `230dd45`. GitHub CI passed on
Python 3.11 and 3.12, the Docs workflow deployed successfully, and the live docs
root and providers page returned `200` with Phase 3 provider content.

## Phase 4: Ecosystem Adapter Prototypes

Parent issue: #28

Branch: `feature/p4-ecosystem-adapter-prototype`

Status: complete

Goal: prove FreshForge can compose a small public-safe workflow using adapters
from one or more FRESH ecosystem tools without turning FreshForge into a
domain-package dependency hub.

- [x] P4.1 Entry-point provider discovery (#29)
  - [x] Add entry-point discovery API.
  - [x] Support provider factories returning `Provider` instances.
  - [x] Return diagnostics for load failures, invalid objects, duplicate
        provider IDs, and metadata errors.
  - [x] Keep explicit registry registration working unchanged.
- [x] P4.2 Public-safe fixture adapter (#30)
  - [x] Add provider id `freshforge.fixture`.
  - [x] Register fixture provider through FreshForge package entry points.
  - [x] Add FRESH-flavoured non-executing node types.
  - [x] Validate only declared broad keys and simple parameters.
- [x] P4.3 Multi-provider example and CLI behavior (#31)
  - [x] Add multi-provider public-safe example workflow.
  - [x] Ensure `freshforge providers [--json]` lists fixture provider.
  - [x] Ensure validate, inspect, and plan resolve fixture references by
        default.
  - [x] Keep `freshforge run` absent.
- [x] P4.4 Docs, planning note, and tests (#32)
  - [x] Add adapter/discovery docs page.
  - [x] Update README, architecture, providers, roadmap docs, roadmap, and
        changelog.
  - [x] Add entry-point-discovery planning note.
  - [x] Add provider discovery, fixture adapter, CLI, and workflow tests.
- [x] P4.5 Phase closeout and verification (#33)
  - [x] Run local acceptance commands.
  - [x] Update roadmap and changelog closeout notes.
  - [x] Comment on child issues and parent issue with verification result.
  - [x] Open PR to `main`.
  - [x] Merge after green CI and verify live docs.

Phase 4 local verification passed with:

- `python -m pip install -e .[dev]`
- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`

Phase 4 entry-point artifact and CLI smoke verification also passed:

- inspected the sdist `entry_points.txt` and confirmed the
  `freshforge.providers` fixture entry point;
- `freshforge providers --json` listed `freshforge.example` and
  `freshforge.fixture` with no diagnostics;
- `freshforge plan examples/ecosystem_adapter_workflow.yaml --json` produced a
  provider-aware non-executing plan using both providers.

Phase 4 merged to `main` through PR #34 at `8d049ef`. GitHub CI passed on
Python 3.11 and 3.12, the Docs workflow deployed successfully, and the live docs
root and adapter discovery page returned `200` with Phase 4 adapter content.

## Phase 5: Documentation, Examples, And Public Alpha Hardening

Parent issue: #35

Branch: `feature/p5-public-alpha-hardening`

Status: complete

Goal: harden docs, examples, tests, CI, and release workflows enough to support
the first public alpha release.

- [x] P5.1 Docs and API status polish (#36)
  - [x] Update README alpha status.
  - [x] Update installation docs.
  - [x] Update provider and adapter discovery docs.
  - [x] Keep non-goals explicit: no execution, no stable DSL, no real ecosystem
        adapters, no PyPI publication.
- [x] P5.2 Example workflow hardening (#37)
  - [x] Keep both tracked workflows public-safe.
  - [x] Add concise examples documentation page.
  - [x] Cover validate, inspect, and plan usage for both examples.
  - [x] Ensure examples remain included in package artifacts.
- [x] P5.3 CI and release-artifact hardening (#38)
  - [x] Keep release workflow artifact-only.
  - [x] Add artifact inspection tests or checks for sdist examples.
  - [x] Add artifact inspection tests or checks for wheel entry-point metadata.
  - [x] Preserve Python 3.11 and 3.12 CI coverage.
- [x] P5.4 Release notes and GitHub release preparation (#39)
  - [x] Update `RELEASE_NOTES.md` for Phase 0-4 implemented scope.
  - [x] Add documented release checklist for tag, workflow, artifacts, and
        GitHub release.
  - [x] Keep PyPI publication explicitly deferred.
  - [x] Ensure release title and tag target are documented.
- [x] P5.5 Phase closeout, tag, release, and verification (#40)
  - [x] Run local acceptance commands.
  - [x] Update roadmap and changelog closeout notes.
  - [x] Open and merge PR after green CI/docs.
  - [x] Verify live docs root, examples page, and release checklist page.
  - [x] Create and push tag `v0.1.0a1`.
  - [x] Verify release workflow passes.
  - [x] Create GitHub prerelease `FreshForge 0.1.0a1` with checked artifacts.

Phase 5 local verification passed with:

- `python -m pip install -e .[dev]`
- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`

Phase 5 artifact and CLI smoke verification also passed:

- inspected the sdist and confirmed both tracked example workflows are included;
- inspected the wheel metadata and confirmed the `freshforge.providers` fixture
  entry point;
- `freshforge providers --json` listed `freshforge.example` and
  `freshforge.fixture` with no diagnostics;
- `freshforge plan examples/ecosystem_adapter_workflow.yaml --json` produced a
  provider-aware non-executing plan using both providers.

Phase 5 merged to `main` through PR #41 at `d3ee05f`. GitHub CI passed on
Python 3.11 and 3.12, the Docs workflow deployed successfully, and the live docs
root, examples page, and release checklist page returned `200` with Phase 5
alpha-release content.

Phase 5 release closeout tagged `v0.1.0a1` at `43ed413`. The Release Artifacts
workflow passed, the downloaded workflow artifacts passed `twine check`, the
sdist included both tracked example workflows, and the wheel metadata included
the `freshforge.providers` fixture entry point. GitHub prerelease
`FreshForge 0.1.0a1` was created with the checked wheel and sdist artifacts.

## Phase 6: Local Workflow Run Runtime

Parent issue: #48

Branch: `feature/p6-workflow-run-runtime`

Status: complete

Goal: add FreshForge's first provider-native local workflow runner while keeping
domain work inside providers.

- [x] P6.1 Add run records and executable-provider protocol (#49)
  - [x] Add deterministic run-status and run-result records.
  - [x] Add provider-owned `ProviderRunResult`.
  - [x] Keep plan-only providers valid for validation and planning.
- [x] P6.2 Add serial local workflow runner (#50)
  - [x] Add `freshforge.execution.run_workflow(...)`.
  - [x] Execute nodes in deterministic plan order.
  - [x] Resolve relative artifact paths against the selected work directory.
  - [x] Stop on unsupported or failed node execution.
- [x] P6.3 Add CLI run command and JSON output (#51)
  - [x] Add `freshforge run WORKFLOW --json --workdir PATH`.
  - [x] Preserve the existing JSON envelope style.
- [x] P6.4 Add docs, examples, and tests (#52)
  - [x] Document run semantics, provider hooks, and deferred execution features.
  - [x] Test execution order, unsupported providers, failure stopping, workdir
        resolution, and CLI JSON.
- [x] P6.5 Verify, PR, deploy docs, and close phase (#53)
  - [x] Run local verification.
  - [x] Open PR and verify CI/docs.
  - [x] Confirm live docs after merge.

Acceptance boundary:

- May claim FreshForge has a first serial local runner for executable providers.
- Must not claim caching, checkpointing, parallel execution, remote execution,
  retries, shell-command nodes, stable workflow schema, or real ecosystem
  adapters.

## Current Next Steps

Phase 6 is complete: the first serial local workflow runner is merged, and the executable-provider
surface has been handed to Modelwright for the generated-model workflow lane.

Implementation evidence:

- Added run records in `freshforge.records`.
- Added `freshforge.execution.run_workflow(...)`, `RunContext`, and
  `artifact_paths(...)`.
- Added `freshforge run WORKFLOW --json --workdir PATH`.
- Added docs page `docs/workflow-runner.rst`.
- Added tests for serial execution order, unsupported providers, failure
  stopping, workdir resolution, and CLI JSON output.

Local verification:

- `.venv/bin/python -m ruff check .` passed.
- `.venv/bin/python -m pytest` passed with 65 tests.
- `.venv/bin/sphinx-build -b html docs _build/html -W` passed.
- `.venv/bin/python -m build` passed.
- `.venv/bin/twine check dist/*` passed.

Closeout evidence:

- Phase 6 PR #54 merged to `main`.
- PR checks passed on Python 3.11 and 3.12.
- Post-merge docs workflow passed and deployed the Phase 6 workflow-runner docs.
