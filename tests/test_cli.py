"""CLI smoke tests."""

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
    assert "workflow DSL not implemented yet" in result.stdout
