"""Release artifact contract tests."""

from __future__ import annotations

import tomllib
from pathlib import Path

import freshforge

ROOT = Path(__file__).resolve().parents[1]


def test_release_version_contract_is_0_1_0a2() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["version"] == "0.1.0a2"
    assert freshforge.__version__ == "0.1.0a2"


def test_release_manifest_includes_tracked_examples() -> None:
    manifest = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")

    assert "recursive-include examples *.yaml" in manifest
    assert (ROOT / "examples" / "stand_treatment_workflow.yaml").is_file()
    assert (ROOT / "examples" / "ecosystem_adapter_workflow.yaml").is_file()


def test_release_metadata_declares_fixture_provider_entry_point() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    entry_points = pyproject["project"]["entry-points"]["freshforge.providers"]

    assert entry_points["fixture"] == "freshforge.providers:fixture_provider_factory"


def test_release_notes_document_alpha_boundaries() -> None:
    release_notes = (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")

    assert "0.1.0a2" in release_notes
    assert "not published to PyPI" in release_notes
    assert "serial local runner" in release_notes
