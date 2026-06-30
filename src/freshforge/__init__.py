"""FreshForge package."""

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
    "PlannedNode",
    "RunPlan",
    "WorkflowNode",
    "WorkflowSpec",
    "__version__",
]
