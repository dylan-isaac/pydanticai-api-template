import importlib.metadata
import importlib.util
import os
import sys
from pathlib import Path
from typing import Optional

import typer
import uvicorn
import yaml  # Moved import to top level

# Get the project name from pyproject.toml or define it
PROJECT_NAME = "pydanticai-api-template"
CLI_NAME = "pat"  # New CLI command name

app = typer.Typer(help=f"{PROJECT_NAME} CLI")


@app.command()  # type: ignore[misc]
def run(
    host: str = typer.Option(
        "0.0.0.0", "--host", "-h", help="Host address to bind the server to."
    ),
    port: int = typer.Option(
        8000, "--port", "-p", help="Port number to bind the server to."
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
    # Updated path to the FastAPI app instance
    app_path = "pydanticai_api_template.api.endpoints:app"
    typer.echo(f"Starting Uvicorn server for {app_path}...")
    uvicorn.run(
        app_path,  # Use the updated path
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_level=log_level.lower(),  # Ensure log level is lowercase
    )


@app.command()  # type: ignore[misc]
def version() -> None:
    """Show the application version."""
    try:
        pkg_version = importlib.metadata.version(PROJECT_NAME)
        typer.echo(f"{PROJECT_NAME} version: {pkg_version}")
    except importlib.metadata.PackageNotFoundError:
        typer.echo(
            f"{PROJECT_NAME} version: unknown "
            "(package not installed or metadata missing?)"
        )


@app.command()  # type: ignore[misc]
def install_completion(
    shell: Optional[str] = typer.Argument(
        None,
        help=(
            "The shell to install completion for. "
            "If not provided, detects the current shell."
        ),
        show_default=False,  # Don't show default value in help
    ),
) -> None:
    """Install shell completion for the CLI.

    Tries to detect the shell if not provided.
    Supported shells: bash, zsh, fish
    Example: pat install-completion zsh
    """
    # Improved shell detection and handling from axe-ai
    if shell is None:
        shell = typer.prompt(
            "Which shell do you want to install completion for? (bash, zsh, fish)",
            default=os.path.basename(os.getenv("SHELL", "bash")),  # Sensible default
        )

    shell = shell.lower()
    cli_name = CLI_NAME  # Use the defined CLI name
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

    # Ensure config directory exists for fish
    if shell == "fish":
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        config_content = ""
        if config_file_path.exists():
            config_content = config_file_path.read_text()

        completion_comment = f"# {PROJECT_NAME} completion"
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


@app.command()  # type: ignore[misc]
def validate() -> None:
    """Validate application configuration and environment."""
    typer.echo("🔍 Validating environment...")
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    typer.echo(f"✅ Python version: {python_version}")

    # Check key dependencies
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

    # Check OpenAI Key (optional)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        typer.echo(f"✅ OpenAI API Key found (Length: {len(openai_key)})")
    else:
        typer.echo("⚠️ OpenAI API Key (OPENAI_API_KEY) not set in environment.")

    # Check if running in Docker (more robust check)
    if Path("/.dockerenv").exists() or os.getenv("DOTENV_RUNNING_IN_DOCKER") == "true":
        typer.echo("✅ Running inside a Docker container")
    else:
        typer.echo("ℹ️ Not running inside a known Docker container environment")

    typer.echo("\nValidation complete. Basic checks passed. ��")


@app.command()  # type: ignore[misc]
def cleanup() -> None:
    """Clean up temporary files and directories (like __pycache__)."""
    typer.echo("🧹 Cleaning up temporary files...")
    # Updated path to the cleanup script
    cleanup_script_path = Path(__file__).parent / "utils" / "cleanup.py"

    if not cleanup_script_path.exists():
        typer.echo(f"❌ Cleanup script not found at: {cleanup_script_path}", err=True)
        raise typer.Exit(code=1)

    try:
        # Dynamically import and run the main function from the cleanup script
        spec = importlib.util.spec_from_file_location(
            "cleanup_script", str(cleanup_script_path)
        )
        if spec and spec.loader:
            cleanup_module = importlib.util.module_from_spec(spec)
            sys.modules["cleanup_script"] = (
                cleanup_module  # Add to sys.modules temporarily
            )
            spec.loader.exec_module(cleanup_module)
            if hasattr(cleanup_module, "main"):  # Check if main function exists
                cleanup_module.main()  # Execute the main function
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


@app.command()  # type: ignore[misc]
def lint() -> None:
    """Run code quality checks using Ruff."""
    import shutil
    import subprocess

    typer.echo("🔍 Running code quality checks...")

    # Check if we're inside a dev container
    in_container = Path("/.dockerenv").exists()

    # Check if 'make' is available
    if shutil.which("make"):
        try:
            # Use Make command which handles dependency installation if needed
            result = subprocess.run(
                ["make", "lint"], check=True, capture_output=True, text=True
            )
            typer.echo(result.stdout)
            typer.echo("✅ Linting complete!")
        except subprocess.CalledProcessError as e:
            if in_container:
                # If in container and make failed, try direct commands
                # with --system flag
                typer.echo("Make command failed, trying direct commands...")
                try:
                    # Run Ruff check
                    typer.echo("Running Ruff check...")
                    subprocess.run(["ruff", "check", "."], check=True)

                    # Run Ruff format check
                    typer.echo("Running Ruff format check...")
                    subprocess.run(["ruff", "format", "--check", "."], check=True)

                    typer.echo("✅ Linting complete!")
                    return
                except subprocess.CalledProcessError:
                    pass
            # If we get here, both approaches failed
            typer.echo(f"❌ Linting failed:\n{e.stdout}\n{e.stderr}", err=True)
            raise typer.Exit(code=1)
    else:
        # Fallback to direct commands if Make is not available
        try:
            # Install dev dependencies if not in container (container should have them)
            if not in_container:
                typer.echo("Installing development dependencies...")
                subprocess.run(
                    ["uv", "pip", "install", "-e", ".[dev]"],
                    check=True,
                    capture_output=True,
                )
            else:
                # In container, use --system flag to avoid venv issues
                typer.echo("Installing development dependencies with system flag...")
                subprocess.run(
                    ["uv", "pip", "install", "--system", "-e", ".[dev]"],
                    check=True,
                    capture_output=True,
                )

            # Run Ruff check
            typer.echo("Running Ruff check...")
            subprocess.run(["ruff", "check", "."], check=True)

            # Run Ruff format check
            typer.echo("Running Ruff format check...")
            subprocess.run(["ruff", "format", "--check", "."], check=True)

            typer.echo("✅ Linting complete!")
        except subprocess.CalledProcessError:
            typer.echo("❌ Linting failed!", err=True)
            raise typer.Exit(code=1)


@app.command()  # type: ignore[misc]
def test() -> None:
    """Run tests using pytest."""
    import shutil
    import subprocess

    typer.echo("🧪 Running tests...")

    # Check if we're inside a dev container
    in_container = Path("/.dockerenv").exists()

    # Check if 'make' is available
    if shutil.which("make"):
        try:
            # Use Make command which handles dependency installation if needed
            result = subprocess.run(
                ["make", "test"], check=True, capture_output=True, text=True
            )
            typer.echo(result.stdout)
            typer.echo("✅ Tests complete!")
        except subprocess.CalledProcessError as e:
            if in_container:
                # If in container and make failed, try direct command
                typer.echo("Make command failed, trying direct command...")
                try:
                    subprocess.run(["pytest"], check=True)
                    typer.echo("✅ Tests complete!")
                    return
                except subprocess.CalledProcessError:
                    pass
            # If we get here, both approaches failed
            typer.echo(f"❌ Tests failed:\n{e.stdout}\n{e.stderr}", err=True)
            raise typer.Exit(code=1)
    else:
        # Fallback to direct commands if Make is not available
        try:
            # Install test dependencies if not in container (container should have them)
            if not in_container:
                typer.echo("Installing test dependencies...")
                subprocess.run(
                    ["uv", "pip", "install", "-e", ".[dev,test]"],
                    check=True,
                    capture_output=True,
                )
            else:
                # In container, use --system flag to avoid venv issues
                typer.echo("Installing test dependencies with system flag...")
                subprocess.run(
                    ["uv", "pip", "install", "--system", "-e", ".[dev,test]"],
                    check=True,
                    capture_output=True,
                )

            # Run pytest
            typer.echo("Running pytest...")
            subprocess.run(["pytest"], check=True)

            typer.echo("✅ Tests complete!")
        except subprocess.CalledProcessError:
            typer.echo("❌ Tests failed!", err=True)
            raise typer.Exit(code=1)


@app.command()  # type: ignore[misc]
def sync() -> None:
    """Synchronize project configuration files."""
    typer.echo("🔄 Synchronizing configuration files...")
    # Updated path to the sync script
    sync_script_path = (
        Path(__file__).parent.parent.parent / "scripts" / "tasks" / "update_configs.py"
    )

    if not sync_script_path.exists():
        typer.echo(f"❌ Sync script not found at: {sync_script_path}", err=True)
        raise typer.Exit(code=1)

    try:
        # Dynamically import and run the main function from the sync script
        spec = importlib.util.spec_from_file_location(
            "sync_script", str(sync_script_path)
        )
        if spec and spec.loader:
            sync_module = importlib.util.module_from_spec(spec)
            sys.modules["sync_script"] = sync_module  # Add to sys.modules temporarily
            spec.loader.exec_module(sync_module)
            if hasattr(sync_module, "main"):  # Check if main function exists
                sync_module.main()  # Execute the main function
                typer.echo("✅ Configuration synchronization complete!")
            else:
                typer.echo(
                    f"❌ 'main' function not found in {sync_script_path}", err=True
                )
                raise typer.Exit(code=1)
        else:
            typer.echo(
                f"❌ Could not load sync script from {sync_script_path}", err=True
            )
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ An error occurred during synchronization: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()  # type: ignore[misc]
def check() -> None:
    """Perform a quick status check of the development environment."""
    import shutil
    import socket

    typer.echo("🔍 PydanticAI API Template Status Check")

    # Check Python and dependencies (reuse validate command)
    validate()

    # Check if server port is available
    port = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("localhost", port))
        typer.echo(f"✅ Port {port} is available")
    except socket.error:
        typer.echo(f"⚠️ Port {port} is already in use. Is the server running?")
    finally:
        s.close()

    # Check Docker status if in container
    if os.path.exists("/.dockerenv"):
        typer.echo("✅ Running inside Docker container")

    # Check required CLI tools
    for cmd in ["curl", "make", "git"]:
        if shutil.which(cmd):
            typer.echo(f"✅ {cmd} is installed")
        else:
            typer.echo(f"❌ {cmd} is not installed")

    typer.echo("\n✨ Status check complete")


@app.command()  # type: ignore[misc]
def run_mcp(
    host: str = typer.Option(
        "0.0.0.0", "--host", "-h", help="Host address to bind the MCP server to."
    ),
    port: int = typer.Option(
        3001, "--port", "-p", help="Port number to bind the MCP server to."
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
    """Run the MCP server for AI agent access."""
    # Set environment variables for the MCP server
    os.environ["MCP_HOST"] = host
    os.environ["MCP_PORT"] = str(port)

    # Use an import string instead of directly calling create_app()
    app_path = "pydanticai_api_template.mcp_server:create_app"

    typer.echo(f"Starting MCP server on {host}:{port}...")
    try:
        uvicorn.run(
            app_path,
            host=host,
            port=port,
            reload=reload,
            log_level=log_level.lower(),
            factory=True,  # Explicitly tell Uvicorn this is a factory function
        )
    except ImportError as e:
        typer.echo(f"Error importing MCP server: {e}", err=True)
        typer.echo("Please make sure pydantic-ai[mcp] and mcp packages are installed.")
        raise typer.Exit(code=1)


@app.command()  # type: ignore[misc]
def prompt_test(
    config_path: str = typer.Option(
        "promptfoo/config.yaml",
        "--config",
        "-c",
        help="Path to the promptfoo config file.",
    ),
    view: bool = typer.Option(
        False, "--view", "-v", help="Open the web UI after running tests."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="Show detailed logs during test execution."
    ),
) -> None:
    """Test prompts using promptfoo."""
    import shutil
    import subprocess
    from pathlib import Path

    # Check if npm is available
    npm_exec = shutil.which("npm")
    if not npm_exec:
        typer.echo(
            "❌ npm command not found. Please install Node.js and npm.",
            err=True,
        )
        raise typer.Exit(code=1)

    # Check if config file exists
    config_file = Path(config_path)
    if not config_file.exists():
        typer.echo(f"❌ Config file not found at: {config_file}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"🧪 Running prompt tests using config at {config_file}...")

    # Use environment variables from .env file
    from dotenv import load_dotenv

    load_dotenv()

    # Setup logfire for prompt testing
    from pydanticai_api_template.utils.observability import setup_logfire

    setup_logfire(service_name="promptfoo-testing")

    # If verbose, display the test cases being run
    if verbose:
        try:
            # Try to import yaml in a way that mypy won't complain about
            # import yaml  # type: ignore # Removed from here
            yaml_available = True
        except ImportError:
            yaml_available = False

        if yaml_available:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
                typer.echo("\n📋 Test Configuration:")
                typer.echo(f"  Prompts: {len(config.get('prompts', []))} defined")
                typer.echo(f"  Providers: {len(config.get('providers', []))} defined")

                test_cases = config.get("testCases", [])
                typer.echo(f"  Test Cases: {len(test_cases)} defined")
                for i, test in enumerate(test_cases):
                    typer.echo(
                        f"    {i + 1}. {test.get('description', 'Unnamed test')}"
                    )
                    input_text = test.get("vars", {}).get("input", "None")
                    # Truncate long inputs for display
                    truncated_input = (
                        input_text[:50] + "..." if len(input_text) > 50 else input_text
                    )
                    typer.echo(f"       Input: {truncated_input}")
                    typer.echo(f"       Assertions: {len(test.get('assert', []))}")
                typer.echo("")
        else:
            typer.echo("⚠️ PyYAML not installed. Skipping verbose test case display.")

    try:
        # Use npm directly for running promptfoo commands
        typer.echo("Running promptfoo using npm...")

        # Create environment with PATH that doesn't include Python's bin directory
        # to avoid confusion with any pip-installed promptfoo
        env = os.environ.copy()
        node_path = os.path.dirname(npm_exec)
        if "PATH" in env:
            paths = env["PATH"].split(os.pathsep)
            # Filter out paths that might contain pip-installed binaries
            filtered_paths = [
                p for p in paths if not (p.endswith("/bin") and "python" in p)
            ]
            # Ensure node path is first
            if node_path not in filtered_paths:
                filtered_paths.insert(0, node_path)
            env["PATH"] = os.pathsep.join(filtered_paths)

        # Add verbose flag if requested
        extra_args = ["--verbose"] if verbose else []

        # Run promptfoo eval using npm exec
        eval_cmd = [
            "npm",
            "exec",
            "--",
            "promptfoo",
            "eval",
            "--config",
            str(config_file),
        ] + extra_args
        subprocess.run(eval_cmd, check=True, env=env)
        typer.echo("✅ Prompt tests complete!")

        # Open web UI if requested
        if view:
            typer.echo("🌐 Opening promptfoo web UI...")
            view_cmd = ["npm", "exec", "--", "promptfoo", "view"]
            subprocess.run(view_cmd, check=True, env=env)
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Prompt tests failed: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()  # type: ignore[misc]
def setup_logfire() -> None:
    """Set up Logfire authentication and project configuration.

    This runs the Logfire CLI commands to authenticate and set the current project.
    """
    import shutil
    import subprocess

    typer.echo("🔄 Setting up Logfire...")

    # Check if logfire is available
    logfire_exec = shutil.which("logfire")
    if not logfire_exec:
        typer.echo(
            "❌ logfire command not found. Please ensure it's installed.", err=True
        )
        raise typer.Exit(code=1)

    try:
        # Run logfire auth
        typer.echo("📝 Running logfire authentication...")
        subprocess.run(["logfire", "auth"], check=True)

        # Set project to pydantic-ai-template
        typer.echo("🔧 Setting Logfire project to pydantic-ai-template...")
        subprocess.run(
            ["logfire", "projects", "use", "pydantic-ai-template"], check=True
        )

        typer.echo("✅ Logfire setup complete!")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Error setting up Logfire: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
