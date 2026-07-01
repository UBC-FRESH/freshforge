Workflow Runner
===============

Phase 6 adds FreshForge's first workflow execution surface: a serial local
runner for provider-owned nodes.

The runner keeps FreshForge generic. FreshForge validates the workflow, creates
the deterministic run plan, resolves relative artifact paths against a run
working directory, and calls provider ``run_node`` hooks in plan order. Domain
packages still own the actual work.

Command Line
------------

Use ``freshforge run`` with a workflow spec:

.. code-block:: bash

   freshforge run examples/stand_treatment_workflow.yaml --json

Plan-only providers fail with a clear diagnostic instead of pretending to run:

.. code-block:: text

   node.execution.unsupported

Executable provider packages may implement ``run_node(node, node_type,
context=...)`` and return a ``ProviderRunResult``. The run result is serialized
as deterministic JSON and includes workflow status, per-node status, provider
outputs, artifact paths, and diagnostics.

Working Directory
-----------------

Relative artifact paths are resolved against the selected work directory:

.. code-block:: bash

   freshforge run path/to/workflow.yaml --workdir /path/to/project --json

The default work directory is the current directory. Providers can use
``context.resolve_path(...)`` to resolve workflow-declared paths.

Boundaries
----------

The Phase 6 runner is intentionally small. It does not add caching,
checkpointing, parallel execution, remotes, retries, shell-command nodes, or
domain-package imports in FreshForge core.
