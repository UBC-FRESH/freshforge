Execution
=========

Phase 6 adds the first FreshForge execution surface. The command is explicit:

.. code-block:: bash

   freshforge run path/to/workflow.yaml --run-id example_run

FreshForge still validates and plans the workflow first. If loading,
validation, provider discovery, or planning returns error-severity diagnostics,
execution does not start. ``validate``, ``inspect``, and ``plan`` remain
non-mutating commands.

Provider Contract
-----------------

Providers may implement an ``execute_node`` hook. FreshForge calls that hook in
deterministic topological order and passes the workflow ID, run ID, workflow
source path, and previous node results. Providers own domain-specific command
launches, scientific logic, runtime discovery, and artifact creation.

Providers that only implement metadata and validation remain valid for
``validate``, ``inspect``, and ``plan``. They cannot be used with
``freshforge run``. FreshForge reports missing execution support as a structured
diagnostic instead of a Python traceback.

Dry Runs
--------

Use ``--dry-run`` to produce an execution-shaped report without calling provider
hooks:

.. code-block:: bash

   freshforge run examples/stand_treatment_workflow.yaml --run-id smoke --dry-run --json

Dry runs are useful for checking provider resolution and planned node order
before expensive or stateful domain tools are launched.

Run Reports
-----------

``freshforge run`` can write a JSON report:

.. code-block:: bash

   freshforge run workflow.yaml --run-id rebuild_001 --report runtime/freshforge/runs/rebuild_001.json

Reports include the workflow ID, run ID, planned order, node statuses, provider
IDs, node types, timestamps, durations, provider command/display metadata,
diagnostics, and declared artifacts.

Run reports are runtime artifacts. Projects should write them under ignored
runtime directories unless they intentionally curate a specific report as
release evidence.

Current Limits
--------------

Execution remains alpha and provider-owned. FreshForge does not yet provide
caching, checkpoint resume, materialization workflows, artifact verification,
parallel execution, retry policy, or built-in FRESH ecosystem execution logic.
