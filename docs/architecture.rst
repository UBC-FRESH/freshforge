Architecture
============

FreshForge is intended to become a neutral workflow core rather than a domain
package that imports every FRESH modelling tool. Phase 1 records the first
architecture contracts for that direction. Phase 2 adds provisional workflow
records, Phase 3 adds provider-aware validation and planning, Phase 4 adds
entry-point adapter discovery, and Phase 6 adds explicit provider-backed
execution.

Intended Dependency Direction
-----------------------------

.. code-block:: text

   freshforge core
           ^
           |
   domain package adapters and provider registrations
           ^
           |
   project recipes and instance workflows

Domain packages such as FEMIC, FHOPS, ws3, Modelwright, and Nemora should own
their own scientific logic. FreshForge should own shared workflow contracts,
validation, execution planning, provenance, and orchestration semantics.

Core Concepts
-------------

The Phase 1 vocabulary uses these terms:

``workflow``
   A version-controlled graph specification.

``node``
   A logical workflow step with a stable ID, provider reference, declared inputs,
   outputs, parameters, dependencies, and diagnostics.

``provider``
   A package-owned implementation surface that can describe and validate a node
   type, and may optionally execute that node type.

``artifact``
   A materialized file, dataset, model package, report, or other durable output.

``diagnostic``
   A structured message about invalid configuration, missing providers,
   unsupported features, uncertainty, or failed validation.

``run plan``
   A pre-execution interpretation of a workflow graph. It should explain node
   order, provider requirements, expected inputs and outputs, and missing pieces
   before any expensive or stateful work runs.

Source Format Direction
-----------------------

FreshForge should target text-backed author-authored workflow specs first. YAML
is the preferred starting point because it is readable for analysts and suited to
nested workflow records. JSON compatibility should remain possible for generated
records, tests, and machine interchange.

Phase 1 does not define final syntax. Phase 2 should create the smallest
round-trippable record model before adding a complete grammar.

Provider Boundary
-----------------

FreshForge core should model provider references and diagnostics without directly
importing domain packages. Domain packages or thin companion adapters should own
scientific logic, runtime dependencies, external executable discovery, and
domain-specific validation.

Acceptable future provider locations include native modules inside domain
packages, thin companion packages such as ``freshforge-femic``, and local project
providers for one-off research workflows.

Phase 4 proves the packaging path with Python entry points under the
``freshforge.providers`` group. FreshForge discovers provider factories from
installed packages, but it still does not import domain packages directly.

CLI And API Direction
---------------------

Future CLI command groups should be thin wrappers over Python APIs:

``validate``
   Validate workflow structure, dependencies, provider references, artifacts, and
   provenance requirements.

``plan``
   Produce a run plan without executing nodes.

``inspect``
   Display workflow metadata, graph structure, provider references, artifacts,
   or run records.

``providers``
   List registered providers and node types.

``run``
   Execute a validated run plan through provider-owned execution hooks.

Current Boundary
----------------

Phase 6 implements provisional workflow records, YAML/JSON loading, structural
and provider-aware validation, explicit provider registry support, entry-point
provider discovery, workflow inspection, provider-aware planning, and explicit
provider-backed execution.

FreshForge still does not implement cache or checkpoint semantics, artifact
materialization, parallel execution, or real ecosystem adapters.

Phase 1 Planning Records
------------------------

The detailed Phase 1 contracts live in:

* ``planning/phase1_workflow_language_survey.md``
* ``planning/phase1_workflow_architecture.md``
* ``planning/phase1_provider_boundary_contract.md``
* ``planning/phase1_cli_api_boundary.md``
