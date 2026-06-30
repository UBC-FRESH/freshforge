"""Workflow validation for FreshForge."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from freshforge.providers import (
    ProviderRegistry,
    default_provider_registry,
    parse_provider_reference,
)
from freshforge.records import Diagnostic, DiagnosticSeverity, WorkflowNode, WorkflowSpec

_SLUG_RE = re.compile(r"^[a-z][a-z0-9_-]*$")
_MAPPING_FIELDS = ("inputs", "outputs", "parameters", "provenance")


def has_error_diagnostics(diagnostics: Sequence[Diagnostic]) -> bool:
    """Return true when diagnostics contain at least one error."""
    return any(diagnostic.severity is DiagnosticSeverity.ERROR for diagnostic in diagnostics)


def validate_workflow_document(
    document: Any,
    *,
    source_path: str | None = None,
) -> tuple[WorkflowSpec | None, list[Diagnostic]]:
    """Validate a raw workflow document and return a spec when possible."""
    diagnostics: list[Diagnostic] = []
    if not isinstance(document, Mapping):
        return None, [
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="source.not_mapping",
                message="Workflow source must be a mapping.",
                location="$",
            )
        ]

    workflow_data = document.get("workflow")
    if not isinstance(workflow_data, Mapping):
        diagnostics.append(
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="workflow.not_mapping",
                message="Top-level 'workflow' must be a mapping.",
                location="workflow",
            )
        )
        workflow_data = {}

    workflow_id = _optional_string(workflow_data.get("id")) if workflow_data else None
    if not workflow_id:
        diagnostics.append(
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="workflow.id.required",
                message="Workflow id is required.",
                location="workflow.id",
            )
        )
        workflow_id = ""
    elif not _is_slug(workflow_id):
        diagnostics.append(
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="workflow.id.invalid",
                message=(
                    "Workflow id must be slug-like: lowercase letters, numbers, "
                    "hyphens, or underscores."
                ),
                location="workflow.id",
            )
        )

    nodes_data = document.get("nodes", [])
    if not isinstance(nodes_data, list):
        diagnostics.append(
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="nodes.not_list",
                message="Top-level 'nodes' must be a list.",
                location="nodes",
            )
        )
        nodes_data = []

    nodes: list[WorkflowNode] = []
    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()
    for index, node_data in enumerate(nodes_data):
        location = f"nodes[{index}]"
        if not isinstance(node_data, Mapping):
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.not_mapping",
                    message="Each node must be a mapping.",
                    location=location,
                )
            )
            continue

        node_id = _optional_string(node_data.get("id"))
        if not node_id:
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.id.required",
                    message="Node id is required.",
                    location=f"{location}.id",
                )
            )
            node_id = ""
        elif not _is_slug(node_id):
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.id.invalid",
                    message=(
                        "Node id must be slug-like: lowercase letters, numbers, "
                        "hyphens, or underscores."
                    ),
                    location=f"{location}.id",
                )
            )
        elif node_id in seen_ids:
            duplicate_ids.add(node_id)
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.id.duplicate",
                    message=f"Node id '{node_id}' is duplicated.",
                    location=f"{location}.id",
                )
            )
        seen_ids.add(node_id)

        provider = _optional_string(node_data.get("provider"))
        if not provider:
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.provider.required",
                    message="Node provider is required.",
                    location=f"{location}.provider",
                )
            )
            provider = ""

        needs = _parse_needs(node_data.get("needs", []), location, diagnostics)
        for field_name in _MAPPING_FIELDS:
            _validate_mapping_field(node_data, field_name, location, diagnostics)
        _validate_artifacts_field(node_data, location, diagnostics)

        nodes.append(
            WorkflowNode(
                id=node_id,
                provider=provider,
                name=_optional_string(node_data.get("name")),
                description=_optional_string(node_data.get("description")),
                needs=tuple(needs),
                inputs=dict(node_data.get("inputs", {}))
                if isinstance(node_data.get("inputs", {}), Mapping)
                else {},
                outputs=dict(node_data.get("outputs", {}))
                if isinstance(node_data.get("outputs", {}), Mapping)
                else {},
                parameters=dict(node_data.get("parameters", {}))
                if isinstance(node_data.get("parameters", {}), Mapping)
                else {},
                artifacts=node_data.get("artifacts", {}),
                provenance=dict(node_data.get("provenance", {}))
                if isinstance(node_data.get("provenance", {}), Mapping)
                else {},
            )
        )

    node_ids = {node.id for node in nodes if node.id and node.id not in duplicate_ids}
    _validate_dependencies(nodes, node_ids, diagnostics)
    _validate_acyclic(nodes, node_ids, diagnostics)

    return (
        WorkflowSpec(
            id=workflow_id,
            name=_optional_string(workflow_data.get("name")),
            description=_optional_string(workflow_data.get("description")),
            nodes=tuple(nodes),
            source_path=source_path,
        ),
        diagnostics,
    )


def validate_workflow_spec(spec: WorkflowSpec) -> list[Diagnostic]:
    """Validate an already constructed workflow spec."""
    return validate_workflow_document(spec.to_dict(), source_path=spec.source_path)[1]


def validate_workflow_with_providers(
    spec: WorkflowSpec,
    *,
    registry: ProviderRegistry | None = None,
    structural_diagnostics: Sequence[Diagnostic] | None = None,
) -> list[Diagnostic]:
    """Validate a workflow spec with provider registry diagnostics."""
    diagnostics = (
        list(structural_diagnostics)
        if structural_diagnostics is not None
        else validate_workflow_spec(spec)
    )
    provider_registry = registry if registry is not None else default_provider_registry()

    for index, node in enumerate(spec.nodes):
        if not node.provider:
            continue
        location = f"nodes[{index}]"
        parsed_reference = parse_provider_reference(node.provider)
        if parsed_reference is None:
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.provider.reference.invalid",
                    message=(
                        "Node provider must use '<provider namespace>.<node type>' syntax."
                    ),
                    location=f"{location}.provider",
                )
            )
            continue

        provider = provider_registry.get(parsed_reference.provider_id)
        if provider is None:
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.provider.unavailable",
                    message=(
                        f"Provider '{parsed_reference.provider_id}' is not registered."
                    ),
                    location=f"{location}.provider",
                )
            )
            continue

        node_type = _provider_node_type(provider.metadata(), parsed_reference.node_type)
        if node_type is None:
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.provider.node_type.unknown",
                    message=(
                        f"Provider '{parsed_reference.provider_id}' does not define "
                        f"node type '{parsed_reference.node_type}'."
                    ),
                    location=f"{location}.provider",
                )
            )
            continue

        diagnostics.extend(provider.validate_node(node, node_type, location=location))

    return diagnostics


def _optional_string(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _is_slug(value: str) -> bool:
    return bool(_SLUG_RE.fullmatch(value))


def _provider_node_type(metadata: Any, node_type_id: str) -> Any | None:
    for node_type in metadata.node_types:
        if node_type.id == node_type_id:
            return node_type
    return None


def _parse_needs(value: Any, location: str, diagnostics: list[Diagnostic]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        diagnostics.append(
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="node.needs.not_list",
                message="Node needs must be a list of node ids.",
                location=f"{location}.needs",
            )
        )
        return []
    needs: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="node.needs.item.invalid",
                    message="Each node dependency must be a nonempty string.",
                    location=f"{location}.needs[{index}]",
                )
            )
            continue
        needs.append(item.strip())
    return needs


def _validate_mapping_field(
    node_data: Mapping[str, Any],
    field_name: str,
    location: str,
    diagnostics: list[Diagnostic],
) -> None:
    if field_name in node_data and not isinstance(node_data[field_name], Mapping):
        diagnostics.append(
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code=f"node.{field_name}.not_mapping",
                message=f"Node {field_name} must be a mapping.",
                location=f"{location}.{field_name}",
            )
        )


def _validate_artifacts_field(
    node_data: Mapping[str, Any],
    location: str,
    diagnostics: list[Diagnostic],
) -> None:
    if "artifacts" in node_data and not isinstance(node_data["artifacts"], Mapping | list):
        diagnostics.append(
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="node.artifacts.invalid_shape",
                message="Node artifacts must be a mapping or list.",
                location=f"{location}.artifacts",
            )
        )


def _validate_dependencies(
    nodes: Sequence[WorkflowNode],
    node_ids: set[str],
    diagnostics: list[Diagnostic],
) -> None:
    for node in nodes:
        if not node.id:
            continue
        for dependency in node.needs:
            if dependency not in node_ids:
                diagnostics.append(
                    Diagnostic(
                        severity=DiagnosticSeverity.ERROR,
                        code="node.needs.unknown",
                        message=f"Node '{node.id}' depends on unknown node '{dependency}'.",
                        location=f"nodes.{node.id}.needs",
                    )
                )


def _validate_acyclic(
    nodes: Sequence[WorkflowNode],
    node_ids: set[str],
    diagnostics: list[Diagnostic],
) -> None:
    dependencies = {node.id: set(node.needs) & node_ids for node in nodes if node.id in node_ids}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str, path: tuple[str, ...]) -> None:
        if node_id in visited:
            return
        if node_id in visiting:
            cycle_path = " -> ".join((*path, node_id))
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="workflow.cycle",
                    message=f"Workflow contains a dependency cycle: {cycle_path}.",
                    location=f"nodes.{node_id}.needs",
                )
            )
            return
        visiting.add(node_id)
        for dependency in sorted(dependencies.get(node_id, ())):
            visit(dependency, (*path, node_id))
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in sorted(dependencies):
        visit(node_id, ())
