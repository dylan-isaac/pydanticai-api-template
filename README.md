# PydanticAI API Template: Leveraging PydanticAI with FastAPI, UV, and Docker

A modern Python project demonstrating structured AI interactions using PydanticAI, served via a high-performance FastAPI web API, managed with UV, and containerized with Docker for an exceptional developer experience.

## 🚀 Features

- **PydanticAI**: Structured interactions with Large Language Models (LLMs) using Pydantic models
- **FastAPI**: High-performance API framework with automatic docs
- **UV**: Fast dependency management and virtual environments
- **Docker**: Containerization for consistent deployment
- **Python 3.12**: Latest Python features and performance
- **Typer CLI**: Command-line interface for easy application management
- **Dev Containers**: VS Code integration for zero-configuration setup
- **Pre-configured tools**: Linting, formatting, and testing ready to go
- **Config Sync**: Automated tool to keep configuration files in sync

## 📋 Prerequisites

- Python 3.12+
- [UV](https://github.com/astral-sh/uv) package manager
- Docker (optional, for containerization)
- [Cursor](https://cursor.sh) (optional, for optimal dev experience)

## 🛠️ Development Quick Start

Choose your preferred development workflow:

### Option 1: Cursor Dev Containers (Recommended)

The most seamless experience with zero configuration:

1. Install [Cursor](https://cursor.sh/)
2. Clone the repository and open it in Cursor
3. Click "Reopen in Container" when prompted
4. Everything is automatically set up - dependencies, extensions, and tools!
5. Press `Cmd+Shift+B` (macOS) or `Ctrl+Shift+B` (Windows/Linux) to start the development server

Benefits:
- No local Python/dependency setup needed
- Consistent environment for all developers
- Pre-configured extensions and settings

### Option 2: Make Commands (Universal)

Use Make as a universal interface for common commands:

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Set up everything in one command
make setup

# Start development server
make dev

# Run linting tools
make lint

# Run tests
make test

# Start docker development container
make docker-up

# Get a shell in the running container
make docker-shell

# Sync configurations
make sync-configs
```

Available make commands:
- `make setup` - Complete first-time setup
- `make dev` - Start development server
- `make lint` - Run linting tools
- `make test` - Run tests
- `make docker-up` - Start docker development container
- `make docker-shell` - Get a shell in the running container
- `make sync-configs` - Synchronize configuration files

### Option 3: Docker Compose Directly

```bash
# Start the development container with hot reload
docker compose up pydanticai-api-template-dev

# Run commands in the container
docker compose exec pydanticai-api-template-dev pydanticai-api-template run --reload
```

### Option 4: Local Python Development

For traditional local Python development:

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Install dependencies (UV automatically creates a virtual environment)
uv sync
uv pip install -e .

# Run the app with hot reload
pydanticai-api-template run --reload

# Install shell completion for CLI
pydanticai-api-template install-completion
```

## 📚 Development Tools & Features

### Interactive CLI

The project includes a powerful command-line interface:

```bash
# Start the server
pydanticai-api-template run

# Show the application version
pydanticai-api-template version

# Install shell completion
pydanticai-api-template install-completion

# Validate your environment
pydanticai-api-template validate
```

### Cursor Integration

When using Cursor (either with or without Dev Containers):

- Press `Cmd+Shift+B` (macOS) or `Ctrl+Shift+B` (Windows/Linux) to run the development server
- Use Command Palette (`Cmd+P` or `Ctrl+P`) → Type `task ` and select "Tasks: Run Task" to access other tasks
- Automatic code formatting on save
- Integrated linting and type checking
- Preconfigured testing

### Pre-commit Hooks

The repository includes pre-commit hooks for code quality:

```bash
# Install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

### Config Synchronization

The project includes a tool to keep configuration files in sync:

```bash
# Sync configurations from pyproject.toml
make sync-configs
```

This ensures that:
- Pre-commit hook versions match dev dependencies
- Cursor tasks reflect available CLI commands
- Configurations stay in sync as the project evolves

### API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Example API Endpoints

- `GET /`: Basic welcome endpoint.
- `POST /chat`: Sends a message to the PydanticAI agent and receives a structured reply.
  - Request Body: `{ "message": "Your message here" }`
  - Response Body: `{ "reply": "AI's response here" }`

## ⚙️ Configuration

The application uses environment variables for configuration. Key variables:

- `OPENAI_API_KEY`: **Required** for the `/chat` endpoint. Your API key for OpenAI.

Environment variables can be set directly in your shell or placed in a `.env` file in the project root (this file is ignored by Git).

## 🤔 Why This Stack?

This project template combines several modern tools to create a robust and efficient development experience for building AI-powered applications:

- **PydanticAI**: Central to the project, it leverages Pydantic models for structured, predictable, and type-safe interactions with Large Language Models (LLMs). This simplifies data validation and parsing of AI outputs.
- **FastAPI**: For building high-performance APIs quickly. Its native Pydantic integration complements PydanticAI perfectly, providing automatic validation and documentation for AI-driven endpoints.
- **UV**: Provides extremely fast dependency management and virtual environment handling, significantly speeding up setup, development iterations, and CI/CD pipelines.
- **Typer**: Creates a clean and user-friendly command-line interface for managing the application, including AI-related tasks or configurations.
- **Docker & Dev Containers**: Ensures consistent development and production environments, simplifying onboarding and deployment.
- **Pre-commit & Ruff/Black/MyPy**: Enforces code quality and consistency automatically.

## 🐳 Docker Configuration

### Development Container Features

Our development container provides:
- Hot code reloading
- Volume mounting for real-time code editing
- Git credentials automatically mounted from host (no manual Git setup needed)
- Performance optimizations:
  - Python bytecode caching disabled for faster reloads
  - Smart volume exclusions for dependency directories
  - Health checks for service status monitoring
- Proper installation of the CLI tool

### Production Container

Build and run the production container:

```bash
docker build -t pydanticai-api-template .
docker run -p 8000:8000 pydanticai-api-template
```

## �� Project Structure

```
.
├── app/                 # Application code
│   ├── main.py          # Main FastAPI application
│   └── cli.py           # Typer CLI implementation
├── scripts/             # Utility scripts
│   └── update_configs.py # Configuration synchronization tool
├── .devcontainer/       # VS Code / Cursor container configuration
├── .vscode/             # VS Code / Cursor settings and tasks
├── main.py              # CLI entrypoint
├── .dockerignore        # Files to exclude from Docker context
├── Dockerfile           # Production container configuration
├── Dockerfile.dev       # Development container configuration
├── docker-compose.yml   # Docker Compose configuration for dev workflow
├── pyproject.toml       # Project metadata and dependencies
├── Makefile             # Universal command interface
├── MAINTENANCE.md       # Maintenance documentation
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── uv.lock              # Locked dependencies (generated by UV)
└── README.md            # Project documentation
```

## 📝 Dependency Management

UV is used for fast, reliable dependency management:

```bash
# Add dependencies
uv add <package-name>

# Add dev dependencies
uv add --dev <package-name>

# Update lock file
uv sync
```

## 🔄 CI/CD Preparation

This project is set up for easy CI/CD integration:

- **Reproducible builds**: UV lock file ensures consistent dependencies
- **Health checks**: Container health monitoring for deployment verification
- **Optimized Docker images**: Multi-stage builds and proper .dockerignore
- **Environment separation**: Development vs production configurations

For a CI pipeline, use the following example workflow:

```yaml
# Example GitHub Actions workflow
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build container
        run: docker build -t pydanticai-api-template .
      - name: Validate
        run: docker run pydanticai-api-template pydanticai-api-template validate
      - name: Run tests
        run: docker run pydanticai-api-template pytest
```

## 🧪 Testing

```bash
# Run tests with local Python
pytest

# With make
make test

# In Docker
docker compose exec pydanticai-api-template-dev pytest
```

## ⚡ Performance Tips

- The development container disables Python bytecode generation for faster reloads
- Volume mounting excludes `.venv` and `__pycache__` directories for better performance
- UV provides much faster dependency resolution than pip

## 📖 Additional Documentation

For maintainers, see [MAINTENANCE.md](./MAINTENANCE.md) for detailed information on:
- Configuration file relationships
- How to update dependencies properly
- Maintaining multiple configuration files
- Troubleshooting common issues

## ✅ TODO

- [ ] Add project-specific [Rules for AI](https://docs.cursor.com/context/rules-for-ai) in `.cursor/rules` to guide AI behavior (e.g., preferred coding styles, framework usage).
