import logging
import os
import sys  # Import sys to configure logging output stream
from typing import Dict, Optional

# Load environment variables from .env file BEFORE other imports
# This ensures they are available when other modules might need them
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from pydantic_ai import Agent

# Import models from the new location
from .models import ChatMessage, ChatResponse, StoryIdea

# --- Logging Configuration ---
# Consistent logging setup from axe-ai
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),  # Allow configuring level via env var
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - "
    "%(message)s",
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
    version="0.1.0",  # Consider reading from __init__.py in the future
)

# --- CORS Middleware ---
# Allow all origins for development, be more specific in production
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
logger.info(f"Allowing CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Read from env var or default to all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PydanticAI Agent ---
try:
    # Use a more robust initialization
    ai_agent: Optional[Agent] = (
        Agent("openai:gpt-4o", result_type=ChatResponse) if OPENAI_API_KEY else None
    )

    # Initialize a specialized agent for story ideas
    story_agent: Optional[Agent] = (
        Agent("openai:gpt-4o", result_type=StoryIdea) if OPENAI_API_KEY else None
    )

    if ai_agent:
        logger.info("PydanticAI Agent initialized with openai:gpt-4o")
    else:
        logger.warning(
            "PydanticAI Agent not initialized due to missing OPENAI_API_KEY."
        )
except ImportError as e:
    logger.error(f"Failed to import PydanticAI dependencies (likely openai): {e}")
    logger.error("Ensure 'pydantic-ai[openai]' is installed correctly.")
    ai_agent = None  # Ensure agent is None if import fails
except Exception:
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
    logger.info(
        f"Received chat request: '{chat_message.message[:50]}...'"
    )  # Log truncated message

    if not ai_agent:
        logger.error(
            "Chat request failed: PydanticAI Agent not initialized or "
            "OpenAI key missing."
        )
        raise HTTPException(
            status_code=503,  # Service Unavailable
            detail="AI service is not available. Please check server configuration.",
        )

    try:
        logger.debug(
            f"Running PydanticAI agent for message: {chat_message.message[:50]}..."
        )
        # Explicitly assert that ai_agent is not None to satisfy type checker
        assert ai_agent is not None

        # Use the initialized agent
        agent_run_result = await ai_agent.run(chat_message.message)

        # Get response data
        response_data = agent_run_result.data

        # Check if result is already a ChatResponse or needs conversion
        if isinstance(response_data, ChatResponse):
            chat_response = response_data
        else:
            # Convert string or dict response to ChatResponse
            reply = str(response_data)
            chat_response = ChatResponse(reply=reply)
        logger.info("Agent returned reply.")
        return chat_response
    except Exception as e:
        # Catch-all for any other exceptions that might occur
        logger.exception(f"Error in chat_with_agent: {e}")
        # We don't want to expose internal errors to clients
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while processing your request.",
        )


@app.post("/story", response_model=StoryIdea)
async def generate_story_idea(chat_message: ChatMessage) -> StoryIdea:
    """Endpoint to generate a story idea with title and premise."""
    logger.info(
        f"Received story idea request: '{chat_message.message[:50]}...'"
    )  # Log truncated message

    if not story_agent:
        logger.error(
            "Story idea request failed: PydanticAI Agent not initialized or "
            "OpenAI key missing."
        )
        raise HTTPException(
            status_code=503,  # Service Unavailable
            detail="AI service is not available. Please check server configuration.",
        )

    try:
        logger.debug(
            f"Running PydanticAI story agent for message: "
            f"{chat_message.message[:50]}..."
        )
        # Explicitly assert that story_agent is not None to satisfy type checker
        assert story_agent is not None

        # Enhance the prompt to get high-quality story ideas
        enhanced_prompt = (
            f"Generate a creative and original story idea based on this input: "
            f"{chat_message.message}"
        )

        # Use the initialized agent
        agent_run_result = await story_agent.run(enhanced_prompt)

        # Get response data
        response_data = agent_run_result.data

        # Check if result is already a StoryIdea or needs conversion
        if isinstance(response_data, StoryIdea):
            story_idea = response_data
        else:
            # This should not happen with proper configuration, but handle just in case
            raise ValueError("Agent did not return a StoryIdea object")

        logger.info(f"Agent returned story idea: {story_idea.title}")
        return story_idea
    except Exception as e:
        # Catch-all for any other exceptions that might occur
        logger.exception(f"Error in generate_story_idea: {e}")
        # We don't want to expose internal errors to clients
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while processing your request.",
        )
