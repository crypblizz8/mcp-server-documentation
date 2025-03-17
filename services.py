"""Services for web search and content fetching."""

from typing import List
import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from config import HTTP_TIMEOUT, MAX_SEARCH_RESULTS


async def search_web(query: str) -> List[str]:
    """Performs a web search using DuckDuckGo and returns result URLs.

    Args:
        query (str): The search query to execute

    Returns:
        List[str]: A list of URLs from the search results
    """
    result = DDGS().text(query, max_results=MAX_SEARCH_RESULTS)
    return [item["href"] for item in result]


async def fetch_url(url: str) -> str:
    """Asynchronously fetches and extracts text content from a URL.

    Args:
        url (str): The URL to fetch content from

    Returns:
        str: The extracted text content or error message if fetch fails
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, timeout=HTTP_TIMEOUT)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text()
        except httpx.TimeoutException as e:
            return f"❌ Timeout error: {e}"
        except httpx.HTTPStatusError as e:
            return f"❌ HTTP error: {e}"
        except httpx.RequestError as e:
            return f"❌ Request error: {e}"


async def search_documentation(query: str, site_url: str) -> str:
    """Searches documentation on a specific site and returns combined results.

    Args:
        query (str): The search query
        site_url (str): The documentation site URL

    Returns:
        str: Combined text content from search results
    """
    site_query = f"site:{site_url} {query}"
    results = await search_web(site_query)

    if not results:
        return f"❌ No results found for {query}"

    combined_text = ""
    for result in results:
        content = await fetch_url(result)
        combined_text += content

    return combined_text
