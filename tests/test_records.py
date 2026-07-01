"""Record construction and serialization tests."""

from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    NodeRunResult,
    PlannedNode,
    RunPlan,
    RunStatus,
    WorkflowNode,
    WorkflowRunResult,
    WorkflowSpec,
)


def test_workflow_spec_to_dict_is_json_serializable_shape() -> None:
    spec = WorkflowSpec(
        id="demo",
        name="Demo",
        nodes=(
            WorkflowNode(
                id="load_inventory",
                provider="freshforge.example.load_inventory",
                outputs={"inventory": "stand_inventory"},
            ),
        ),
    )

    assert spec.to_dict() == {
        "workflow": {"id": "demo", "name": "Demo"},
        "nodes": [
            {
                "id": "load_inventory",
                "provider": "freshforge.example.load_inventory",
                "outputs": {"inventory": "stand_inventory"},
            }
        ],
    }


def test_run_plan_to_dict_includes_diagnostics() -> None:
    plan = RunPlan(
        workflow_id="demo",
        nodes=(PlannedNode(id="load", provider="example.load"),),
        diagnostics=(
            Diagnostic(
                severity=DiagnosticSeverity.WARNING,
                code="example.warning",
                message="Example warning.",
                location="nodes[0]",
            ),
        ),
    )

    assert plan.to_dict() == {
        "workflow_id": "demo",
        "nodes": [
            {
                "id": "load",
                "provider": "example.load",
                "provider_id": None,
                "node_type": None,
                "provider_available": False,
                "needs": [],
            }
        ],
        "diagnostics": [
            {
                "severity": "warning",
                "code": "example.warning",
                "message": "Example warning.",
                "location": "nodes[0]",
            }
        ],
    }


def test_workflow_run_result_to_dict_includes_namespace_and_full_nodes() -> None:
    result = WorkflowRunResult(
        workflow_id="demo",
        run_namespace="strategy/output-columns",
        status=RunStatus.SUCCESS,
        nodes=(
            NodeRunResult(
                id="load",
                provider="example.load",
                provider_id="example",
                node_type="load",
                status=RunStatus.SUCCESS,
                outputs={"value": "ok"},
                artifacts={"report": "runs/demo/report.json"},
            ),
        ),
    )

    assert result.to_dict() == {
        "workflow_id": "demo",
        "run_namespace": "strategy/output-columns",
        "status": "success",
        "nodes": [
            {
                "id": "load",
                "provider": "example.load",
                "provider_id": "example",
                "node_type": "load",
                "status": "success",
                "outputs": {"value": "ok"},
                "artifacts": {"report": "runs/demo/report.json"},
                "diagnostics": [],
                "data": {},
            }
        ],
        "diagnostics": [],
    }
