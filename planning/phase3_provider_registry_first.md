# Phase 3 Provider Registry First

Phase 3 adds a provider API without adding automatic plugin discovery. The goal
is to make provider metadata, diagnostics, CLI inspection, and non-executing run
plans concrete before FreshForge starts importing installed packages or domain
adapters.

## Accepted Direction

FreshForge core owns:

- provider reference parsing;
- provider and node-type metadata records;
- an explicit in-process provider registry;
- provider-aware validation diagnostics;
- provider-aware non-executing run-plan records;
- a built-in public-safe example provider for tests and docs.

Provider references use the final dotted component as the node type. For
example, `freshforge.example.load_inventory` resolves to provider ID
`freshforge.example` and node type `load_inventory`.

## Deferred Discovery

Python entry-point discovery is deferred. Phase 3 should not scan installed
packages, auto-import provider modules, or require a particular adapter packaging
pattern. The Phase 1 provider boundary keeps three later options open:

1. native provider modules inside domain packages;
2. thin companion packages such as `freshforge-femic`;
3. local project providers for one-off research workflows.

Deferring entry points keeps Phase 3 testable and public-safe while the provider
contract is still provisional.

## Non-Goals

Phase 3 does not add node execution, `freshforge run`, provider package
auto-import, caching, checkpoints, run records, artifact materialization, or
FRESH ecosystem adapters.
