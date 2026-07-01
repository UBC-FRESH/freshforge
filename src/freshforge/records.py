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
class WorkflowRunResult:
    """FreshForge execution record for a whole workflow run."""

    workflow_id: str
    status: RunStatus
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
            "status": self.status.value,
            "nodes": [node.to_dict() for node in self.nodes],
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }
