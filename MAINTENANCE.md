# Project Maintenance Guide

This document explains how the project's configuration files are structured, how they relate to each other, and how to maintain them when making changes.

## Configuration File Hierarchy

The project uses several configuration files that work together to create a seamless developer experience:

1. **pyproject.toml** - Primary configuration file (dependencies, project metadata, tool configs)
2. **Makefile** - Universal command interface 
3. **Docker** files (Dockerfile, Dockerfile.dev, docker-compose.yml)
4. **VS Code** configurations (.devcontainer/devcontainer.json, .vscode/tasks.json)
5. **Pre-commit** configuration (.pre-commit-config.yaml)

## Git Configuration in Dev Containers

The development container includes Git configuration from the host system to provide a seamless experience. The configuration in `docker-compose.yml` maps your host Git config and credentials into the container, eliminating the need to configure Git inside the container.

Git environment variables (GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME, GIT_COMMITTER_EMAIL) are also passed from the host to the container if they are set. This ensures that Git commits made inside the container are attributed correctly.

If users experience Git credential issues, ensure they have configured Git on their host machine.

## Config Synchronization Tool

To help keep configuration files in sync, the project includes a config synchronization tool in `scripts/update_configs.py`. This tool:

1. Reads from `pyproject.toml` as the single source of truth
2. Updates related configuration files automatically

To use it:

```bash
# Using make
make sync-configs

# Or directly
python scripts/update_configs.py
```

This will:
- Update pre-commit hook versions from dev dependencies
- Generate VS Code tasks based on available CLI commands
- Keep configurations in sync

Run this tool whenever you make significant changes to dependencies or CLI commands.

## Maintenance Guidelines

### Adding New Dependencies

When adding new dependencies:

1. Update `pyproject.toml` first:
   ```bash
   # For regular dependencies
   uv add <package-name>
   
   # For dev dependencies
   uv add --dev <package-name>
   ```

2. Run the config sync tool:
   ```bash
   make sync-configs
   ```

3. Update Docker images if needed:
   ```bash
   # Rebuild Docker images with new dependencies
   docker compose build
   ```

### Adding/Changing CLI Commands

When modifying the CLI:

1. Update `app/cli.py` to add or modify commands
2. Update automated tests as needed
3. Run the config sync tool to update VS Code tasks:
   ```bash
   make sync-configs
   ```
4. If necessary, manually update:
   - Makefile commands
   - README.md documentation

### Updating Docker Configuration

When changing Docker setup:

1. Modify `Dockerfile` and/or `Dockerfile.dev`
2. Update `docker-compose.yml` if service configuration changes
3. Test both production and development containers
4. If changing mounted paths or environment variables, also update `.devcontainer/devcontainer.json`

### Updating VS Code Configuration

When enhancing VS Code experience:

1. Modify `.devcontainer/devcontainer.json` for container settings, extensions, etc.
2. Tasks will be updated automatically by the sync tool, but you can manually edit `.vscode/tasks.json` if needed
3. Consider adding helpful VS Code settings in `.vscode/settings.json`

### Modifying Linting/Formatting Rules

When changing code quality tools:

1. Update configurations in `pyproject.toml` (ruff, black, mypy sections)
2. Run the config sync tool to update pre-commit hook versions:
   ```bash
   make sync-configs
   ```
3. Consider running linting on entire codebase after changes

### Updating Core Dependencies

When updating major dependencies like Python, FastAPI, or UV:

1.  **Review Changelogs**: Check the official changelogs for breaking changes or important migration notes.
2.  **Update `pyproject.toml`**: Modify the version constraints as needed (e.g., `python = "^3.12"`). Use `uv add <package>@latest` or specify versions.
3.  **Update `Dockerfile` / `.devcontainer`**: Ensure the base images (e.g., `python:3.12-slim`) or setup steps reflect the new versions.
4.  **Run `uv sync`**: Update the `uv.lock` file.
5.  **Run `make sync-configs`**: Update any related config files.
6.  **Thorough Testing**: Run all tests (`make test`) and manually test key features, especially those related to the updated dependency.
7.  **Update Documentation**: Note the new versions in `README.md` or relevant places if significant.

## Dependency Graph

Here's how the configuration files depend on each other:

```
pyproject.toml           # Primary source of truth for dependencies
    │
    ├── Dockerfile       # Uses dependencies from pyproject.toml
    │   └── CI/CD        # Production container used in CI/CD
    │
    ├── Dockerfile.dev   # Development container definition
    │   ├── docker-compose.yml       # Uses dev container
    │   └── .devcontainer/devcontainer.json  # Uses docker-compose
    │
    ├── .pre-commit-config.yaml  # Should align with dev dependencies
    │   └── (updated by sync tool)
    │
    ├── Makefile         # Commands should match available CLI commands
    │
    └── .vscode/tasks.json  # Tasks should align with CLI commands
        └── (updated by sync tool)
```

## Adding New Development Tools

When adding new development tools:

1. Add as a dev dependency in `pyproject.toml`
2. Run `make sync-configs` to update related configs
3. Add tool configuration in `pyproject.toml` if supported
4. Update VS Code extensions in `.devcontainer/devcontainer.json` if there's a corresponding extension
5. Add helpful Make commands in `Makefile`
6. Document in README.md

## Troubleshooting

### Container-related Issues

If the CLI doesn't work in containers:
1. Verify the symlink in the Dockerfile: `RUN ... && ln -s $(which pydanticai-api-template) /usr/local/bin/pydanticai-api-template`
2. Check Python path and installation: `python -m app.cli`
3. Debug with `docker compose exec pydanticai-api-template-dev which pydanticai-api-template`

### VS Code Dev Container Issues

If VS Code dev containers don't work:
1. Check Docker installation and permissions
2. Verify Dev Containers extension is installed
3. Try rebuilding: Command Palette → "Dev Containers: Rebuild Container"
4. Check VS Code logs: Command Palette → "Developer: Show Logs"

### Make Command Issues

If Make commands fail:
1. Verify Make is installed: `make --version`
2. Check command formatting in Makefile
3. Run with verbose output: `make -v <command>`

## CI/CD Integration

For CI/CD integration:

1. Use the production Docker container as the environment
2. Run validation using `pydanticai-api-template validate`
3. Run tests using your test framework of choice
4. Use health checks to verify deployment

Example GitHub Actions workflow fragment:
```yaml
- uses: actions/checkout@v3
- name: Build container
  run: docker build -t pydanticai-api-template .
- name: Validate
  run: docker run pydanticai-api-template pydanticai-api-template validate
- name: Run tests
  run: docker run pydanticai-api-template pytest
```

## Final Checklist for Updates

Before committing significant changes:

- [ ] Update `pyproject.toml` with new dependencies/configurations
- [ ] Run `make sync-configs` to update related configuration files
- [ ] Update Docker configurations if needed
- [ ] Verify dev container works with VS Code
- [ ] Test all Make commands
- [ ] Update documentation in README.md
- [ ] Run pre-commit hooks: `pre-commit run --all-files` 