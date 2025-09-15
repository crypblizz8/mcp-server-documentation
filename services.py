"""Services for web search and content fetching."""

from typing import List
import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from config import HTTP_TIMEOUT, MAX_SEARCH_RESULTS
import asyncio


async def search_web(query: str) -> List[str]:
    """Performs a web search using DuckDuckGo and returns result URLs.

    Args:
        query (str): The search query to execute

    Returns:
        List[str]: A list of URLs from the search results
    """
    try:
        # Run the synchronous DDGS in a thread pool
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None, 
            lambda: list(DDGS().text(query, max_results=MAX_SEARCH_RESULTS))
        )
        
        urls = []
        for item in results:
            if isinstance(item, dict) and "href" in item:
                urls.append(item["href"])
        
        print(f"DEBUG: Search query: {query}")
        print(f"DEBUG: Found {len(urls)} URLs: {urls}")
        return urls
    except Exception as e:
        print(f"DEBUG: Search error: {e}")
        return []


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
    # Try multiple search strategies
    strategies = [
        f"site:{site_url} {query}",  # Site-specific search
        f"{query} site:{site_url.replace('https://', '').replace('http://', '')}",  # Without protocol
        f"{query} {site_url}",  # Direct URL mention
    ]
    
    results = []
    for strategy in strategies:
        print(f"DEBUG: Trying search strategy: {strategy}")
        search_results = await search_web(strategy)
        if search_results:
            results = search_results
            break
    
    # If no results with site-specific search, try a general search and filter
    if not results:
        print(f"DEBUG: Site-specific search failed, trying general search")
        general_results = await search_web(f"{query} documentation")
        # Filter for URLs that might be from the target site
        site_domain = site_url.replace('https://', '').replace('http://', '').split('/')[0]
        results = [url for url in general_results if site_domain in url]
    
    if not results:
        return f"❌ No results found for {query}"

    combined_text = ""
    for result in results:
        content = await fetch_url(result)
        if not content.startswith("❌"):
            combined_text += content + "\n\n"

    if not combined_text:
        return f"❌ Could not fetch content from search results"
    
    return combined_text
