# FreshForge

`freshforge` is an early public-alpha Python package for workflow-as-code in open
forest resources and ecosystem services modelling.

FreshForge is intended to provide a small, neutral workflow layer for composing
open FRESH ecosystem tools as typed, version-controlled, executable graphs. The
long-term goal is to make forest modelling workflows easier to review, test,
rerun, publish, and adapt across projects that use tools such as FEMIC, FHOPS,
ws3, Modelwright, Nemora, and future FRESH packages.

FreshForge is pre-release alpha software. It implements provisional workflow
records, YAML/JSON loading, structural and provider-aware validation, explicit
provider registry support, Python entry-point provider discovery, workflow
inspection, non-executing run planning, and a first serial local runner for
provider-owned node execution. The `0.1.0a2` release is a GitHub alpha release
with checked artifacts, not a PyPI publication. FreshForge does not yet
implement a stable workflow DSL, caching, checkpointing, parallel execution,
remote execution, or real domain adapters.

Documentation: https://ubc-fresh.github.io/freshforge/

Repository: https://github.com/UBC-FRESH/freshforge

## Statement Of Need

Forest modelling workflows often live across scripts, spreadsheets, GIS model
builders, notebooks, command-line calls, consultant documentation, and tacit
project knowledge. That makes them hard to audit, rerun, compare, teach, or port
between computing environments.

FreshForge starts from a different premise: the durable source of truth should be
a declarative workflow graph and its provenance, not a GUI canvas or a one-off
script chain. GIS, optimization, spreadsheet conversion, simulation, reporting,
and publication steps should be composable as explicit nodes with typed inputs,
outputs, diagnostics, and verification records.

## Current Alpha Scope

Supported in `0.1.0a2`:

- Python package skeleton using `src/` layout;
- minimal `freshforge` command-line interface;
- strict roadmap, issue, changelog, and planning workflow;
- Phase 1 architecture contracts for workflow vocabulary, provider boundaries,
  and CLI/API direction;
- provisional Phase 2 YAML/JSON workflow loading, validation diagnostics, and
  non-executing run planning;
- Phase 3 explicit provider registry support, built-in example provider
  metadata, provider-aware diagnostics, and workflow inspection;
- Phase 4 Python entry-point provider discovery and a public-safe fixture
  adapter that proves the adapter packaging path;
- Phase 6 serial local workflow execution for providers that implement
  `run_node(...)`, including run records and work-directory-aware artifact
  path resolution;
- public-safe example workflow specs;
- Sphinx documentation;
- CI, documentation, and release-artifact workflows.

Not supported yet:

- stable workflow YAML/TOML/JSON schema;
- real FEMIC/FHOPS/ws3/Modelwright/Nemora provider adapters;
- caching, checkpointing, parallel execution, or remote execution;
- direct integration with FEMIC, FHOPS, ws3, Modelwright, Nemora, or GIS tools;
- PyPI publication.

Release artifacts are distributed through GitHub for this alpha. PyPI
publication is deferred to a later release phase.

## Install For Development

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Run the local checks:

```bash
python -m ruff check .
python -m pytest
sphinx-build -b html docs _build/html -W
python -m build
twine check dist/*
```

## Command Line

```bash
freshforge --version
freshforge info
freshforge providers
freshforge inspect examples/stand_treatment_workflow.yaml
freshforge inspect examples/ecosystem_adapter_workflow.yaml
freshforge validate examples/stand_treatment_workflow.yaml
freshforge validate examples/ecosystem_adapter_workflow.yaml
freshforge plan examples/stand_treatment_workflow.yaml
freshforge plan examples/ecosystem_adapter_workflow.yaml
freshforge run examples/stand_treatment_workflow.yaml --json
```

The CLI commands are thin wrappers over package APIs. They validate, inspect,
plan, and run executable provider nodes. Built-in example providers are
plan-only, so `freshforge run` reports an unsupported-execution diagnostic for
those examples.

## Roadmap

Near-term phases are tracked in `ROADMAP.md`:

- Phase 0: bootstrap package, governance, docs, and automation scaffold.
- Phase 1: architecture and workflow-language research.
- Phase 2: core workflow records and validation contracts.
- Phase 3: node provider API and execution-planning prototype.
- Phase 4: ecosystem adapter prototypes.
- Phase 5: documentation, examples, and public alpha hardening.
- Phase 6: serial local workflow run runtime.

Development follows the FRESH phase/task/subtask workflow:

- `ROADMAP.md` maps phases and tasks to GitHub issues.
- `CHANGE_LOG.md` records the dated project narrative.
- `planning/` stores focused design notes and decisions.
- One active phase generally maps to one parent issue and feature branch.
- Roadmap tasks map to child issues linked from the parent issue body.

## Public-Repo Hygiene

Do not commit private project data, raw chat transcripts, unpublished source
documents, generated local outputs, or machine-specific paths. Keep scratch
material under ignored local paths such as `tmp/`, `local/`, `data/private/`, or
`outputs/`.

Use GitHub issues for public bug reports, documentation issues, and feature
requests. Do not attach private project material to public issues.
