#!/usr/bin/env python
"""
Cleanup Script

This script removes unwanted files and directories that might be created
during development or container startup.

Usage:
    python scripts/cleanup.py
"""

import os
import shutil
from pathlib import Path


def remove_invalid_dirs() -> None:
    """Remove directories with invalid names (like '*' wildcards)."""
    root_dir = Path(".")

    # List of problematic directory patterns to check and remove
    problem_dirs = ["**", "@**", "*"]

    for item in root_dir.iterdir():
        if item.is_dir() and item.name in problem_dirs:
            try:
                print(f"Removing problematic directory: {item}")
                shutil.rmtree(item, ignore_errors=True)
            except Exception as e:
                print(f"Error removing {item}: {e}")


def clean_pycache() -> None:
    """Clean __pycache__ directories recursively."""
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                print(f"Removing __pycache__ from: {pycache_path}")
                shutil.rmtree(pycache_path)
            except Exception as e:
                print(f"Error removing {pycache_path}: {e}")


def remove_egg_info() -> None:
    """Remove .egg-info directories if present and in .gitignore."""
    root_dir = Path(".")
    for item in root_dir.iterdir():
        if item.is_dir() and item.name.endswith(".egg-info"):
            try:
                print(f"Removing egg-info: {item}")
                shutil.rmtree(item)
            except Exception as e:
                print(f"Error removing {item}: {e}")


def main() -> None:
    """Main cleanup function."""
    print("Starting cleanup...")

    # Remove problematic directories
    remove_invalid_dirs()

    # Clean __pycache__ directories
    clean_pycache()

    # Remove .egg-info if present
    remove_egg_info()

    print("Cleanup complete!")


if __name__ == "__main__":
    main()
