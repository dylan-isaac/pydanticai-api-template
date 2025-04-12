# PydanticAI API Template: Leveraging PydanticAI with FastAPI, UV, and Docker

A modern Python project demonstrating structured AI interactions using PydanticAI, served via a high-performance FastAPI web API, managed with UV, and containerized with Docker for an exceptional developer experience.

## 🚀 Features

- **PydanticAI**: Structured interactions with Large Language Models (LLMs) using Pydantic models
- **FastAPI**: High-performance API framework with automatic docs
- **UV**: Fast dependency management and virtual environments
- **Docker**: Containerization for consistent deployment
- **Python 3.12**: Latest Python features and performance
- **Typer CLI**: Command-line interface for easy application management
- **Dev Containers**: VS Code / Cursor integration for zero-configuration setup
- **Pre-configured tools**: Linting, formatting (Ruff), and testing ready to go
- **Config Sync**: Automated tool to keep configuration files in sync

## 📋 Prerequisites

- Python 3.12+
- [UV](https://github.com/astral-sh/uv) package manager
- Docker (optional, for containerization)
- [Cursor](https://cursor.sh) or VS Code with Dev Containers extension (optional, for optimal dev experience)

### Font for Terminal Icons (Optional but Recommended)

The development environment uses tools like `eza` (a modern `ls` replacement) with icons enabled (`--icons`). For these icons to render correctly in the integrated terminal (VS Code / Cursor), you need to install a "Nerd Font" on your **host machine** and configure your terminal emulator (or VS Code/Cursor directly) to use it.

- The `.devcontainer/devcontainer.json` suggests using `MesloLGS NF`.
- You can download `MesloLGS NF` or other Nerd Fonts from the [Nerd Fonts website](https://www.nerdfonts.com/) or directly from [here](https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/Meslo.zip).
- After installation, ensure your terminal or VS Code/Cursor settings (outside the dev container config) are updated to use the chosen Nerd Font. For VS Code/Cursor, you might add `"terminal.integrated.fontFamily": "MesloLGS NF"` to your user `settings.json`.

## 🛠️ Development Quick Start

Choose your preferred development workflow:

### ✨ Recommended: Dev Containers (Cursor or VS Code)

The most seamless experience with zero configuration:

1. Install [Cursor](https://cursor.sh/) or VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. Clone the repository and open it in Cursor/VS Code.
3. Click "Reopen in Container" when prompted (or use the Command Palette: `Dev Containers: Reopen in Container`).
4. Everything is automatically set up - dependencies, extensions, and tools!
5. Press `Cmd+Shift+B` (macOS) or `Ctrl+Shift+B` (Windows/Linux) to run the default build task (start development server).

Benefits:
- No local Python/dependency setup needed.
- Consistent environment for all developers.
- Pre-configured extensions and settings.
- Enhanced terminal experience with Zsh, Oh My Zsh, and modern tools.

### Alternative Setup Options

⚠️ These options require manual setup and are less recommended than Dev Containers:

<details>
<summary><b>Option 2: Make Commands (Universal Interface)</b></summary>

Use Make as a universal interface for common commands, assuming you have Python 3.12, UV, and Make installed locally.

```bash
# Clone the repository
git clone <your-repo-url>
cd pydanticai-api-template # Changed directory name

# Set up everything in one command (installs dependencies, etc.)
make setup

# Start development server locally
make dev

# Run linting tools locally
make lint

# Run tests locally
make test

# Start docker development container (requires Docker)
make docker-up

# Get a zsh shell in the running container (requires Docker)
make docker-shell

# Sync configurations (see Configuration Sync section below)
make sync-configs
```

See the `Makefile` for all available commands.
</details>

<details>
<summary><b>Option 3: Docker Compose Directly</b></summary>

Requires Docker installed.

```bash
# Start the development container with hot reload
# Use the service name defined in docker-compose.yml
docker compose up pydanticai-api-template-dev # Updated service name

# Run commands in the container
docker compose exec pydanticai-api-template-dev pydanticai-api-template run --reload # Updated service and command name
```
</details>

<details>
<summary><b>Option 4: Local Python Development</b></summary>

Requires Python 3.12 and UV installed locally.

```bash
# Clone the repository
git clone <your-repo-url>
cd pydanticai-api-template # Changed directory name

# Install dependencies (UV automatically creates/uses a virtual environment)
uv sync
# Install the package in editable mode for development
uv pip install -e .

# Run the app with hot reload
pydanticai-api-template run --reload # Updated command name

# Install shell completion for CLI (optional)
# This adds completion logic to your shell's config file (e.g., .bashrc, .zshrc)
pydanticai-api-template install-completion # Updated command name
```
</details>

### Configuration Synchronization

The project includes a tool (`scripts/update_configs.py`) to keep configuration files in sync with `pyproject.toml`.

```bash
# Sync configurations from pyproject.toml using Make
make sync-configs

# Or run the script directly (ensure dev dependencies are installed)
python scripts/update_configs.py
```

**When to run this command:**
1. After adding or modifying CLI commands in `src/pydanticai_api_template/cli.py` - this updates VS Code tasks in `.vscode/tasks.json`.
2. After updating development tool versions (like Ruff, MyPy, pre-commit) in `pyproject.toml` - this syncs versions in `.pre-commit-config.yaml`.
3. After pulling changes that might affect these areas.

This ensures that your VS Code tasks and pre-commit hooks stay consistent with the primary project definitions. See [MAINTENANCE.md](./MAINTENANCE.md) for more details.

## 📚 Development Tools & Features

### Interactive CLI

The project includes a command-line interface built with Typer:

```bash
# Start the server
pydanticai-api-template run

# Show the application version
pydanticai-api-template version

# Install shell completion (Bash, Zsh, Fish supported)
pydanticai-api-template install-completion

# Validate your environment (basic checks)
pydanticai-api-template validate

# Clean up temporary files (like __pycache__)
pydanticai-api-template cleanup
```

### Cursor / VS Code Integration (via Dev Containers)

When using Dev Containers:

- Press `Cmd+Shift+B` (macOS) or `Ctrl+Shift+B` (Windows/Linux) to run the default task (development server).
- Use Command Palette (`Cmd+P` or `Ctrl+P`) → Type `task ` and select "Tasks: Run Task" to access other tasks (linting, testing, config sync) defined in `.vscode/tasks.json`.
- Automatic code formatting on save using Ruff.
- Integrated linting (Ruff) and type checking (MyPy).
- Preconfigured testing with pytest.
- Useful VS Code extensions are automatically installed inside the container:
  - Python tooling (Python, Pylance, Ruff, MyPy)
  - Documentation helpers (AutoDocstring, Spell Checker)
  - Docker support
  - Git integration (GitLens, GitHub PR)
  - TOML, YAML, and EditorConfig support
  - Development utilities (Live Share, TODO highlighting)

### Pre-commit Hooks

The repository includes pre-commit hooks configured in `.pre-commit-config.yaml` for code quality (linting, formatting checks). They run automatically on commit if installed.

```bash
# Install hooks into your .git/hooks directory (run once per clone)
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### API Documentation

FastAPI automatically generates interactive API documentation, available when the server is running:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Example API Endpoints

- `GET /`: Basic welcome endpoint.
- `POST /chat`: Sends a message to the PydanticAI agent and receives a structured reply.
  - Requires `OPENAI_API_KEY` environment variable to be set.
  - Request Body: `{ "message": "Your message here" }`
  - Response Body: `{ "reply": "AI's response here" }` (Structure defined by `ChatResponse` model)

## ⚙️ Configuration

The application uses environment variables for configuration. Key variables:

- `OPENAI_API_KEY`: **Required** for the `/chat` endpoint. Your API key for OpenAI.

Environment variables can be set:
- Directly in your shell: `export OPENAI_API_KEY='your_key'`
- In a `.env` file in the project root (this file is ignored by Git). The application will load it automatically using `python-dotenv`. Example `.env` file:
  ```
  OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
- Via Docker environment variables (e.g., in `docker-compose.yml` or `docker run -e`).

## 🤔 Why This Stack?

This project template combines several modern tools for a robust and efficient development experience for building AI-powered applications:

- **PydanticAI**: Central to the project, it leverages Pydantic models for structured, predictable, and type-safe interactions with LLMs. This simplifies data validation and parsing of AI outputs.
- **FastAPI**: For building high-performance APIs quickly. Its native Pydantic integration complements PydanticAI perfectly, providing automatic data validation, serialization, and documentation for API endpoints.
- **UV**: Provides extremely fast dependency management and virtual environment handling, significantly speeding up setup, development iterations, and CI/CD pipelines compared to traditional tools.
- **Typer**: Creates a clean and user-friendly command-line interface for managing the application, based on Python type hints.
- **Docker & Dev Containers**: Ensures consistent development and production environments, simplifying onboarding, reducing "works on my machine" issues, and streamlining deployment. Includes an enhanced terminal environment.
- **Ruff**: An extremely fast Python linter and formatter, written in Rust. Used for linting, formatting, and import sorting, replacing tools like Black, Flake8, and isort.
- **Pre-commit**: Automates running checks (like linting and formatting) before commits, ensuring code quality and consistency.
- **MyPy**: Static type checker to help catch type errors before runtime.

## 🐳 Docker Configuration

### Development Container (`Dockerfile.dev` / `docker-compose.yml`)

Our development container (`pydanticai-api-template-dev` service in `docker-compose.yml`) provides:
- **Hot code reloading**: Changes in the mounted `/app` directory trigger server restarts.
- **Volume mounting**: Your local code is mounted into `/app` for real-time editing.
  - **Performance**: Key directories like `.venv` and `__pycache__` inside the container are excluded from the host mount to improve performance using named volumes or excluding paths.
- **Git Integration**: Host `.gitconfig` and `.git-credentials` are mounted into the container for seamless Git operations. Environment variables like `GIT_AUTHOR_NAME` are also passed through.
- **Enhanced Shell**: Zsh with Oh My Zsh, useful plugins (autosuggestions, syntax highlighting), and modern CLI tools (Eza, Bat, Zoxide, Starship prompt) are pre-installed.
- **Performance Optimizations**:
  - Python bytecode generation (`.pyc` files) is disabled (`PYTHONDONTWRITEBYTECODE=1`) for faster startup/reloads in development.
  - Health checks monitor the FastAPI application's status.
- **Editable Install**: The project is installed using `uv pip install -e .` so the `pydanticai-api-template` command works directly.

### Production Container (`Dockerfile`)

A multi-stage build optimized for production:
- Uses a slim Python base image.
- Installs only necessary dependencies (no dev tools).
- Copies only required source code.
- Runs the application using the `pydanticai-api-template` CLI entry point.

Build and run the production container:

```bash
# Build the production image
docker build -t pydanticai-api-template .

# Run the container
# Make sure to pass required environment variables (e.g., OPENAI_API_KEY)
docker run -p 8000:8000 -e OPENAI_API_KEY='your_key' pydanticai-api-template
```

## 📁 Project Structure (Post-Refactor)

```
.
├── src/                             # Source code directory
│   └── pydanticai_api_template/     # Main Python package
│       ├── __init__.py              # Package marker, exports version
│       ├── api/                     # API related modules
│       │   ├── __init__.py          # API sub-package marker
│       │   ├── endpoints.py         # FastAPI endpoints/routes
│       │   └── models.py            # Pydantic models for API requests/responses
│       └── cli.py                   # Typer CLI application logic
├── scripts/                         # Utility scripts
│   ├── update_configs.py            # Configuration synchronization tool
│   └── cleanup.py                   # Cleanup utility script
├── tests/                           # Tests (Example placeholder)
│   └── __init__.py
├── .devcontainer/                   # VS Code / Cursor Dev Container configuration
│   └── devcontainer.json
├── .vscode/                         # VS Code / Cursor settings and tasks
│   ├── extensions.json              # Recommended extensions (for non-devcontainer users)
│   ├── launch.json                  # Debug configurations (example)
│   └── settings.json                # Workspace settings
│   └── tasks.json                   # Task definitions (run, lint, test, sync)
├── .dockerignore                    # Files to exclude from Docker build context
├── .env.example                     # Example environment variables file
├── .gitignore                       # Files ignored by Git
├── .pre-commit-config.yaml          # Pre-commit hook configurations
├── .python-version                  # Specifies Python version (for tools like pyenv)
├── Dockerfile                       # Production container build definition
├── Dockerfile.dev                   # Development container build definition
├── docker-compose.yml               # Docker Compose configuration for dev workflow
├── LICENSE                          # Project License file (Consider adding one, e.g., MIT)
├── main.py                          # Simple entry point for CLI (if needed, often redundant with project.scripts)
├── MAINTENANCE.md                   # Documentation for maintainers
├── Makefile                         # Universal command interface using Make
├── pyproject.toml                   # Project metadata, dependencies, tool config (PEP 621)
├── README.md                        # This file
└── uv.lock                          # Locked dependencies (generated by `uv sync`)
```

## 📝 Dependency Management

[UV](https://github.com/astral-sh/uv) is used for fast, reliable dependency management and virtual environment creation.

```bash
# Install/update dependencies based on pyproject.toml and lock file
# Creates a .venv if one doesn't exist
uv sync

# Add a runtime dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Install the project itself in editable mode (for development)
uv pip install -e .

# Show installed packages
uv pip list

# Run a command within the managed environment
uv run <command> # e.g., uv run pytest
```

The `uv.lock` file ensures reproducible builds by locking dependency versions. Commit this file to your repository.

## 🔄 CI/CD Preparation

This project is structured for straightforward CI/CD integration:

- **Reproducible builds**: `uv.lock` ensures consistent dependencies across environments.
- **Health checks**: The development container includes health checks; similar checks can be implemented in production deployments.
- **Optimized Docker images**: The production `Dockerfile` uses best practices for smaller, more secure images.
- **CLI Validation**: `pydanticai-api-template validate` command can be used as a basic check.
- **Testing**: Tests can be run easily within the container (`make test` or `docker compose exec ... pytest`).

Example GitHub Actions workflow snippet:

```yaml
name: CI Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4 # Updated action version

      - name: Build Production Container
        run: docker build -t pydanticai-api-template .

      - name: Run Basic Validation (using CLI)
        run: docker run pydanticai-api-template pydanticai-api-template validate

      - name: Run Tests (using pytest via CLI)
        # Mount test results or artifacts if needed
        # Ensure required env vars for tests are passed if necessary
        run: docker run pydanticai-api-template pytest # Assumes tests are included or run via CLI command
```

## 🧪 Testing

Testing is set up using `pytest`.

```bash
# Run tests using Make (recommended, handles environment)
make test

# Run tests directly using uv (if uv sync/install is done)
uv run pytest

# Run tests inside the running development Docker container
docker compose exec pydanticai-api-template-dev pytest # Updated service name
```

Consider adding more tests in the `tests/` directory.

## ⚡ Performance Tips

- The development container disables Python bytecode generation (`PYTHONDONTWRITEBYTECODE=1`) for faster reloads.
- Docker volume mounting excludes virtual environment and cache directories (`/app/.venv`, `/app/**/__pycache__`) from the host bind mount to improve I/O performance, using container volumes instead where appropriate.
- UV provides significantly faster dependency resolution and installation compared to pip+venv.

## 📖 Additional Documentation

For maintainers, see [MAINTENANCE.md](./MAINTENANCE.md) for detailed information on:
- Configuration file relationships and the sync tool.
- How to update dependencies and core components.
- Maintaining Docker and Dev Container configurations.
- Troubleshooting common issues.

## ✅ TODO / Next Steps

- [ ] **Add Your Code**: Implement your specific PydanticAI agents, API logic, and features within the `src/pydanticai_api_template/` directory.
- [ ] **Write Tests**: Add comprehensive tests for your application logic in the `tests/` directory.
- [ ] **Add License**: Choose and add a `LICENSE` file (e.g., MIT, Apache 2.0).
- [ ] **Configure CI/CD**: Set up a full CI/CD pipeline using GitHub Actions, GitLab CI, or another service based on the example provided.
- [ ] **Customize Rules for AI**: Consider adding project-specific [Rules for AI](https://docs.cursor.com/context/rules-for-ai) in `.cursor/rules` (if using Cursor) to guide AI behavior (e.g., preferred coding styles, framework usage).
- [ ] **Review Dependencies**: Ensure all dependencies in `pyproject.toml` are necessary for your project.
