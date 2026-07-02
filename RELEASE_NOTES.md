# Release Notes

## 0.1.0a4

FreshForge `0.1.0a4` is the run matrix alpha. It packages the Phase 8
orchestration milestone as a GitHub prerelease with checked source and wheel
artifacts. It is not published to PyPI.

### Implemented

- Everything from `0.1.0a3`.
- Generic workflow matrix records for explicit cases and Cartesian-product
  axes.
- Workflow-template expansion with `${matrix.*}` placeholders.
- Default matrix case namespaces such as `matrix-id/case-id`.
- Matrix planning and serial matrix execution APIs.
- `freshforge matrix expand`, `freshforge matrix plan`, and
  `freshforge matrix run` CLI commands.
- Public-safe matrix examples for repeated workflow-template expansion.

### Explicit Limitations

- Workflow and matrix syntax remain alpha and provisional.
- Matrix execution is serial.
- FreshForge matrices do not define domain scenario semantics, parameter
  meaning, validation meaning, or artifact interpretation.
- FreshForge does not implement caching, checkpointing, parallel execution,
  remote execution, retries, production scheduling, or real ecosystem adapters.
- FreshForge is not published to PyPI in this release.

### Verification

The release is expected to pass:

- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`
- `freshforge --version`
- `freshforge matrix --help`
- `freshforge matrix plan examples/run_matrix.yaml --json`

## 0.1.0a3

FreshForge `0.1.0a3` is the run namespace and workflow-run summary alpha. It
packages the post-runner orchestration milestone as a GitHub prerelease with
checked source and wheel artifacts. It is not published to PyPI.

### Implemented

- Everything from `0.1.0a2`.
- Optional run namespaces for `run_workflow(...)` and `freshforge run
  --namespace NAME`.
- Namespace-aware relative artifact path resolution under
  `workdir / namespace`.
- Compact `NodeRunSummary` and `WorkflowRunSummary` records.
- `WorkflowRunResult.summary()` for downstream tools that need status, node
  counts, diagnostic counts, and artifact paths without parsing full run
  payloads.
- `freshforge run --json` output that includes both full run records and compact
  summaries.

### Explicit Limitations

- Workflow syntax and JSON output remain alpha and provisional.
- FreshForge does not implement caching, checkpointing, parallel execution,
  remote execution, retries, run matrices, or real ecosystem adapters.
- Run namespaces are path prefixes for local artifacts, not a global run
  database or scheduling system.
- FreshForge is not published to PyPI in this release.

### Verification

The release is expected to pass:

- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`
- `freshforge --version`
- `freshforge run --help`

## 0.1.0a2

FreshForge `0.1.0a2` is the local workflow runner alpha. It packages
FreshForge's first serial local runner for provider-owned workflow nodes. It is
distributed as a GitHub prerelease with checked source and wheel artifacts. It
is not published to PyPI.

### Implemented

- Everything from `0.1.0a1`.
- Provider-native serial local workflow execution through
  `freshforge.execution.run_workflow(...)`.
- `freshforge run WORKFLOW --json --workdir PATH`.
- `ProviderRunResult`, per-node run records, workflow run records, and
  deterministic run status serialization.
- Work-directory-aware artifact path resolution through the run context.
- Clear unsupported-execution diagnostics when plan-only providers are run.

### Explicit Limitations

- Workflow syntax and JSON output remain alpha and provisional.
- FreshForge runs provider-owned nodes only; it does not execute arbitrary shell
  commands or import domain packages directly.
- FreshForge does not implement caching, checkpointing, parallel execution,
  remote execution, retries, run namespaces, run matrices, or real ecosystem
  adapters.
- FreshForge is not published to PyPI in this release.

### Verification

The release is expected to pass:

- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`
- `freshforge --version`
- `freshforge run --help`

## 0.1.0a1

FreshForge `0.1.0a1` is the first public alpha release. It is distributed as a
GitHub prerelease with checked source and wheel artifacts. It is not published to
PyPI.

### Implemented

- Package-backed Python project using `src/` layout and versioned package
  metadata.
- Typer CLI with `freshforge --version`, `info`, `providers`, `validate`,
  `inspect`, and `plan`.
- Provisional YAML/JSON workflow records for workflow metadata, nodes,
  dependencies, broad structured fields, diagnostics, and non-executing run
  plans.
- Structural validation for workflow IDs, node IDs, dependencies, graph cycles,
  and broad field shapes.
- Provider metadata records, provider reference parsing, explicit provider
  registry support, and provider-aware diagnostics.
- Python entry-point provider discovery through the `freshforge.providers`
  group.
- Built-in public-safe `freshforge.example` provider and entry-point-discovered
  `freshforge.fixture` provider.
- Public-safe example workflows:
  - `examples/stand_treatment_workflow.yaml`;
  - `examples/ecosystem_adapter_workflow.yaml`.
- Sphinx documentation, GitHub Pages deployment, CI, release-artifact workflow,
  roadmap, changelog, and public contribution/governance files.

### Explicit Limitations

- Workflow syntax is alpha and provisional.
- CLI JSON output is deterministic enough for tests but is not a stable external
  automation contract.
- FreshForge does not execute workflow nodes.
- FreshForge does not implement `freshforge run`.
- FreshForge does not read declared datasets, inspect artifact files, create
  workflow outputs, cache results, checkpoint runs, or write run records.
- FreshForge does not include real FEMIC, FHOPS, ws3, Modelwright, Nemora, GIS,
  optimization, or spreadsheet adapters.
- FreshForge is not published to PyPI in this release.

### Verification

The release is expected to pass:

- `python -m pip install -e .[dev]`
- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
- `python -m build`
- `twine check dist/*`

Release artifacts should include the tracked example workflow specs and the
`freshforge.providers` fixture entry-point metadata.
