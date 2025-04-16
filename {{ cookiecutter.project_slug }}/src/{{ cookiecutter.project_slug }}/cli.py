import importlib.metadata
import importlib.util
import os
import secrets
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
import uvicorn

# Placeholder flags - These will be replaced by the post-gen hook
_MCP_ENABLED = False
_LOGFIRE_ENABLED = False

# Static values - these might need adjustment or post-gen modification
# Consider deriving these dynamically if possible, or set by post-gen hook
_PROJECT_SLUG = "pydanticai_api_template"  # Placeholder, adjust post-gen
_PROJECT_NAME_DISPLAY = "PydanticAI API Template"  # Placeholder, adjust post-gen
_CLI_COMMAND = "pat"
_DEFAULT_PORT = 8000  # Placeholder, adjust post-gen
_MCP_PORT = 3001  # Placeholder, adjust post-gen

app = typer.Typer(help=f"{_PROJECT_NAME_DISPLAY} CLI")


@app.command()
def run(
    host: str = typer.Option(
        "0.0.0.0", "--host", "-h", help="Host address to bind the server to."
    ),
    port: int = typer.Option(
        _DEFAULT_PORT, "--port", "-p", help="Port number to bind the server to."
    ),
    reload: bool = typer.Option(
        True, "--reload", help="Enable auto-reload on code changes."
    ),
    workers: int = typer.Option(
        1, "--workers", "-w", help="Number of worker processes."
    ),
    log_level: str = typer.Option(
        "info",
        "--log-level",
        help="Logging level (e.g., debug, info, warning, error, critical).",
    ),
) -> None:
    """Run the FastAPI application server."""
    app_path = f"{_PROJECT_SLUG}.api.endpoints:app"
    typer.echo(f"Starting Uvicorn server for {app_path}...")
    uvicorn.run(
        app_path,
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_level=log_level.lower(),
    )


@app.command()
def version() -> None:
    """Show the application version."""
    try:
        pkg_version = importlib.metadata.version(_PROJECT_SLUG)
        typer.echo(f"'{_PROJECT_NAME_DISPLAY}' version: {pkg_version}")
    except importlib.metadata.PackageNotFoundError:
        typer.echo(
            f"'{_PROJECT_NAME_DISPLAY}' version: unknown "
            "(package not installed or metadata missing?)"
        )


@app.command()
def install_completion(
    shell: Optional[str] = typer.Argument(
        None,
        help=(
            "The shell to install completion for. "
            "If not provided, detects the current shell."
        ),
        show_default=False,
    ),
) -> None:
    """Install shell completion for the CLI."""
    if shell is None:
        shell = typer.prompt(
            "Which shell do you want to install completion for? (bash, zsh, fish)",
            default=os.path.basename(os.getenv("SHELL", "bash")),
        )

    shell = shell.lower()
    cli_name = _CLI_COMMAND
    env_var_name = f"_{cli_name.upper().replace('-', '_')}_COMPLETE"

    completion_script = ""
    config_file_path = None

    if shell == "bash":
        completion_script = f'eval "$({env_var_name}=bash_source {cli_name})"'
        config_file_path = Path.home() / ".bashrc"
    elif shell == "zsh":
        completion_script = f'eval "$({env_var_name}=zsh_source {cli_name})"'
        config_file_path = Path.home() / ".zshrc"
    elif shell == "fish":
        completion_script = f"eval (env {env_var_name}=fish_source {cli_name})"
        config_file_path = Path.home() / ".config/fish/config.fish"
    else:
        typer.echo(
            f"Unsupported shell: {shell}. Supported shells are bash, zsh, fish.",
            err=True,
        )
        raise typer.Exit(code=1)

    typer.echo(f"Attempting to add completion for {shell} to {config_file_path}...")

    if shell == "fish":
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        config_content = ""
        if config_file_path.exists():
            config_content = config_file_path.read_text()

        completion_comment = f"# {_PROJECT_NAME_DISPLAY} completion"
        if completion_script not in config_content:
            with config_file_path.open("a") as f:
                f.write(f"\n{completion_comment}\n{completion_script}\n")
            typer.echo(f"✅ Added completion script to {config_file_path}")
        else:
            typer.echo(f"ℹ️ Completion script already exists in {config_file_path}")

        typer.echo(
            "\nPlease restart your shell or source the config file "
            "(e.g., 'source ~/.zshrc') for changes to take effect."
        )

    except OSError as e:
        typer.echo(
            f"❌ Error accessing shell configuration file {config_file_path}: {e}",
            err=True,
        )
        typer.echo("You may need to add the script manually:")
        typer.echo(f"  {completion_script}")
        raise typer.Exit(code=1)


@app.command()
def validate() -> None:
    """Validate application configuration and environment."""
    typer.echo("🔍 Validating environment...")
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    typer.echo(f"✅ Python version: {python_version}")

    deps_to_check = ["fastapi", "uvicorn", "pydantic", "pydantic_ai", "typer"]
    for dep in deps_to_check:
        try:
            version = importlib.metadata.version(dep)
            typer.echo(f"✅ {dep} version: {version}")
        except importlib.metadata.PackageNotFoundError:
            typer.echo(
                f"⚠️ {dep} package not found "
                "(might be OK if not needed for current task)"
            )

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        typer.echo(f"✅ OpenAI API Key found (Length: {len(openai_key)})")
    else:
        typer.echo("⚠️ OpenAI API Key (OPENAI_API_KEY) not set in environment.")

    if Path("/.dockerenv").exists() or os.getenv("DOTENV_RUNNING_IN_DOCKER") == "true":
        typer.echo("✅ Running inside a Docker container")
    else:
        typer.echo("ℹ️ Not running inside a known Docker container environment")

    typer.echo("\nValidation complete. Basic checks passed.")


@app.command()
def cleanup() -> None:
    """Clean up temporary files and directories (like __pycache__)."""
    typer.echo("🧹 Cleaning up temporary files...")
    # Assuming utils/cleanup.py is generic enough or handled by post-gen
    cleanup_script_path = Path(__file__).parent / "utils" / "cleanup.py"

    if not cleanup_script_path.exists():
        typer.echo(f"❌ Cleanup script not found at: {cleanup_script_path}", err=True)
        raise typer.Exit(code=1)
    try:
        spec = importlib.util.spec_from_file_location(
            "cleanup_script", str(cleanup_script_path)
        )
        if spec and spec.loader:
            cleanup_module = importlib.util.module_from_spec(spec)
            sys.modules["cleanup_script"] = cleanup_module
            spec.loader.exec_module(cleanup_module)
            if hasattr(cleanup_module, "main"):
                cleanup_module.main()
                typer.echo("✅ Cleanup complete!")
            else:
                typer.echo(
                    f"❌ 'main' function not found in {cleanup_script_path}", err=True
                )
                raise typer.Exit(code=1)
        else:
            typer.echo(
                f"❌ Could not load cleanup script from {cleanup_script_path}", err=True
            )
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ An error occurred during cleanup: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def lint() -> None:
    """Run code quality checks using Ruff and Markdownlint."""
    typer.echo("🔍 Running code quality checks...")
    errors_found = False

    in_container = Path("/.dockerenv").exists()

    typer.echo("--- Running lint commands ---")
    commands = [
        ("Ruff check", ["ruff", "check", "."]),
        ("Ruff format check", ["ruff", "format", "--check", "."]),
        ("Markdownlint", ["markdownlint", "README.md", "docs/"]),
    ]

    required_tools = ["ruff", "markdownlint"]
    missing_tools = [tool for tool in required_tools if not shutil.which(tool)]

    if missing_tools:
        install_cmd = "uv pip install -U ruff markdownlint-cli"
        typer.echo(
            f"⚠️ Missing tools: {', '.join(missing_tools)}. Attempting install..."
        )
        try:
            subprocess.run(install_cmd, shell=True, check=True, capture_output=True)
            typer.echo("✅ Tools installed successfully.")
        except subprocess.CalledProcessError as e:
            typer.echo(f"❌ Failed to install missing tools: {e}", err=True)
            typer.echo(f"Output:\n{e.stderr.decode()}")
            raise typer.Exit(code=1)

    for name, cmd in commands:
        try:
            typer.echo(f"\n▶️ Running {name}...")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if result.stdout:
                typer.echo(result.stdout)
            if result.stderr:
                typer.echo(result.stderr, err=True)
            typer.echo(f"✅ {name} passed.")
        except FileNotFoundError:
            typer.echo(f"❌ Error: Command '{cmd[0]}' not found.", err=True)
            errors_found = True
        except subprocess.CalledProcessError as e:
            typer.echo(f"❌ {name} failed:", err=True)
            typer.echo(e.stdout, err=True)
            typer.echo(e.stderr, err=True)
            errors_found = True
        except Exception as e:
            typer.echo(f"❌ An unexpected error occurred during {name}: {e}", err=True)
            errors_found = True

    if errors_found:
        typer.echo("\n❌ Code quality checks failed.")
        raise typer.Exit(code=1)
    else:
        typer.echo("\n✅ All code quality checks passed.")


@app.command()
def test() -> None:
    """Run tests using pytest."""
    typer.echo("🚀 Running tests...")
    pytest_cmd = ["pytest"]

    if not shutil.which("pytest"):
        install_cmd = "uv pip install -U pytest pytest-cov pytest-asyncio"
        typer.echo("⚠️ pytest not found. Attempting install...")
        try:
            subprocess.run(install_cmd, shell=True, check=True, capture_output=True)
            typer.echo("✅ pytest installed successfully.")
        except subprocess.CalledProcessError as e:
            typer.echo(f"❌ Failed to install pytest: {e}", err=True)
            typer.echo(f"Output:\n{e.stderr.decode()}")
            raise typer.Exit(code=1)

    try:
        subprocess.run(pytest_cmd, check=True)
        typer.echo("\n✅ Tests passed!")
    except subprocess.CalledProcessError:
        typer.echo("\n❌ Tests failed.", err=True)
        raise typer.Exit(code=1)
    except FileNotFoundError:
        typer.echo("❌ Error: 'pytest' command not found.", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ An unexpected error occurred during testing: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def sync() -> None:
    """Synchronize configurations (e.g., pre-commit hooks, VSCode tasks)."""
    typer.echo("🔄 Synchronizing configurations...")
    sync_script = Path("scripts/tasks/update_configs.py")
    if not sync_script.exists():
        typer.echo(f"❌ Sync script not found: {sync_script}", err=True)
        raise typer.Exit(code=1)

    try:
        # Ensure dependencies for the script are installed if needed
        try:
            import tomli
        except ImportError:
            typer.echo("Installing dependencies for sync script...")
            subprocess.run(
                ["uv", "pip", "install", "tomli"],
                check=True,
                capture_output=True,
            )

        subprocess.run([sys.executable, str(sync_script)], check=True)
        typer.echo("✅ Configurations synchronized.")
    except Exception as e:
        typer.echo(f"❌ Error during configuration sync: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def check() -> None:
    """Run all checks: validate, lint, and test."""
    typer.echo("🔄 Running all checks...")
    try:
        validate()
        lint()
        test()
        typer.echo("\n✅ All checks passed!")
    except typer.Exit as e:
        typer.echo("\n❌ One or more checks failed.", err=True)
        raise typer.Exit(code=e.code)
    except Exception as e:
        typer.echo(f"\n❌ An unexpected error occurred during checks: {e}", err=True)
        raise typer.Exit(code=1)


# --- MCP Server Command --- #
@app.command()
def run_mcp(
    host: str = typer.Option(
        "0.0.0.0", "--host", "-h", help="Host address to bind the MCP server to."
    ),
    port: int = typer.Option(
        _MCP_PORT, "--port", "-p", help="Port number to bind the MCP server to."
    ),
    reload: bool = typer.Option(
        True, "--reload", help="Enable auto-reload on code changes."
    ),
    log_level: str = typer.Option(
        "info",
        "--log-level",
        help="Logging level (e.g., debug, info, warning, error, critical).",
    ),
) -> None:
    """Run the MCP (Model Context Protocol) server (if enabled)."""
    if not _MCP_ENABLED:
        typer.echo(
            "MCP Server feature is not enabled in the project configuration.", err=True
        )
        raise typer.Exit(code=1)

    try:
        # Assumes mcp_server:app exists for uvicorn and slug is correct
        mcp_app_path = f"{_PROJECT_SLUG}.mcp_server:app"
        typer.echo(f"Starting MCP server on {host}:{port}...")
        uvicorn.run(
            mcp_app_path,
            host=host,
            port=port,
            reload=reload,
            log_level=log_level.lower(),
        )
    except ImportError:
        typer.echo(
            "Error: Could not import MCP server components. Is 'mcp' extra installed?",
            err=True,
        )
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error running MCP server: {e}", err=True)
        raise typer.Exit(code=1)


# --- Logfire Setup Command --- #
@app.command()
def setup_logfire() -> None:
    """Authenticate with Logfire and configure the current project (if enabled)."""
    if not _LOGFIRE_ENABLED:
        typer.echo(
            "Logfire feature is not enabled in the project configuration.", err=True
        )
        raise typer.Exit(code=1)

    typer.echo("🔧 Setting up Logfire...")

    if not shutil.which("logfire"):
        typer.echo(
            "Error: 'logfire' CLI tool not found. Please install it (`uv pip install logfire`) or ensure it's in your PATH.",
            err=True,
        )
        raise typer.Exit(code=1)

    try:
        typer.echo("--- Running Logfire Authentication ---")
        auth_result = subprocess.run(["logfire", "auth"], check=False)
        if auth_result.returncode != 0:
            typer.echo("Logfire authentication failed or was cancelled.", err=True)
            raise typer.Exit(code=1)
        typer.echo("Authenticated successfully.")

        project_name_suggestion = _PROJECT_NAME_DISPLAY
        typer.echo(
            f"--- Configuring Logfire project (Suggested: {project_name_suggestion}) ---"
        )
        use_result = subprocess.run(["logfire", "use"], check=False)
        if use_result.returncode != 0:
            typer.echo(
                "Logfire project configuration failed or was cancelled.", err=True
            )
            raise typer.Exit(code=1)
        typer.echo("Logfire project configured successfully.")

        typer.echo("✅ Logfire setup complete.")

    except Exception as e:
        typer.echo(f"An error occurred during Logfire setup: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def generate_api_key() -> None:
    """Generate a secure random API key."""
    # ... (Keep existing key generation logic) ...
    key = secrets.token_urlsafe(32)
    typer.echo("Generated API Key:")
    typer.echo(key)
    typer.echo("\nPlease add this key to your .env file.")
    # Consider showing the exact variable name based on cookiecutter input?
    # Example: typer.echo(f"Add as: {{ cookiecutter.api_key_env_var }}={key}")
    # Requires passing the variable to the script or reading it post-gen
    # For now, keep it generic.


if __name__ == "__main__":
    app()
