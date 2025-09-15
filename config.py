"""Configuration settings for the MCP Documentation Search Server."""

# Documentation URLs for supported libraries
DOCS_URLS = {
    "nillion": "https://docs.nillion.com",
    "nextjs": "https://nextjs.org/docs",
    "tailwind": "https://tailwindcss.com/docs",
    "mcp": "https://docs.fastmcp.com",
}

# Library name aliases mapping
LIBRARY_ALIASES = {
    "nillion": "nillion",
    "tailwindcss": "tailwind",
    "tailwind-css": "tailwind",
    "next.js": "nextjs",
    "next": "nextjs",
    "nextjs": "nextjs",
    "fastmcp": "mcp",
}

# HTTP client settings
HTTP_TIMEOUT = 30.0
MAX_SEARCH_RESULTS = 2
