"""Record construction and serialization tests."""

from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    PlannedNode,
    RunPlan,
    WorkflowNode,
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
