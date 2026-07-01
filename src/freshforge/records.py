"""Core workflow records for FreshForge."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class DiagnosticSeverity(StrEnum):
    """Severity for workflow diagnostics."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class RunStatus(StrEnum):
    """Status for workflow and node execution records."""

    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class Diagnostic:
    """Structured validation or planning diagnostic."""

    severity: DiagnosticSeverity
    code: str
    message: str
    location: str | None = None

    def to_dict(self) -> dict[str, str]:
        data = {
            "severity": self.severity.value,
            "code": self.code,
            "message": self.message,
        }
        if self.location is not None:
            data["location"] = self.location
        return data


@dataclass(frozen=True)
class WorkflowNode:
    """A single non-executed workflow node specification."""

    id: str
    provider: str
    name: str | None = None
    description: str | None = None
    needs: tuple[str, ...] = ()
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, Any] | list[Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "provider": self.provider,
        }
        if self.name is not None:
            data["name"] = self.name
        if self.description is not None:
            data["description"] = self.description
        if self.needs:
            data["needs"] = list(self.needs)
        if self.inputs:
            data["inputs"] = self.inputs
        if self.outputs:
            data["outputs"] = self.outputs
        if self.parameters:
            data["parameters"] = self.parameters
        if self.artifacts:
            data["artifacts"] = self.artifacts
        if self.provenance:
            data["provenance"] = self.provenance
        return data


@dataclass(frozen=True)
class WorkflowSpec:
    """A loaded workflow specification."""

    id: str
    nodes: tuple[WorkflowNode, ...]
    name: str | None = None
    description: str | None = None
    source_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        workflow: dict[str, Any] = {"id": self.id}
        if self.name is not None:
            workflow["name"] = self.name
        if self.description is not None:
            workflow["description"] = self.description

        data: dict[str, Any] = {
            "workflow": workflow,
            "nodes": [node.to_dict() for node in self.nodes],
        }
        if self.source_path is not None:
            data["source_path"] = self.source_path
        return data


@dataclass(frozen=True)
class PlannedNode:
    """A node in a non-executing run plan."""

    id: str
    provider: str
    provider_id: str | None = None
    node_type: str | None = None
    provider_available: bool = False
    needs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "provider": self.provider,
            "provider_id": self.provider_id,
            "node_type": self.node_type,
            "provider_available": self.provider_available,
            "needs": list(self.needs),
        }


@dataclass(frozen=True)
class RunPlan:
    """A deterministic non-executing workflow plan."""

    workflow_id: str
    nodes: tuple[PlannedNode, ...]
    diagnostics: tuple[Diagnostic, ...] = ()

    @property
    def has_errors(self) -> bool:
        return any(
            diagnostic.severity is DiagnosticSeverity.ERROR for diagnostic in self.diagnostics
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "nodes": [node.to_dict() for node in self.nodes],
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class ProviderRunResult:
    """Provider-owned result for one executed workflow node."""

    status: RunStatus
    outputs: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, Any] = field(default_factory=dict)
    diagnostics: tuple[Diagnostic, ...] = ()
    data: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.status is RunStatus.SUCCESS and not any(
            diagnostic.severity is DiagnosticSeverity.ERROR for diagnostic in self.diagnostics
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "outputs": self.outputs,
            "artifacts": self.artifacts,
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
            "data": self.data,
        }


@dataclass(frozen=True)
class NodeRunResult:
    """FreshForge execution record for one workflow node."""

    id: str
    provider: str
    provider_id: str | None
    node_type: str | None
    status: RunStatus
    outputs: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, Any] = field(default_factory=dict)
    diagnostics: tuple[Diagnostic, ...] = ()
    data: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.status is RunStatus.SUCCESS and not any(
            diagnostic.severity is DiagnosticSeverity.ERROR for diagnostic in self.diagnostics
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "provider": self.provider,
            "provider_id": self.provider_id,
            "node_type": self.node_type,
            "status": self.status.value,
            "outputs": self.outputs,
            "artifacts": self.artifacts,
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
            "data": self.data,
        }


@dataclass(frozen=True)
class NodeRunSummary:
    """Compact execution summary for one workflow node."""

    id: str
    provider_id: str | None
    node_type: str | None
    status: RunStatus
    diagnostic_count: int = 0
    error_count: int = 0
    warning_count: int = 0
    artifact_count: int = 0
    artifacts: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "provider_id": self.provider_id,
            "node_type": self.node_type,
            "status": self.status.value,
            "diagnostic_count": self.diagnostic_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "artifact_count": self.artifact_count,
            "artifacts": self.artifacts,
        }


@dataclass(frozen=True)
class WorkflowRunSummary:
    """Compact execution summary for a workflow run."""

    workflow_id: str
    status: RunStatus
    run_namespace: str | None = None
    node_count: int = 0
    succeeded_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    diagnostic_count: int = 0
    error_count: int = 0
    warning_count: int = 0
    artifact_count: int = 0
    nodes: tuple[NodeRunSummary, ...] = ()

    @property
    def ok(self) -> bool:
        return self.status is RunStatus.SUCCESS and self.error_count == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "run_namespace": self.run_namespace,
            "status": self.status.value,
            "node_count": self.node_count,
            "succeeded_count": self.succeeded_count,
            "failed_count": self.failed_count,
            "skipped_count": self.skipped_count,
            "diagnostic_count": self.diagnostic_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "artifact_count": self.artifact_count,
            "nodes": [node.to_dict() for node in self.nodes],
        }


@dataclass(frozen=True)
class WorkflowRunResult:
    """FreshForge execution record for a whole workflow run."""

    workflow_id: str
    status: RunStatus
    run_namespace: str | None = None
    nodes: tuple[NodeRunResult, ...] = ()
    diagnostics: tuple[Diagnostic, ...] = ()

    @property
    def ok(self) -> bool:
        return self.status is RunStatus.SUCCESS and not any(
            diagnostic.severity is DiagnosticSeverity.ERROR for diagnostic in self.diagnostics
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "run_namespace": self.run_namespace,
            "status": self.status.value,
            "nodes": [node.to_dict() for node in self.nodes],
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }

    def summary(self) -> WorkflowRunSummary:
        """Return a compact summary of this workflow run."""
        node_summaries = tuple(_node_run_summary(node) for node in self.nodes)
        diagnostics = self.diagnostics
        return WorkflowRunSummary(
            workflow_id=self.workflow_id,
            run_namespace=self.run_namespace,
            status=self.status,
            node_count=len(self.nodes),
            succeeded_count=sum(1 for node in self.nodes if node.status is RunStatus.SUCCESS),
            failed_count=sum(1 for node in self.nodes if node.status is RunStatus.FAILED),
            skipped_count=sum(1 for node in self.nodes if node.status is RunStatus.SKIPPED),
            diagnostic_count=len(diagnostics),
            error_count=sum(
                1 for diagnostic in diagnostics if diagnostic.severity is DiagnosticSeverity.ERROR
            ),
            warning_count=sum(
                1 for diagnostic in diagnostics if diagnostic.severity is DiagnosticSeverity.WARNING
            ),
            artifact_count=sum(summary.artifact_count for summary in node_summaries),
            nodes=node_summaries,
        )


def _node_run_summary(node: NodeRunResult) -> NodeRunSummary:
    return NodeRunSummary(
        id=node.id,
        provider_id=node.provider_id,
        node_type=node.node_type,
        status=node.status,
        diagnostic_count=len(node.diagnostics),
        error_count=sum(
            1 for diagnostic in node.diagnostics if diagnostic.severity is DiagnosticSeverity.ERROR
        ),
        warning_count=sum(
            1
            for diagnostic in node.diagnostics
            if diagnostic.severity is DiagnosticSeverity.WARNING
        ),
        artifact_count=len(node.artifacts),
        artifacts=dict(node.artifacts),
    )
