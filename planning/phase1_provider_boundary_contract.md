# Phase 1 Provider Boundary Contract

This note defines how FreshForge should relate to FEMIC, FHOPS, ws3, Modelwright,
Nemora, and future ecosystem tools.

## Dependency Direction

FreshForge core should define workflow contracts and orchestration semantics.
Domain packages should provide domain-specific node implementations.

```text
freshforge core
        ^
        |
provider/adapters from domain packages or companion packages
        ^
        |
project recipes and instance workflows
```

FreshForge core must not directly import FEMIC, FHOPS, ws3, Modelwright, Nemora,
GIS desktop runtimes, optimization engines, spreadsheet tooling, or remote
execution frameworks during early phases.

## Core Responsibilities

FreshForge core may own:

- workflow and node records;
- validation and diagnostic records;
- provider reference syntax;
- run-plan records;
- provenance and artifact contracts;
- CLI/API surfaces for loading, validating, planning, and inspecting workflows;
- generic built-in providers needed for tests and examples.

## Domain Responsibilities

Domain packages or companion adapters should own:

- scientific and operational domain logic;
- package-specific configuration validation;
- runtime dependencies;
- external executable discovery;
- interpretation of domain-specific artifacts;
- domain-specific smoke tests and scientific validation.

For example, FEMIC should own FEMIC THLB/Patchworks semantics. Modelwright should
own spreadsheet conversion semantics. FreshForge should only understand that a
node refers to a provider and that the provider can expose validation/planning
metadata.

## Adapter Packaging Options

Three packaging patterns remain acceptable for later phases:

1. Native provider modules inside domain packages, such as `femic.freshforge`.
2. Thin companion packages, such as `freshforge-femic`.
3. Local project providers for one-off research workflows.

Phase 2 and Phase 3 should not require choosing exactly one. The core provider
reference model should allow all three.

## Phase 2 And Phase 3 Implications

Phase 2 should model provider references as strings plus metadata, not as direct
imports. Phase 3 can add provider discovery and provider protocol code after the
record model is stable.

Provider unavailability should be a first-class diagnostic, not a Python import
traceback exposed to users.

Provider implementations should be able to participate in validation and
planning before they execute expensive or stateful work.
