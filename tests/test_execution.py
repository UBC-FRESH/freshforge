"""Workflow execution tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from freshforge.execution import execute_workflow
from freshforge.providers import NodeTypeMetadata, ProviderMetadata, ProviderRegistry
from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    ProviderExecutionResult,
    WorkflowNode,
    WorkflowSpec,
)


class _Clock:
    def __init__(self) -> None:
        self._value = datetime(2026, 1, 1, tzinfo=UTC)

    def __call__(self) -> datetime:
        value = self._value
        self._value += timedelta(seconds=1)
        return value


class _ExecutableProvider:
    def __init__(self, calls: list[str], *, fail_on: str | None = None) -> None:
        self.calls = calls
        self.fail_on = fail_on

    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            id="example.exec",
            version="1",
            node_types=(
                NodeTypeMetadata(id="first", outputs=("first",)),
                NodeTypeMetadata(id="second", inputs=("first",), outputs=("second",)),
                NodeTypeMetadata(id="third", inputs=("second",), outputs=("third",)),
            ),
        )

    def validate_node(self, node, node_type, *, location):
        return ()

    def execute_node(self, node, node_type, *, context):
        self.calls.append(node.id)
        if node.id == self.fail_on:
            return ProviderExecutionResult(
                diagnostics=(
                    Diagnostic(
                        severity=DiagnosticSeverity.ERROR,
                        code="example.failed",
                        message="Example failure.",
                        location=f"nodes.{node.id}",
                    ),
                )
            )
        return ProviderExecutionResult(
            command=("example", node.id),
            metadata={"node": node.id, "run_id": context.run_id},
            artifacts=node.artifacts,
        )


class _ValidateOnlyProvider:
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            id="example.validate",
            version="1",
            node_types=(NodeTypeMetadata(id="load", outputs=("data",)),),
        )

    def validate_node(self, node, node_type, *, location):
        return ()


def test_execute_workflow_dry_run_does_not_call_provider() -> None:
    calls: list[str] = []
    registry = ProviderRegistry()
    registry.register(_ExecutableProvider(calls))
    spec = _spec()

    report = execute_workflow(
        spec,
        run_id="run-1",
        registry=registry,
        dry_run=True,
        now_fn=_Clock(),
    )

    assert calls == []
    assert not report.failed
    assert report.dry_run is True
    assert [node.status.value for node in report.nodes] == ["dry_run"] * 3


def test_execute_workflow_runs_nodes_in_plan_order() -> None:
    calls: list[str] = []
    registry = ProviderRegistry()
    registry.register(_ExecutableProvider(calls))

    report = execute_workflow(
        _spec(),
        run_id="run-1",
        registry=registry,
        now_fn=_Clock(),
    )

    assert calls == ["first", "second", "third"]
    assert not report.failed
    assert [node.status.value for node in report.nodes] == ["ok", "ok", "ok"]
    assert report.nodes[0].command == ("example", "first")
    assert report.nodes[0].metadata["run_id"] == "run-1"


def test_execute_workflow_stops_after_failed_node() -> None:
    calls: list[str] = []
    registry = ProviderRegistry()
    registry.register(_ExecutableProvider(calls, fail_on="second"))

    report = execute_workflow(
        _spec(),
        run_id="run-1",
        registry=registry,
        now_fn=_Clock(),
    )

    assert calls == ["first", "second"]
    assert report.failed
    assert [node.status.value for node in report.nodes] == ["ok", "failed", "skipped"]


def test_execute_workflow_reports_missing_execution_hook() -> None:
    registry = ProviderRegistry()
    registry.register(_ValidateOnlyProvider())
    spec = WorkflowSpec(
        id="unsupported",
        nodes=(
            WorkflowNode(
                id="load",
                provider="example.validate.load",
                outputs={"data": "data"},
            ),
        ),
    )

    report = execute_workflow(
        spec,
        run_id="run-1",
        registry=registry,
        now_fn=_Clock(),
    )

    assert report.failed
    assert report.nodes[0].status.value == "unsupported"
    assert "execution.provider.unsupported" in {
        diagnostic.code for diagnostic in report.diagnostics
    }


def _spec() -> WorkflowSpec:
    return WorkflowSpec(
        id="exec_demo",
        nodes=(
            WorkflowNode(
                id="first",
                provider="example.exec.first",
                outputs={"first": "first"},
                artifacts={"first": "first.json"},
            ),
            WorkflowNode(
                id="second",
                provider="example.exec.second",
                needs=("first",),
                inputs={"first": "first.first"},
                outputs={"second": "second"},
            ),
            WorkflowNode(
                id="third",
                provider="example.exec.third",
                needs=("second",),
                inputs={"second": "second.second"},
                outputs={"third": "third"},
            ),
        ),
    )
