Providers
=========

Phase 3 introduces FreshForge's first provider API. Phase 4 adds entry-point
discovery for provider adapters. Phase 6 adds optional provider-owned node
execution. Providers describe node types, validate provider-owned node
configuration, and may implement ``run_node(...)`` when they can execute a node.

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

Execution
---------

Executable providers implement ``run_node(node, node_type, context=...)`` and
return ``ProviderRunResult``. FreshForge's serial local runner calls those hooks
in deterministic plan order:

.. code-block:: bash

   freshforge run path/to/workflow.yaml --json

Plan-only providers remain valid for validation and planning. When a plan-only
provider is used with ``freshforge run``, FreshForge fails the run with
``node.execution.unsupported``.

Deferred Work
-------------

Phase 6 does not add caching, checkpoints, parallel execution, remote execution,
retries, shell-command nodes, or real FRESH ecosystem adapters.

Syntax Status
-------------

Provider syntax is alpha and provisional. Entry-point discovery is intended to
stabilize adapter packaging before FreshForge adds real domain adapters. CLI
JSON output is deterministic enough for the test suite, but it remains part of
the alpha API surface.
