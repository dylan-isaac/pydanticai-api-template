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
   - Inside the container, run `start` or press `Cmd+Shift+B` (macOS) / `Ctrl+Shift+B` (Windows/Linux) to start the server
   - Visit http://localhost:8000/docs to see API documentation
   - For the MCP server, run `pydanticai-api-template run-mcp` and connect to http://localhost:3001

## Project Documentation

- [Developer Guide](./docs/DEVELOPER.md) - Detailed setup and workflows
- [Architecture](./docs/ARCHITECTURE.md) - System design and patterns
- [Maintenance](./MAINTENANCE.md) - Configuration management
- [API Reference](./docs/API.md) - API endpoint documentation

## Features

- **PydanticAI**: Structured interactions with LLMs using Pydantic models
- **FastAPI**: High-performance API framework with automatic docs
- **MCP Server**: Model Context Protocol server for AI agent access
- **UV**: Fast dependency management and virtual environments
- **Docker**: Containerization for consistent deployment
- **Dev Containers**: VS Code / Cursor integration for zero-configuration setup
- **Modern Tooling**: Ruff, MyPy, Typer CLI, and more

## MCP Server

This project includes an MCP (Model Context Protocol) server that allows AI agents to interact with the API. To start the MCP server:

```bash
pydanticai-api-template run-mcp
```

The MCP server will be available at http://localhost:3001, and provides the following tools:
- `chat`: Send a message to the AI assistant and receive a response

You can connect to the MCP server from any MCP client, for example:

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP

server = MCPServerHTTP(url='http://localhost:3001/sse')
agent = Agent('openai:gpt-4o', mcp_servers=[server])

async def main():
    async with agent.run_mcp_servers():
        result = await agent.run('Your message here')
    print(result.data)
```

## Environment Variables

Create a `.env` file in the project root to store your API keys and other environment variables:

```
OPENAI_API_KEY=your_api_key_here
```

The application will load these variables automatically at runtime. Note that the status check command looks for environment variables directly, so it may show warnings even when your app is working correctly with the .env file.

## Status Check

Run `check` or `pydanticai-api-template check` to verify your environment is properly configured.

## Alternative Setup Options

While Dev Containers is the recommended approach, alternative setup options are documented in the [Developer Guide](./docs/DEVELOPER.md).
