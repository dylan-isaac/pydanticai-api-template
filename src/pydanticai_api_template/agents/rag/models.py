from typing import Any, List, Protocol

from pydantic import BaseModel


class Chunk(BaseModel):
    title: str
    content: str


class EmbeddingClient(Protocol):
    async def create(self, model: str, input: str) -> dict: ...


class VectorDBClient(Protocol):
    async def search_embeddings(self, vector: List[float], top_k: int, filter: dict) -> list[Chunk]: ...

    async def list_urls(self, source: str) -> list[str]: ...

    async def get_chunks(self, url: str, source: str) -> list[Chunk]: ...


class AgentDeps(BaseModel):
    llm_client: Any  # e.g. OpenAIModel or local model client
    # Use Protocol types for injected dependencies.
    embedding_client: EmbeddingClient
    db_client: VectorDBClient
    reasoner_output: str | None = None  # optional reasoner scope text

    # Allow protocol types (EmbeddingClient, VectorDBClient) without Pydantic
    # trying to build validation schemas for them, as they are injected dependencies.
    model_config = {"arbitrary_types_allowed": True}
