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

## Project Documentation

- [Developer Guide](./docs/DEVELOPER.md) - Detailed setup and workflows
- [Architecture](./docs/ARCHITECTURE.md) - System design and patterns
- [Maintenance](./MAINTENANCE.md) - Configuration management
- [API Reference](./docs/API.md) - API endpoint documentation

## Features

- **PydanticAI**: Structured interactions with LLMs using Pydantic models
- **FastAPI**: High-performance API framework with automatic docs
- **UV**: Fast dependency management and virtual environments
- **Docker**: Containerization for consistent deployment
- **Dev Containers**: VS Code / Cursor integration for zero-configuration setup
- **Modern Tooling**: Ruff, MyPy, Typer CLI, and more

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
