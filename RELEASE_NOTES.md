# Release Notes

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
