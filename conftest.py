"""Pytest configuration file for the MCP Documentation Search Server.

This module contains pytest configuration settings and fixtures used across
all test modules. It defines markers and provides common utilities needed
for testing, such as event loop setup for asynchronous tests.
"""

import pytest
import asyncio


def pytest_configure(config):
    """Configure pytest with custom markers and settings.

    This function is called by pytest during initialization to set up
    custom markers and other configuration options.

    Args:
        config: The pytest configuration object
    """
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as requiring asyncio",
    )


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case.

    This fixture provides a fresh event loop for each test session,
    ensuring that tests don't interfere with each other's event loops.
    It's used by pytest-asyncio when running asynchronous tests.

    Yields:
        An asyncio event loop instance
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
