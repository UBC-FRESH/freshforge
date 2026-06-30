Providers
=========

Phase 3 introduces FreshForge's first provider API. Providers are still
non-executing. They describe node types, validate provider-owned node
configuration, and let run plans explain what would run before any domain tool is
called.

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

Phase 3 uses an explicit in-process provider registry. The default registry
contains only the built-in ``freshforge.example`` provider used by public docs
and tests.

FreshForge reports provider problems as diagnostics:

* invalid provider reference syntax;
* provider namespace not registered;
* node type not defined by the provider;
* provider-declared input or output keys missing from a node.

The registry does not import installed packages, scan entry points, import FRESH
ecosystem tools, or call external runtimes.

CLI Examples
------------

.. code-block:: bash

   freshforge providers
   freshforge providers --json
   freshforge inspect examples/stand_treatment_workflow.yaml
   freshforge inspect examples/stand_treatment_workflow.yaml --json
   freshforge validate examples/stand_treatment_workflow.yaml
   freshforge plan examples/stand_treatment_workflow.yaml

Planning remains non-executing. A run plan includes node order, provider ID,
node type, declared dependencies, and provider availability. It does not create
files, inspect artifacts, or execute provider code beyond validation hooks.

Deferred Work
-------------

Phase 3 does not add ``freshforge run``, Python entry-point provider discovery,
provider package auto-import, caching, checkpoints, run records, artifact
materialization, or FRESH ecosystem adapters.

Syntax Status
-------------

Provider syntax is alpha and provisional. The explicit registry is intended to
stabilize metadata, diagnostics, and planning behavior before FreshForge adds
plugin discovery or domain adapters.
