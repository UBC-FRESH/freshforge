"""Command-line interface for FreshForge."""

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from freshforge import __version__
from freshforge.loading import load_workflow
from freshforge.planning import create_run_plan
from freshforge.providers import ProviderRegistry, default_provider_registry
from freshforge.records import Diagnostic, DiagnosticSeverity
from freshforge.validation import validate_workflow_with_providers

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
    console.print(
        "Status: Phase 4 entry-point provider discovery and adapter prototype."
    )


@app.command(name="providers")
def providers_command(
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic JSON output."),
    ] = False,
) -> None:
    """List registered providers and node types."""
    registry, diagnostics = default_provider_registry()
    provider_metadata = registry.list()
    if json_output:
        payload = {
            "ok": not _has_errors(diagnostics),
            "providers": [metadata.to_dict() for metadata in provider_metadata],
            "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
        }
        console.out(json.dumps(payload, indent=2, sort_keys=True))
    else:
        console.print("Registered providers:")
        for metadata in provider_metadata:
            console.print(f"- {metadata.id} {metadata.version}")
            for node_type in metadata.node_types:
                console.print(f"  - {node_type.id}")
        _print_diagnostics(diagnostics)

    if _has_errors(diagnostics):
        raise typer.Exit(code=1)


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
    if spec is not None:
        diagnostics = validate_workflow_with_providers(
            spec,
            structural_diagnostics=diagnostics,
        )
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
                provider = node.provider_id or "unresolved"
                node_type = node.node_type or "unresolved"
                console.print(
                    f"{index}. {node.id} ({provider}.{node_type}); needs: {needs}"
                )
    if plan.has_errors:
        raise typer.Exit(code=1)


@app.command(name="inspect")
def inspect_command(
    path: Annotated[Path, typer.Argument(help="Path to a YAML or JSON workflow spec.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic JSON output."),
    ] = False,
) -> None:
    """Inspect a workflow spec and provider references without planning or executing."""
    spec, diagnostics = load_workflow(path)
    registry, discovery_diagnostics = default_provider_registry()
    diagnostics.extend(discovery_diagnostics)
    if spec is not None:
        diagnostics = validate_workflow_with_providers(
            spec,
            registry=registry,
            structural_diagnostics=diagnostics,
        )
    has_errors = _has_errors(diagnostics)

    if json_output:
        payload = {
            "ok": not has_errors,
            "workflow": spec.to_dict() if spec is not None else None,
            "providers": _provider_resolutions(spec, registry) if spec is not None else [],
            "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
        }
        console.out(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if spec is None:
            console.print("Inspection failed.")
        else:
            console.print(f"Workflow: {spec.id}")
            console.print(f"Nodes: {len(spec.nodes)}")
            for node in spec.nodes:
                resolution = registry.resolve(node.provider)
                provider_id = resolution.provider_id or "unresolved"
                node_type = resolution.node_type or "unresolved"
                status = "available" if resolution.node_type_available else "unavailable"
                console.print(f"- {node.id}: {provider_id}.{node_type} ({status})")
        _print_diagnostics(diagnostics)
    if has_errors:
        raise typer.Exit(code=1)


def _has_errors(diagnostics: list[Diagnostic] | tuple[Diagnostic, ...]) -> bool:
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


def _provider_resolutions(spec, registry: ProviderRegistry) -> list[dict[str, object]]:
    return [
        {
            "node_id": node.id,
            **registry.resolve(node.provider).to_dict(),
        }
        for node in spec.nodes
    ]
