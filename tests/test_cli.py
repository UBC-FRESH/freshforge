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
    assert "0.1.0a1 public alpha" in result.stdout


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
    assert payload["run"]["nodes"][0]["diagnostics"][0]["code"] == "node.execution.unsupported"
