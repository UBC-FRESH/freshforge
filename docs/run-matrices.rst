Run Matrices
============

Phase 8 adds generic run matrices for repeated workflow runs. A matrix expands a
workflow template into ordinary FreshForge workflow specs, assigns each case a
run namespace, and can plan or run each case serially.

FreshForge stays domain-neutral. Matrix variables are just values used for
template substitution. Domain packages decide what those variables mean.

Matrix Shape
------------

Matrix files may be YAML or JSON. They point to a workflow template and define
either explicit ``cases`` or Cartesian-product ``axes``:

.. code-block:: yaml

   matrix:
     id: treatment_matrix_demo
     workflow_template: matrix_workflow_template.yaml
   axes:
     - id: strategy
       values:
         - id: baseline
           variables:
             classification: baseline
         - id: thinning
           variables:
             classification: thinning

FreshForge expands axis values into case IDs such as
``strategy-baseline`` and ``strategy-thinning``. By default, run namespaces are
``{matrix_id}/{case_id}``, for example
``treatment_matrix_demo/strategy-baseline``. Explicit cases may provide their
own ``namespace``.

Template Substitution
---------------------

Workflow templates are ordinary workflow specs with ``${matrix.*}``
placeholders in string values:

.. code-block:: yaml

   workflow:
     id: matrix_${matrix.case_id}_demo
   nodes:
     - id: classify_fuel
       provider: freshforge.example.classify_fuel
       parameters:
         classification: ${matrix.classification}
       artifacts:
         report: reports/${matrix.case_id}/summary.json

Supported placeholders are:

``${matrix.case_id}``
   The expanded case ID.

``${matrix.namespace}``
   The namespace assigned to the case.

``${matrix.<variable>}``
   Any variable declared by an explicit case or by an axis value.

Missing placeholders produce diagnostics. Expanded workflows are validated with
the same workflow validation used by ``freshforge validate``.

CLI
---

Expand without planning or running:

.. code-block:: bash

   freshforge matrix expand examples/run_matrix.yaml --json

Plan every expanded case:

.. code-block:: bash

   freshforge matrix plan examples/run_matrix.yaml --json

Run every expanded case serially:

.. code-block:: bash

   freshforge matrix run examples/run_matrix.yaml --workdir tmp/matrix-runs --json

Use ``--fail-fast`` to stop after the first failed case. Without
``--fail-fast``, FreshForge attempts every case and reports a combined matrix
summary.

Boundaries
----------

Matrices do not add caching, checkpointing, parallel execution, remote
execution, retries, or production scheduling. They do not know what a FABLE
scenario, Modelwright validation scope, or FEMIC treatment setting means. They
only expand a template, run cases with namespaces, and summarize the results.

