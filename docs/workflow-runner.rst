Workflow Runner
===============

Phase 6 adds FreshForge's first workflow execution surface: a serial local
runner for provider-owned nodes. Phase 7 adds optional run namespaces and
compact run summaries so repeated local runs can be compared without artifact
collisions.

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

Run Namespaces
--------------

Use ``--namespace`` to isolate relative artifacts for repeated local runs:

.. code-block:: bash

   freshforge run path/to/workflow.yaml --workdir tmp/runs --namespace strategy/output-columns --json

With that command, a workflow artifact declared as ``reports/out.json`` resolves
under ``tmp/runs/strategy/output-columns/reports/out.json``. Absolute artifact
paths remain absolute. Namespaces must be non-empty relative paths and may not
contain ``..``.

Run Summaries
-------------

JSON run output includes both the full ``run`` record and a compact
``summary`` record:

.. code-block:: json

   {
     "ok": true,
     "run": {"workflow_id": "demo"},
     "summary": {"workflow_id": "demo", "node_count": 3}
   }

The summary includes the workflow id, optional namespace, status, node counts,
diagnostic counts, artifact count, and per-node compact summaries. Full outputs,
artifacts, diagnostics, and provider data remain available in the full run
record.

If providers emit optional provider evidence mappings, FreshForge includes those
mappings in full node run results and includes evidence counts plus compact
evidence mappings in per-node summaries. Evidence remains provider-owned data:
FreshForge core serializes it but does not interpret validation labels, artifact
roles, paths, URIs, or scientific meaning.

This means the summary is suitable for dashboards or matrix comparison tools
that need to know whether evidence exists, while the full run record and
evidence manifest retain the complete provider-owned mapping for downstream
validation.

For downstream tools that only need the compact record, use ``--summary``:

.. code-block:: bash

   freshforge run examples/stand_treatment_workflow.yaml --summary

This emits the same deterministic summary object that appears under
``summary`` in ``--json`` output, without the full run record.

Evidence Manifests
------------------

Use ``--evidence`` to write a durable JSON evidence manifest while preserving
the normal command output mode:

.. code-block:: bash

   freshforge run examples/stand_treatment_workflow.yaml --workdir tmp/runs --evidence tmp/run-evidence.json

The manifest records the FreshForge version, workflow source path, work
directory, optional run namespace, workflow id, run status, compact summary,
full run record, and top-level diagnostics. Failed runs can still write
evidence manifests, which lets downstream tools audit why a workflow did not
complete.

Evidence manifests are a persistence contract, not a new execution engine. They
do not add caching, checkpointing, retries, remotes, parallel execution, artifact
content validation, or provider-specific evidence semantics.

Boundaries
----------

The Phase 7 runner is intentionally small. It does not add caching,
checkpointing, parallel execution, remotes, retries, shell-command nodes, or
domain-package imports in FreshForge core. Phase 8 builds on the runner with
generic repeated-run matrices; see :doc:`run-matrices`.
