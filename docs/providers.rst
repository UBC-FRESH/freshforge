Providers
=========

Phase 3 introduces FreshForge's first provider API. Phase 4 adds entry-point
discovery for provider adapters. Providers are still non-executing. They
describe node types, validate provider-owned node configuration, and let run
plans explain what would run before any domain tool is called.

Provider References
-------------------

Workflow nodes keep provider references as strings:

.. code-block:: yaml

   nodes:
     - id: load_inventory
       provider: freshforge.example.load_inventory

FreshForge interprets the final dotted component as the node type. In this
example, ``freshforge.example`` is the provider ID and ``load_inventory`` is the
node type.

Registry Behavior
-----------------

FreshForge supports explicit in-process provider registration. The default
registry includes the built-in ``freshforge.example`` provider and discovers
installed provider entry points from the ``freshforge.providers`` group.

FreshForge reports provider problems as diagnostics:

* invalid provider reference syntax;
* provider namespace not registered;
* node type not defined by the provider;
* provider-declared input or output keys missing from a node.

The registry does not import FRESH ecosystem tools directly or call external
runtimes. Entry-point discovery loads only provider factories advertised by
installed packages.

CLI Examples
------------

.. code-block:: bash

   freshforge providers
   freshforge providers --json
   freshforge inspect examples/stand_treatment_workflow.yaml
   freshforge inspect examples/stand_treatment_workflow.yaml --json
   freshforge inspect examples/ecosystem_adapter_workflow.yaml
   freshforge validate examples/stand_treatment_workflow.yaml
   freshforge validate examples/ecosystem_adapter_workflow.yaml
   freshforge plan examples/stand_treatment_workflow.yaml
   freshforge plan examples/ecosystem_adapter_workflow.yaml

Planning remains non-executing. A run plan includes node order, provider ID,
node type, declared dependencies, and provider availability. It does not create
files, inspect artifacts, or execute provider code beyond validation hooks.

Deferred Work
-------------

Phase 4 does not add ``freshforge run``, node execution, artifact
materialization, caching, checkpoints, run records, or real FRESH ecosystem
adapters.

Syntax Status
-------------

Provider syntax is alpha and provisional. Entry-point discovery is intended to
stabilize adapter packaging before FreshForge adds real domain adapters.
