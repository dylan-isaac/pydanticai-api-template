from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Request model for chat messages."""

    message: str = Field(..., description="The user's message to the AI agent.")


class ChatResponse(BaseModel):
    """Response model for the AI agent's reply."""

    reply: str = Field(..., description="The AI agent's response.")
