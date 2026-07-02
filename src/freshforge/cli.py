"""Command-line interface for FreshForge."""

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from freshforge import __version__
from freshforge.execution import run_workflow
from freshforge.loading import load_workflow
from freshforge.matrix import (
    expand_workflow_matrix,
    load_workflow_matrix,
    plan_workflow_matrix,
    run_workflow_matrix,
)
from freshforge.planning import create_run_plan
from freshforge.providers import ProviderRegistry, default_provider_registry
from freshforge.records import Diagnostic, DiagnosticSeverity
from freshforge.validation import validate_workflow_with_providers

app = typer.Typer(
    add_completion=False,
    help="Workflow-as-code for open forest resources and ecosystem services modelling.",
)
matrix_app = typer.Typer(help="Expand, plan, and run workflow matrices.")
app.add_typer(matrix_app, name="matrix")
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
        "Status: 0.1.0a4 public alpha; "
        "serial local workflow execution with run namespaces, summaries, and matrices."
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


@app.command(name="run")
def run_command(
    path: Annotated[Path, typer.Argument(help="Path to a YAML or JSON workflow spec.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic JSON output."),
    ] = False,
    workdir: Annotated[
        Path,
        typer.Option(
            "--workdir",
            help="Directory used to resolve relative workflow artifact paths.",
        ),
    ] = Path("."),
    namespace: Annotated[
        str | None,
        typer.Option(
            "--namespace",
            help="Relative run namespace used to isolate run artifacts.",
        ),
    ] = None,
) -> None:
    """Execute a workflow with provider-owned node implementations."""
    spec, diagnostics = load_workflow(path)
    if spec is None:
        if json_output:
            payload = {
                "ok": False,
                "run": None,
                "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
            }
            console.out(json.dumps(payload, indent=2, sort_keys=True))
        else:
            console.print("Run failed.")
            _print_diagnostics(diagnostics)
        raise typer.Exit(code=1)

    result = run_workflow(
        spec,
        diagnostics=diagnostics,
        workdir=workdir,
        run_namespace=namespace,
    )
    summary = result.summary()
    if json_output:
        payload = {
            "ok": result.ok,
            "run": result.to_dict(),
            "summary": summary.to_dict(),
        }
        console.out(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if result.ok:
            console.print(f"Run passed: workflow '{result.workflow_id}'")
        else:
            console.print("Run failed.")
        if result.run_namespace is not None:
            console.print(f"Namespace: {result.run_namespace}")
        console.print(
            "Summary: "
            f"{summary.succeeded_count} succeeded, "
            f"{summary.failed_count} failed, "
            f"{summary.skipped_count} skipped; "
            f"{summary.error_count} error(s), "
            f"{summary.warning_count} warning(s); "
            f"{summary.artifact_count} artifact(s)."
        )
        for index, node in enumerate(result.nodes, start=1):
            provider = node.provider_id or "unresolved"
            node_type = node.node_type or "unresolved"
            console.print(f"{index}. {node.id} ({provider}.{node_type}): {node.status.value}")
        _print_diagnostics(result.diagnostics)
    if not result.ok:
        raise typer.Exit(code=1)


@matrix_app.command(name="expand")
def matrix_expand_command(
    path: Annotated[Path, typer.Argument(help="Path to a YAML or JSON matrix spec.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic JSON output."),
    ] = False,
) -> None:
    """Expand a workflow matrix into ordinary workflow specs."""
    matrix, diagnostics = load_workflow_matrix(path)
    if matrix is None:
        _print_matrix_load_failure("Matrix expansion failed.", diagnostics, json_output)
        raise typer.Exit(code=1)

    expanded = expand_workflow_matrix(matrix, diagnostics=diagnostics)
    has_errors = _has_errors(diagnostics) or any(_has_errors(case.diagnostics) for case in expanded)
    if json_output:
        payload = {
            "ok": not has_errors,
            "matrix": matrix.to_dict(),
            "cases": [case.to_dict() for case in expanded],
            "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
        }
        console.out(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if has_errors:
            console.print("Matrix expansion failed.")
        else:
            console.print(f"Matrix expansion: '{matrix.id}' with {len(expanded)} case(s).")
        for case in expanded:
            status = "ok" if case.ok else "failed"
            console.print(f"- {case.case.id}: {status}; namespace: {case.namespace}")
        _print_diagnostics(diagnostics)
        for case in expanded:
            _print_diagnostics(case.diagnostics)
    if has_errors:
        raise typer.Exit(code=1)


@matrix_app.command(name="plan")
def matrix_plan_command(
    path: Annotated[Path, typer.Argument(help="Path to a YAML or JSON matrix spec.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic JSON output."),
    ] = False,
) -> None:
    """Create non-executing plans for every matrix case."""
    matrix, diagnostics = load_workflow_matrix(path)
    if matrix is None:
        _print_matrix_load_failure("Matrix planning failed.", diagnostics, json_output)
        raise typer.Exit(code=1)

    plan = plan_workflow_matrix(matrix, diagnostics=diagnostics)
    if json_output:
        payload = {
            "ok": plan.ok,
            "plan": plan.to_dict(),
        }
        console.out(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if plan.ok:
            console.print(f"Matrix plan: '{plan.matrix_id}' with {len(plan.cases)} case(s).")
        else:
            console.print("Matrix planning failed.")
        for case in plan.cases:
            status = "ok" if case.ok else "failed"
            console.print(f"- {case.case_id}: {status}; namespace: {case.namespace}")
        _print_diagnostics(plan.diagnostics)
        for case in plan.cases:
            _print_diagnostics(case.diagnostics)
            if case.plan is not None:
                _print_diagnostics(case.plan.diagnostics)
    if not plan.ok:
        raise typer.Exit(code=1)


@matrix_app.command(name="run")
def matrix_run_command(
    path: Annotated[Path, typer.Argument(help="Path to a YAML or JSON matrix spec.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic JSON output."),
    ] = False,
    workdir: Annotated[
        Path,
        typer.Option(
            "--workdir",
            help="Directory used to resolve relative workflow artifact paths.",
        ),
    ] = Path("."),
    fail_fast: Annotated[
        bool,
        typer.Option("--fail-fast", help="Stop after the first failed matrix case."),
    ] = False,
) -> None:
    """Execute every workflow case in a matrix serially."""
    matrix, diagnostics = load_workflow_matrix(path)
    if matrix is None:
        _print_matrix_load_failure("Matrix run failed.", diagnostics, json_output)
        raise typer.Exit(code=1)

    result = run_workflow_matrix(
        matrix,
        diagnostics=diagnostics,
        workdir=workdir,
        fail_fast=fail_fast,
    )
    summary = result.summary()
    if json_output:
        payload = {
            "ok": result.ok,
            "run": result.to_dict(),
            "summary": summary.to_dict(),
        }
        console.out(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if result.ok:
            console.print(f"Matrix run passed: '{result.matrix_id}'")
        else:
            console.print("Matrix run failed.")
        console.print(
            "Summary: "
            f"{summary.succeeded_count} succeeded, "
            f"{summary.failed_count} failed, "
            f"{summary.skipped_count} skipped; "
            f"{summary.error_count} error(s), "
            f"{summary.warning_count} warning(s)."
        )
        for case in result.cases:
            status = case.run.status.value if case.run is not None else "failed"
            console.print(f"- {case.case_id}: {status}; namespace: {case.namespace}")
        _print_diagnostics(result.diagnostics)
        for case in result.cases:
            _print_diagnostics(case.diagnostics)
            if case.run is not None:
                _print_diagnostics(case.run.diagnostics)
    if not result.ok:
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


def _print_matrix_load_failure(
    message: str,
    diagnostics: list[Diagnostic],
    json_output: bool,
) -> None:
    if json_output:
        payload = {
            "ok": False,
            "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
        }
        console.out(json.dumps(payload, indent=2, sort_keys=True))
    else:
        console.print(message)
        _print_diagnostics(diagnostics)


def _provider_resolutions(spec, registry: ProviderRegistry) -> list[dict[str, object]]:
    return [
        {
            "node_id": node.id,
            **registry.resolve(node.provider).to_dict(),
        }
        for node in spec.nodes
    ]
