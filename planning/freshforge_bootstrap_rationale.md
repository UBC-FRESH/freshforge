# FreshForge Bootstrap Rationale

This note records the cleaned public rationale behind the FreshForge bootstrap.
It intentionally avoids raw chat transcripts and private project details.

## Problem

Forest modelling workflows are often expressed through GUI model builders,
project-specific scripts, spreadsheets, notebooks, ad hoc command sequences, and
consultant documentation. Those representations are hard to review, diff, test,
rerun, publish, or port across operating systems and compute environments.

ArcGIS ModelBuilder and QGIS Graphical Modeler are useful interfaces, but the
GUI canvas should not be the durable source of truth for open scientific
workflows. The durable source should be a declarative graph, its node contracts,
its inputs and outputs, its provenance, and its validation evidence.

## FreshForge Direction

FreshForge should become a small workflow-as-code layer for open forest
resources and ecosystem services modelling. The core package should focus on
workflow graph specifications, typed node interfaces, validation, diagnostics,
execution planning, provenance, run records, and adapter boundaries.

The initial scaffold does not implement those features. Phase 0 only creates the
package, governance, documentation, testing, and automation foundation needed to
develop them cleanly.

## Ecosystem Boundary

FreshForge should not be a god package that imports every FRESH modelling tool.
The intended dependency direction is:

```text
freshforge core
        ^
        |
domain package adapters and provider registrations
        ^
        |
project recipes and instance workflows
```

FEMIC, FHOPS, ws3, Modelwright, Nemora, and other tools should own their domain
science. FreshForge should own the shared workflow contracts and orchestration
semantics.

## Early Non-Goals

- No workflow DSL in Phase 0.
- No graph executor in Phase 0.
- No provider registry in Phase 0.
- No direct dependency on FEMIC, FHOPS, ws3, Modelwright, Nemora, GIS desktop
  software, or commercial runtimes.
- No PyPI publication until a later release phase records readiness evidence.
