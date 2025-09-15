"""Unit tests for the utility functions in the MCP Documentation Search Server.

This module contains tests for the utility functions that handle library name normalization,
validation, and URL retrieval. These tests ensure that the core functionality of mapping
library names to their documentation URLs works correctly.
"""

import pytest
from utils import normalize_library_name, validate_library, get_library_url
from config import DOCS_URLS, LIBRARY_ALIASES


@pytest.mark.parametrize(
    "input_name,expected",
    [
        ("nillion", "nillion"),  # Test exact match
        ("tailwindcss", "tailwind"),  # Test common alias
        ("TAILWIND-CSS", "tailwind"),  # Test case insensitivity
        ("next.js", "nextjs"),  # Test dot notation
        ("next", "nextjs"),  # Test short name
        ("fastmcp", "mcp"),  # Test mcp alias
        ("unknown-lib", "unknown-lib"),  # Test unknown library
        ("  nillion  ", "nillion"),  # Test whitespace handling
        ("NextJS", "nextjs"),  # Test mixed case
    ],
)
def test_normalize_library_name(input_name: str, expected: str):
    """Test library name normalization with various input formats.

    This test verifies that the normalize_library_name function correctly handles:
    - Common aliases
    - Case insensitivity
    - Whitespace
    - Special characters
    - Unknown libraries

    Args:
        input_name: The library name to normalize
        expected: The expected normalized name
    """
    assert normalize_library_name(input_name) == expected


@pytest.mark.parametrize(
    "input_name,expected",
    [
        ("nillion", True),  # Valid library
        ("nextjs", True),  # Valid library
        ("tailwind", True),  # Valid library
        ("mcp", True),  # Valid library
        ("unknown-lib", False),  # Invalid library
        ("", False),  # Empty string
        (None, False),  # None value
    ],
)
def test_validate_library(input_name: str, expected: bool):
    """Test library validation with various inputs.

    This test ensures that the validate_library function correctly:
    - Accepts valid library names
    - Rejects invalid library names
    - Handles edge cases like empty strings and None values

    Args:
        input_name: The library name to validate
        expected: Whether the library should be considered valid
    """
    result = validate_library(input_name)
    if expected:
        assert result is not None
        assert result in DOCS_URLS
    else:
        assert result is None


@pytest.mark.parametrize(
    "input_name,expected_url",
    [
        ("nillion", "https://docs.nillion.com"),  # Nillion URL
        ("nextjs", "https://nextjs.org/docs"),  # Next.js URL
        ("tailwind", "https://tailwindcss.com/docs"),  # Tailwind URL
        ("mcp", "https://docs.fastmcp.com"),  # MCP URL
        ("unknown-lib", None),  # Invalid library should return None
    ],
)
def test_get_library_url(input_name: str, expected_url: str):
    """Test retrieving documentation URLs for various libraries.

    This test verifies that the get_library_url function:
    - Returns the correct URL for valid libraries
    - Returns None for invalid libraries

    Args:
        input_name: The library name to get the URL for
        expected_url: The expected documentation URL
    """
    assert get_library_url(input_name) == expected_url


def test_all_aliases_are_valid():
    """Test that all defined aliases map to valid libraries.

    This test ensures that every alias defined in the configuration
    maps to a valid library that exists in the DOCS_URLS dictionary.
    This prevents configuration errors where an alias points to a
    non-existent library.
    """
    for alias, library in LIBRARY_ALIASES.items():
        assert (
            library in DOCS_URLS
        ), f"Alias '{alias}' maps to invalid library '{library}'"