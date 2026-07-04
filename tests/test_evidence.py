"""Evidence manifest tests."""

from pathlib import Path

from freshforge.evidence import workflow_run_evidence_manifest
from freshforge.records import NodeRunResult, RunStatus, WorkflowRunResult


def test_workflow_evidence_manifest_includes_provider_evidence_mapping() -> None:
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
                evidence={
                    "freshforge.dev/evidence/report": {
                        "label": "report-valid",
                        "role": "summary-report",
                        "status": "passed",
                        "path": "runs/demo/report.json",
                    }
                },
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
    assert node["evidence"]["freshforge.dev/evidence/report"]["label"] == "report-valid"
    summary_node = manifest["summary"]["nodes"][0]
    assert summary_node["evidence_count"] == 1
    assert summary_node["evidence"]["freshforge.dev/evidence/report"]["status"] == "passed"
