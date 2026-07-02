from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from freshforge.execution import artifact_paths
from freshforge.matrix import (
    expand_workflow_matrix,
    load_workflow_matrix,
    plan_workflow_matrix,
    run_workflow_matrix,
    validate_workflow_matrix_document,
)
from freshforge.providers import NodeTypeMetadata, ProviderMetadata, ProviderRegistry
from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    ProviderRunResult,
    RunStatus,
    WorkflowNode,
)

EXAMPLE_MATRIX = Path("examples/run_matrix.yaml")


class WritingProvider:
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            id="test.runner",
            version="test",
            node_types=(
                NodeTypeMetadata(
                    id="write",
                    name="Write",
                    artifacts=("out",),
                ),
            ),
        )

    def validate_node(
        self,
        node: WorkflowNode,
        node_type: NodeTypeMetadata,
        *,
        location: str,
    ) -> tuple[Diagnostic, ...]:
        if not isinstance(node.artifacts, dict) or "out" not in node.artifacts:
            return (
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="test.out.required",
                    message="Test node requires an out artifact.",
                    location=f"{location}.artifacts.out",
                ),
            )
        return ()

    def run_node(
        self,
        node: WorkflowNode,
        node_type: NodeTypeMetadata,
        *,
        context: Any,
    ) -> ProviderRunResult:
        paths = artifact_paths(node, context)
        out = paths["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(str(node.parameters.get("message", "")), encoding="utf-8")
        return ProviderRunResult(
            status=RunStatus.SUCCESS,
            outputs={"written": str(out)},
            artifacts={"out": str(out)},
        )


def test_load_and_expand_axis_product_example_matrix() -> None:
    matrix, diagnostics = load_workflow_matrix(EXAMPLE_MATRIX)

    assert diagnostics == []
    assert matrix is not None
    assert matrix.id == "treatment_matrix_demo"

    expanded = expand_workflow_matrix(matrix)

    assert [case.case.id for case in expanded] == [
        "strategy-baseline",
        "strategy-thinning",
    ]
    assert [case.namespace for case in expanded] == [
        "treatment_matrix_demo/strategy-baseline",
        "treatment_matrix_demo/strategy-thinning",
    ]
    assert expanded[0].workflow is not None
    assert expanded[0].workflow.id == "matrix_strategy-baseline_demo"
    assert expanded[0].workflow.nodes[1].parameters == {"classification": "baseline"}


def test_explicit_cases_expand_with_custom_namespace(tmp_path: Path) -> None:
    template = tmp_path / "template.yaml"
    template.write_text(
        """
        workflow:
          id: explicit_${matrix.case_id}
        nodes:
          - id: write
            provider: test.runner.write
            parameters:
              message: ${matrix.message}
            artifacts:
              out: reports/${matrix.case_id}.txt
        """,
        encoding="utf-8",
    )
    matrix_path = tmp_path / "matrix.yaml"
    matrix_path.write_text(
        """
        matrix:
          id: explicit_demo
          workflow_template: template.yaml
        cases:
          - id: first
            namespace: custom/first
            variables:
              message: hello
        """,
        encoding="utf-8",
    )

    matrix, diagnostics = load_workflow_matrix(matrix_path)
    assert matrix is not None
    assert diagnostics == []

    expanded = expand_workflow_matrix(matrix)

    assert len(expanded) == 1
    assert expanded[0].namespace == "custom/first"
    assert expanded[0].workflow is not None
    assert expanded[0].workflow.nodes[0].parameters["message"] == "hello"


def test_matrix_validation_rejects_ambiguous_shape() -> None:
    matrix, diagnostics = validate_workflow_matrix_document(
        {
            "matrix": {"id": "bad", "workflow_template": "template.yaml"},
            "cases": [{"id": "one"}],
            "axes": [{"id": "strategy", "values": [{"id": "baseline"}]}],
        }
    )

    assert matrix is not None
    assert "matrix.shape.ambiguous" in {diagnostic.code for diagnostic in diagnostics}


def test_matrix_validation_rejects_invalid_case_id() -> None:
    matrix, diagnostics = validate_workflow_matrix_document(
        {
            "matrix": {"id": "demo", "workflow_template": "template.yaml"},
            "cases": [{"id": "Bad Case"}],
        }
    )

    assert matrix is not None
    assert "matrix.case.id.invalid" in {diagnostic.code for diagnostic in diagnostics}


def test_missing_placeholder_produces_diagnostic(tmp_path: Path) -> None:
    template = tmp_path / "template.yaml"
    template.write_text(
        """
        workflow:
          id: missing_${matrix.unknown}
        nodes: []
        """,
        encoding="utf-8",
    )
    matrix_path = tmp_path / "matrix.yaml"
    matrix_path.write_text(
        """
        matrix:
          id: missing_demo
          workflow_template: template.yaml
        cases:
          - id: first
        """,
        encoding="utf-8",
    )

    matrix, diagnostics = load_workflow_matrix(matrix_path)
    assert matrix is not None
    expanded = expand_workflow_matrix(matrix, diagnostics=diagnostics)

    codes = {diagnostic.code for diagnostic in expanded[0].diagnostics}
    assert "matrix.placeholder.missing" in codes
    assert "workflow.id.invalid" in codes


def test_invalid_namespace_produces_diagnostic(tmp_path: Path) -> None:
    template = tmp_path / "template.yaml"
    template.write_text(
        """
        workflow:
          id: namespace_demo
        nodes: []
        """,
        encoding="utf-8",
    )
    matrix_path = tmp_path / "matrix.yaml"
    matrix_path.write_text(
        """
        matrix:
          id: namespace_demo
          workflow_template: template.yaml
        cases:
          - id: first
            namespace: ../bad
        """,
        encoding="utf-8",
    )

    matrix, diagnostics = load_workflow_matrix(matrix_path)
    assert matrix is not None
    expanded = expand_workflow_matrix(matrix, diagnostics=diagnostics)

    assert "run.namespace.invalid" in {diagnostic.code for diagnostic in expanded[0].diagnostics}


def test_duplicate_axis_variables_produce_diagnostic(tmp_path: Path) -> None:
    template = tmp_path / "template.yaml"
    template.write_text(
        """
        workflow:
          id: duplicate_${matrix.case_id}
        nodes: []
        """,
        encoding="utf-8",
    )
    matrix_path = tmp_path / "matrix.yaml"
    matrix_path.write_text(
        """
        matrix:
          id: duplicate_demo
          workflow_template: template.yaml
        axes:
          - id: first
            values:
              - id: a
                variables:
                  shared: one
          - id: second
            values:
              - id: b
                variables:
                  shared: two
        """,
        encoding="utf-8",
    )

    matrix, diagnostics = load_workflow_matrix(matrix_path)
    assert matrix is not None
    expanded = expand_workflow_matrix(matrix, diagnostics=diagnostics)

    assert "matrix.axis.variables.duplicate" in {
        diagnostic.code for diagnostic in expanded[0].diagnostics
    }


def test_matrix_plan_uses_existing_workflow_planner() -> None:
    matrix, diagnostics = load_workflow_matrix(EXAMPLE_MATRIX)
    assert matrix is not None

    plan = plan_workflow_matrix(matrix, diagnostics=diagnostics)

    assert plan.ok
    assert [case.case_id for case in plan.cases] == [
        "strategy-baseline",
        "strategy-thinning",
    ]
    assert [case.plan.workflow_id for case in plan.cases if case.plan is not None] == [
        "matrix_strategy-baseline_demo",
        "matrix_strategy-thinning_demo",
    ]


def test_matrix_run_executes_all_cases_and_resolves_namespaced_artifacts(tmp_path: Path) -> None:
    matrix_path = _write_executable_matrix(tmp_path)
    matrix, diagnostics = load_workflow_matrix(matrix_path)
    assert matrix is not None

    registry = ProviderRegistry()
    registry.register(WritingProvider())
    result = run_workflow_matrix(
        matrix,
        diagnostics=diagnostics,
        registry=registry,
        workdir=tmp_path / "runs",
    )

    assert result.ok
    assert [case.case_id for case in result.cases] == ["first", "second"]
    assert (tmp_path / "runs" / "write_demo" / "first" / "reports" / "first.txt").read_text(
        encoding="utf-8"
    ) == "hello"
    assert (tmp_path / "runs" / "write_demo" / "second" / "reports" / "second.txt").read_text(
        encoding="utf-8"
    ) == "goodbye"
    summary = result.summary()
    assert summary.ok
    assert summary.case_count == 2
    assert summary.succeeded_count == 2


def test_matrix_run_fail_fast_stops_after_first_failure() -> None:
    matrix, diagnostics = load_workflow_matrix(EXAMPLE_MATRIX)
    assert matrix is not None

    result = run_workflow_matrix(matrix, diagnostics=diagnostics, fail_fast=True)

    assert not result.ok
    assert [case.case_id for case in result.cases] == ["strategy-baseline"]


def test_matrix_run_without_fail_fast_runs_all_cases() -> None:
    matrix, diagnostics = load_workflow_matrix(EXAMPLE_MATRIX)
    assert matrix is not None

    result = run_workflow_matrix(matrix, diagnostics=diagnostics, fail_fast=False)

    assert not result.ok
    assert [case.case_id for case in result.cases] == [
        "strategy-baseline",
        "strategy-thinning",
    ]
    assert result.summary().failed_count == 2


def test_matrix_records_serialize_deterministically() -> None:
    matrix, diagnostics = load_workflow_matrix(EXAMPLE_MATRIX)
    assert matrix is not None
    expanded = expand_workflow_matrix(matrix, diagnostics=diagnostics)

    payload = expanded[0].to_dict()

    assert json.loads(json.dumps(payload, sort_keys=True))["case"]["id"] == "strategy-baseline"


def _write_executable_matrix(tmp_path: Path) -> Path:
    template = tmp_path / "template.yaml"
    template.write_text(
        """
        workflow:
          id: write_${matrix.case_id}
        nodes:
          - id: write
            provider: test.runner.write
            parameters:
              message: ${matrix.message}
            artifacts:
              out: reports/${matrix.case_id}.txt
        """,
        encoding="utf-8",
    )
    matrix_path = tmp_path / "matrix.yaml"
    matrix_path.write_text(
        """
        matrix:
          id: write_demo
          workflow_template: template.yaml
        cases:
          - id: first
            variables:
              message: hello
          - id: second
            variables:
              message: goodbye
        """,
        encoding="utf-8",
    )
    return matrix_path
