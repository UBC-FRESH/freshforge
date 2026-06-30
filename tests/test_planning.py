"""Non-executing run planning tests."""

from freshforge.loading import load_workflow
from freshforge.planning import create_run_plan
from freshforge.validation import validate_workflow_document


def test_create_run_plan_uses_deterministic_topological_order() -> None:
    spec, diagnostics = load_workflow("examples/stand_treatment_workflow.yaml")
    assert spec is not None
    assert diagnostics == []

    plan = create_run_plan(spec, diagnostics=diagnostics)

    assert not plan.has_errors
    assert [node.id for node in plan.nodes] == [
        "load_inventory",
        "classify_fuel",
        "choose_treatment",
    ]
    assert [node.provider for node in plan.nodes] == [
        "freshforge.example.load_inventory",
        "freshforge.example.classify_fuel",
        "freshforge.example.choose_treatment",
    ]


def test_create_run_plan_refuses_specs_with_error_diagnostics() -> None:
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "bad_demo"},
            "nodes": [{"id": "load", "provider": "example.load", "needs": ["missing"]}],
        }
    )
    assert spec is not None

    plan = create_run_plan(spec, diagnostics=diagnostics)

    assert plan.has_errors
    assert plan.nodes == ()
    assert {diagnostic.code for diagnostic in plan.diagnostics} == {"node.needs.unknown"}
