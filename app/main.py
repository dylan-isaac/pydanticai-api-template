import logging
import os
import sys  # Import sys to configure logging output stream
from typing import Any, Dict

# Load environment variables from .env file BEFORE other imports
# This ensures they are available when other modules might need them
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# --- Logging Configuration ---
# Configure logging to output to stdout with a specific format and level
logging.basicConfig(
    level=logging.INFO,  # Set the default logging level (e.g., INFO, DEBUG)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],  # Explicitly direct logs to stdout
)
logger = logging.getLogger(__name__)  # Get a logger instance for this module

# --- Configuration ---
# Now, os.getenv will correctly pick up values from your .env file if set
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logger.warning(
        "OPENAI_API_KEY environment variable not set (or not found in .env). The /chat endpoint will not work."
    )
    # In a real app, you might want to handle this more gracefully
    # or prevent the app from starting. For now, we'll let it run but the endpoint will fail.


# --- Pydantic Models ---
class ChatMessage(BaseModel):
    """Request model for chat messages."""

    message: str = Field(..., description="The user's message to the AI agent.")


class ChatResponse(BaseModel):
    """Response model for the AI agent's reply."""

    reply: str = Field(..., description="The AI agent's response.")


# --- FastAPI App ---
app = FastAPI(
    title="PydanticAI API Template",
    description="FastAPI project with PydanticAI integration.",
    version="0.1.0",
)

# --- CORS Middleware ---
# Add this section BEFORE your routes/endpoints
origins = [
    "http://localhost",  # Allow your local machine
    "http://localhost:8000",  # Allow the default FastAPI port
    # Add any other origins if your frontend/docs are served differently
    # "*" # Use this cautiously for local dev if needed, but be specific for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# --- PydanticAI Agent ---
# Initialize the agent. We'll use OpenAI's gpt-4o model here.
# PydanticAI handles the interaction with the LLM based on the string identifier.
ai_agent = Agent("openai:gpt-4o", result_type=ChatResponse)


# --- API Endpoints ---
@app.get("/")
async def read_root() -> Dict[str, str]:
    """Basic root endpoint."""
    logger.info("Root endpoint '/' accessed.")
    return {"message": "Welcome to PydanticAI API Template with PydanticAI!"}


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(chat_message: ChatMessage) -> ChatResponse:
    """Endpoint to chat with the PydanticAI agent."""
    logger.info(f"Received chat request: {chat_message.message}")
    if not OPENAI_API_KEY:
        logger.error("Chat request failed: OpenAI API key not configured.")
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured on the server (or not found in .env).",
        )
    try:
        logger.debug("Running PydanticAI agent...")
        # Correctly handle the AgentRunResult
        agent_run_result = await ai_agent.run(chat_message.message)
        chat_response: ChatResponse = agent_run_result.data  # Extract the data
        logger.info(f"Agent returned reply: {chat_response.reply}")
        return chat_response
    except Exception as e:
        # Log the exception with stack trace
        logger.exception("An error occurred during agent run:")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request.",  # Avoid leaking exception details to client
        )
