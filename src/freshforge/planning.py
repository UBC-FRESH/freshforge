"""Non-executing workflow planning."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from freshforge.providers import ProviderRegistry, default_provider_registry
from freshforge.records import Diagnostic, DiagnosticSeverity, PlannedNode, RunPlan, WorkflowSpec
from freshforge.validation import has_error_diagnostics, validate_workflow_with_providers


def create_run_plan(
    spec: WorkflowSpec,
    *,
    diagnostics: Sequence[Diagnostic] | None = None,
    registry: ProviderRegistry | None = None,
) -> RunPlan:
    """Create a deterministic non-executing run plan."""
    if registry is None:
        provider_registry, discovery_diagnostics = default_provider_registry()
        initial_diagnostics = list(diagnostics) if diagnostics is not None else []
        initial_diagnostics.extend(discovery_diagnostics)
    else:
        provider_registry = registry
        initial_diagnostics = list(diagnostics) if diagnostics is not None else []
    validation_diagnostics = (
        validate_workflow_with_providers(
            spec,
            registry=provider_registry,
            structural_diagnostics=initial_diagnostics,
        )
        if initial_diagnostics
        else validate_workflow_with_providers(spec, registry=provider_registry)
    )
    if has_error_diagnostics(validation_diagnostics):
        return RunPlan(
            workflow_id=spec.id,
            nodes=(),
            diagnostics=tuple(validation_diagnostics),
        )

    nodes_by_id = {node.id: node for node in spec.nodes}
    incoming_count = {node.id: len(node.needs) for node in spec.nodes}
    dependents: dict[str, list[str]] = defaultdict(list)
    for node in spec.nodes:
        for dependency in node.needs:
            dependents[dependency].append(node.id)

    ready = [node.id for node in spec.nodes if incoming_count[node.id] == 0]
    planned: list[PlannedNode] = []

    while ready:
        node_id = ready.pop(0)
        node = nodes_by_id[node_id]
        provider_resolution = provider_registry.resolve(node.provider)
        planned.append(
            PlannedNode(
                id=node.id,
                provider=node.provider,
                provider_id=provider_resolution.provider_id,
                node_type=provider_resolution.node_type,
                provider_available=provider_resolution.provider_available,
                needs=node.needs,
            )
        )
        for dependent_id in sorted(dependents.get(node_id, [])):
            incoming_count[dependent_id] -= 1
            if incoming_count[dependent_id] == 0:
                ready.append(dependent_id)

    if len(planned) != len(spec.nodes):
        validation_diagnostics.append(
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="workflow.plan.incomplete",
                message="Could not produce a complete run plan for the workflow.",
                location="nodes",
            )
        )
        return RunPlan(workflow_id=spec.id, nodes=(), diagnostics=tuple(validation_diagnostics))

    return RunPlan(
        workflow_id=spec.id,
        nodes=tuple(planned),
        diagnostics=tuple(validation_diagnostics),
    )
