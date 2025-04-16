# AI Agent Context: Cookiecutter Template Refactor

**Date:** 2024-07-17

**Goal:** Convert the `pydanticai-api-template` project into a dynamic Cookiecutter template based on the PRD and exploration findings in `Untitled-1`.

**Overall Plan:**

1.  **Setup:** Create `cookiecutter.json` for variables and `hooks/` directory for pre/post-generation scripts. Set up `licenses/` directory.
2.  **Restructure:** Move all project files into the main template directory `{{ cookiecutter.project_slug }}/`. Rename the core source directory `src/pydanticai_api_template` to `src/{{ cookiecutter.project_slug }}`.
3.  **Template Config Files:** Apply Jinja templating (`{{ var }}` and `{% if %}`) to key configuration files (`pyproject.toml`, `docker-compose.yml`, Dockerfiles, `.env.example`, etc.), handling conditional dependencies and settings.
4.  **Template Documentation:** Apply Jinja templating to `README.md` and files within `docs/`, updating names, ports, and adding conditional sections for optional features.
5.  **Template Source Code:** Update import paths and any hardcoded references to the old project name/slug within `src/{{ cookiecutter.project_slug }}/`. Use placeholder flags or post-gen hooks for complex conditional logic within Python code if Jinja causes issues.
6.  **Template Helper Scripts:** Update `Makefile`, `.vscode/tasks.json`, etc., to use templated names/paths and handle conditional tasks where feasible.
7.  **Refine Hooks:** Ensure `post_gen_project.py` handles necessary post-processing, like license file placement and modifying Python files with placeholder flags.
8.  **Testing:** Generate projects using the template with various configurations (`use_mcp_server`, `use_logfire`, different licenses) and test their validity (install, run, basic functionality).

**Progress So Far:**

*   ✅ Created `cookiecutter.json` with variables.
*   ✅ Created `hooks/pre_gen_project.py` for validation.
*   ✅ Created `licenses/` directory and license files (MIT, Apache-2.0).
*   ✅ Created `hooks/post_gen_project.py` with Git init, license handling placeholders, next steps, and logic to modify `cli.py` placeholders.
*   ✅ Restructured project files into `{{ cookiecutter.project_slug }}/`.
*   ✅ Renamed source directory to `src/{{ cookiecutter.project_slug }}/`.
*   ✅ Templated `{{ cookiecutter.project_slug }}/LICENSE` using Jinja includes.
*   ⚠️ Attempted templating `{{ cookiecutter.project_slug }}/pyproject.toml` (Jinja syntax caused linter errors; needs revisit/alternative approach). Current version contains templated values but might fail linters *before* generation.
*   ✅ Templated `{{ cookiecutter.project_slug }}/README.md`.
*   ✅ Templated `{{ cookiecutter.project_slug }}/Makefile`.
*   ✅ Templated `{{ cookiecutter.project_slug }}/.devcontainer/devcontainer.json` (used static ports workaround for Jinja/JSON linting issues).
*   ✅ Templated `{{ cookiecutter.project_slug }}/.vscode/tasks.json` (used static tasks workaround for Jinja/JSON linting issues).
*   ✅ Templated `{{ cookiecutter.project_slug }}/.env.example` (with conditional block for Logfire).
*   ✅ Templated `{{ cookiecutter.project_slug }}/src/{{ cookiecutter.project_slug }}/__init__.py`.
*   ✅ Templated `{{ cookiecutter.project_slug }}/src/{{ cookiecutter.project_slug }}/cli.py` (using placeholder flag strategy to avoid Jinja/Python syntax conflicts).
*   ✅ Templated `{{ cookiecutter.project_slug }}/docker-compose.yml` (used quoted keys workaround for Jinja/YAML linting issues).
*   ✅ Templated `{{ cookiecutter.project_slug }}/Dockerfile` (used static ports/env workaround for Jinja/Dockerfile linting issues).
*   ✅ Templated `{{ cookiecutter.project_slug }}/Dockerfile.dev` (used static ports workaround, templated aliases).
*   ⏳ Reading `{{ cookiecutter.project_slug }}/.pre-commit-config.yaml` for templating.

**Remaining Tasks:**

*   **Finish `.pre-commit-config.yaml`:** Template mypy entry point path (`src/{{ cookiecutter.project_slug }}`) and conditional dependencies.
*   **Template `docs/`:** Review and template all files in `docs/` (replace project names, slugs, ports; add conditional blocks for MCP/Logfire sections).
*   **Conditional `docs/OBSERVABILITY.md`:** Ensure this file is only included if `use_logfire == 'y'`. This might require a `post_gen_project.py` hook action to remove the file if the condition is false, as conditionally *including* files is sometimes tricky.
*   **Template Source Code (`src/`):**
    *   Review/template `api/`, `models/`, `utils/`, `types/`, `config.py` (if created), etc.
    *   Replace any remaining `pydanticai_api_template` imports with `{{ cookiecutter.project_slug }}`.
    *   Ensure conditional code related to MCP/Logfire is correctly implemented (likely using the placeholder flag approach from `cli.py` if needed).
    *   Conditionally include/exclude `src/{{ cookiecutter.project_slug }}/mcp/` or `mcp_server.py` (Best handled by removing the directory/file in the `post_gen_project.py` hook if `use_mcp_server == 'n'`).
*   **Template `tests/`:** Update imports and any fixtures/tests using hardcoded paths or names.
*   **Template `promptfoo/`:** Review `promptfoo/config.yaml` for any necessary templating.
*   **Template `.github/`:** Review workflow files for hardcoded names or paths.
*   **Template `.cursor/`:** Review rules/config for necessary templating.
*   **Revisit `pyproject.toml`:** Determine the best way to handle Jinja templating for conditional dependencies and overrides while minimizing pre-generation linting errors. Consider if the current state is acceptable or if parts need to be modified post-generation by the hook.
*   **Testing:** Perform thorough end-to-end testing by generating projects with different Cookiecutter options.
*   **Cleanup:** Ensure no stray files from the original project remain outside the main `{{ cookiecutter.project_slug }}/` directory.

**Challenges & Tips:**

*   **Challenge:** Linters struggle with Jinja syntax embedded within JSON, YAML, Dockerfiles, and even Python before Cookiecutter renders the template. This causes false positive errors during templating.
*   **Tip/Workaround (Config/Docker):** For complex conditional logic or templated keys in JSON/YAML/Dockerfiles, prefer static definitions in the template file with comments indicating their purpose/conditionality. Simpler value replacements (`{{ cookiecutter.variable }}`) are usually okay, but complex structures (`{% if %}`) often cause issues. If essential, use the `post_gen_project.py` hook for targeted modifications, but this adds complexity.
*   **Tip/Workaround (Python):** Avoid complex Jinja logic directly within Python files (`.py`). For conditional imports or logic based on Cookiecutter choices, use placeholder flags (e.g., `_FEATURE_ENABLED = False`) in the template's Python code. Then, use the `post_gen_project.py` hook to replace these placeholders with `True` or `False` based on the actual Cookiecutter variables (`{{ cookiecutter.use_feature }}`).
*   **Tip (Testing):** Generate the template locally (`cookiecutter . --no-input` using defaults, or provide inputs) frequently during development to catch rendering errors or structural issues early. Test with different combinations of boolean options (`y`/`n`).
*   **Wisdom:** Refactoring requires patience. Search globally for the old project name/slug (`pydanticai-api-template`) periodically to catch missed references. Hooks are powerful tools for validation and post-processing but use them judiciously. Prefer standard Cookiecutter templating where possible.

This context should help resume the refactoring process later. Good luck!
