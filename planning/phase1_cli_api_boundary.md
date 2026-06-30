# Phase 1 CLI And Python API Boundary Contract

This note records the intended CLI and Python API direction for FreshForge.
Phase 1 does not implement these commands beyond the existing Phase 0 CLI.

## CLI Principles

FreshForge CLI commands should be thin wrappers over importable Python APIs. The
CLI should be useful for automation, teaching, and agent-assisted workflows, but
the implementation should not live only inside Typer command handlers.

CLI output should default to readable text for humans and eventually support
structured JSON for automation where appropriate.

## Current Phase 0 CLI

The existing CLI remains:

```bash
freshforge --version
freshforge info
```

It should continue to describe FreshForge honestly as a scaffold until workflow
records and validation behavior exist.

## Future Command Groups

validate
   Load a workflow spec, validate structure, dependencies, provider references,
   artifacts, and provenance requirements, and emit diagnostics.

plan
   Produce a run plan without executing nodes. This should list node order,
   provider requirements, expected inputs/outputs, missing pieces, and warnings.

inspect
   Display workflow metadata, graph structure, provider references, artifacts,
   or run records.

providers
   List available providers and their node types after provider discovery exists.

run
   Execute a validated run plan. This is intentionally deferred until records,
   validation, planning, provenance, and artifact contracts are stable.

## Python API Layers

Future implementation should separate:

- records: dataclasses or typed models for workflows, nodes, diagnostics,
  provenance, artifacts, and run plans;
- loading: source parsing and normalization;
- validation: pure checks that produce diagnostics;
- planning: graph interpretation without execution;
- provider protocol: provider-owned metadata, validation, and execution hooks;
- CLI: presentation and argument parsing only.

## IO And Output Principles

- Validation and planning APIs should return structured results rather than
  printing directly.
- CLI commands should map nonzero exit codes to invalid or failed states.
- Diagnostics should include severity, code, message, and location where
  practical.
- JSON output should be stable enough for tests before it is advertised for
  external automation.

## Phase 2 And Phase 3 Implications

Phase 2 should implement records and validation APIs first. Phase 3 can add
provider protocols and planning behavior. The `run` command should remain
deferred until run records and provenance are credible.
