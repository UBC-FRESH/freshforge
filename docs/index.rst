FreshForge
==========

FreshForge is workflow-as-code for open forest resources and ecosystem services
modelling.

FreshForge is currently a public-alpha package. It does not yet implement a
stable workflow language, real ecosystem adapters, caching, checkpointing,
parallel execution, or remote execution.

Phase 2 adds provisional workflow records, YAML/JSON loading, structural
validation diagnostics, and non-executing run planning.

Phase 3 adds an explicit provider registry, built-in example provider metadata,
provider-aware diagnostics, workflow inspection, and provider-aware run plans
without executing nodes.

Phase 4 adds Python entry-point provider discovery and a public-safe fixture
adapter that proves the adapter packaging path without importing real FRESH
ecosystem tools.

Phase 5 hardens public documentation, examples, release notes, and artifact
checks for the ``0.1.0a1`` GitHub alpha release.

Phase 6 adds the first serial local workflow runner for provider-owned node
execution.

Phase 9 packages that runner milestone as the ``0.1.0a2`` GitHub alpha release.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   development-workflow
   governance
   architecture
   workflow-records
   examples
   providers
   adapter-discovery
   workflow-runner
   release-checklist
   roadmap
