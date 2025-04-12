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
from pydantic_ai import Agent

# Import models from the new location
from .models import ChatMessage, ChatResponse

# --- Logging Configuration ---
# Consistent logging setup from axe-ai
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(), # Allow configuring level via env var
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# --- Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logger.warning(
        "OPENAI_API_KEY environment variable not set (or not found in .env). "
        "The /chat endpoint will not work."
    )

# --- Pydantic Models ---
# Models moved to src/pydanticai_api_template/api/models.py


# --- FastAPI App ---
app = FastAPI(
    title="PydanticAI API Template",
    description="FastAPI project with PydanticAI integration.",
    version="0.1.0", # Consider reading from __init__.py in the future
)

# --- CORS Middleware ---
# Allow all origins for development, be more specific in production
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
logger.info(f"Allowing CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Read from env var or default to all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PydanticAI Agent ---
try:
    # Use a more robust initialization
    ai_agent = Agent("openai:gpt-4o", result_type=ChatResponse) if OPENAI_API_KEY else None
    if ai_agent:
        logger.info("PydanticAI Agent initialized with openai:gpt-4o")
    else:
        logger.warning("PydanticAI Agent not initialized due to missing OPENAI_API_KEY.")
except ImportError as e:
    logger.error(f"Failed to import PydanticAI dependencies (likely openai): {e}")
    logger.error("Ensure 'pydantic-ai[openai]' is installed correctly.")
    ai_agent = None # Ensure agent is None if import fails
except Exception as e:
    logger.exception("Unexpected error initializing PydanticAI Agent:")
    ai_agent = None

# --- API Endpoints ---
@app.get("/")
async def read_root() -> Dict[str, str]:
    """Basic root endpoint."""
    logger.info("Root endpoint '/' accessed.")
    return {"message": "Welcome to the PydanticAI API Template!"}


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(chat_message: ChatMessage) -> ChatResponse:
    """Endpoint to chat with the PydanticAI agent."""
    logger.info(f"Received chat request: '{chat_message.message[:50]}...'" ) # Log truncated message

    if not ai_agent:
        logger.error("Chat request failed: PydanticAI Agent not initialized or OpenAI key missing.")
        raise HTTPException(
            status_code=503, # Service Unavailable
            detail="AI service is not available. Please check server configuration."
        )

    try:
        logger.debug(f"Running PydanticAI agent for message: {chat_message.message[:50]}...")
        # Explicitly assert that ai_agent is not None to satisfy type checker
        assert ai_agent is not None
        # Use the initialized agent
        agent_run_result = await ai_agent.run(chat_message.message)

        # Add check for result type, although PydanticAI should handle this
        if not isinstance(agent_run_result.data, ChatResponse):
             logger.error(f"Agent returned unexpected data type: {type(agent_run_result.data)}")
             raise HTTPException(status_code=500, detail="AI agent returned unexpected data format.")

        chat_response: ChatResponse = agent_run_result.data
        # Simplified logging to try and clear linter state
        logger.info("Agent returned reply.")
        return chat_response
    except Exception as e:
        # Use a generic exception handler for all PydanticAI errors
        if "LLM" in str(e) or "Agent" in str(e):
            # This is likely an LLM or Agent error from PydanticAI
            logger.error(f"PydanticAI Error during agent run: {e}")
            raise HTTPException(
                status_code=502, # Bad Gateway (error communicating with upstream LLM)
                detail=f"Error communicating with the AI model: {e}",
            )
        else:
            logger.exception("An unexpected error occurred during agent run:") # Log full traceback
            raise HTTPException(
                status_code=500,
                detail="An internal server error occurred while processing your request.",
            )
