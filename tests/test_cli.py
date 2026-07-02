"""CLI smoke tests."""

import json
from pathlib import Path

from typer.testing import CliRunner

from freshforge import __version__
from freshforge.cli import app

runner = CliRunner()


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Workflow-as-code" in result.stdout


def test_cli_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert f"freshforge {__version__}" in result.stdout


def test_cli_info() -> None:
    result = runner.invoke(app, ["info"])

    assert result.exit_code == 0
    assert "FreshForge" in result.stdout
    assert "0.1.0a5 public alpha" in result.stdout
    assert "matrices" in result.stdout


def test_cli_providers() -> None:
    result = runner.invoke(app, ["providers"])

    assert result.exit_code == 0
    assert "freshforge.example" in result.stdout
    assert "freshforge.fixture" in result.stdout
    assert "load_inventory" in result.stdout


def test_cli_providers_json_output() -> None:
    result = runner.invoke(app, ["providers", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    provider_ids = [provider["id"] for provider in payload["providers"]]
    assert payload["ok"] is True
    assert "freshforge.example" in provider_ids
    assert "freshforge.fixture" in provider_ids


def test_cli_validate_example_success() -> None:
    result = runner.invoke(app, ["validate", "examples/stand_treatment_workflow.yaml"])

    assert result.exit_code == 0
    assert "Validation passed" in result.stdout
    assert "stand_treatment_demo" in result.stdout


def test_cli_validate_failure_exit_code(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(
        """
        workflow:
          id: bad_demo
        nodes:
          - id: load
            provider: example.load
            needs: [missing]
        """,
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", str(path)])

    assert result.exit_code == 1
    assert "node.needs.unknown" in result.stdout


def test_cli_validate_json_output() -> None:
    result = runner.invoke(app, ["validate", "examples/stand_treatment_workflow.yaml", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["workflow"]["workflow"]["id"] == "stand_treatment_demo"


def test_cli_validate_multi_provider_example_success() -> None:
    result = runner.invoke(app, ["validate", "examples/ecosystem_adapter_workflow.yaml"])

    assert result.exit_code == 0
    assert "Validation passed" in result.stdout
    assert "ecosystem_adapter_demo" in result.stdout


def test_cli_inspect_example_success() -> None:
    result = runner.invoke(app, ["inspect", "examples/stand_treatment_workflow.yaml"])

    assert result.exit_code == 0
    assert "Workflow: stand_treatment_demo" in result.stdout
    assert "freshforge.example.load_inventory" in result.stdout


def test_cli_inspect_json_output() -> None:
    result = runner.invoke(app, ["inspect", "examples/stand_treatment_workflow.yaml", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["providers"][0]["provider_id"] == "freshforge.example"
    assert payload["providers"][0]["node_type"] == "load_inventory"


def test_cli_inspect_multi_provider_json_output() -> None:
    result = runner.invoke(app, ["inspect", "examples/ecosystem_adapter_workflow.yaml", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    provider_ids = {provider["provider_id"] for provider in payload["providers"]}
    assert payload["ok"] is True
    assert provider_ids == {"freshforge.example", "freshforge.fixture"}


def test_cli_plan_example_success() -> None:
    result = runner.invoke(app, ["plan", "examples/stand_treatment_workflow.yaml"])

    assert result.exit_code == 0
    assert "Run plan" in result.stdout
    assert "1. load_inventory" in result.stdout
    assert "3. choose_treatment" in result.stdout


def test_cli_plan_json_output() -> None:
    result = runner.invoke(app, ["plan", "examples/stand_treatment_workflow.yaml", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert [node["id"] for node in payload["plan"]["nodes"]] == [
        "load_inventory",
        "classify_fuel",
        "choose_treatment",
    ]
    assert payload["plan"]["nodes"][0]["provider_id"] == "freshforge.example"
    assert payload["plan"]["nodes"][0]["node_type"] == "load_inventory"
    assert payload["plan"]["nodes"][0]["provider_available"] is True


def test_cli_plan_multi_provider_json_output() -> None:
    result = runner.invoke(app, ["plan", "examples/ecosystem_adapter_workflow.yaml", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert [node["id"] for node in payload["plan"]["nodes"]] == [
        "load_inventory",
        "summarize_inventory",
        "check_yields",
        "declare_scenario_report",
    ]
    assert {node["provider_id"] for node in payload["plan"]["nodes"]} == {
        "freshforge.example",
        "freshforge.fixture",
    }


def test_cli_run_plan_only_provider_fails_with_json_diagnostic() -> None:
    result = runner.invoke(app, ["run", "examples/stand_treatment_workflow.yaml", "--json"])

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["run"]["status"] == "failed"
    assert payload["run"]["run_namespace"] is None
    assert payload["summary"]["status"] == "failed"
    assert payload["run"]["nodes"][0]["diagnostics"][0]["code"] == "node.execution.unsupported"


def test_cli_run_json_accepts_namespace() -> None:
    result = runner.invoke(
        app,
        [
            "run",
            "examples/stand_treatment_workflow.yaml",
            "--json",
            "--namespace",
            "demo",
        ],
    )

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["run"]["run_namespace"] == "demo"
    assert payload["summary"]["run_namespace"] == "demo"


def test_cli_run_human_output_includes_namespace_and_summary() -> None:
    result = runner.invoke(
        app,
        [
            "run",
            "examples/stand_treatment_workflow.yaml",
            "--namespace",
            "demo",
        ],
    )

    assert result.exit_code == 1
    assert "Namespace: demo" in result.stdout
    assert "Summary:" in result.stdout


def test_cli_run_rejects_invalid_namespace() -> None:
    result = runner.invoke(
        app,
        [
            "run",
            "examples/stand_treatment_workflow.yaml",
            "--json",
            "--namespace",
            "../bad",
        ],
    )

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["run"]["diagnostics"][0]["code"] == "run.namespace.invalid"
    assert payload["summary"]["error_count"] == 1


def test_cli_matrix_expand_json_output() -> None:
    result = runner.invoke(app, ["matrix", "expand", "examples/run_matrix.yaml", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["matrix"]["matrix"]["id"] == "treatment_matrix_demo"
    assert [case["case"]["id"] for case in payload["cases"]] == [
        "strategy-baseline",
        "strategy-thinning",
    ]


def test_cli_matrix_plan_json_output() -> None:
    result = runner.invoke(app, ["matrix", "plan", "examples/run_matrix.yaml", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["plan"]["matrix_id"] == "treatment_matrix_demo"
    assert [case["workflow_id"] for case in payload["plan"]["cases"]] == [
        "matrix_strategy-baseline_demo",
        "matrix_strategy-thinning_demo",
    ]


def test_cli_matrix_run_json_output() -> None:
    result = runner.invoke(app, ["matrix", "run", "examples/run_matrix.yaml", "--json"])

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["run"]["matrix_id"] == "treatment_matrix_demo"
    assert payload["summary"]["case_count"] == 2
    assert payload["summary"]["failed_count"] == 2


def test_cli_matrix_run_human_output_includes_case_counts() -> None:
    result = runner.invoke(app, ["matrix", "run", "examples/run_matrix.yaml"])

    assert result.exit_code == 1
    assert "Matrix run failed." in result.stdout
    assert "Summary:" in result.stdout
    assert "strategy-baseline" in result.stdout
    assert "strategy-thinning" in result.stdout


def test_cli_matrix_invalid_input_exits_nonzero_with_json_diagnostic(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(
        """
        matrix:
          id: Bad Matrix
          workflow_template: missing.yaml
        cases:
          - id: first
        """,
        encoding="utf-8",
    )

    result = runner.invoke(app, ["matrix", "expand", str(path), "--json"])

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert "matrix.id.invalid" in {diagnostic["code"] for diagnostic in payload["diagnostics"]}
