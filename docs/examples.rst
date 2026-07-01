Examples
========

FreshForge ships public-safe example workflow specs that exercise the current
alpha validation, inspection, provider discovery, planning, and dry-run
surfaces. They are synthetic examples and do not represent real project data.

Stand Treatment Workflow
------------------------

``examples/stand_treatment_workflow.yaml`` is the smallest single-provider
example. It uses the built-in ``freshforge.example`` provider and declares a
three-node graph:

* load synthetic inventory;
* classify placeholder fuel information;
* declare a treatment prescription report.

.. code-block:: bash

   freshforge validate examples/stand_treatment_workflow.yaml
   freshforge inspect examples/stand_treatment_workflow.yaml
   freshforge plan examples/stand_treatment_workflow.yaml
   freshforge run examples/stand_treatment_workflow.yaml --run-id smoke --dry-run

Ecosystem Adapter Workflow
--------------------------

``examples/ecosystem_adapter_workflow.yaml`` is the Phase 4 multi-provider
example. It uses both the built-in ``freshforge.example`` provider and the
entry-point-discovered ``freshforge.fixture`` provider:

* load synthetic inventory;
* declare an inventory summary;
* declare a yield table check;
* declare a scenario report artifact.

.. code-block:: bash

   freshforge validate examples/ecosystem_adapter_workflow.yaml
   freshforge inspect examples/ecosystem_adapter_workflow.yaml --json
   freshforge plan examples/ecosystem_adapter_workflow.yaml --json

Example Boundaries
------------------

The bundled examples are intentionally validate-only provider examples. They can
be used with ``freshforge run --dry-run`` to produce execution-shaped reports,
but real execution requires providers that implement execution hooks. FreshForge
does not read datasets, inspect declared artifact files, or create workflow
outputs for these examples.
