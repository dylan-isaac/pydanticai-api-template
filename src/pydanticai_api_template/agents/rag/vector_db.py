# src/pydanticai_api_template/agents/rag/vector_db.py

import asyncio
import os
from pathlib import Path

import pinecone

from .models import Chunk, VectorDBClient


class PineconeVectorDBClient(VectorDBClient):
    """
    Concrete VectorDBClient using Pinecone vector database.
    """

    def __init__(self, index_name: str, namespace: str = "docs"):
        api_key = os.getenv("PINECONE_API_KEY")
        environment = os.getenv("PINECONE_ENVIRONMENT")
        pinecone.init(api_key=api_key, environment=environment)
        # Ensure the index exists
        if index_name not in pinecone.list_indexes():
            raise ValueError(f"Pinecone index '{index_name}' does not exist.")
        self.index = pinecone.Index(index_name)
        self.namespace = namespace

    async def search_embeddings(self, vector: list[float], top_k: int, filter: dict) -> list[Chunk]:
        """
        Search for documents by embedding vector and metadata filter.
        """
        response = await asyncio.to_thread(
            self.index.query,
            namespace=self.namespace,
            top_k=top_k,
            vector=vector,
            filter=filter,
            include_metadata=True,
        )
        return [
            Chunk(
                title=match.metadata.get("title", match.id),
                content=match.metadata.get("content", ""),
            )
            for match in response.matches
        ]

    async def list_urls(self, source: str) -> list[str]:
        """
        List documentation pages by scanning the local docs/ directory.
        """
        project_root = Path(__file__).resolve().parents[3]
        docs_dir = project_root / "docs"
        return [str(p.relative_to(project_root)) for p in docs_dir.glob("*.md")]

    async def get_chunks(self, url: str, source: str) -> list[Chunk]:
        """
        Retrieve all chunks for a given URL by filtering metadata.
        """
        # Filter by metadata field 'url'
        return await self.search_embeddings([], top_k=100, filter={"url": url})
