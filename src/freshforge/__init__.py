"""FreshForge package."""

from freshforge.providers import (
    NodeTypeMetadata,
    ProviderMetadata,
    ProviderReference,
    ProviderRegistry,
    ProviderResolution,
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
]
