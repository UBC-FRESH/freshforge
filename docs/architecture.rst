Architecture
============

FreshForge is intended to become a neutral workflow core rather than a domain
package that imports every FRESH modelling tool.

Intended Dependency Direction
-----------------------------

.. code-block:: text

   freshforge core
           ^
           |
   domain package adapters and provider registrations
           ^
           |
   project recipes and instance workflows

Domain packages such as FEMIC, FHOPS, ws3, Modelwright, and Nemora should own
their own scientific logic. FreshForge should own shared workflow contracts,
validation, execution planning, provenance, and orchestration semantics.

Phase 0 Boundary
----------------

Phase 0 does not implement workflow schema, node protocol, provider registry,
graph executor, cache or checkpoint semantics, or ecosystem adapters.
