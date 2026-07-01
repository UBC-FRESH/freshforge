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
    NodeRunResult,
    PlannedNode,
    ProviderRunResult,
    RunPlan,
    RunStatus,
    WorkflowNode,
    WorkflowRunResult,
    WorkflowSpec,
)

__version__ = "0.1.0a2"

__all__ = [
    "Diagnostic",
    "DiagnosticSeverity",
    "FixtureProvider",
    "NodeTypeMetadata",
    "NodeRunResult",
    "PlannedNode",
    "ProviderMetadata",
    "ProviderReference",
    "ProviderRegistry",
    "ProviderResolution",
    "ProviderRunResult",
    "RunPlan",
    "RunStatus",
    "WorkflowNode",
    "WorkflowRunResult",
    "WorkflowSpec",
    "__version__",
    "discover_entry_point_providers",
    "fixture_provider_factory",
]
