"""Unit tests for web services in the MCP Documentation Search Server.

This module contains tests for the web service functions that handle searching
documentation sites, fetching content from URLs, and processing the results.
These tests verify that the server correctly interacts with external services
and handles various response scenarios.
"""

import pytest
from unittest.mock import AsyncMock, patch
import asyncio
from services import search_web, fetch_url, search_documentation
import httpx


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


def test_search_web():
    """Test web search functionality using DuckDuckGo.

    This test verifies that the search_web function correctly:
    - Calls the DuckDuckGo search API with the provided query
    - Extracts URLs from the search results
    - Returns a list of result URLs
    """
    mock_results = [{"href": "http://test1.com"}, {"href": "http://test2.com"}]

    with patch("services.DDGS") as mock_ddgs:
        mock_ddgs.return_value.text.return_value = mock_results
        results = run_async(search_web("test query"))

        assert results == ["http://test1.com", "http://test2.com"]
        mock_ddgs.return_value.text.assert_called_once_with("test query", max_results=2)


def test_fetch_url_success():
    """Test successful URL content fetching.

    This test ensures that the fetch_url function correctly:
    - Makes an HTTP request to the specified URL
    - Processes the HTML response
    - Extracts and returns the text content
    """
    mock_response = AsyncMock()
    mock_response.text = "<html><body>Test content</body></html>"

    with patch("services.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get.return_value = (
            mock_response
        )
        content = run_async(fetch_url("http://test.com"))

        assert "Test content" in content
        mock_client.return_value.__aenter__.return_value.get.assert_called_once()


def test_fetch_url_timeout():
    """Test URL fetching with timeout error.

    This test verifies that the fetch_url function properly handles
    timeout errors by returning an appropriate error message rather
    than failing with an exception.
    """
    with patch("services.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get.side_effect = (
            httpx.TimeoutException("Connection timed out")
        )

        content = run_async(fetch_url("http://test.com"))
        assert "❌ Timeout error" in content


def test_search_documentation():
    """Test documentation search integration.

    This test verifies that the search_documentation function correctly:
    - Constructs a site-specific search query
    - Calls the search_web function to get result URLs
    - Fetches content from each result URL
    - Combines and returns the content
    """
    mock_results = ["http://test.com/docs"]
    mock_content = "Documentation content"

    with (
        patch("services.search_web", new_callable=AsyncMock) as mock_search,
        patch("services.fetch_url", new_callable=AsyncMock) as mock_fetch,
    ):

        mock_search.return_value = mock_results
        mock_fetch.return_value = mock_content

        result = run_async(search_documentation("test query", "http://test.com"))

        assert mock_content in result
        mock_search.assert_called_once_with("site:http://test.com test query")
        mock_fetch.assert_called_once_with("http://test.com/docs")


def test_search_documentation_no_results():
    """Test documentation search with no results.

    This test ensures that the search_documentation function properly
    handles the case where no search results are found, returning an
    appropriate error message rather than failing.
    """
    with patch("services.search_web", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = []

        result = run_async(search_documentation("test query", "http://test.com"))
        assert "❌ No results found" in result
