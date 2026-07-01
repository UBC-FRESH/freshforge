from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from freshforge.execution import RunContext, artifact_paths, run_workflow
from freshforge.providers import NodeTypeMetadata, ProviderMetadata, ProviderRegistry
from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    ProviderRunResult,
    RunStatus,
    WorkflowNode,
)
from freshforge.validation import validate_workflow_document


class RecordingProvider:
    def __init__(self, seen: list[str]) -> None:
        self.seen = seen

    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            id="test.exec",
            version="0",
            node_types=(
                NodeTypeMetadata(id="write", outputs=("value",), artifacts=("report",)),
                NodeTypeMetadata(id="fail", outputs=("value",)),
            ),
        )

    def validate_node(
        self,
        node: WorkflowNode,
        node_type: NodeTypeMetadata,
        *,
        location: str,
    ) -> tuple[Diagnostic, ...]:
        return ()

    def run_node(
        self,
        node: WorkflowNode,
        node_type: NodeTypeMetadata,
        *,
        context: Any,
    ) -> ProviderRunResult:
        self.seen.append(node.id)
        if node_type.id == "fail":
            return ProviderRunResult(
                status=RunStatus.FAILED,
                diagnostics=(
                    Diagnostic(
                        severity=DiagnosticSeverity.ERROR,
                        code="fixture.failed",
                        message="fixture failure",
                        location=f"nodes.{node.id}",
                    ),
                ),
            )
        paths = artifact_paths(node, context)
        paths["report"].parent.mkdir(parents=True, exist_ok=True)
        paths["report"].write_text(json.dumps({"node": node.id}), encoding="utf-8")
        return ProviderRunResult(
            status=RunStatus.SUCCESS,
            outputs={"value": node.id},
            artifacts={"report": str(paths["report"])},
        )


def test_run_workflow_executes_nodes_in_plan_order_and_resolves_workdir(tmp_path: Path) -> None:
    seen: list[str] = []
    registry = ProviderRegistry()
    registry.register(RecordingProvider(seen))
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "exec_demo"},
            "nodes": [
                {
                    "id": "first",
                    "provider": "test.exec.write",
                    "outputs": {"value": "first_value"},
                    "artifacts": {"report": "reports/first.json"},
                },
                {
                    "id": "second",
                    "provider": "test.exec.write",
                    "needs": ["first"],
                    "outputs": {"value": "second_value"},
                    "artifacts": {"report": "reports/second.json"},
                },
            ],
        }
    )
    assert spec is not None

    result = run_workflow(spec, diagnostics=diagnostics, registry=registry, workdir=tmp_path)

    assert result.ok
    assert result.status is RunStatus.SUCCESS
    assert seen == ["first", "second"]
    assert [node.id for node in result.nodes] == ["first", "second"]
    assert result.nodes[0].outputs == {"value": "first"}
    assert (tmp_path / "reports" / "first.json").exists()
    assert result.nodes[0].artifacts["report"] == str(tmp_path / "reports" / "first.json")
    assert result.run_namespace is None
    assert result.to_dict()["run_namespace"] is None


def test_run_workflow_stops_on_failed_node(tmp_path: Path) -> None:
    seen: list[str] = []
    registry = ProviderRegistry()
    registry.register(RecordingProvider(seen))
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "failure_demo"},
            "nodes": [
                {"id": "first", "provider": "test.exec.fail", "outputs": {"value": "first_value"}},
                {
                    "id": "second",
                    "provider": "test.exec.write",
                    "needs": ["first"],
                    "outputs": {"value": "second_value"},
                    "artifacts": {"report": "reports/second.json"},
                },
            ],
        }
    )
    assert spec is not None

    result = run_workflow(spec, diagnostics=diagnostics, registry=registry, workdir=tmp_path)

    assert not result.ok
    assert result.status is RunStatus.FAILED
    assert seen == ["first"]
    assert [node.id for node in result.nodes] == ["first"]
    assert result.diagnostics[0].code == "fixture.failed"
    summary = result.summary()
    assert summary.status is RunStatus.FAILED
    assert summary.node_count == 1
    assert summary.failed_count == 1
    assert summary.error_count == 1


def test_run_workflow_reports_plan_only_provider_as_unsupported() -> None:
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "unsupported_demo"},
            "nodes": [
                {
                    "id": "load",
                    "provider": "freshforge.example.load_inventory",
                    "outputs": {"inventory": "inventory"},
                }
            ],
        }
    )
    assert spec is not None

    result = run_workflow(spec, diagnostics=diagnostics)

    assert not result.ok
    assert result.nodes[0].status is RunStatus.FAILED
    assert result.nodes[0].diagnostics[0].code == "node.execution.unsupported"


def test_run_workflow_resolves_relative_artifacts_under_namespace(tmp_path: Path) -> None:
    seen: list[str] = []
    registry = ProviderRegistry()
    registry.register(RecordingProvider(seen))
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "namespace_demo"},
            "nodes": [
                {
                    "id": "write",
                    "provider": "test.exec.write",
                    "outputs": {"value": "value"},
                    "artifacts": {"report": "reports/out.json"},
                }
            ],
        }
    )
    assert spec is not None

    result = run_workflow(
        spec,
        diagnostics=diagnostics,
        registry=registry,
        workdir=tmp_path,
        run_namespace="strategy/output-columns",
    )

    expected = tmp_path / "strategy" / "output-columns" / "reports" / "out.json"
    assert result.ok
    assert result.run_namespace == "strategy/output-columns"
    assert expected.exists()
    assert result.nodes[0].artifacts["report"] == str(expected)
    assert result.summary().run_namespace == "strategy/output-columns"


def test_run_workflow_rejects_invalid_namespace_before_execution(tmp_path: Path) -> None:
    seen: list[str] = []
    registry = ProviderRegistry()
    registry.register(RecordingProvider(seen))
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "bad_namespace_demo"},
            "nodes": [
                {
                    "id": "write",
                    "provider": "test.exec.write",
                    "outputs": {"value": "value"},
                    "artifacts": {"report": "reports/out.json"},
                }
            ],
        }
    )
    assert spec is not None

    result = run_workflow(
        spec,
        diagnostics=diagnostics,
        registry=registry,
        workdir=tmp_path,
        run_namespace="../bad",
    )

    assert not result.ok
    assert seen == []
    assert result.nodes == ()
    assert result.diagnostics[0].code == "run.namespace.invalid"


def test_artifact_paths_do_not_prefix_absolute_paths_with_namespace(tmp_path: Path) -> None:
    absolute = tmp_path / "absolute.json"
    context = RunContext(
        workflow_id="absolute_demo",
        workdir=tmp_path / "work",
        run_namespace="demo",
    )
    node = WorkflowNode(
        id="write",
        provider="test.exec.write",
        artifacts={"report": str(absolute)},
    )

    assert artifact_paths(node, context)["report"] == absolute


def test_workflow_run_summary_counts_artifacts_and_diagnostics(tmp_path: Path) -> None:
    seen: list[str] = []
    registry = ProviderRegistry()
    registry.register(RecordingProvider(seen))
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "summary_demo"},
            "nodes": [
                {
                    "id": "write",
                    "provider": "test.exec.write",
                    "outputs": {"value": "value"},
                    "artifacts": {"report": "reports/out.json"},
                }
            ],
        }
    )
    assert spec is not None

    result = run_workflow(spec, diagnostics=diagnostics, registry=registry, workdir=tmp_path)
    summary = result.summary()

    assert summary.ok
    assert summary.to_dict() == {
        "workflow_id": "summary_demo",
        "run_namespace": None,
        "status": "success",
        "node_count": 1,
        "succeeded_count": 1,
        "failed_count": 0,
        "skipped_count": 0,
        "diagnostic_count": 0,
        "error_count": 0,
        "warning_count": 0,
        "artifact_count": 1,
        "nodes": [
            {
                "id": "write",
                "provider_id": "test.exec",
                "node_type": "write",
                "status": "success",
                "diagnostic_count": 0,
                "error_count": 0,
                "warning_count": 0,
                "artifact_count": 1,
                "artifacts": {"report": str(tmp_path / "reports" / "out.json")},
            }
        ],
    }
