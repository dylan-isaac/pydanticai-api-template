# Consolidated Cursor Rules (For Reference)

This file combines the content intended for individual `.mdc` files in `.cursor/rules/`. It can be used for reference or potentially adapted into a single `.cursorrules` file or revisited for the `.cursor/rules/*.mdc` structure later.

---

## Test-Driven Development (TDD) Guidance

*Intended Globs: `["src/pydanticai_api_template/**.py", "!tests/**"]`*

🧪 **Rule Triggered:** Code modified in `src/` but not `tests/`.

**Core Principle:** Write meaningful tests *before* implementation. Validate edge cases, failure modes, and expected behavior. Include prompt tests for LLM logic changes.

**Action Required:**
- If adding new functionality: Have you written tests for it first in the `tests/` directory?
- If modifying existing functionality: Have you updated corresponding tests in `tests/` to reflect the changes?
- If modifying AI interactions (e.g., prompts, PydanticAI models): Have you added or updated relevant prompt tests (e.g., using promptfoo)?

**Reference:** See @docs/TESTING.md for detailed strategies and examples.

**Decision Point:** If the testing strategy for this change is unclear, please clarify with the user.

---

## Type Safety Guidance

*Intended Globs: `["src/pydanticai_api_template/**.py"]`*

🔒 **Rule Triggered:** Code potentially introducing `Any` type hints.

**Core Principle:** Use strict type annotations and Pydantic models for runtime validation. Avoid `Any` unless absolutely necessary.

**Action Required:**
- Review any usage of `Any`. Can a more specific type be used?
  - Collections: `list[T]`, `dict[K, V]`, `tuple[T1, T2]`, `set[T]`
  - Optional values: `Optional[T]` or `T | None`
  - Multiple types: `Union[T1, T2]` or `T1 | T2`
  - Specific literals: `Literal['a', 'b']`
  - Dictionary shapes: `TypedDict`
  - Pydantic models for structured data.
- Ensure function signatures and Pydantic fields have explicit types.

**Reference:** See @docs/MODELS.md for Pydantic best practices and type examples.

**Decision Point:** Only use `Any` if unavoidable and explain the reasoning clearly.

---

## SOLID: Single Responsibility Principle (SRP)

*Intended Globs: `["src/pydanticai_api_template/**.py"]`*

🎯 **Rule Triggered:** Class or function modification/addition.

**Core Principle:** A class or function should have only one reason to change, meaning it should have only one job or responsibility.

**Action Required:**
- Examine the modified/added class or function. What is its primary responsibility?
- Does it handle multiple, distinct concerns (e.g., data fetching AND presentation AND business logic)?
- Could its responsibilities be logically separated into smaller, more focused units (classes, functions, modules)?
- Are the boundaries between responsibilities clear?

**Reference:** Discussed in @docs/ARCHITECTURE.md (SOLID Principles section).

**Decision Point:** If a component appears to violate SRP by handling multiple unrelated responsibilities, propose refactoring options to the user.

---

## Documentation-First Guidance

*Intended Globs: `["src/pydanticai_api_template/**.py"]`*

📝 **Rule Triggered:** Code modification/addition in `src/`.

**Core Principle:** Keep documentation (`README.md`, `docs/**/*.md`) as the source of truth. Ensure every feature/change is documented with purpose, examples, and assumptions.

**Action Required:**
- Based on the changes made, determine which documentation files need updates:
  - API endpoint changes (routes, request/response models)? -> Update @docs/API.md
  - Pydantic model changes (new models, fields, validation)? -> Update @docs/MODELS.md
  - Architectural changes (new components, interactions, libraries)? -> Update @docs/ARCHITECTURE.md
  - Core concepts or overall structure changes? -> Consider updates to @docs/OVERVIEW.md or @README.md
  - CLI command changes? -> Update @README.md
- Ensure documentation is clear, concise, and reflects the current state of the code.

**Reference:** See @docs/CURSOR_RULES.md for how rules integrate with docs.

**Decision Point:** Inform the user which documentation files likely need updating based on the code changes.

---

## Functional Style: MCP Tool Guidance

*Intended Globs: `["src/pydanticai_api_template/mcp_server.py"]`*

🔌 **Rule Triggered:** Modification of `mcp_server.py`, potentially adding/changing tools.

**Core Principle:** Write pure functions with no side effects when feasible. Prefer immutability, composition, and observability.

**Action Required when defining `@server.tool()` functions:**
- **Purity:** Aim for pure functions. If side effects (I/O, state changes) are necessary, isolate them and make them explicit.
- **Typing:** Use precise type hints for all parameters and return values. Leverage Pydantic models for complex inputs/outputs.
- **Docstrings:** Write clear docstrings explaining the tool's purpose, parameters, return value, and any potential side effects or exceptions.
- **Observability:** Wrap tool logic with `logfire.span()` or use `logfire.instrument()` for automatic tracing and logging.
- **Error Handling:** Handle potential exceptions gracefully and return informative error messages, possibly using custom exception types.

**Reference:** Functional style concepts in @docs/ARCHITECTURE.md, Observability in @docs/OBSERVABILITY.md.

**Decision Point:** If a tool design requires significant side effects or state management, discuss the trade-offs and design with the user.

---

## Pydantic Model Standards

*Intended Globs: `["src/pydanticai_api_template/types/**.py"]`*

📝 **Rule Triggered:** Addition or modification of files in `src/pydanticai_api_template/types/` (likely Pydantic models).

**Core Principle:** Use Pydantic models for robust data validation and clear schema definition, leveraging its features for documentation and examples.

**Action Required when defining `BaseModel` subclasses:**
1.  **Docstrings:** Add clear, descriptive class docstrings. Explain the model's purpose. These influence AI understanding.
2.  **Field Descriptions:** Use `Field(description="...")` for all fields to explain their meaning.
3.  **Field Examples:** Use `Field(examples=["example1", ...])` to provide concrete examples.
4.  **Validators:** Add `@validator` or `@field_validator` methods for complex constraints beyond basic types.
5.  **Model Config:** Use `model_config` (Pydantic V2) or `Config` (V1) to add `json_schema_extra={"examples": [...]}` for model-level examples.
6.  **Documentation:** Ensure the new/modified model is documented appropriately in @docs/MODELS.md.

**Reference:** Detailed guidelines and examples in @docs/MODELS.md.

**Decision Point:** Discuss with the user if creating novel or complex validation patterns not covered in the documentation.

---

## SOLID & Unix Philosophy: Component Modularity

*Intended Globs: `["src/pydanticai_api_template/**.py"]`*

🧩 **Rule Triggered:** Addition or modification of Python files in `src/`.

**Core Principle:** Design components (classes, functions, modules) that follow the Unix philosophy: "Do one thing and do it well." This aligns with SOLID principles like SRP and Interface Segregation.

**Action Required:**
- When creating or modifying components, consider:
  - **Focus:** Does this component have a single, well-defined purpose?
  - **Composability:** Is it designed to work together well with other components? Are interfaces clear and minimal?
  - **Simplicity:** Is the internal logic straightforward? Can complexity be reduced or abstracted?
- Avoid creating monolithic components that handle too many unrelated tasks.
- Prefer composing smaller, specialized components over building large, complex ones.

**Reference:** Concepts discussed in @docs/ARCHITECTURE.md.

**Decision Point:** If a component's design seems overly broad or complex, suggest potential ways to break it down into more modular parts.

---

## README Integrity: CLI Commands

*Intended Globs: `["README.md"]`*

🔑 **Rule Triggered:** Modification of `README.md`.

**Core Principle:** The root `README.md` must serve as the primary, immediately accessible reference for essential project setup and CLI commands.

**Action Required:**
- Verify that the "CLI Commands" section is present and accurate.
- Ensure all critical commands (`start`, `pat test`, `pat lint`, etc.) are listed, preferably in a table format.
- Do **not** remove or relocate these essential command references to other documentation files. They must remain in the root README for discoverability.

**Reference:** The structure defined in @README.md.

**Decision Point:** If considering removing or significantly altering the CLI commands section in the README, confirm this deviation with the user, as it goes against project standards.

---

## Package Management: Use `uv`

*Intended Globs: `["pyproject.toml", "requirements.txt", "**/*.py"]`*

📦 **Rule Triggered:** Modification of dependency files (`pyproject.toml`, `requirements.txt`) or Python files (potential imports).

**Core Principle:** This project uses `uv` for all Python package management tasks. Manual editing of `pyproject.toml` for dependencies is discouraged.

**Action Required:**
- **Adding Dependencies:** Use `uv add <package>` or `uv add --dev <package>`.
- **Installing Dependencies:** Use `uv pip install <package>` (infrequent) or `uv sync` (preferred way to install from `pyproject.toml` lock file if present, or requirements).
- **Removing Dependencies:** Use `uv remove <package>`.
- **Checking Dependencies:** Do not suggest adding packages already present in `pyproject.toml`.
- **Avoid `pip`:** Do not use `pip install` commands directly.
- **Python Version:** Remember the project requires Python 3.12+.

**Reference:** Standard project setup in @README.md and @docs/DEVELOPER.md.

**Decision Point:** If a specific version constraint or dependency configuration seems necessary that `uv` commands don't easily handle, discuss the approach with the user before manually editing `pyproject.toml`.
