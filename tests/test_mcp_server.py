"""
Tests for the MCP server functionality.
"""

from unittest.mock import MagicMock, patch

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
    client: AsyncClient,
    mock_agent_run: MagicMock,
) -> None:
    """Test successful chat interaction."""
    mock_agent_run.return_value = "Mocked response"

    # Call the chat tool
    response = await chat("Hello, how are you?")

    # Assertions
    mock_agent_run.assert_called_once_with("Hello, how are you?")
    assert response == "Mocked response"


@pytest.mark.asyncio
@patch("pydanticai_api_template.mcp_server.ai_agent", None)
async def test_chat_no_agent(
    client: AsyncClient,
    mock_get_agent: MagicMock,
) -> None:
    """Test chat interaction when agent is not found."""
    mock_get_agent.return_value = None

    response = await chat("Hello")
    assert "AI service is not available" in response


@pytest.mark.asyncio
@patch("pydanticai_api_template.mcp_server.ai_agent")
async def test_chat_exception(
    client: AsyncClient,
    mock_agent_run: MagicMock,
) -> None:
    """Test chat interaction when agent run raises an exception."""
    mock_agent_run.side_effect = Exception("Test exception")

    # Call the chat tool
    response = await chat("Hello")

    # Assertions
    assert "An error occurred" in response
    assert "Test exception" in response
