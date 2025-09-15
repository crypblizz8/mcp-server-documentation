"""Main entry point for the MCP Documentation Search Server."""

from fastmcp import FastMCP
from utils import validate_library, get_library_url
from services import search_documentation

mcp = FastMCP("docs")


@mcp.tool()
async def get_docs(query: str, library: str) -> str:
    """Search the documentation of a library.
    Supports nillion, nextjs, tailwind, mcp.

    This function performs the following steps:
    1. Normalizes the library name to handle variations
    2. Validates the library is supported
    3. Performs a site-specific search
    4. Fetches and returns the content from search results

    Args:
        query (str): The search query (e.g. "Chroma DB")
        library (str): The library to search docs for (e.g. "langchain")

    Returns:
        str: Combined text content from the search results or error message
    """
    # Validate library and get normalized name
    normalized_library = validate_library(library)
    if not normalized_library:
        from config import DOCS_URLS

        return f"❌ Library not supported: {library}. Available libraries: {', '.join(DOCS_URLS.keys())}"

    # Get documentation URL
    docs_url = get_library_url(normalized_library)
    if not docs_url:
        return f"❌ Documentation URL not found for library: {library}"

    # Search documentation and return results
    return await search_documentation(query, docs_url)


if __name__ == "__main__":
    mcp.run(transport="stdio")
