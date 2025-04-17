# src/pydanticai_api_template/agents/rag/orchestrator.py

import os

from .embedding_client import OpenAIEmbeddingClient
from .models import AgentDeps
from .tools import agent
from .vector_db import PineconeVectorDBClient


def build_deps() -> AgentDeps:
    """
    Instantiate and return the AgentDeps with embedding and vector DB clients configured.
    """
    # Initialize embedding client
    embedding_client = OpenAIEmbeddingClient(api_key=os.getenv("OPENAI_API_KEY"))
    # Initialize vector DB client
    index_name = os.getenv("PINECONE_INDEX_NAME", "")
    namespace = os.getenv("PINECONE_NAMESPACE", "docs")
    db_client = PineconeVectorDBClient(
        index_name=index_name,
        namespace=namespace,
    )
    # Optional reasoner scope
    reasoner_output = os.getenv("REASONER_MODEL")
    return AgentDeps(
        llm_client=None,
        embedding_client=embedding_client,
        db_client=db_client,
        reasoner_output=reasoner_output,
    )


async def run_agentic_rag(query: str) -> str:
    """
    Run the RAG agent workflow for a given query and return the raw answer.
    """
    deps = build_deps()
    result = await agent.run(query, deps=deps)
    return result.data
