import os
import re  # Import re for substitutions
import shutil
import subprocess
import sys

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
LICENSE_CHOICE = "{{ cookiecutter.open_source_license }}"
USE_MCP = "{{ cookiecutter.use_mcp_server }}" == "y"
USE_LOGFIRE = "{{ cookiecutter.use_logfire }}" == "y"  # Added flag for Logfire
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PROJECT_NAME_DISPLAY = "{{ cookiecutter.project_name }}"
DEFAULT_PORT = "{{ cookiecutter.default_port }}"
MCP_PORT = "{{ cookiecutter.mcp_server_port }}"
REPO_NAME = "{{ cookiecutter.repo_name }}"


def remove_file(filepath):
    try:
        os.remove(os.path.join(PROJECT_DIRECTORY, filepath))
    except FileNotFoundError:
        print(f"Warning: Could not find file {filepath} to remove.")
    except OSError as e:
        print(f"Error removing file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def copy_license_file(license_name):
    """Copies the selected license file from the template root to the project root."""
    # NOTE: This assumes cookiecutter runs hooks AFTER copying the project
    # directory but BEFORE removing the temporary source template directory.
    # A safer approach might involve including the license file within the
    # templated directory itself and then moving/removing it here.
    # Let's stick to the simpler approach for now, assuming the hook
    # environment allows access relative to the template source OR placing
    # licenses/ inside the {{cookiecutter.project_slug}} initially.

    # --- Robust approach: Expect licenses dir INSIDE generated project initially ---
    # This is more reliable as cookiecutter guarantees the context.
    source_path = os.path.join(PROJECT_DIRECTORY, "licenses", license_name)
    dest_path = os.path.join(PROJECT_DIRECTORY, "LICENSE")
    placeholder_path = os.path.join(PROJECT_DIRECTORY, "LICENSE_PLACEHOLDER.txt")

    # First remove the placeholder LICENSE file we created
    remove_file("LICENSE")

    if os.path.exists(source_path):
        try:
            shutil.copyfile(source_path, dest_path)
            print(f"Copied {license_name} license to LICENSE.")
        except Exception as e:
            print(f"Error copying license file {license_name}: {e}", file=sys.stderr)
            # Keep the placeholder if copy fails?
            sys.exit(1)
    else:
        print(
            f"Warning: License template file {source_path} not found.", file=sys.stderr
        )
        # Leave no LICENSE file in this case


def remove_licenses_dir():
    licenses_dir = os.path.join(PROJECT_DIRECTORY, "licenses")
    if os.path.isdir(licenses_dir):
        try:
            shutil.rmtree(licenses_dir)
            print("Removed temporary licenses/ directory.")
        except OSError as e:
            print(
                f"Error removing licenses directory {licenses_dir}: {e}",
                file=sys.stderr,
            )
            # Non-fatal error, proceed


def modify_cli_py():
    """Modifies cli.py to set placeholder flags and potentially other values."""
    cli_path = os.path.join(PROJECT_DIRECTORY, "src", PROJECT_SLUG, "cli.py")

    if not os.path.exists(cli_path):
        print(
            f"Warning: cli.py not found at {cli_path}. Skipping modification.",
            file=sys.stderr,
        )
        return

    print(f"Modifying {cli_path} based on Cookiecutter settings...")
    try:
        with open(cli_path, "r") as f:
            content = f.read()

        # Replace placeholder flags
        content = re.sub(
            r"^_MCP_ENABLED\s*=\s*False", f"_MCP_ENABLED = {USE_MCP}", content
        )
        content = re.sub(
            r"^_LOGFIRE_ENABLED\s*=\s*False",
            f"_LOGFIRE_ENABLED = {USE_LOGFIRE}",
            content,
        )

        # Replace placeholder static values (example)
        content = re.sub(
            r"^_PROJECT_SLUG\s*=\s*\"pydanticai_api_template\"",
            f'_PROJECT_SLUG = "{PROJECT_SLUG}"',
            content,
        )
        content = re.sub(
            r"^_PROJECT_NAME_DISPLAY\s*=\s*\"PydanticAI API Template\"",
            f'_PROJECT_NAME_DISPLAY = "{PROJECT_NAME_DISPLAY}"',
            content,
        )
        content = re.sub(
            r"^_DEFAULT_PORT\s*=\s*8000", f"_DEFAULT_PORT = {DEFAULT_PORT}", content
        )
        content = re.sub(r"^_MCP_PORT\s*=\s*3001", f"_MCP_PORT = {MCP_PORT}", content)

        with open(cli_path, "w") as f:
            f.write(content)
        print(f"Successfully updated flags and placeholders in {cli_path}")

    except Exception as e:
        print(f"Error modifying {cli_path}: {e}", file=sys.stderr)
        # Continue script, modification is best-effort


def initialize_git():
    """Initializes git, adds all files, and makes the initial commit."""
    try:
        print("Initializing Git repository...")
        subprocess.check_call(["git", "init"])
        print("Adding files to Git...")
        subprocess.check_call(["git", "add", "."])
        print("Creating initial commit...")
        # Use a non-interactive commit message
        commit_msg = f"Initial commit from PydanticAI Cookiecutter template\n\nProject: {{ cookiecutter.project_name }}\nSlug: {{ cookiecutter.project_slug }}\nLicense: {LICENSE_CHOICE}"
        subprocess.check_call(["git", "commit", "-m", commit_msg])
        print("Git repository initialized successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git initialization: {e}", file=sys.stderr)
        print("Please check your Git installation and run git commands manually.")
        # Continue script execution, as Git init failure isn't critical for project files
    except FileNotFoundError:
        print(
            "Error: 'git' command not found. Skipping Git initialization.",
            file=sys.stderr,
        )
        print("Please install Git or initialize the repository manually.")


def print_next_steps():
    """Prints helpful next steps to the console."""
    message = f"""
    --------------------------------------------------
    Project {{ cookiecutter.project_name }} generated successfully!
    --------------------------------------------------

    Next steps:

    1. Navigate to your project directory:
       cd {REPO_NAME}/

    2. Create your environment file (and add secrets):
       cp .env.example .env

    3. Open the project in VS Code or Cursor.

    4. When prompted, click "Reopen in Container".
       (This may take a few minutes on the first run to build the container.)

    5. Inside the container's terminal, start the application:
       start
       (Alternatively: make setup && make run)

    6. Access the API documentation at:
       http://localhost:{DEFAULT_PORT}/docs
"""

    if USE_MCP:
        message += f"""
    7. Access the MCP server (if enabled) at:
       http://localhost:{MCP_PORT}
"""

    message += """
    Happy coding!
    """
    print(message)


# --- Main Execution ---

print("Running post-generation hook...")

# Handle License
if LICENSE_CHOICE == "None":
    print("No license selected, removing LICENSE file.")
    remove_file("LICENSE")
elif LICENSE_CHOICE in ["MIT", "Apache-2.0"]:
    # We need to adjust the copy logic if licenses/ isn't inside the final dir
    # For now, assume it IS copied initially by cookiecutter
    # copy_license_file(LICENSE_CHOICE)
    print(
        f"License '{LICENSE_CHOICE}' selected. Placeholder LICENSE file should be updated by Cookiecutter include/copy."
    )
    # If cookiecutter didn't handle copying via includes/copy_without_render, we'd need to copy manually here.
    # For simplicity with includes, we assume cookiecutter handled it, so just remove the placeholder if needed.
    # Check if the placeholder exists and remove it if the real one should be there.
    placeholder_content = "Placeholder for License file."
    license_path = os.path.join(PROJECT_DIRECTORY, "LICENSE")
    try:
        with open(license_path, "r") as f:
            first_line = f.readline()
            if placeholder_content in first_line:
                print(
                    f"LICENSE file seems to be the placeholder, but license '{LICENSE_CHOICE}' was chosen. This indicates an issue with template setup (expected include/copy). Leaving placeholder."
                )
            else:
                print(
                    f"LICENSE file appears to contain the '{LICENSE_CHOICE}' license."
                )
    except FileNotFoundError:
        print(
            f"LICENSE file not found, but license '{LICENSE_CHOICE}' was chosen. Template setup might need adjustment."
        )
    except Exception as e:
        print(f"Error checking LICENSE file content: {e}")
else:
    print(f"Warning: Unknown license choice '{LICENSE_CHOICE}'. Removing LICENSE file.")
    remove_file("LICENSE")

# Remove the licenses directory (if it was copied into the project)
# remove_licenses_dir() # Only if licenses/ was part of {{cookiecutter.project_slug}}

# Modify cli.py BEFORE git commit
modify_cli_py()

# Initialize Git
initialize_git()

# Print Next Steps
print_next_steps()

print("Post-generation hook finished.")
