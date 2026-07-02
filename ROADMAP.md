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
| P8 Run matrices and scenario-grid workflow expansion | #56 | `feature/p8-run-matrices-scenario-grids` | Complete |
| P9 v0.1.0a2 local workflow runner GitHub alpha release | #57 | `feature/p9-v0.1.0a2-release` | Complete |
| P10 v0.1.0a3 run namespace and summary GitHub alpha release | #69 | `feature/p10-v0.1.0a3-release` | Complete |
| P11 v0.1.0a4 matrix runner GitHub alpha release | #81 | `feature/p11-v0.1.0a4-release` | Complete |
| P12 v0.1.0a5 PyPI alpha release | #87 | `feature/p12-v0.1.0a5-pypi-alpha-release` | Active |

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

FreshForge Phase 9 is complete: `v0.1.0a2` is tagged and published as a GitHub prerelease with
checked workflow-built artifacts attached, while PyPI publication remains deferred.

FreshForge's most recent CLEWs-C2020 orchestration work is complete:

- Phase 7 (#55): complete; added run namespaces and clearer workflow-run summaries so repeated local
  Modelwright/FABLE runs can be compared without artifact collisions.
- Phase 8 (#56): complete; added generic run-matrix and scenario-grid expansion now that FABLE
  Pyculator has concrete strategy-comparison and scenario-bundle examples.

Phase 7 child issues #63 through #67 and Phase 8 child issues #75 through #79 are complete. The
coordinated downstream sequence through FABLE Pyculator Phase 20 is now implemented.

Implementation evidence:

- Added `run_namespace` support to `freshforge.execution.run_workflow(...)` and `RunContext`.
- Added namespace validation with `run.namespace.invalid` diagnostics before node execution.
- Added compact `NodeRunSummary`, `WorkflowRunSummary`, and `WorkflowRunResult.summary()` records.
- Added `freshforge run WORKFLOW --namespace NAME` and JSON `summary` output.
- Updated workflow runner and workflow records docs.
- Added tests for default compatibility, namespace path resolution, invalid namespaces, summaries,
  and CLI JSON/human output.

Local verification:

- `.venv/bin/python -m ruff check .` passed.
- `.venv/bin/python -m pytest` passed with 73 tests.
- `.venv/bin/sphinx-build -b html docs _build/html -W` passed.
- `.venv/bin/python -m build` passed.
- `.venv/bin/twine check dist/*` passed.
- `git diff --check` passed.
- CLI namespace smoke test passed with namespace/summary output and expected plan-only provider
  unsupported diagnostic.

Closeout evidence:

- Phase 7 PR #68 merged to `main`.
- PR CI run 28544860414 passed on Python 3.11 and 3.12.
- Post-merge CI run 28544897942 passed on Python 3.11 and 3.12.
- Post-merge Docs run 28544897990 passed and deployed GitHub Pages.

## Phase 7: Run Namespaces And Workflow-Run Summaries

Parent issue: #55

Branch: `feature/p7-run-namespaces-summaries`

Status: complete

Goal: add run namespace support and clearer workflow-run summaries so repeated local runs can be
compared without artifact collisions.

- [x] P7.1 Define run namespace and summary contracts. Child issue: #63.
  - [x] Define namespace validation rules.
  - [x] Add compact run summary records.
- [x] P7.2 Add namespaced artifact path resolution. Child issue: #64.
  - [x] Add `run_namespace` to the run context.
  - [x] Prefix relative artifact paths with `workdir / namespace`.
  - [x] Keep absolute artifact paths unchanged.
- [x] P7.3 Add compact workflow-run summaries. Child issue: #65.
  - [x] Add `WorkflowRunResult.summary()`.
  - [x] Include node, diagnostic, and artifact counts.
- [x] P7.4 Update CLI, docs, and tests. Child issue: #66.
  - [x] Add `freshforge run --namespace`.
  - [x] Include `summary` in JSON run output.
  - [x] Update runner and record docs.
- [x] P7.5 Verify, PR, and close phase. Child issue: #67.
  - [x] Run full local verification.
  - [x] Open and merge PR after CI passes.
  - [x] Confirm post-merge CI and Docs workflows pass.

Downstream dependency: Modelwright Phase 35 and FABLE Pyculator Phase 18 should consume these
generic summaries/namespaces rather than inventing package-local collision-avoidance conventions.

Acceptance boundary:

- May organize repeated run artifacts and summarize run status.
- Must not add scenario-matrix expansion, caching, checkpointing, remote execution, retries, or
  Modelwright/FABLE domain semantics in this phase.

Local verification:

- `.venv/bin/python -m ruff check .` passed.
- `.venv/bin/python -m pytest` passed with 73 tests.
- `.venv/bin/sphinx-build -b html docs _build/html -W` passed.
- `.venv/bin/python -m build` passed.
- `.venv/bin/twine check dist/*` passed.
- `git diff --check` passed.
- `.venv/bin/freshforge run examples/stand_treatment_workflow.yaml --json --namespace smoke/demo`
  emitted `run_namespace` and `summary.run_namespace`; the run failed as expected because the sample
  provider is plan-only.

Closeout evidence:

- PR #68 merged to `main`.
- PR CI run 28544860414 passed on Python 3.11 and 3.12.
- Post-merge CI run 28544897942 passed on Python 3.11 and 3.12.
- Post-merge Docs run 28544897990 passed and deployed GitHub Pages.

## Phase 8: Run Matrices And Scenario-Grid Workflow Expansion

Parent issue: #56

Branch: `feature/p8-run-matrices-scenario-grids`

Status: complete

Goal: add generic workflow-template expansion across scenario grids once real CLEWs-C2020 examples
justify the interface.

- [x] P8.1 Define matrix document and expansion records. Child issue: #75.
  - [x] Add matrix specs, axes, cases, expanded cases, plan records, run records, and summaries.
  - [x] Export public matrix APIs.
- [x] P8.2 Add workflow-template expansion and namespace defaults. Child issue: #76.
  - [x] Support explicit cases and Cartesian-product axes.
  - [x] Substitute `${matrix.case_id}`, `${matrix.namespace}`, and matrix variables.
  - [x] Default namespaces to `{matrix_id}/{case_id}` and reuse namespace validation.
- [x] P8.3 Add matrix plan/run APIs and CLI. Child issue: #77.
  - [x] Add `plan_workflow_matrix(...)` and `run_workflow_matrix(...)`.
  - [x] Add `freshforge matrix expand`, `freshforge matrix plan`, and `freshforge matrix run`.
  - [x] Keep execution serial and add opt-in `--fail-fast`.
- [x] P8.4 Update docs, examples, and tests. Child issue: #78.
  - [x] Add public-safe matrix template and matrix example.
  - [x] Add run-matrix docs and update runner/record docs.
  - [x] Add unit and CLI coverage for matrix loading, expansion, planning, running, and diagnostics.
- [x] P8.5 Verify, PR, deploy docs, and close phase. Child issue: #79.
  - [x] Run full local verification.
  - [x] Open and merge PR after CI passes.
  - [x] Confirm post-merge CI and Docs workflows pass.

Dependency note: start this after FreshForge Phase 7 and after FABLE Pyculator Phase 18 provides real
strategy-comparison examples that justify the run-matrix interface.

Acceptance boundary:

- May provide generic matrix expansion primitives.
- Must leave scenario schemas, parameter mappings, and validation semantics in domain packages.

Implementation evidence:

- Added `freshforge.matrix` with typed matrix records and public helpers for loading, expanding,
  planning, and serially running matrix cases.
- Added template substitution for `${matrix.case_id}`, `${matrix.namespace}`, and explicit matrix
  variables, with diagnostics for missing placeholders, invalid matrix shapes, invalid namespaces,
  duplicate variables, and invalid expanded workflows.
- Added CLI commands for `freshforge matrix expand`, `freshforge matrix plan`, and
  `freshforge matrix run`.
- Added public-safe `examples/run_matrix.yaml` and `examples/matrix_workflow_template.yaml`.
- Added Sphinx documentation for run matrices and updated runner/record docs to explain the
  one-run, namespaced-run, and matrix-run distinction.

Local verification:

- `.venv/bin/python -m ruff check .` passed.
- `.venv/bin/python -m pytest` passed with 90 tests.
- `.venv/bin/sphinx-build -b html docs _build/html -W` passed.
- `.venv/bin/python -m build` passed.
- `.venv/bin/twine check dist/*` passed.
- `git diff --check` passed.

Closeout evidence:

- PR #80 merged to `main` at `a14cb2f`.
- PR CI run #28561438088 passed on Python 3.11 and 3.12.
- Post-merge CI run #28561466037 passed on Python 3.11 and 3.12.
- Post-merge Docs run #28561466089 passed and deployed GitHub Pages.

## Phase 9: v0.1.0a2 Local Workflow Runner GitHub Alpha Release

Parent issue: #57

Branch: `feature/p9-v0.1.0a2-release`

Status: complete

Goal: publish FreshForge `v0.1.0a2` as a GitHub prerelease that marks the Phase 6 serial local
workflow runner milestone.

- [x] P9.1 Bump version and release metadata (#58)
  - [x] Bump package and import metadata to `0.1.0a2`.
  - [x] Update version contract tests and CLI status text.
- [x] P9.2 Update release docs and notes (#59)
  - [x] Update release checklist, installation docs, README, docs roadmap, and release notes.
  - [x] Keep PyPI publication explicitly deferred.
- [x] P9.3 Verify release artifacts and smoke tests (#60)
  - [x] Run local quality, tests, docs, build, and twine checks.
  - [x] Smoke-test `freshforge --version` and `freshforge run --help`.
- [x] P9.4 Tag GitHub prerelease and close phase (#61)
  - [x] Open and merge release PR after CI passes.
  - [x] Tag `v0.1.0a2`.
  - [x] Verify tag release-artifact workflow.
  - [x] Create GitHub prerelease with checked artifacts attached.

Acceptance boundary:

- May claim FreshForge has a GitHub alpha release for its first provider-native serial local runner.
- Must not claim PyPI publication, stable workflow syntax, caching, checkpointing, parallel
  execution, remote execution, run matrices, or real ecosystem adapters.

Local verification:

- `.venv/bin/python -m ruff check .` passed.
- `.venv/bin/python -m pytest` passed with 65 tests.
- `.venv/bin/sphinx-build -b html docs _build/html -W` passed.
- `.venv/bin/python -m build` passed.
- `.venv/bin/twine check dist/*` passed.
- `.venv/bin/freshforge --version` reported `freshforge 0.1.0a2`.
- `.venv/bin/freshforge run --help` passed.

Closeout evidence:

- Phase 9 PR #62 merged to `main` at `1413609`.
- Post-merge CI run #28539847114 passed on Python 3.11 and 3.12.
- Post-merge Docs run #28539847111 passed and deployed.
- Annotated tag `v0.1.0a2` was pushed.
- Tag-triggered Release Artifacts workflow #28539893525 passed.
- Downloaded workflow-built artifacts passed `twine check`.
- GitHub prerelease `FreshForge 0.1.0a2` was created with the checked wheel and sdist attached.

## Phase 10: v0.1.0a3 Run Namespace And Summary GitHub Alpha Release

Parent issue: #69

Branch: `feature/p10-v0.1.0a3-release`

Status: complete

Goal: publish FreshForge `v0.1.0a3` as a GitHub prerelease that marks the Phase 7 run namespace and
compact workflow-run summary milestone.

- [x] P10.1 Bump FreshForge version and release metadata (#70)
  - [x] Bump package and import metadata to `0.1.0a3`.
  - [x] Update version contract tests, provider metadata versions, and CLI status text.
- [x] P10.2 Update FreshForge release docs and notes (#71)
  - [x] Update release checklist, installation docs, README, docs roadmap, and release notes.
  - [x] Keep PyPI publication explicitly deferred.
- [x] P10.3 Verify FreshForge release artifacts and smoke tests (#72)
  - [x] Run local quality, tests, docs, build, and twine checks.
  - [x] Smoke-test `freshforge --version` and `freshforge run --help`.
- [x] P10.4 Tag GitHub prerelease and close phase (#73)
  - [x] Open and merge release PR after CI passes.
  - [x] Tag `v0.1.0a3`.
  - [x] Verify tag release-artifact workflow.
  - [x] Create GitHub prerelease with checked artifacts attached.

Acceptance boundary:

- May claim FreshForge has a GitHub alpha release for run namespaces and compact workflow-run
  summaries.
- Must not claim PyPI publication, stable workflow syntax, caching, checkpointing, parallel
  execution, remote execution, run matrices, or real ecosystem adapters.

Local verification:

- `.venv/bin/python -m ruff check .` passed.
- `.venv/bin/python -m pytest` passed with 73 tests.
- `.venv/bin/sphinx-build -b html docs _build/html -W` passed.
- `.venv/bin/python -m build` passed.
- `.venv/bin/twine check dist/*` passed.
- `.venv/bin/freshforge --version` reported `freshforge 0.1.0a3`.
- `.venv/bin/freshforge run --help` passed.

Closeout evidence:

- Phase 10 PR #74 merged to `main` at `4a64551`.
- Post-merge CI run #28559392850 passed on Python 3.11 and 3.12.
- Post-merge Docs run #28559392858 passed and deployed.
- Annotated tag `v0.1.0a3` was pushed.
- Tag-triggered Release Artifacts workflow #28559427242 passed.
- GitHub prerelease `FreshForge 0.1.0a3` was created with the checked wheel and sdist attached.
- Clean tag install smoke test reported `freshforge 0.1.0a3` and `freshforge run --help` passed.

## Phase 11: v0.1.0a4 Matrix Runner GitHub Alpha Release

Parent issue: #81

Branch: `feature/p11-v0.1.0a4-release`

Status: complete

Goal: publish FreshForge `v0.1.0a4` as a GitHub prerelease that marks the Phase 8 generic run matrix
milestone while keeping PyPI publication deferred.

- [x] P11.1 Bump version and release metadata (#82)
  - [x] Bump package and import metadata to `0.1.0a4`.
  - [x] Update version contract tests, provider metadata versions, and CLI status text.
- [x] P11.2 Update release docs, notes, and alpha boundary language (#83)
  - [x] Update release checklist, installation docs, README, docs roadmap, and release notes.
  - [x] Keep PyPI publication explicitly deferred.
- [x] P11.3 Verify artifacts, tag, and publish GitHub prerelease (#84)
  - [x] Run local quality, tests, docs, build, and twine checks.
  - [x] Smoke-test `freshforge --version`, `freshforge matrix --help`, and matrix planning.
  - [x] Tag `v0.1.0a4`.
  - [x] Verify tag release-artifact workflow.
  - [x] Create GitHub prerelease with checked artifacts attached.
- [x] P11.4 PR, docs deploy, and close phase (#85)
  - [x] Open and merge release PR after CI passes.
  - [x] Confirm post-merge CI and Docs workflows.
  - [x] Update roadmap and changelog closeout evidence.

Acceptance boundary:

- May claim FreshForge has a GitHub alpha release for generic run matrix expansion, planning, and
  serial execution.
- Must not claim PyPI publication, stable workflow or matrix syntax, caching, checkpointing,
  parallel execution, remote execution, retries, production scheduling, or real ecosystem adapters.

Local verification:

- `.venv/bin/python -m pip install -e .[dev]` refreshed editable metadata for `0.1.0a4`.
- `.venv/bin/python -m ruff check .` passed.
- `.venv/bin/python -m pytest` passed with 90 tests.
- `.venv/bin/sphinx-build -b html docs _build/html -W` passed.
- `.venv/bin/python -m build` passed.
- `.venv/bin/twine check dist/*` passed.
- `.venv/bin/freshforge --version` reported `freshforge 0.1.0a4`.
- `.venv/bin/freshforge matrix --help` passed.
- `.venv/bin/freshforge matrix plan examples/run_matrix.yaml --json` passed.
- `git diff --check` passed.

Closeout evidence:

- Phase 11 PR #86 merged to `main` at `17d6570`.
- Post-merge CI run #28562671869 passed on Python 3.11 and 3.12.
- Post-merge Docs run #28562671834 passed and deployed.
- Annotated tag `v0.1.0a4` was pushed.
- Tag-triggered Release Artifacts workflow #28562704658 passed.
- Downloaded workflow-built artifacts passed `twine check`.
- Clean wheel install smoke test reported `freshforge 0.1.0a4` and `freshforge matrix --help` passed.
- GitHub prerelease `FreshForge 0.1.0a4` was created with the checked wheel and sdist attached.

## Phase 12: v0.1.0a5 PyPI Alpha Release

Parent issue: #87

Branch: `feature/p12-v0.1.0a5-pypi-alpha-release`

Status: active

Goal: publish FreshForge `v0.1.0a5` as the first PyPI alpha release while preserving the current
Phase 8 feature surface: validation, inspection, planning, serial local runs, run namespaces,
compact run summaries, and matrices.

- [x] P12.1 Version and release metadata (#88)
  - [x] Bump package and import metadata to `0.1.0a5`.
  - [x] Update built-in provider metadata versions and CLI status text.
  - [x] Update release-contract tests.
- [x] P12.2 PyPI trusted-publishing workflow (#89)
  - [x] Preserve release artifact build/check/upload behavior.
  - [x] Add tag-triggered PyPI trusted-publishing job using environment `pypi`.
  - [x] Record first-publish trusted-publisher gate.
- [x] P12.3 Installation docs and downstream guidance (#90)
  - [x] Update README, installation docs, release checklist, docs roadmap, and release notes.
  - [x] Document `python -m pip install freshforge==0.1.0a5`.
  - [x] Keep alpha boundaries explicit.
- [x] P12.4 Verification and release candidate checks (#91)
  - [x] Run local quality, tests, docs, build, and twine checks.
  - [x] Smoke-test `freshforge --version`, `freshforge run --help`, and `freshforge matrix --help`.
  - [x] Run `git diff --check`.
- [ ] P12.5 Tag, publish, verify, and close phase (#92)
  - [ ] Open and merge release PR after CI passes.
  - [ ] Confirm PyPI trusted publisher is configured for project `freshforge`, repository
        `UBC-FRESH/freshforge`, workflow `release.yml`, and environment `pypi`.
  - [ ] Tag `v0.1.0a5`.
  - [ ] Verify tag release workflow publishes to PyPI.
  - [ ] Create GitHub prerelease with checked artifacts attached.
  - [ ] Verify clean PyPI install.
  - [ ] Close child issues and parent issue.

Acceptance boundary:

- May claim FreshForge has a PyPI alpha release once the tag workflow publishes successfully.
- Must not claim stable workflow or matrix syntax, stable provider APIs, caching, checkpointing,
  parallel execution, remote execution, retries, production scheduling, or real ecosystem adapters.

Publish gate:

- Do not tag until the maintainer confirms the PyPI trusted publisher is configured for the
  `freshforge` project with repository `UBC-FRESH/freshforge`, workflow `release.yml`, and
  environment `pypi`.

Local verification:

- `.venv/bin/python -m pip install -e .[dev]` refreshed editable metadata for `0.1.0a5`.
- `.venv/bin/python -m ruff check .` passed.
- `.venv/bin/python -m pytest` passed with 90 tests.
- `.venv/bin/sphinx-build -b html docs _build/html -W` passed.
- `.venv/bin/python -m build` passed.
- `.venv/bin/twine check dist/*` passed.
- `.venv/bin/freshforge --version` reported `freshforge 0.1.0a5`.
- `.venv/bin/freshforge run --help` passed.
- `.venv/bin/freshforge matrix --help` passed.
- `git diff --check` passed.
