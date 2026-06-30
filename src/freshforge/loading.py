"""Workflow loading helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from freshforge.records import Diagnostic, DiagnosticSeverity, WorkflowSpec
from freshforge.validation import validate_workflow_document

_SUPPORTED_SUFFIXES = {".yaml", ".yml", ".json"}


def load_workflow(path: str | Path) -> tuple[WorkflowSpec | None, list[Diagnostic]]:
    """Load and validate a workflow specification from YAML or JSON."""
    source_path = Path(path)
    try:
        document = load_workflow_document(source_path)
    except OSError as exc:
        return None, [
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="source.read_failed",
                message=str(exc),
                location=str(source_path),
            )
        ]
    except (ValueError, yaml.YAMLError) as exc:
        return None, [
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="source.load_failed",
                message=str(exc),
                location=str(source_path),
            )
        ]
    return validate_workflow_document(document, source_path=str(source_path))


def load_workflow_document(path: str | Path) -> Any:
    """Load a raw YAML or JSON workflow document."""
    source_path = Path(path)
    suffix = source_path.suffix.lower()
    if suffix not in _SUPPORTED_SUFFIXES:
        supported = ", ".join(sorted(_SUPPORTED_SUFFIXES))
        raise ValueError(
            f"Unsupported workflow file suffix '{suffix}'. Expected one of: {supported}."
        )

    text = source_path.read_text(encoding="utf-8")
    if suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text)
