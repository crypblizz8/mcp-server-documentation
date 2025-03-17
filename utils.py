"""Utility functions for the MCP Documentation Search Server."""

from typing import Optional
from config import DOCS_URLS, LIBRARY_ALIASES


def normalize_library_name(library: Optional[str]) -> Optional[str]:
    """Normalizes library names by handling common variations.

    This function processes library names to match their standard form by:
    1. Converting to lowercase and removing whitespace
    2. Checking against known aliases
    3. Validating against supported libraries
    4. Attempting partial matching as fallback

    Args:
        library (Optional[str]): The library name to normalize

    Returns:
        Optional[str]: The normalized library name, or None if input is invalid
    """
    if not library:  # Handle None or empty string
        return None

    # Convert to lowercase and remove whitespace
    normalized = library.lower().strip()
    if not normalized:  # Handle strings that are only whitespace
        return None

    # Check if it's a known variation
    if normalized in LIBRARY_ALIASES:
        return LIBRARY_ALIASES[normalized]

    # If already a valid name, return as is
    if normalized in DOCS_URLS:
        return normalized

    # Try partial matching
    for valid_name in DOCS_URLS.keys():
        if valid_name in normalized or normalized in valid_name:
            return valid_name

    return normalized


def validate_library(library: Optional[str]) -> Optional[str]:
    """Validates if a library is supported and returns its normalized name.

    Args:
        library (Optional[str]): The library name to validate

    Returns:
        Optional[str]: The normalized library name if supported, None otherwise
    """
    if not library:  # Handle None or empty string
        return None

    normalized = normalize_library_name(library)
    return normalized if normalized and normalized in DOCS_URLS else None


def get_library_url(library: str) -> Optional[str]:
    """Gets the documentation URL for a library.

    Args:
        library (str): The library name

    Returns:
        Optional[str]: The documentation URL if library is supported, None otherwise
    """
    normalized = normalize_library_name(library)
    return DOCS_URLS.get(normalized) if normalized else None
