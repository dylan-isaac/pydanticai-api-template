import argparse
import logging
import os
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Initialize the OpenAI agent
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Define Pydantic models for MCP server
class ChatRequest(BaseModel):
    """Model for chat request to the MCP server."""

    message: str = Field(..., description="The user's message to the AI agent.")


class ChatResponse(BaseModel):
    """Model for chat response from the MCP server."""

    reply: str = Field(..., description="The AI agent's response.")


# Initialize AI agent
try:
    ai_agent: Optional[Agent] = (
        Agent("openai:gpt-4o", result_type=ChatResponse) if OPENAI_API_KEY else None
    )
    if ai_agent:
        logger.info("PydanticAI Agent initialized with openai:gpt-4o for MCP server")
    else:
        logger.warning(
            "PydanticAI Agent not initialized due to missing OPENAI_API_KEY."
        )
except Exception as e:
    logger.exception(f"Error initializing PydanticAI Agent: {e}")
    ai_agent = None

# Create FastMCP server
server = FastMCP("PydanticAI API MCP Server")


@server.tool()
async def chat(message: str) -> str:
    """Chat with the AI assistant

    Send a message to the AI assistant and receive a response.
    """
    if not ai_agent:
        return "AI service is not available. Please check server configuration."

    try:
        # Create a properly typed request object
        request = ChatRequest(message=message)

        # Ensure the agent is properly typed for mypy
        assert ai_agent is not None

        result: Any = await ai_agent.run(request.message)

        # Properly handle the response based on its type
        if hasattr(result.data, "reply"):
            return str(result.data.reply)
        return str(result.data)
    except Exception as e:
        logger.exception(f"Error in MCP chat tool: {e}")
        return f"An error occurred while processing your request: {str(e)}"


def create_app() -> FastAPI:
    """Create a FastAPI app with the MCP server"""
    app = FastAPI(
        title="PydanticAI MCP Server",
        description="MCP server for PydanticAI API Template",
        version="0.1.0",
    )

    # Create the SSE app from the server and mount it to our FastAPI app
    sse_app = server.sse_app()
    app.mount("/sse", sse_app)

    return app


def run_standalone() -> None:
    """Run the MCP server standalone in SSE mode"""
    import uvicorn

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the MCP server")
    parser.add_argument(
        "--host",
        default=os.getenv("MCP_HOST", "0.0.0.0"),
        help="Host to bind the server to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MCP_PORT", "3001")),
        help="Port to bind the server to",
    )
    args = parser.parse_args()

    host = args.host
    port = args.port

    logger.info(f"Starting MCP server on {host}:{port}")
    uvicorn.run(create_app(), host=host, port=port)


if __name__ == "__main__":
    run_standalone()
