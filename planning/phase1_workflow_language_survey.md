# Phase 1 Workflow-Language Survey

This note records the Phase 1 design survey for FreshForge. It is intentionally
pragmatic: the goal is to identify useful patterns, not to copy another workflow
system wholesale.

## Design Pressure

FreshForge workflows must be readable by researchers, reviewable in Git,
portable across operating systems, and usable by coding agents. Forest modelling
workflows also need stronger provenance than many general task runners provide:
the source of every dataset, rule, node implementation, parameter, artifact, and
validation result matters.

The durable object should be the workflow specification and its run evidence, not
a GUI canvas, notebook state, or terminal transcript.

## Relevant Patterns

Declarative DAG systems
   Useful for explicit dependencies, repeatability, validation before execution,
   and workflow visualization. FreshForge should adopt explicit node IDs,
   dependency relationships, and validation-before-run behavior.

Scientific workflow systems
   Useful for separating workflow definition from execution backend. FreshForge
   should eventually support local, batch, and remote execution modes without
   changing author-authored recipes.

Infrastructure-as-code
   Useful for plan-first behavior: inspect what will change before executing.
   FreshForge should have a future run-planning surface that can explain nodes,
   inputs, providers, artifacts, and missing requirements before execution.

GIS graphical model builders
   Useful as proof that analysts need composable spatial-processing workflows.
   FreshForge should not make a GUI model the source of truth; any GUI should
   edit or inspect text-backed workflow records.

Rule and decision graphs
   Useful for stand-level treatment logic, THLB netdown recipes, and management
   decision processes. FreshForge should allow decision/rule-like nodes without
   forcing all workflows to look like file-processing pipelines.

Notebook workflows
   Useful for exploration and teaching, but weak as durable workflow contracts.
   FreshForge should interoperate with notebooks later while keeping specs,
   plans, and run records in version-controlled files.

## Accepted Principles

- Prefer author-authored declarative specs over generated opaque scripts.
- Validate structure, dependencies, provider availability, and provenance before
  execution.
- Keep workflow specs small enough to review in pull requests.
- Keep domain logic in provider packages rather than embedding forest science in
  the workflow core.
- Treat artifacts as declared inputs and outputs, not incidental files.
- Preserve diagnostics and uncertainty instead of silently coercing invalid
  workflow states.
- Keep GUI, notebook, CLI, and web interfaces optional frontends.

## Anti-Patterns

- Treating a GUI canvas as the only authoritative workflow representation.
- Turning FreshForge into a meta-package that imports every FRESH modelling
  package.
- Encoding domain science as stringly typed command snippets in workflow specs.
- Treating successful process exit as sufficient validation of scientific
  output.
- Adding a distributed execution backend before local contracts are stable.

## Deferred Features

- Parallel and remote execution.
- Caching, checkpointing, and artifact stores.
- GUI editors and visualization.
- Rich rule-engine syntax.
- Plugin discovery implementation.
- Formal JSON Schema or Pydantic validation.

These features should be designed after Phase 2 establishes the first workflow
records and validation contract.
