Workflow Records
================

Phase 2 introduces FreshForge's first provisional workflow records. Phase 3 adds
provider-aware validation and planning while keeping the records themselves
declarative. Phase 6 adds serial local execution through provider-owned
``run_node`` hooks.

Minimal Shape
-------------

Author-authored workflow specs may be YAML or JSON. YAML is the preferred human
authoring format for now.

.. code-block:: yaml

   workflow:
     id: stand_treatment_demo
     name: Stand treatment demonstration workflow
   nodes:
     - id: load_inventory
       provider: freshforge.example.load_inventory
       outputs:
         inventory: stand_inventory
     - id: classify_fuel
       provider: freshforge.example.classify_fuel
       needs:
         - load_inventory

The top-level ``workflow`` mapping requires ``id`` and may include ``name`` and
``description``. The top-level ``nodes`` list contains node mappings. Each node
requires ``id`` and ``provider``.

Node Fields
-----------

Optional node fields are intentionally broad in Phase 2:

``name`` and ``description``
   Human-readable metadata.

``needs``
   List of upstream node IDs.

``inputs``, ``outputs``, ``parameters``, and ``provenance``
   Generic mappings.

``artifacts``
   Generic mapping or list.

Validation
----------

Validation checks broad structural correctness:

* loaded source is a mapping;
* workflow ID and node IDs are required, unique, and slug-like;
* provider references are required;
* dependencies reference existing nodes;
* the dependency graph is acyclic;
* structured fields have the expected broad shape.

Diagnostics include severity, code, message, and optional location.

Phase 3 also checks provider references against the explicit default registry
when callers use provider-aware validation. Provider-aware diagnostics cover
invalid reference syntax, unavailable providers, unknown node types, and
provider-declared missing input or output keys.

Planning
--------

Planning produces a deterministic topological order for validated nodes. Phase 3
run plans include provider ID, node type, declared dependencies, and provider
availability. Planning does not execute nodes, inspect artifacts, create files,
auto-discover providers, or call external runtimes.

Execution uses the planned order but remains separate from planning. See
:doc:`workflow-runner` for the Phase 6 runner.

CLI Examples
------------

.. code-block:: bash

   freshforge validate examples/stand_treatment_workflow.yaml
   freshforge validate examples/stand_treatment_workflow.yaml --json
   freshforge inspect examples/stand_treatment_workflow.yaml
   freshforge inspect examples/stand_treatment_workflow.yaml --json
   freshforge plan examples/stand_treatment_workflow.yaml
   freshforge plan examples/stand_treatment_workflow.yaml --json
   freshforge run examples/stand_treatment_workflow.yaml --json

Syntax Status
-------------

The workflow shape is alpha and provisional. Future phases may refine the syntax
after provider protocols, planning, provenance, and examples mature.
