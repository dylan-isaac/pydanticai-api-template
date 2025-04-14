"""
Tests for the MCP server functionality.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from pydanticai_api_template.mcp_server import chat, create_app


@pytest.fixture
def app() -> FastAPI:
    """Create a FastAPI app for testing."""
    return create_app()


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    """Create an HTTP client for testing the FastAPI app."""
    async with AsyncClient(base_url="http://test") as client:
        return client


def test_create_app() -> None:
    """Test that the application is created successfully."""
    app = create_app()
    assert app.title == "PydanticAI MCP Server"
    assert app.description == "MCP server for PydanticAI API Template"
    # Check that the SSE endpoint is mounted
    assert any("/sse" in str(route) for route in app.routes)


@pytest.mark.asyncio
@patch("pydanticai_api_template.mcp_server.ai_agent")
async def test_chat_success(
    mock_ai_agent: MagicMock,
    client: AsyncClient,
) -> None:
    """Test successful chat interaction."""
    # Create a mock object with a 'data' attribute
    mock_result = MagicMock()
    mock_result.data = "Mocked response"

    # Make the mock's run method awaitable and return the mock_result
    mock_ai_agent.run = AsyncMock(return_value=mock_result)

    # Call the chat tool
    response = await chat("Hello, how are you?")

    # Assertions
    mock_ai_agent.run.assert_called_once_with("Hello, how are you?")
    assert response == "Mocked response"


@pytest.mark.asyncio
@patch("pydanticai_api_template.mcp_server.ai_agent", None)
async def test_chat_no_agent(
    client: AsyncClient,
) -> None:
    """Test chat interaction when agent is not found."""
    response = await chat("Hello")
    assert "AI service is not available" in response


@pytest.mark.asyncio
@patch("pydanticai_api_template.mcp_server.ai_agent")
async def test_chat_exception(
    mock_ai_agent: MagicMock,
    client: AsyncClient,
) -> None:
    """Test chat interaction when agent run raises an exception."""
    mock_ai_agent.run = AsyncMock(side_effect=Exception("Test exception"))

    # Call the chat tool
    response = await chat("Hello")

    # Assertions
    assert "An error occurred" in response
    assert "Test exception" in response
