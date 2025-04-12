# Developer Guide

This guide provides detailed setup instructions and development workflows for the PydanticAI API Template.

## Setting Up Your Development Environment

### Recommended: VS Code / Cursor with Dev Containers

This provides the most seamless experience:

1. Install the prerequisites:
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - [VS Code](https://code.visualstudio.com/) or [Cursor](https://cursor.sh/)
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   - A [Nerd Font](https://www.nerdfonts.com/) for terminal icons (optional but recommended)

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pydanticai-api-template.git
   cd pydanticai-api-template
   ```

3. Open in VS Code/Cursor:
   ```bash
   code .  # Or open using the editor's UI
   ```

4. When prompted, click "Reopen in Container" or use the Command Palette:
   ```
   Dev Containers: Reopen in Container
   ```

5. After the container builds (may take a few minutes the first time), you'll see a welcome message with available commands.

### Development Workflow

Once the dev container is running:

1. **Start the server:**
   - Type `start` in the terminal, or
   - Press `Cmd+Shift+B` (macOS) or `Ctrl+Shift+B` (Windows/Linux), or
   - Use VS Code's tasks menu

2. **Access the API:**
   - API documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Run common tasks:**
   - `lint` - Check code quality
   - `test` - Run tests
   - `validate` - Verify environment
   - `sync` - Sync configurations
   - `help` - Show all available commands

4. **Debugging:**
   - Open the Debug panel in VS Code/Cursor
   - Select "FastAPI: Debug Server" configuration
   - Press F5 to start debugging

## Environment Variables

Create a `.env` file in the project root to store your API keys and other configuration:

```
OPENAI_API_KEY=your_api_key_here
```

The application will load these variables automatically at runtime. Note that the status check command looks for environment variables directly, so it may show warnings even when your app is working correctly with the .env file.

## Project Structure

```
src/
└── pydanticai_api_template/    # Main Python package
    ├── __init__.py             # Package marker, exports version
    ├── api/                    # API related modules
    │   ├── endpoints.py        # FastAPI endpoints/routes
    │   └── models.py           # Pydantic models for API requests/responses
    └── cli.py                  # Typer CLI application logic
```

## Common Development Tasks

### Adding a New Endpoint

1. Add your Pydantic models in `src/pydanticai_api_template/api/models.py`
2. Create your endpoint in `src/pydanticai_api_template/api/endpoints.py`
3. Test your endpoint using the interactive docs

### Adding a New CLI Command

1. Modify `src/pydanticai_api_template/cli.py`
2. Run `sync` to update VS Code tasks

### Updating Dependencies

1. Update `pyproject.toml`
2. Run `uv sync` to update the lock file
3. Run `sync` to keep configurations in sync

## Troubleshooting

### Server Won't Start

Check:
- Port 8000 availability: `check` will verify
- Logging: Look for error messages
- Container status: Run `docker ps` on the host

### Dev Container Issues

- Try rebuilding: Command Palette → "Dev Containers: Rebuild Container"
- Check Docker logs: `docker logs <container-id>`
- Verify Docker Desktop is running

### Environment Variable Issues

- If the application works but status checks still show warnings about missing environment variables, this is expected behavior. The status check looks for variables directly in the environment while the app loads from the `.env` file.
- Ensure your `.env` file is in the project root directory
- Double-check that the variables match the expected format

### Other Issues

See [MAINTENANCE.md](../MAINTENANCE.md) for more troubleshooting information.
