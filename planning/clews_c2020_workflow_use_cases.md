# CLEWs-C2020 Workflow Use-Case Pool

Date: 2026-07-01

Purpose: collect plausible FreshForge use cases from an active, complex, multi-year, multi-institution,
multi-disciplinary modelling collaboration. These notes should inform future FreshForge phase scoping,
provider vocabulary, examples, and documentation, but they are not current capability claims.

## Context

The CLEWs-C2020 modelling space spans linked climate, land, energy, water, agriculture, and forestry
questions. The practical workflow is not one model. It is a chain of workbook conversion, generated
Python models, notebooks, scenario assumptions, validation reports, forestry/agriculture/energy
intermediate products, and publication/reporting outputs.

FreshForge is useful here if it can make those steps explicit, runnable, inspectable, and repeatable
without forcing every domain package to depend on every other package.

## Near-Term Concrete Examples

- FABLE Calculator workbook -> Modelwright generated Python model -> FABLE Pyculator notebook outputs.
- FABLE land-use and agriculture scenario assumptions -> downstream forestry biomass supply
  assumptions.
- Forest inventory and treatment scenarios -> FEMIC feedstock curves -> energy-system model inputs.
- FABLE crop, land, water, and GHG outputs -> CLEWs reporting tables and figures.
- Bioenergy demand assumptions -> land-use pressure scenarios -> regenerated FABLE runs.
- Shared scenario bundles, such as SSP1, SSP2, and SSP3, flowing through agriculture, forestry, and
  energy model nodes with consistent assumptions.
- Validation workflows that compare generated Python model outputs against source workbook outputs
  before results are interpreted.
- Reproducible run books for each modelling experiment: derive inputs, run model nodes, collect
  outputs, validate, and render reports.
- Cross-model sensitivity sweeps where one parameter set fans out across FABLE, forestry, and energy
  calculations.
- Publication-ready audit trails showing which source workbook, generated model, scenario settings,
  and validation report produced each figure or table.

## Workflow Pattern Candidates

### Workbook-To-Notebook Build

Use FABLE Pyculator to derive FABLE-specific output refs, Modelwright to infer/generate/execute the
Python model, and FreshForge to orchestrate the build and validation artifacts.

Potential node families:

- workbook surface discovery;
- output-ref derivation;
- contract inference;
- model generation;
- model execution;
- cached workbook validation;
- notebook/report rendering.

### Cross-Domain Scenario Propagation

Represent shared scenario settings once, then route those assumptions into agriculture, forestry, and
energy workflow nodes.

Potential node families:

- scenario bundle declaration;
- scenario parameter mapping;
- unit and naming harmonization;
- model-specific input materialization;
- cross-model consistency checks.

### Forestry-Agriculture-Energy Coupling

Link land-use or crop outputs to forestry feedstock and energy-system assumptions while preserving
intermediate artifacts.

Potential node families:

- FABLE land/agriculture outputs;
- forestry inventory/treatment scenario generation;
- FEMIC feedstock curve generation;
- bioenergy demand/input table materialization;
- downstream energy model handoff.

### Validation And Audit Trail

Make validation evidence a first-class workflow product, not an afterthought.

Potential node families:

- source artifact checksum;
- generated artifact manifest;
- cached-output comparison;
- scenario-output comparison;
- mismatch taxonomy;
- figure/table provenance manifest.

### Sensitivity And Ensemble Runs

Run the same declared workflow over a scenario grid and preserve comparable outputs from each run.

Potential node families:

- parameter grid definition;
- run matrix expansion;
- per-run artifact namespace;
- result aggregation;
- scenario comparison plots/tables.

## FreshForge Design Implications

- Providers should stay domain-owned. FreshForge should orchestrate; FABLE Pyculator, Modelwright,
  FEMIC, and future energy-model packages should own domain-specific interpretation.
- Workflow records need clear artifact provenance, because source workbooks, generated models,
  validation reports, and rendered figures all have different trust boundaries.
- Scenario bundles and parameter mappings may become first-class concepts, but they should be
  introduced only after concrete examples prove the right shape.
- Run output should remain machine-readable enough for notebooks, dashboards, and CI checks.
- Validation status should travel with outputs so downstream users can distinguish "ran" from
  "validated".
- Relative artifact paths and per-run namespaces matter for long experiments with many scenarios.

## Coordinated Post-Alpha Roadmap Chain

The first CLEWs-C2020 workflow-automation release train is now published:

- FreshForge `v0.1.0a2`: serial local workflow runner.
- Modelwright `v0.1.0a7`: generated-model materialization and executable FreshForge provider support.
- FABLE Pyculator `v0.1.0a2`: FABLE workflow automation helpers, scenario bundles, and validation
  evidence packaging.

The current post-alpha work is proceeding in dependency order:

1. FreshForge Phase 7: add run namespaces and clearer workflow-run summaries.
2. Modelwright Phase 35: expose generated-model workflow summaries and provider diagnostics.
3. Modelwright Phase 36: extract compact validation evidence for downstream automation.
4. FABLE Pyculator Phase 18: compare output-ref strategies using those summaries.
5. FreshForge Phase 8: add generic run matrices now that FABLE strategy and scenario examples exist.
6. FABLE Pyculator Phase 19: orchestrate scenario bundles through FreshForge summaries/namespaces.
7. FABLE Pyculator Phase 20: upgrade opt-in benchmark workflows with sanitized evidence packaging.

Phase 7 preceded Phase 8 because repeated strategy and scenario runs need a collision-free artifact
namespace and compact run summary before matrix expansion multiplies local artifacts. Phase 8 should
still avoid Modelwright/FABLE domain semantics: matrices are generic expansion primitives, not a
scenario schema.

## Deferred Questions

- What is the smallest useful scenario-bundle schema that works across FABLE, forestry, and energy
  model nodes?
- Should FreshForge core learn about run matrices, or should a provider/package expand scenario grids
  into plain workflow specs?
- How should cross-model unit conversion and naming harmonization be represented without making
  FreshForge domain-specific?
- What provenance metadata is required for a publication-quality figure or table?
- Which CLEWs-C2020 workflow slice is small enough to become the first public cross-domain example?

## Non-Claims

These examples do not mean FreshForge currently supports all CLEWs-C2020 orchestration needs. They
are planning inputs for future phases. Each candidate workflow needs a scoped phase, provider
contract, tests, documentation, and validation evidence before it becomes a supported capability.
