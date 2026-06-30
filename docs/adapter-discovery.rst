Adapter Discovery
=================

Phase 4 introduces Python entry-point discovery for provider adapters. The goal
is to prove how a companion package or native domain package can expose provider
metadata to FreshForge without FreshForge importing real ecosystem tools
directly.

Entry-Point Contract
--------------------

Provider packages may expose factories through the ``freshforge.providers``
entry-point group:

.. code-block:: toml

   [project.entry-points."freshforge.providers"]
   example = "some_package.freshforge:provider_factory"

Each entry point must load to a callable factory. The factory must return an
object that implements the FreshForge provider protocol: ``metadata()`` and
``validate_node(...)``. FreshForge registers the returned provider by
``ProviderMetadata.id``.

Discovery Diagnostics
---------------------

Discovery failures are reported as FreshForge diagnostics instead of Python
tracebacks. Diagnostics cover:

* entry-point load failures;
* factory failures;
* invalid provider objects;
* invalid provider metadata;
* duplicate provider IDs.

CLI commands use entry-point discovery by default. The Python API also supports
explicit registration and can construct a registry without entry points for
tests or tightly controlled applications.

Fixture Adapter
---------------

FreshForge ships a public-safe fixture adapter under provider ID
``freshforge.fixture``. It is registered through FreshForge's own
``freshforge.providers`` entry point so tests and docs exercise the same
discovery path that a future companion package would use.

The fixture adapter is intentionally non-executing. Its node types declare
FRESH-flavoured workflow steps such as inventory summary, yield table check, and
scenario report declaration. Validation checks only broad declared keys and
simple parameters; it does not read datasets, inspect artifacts, or call external
tools.

Example
-------

.. code-block:: bash

   freshforge providers
   freshforge validate examples/ecosystem_adapter_workflow.yaml
   freshforge inspect examples/ecosystem_adapter_workflow.yaml --json
   freshforge plan examples/ecosystem_adapter_workflow.yaml

Deferred Work
-------------

Phase 4 does not add real FEMIC, FHOPS, ws3, Modelwright, or Nemora adapters. It
also does not add node execution, ``freshforge run``, artifact materialization,
caching, checkpoints, or run records.
