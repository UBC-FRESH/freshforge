from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from freshforge.execution import artifact_paths, run_workflow
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
