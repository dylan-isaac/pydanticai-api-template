"""
Tests for the MCP server functionality.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from pydanticai_api_template.mcp_server import ChatResponse, chat, create_app


@pytest.fixture
def app() -> FastAPI:
    """Create a FastAPI app for testing."""
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a test client for the app."""
    return TestClient(app)


def test_create_app() -> None:
    """Test that the application is created successfully."""
    app = create_app()
    assert app.title == "PydanticAI MCP Server"
    assert app.description == "MCP server for PydanticAI API Template"
    # Check that the SSE endpoint is mounted
    assert any("/sse" in str(route) for route in app.routes)


@pytest.mark.asyncio
@patch("pydanticai_api_template.mcp_server.ai_agent")
async def test_chat_success(mock_agent: MagicMock) -> None:
    """Test the chat tool with a successful response."""
    # Setup mock
    mock_result = MagicMock()
    mock_data = MagicMock(spec=ChatResponse)
    mock_data.reply = "This is a test response"
    mock_result.data = mock_data
    mock_agent.run = AsyncMock(return_value=mock_result)

    # Call the chat tool
    response = await chat("Hello, how are you?")

    # Assertions
    mock_agent.run.assert_called_once_with("Hello, how are you?")
    assert response == "This is a test response"


@pytest.mark.asyncio
@patch("pydanticai_api_template.mcp_server.ai_agent", None)
async def test_chat_no_agent() -> None:
    """Test the chat tool when no agent is available."""
    response = await chat("Hello")
    assert "AI service is not available" in response


@pytest.mark.asyncio
@patch("pydanticai_api_template.mcp_server.ai_agent")
async def test_chat_exception(mock_agent: MagicMock) -> None:
    """Test the chat tool when an exception occurs."""
    # Setup mock to raise an exception
    mock_agent.run = AsyncMock(side_effect=Exception("Test exception"))

    # Call the chat tool
    response = await chat("Hello")

    # Assertions
    assert "An error occurred" in response
    assert "Test exception" in response
