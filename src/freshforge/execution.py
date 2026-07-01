"""Workflow execution support."""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from freshforge.planning import create_run_plan
from freshforge.providers import NodeTypeMetadata, ProviderRegistry, default_provider_registry
from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    ExecutionContext,
    NodeRunRecord,
    NodeRunStatus,
    ProviderExecutionResult,
    WorkflowRunReport,
    WorkflowSpec,
)

NowFn = Callable[[], datetime]


def execute_workflow(
    spec: WorkflowSpec,
    *,
    run_id: str,
    diagnostics: Sequence[Diagnostic] | None = None,
    registry: ProviderRegistry | None = None,
    dry_run: bool = False,
    report_path: Path | None = None,
    now_fn: NowFn | None = None,
) -> WorkflowRunReport:
    """Execute a workflow through provider hooks in deterministic plan order."""
    now = now_fn or (lambda: datetime.now(UTC))
    provider_registry, initial_diagnostics = _registry_and_diagnostics(
        registry=registry,
        diagnostics=diagnostics,
    )
    started_at = now()
    plan = create_run_plan(
        spec,
        diagnostics=initial_diagnostics,
        registry=provider_registry,
    )
    if plan.has_errors:
        report = WorkflowRunReport(
            workflow_id=spec.id,
            run_id=run_id,
            planned_order=(),
            nodes=(),
            diagnostics=tuple(plan.diagnostics),
            started_at_utc=_iso_utc(started_at),
            finished_at_utc=_iso_utc(now()),
            dry_run=dry_run,
        )
        _write_report(report, report_path)
        return report

    planned_order = tuple(node.id for node in plan.nodes)
    nodes_by_id = {node.id: node for node in spec.nodes}
    node_types = _node_types_by_id(spec, provider_registry)
    if dry_run:
        records = tuple(
            NodeRunRecord(
                id=planned.id,
                provider=planned.provider,
                provider_id=planned.provider_id,
                node_type=planned.node_type,
                status=NodeRunStatus.DRY_RUN,
                artifacts=_node_artifacts(nodes_by_id[planned.id]),
            )
            for planned in plan.nodes
        )
        report = WorkflowRunReport(
            workflow_id=spec.id,
            run_id=run_id,
            planned_order=planned_order,
            nodes=records,
            diagnostics=tuple(plan.diagnostics),
            started_at_utc=_iso_utc(started_at),
            finished_at_utc=_iso_utc(now()),
            dry_run=True,
        )
        _write_report(report, report_path)
        return report

    support_diagnostics = _execution_support_diagnostics(
        spec=spec,
        registry=provider_registry,
        node_types=node_types,
    )
    if support_diagnostics:
        records = tuple(
            NodeRunRecord(
                id=planned.id,
                provider=planned.provider,
                provider_id=planned.provider_id,
                node_type=planned.node_type,
                status=NodeRunStatus.UNSUPPORTED,
                artifacts=_node_artifacts(nodes_by_id[planned.id]),
                diagnostics=tuple(
                    diagnostic
                    for diagnostic in support_diagnostics
                    if diagnostic.location == f"nodes.{planned.id}"
                ),
            )
            for planned in plan.nodes
        )
        report = WorkflowRunReport(
            workflow_id=spec.id,
            run_id=run_id,
            planned_order=planned_order,
            nodes=records,
            diagnostics=tuple(plan.diagnostics) + tuple(support_diagnostics),
            started_at_utc=_iso_utc(started_at),
            finished_at_utc=_iso_utc(now()),
            dry_run=False,
        )
        _write_report(report, report_path)
        return report

    records: list[NodeRunRecord] = []
    previous: dict[str, dict[str, Any]] = {}
    failed = False
    for planned in plan.nodes:
        node = nodes_by_id[planned.id]
        provider = provider_registry.get(planned.provider_id or "")
        node_type = node_types[planned.id]
        if failed:
            records.append(
                NodeRunRecord(
                    id=node.id,
                    provider=node.provider,
                    provider_id=planned.provider_id,
                    node_type=planned.node_type,
                    status=NodeRunStatus.SKIPPED,
                    artifacts=_node_artifacts(node),
                )
            )
            continue
        step_started = now()
        try:
            result = provider.execute_node(  # type: ignore[union-attr]
                node,
                node_type,
                context=ExecutionContext(
                    workflow_id=spec.id,
                    run_id=run_id,
                    workflow_source_path=spec.source_path,
                    previous=previous,
                ),
            )
            if not isinstance(result, ProviderExecutionResult):
                raise TypeError("execute_node() must return ProviderExecutionResult.")
            step_status = (
                NodeRunStatus.FAILED
                if _has_error_diagnostics(result.diagnostics)
                else NodeRunStatus.OK
            )
            step_finished = now()
            record = NodeRunRecord(
                id=node.id,
                provider=node.provider,
                provider_id=planned.provider_id,
                node_type=planned.node_type,
                status=step_status,
                started_at_utc=_iso_utc(step_started),
                finished_at_utc=_iso_utc(step_finished),
                duration_seconds=(step_finished - step_started).total_seconds(),
                command=result.command,
                metadata=result.metadata,
                artifacts=result.artifacts or _node_artifacts(node),
                diagnostics=result.diagnostics,
            )
        except Exception as exc:  # noqa: BLE001
            step_finished = now()
            record = NodeRunRecord(
                id=node.id,
                provider=node.provider,
                provider_id=planned.provider_id,
                node_type=planned.node_type,
                status=NodeRunStatus.FAILED,
                started_at_utc=_iso_utc(step_started),
                finished_at_utc=_iso_utc(step_finished),
                duration_seconds=(step_finished - step_started).total_seconds(),
                artifacts=_node_artifacts(node),
                error=f"{type(exc).__name__}: {exc}",
                diagnostics=(
                    Diagnostic(
                        severity=DiagnosticSeverity.ERROR,
                        code="execution.node.failed",
                        message=f"Node '{node.id}' failed: {exc}",
                        location=f"nodes.{node.id}",
                    ),
                ),
            )
        records.append(record)
        previous[node.id] = {
            "status": record.status.value,
            "metadata": record.metadata,
            "artifacts": record.artifacts,
        }
        failed = record.status is NodeRunStatus.FAILED

    report = WorkflowRunReport(
        workflow_id=spec.id,
        run_id=run_id,
        planned_order=planned_order,
        nodes=tuple(records),
        diagnostics=tuple(plan.diagnostics),
        started_at_utc=_iso_utc(started_at),
        finished_at_utc=_iso_utc(now()),
        dry_run=False,
    )
    _write_report(report, report_path)
    return report


def _registry_and_diagnostics(
    *,
    registry: ProviderRegistry | None,
    diagnostics: Sequence[Diagnostic] | None,
) -> tuple[ProviderRegistry, list[Diagnostic]]:
    initial_diagnostics = list(diagnostics or [])
    if registry is not None:
        return registry, initial_diagnostics
    provider_registry, discovery_diagnostics = default_provider_registry()
    initial_diagnostics.extend(discovery_diagnostics)
    return provider_registry, initial_diagnostics


def _node_types_by_id(
    spec: WorkflowSpec,
    registry: ProviderRegistry,
) -> dict[str, NodeTypeMetadata]:
    node_types: dict[str, NodeTypeMetadata] = {}
    for node in spec.nodes:
        resolution = registry.resolve(node.provider)
        provider = registry.get(resolution.provider_id or "")
        if provider is None or resolution.node_type is None:
            continue
        metadata = provider.metadata()
        for node_type in metadata.node_types:
            if node_type.id == resolution.node_type:
                node_types[node.id] = node_type
                break
    return node_types


def _execution_support_diagnostics(
    *,
    spec: WorkflowSpec,
    registry: ProviderRegistry,
    node_types: dict[str, NodeTypeMetadata],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for node in spec.nodes:
        resolution = registry.resolve(node.provider)
        provider = registry.get(resolution.provider_id or "")
        if node.id not in node_types or provider is None:
            continue
        if not hasattr(provider, "execute_node") or not callable(provider.execute_node):
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="execution.provider.unsupported",
                    message=(
                        f"Provider '{resolution.provider_id}' does not support "
                        f"execution for node '{node.id}'."
                    ),
                    location=f"nodes.{node.id}",
                )
            )
    return diagnostics


def _node_artifacts(node) -> dict[str, Any]:
    return node.artifacts if isinstance(node.artifacts, dict) else {}


def _has_error_diagnostics(diagnostics: Sequence[Diagnostic]) -> bool:
    return any(diagnostic.severity is DiagnosticSeverity.ERROR for diagnostic in diagnostics)


def _write_report(report: WorkflowRunReport, report_path: Path | None) -> None:
    if report_path is None:
        return
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _iso_utc(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
