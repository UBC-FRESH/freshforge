"""Evidence manifest tests."""

from pathlib import Path

from freshforge.evidence import workflow_run_evidence_manifest
from freshforge.records import (
    NodeRunResult,
    ProviderEvidence,
    RunStatus,
    WorkflowRunResult,
)


def test_workflow_evidence_manifest_includes_provider_evidence() -> None:
    result = WorkflowRunResult(
        workflow_id="demo",
        status=RunStatus.SUCCESS,
        nodes=(
            NodeRunResult(
                id="report",
                provider="example.report",
                provider_id="example",
                node_type="report",
                status=RunStatus.SUCCESS,
                artifacts={"report": "runs/demo/report.json"},
                evidence=(
                    ProviderEvidence(
                        label="report-valid",
                        status="passed",
                        artifact_role="summary-report",
                        path="runs/demo/report.json",
                    ),
                ),
            ),
        ),
    )

    manifest = workflow_run_evidence_manifest(
        source_path=Path("workflow.yaml"),
        workdir=Path("runs"),
        result=result,
        freshforge_version="0.0.test",
    )

    node = manifest["run"]["nodes"][0]
    assert node["evidence"] == [
        {
            "label": "report-valid",
            "status": "passed",
            "artifact_role": "summary-report",
            "path": "runs/demo/report.json",
        }
    ]
    summary_node = manifest["summary"]["nodes"][0]
    assert summary_node["evidence_count"] == 1
    assert summary_node["evidence"][0]["label"] == "report-valid"
