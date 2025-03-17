"""Configuration settings for the MCP Documentation Search Server."""

# Documentation URLs for supported libraries
DOCS_URLS = {
    "langchain": "https://js.langchain.com/docs",
    "langgraph": "https://langchain-ai.github.io/langgraphjs",
    "nextjs": "https://nextjs.org/docs",
    "tailwind": "https://tailwindcss.com/docs",
    "mcp": "https://docs.fastmcp.com",
    "framer": "https://motion.dev/docs/",
}

# Library name aliases mapping
LIBRARY_ALIASES = {
    "framermotion": "framer",
    "framer-motion": "framer",
    "motion": "framer",
    "tailwindcss": "tailwind",
    "next.js": "nextjs",
    "next": "nextjs",
    "langchainjs": "langchain",
    "langgraphjs": "langgraph",
}

# HTTP client settings
HTTP_TIMEOUT = 30.0
MAX_SEARCH_RESULTS = 2
