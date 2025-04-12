from typing import Any, ClassVar

from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    """Request model for chat messages."""

    message: str = Field(
        ...,
        description="The user's message to the AI agent.",
        min_length=1,
        examples=["Tell me about Pydantic", "How can I use PydanticAI?"],
    )

    @classmethod
    @field_validator("message")
    def message_not_empty(cls, v: str) -> str:
        """Validate that the message is not empty."""
        if not v.strip():
            raise ValueError("Message cannot be empty or consist only of whitespace")
        return v


class ChatResponse(BaseModel):
    """Response model for the AI agent's reply."""

    reply: str = Field(
        ...,
        description="The AI agent's response.",
        examples=["Pydantic is a data validation and settings management library..."],
    )

    model_config: ClassVar[dict[str, Any]] = {
        "json_schema_extra": {
            "example": {
                "reply": "Pydantic is a Python library for data validation and settings management."
            }
        }
    }


class ErrorResponse(BaseModel):
    """Model for error responses."""

    detail: str = Field(..., description="Error message details")
    status_code: int = Field(..., description="HTTP status code")
