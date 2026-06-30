"""Workflow loading and validation tests."""

from pathlib import Path

import pytest

from freshforge.loading import load_workflow
from freshforge.validation import validate_workflow_document, validate_workflow_with_providers

EXAMPLE_WORKFLOW = Path("examples/stand_treatment_workflow.yaml")


def diagnostic_codes(document: object) -> set[str]:
    return {diagnostic.code for diagnostic in validate_workflow_document(document)[1]}


def test_load_yaml_example_workflow() -> None:
    spec, diagnostics = load_workflow(EXAMPLE_WORKFLOW)

    assert diagnostics == []
    assert spec is not None
    assert spec.id == "stand_treatment_demo"
    assert [node.id for node in spec.nodes] == [
        "load_inventory",
        "classify_fuel",
        "choose_treatment",
    ]


def test_load_json_workflow(tmp_path: Path) -> None:
    path = tmp_path / "workflow.json"
    path.write_text(
        """
        {
          "workflow": {"id": "json_demo"},
          "nodes": [{"id": "load", "provider": "example.load"}]
        }
        """,
        encoding="utf-8",
    )

    spec, diagnostics = load_workflow(path)

    assert diagnostics == []
    assert spec is not None
    assert spec.id == "json_demo"


def test_load_malformed_yaml_returns_diagnostic(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("workflow: [", encoding="utf-8")

    spec, diagnostics = load_workflow(path)

    assert spec is None
    assert {diagnostic.code for diagnostic in diagnostics} == {"source.load_failed"}


def test_load_unsupported_suffix_returns_diagnostic(tmp_path: Path) -> None:
    path = tmp_path / "workflow.txt"
    path.write_text("", encoding="utf-8")

    spec, diagnostics = load_workflow(path)

    assert spec is None
    assert {diagnostic.code for diagnostic in diagnostics} == {"source.load_failed"}


@pytest.mark.parametrize(
    ("document", "expected_code"),
    [
        ([], "source.not_mapping"),
        ({"nodes": []}, "workflow.not_mapping"),
        ({"workflow": {}, "nodes": []}, "workflow.id.required"),
        (
            {"workflow": {"id": "Bad Id"}, "nodes": []},
            "workflow.id.invalid",
        ),
        (
            {"workflow": {"id": "demo"}, "nodes": [{"provider": "example.load"}]},
            "node.id.required",
        ),
        (
            {"workflow": {"id": "demo"}, "nodes": [{"id": "load"}]},
            "node.provider.required",
        ),
        (
            {"workflow": {"id": "demo"}, "nodes": [{"id": "load", "provider": "x"}] * 2},
            "node.id.duplicate",
        ),
        (
            {
                "workflow": {"id": "demo"},
                "nodes": [{"id": "load", "provider": "x", "needs": ["missing"]}],
            },
            "node.needs.unknown",
        ),
        (
            {"workflow": {"id": "demo"}, "nodes": [{"id": "load", "provider": "x", "inputs": []}]},
            "node.inputs.not_mapping",
        ),
        (
            {
                "workflow": {"id": "demo"},
                "nodes": [{"id": "load", "provider": "x", "artifacts": "out.txt"}],
            },
            "node.artifacts.invalid_shape",
        ),
    ],
)
def test_validation_error_cases(document: object, expected_code: str) -> None:
    assert expected_code in diagnostic_codes(document)


def test_validation_detects_cycles() -> None:
    document = {
        "workflow": {"id": "cycle_demo"},
        "nodes": [
            {"id": "first", "provider": "example.first", "needs": ["second"]},
            {"id": "second", "provider": "example.second", "needs": ["first"]},
        ],
    }

    assert "workflow.cycle" in diagnostic_codes(document)


def test_provider_aware_validation_accepts_example_workflow() -> None:
    spec, diagnostics = load_workflow(EXAMPLE_WORKFLOW)
    assert spec is not None

    provider_diagnostics = validate_workflow_with_providers(
        spec,
        structural_diagnostics=diagnostics,
    )

    assert provider_diagnostics == []


def test_provider_aware_validation_reports_missing_provider() -> None:
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "demo"},
            "nodes": [{"id": "load", "provider": "freshforge.missing.load"}],
        }
    )
    assert spec is not None

    provider_diagnostics = validate_workflow_with_providers(
        spec,
        structural_diagnostics=diagnostics,
    )

    assert "node.provider.unavailable" in {
        diagnostic.code for diagnostic in provider_diagnostics
    }


def test_provider_aware_validation_reports_unknown_node_type() -> None:
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "demo"},
            "nodes": [{"id": "load", "provider": "freshforge.example.unknown"}],
        }
    )
    assert spec is not None

    provider_diagnostics = validate_workflow_with_providers(
        spec,
        structural_diagnostics=diagnostics,
    )

    assert "node.provider.node_type.unknown" in {
        diagnostic.code for diagnostic in provider_diagnostics
    }


def test_provider_aware_validation_reports_provider_specific_diagnostics() -> None:
    spec, diagnostics = validate_workflow_document(
        {
            "workflow": {"id": "demo"},
            "nodes": [{"id": "load", "provider": "freshforge.example.load_inventory"}],
        }
    )
    assert spec is not None

    provider_diagnostics = validate_workflow_with_providers(
        spec,
        structural_diagnostics=diagnostics,
    )

    assert "node.outputs.missing" in {diagnostic.code for diagnostic in provider_diagnostics}
