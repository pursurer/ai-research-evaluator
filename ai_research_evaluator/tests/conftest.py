"""
Pytest configuration and fixtures.
pytest 配置与共享 fixtures
"""

import pytest
from pathlib import Path


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def test_data_dir(project_root: Path) -> Path:
    """Return the test data directory."""
    return project_root / "tests" / "test_data"


@pytest.fixture
def sample_papers_csv(test_data_dir: Path) -> Path:
    """Return path to sample papers CSV for testing."""
    return test_data_dir / "sample_papers.csv"
