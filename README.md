# MCP Documentation Search Server

A powerful documentation search server built with FastMCP that enables intelligent searching across multiple popular framework and library documentations. This tool helps developers quickly find relevant information from various documentation sources using a unified interface.

## 🌟 Features

- **📚 Multi-Library Support**: Search documentation across multiple libraries:

  - [LangChain](https://js.langchain.com/docs) - JavaScript/TypeScript LangChain documentation
  - [LangGraph](https://langchain-ai.github.io/langgraphjs) - LangGraph.js documentation
  - [Next.js](https://nextjs.org/docs) - Next.js framework documentation
  - [Tailwind CSS](https://tailwindcss.com/docs) - Utility-first CSS framework
  - [FastMCP](https://docs.fastmcp.com) - FastMCP documentation
  - [Framer Motion](https://motion.dev/docs/) - Animation library for React

- **🔍 Intelligent Search**

  - Smart name resolution for library variations
  - DuckDuckGo-powered search for accurate results
  - Site-specific search targeting

- **⚡ Performance Features**

  - Asynchronous processing
  - Efficient web request handling
  - Parallel content fetching

- **🛡️ Robust Error Handling**
  - Network timeout management
  - Invalid input validation
  - HTTP error handling
  - Request failure recovery

## 📋 Requirements

- Python 3.8+
- pip or uv package manager
- Virtual environment (recommended)

## 🚀 Quick Start

1. **Clone the Repository**

```bash
git clone <repository-url>
cd mcp-server
```

2. **Set Up Virtual Environment**

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the Server**

```bash
python main.py
```

## 💻 Usage

### Basic Usage

```python
from main import get_docs

# Search Framer Motion documentation
result = await get_docs(
    query="how to animate on scroll",
    library="framer-motion"
)

# Search Next.js documentation
result = await get_docs(
    query="how to use app router",
    library="next"
)
```

### Library Name Variations

The system intelligently handles various library name formats:

```python
# All these calls will work the same way
await get_docs(query="animations", library="framer")
await get_docs(query="animations", library="framermotion")
await get_docs(query="animations", library="framer-motion")
await get_docs(query="animations", library="motion")
```

## 🧪 Testing

The project includes a comprehensive test suite to ensure reliability and correctness. Tests are organized into three main categories:

### Test Structure

- **Unit Tests**: Test individual components in isolation

  - `test_utils.py`: Tests for library name normalization and URL retrieval
  - `test_services.py`: Tests for web search and content fetching services

- **Integration Tests**: Test how components work together
  - `test_main.py`: Tests for the main API function `get_docs`

### Running Tests

To run all tests:

```bash
python -m pytest
```

To run specific test modules:

```bash
python -m pytest tests/test_utils.py
python -m pytest tests/test_services.py
python -m pytest tests/test_main.py
```

To run tests with verbose output:

```bash
python -m pytest -v
```

### Test Coverage

The tests cover:

- ✅ Library name normalization and validation
- ✅ URL retrieval for different libraries
- ✅ Web search functionality
- ✅ Content fetching and error handling
- ✅ Documentation search integration
- ✅ API input validation and error handling
- ✅ Alias resolution for different library name formats

### Asynchronous Testing

The project uses a custom `run_async` helper function to test asynchronous code in a synchronous test environment. This approach allows for testing async functions without requiring complex test setup.

## 🏗️ Project Structure

```
mcp-server/
├── main.py          # Entry point and FastMCP tool definition
├── config.py        # Configuration settings and constants
├── services.py      # Web search and content fetching services
├── utils.py         # Utility functions for library name handling
├── tests/           # Test suite
│   ├── test_utils.py    # Tests for utility functions
│   ├── test_services.py # Tests for web services
│   ├── test_main.py     # Tests for main API
│   └── conftest.py      # Pytest configuration
├── requirements.txt # Project dependencies
└── README.md        # Documentation
```

## 🔧 Configuration

### Supported Libraries

To add a new library:

1. Add the documentation URL in `config.py`:

```python
DOCS_URLS = {
    "new-library": "https://docs.new-library.com",
    # ... existing entries
}
```

2. Add common aliases:

```python
LIBRARY_ALIASES = {
    "new-lib": "new-library",
    # ... existing entries
}
```

### HTTP Settings

Modify in `config.py`:

```python
HTTP_TIMEOUT = 30.0        # Timeout in seconds
MAX_SEARCH_RESULTS = 2     # Number of search results to fetch
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Adding New Libraries

1. Update `DOCS_URLS` in `config.py`
2. Add relevant aliases in `LIBRARY_ALIASES`
3. Test the integration
4. Update documentation
5. Submit a pull request

## 🐛 Troubleshooting

Common issues and solutions:

- **TimeoutError**: Increase `HTTP_TIMEOUT` in `config.py`
- **No Results**: Try different search terms or verify the library name
- **HTTP Errors**: Check your internet connection and the documentation URL

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [FastMCP](https://fastmcp.com) for the core functionality
- [DuckDuckGo](https://duckduckgo.com) for search capabilities
- [pytest](https://docs.pytest.org/) for testing framework
- All supported documentation providers
