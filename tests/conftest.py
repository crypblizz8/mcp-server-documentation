"""Pytest configuration and fixtures."""

import pytest
from typing import Dict


@pytest.fixture
def mock_docs_urls() -> Dict[str, str]:
    """Fixture providing mock documentation URLs."""
    return {
        "test-lib": "http://test.com/docs",
        "another-lib": "http://another.com/docs",
    }


@pytest.fixture
def mock_library_aliases() -> Dict[str, str]:
    """Fixture providing mock library aliases."""
    return {
        "test": "test-lib",
        "another": "another-lib",
    }
