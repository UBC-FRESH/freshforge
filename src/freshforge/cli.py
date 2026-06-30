"""Command-line interface for FreshForge."""

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from freshforge import __version__
from freshforge.loading import load_workflow
from freshforge.planning import create_run_plan
from freshforge.records import Diagnostic, DiagnosticSeverity

app = typer.Typer(
    add_completion=False,
    help="Workflow-as-code for open forest resources and ecosystem services modelling.",
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"freshforge {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            help="Show the FreshForge version and exit.",
            is_eager=True,
        ),
    ] = False,
) -> None:
    """FreshForge command-line interface."""


@app.command()
def info() -> None:
    """Print a short package status summary."""
    console.print("FreshForge")
    console.print(f"Version: {__version__}")
    console.print("Status: Phase 2 provisional workflow records, validation, and planning.")


@app.command(name="validate")
def validate_command(
    path: Annotated[Path, typer.Argument(help="Path to a YAML or JSON workflow spec.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic JSON output."),
    ] = False,
) -> None:
    """Validate a workflow spec without executing it."""
    spec, diagnostics = load_workflow(path)
    has_errors = _has_errors(diagnostics)
    if json_output:
        payload = {
            "ok": not has_errors,
            "workflow": spec.to_dict() if spec is not None else None,
            "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
        }
        console.out(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if spec is not None and not has_errors:
            console.print(
                f"Validation passed: workflow '{spec.id}' with {len(spec.nodes)} node(s)."
            )
        else:
            console.print("Validation failed.")
        _print_diagnostics(diagnostics)
    if has_errors:
        raise typer.Exit(code=1)


@app.command(name="plan")
def plan_command(
    path: Annotated[Path, typer.Argument(help="Path to a YAML or JSON workflow spec.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic JSON output."),
    ] = False,
) -> None:
    """Create a non-executing run plan for a workflow spec."""
    spec, diagnostics = load_workflow(path)
    if spec is None:
        if json_output:
            payload = {
                "ok": False,
                "plan": None,
                "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
            }
            console.out(json.dumps(payload, indent=2, sort_keys=True))
        else:
            console.print("Planning failed.")
            _print_diagnostics(diagnostics)
        raise typer.Exit(code=1)

    plan = create_run_plan(spec, diagnostics=diagnostics)
    if json_output:
        payload = {
            "ok": not plan.has_errors,
            "plan": plan.to_dict(),
        }
        console.out(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if plan.has_errors:
            console.print("Planning failed.")
            _print_diagnostics(plan.diagnostics)
        else:
            console.print(f"Run plan: workflow '{plan.workflow_id}'")
            for index, node in enumerate(plan.nodes, start=1):
                needs = ", ".join(node.needs) if node.needs else "none"
                console.print(f"{index}. {node.id} ({node.provider}); needs: {needs}")
    if plan.has_errors:
        raise typer.Exit(code=1)


def _has_errors(diagnostics: list[Diagnostic]) -> bool:
    return any(diagnostic.severity is DiagnosticSeverity.ERROR for diagnostic in diagnostics)


def _print_diagnostics(diagnostics: list[Diagnostic] | tuple[Diagnostic, ...]) -> None:
    if not diagnostics:
        return
    console.print("Diagnostics:")
    for diagnostic in diagnostics:
        location = f" [{diagnostic.location}]" if diagnostic.location else ""
        console.print(
            f"- {diagnostic.severity.value}: {diagnostic.code}{location}: {diagnostic.message}"
        )
