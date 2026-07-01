"""Serial local workflow execution."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from freshforge.planning import create_run_plan
from freshforge.providers import (
    NodeTypeMetadata,
    Provider,
    ProviderRegistry,
    default_provider_registry,
)
from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    NodeRunResult,
    ProviderRunResult,
    RunStatus,
    WorkflowNode,
    WorkflowRunResult,
    WorkflowSpec,
)


@dataclass
class RunContext:
    """Execution context passed to provider ``run_node`` implementations."""

    workflow_id: str
    workdir: Path
    run_namespace: str | None = None
    completed_outputs: dict[str, dict[str, Any]] = field(default_factory=dict)
    completed_artifacts: dict[str, dict[str, Any]] = field(default_factory=dict)

    def resolve_path(self, value: str | Path) -> Path:
        """Resolve a workflow-declared path against the run working directory."""
        path = Path(value)
        if path.is_absolute():
            return path
        if self.run_namespace is None:
            return self.workdir / path
        return self.workdir / self.run_namespace / path


def run_workflow(
    spec: WorkflowSpec,
    *,
    diagnostics: Sequence[Diagnostic] | None = None,
    registry: ProviderRegistry | None = None,
    workdir: str | Path | None = None,
    run_namespace: str | None = None,
) -> WorkflowRunResult:
    """Execute a workflow with provider-owned nodes in deterministic plan order."""
    namespace_diagnostic = validate_run_namespace(run_namespace)
    if namespace_diagnostic is not None:
        return WorkflowRunResult(
            workflow_id=spec.id,
            run_namespace=run_namespace,
            status=RunStatus.FAILED,
            diagnostics=(namespace_diagnostic,),
        )

    provider_registry, initial_diagnostics = _registry_and_diagnostics(registry, diagnostics)
    plan = create_run_plan(
        spec,
        diagnostics=initial_diagnostics,
        registry=provider_registry,
    )
    if plan.has_errors:
        return WorkflowRunResult(
            workflow_id=spec.id,
            run_namespace=run_namespace,
            status=RunStatus.FAILED,
            diagnostics=tuple(plan.diagnostics),
        )

    context = RunContext(
        workflow_id=spec.id,
        workdir=Path.cwd() if workdir is None else Path(workdir).resolve(),
        run_namespace=run_namespace,
    )
    nodes_by_id = {node.id: node for node in spec.nodes}
    run_nodes: list[NodeRunResult] = []
    diagnostics_out: list[Diagnostic] = list(plan.diagnostics)

    for planned in plan.nodes:
        node = nodes_by_id[planned.id]
        provider = provider_registry.get(planned.provider_id or "")
        node_type = _provider_node_type(provider, planned.node_type)
        if provider is None or node_type is None:
            failed = _failed_node(
                node=node,
                provider_id=planned.provider_id,
                node_type=planned.node_type,
                diagnostic=Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.execution.provider_unavailable",
                    message="Node provider or node type is unavailable during execution.",
                    location=f"nodes.{node.id}.provider",
                ),
            )
            run_nodes.append(failed)
            diagnostics_out.extend(failed.diagnostics)
            break

        run_node = getattr(provider, "run_node", None)
        if not callable(run_node):
            failed = _failed_node(
                node=node,
                provider_id=planned.provider_id,
                node_type=planned.node_type,
                diagnostic=Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.execution.unsupported",
                    message=(
                        f"Provider '{planned.provider_id}' does not implement node execution."
                    ),
                    location=f"nodes.{node.id}",
                ),
            )
            run_nodes.append(failed)
            diagnostics_out.extend(failed.diagnostics)
            break

        try:
            provider_result = run_node(node, node_type, context=context)
        except Exception as exc:  # noqa: BLE001
            failed = _failed_node(
                node=node,
                provider_id=planned.provider_id,
                node_type=planned.node_type,
                diagnostic=Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.execution.failed",
                    message=f"Provider execution failed: {exc}",
                    location=f"nodes.{node.id}",
                ),
            )
            run_nodes.append(failed)
            diagnostics_out.extend(failed.diagnostics)
            break

        if not isinstance(provider_result, ProviderRunResult):
            failed = _failed_node(
                node=node,
                provider_id=planned.provider_id,
                node_type=planned.node_type,
                diagnostic=Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.execution.invalid_result",
                    message="Provider run_node() must return ProviderRunResult.",
                    location=f"nodes.{node.id}",
                ),
            )
            run_nodes.append(failed)
            diagnostics_out.extend(failed.diagnostics)
            break

        node_result = NodeRunResult(
            id=node.id,
            provider=node.provider,
            provider_id=planned.provider_id,
            node_type=planned.node_type,
            status=provider_result.status,
            outputs=dict(provider_result.outputs),
            artifacts=dict(provider_result.artifacts),
            diagnostics=tuple(provider_result.diagnostics),
            data=dict(provider_result.data),
        )
        run_nodes.append(node_result)
        diagnostics_out.extend(node_result.diagnostics)
        context.completed_outputs[node.id] = dict(provider_result.outputs)
        context.completed_artifacts[node.id] = dict(provider_result.artifacts)

        if not node_result.ok:
            break

    status = (
        RunStatus.SUCCESS
        if len(run_nodes) == len(plan.nodes) and all(node.ok for node in run_nodes)
        else RunStatus.FAILED
    )
    return WorkflowRunResult(
        workflow_id=spec.id,
        run_namespace=run_namespace,
        status=status,
        nodes=tuple(run_nodes),
        diagnostics=tuple(diagnostics_out),
    )


def _registry_and_diagnostics(
    registry: ProviderRegistry | None,
    diagnostics: Sequence[Diagnostic] | None,
) -> tuple[ProviderRegistry, list[Diagnostic]]:
    initial_diagnostics = list(diagnostics) if diagnostics is not None else []
    if registry is not None:
        return registry, initial_diagnostics
    provider_registry, discovery_diagnostics = default_provider_registry()
    initial_diagnostics.extend(discovery_diagnostics)
    return provider_registry, initial_diagnostics


def _provider_node_type(
    provider: Provider | None,
    node_type_id: str | None,
) -> NodeTypeMetadata | None:
    if provider is None or node_type_id is None:
        return None
    for node_type in provider.metadata().node_types:
        if node_type.id == node_type_id:
            return node_type
    return None


def _failed_node(
    *,
    node: WorkflowNode,
    provider_id: str | None,
    node_type: str | None,
    diagnostic: Diagnostic,
) -> NodeRunResult:
    return NodeRunResult(
        id=node.id,
        provider=node.provider,
        provider_id=provider_id,
        node_type=node_type,
        status=RunStatus.FAILED,
        diagnostics=(diagnostic,),
    )


def artifact_paths(node: WorkflowNode, context: RunContext) -> dict[str, Path]:
    """Return node artifact paths resolved against the run context."""
    if not isinstance(node.artifacts, Mapping):
        return {}
    paths: dict[str, Path] = {}
    for key, value in node.artifacts.items():
        if isinstance(value, (str, Path)):
            paths[key] = context.resolve_path(value)
    return paths


def validate_run_namespace(run_namespace: str | None) -> Diagnostic | None:
    """Return a diagnostic when a run namespace is invalid."""
    if run_namespace is None:
        return None
    namespace = run_namespace.strip()
    if namespace == "":
        return _invalid_namespace_diagnostic(run_namespace)
    path = Path(namespace)
    if path.is_absolute() or ".." in path.parts:
        return _invalid_namespace_diagnostic(run_namespace)
    return None


def _invalid_namespace_diagnostic(run_namespace: str) -> Diagnostic:
    return Diagnostic(
        severity=DiagnosticSeverity.ERROR,
        code="run.namespace.invalid",
        message=(
            "Run namespace must be a non-empty relative path and must not contain '..'."
        ),
        location="run.namespace",
    )
