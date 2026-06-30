"""Basic package import and metadata tests."""

from importlib import metadata

import freshforge


def test_version_is_exposed() -> None:
    assert freshforge.__version__ == "0.1.0a1"


def test_package_metadata_matches_version() -> None:
    assert metadata.version("freshforge") == freshforge.__version__
