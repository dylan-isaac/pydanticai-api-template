from typing import Any, List

import pytest
from pydantic_ai import RunContext
from pydantic_ai.types import Model, Usage
from pydanticai_api_template.agents.rag.models import AgentDeps, Chunk
from pydanticai_api_template.agents.rag.tools import (
    get_page_content,
    list_documentation_pages,
    retrieve_relevant_documentation,
)


class DummyEmbeddingClient:
    async def create(self, model: str, input: str) -> dict[str, Any]:
        return {"data": [{"embedding": [0.1, 0.2, 0.3]}]}


class DummyDBClientEmpty:
    async def search_embeddings(self, vector: List[float], top_k: int, filter: dict) -> list[Chunk]:
        return []

    async def list_urls(self, source: str) -> list[str]:
        return ["/docs/one.md", "/docs/two.md"]

    async def get_chunks(self, url: str, source: str) -> list[Chunk]:
        if url == "/docs/one.md":
            return []
        return [
            Chunk(title="Title1", content="Content1"),
            Chunk(title="Title2", content="Content2"),
        ]


@pytest.fixture
def ctx_empty() -> RunContext[AgentDeps]:
    deps = AgentDeps(
        llm_client=None,
        embedding_client=DummyEmbeddingClient(),
        db_client=DummyDBClientEmpty(),
        reasoner_output=None,
    )
    dummy_model = Model(provider="dummy", name="dummy_model")
    dummy_usage = Usage(prompt_tokens=0, completion_tokens=0)
    return RunContext(
        deps=deps,
        model=dummy_model,
        usage=dummy_usage,
        prompt="dummy_prompt",
    )


@pytest.mark.asyncio
async def test_retrieve_relevant_documentation_none_found(
    ctx_empty: RunContext[AgentDeps],
) -> None:
    result = await retrieve_relevant_documentation(ctx_empty, "query")
    assert result == "No relevant documentation found."


@pytest.mark.asyncio
async def test_retrieve_relevant_documentation_formats_snippets(
    monkeypatch: Any,
) -> None:
    class DummyDBClient:
        async def search_embeddings(self, vector: List[float], top_k: int, filter: dict) -> list[Chunk]:
            return [Chunk(title="A", content="cA"), Chunk(title="B", content="cB")]

    deps = AgentDeps(
        llm_client=None,
        embedding_client=DummyEmbeddingClient(),
        db_client=DummyDBClient(),
        reasoner_output=None,
    )
    dummy_model = Model(provider="dummy", name="dummy_model")
    dummy_usage = Usage(prompt_tokens=0, completion_tokens=0)
    ctx = RunContext(
        deps=deps,
        model=dummy_model,
        usage=dummy_usage,
        prompt="dummy_prompt",
    )
    formatted = await retrieve_relevant_documentation(ctx, "anything")
    assert "# A" in formatted
    assert "# B" in formatted
    assert "cA" in formatted and "cB" in formatted


@pytest.mark.asyncio
async def test_list_documentation_pages_lists_urls(
    ctx_empty: RunContext[AgentDeps],
) -> None:
    result = await list_documentation_pages(ctx_empty)
    assert isinstance(result, list)
    assert "/docs/one.md" in result
    assert "/docs/two.md" in result


@pytest.mark.asyncio
async def test_get_page_content_empty_and_nonempty(
    ctx_empty: RunContext[AgentDeps],
) -> None:
    empty = await get_page_content(ctx_empty, "/docs/one.md")
    assert "No content found" in empty

    nonempty = await get_page_content(ctx_empty, "/docs/other.md")
    assert "Content1" in nonempty and "Content2" in nonempty
