# src/pydanticai_api_template/agents/rag/embedding_client.py

import os
from typing import Any

from openai import AsyncOpenAI

from .models import EmbeddingClient


class OpenAIEmbeddingClient(EmbeddingClient):
    """
    EmbeddingClient implementation using OpenAI API.
    """

    def __init__(self, api_key: str | None = None):
        self.client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    async def create(self, model: str, input: str) -> dict[str, Any]:
        """
        Asynchronously request embeddings from OpenAI.
        """
        response = await self.client.embeddings.create(
            model=model,
            input=input,
        )
        # Convert to primitive dict
        return response.model_dump()
