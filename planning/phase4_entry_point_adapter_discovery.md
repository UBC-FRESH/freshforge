# Phase 4 Entry-Point Adapter Discovery

Phase 4 adds Python entry-point discovery for FreshForge providers. The goal is
to prove the adapter packaging path before adding real FRESH ecosystem adapters.

## Accepted Direction

Provider packages can expose provider factories through the
`freshforge.providers` entry-point group. A provider entry point must load to a
callable factory that returns an object with `metadata()` and `validate_node()`.

FreshForge core owns:

- entry-point discovery mechanics;
- discovery diagnostics;
- duplicate-provider handling;
- explicit registry registration;
- CLI use of the default registry with discovery enabled.

FreshForge core still does not own domain semantics, external executable
discovery, dataset interpretation, or scientific validation.

## Fixture Adapter

FreshForge ships a public-safe fixture adapter under provider ID
`freshforge.fixture`. It is registered through FreshForge's own entry-point
metadata so tests and docs exercise the same discovery path that later companion
packages or native domain packages would use.

The fixture adapter declares FRESH-flavoured node types, but it does not read
data, inspect artifacts, execute tools, or represent real FEMIC, FHOPS, ws3,
Modelwright, or Nemora behavior.

## Deferred Work

Real ecosystem adapters remain deferred. Later phases can decide whether each
adapter should live inside a domain package, in a thin companion package, or in a
local project package. Phase 4 keeps all three packaging patterns open.

Phase 4 also defers `freshforge run`, execution hooks, caching, checkpoints,
artifact materialization, and run records.
