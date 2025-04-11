#!/usr/bin/env python
"""
Config Synchronization Tool

This script helps keep configuration files in sync by reading from pyproject.toml
and updating related configuration files like pre-commit config.

Usage:
    python scripts/update_configs.py

This will:
1. Read dependencies from pyproject.toml
2. Update version numbers in .pre-commit-config.yaml
3. Generate/update other configuration files as needed
"""

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, cast

try:
    import tomli  # type: ignore
except ImportError:
    print("tomli not found. Installing...")
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "tomli"])
    import tomli  # type: ignore

try:
    import yaml  # type: ignore
except ImportError:
    print("PyYAML not found. Installing...")
    import subprocess

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "PyYAML", "types-PyYAML"]
    )
    import yaml  # type: ignore


def read_pyproject() -> Dict[str, Any]:
    """Read the pyproject.toml file."""
    try:
        with open("pyproject.toml", "rb") as f:
            return cast(Dict[str, Any], tomli.load(f))
    except Exception as e:
        print(f"Error reading pyproject.toml: {e}")
        sys.exit(1)


def update_precommit_config(pyproject: Dict[str, Any]) -> None:
    """Update pre-commit config with versions from pyproject.toml."""
    precommit_path = Path(".pre-commit-config.yaml")

    if not precommit_path.exists():
        print(".pre-commit-config.yaml not found, skipping")
        return

    # Read current pre-commit config
    with open(precommit_path, "r") as f:
        precommit = yaml.safe_load(f)

    # Get dev dependencies versions
    dev_deps = (
        pyproject.get("project", {}).get("optional-dependencies", {}).get("dev", {})
    )

    # Map package names to pre-commit repos
    package_to_repo = {
        "black": {"repo": "https://github.com/psf/black", "id": "black"},
        "ruff": {"repo": "https://github.com/astral-sh/ruff-pre-commit", "id": "ruff"},
    }

    # Extract versions from dev dependencies
    for dep in dev_deps:
        for pkg, repo_info in package_to_repo.items():
            if dep.startswith(pkg):
                # Extract version using regex
                version_match = re.search(r">=([0-9\.]+)", dep)
                if version_match:
                    version = version_match.group(1)

                    # Update pre-commit config if repo exists
                    for repo in precommit["repos"]:
                        if repo["repo"] == repo_info["repo"]:
                            old_rev = repo["rev"]
                            # Format version as vX.Y.Z for pre-commit
                            new_rev = f"v{version}"
                            if old_rev != new_rev:
                                repo["rev"] = new_rev
                                print(
                                    f"Updated {pkg} version from {old_rev} to {new_rev}"
                                )

    # Write updated pre-commit config
    with open(precommit_path, "w") as f:
        yaml.dump(precommit, f, sort_keys=False)

    print("Updated .pre-commit-config.yaml")


def update_vscode_tasks(pyproject: Dict[str, Any]) -> None:
    """Update VS Code tasks based on available CLI commands."""
    tasks_path = Path(".vscode/tasks.json")

    if not os.path.exists(".vscode"):
        os.makedirs(".vscode")

    # Define base structure if file doesn't exist
    if not tasks_path.exists():
        tasks: Dict[str, Any] = {"version": "2.0.0", "tasks": []}
    else:
        with open(tasks_path, "r") as f:
            tasks = yaml.safe_load(f) or {"version": "2.0.0", "tasks": []}

    # Define tasks based on CLI commands
    cli_tasks = [
        {
            "label": "Run API (Dev)",
            "type": "shell",
            "command": "pydanticai-api-template run --reload",
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "new"},
            "group": {"kind": "build", "isDefault": True},
        },
        {
            "label": "Run Validation",
            "type": "shell",
            "command": "pydanticai-api-template validate",
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "new"},
        },
        {
            "label": "Install Shell Completion",
            "type": "shell",
            "command": "pydanticai-api-template install-completion",
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "new"},
        },
        {
            "label": "Run Cleanup",
            "type": "shell",
            "command": "pydanticai-api-template cleanup",
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "new"},
        },
    ]

    # Update tasks
    tasks["tasks"] = cli_tasks

    # Write updated tasks
    with open(tasks_path, "w") as f:
        yaml.dump(tasks, f, sort_keys=False)

    print("Updated .vscode/tasks.json")


def main() -> None:
    """Main function to update all configs."""
    print("Starting config synchronization...")

    pyproject = read_pyproject()
    update_precommit_config(pyproject)
    update_vscode_tasks(pyproject)

    print("Config synchronization complete!")


if __name__ == "__main__":
    main()
