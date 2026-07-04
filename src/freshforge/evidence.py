"""Durable evidence manifest helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from freshforge.matrix import WorkflowMatrixRunResult
from freshforge.records import WorkflowRunResult

WORKFLOW_RUN_EVIDENCE_VERSION = "freshforge.workflow-run-evidence.v1"
MATRIX_RUN_EVIDENCE_VERSION = "freshforge.matrix-run-evidence.v1"


def workflow_run_evidence_manifest(
    *,
    source_path: str | Path,
    workdir: str | Path,
    result: WorkflowRunResult,
    freshforge_version: str,
) -> dict[str, Any]:
    """Return a deterministic evidence manifest for a workflow run."""
    return {
        "manifest_version": WORKFLOW_RUN_EVIDENCE_VERSION,
        "freshforge_version": freshforge_version,
        "source": {
            "type": "workflow",
            "path": _path_text(source_path),
        },
        "workdir": _path_text(workdir),
        "workflow_id": result.workflow_id,
        "run_namespace": result.run_namespace,
        "status": result.status.value,
        "summary": result.summary().to_dict(),
        "run": result.to_dict(),
        "diagnostics": [diagnostic.to_dict() for diagnostic in result.diagnostics],
    }


def matrix_run_evidence_manifest(
    *,
    source_path: str | Path,
    workdir: str | Path,
    result: WorkflowMatrixRunResult,
    freshforge_version: str,
) -> dict[str, Any]:
    """Return a deterministic evidence manifest for a matrix run."""
    return {
        "manifest_version": MATRIX_RUN_EVIDENCE_VERSION,
        "freshforge_version": freshforge_version,
        "source": {
            "type": "matrix",
            "path": _path_text(source_path),
        },
        "workdir": _path_text(workdir),
        "matrix_id": result.matrix_id,
        "status": result.status.value,
        "summary": result.summary().to_dict(),
        "run": result.to_dict(),
        "diagnostics": [diagnostic.to_dict() for diagnostic in result.diagnostics],
    }


def write_evidence_manifest(path: str | Path, manifest: dict[str, Any]) -> Path:
    """Write a deterministic JSON evidence manifest and return the output path."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path


def _path_text(path: str | Path) -> str:
    return Path(path).as_posix()
