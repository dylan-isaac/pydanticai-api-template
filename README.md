# PydanticAI API Template

A modern Python project template for building AI-powered APIs with PydanticAI, FastAPI, and Docker.

## Quick Start (Recommended)

1. **Prerequisites**:
   - [VS Code](https://code.visualstudio.com/) or [Cursor](https://cursor.sh/)
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   - [Docker](https://www.docker.com/products/docker-desktop/)
   - A [Nerd Font](https://www.nerdfonts.com/) for optimal terminal experience (optional)

2. **Open in Dev Container**:
   - Clone this repository
   - Open in VS Code/Cursor
   - Click "Reopen in Container" when prompted

3. **Start Development**:
   - Inside the container, run `start` or press `Cmd+Shift+B` (macOS) / `Ctrl+Shift+B` (Windows/Linux)
   - Visit http://localhost:8000/docs for API documentation
   - For the MCP server: `pydanticai-api-template run-mcp` (accessible at http://localhost:3001)

## Documentation Map

This README provides a high-level overview. For detailed information, refer to:

| Documentation | Purpose |
|--------------|---------|
| [Documentation Overview](./docs/OVERVIEW.md) | Comprehensive guide to all documentation |
| [Developer Guide](./docs/DEVELOPER.md) | Setup instructions and development workflows |
| [Architecture](./docs/ARCHITECTURE.md) | System design, patterns, and component relationships |
| [Models](./docs/MODELS.md) | Pydantic models, validation, and PydanticAI integration |
| [API Reference](./docs/API.md) | API endpoints, parameters, and response formats |
| [Testing Guide](./docs/TESTING.md) | Testing strategies and examples |
| [Maintenance](./docs/MAINTENANCE.md) | Configuration management and project maintenance |

## Key Features

- **PydanticAI**: Structured interactions with LLMs using Pydantic models
- **FastAPI**: High-performance API framework with automatic docs
- **MCP Server**: Model Context Protocol server for AI agent access
- **Type Safety**: End-to-end type checking with mypy and Pydantic
- **Docker**: Containerization for consistent development and deployment
- **Modern Tooling**: Ruff, MyPy, UV package manager, and more
- **Prompt Testing**: Automated testing for LLM prompts with CI/CD integration

## Project Structure

```
├── .devcontainer    # Dev container configuration
├── .vscode          # VS Code settings and tasks
├── docs/            # Detailed documentation
├── promptfoo/       # Prompt testing configuration
├── src/             # Source code
│   └── pydanticai_api_template/
│       ├── api/     # FastAPI routes and endpoints
│       ├── agents/  # PydanticAI agent definitions
│       ├── models/  # Pydantic data models
│       ├── mcp/     # MCP server implementation
│       └── cli.py   # Command-line interface
├── tests/           # Test suite
├── pyproject.toml   # Project dependencies and config
└── Makefile         # Common development commands
```

## Basic Usage Examples

### PydanticAI Structured Outputs

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class StoryIdea(BaseModel):
    title: str
    premise: str

story_agent = Agent("openai:gpt-4o", result_type=StoryIdea)
result = await story_agent.run("Give me a sci-fi story idea")
```

### Story API Endpoint

You can generate story ideas using the `/story` endpoint:

```bash
curl -X POST "http://localhost:8000/story" \
  -H "Content-Type: application/json" \
  -d '{"message":"Give me a sci-fi story about time travel"}'
```

Response:
```json
{
  "title": "Echoes of Tomorrow",
  "premise": "A physicist discovers that time isn't linear but layered, with each moment existing simultaneously. When she builds a device to view these layers, she witnesses a future catastrophe and must find a way to reach across time to prevent it."
}
```

### MCP Server Connection

Connect any MCP-compatible client to access tools:

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP

server = MCPServerHTTP(url='http://localhost:3001/sse')
agent = Agent('openai:gpt-4o', mcp_servers=[server])
```

## Environment Setup

Create a `.env` file in the project root with your API keys:

```
OPENAI_API_KEY=your_api_key_here
```

## Status Check

Run `check` to verify your environment configuration.

## Documentation Maintenance Guide

Update documentation when making these changes:

| Change Type | Documentation to Update |
|------------|--------------------------|
| API endpoints | [API.md](./docs/API.md), example in README if major |
| Pydantic models | [MODELS.md](./docs/MODELS.md) |
| Project structure | README.md (project structure section) |
| Architecture | [ARCHITECTURE.md](./docs/ARCHITECTURE.md), README.md if major |
| Dev workflow | [DEVELOPER.md](./docs/DEVELOPER.md) |
| Configuration | [MAINTENANCE.md](./docs/MAINTENANCE.md) |
| CLI commands | [DEVELOPER.md](./docs/DEVELOPER.md), README.md if major |
| Testing approach | [TESTING.md](./docs/TESTING.md) |

For all significant changes:
1. Update relevant documentation files
2. Ensure README links remain accurate
3. If adding new documentation, update the Documentation Map table
4. Keep examples concise but functional

## Alternative Setup Options

See [Developer Guide](./docs/DEVELOPER.md) for non-containerized setup options.
