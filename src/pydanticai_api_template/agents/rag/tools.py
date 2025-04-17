# src/pydanticai_api_template/agents/rag/tools.py

import os

from pydantic_ai import Agent, RunContext

from .models import AgentDeps
from .prompts import SYSTEM

# Initialize the PydanticAI agent for RAG
agent = Agent(
    model=os.getenv("PRIMARY_MODEL", "openai:gpt-4o-mini"),
    system_prompt=SYSTEM,
    deps_type=AgentDeps,
    retries=2,
)


@agent.tool
async def retrieve_relevant_documentation(ctx: RunContext[AgentDeps], query: str) -> str:
    """
    Retrieve the top‑K documentation chunks matching the query.
    Returns a formatted string of the most relevant snippets.
    """
    # Generate embedding for the query
    emb_resp = await ctx.deps.embedding_client.create(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        input=query,
    )
    q_emb = emb_resp["data"][0]["embedding"]
    # Search vector DB
    chunks = await ctx.deps.db_client.search_embeddings(
        vector=q_emb,
        top_k=5,
        filter={"source": "docs"},
    )
    if not chunks:
        return "No relevant documentation found."
    # Format retrieved chunks
    return "\n\n---\n\n".join(f"# {c.title}\n{c.content}" for c in chunks)


@agent.tool
async def list_documentation_pages(ctx: RunContext[AgentDeps]) -> list[str]:
    """
    List all documentation page URLs available in the knowledge base.
    """
    return await ctx.deps.db_client.list_urls(source="docs")


@agent.tool
async def get_page_content(ctx: RunContext[AgentDeps], url: str) -> str:
    """
    Retrieve and concatenate all chunks for a given documentation page URL.
    """
    chunks = await ctx.deps.db_client.get_chunks(url=url, source="docs")
    if not chunks:
        return f"No content found for URL: {url}"
    return "\n\n".join(chunk.content for chunk in chunks)
