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
   - Visit <http://localhost:8000/docs> for API documentation
   - For the MCP server: `pat run-mcp` (accessible at <http://localhost:3001>)

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
| [Observability](./docs/OBSERVABILITY.md) | Logging, tracing, and monitoring with Logfire |
| [Cursor Rules](./docs/CURSOR_RULES.md) | AI-assisted development with Cursor |
| [Wishlist](./wishlist/) | Future improvements and feature ideas |

## Key Features

- **PydanticAI**: Structured interactions with LLMs using Pydantic models
- **FastAPI**: High-performance API framework with automatic docs
- **MCP Server**: Model Context Protocol server for AI agent access
- **Type Safety**: End-to-end type checking with mypy and Pydantic
- **Docker**: Containerization for consistent development and deployment
- **Modern Tooling**: Ruff, MyPy, UV package manager, and more
- **Prompt Testing**: Automated testing for LLM prompts with CI/CD integration
- **Observability**: Complete visibility with Logfire integration
- **Cursor Rules**: Smart AI-assisted development with contextual reminders
- **Repomix Runner**: Easily bundle project files for providing context to AI assistants ([VS Code Extension](https://marketplace.cursorapi.com/items?itemName=DorianMassoulier.repomix-runner))

## AI-Assisted Development with Cursor

This project includes custom [Cursor Rules](./docs/CURSOR_RULES.md) to enhance your
development experience when using [Cursor](https://cursor.sh/), an AI-powered code
editor:

- **Documentation Reminders**: Get contextual reminders to update documentation when
  changing code
- **Type Safety Enforcement**: Maintain type safety throughout the codebase
- **Director Pattern Detection**: Identify opportunities for implementing autonomous AI
  workflows
- **Repomix Integration**: Use the [Repomix Runner extension](https://marketplace.cursorapi.com/items?itemName=DorianMassoulier.repomix-runner)
  (automatically installed in the dev container) to easily bundle files or directories
  and copy them to the clipboard for pasting into AI chat prompts.

To get started with the Cursor Rules:

1. Open the project in Cursor
2. The rules will be automatically loaded from `.cursor/rules.yml`
3. Start coding and benefit from smart, contextual assistance
4. Use `@` symbol references (e.g., `@docs/MODELS.md`) to bring relevant context into chats

For detailed information, see the [Cursor Rules Guide](./docs/CURSOR_RULES.md).

## Project Structure

```text
├── .cursor          # Cursor AI rules and configuration
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
├── wishlist/        # Future improvements and feature ideas
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
cURL -X POST "http://localhost:8000/story" \\
  -H "Content-Type: application/json" \\
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

## Wishlist

The project includes a `wishlist/` directory for capturing future improvements and feature ideas. This serves as:

1. **Feature Backlog**: A place to document desired enhancements while focusing on current priorities
2. **AI-Driven Implementation**: Actionable items for AI to implement during coding sessions
3. **Collaborative Planning**: A way to track ideas from the entire team for future sprints

Current wishlist items:

- Templateizing and CookieCutter integration for project scaffolding

To contribute to the wishlist, add markdown files to the `wishlist/` directory with detailed descriptions of proposed features or improvements.

## Observability with Logfire

This template comes with built-in observability powered by Logfire. Key features include:

1. **Automatic Instrumentation** for FastAPI, PydanticAI, and HTTP requests
2. **Live Debugging** with real-time trace visualization
3. **LLM Call Monitoring** including prompts, tokens, and costs
4. **Performance Metrics** to identify bottlenecks

### Local Setup

```bash
# From inside the dev container
auth-logfire     # Authenticate with Logfire
use-logfire      # Set the current project
```

### Production Setup

Set these environment variables:

```dotenv
LOGFIRE_TOKEN="your-write-token"
LOGFIRE_ENABLED="true"
```

For detailed instructions, see [Observability](./docs/OBSERVABILITY.md).

## Environment Setup

Create a `.env` file in the project root with your API keys:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_claude_api_key_here
```
