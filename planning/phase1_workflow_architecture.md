# Phase 1 Workflow Architecture Contract

This note defines the Phase 1 architecture vocabulary and schema direction for
FreshForge. It is a contract for later implementation, not an implementation.

## Core Vocabulary

Workflow
   A named, version-controlled specification describing a graph of nodes, their
   dependencies, parameters, expected artifacts, and provenance requirements.

Node
   A single logical workflow step with a stable ID, provider reference, declared
   inputs, declared outputs, parameters, dependencies, and diagnostics.

Provider
   A package-owned implementation surface that can validate and eventually run a
   node type. Providers belong to FreshForge core only for built-in generic
   behavior; domain providers should live in domain packages or thin companion
   adapter packages.

Input
   A declared value, dataset, artifact, parameter, or upstream node output needed
   by a node.

Output
   A declared value, dataset, artifact, report, or runtime signal produced by a
   node.

Dependency
   A graph relationship showing that one node needs another node's declared
   output or completion state.

Parameter
   A user-authored node setting that changes behavior but is not itself a
   workflow dependency.

Artifact
   A materialized file, directory, dataset, database table, model package,
   report, or other durable output that can be checked, published, or consumed
   by later nodes.

Diagnostic
   A structured message explaining invalid configuration, missing providers,
   unsupported features, uncertainty, failed checks, or deferred behavior.

Provenance
   Structured evidence about source data, node implementation versions,
   commands, environments, assumptions, validations, and outputs.

Run plan
   A pre-execution interpretation of a workflow graph: node order, provider
   requirements, expected inputs/outputs, missing pieces, and validation
   diagnostics.

## Source Format Direction

Phase 2 should target a text-backed authoring format first. YAML is the
preferred starting point because it is readable for analysts and good for nested
workflow records. JSON compatibility should remain possible for generated
records, tests, and machine interchange. TOML can be revisited if workflows
remain shallow, but it is not the initial direction.

Phase 1 does not define final syntax. Phase 2 should create the smallest
round-trippable record model before adding a complete grammar.

## Minimum Phase 2 Target

Phase 2 should implement records and validation for:

- workflow metadata;
- node IDs and provider references;
- node dependencies;
- inputs, outputs, and parameters as structured mappings;
- diagnostics with severity and message;
- provenance placeholders;
- run-plan records that can be produced without executing nodes.

Phase 2 should also add a small public-safe example workflow that validates and
plans without requiring any external forest modelling package.

## Explicit Non-Goals

- No execution engine until validation and planning records are stable.
- No cache/checkpoint behavior before artifacts and provenance are defined.
- No domain-provider import in FreshForge core.
- No GUI contract until text-backed records are stable.
- No promise of stable public workflow syntax before the first alpha release
  explicitly declares it.
