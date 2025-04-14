# Cursor Rules Guide

This document describes the Cursor rules set up for this project and how to get the most out of your AI-assisted development workflow.

## Introduction

[Cursor](https://cursor.sh/) is an AI-powered code editor that enhances developer productivity. This project includes custom rules to maximize the benefits of AI assistance while maintaining code quality and documentation standards.

## Getting Started with Cursor

1. **Install Cursor**: Download from [cursor.sh](https://cursor.sh/)
2. **Open the Project**: Open the project folder in Cursor
3. **Verify Rules**: The rules should be automatically loaded from `.cursor/rules.yml`

## Using @ Symbols for Context

Cursor supports @ symbols for referencing files, docs, and code in chats:

- `@file.py`: Reference a file
- `@docs/OVERVIEW.md`: Reference documentation
- `@src/pydanticai_api_template/api/models.py:10-20`: Reference specific code lines

### Keyboard Shortcuts

- Type `@` in chat to see suggestions
- Use arrow keys to navigate suggestions
- Hit `Enter` to select

## Rule Categories

### 1. Documentation-First Rules

These rules remind you to update documentation when you modify code. They help maintain the documentation and code in sync.

### 2. Type Safety Enforcement

These rules ensure strong typing is maintained throughout the codebase, which is essential for PydanticAI's functionality.

### 3. MCP Tool Validation

When working with Model Context Protocol (MCP), these rules ensure you follow best practices for tool development.

### 4. Pydantic Model Standards

These rules remind you of best practices when creating or modifying Pydantic models.

### 5. Test Coverage Guardian

These rules remind you to update tests when you modify code.

### 6. Accessibility Champion

These rules promote accessibility in user-facing components.

## Best Practices for AI Coding with Cursor

### Prompt Structure for PydanticAI

When asking Cursor to modify PydanticAI code, structure your prompts as:

1. **Location**: Specify where the change should happen
2. **Action**: Use clear action words (CREATE, UPDATE, ADD, etc.)
3. **Detail**: Provide specifics of what should change

Example:
```text
UPDATE src/pydanticai_api_template/api/models.py:
ADD field publication_date to StoryIdea model
Make it Optional[datetime] with ISO format validation
```

### Using the MCP Server

For MCP server development, include relevant context:

```text
@src/pydanticai_api_template/mcp_server.py

Add a new tool that provides text summarization
```

### Documentation References

Reference documentation for context:

```text
@docs/MODELS.md

Update the ProductRecommendation model based on these patterns
```

## Creating Custom Rules

To create additional Cursor rules:

1. Navigate to `.cursor/rules.yml`
2. Add new rules following the existing pattern
3. Restart Cursor to apply changes

## Troubleshooting

- If rules aren't activating, check that `.cursor/rules.yml` is properly formatted
- For reference issues, ensure paths are correct
- For large codebases, use `.cursorignore` to exclude irrelevant files

## Resources

- [Cursor Documentation](https://docs.cursor.com/)
- [Cursor's Model Context Protocol](https://docs.cursor.com/context/model-context-protocol)
- [Cursor Rules Reference](https://docs.cursor.com/context/rules-for-ai)
