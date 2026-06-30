"""FreshForge package."""

from freshforge.providers import (
    FixtureProvider,
    NodeTypeMetadata,
    ProviderMetadata,
    ProviderReference,
    ProviderRegistry,
    ProviderResolution,
    discover_entry_point_providers,
    fixture_provider_factory,
)
from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    PlannedNode,
    RunPlan,
    WorkflowNode,
    WorkflowSpec,
)

__version__ = "0.1.0a1"

__all__ = [
    "Diagnostic",
    "DiagnosticSeverity",
    "FixtureProvider",
    "NodeTypeMetadata",
    "PlannedNode",
    "ProviderMetadata",
    "ProviderReference",
    "ProviderRegistry",
    "ProviderResolution",
    "RunPlan",
    "WorkflowNode",
    "WorkflowSpec",
    "__version__",
    "discover_entry_point_providers",
    "fixture_provider_factory",
]
