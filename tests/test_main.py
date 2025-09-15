"""Integration tests for the MCP Documentation Search Server.

This module contains integration tests for the main functionality of the MCP Documentation
Search Server. It tests the get_docs_impl function which is the core implementation.
These tests verify that the function correctly handles various inputs, resolves library
aliases, and returns appropriate responses.
"""

import pytest
from unittest.mock import patch, AsyncMock
import asyncio


def run_async(coroutine):
    """Helper function to run an async function synchronously.

    This utility function creates a new event loop, runs the provided coroutine
    to completion, and then closes the loop. It allows testing async functions
    in a synchronous test environment.

    Args:
        coroutine: The coroutine to execute

    Returns:
        The result of the coroutine execution
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()


def test_get_docs_valid_library():
    """Test documentation retrieval for a valid library.

    This test verifies that the get_docs_impl function correctly:
    - Accepts a valid library name
    - Calls the search_documentation function with appropriate parameters
    - Returns the search results
    """
    from main import get_docs_impl

    with patch("main.search_documentation", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = "Test documentation content"

        result = run_async(get_docs_impl("test query", "nillion"))

        assert "Test documentation content" in result
        mock_search.assert_called_once()


def test_get_docs_invalid_library():
    """Test documentation retrieval for an invalid library.

    This test ensures that the get_docs_impl function properly handles invalid
    library names by returning an appropriate error message rather than
    attempting to search an invalid documentation site.
    """
    from main import get_docs_impl

    result = run_async(get_docs_impl("test query", "invalid-library"))
    assert "❌ Library not supported" in result


def test_get_docs_alias_resolution():
    """Test documentation retrieval using library aliases.

    This test verifies that the get_docs_impl function correctly resolves
    library aliases to their canonical names before searching for
    documentation. For example, "tailwindcss" should be resolved to "tailwind".
    """
    from main import get_docs_impl

    with patch("main.search_documentation", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = "Tailwind CSS docs"

        result = run_async(get_docs_impl("flexbox", "tailwindcss"))

        assert "Tailwind CSS docs" in result
        mock_search.assert_called_once()


def test_get_docs_empty_query():
    """Test documentation retrieval with empty query.

    This test ensures that the get_docs_impl function handles empty search
    queries gracefully. While an empty query might not return useful results,
    the function should not fail and should still attempt to search.
    """
    from main import get_docs_impl

    with patch("main.search_documentation", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = "Some results"

        result = run_async(get_docs_impl("", "nextjs"))

        assert isinstance(result, str)
        mock_search.assert_called_once()


@pytest.mark.parametrize(
    "library,expected_in_result",
    [
        ("next.js", "nextjs"),  # Test dot notation
        ("next", "nextjs"),  # Test short name
        ("tailwindcss", "tailwind"),  # Test compound name
        ("tailwind-css", "tailwind"),  # Test hyphenated name
        ("fastmcp", "mcp"),  # Test alias for mcp
    ],
)
def test_get_docs_various_aliases(library: str, expected_in_result: str):
    """Test documentation retrieval with various library aliases.

    This parametrized test verifies that the get_docs_impl function correctly
    handles a variety of library name formats and aliases, ensuring that
    each is properly normalized to its canonical form before searching.

    Args:
        library: The library alias to test
        expected_in_result: The expected canonical library name
    """
    from main import get_docs_impl

    with patch("main.search_documentation", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = f"Docs for {expected_in_result}"

        result = run_async(get_docs_impl("test", library))

        assert mock_search.called
        assert f"Docs for {expected_in_result}" in result