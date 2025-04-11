from typing import Optional

import typer
import uvicorn

app = typer.Typer(help="PydanticAI API Template CLI")


@app.command()
def run(
    host: str = typer.Option("0.0.0.0", help="Host address to bind the server to."),
    port: int = typer.Option(8000, help="Port number to bind the server to."),
    reload: bool = typer.Option(True, help="Enable auto-reload on code changes."),
    workers: int = typer.Option(1, help="Number of worker processes."),
    log_level: str = typer.Option(
        "info", help="Logging level (e.g., debug, info, warning, error, critical)."
    ),
) -> None:
    """Run the FastAPI application server."""
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_level=log_level,
    )


@app.command()
def version() -> None:
    """Show the application version."""
    import importlib.metadata

    try:
        version = importlib.metadata.version("pydanticai-api-template")
        typer.echo(f"pydanticai-api-template version: {version}")
    except importlib.metadata.PackageNotFoundError:
        typer.echo("pydanticai-api-template version: unknown")


@app.command()
def install_completion(
    shell: Optional[str] = typer.Argument(
        None, help="The shell to install completion for (bash, zsh, fish)."
    )
) -> None:
    """Install shell completion for the CLI.

    Supported shells: bash, zsh, fish

    Example: pydanticai-api-template install-completion zsh

    """
    typer.echo("Installing shell completion...")
    # Use the simple shell completion approach
    if shell is None:
        # Use Typer's built-in way to show help/error if argument is missing
        # or prompt if interactive
        # For simplicity here, we'll just error out if not provided.
        typer.echo(
            "Error: Missing argument SHELL. Please specify bash, zsh, or fish.",
            err=True,
        )
        raise typer.Exit(code=1)  # Exit with error code

    import os

    # Removed unused import subprocess

    # Get completion script based on shell
    if shell == "bash":
        # Use regular strings, f-string prefix was unnecessary
        completion_script = 'eval "$(_PYDANTICAI_API_TEMPLATE_COMPLETE=bash_source pydanticai-api-template)"'
        config_file = os.path.expanduser("~/.bashrc")
    elif shell == "zsh":
        completion_script = 'eval "$(_PYDANTICAI_API_TEMPLATE_COMPLETE=zsh_source pydanticai-api-template)"'
        config_file = os.path.expanduser("~/.zshrc")
    elif shell == "fish":
        completion_script = "eval (env _PYDANTICAI_API_TEMPLATE_COMPLETE=fish_source pydanticai-api-template)"
        config_file = os.path.expanduser("~/.config/fish/config.fish")
    else:
        typer.echo(
            f"Unsupported shell: {shell}. Supported shells are bash, zsh, fish.",
            err=True,
        )
        raise typer.Exit(code=1)  # Exit with error code

    # Append to shell config if it doesn't exist
    try:
        config_content = ""
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config_content = f.read()

        if completion_script not in config_content:
            with open(config_file, "a") as f:
                f.write(f"\n# PydanticAI API Template completion\n{completion_script}\n")
            typer.echo(f"Added completion to {config_file}")
        else:
            typer.echo(f"Completion script already exists in {config_file}")

    except OSError as e:
        typer.echo(
            f"Error accessing shell configuration file {config_file}: {e}", err=True
        )
        raise typer.Exit(code=1)

    typer.echo(
        "Shell completion script added. Please restart your shell or source the config file (e.g., 'source ~/.zshrc') for changes to take effect."
    )


@app.command()
def validate() -> None:
    """Validate application configuration and environment."""
    import sys

    typer.echo("✅ Python version: " + sys.version)

    import fastapi

    typer.echo(f"✅ FastAPI version: {fastapi.__version__}")

    try:
        import uvicorn

        typer.echo(f"✅ Uvicorn version: {uvicorn.__version__}")
    except ImportError:
        typer.echo("❌ Uvicorn not installed")

    # Check if we're running in a container
    import os

    if os.path.exists("/.dockerenv"):
        typer.echo("✅ Running in Docker container")
    else:
        typer.echo("⚠️ Not running in Docker container")

    typer.echo("\nApplication ready to run! 🚀")


@app.command()
def cleanup() -> None:
    """Clean up temporary files and directories."""
    typer.echo("Cleaning up temporary files and directories...")

    import importlib.util
    import sys

    # Import the cleanup script
    cleanup_path = "scripts/cleanup.py"
    spec = importlib.util.spec_from_file_location("cleanup", cleanup_path)
    if spec and spec.loader:
        cleanup_module = importlib.util.module_from_spec(spec)
        sys.modules["cleanup"] = cleanup_module
        spec.loader.exec_module(cleanup_module)

        # Run the cleanup
        cleanup_module.main()
    else:
        typer.echo(f"❌ Could not find cleanup script at {cleanup_path}")
        return

    typer.echo("✅ Cleanup complete!")


if __name__ == "__main__":
    app()
