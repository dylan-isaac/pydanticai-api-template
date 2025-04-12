# Testing Guide

This document describes how to test the PydanticAI API Template, including the MCP server, model validation, and type checking.

## Running Tests

### Automated Tests

To run the automated tests:

```bash
# Run all tests
pydanticai-api-template test

# Run specific tests with pytest directly
python -m pytest tests/test_mcp_server.py -v
```

### Test Coverage

To generate test coverage reports:

```bash
python -m pytest --cov=pydanticai_api_template tests/
```

## Testing the MCP Server

### Automated Tests

The MCP server has unit tests in `tests/test_mcp_server.py` that test:

1. Server creation
2. Chat tool functionality
3. Error handling

### Manual Testing

#### Prerequisites

1. Install dependencies:
   ```bash
   pip install -e ".[test]"
   ```

2. Set up environment variables:
   ```bash
   # Create a .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

#### Running the MCP Server

Start the MCP server:

```bash
pydanticai-api-template run-mcp
```

The server will start on http://localhost:3001 by default.

#### Using the Example Client

Run the example MCP client to test connection to the server:

```bash
python examples/mcp_client_example.py
```

This will send test messages to the MCP server and display the responses.

#### Testing with curl

You can also test the SSE connection using curl:

```bash
curl -N http://localhost:3001/sse
```

This should establish a connection to the SSE endpoint.

## Testing Pydantic Models

### Writing Model Tests

Testing Pydantic models is crucial for ensuring your validation logic works correctly. Here's how to write effective tests:

```python
import pytest
from pydantic import ValidationError

from pydanticai_api_template.api.models import ChatMessage

def test_chat_message_valid():
    # Valid case
    msg = ChatMessage(message="Hello, how are you?")
    assert msg.message == "Hello, how are you?"

def test_chat_message_empty():
    # Empty message should fail validation
    with pytest.raises(ValidationError) as exc_info:
        ChatMessage(message="")

    # Check specific validation error details
    errors = exc_info.value.errors()
    assert any("empty" in str(err["msg"]) for err in errors)

def test_chat_message_whitespace():
    # Whitespace-only message should fail validation
    with pytest.raises(ValidationError) as exc_info:
        ChatMessage(message="   ")

    # Check specific validation error details
    errors = exc_info.value.errors()
    assert any("empty" in str(err["msg"]) for err in errors)
```

### Testing Complex Validation Rules

For models with interdependent validation rules, test each case:

```python
from pydanticai_api_template.api.models import UserSignup

def test_password_match():
    # Passwords match
    user = UserSignup(
        username="testuser",
        password="secureP@ss123",
        password_confirm="secureP@ss123"
    )
    assert user.password == user.password_confirm

def test_password_mismatch():
    # Passwords don't match
    with pytest.raises(ValidationError) as exc_info:
        UserSignup(
            username="testuser",
            password="secureP@ss123",
            password_confirm="differentP@ss"
        )

    errors = exc_info.value.errors()
    assert any("match" in str(err["msg"]) for err in errors)
```

### Testing JSON Serialization

Test that your models serialize to and from JSON correctly:

```python
import json
from pydanticai_api_template.api.models import ChatResponse

def test_chat_response_serialization():
    # Create model instance
    response = ChatResponse(reply="This is a test response")

    # Serialize to JSON
    json_str = response.model_dump_json()

    # Parse JSON back to Python
    data = json.loads(json_str)

    # Check data structure
    assert data == {"reply": "This is a test response"}

    # Recreate model from JSON
    new_response = ChatResponse.model_validate(data)
    assert new_response.reply == response.reply
```

## Mocking AI Services

Testing AI-powered applications can be challenging due to the need for API keys and the non-deterministic nature of AI responses. Here are effective mocking strategies:

### Mocking PydanticAI Agent

```python
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from pydanticai_api_template.api.models import ChatResponse
from pydanticai_api_template.api.endpoints import chat_with_agent

@pytest.mark.asyncio
@patch("pydanticai_api_template.api.endpoints.ai_agent")
async def test_chat_endpoint(mock_agent):
    # Create a mock result
    mock_result = MagicMock()
    mock_result.data = ChatResponse(reply="This is a mocked AI response")

    # Set up the mock to return our prepared result
    mock_agent.run = AsyncMock(return_value=mock_result)

    # Test the endpoint with a chat message
    from pydanticai_api_template.api.models import ChatMessage
    response = await chat_with_agent(ChatMessage(message="Hello AI"))

    # Verify the response
    assert response.reply == "This is a mocked AI response"

    # Verify the agent was called correctly
    mock_agent.run.assert_called_once_with("Hello AI")
```

### Testing Error Scenarios

```python
@pytest.mark.asyncio
@patch("pydanticai_api_template.api.endpoints.ai_agent", None)
async def test_chat_endpoint_no_agent():
    # Test when AI agent is not available
    from pydanticai_api_template.api.models import ChatMessage
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        await chat_with_agent(ChatMessage(message="Hello AI"))

    # Verify status code and error message
    assert exc_info.value.status_code == 503
    assert "AI service is not available" in str(exc_info.value.detail)
```

## Type Checking Tests

Static type checking is an important part of the testing strategy. The project uses mypy for this purpose.

### Running Type Checks

```bash
# Check all files
mypy src tests

# Check specific modules
mypy src/pydanticai_api_template/api/models.py
```

### Common Type Issues and Solutions

1. **Untyped decorators**: Add specific module overrides in pyproject.toml:
   ```toml
   [[tool.mypy.overrides]]
   module = "pydanticai_api_template.api.models"
   disallow_untyped_decorators = false
   ```

2. **Missing return types**: Always add return types to functions:
   ```python
   def process_data(data: dict) -> dict:  # Add return type
       # Function implementation
       return processed_data
   ```

3. **Optional values**: Use `Optional` for values that might be None:
   ```python
   from typing import Optional

   def find_user(user_id: str) -> Optional[User]:
       # Implementation
       if not found:
           return None
       return user
   ```

## Testing Checklist

- [ ] Unit tests for all models
- [ ] Validation tests for model constraints
- [ ] API endpoint tests with mocked dependencies
- [ ] MCP server functionality tests
- [ ] Type consistency checks with mypy
- [ ] Error handling and edge case tests
- [ ] Accessibility compliance tests
- [ ] Test for race conditions in async code
- [ ] Verify that the MCP server starts without errors
- [ ] Verify that the chat tool responds to messages
- [ ] Verify error handling when the OpenAI API key is missing
- [ ] Verify error handling when the LLM service returns an error
- [ ] Verify that multiple clients can connect to the server

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Make sure you've installed the package with dev dependencies: `pip install -e ".[dev,test]"`

2. **OpenAI API Key issues**:
   - Check that your OpenAI API key is correctly set in the .env file
   - Check that the .env file is in the correct location (project root)

3. **Port already in use**:
   - If port 3001 is already in use, change the port: `pydanticai-api-template run-mcp --port 3002`

4. **Type checking errors**:
   - Check the function signatures and return types
   - Verify imported types are correct
   - Use `# type: ignore` sparingly and with specific error codes

### MCP Server Logs

To see detailed logs from the MCP server:

```bash
pydanticai-api-template run-mcp --log-level debug
```

This will show more detailed information about the server operation and any errors.

## Continuous Integration

If you're setting up CI/CD pipelines, add the following steps to test the MCP server:

```yaml
# Example GitHub Actions step
- name: Test MCP Server
  run: |
    python -m pytest tests/test_mcp_server.py -v
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

# Add type checking
- name: Run Type Checker
  run: |
    pip install mypy
    mypy src tests
```
