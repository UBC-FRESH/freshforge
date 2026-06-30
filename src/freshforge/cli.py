"""Command-line interface for FreshForge."""

from typing import Annotated

import typer
from rich.console import Console

from freshforge import __version__

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
    console.print("Status: Phase 0 package scaffold; workflow DSL not implemented yet.")
