from typing import Any, Dict, Generator, List

import pytest
from fastapi.testclient import TestClient
from pydantic_ai.ai_response import AITextResponse
from pydanticai_api_template.api.endpoints import app, verify_api_key


@pytest.fixture(scope="function")
def client(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[TestClient, None, None]:
    # Patch the API key verification dependency for all tests in this module
    async def skip_auth() -> bool:
        return True

    app.dependency_overrides[verify_api_key] = skip_auth
    with TestClient(app) as c:
        yield c
    # Clean up the override after tests
    del app.dependency_overrides[verify_api_key]


def test_agentic_rag_endpoint(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    # Patch build_deps to use dummy clients
    from pydanticai_api_template.agents.rag.models import AgentDeps, Chunk
    from pydanticai_api_template.agents.rag.tools import agent

    class DummyEmbeddingClient:
        async def create(self, model: str, input: str) -> Dict[str, Any]:
            return {"data": [{"embedding": [0.1, 0.2, 0.3]}]}

    class DummyDBClient:
        async def search_embeddings(self, vector: List[float], top_k: int, filter: dict) -> List[Chunk]:
            return [
                Chunk(title="Doc1", content="Content1"),
                Chunk(title="Doc2", content="Content2"),
            ]

        async def list_urls(self, source: str) -> List[str]:
            return ["/docs/one.md", "/docs/two.md"]

        async def get_chunks(self, url: str, source: str) -> List[Chunk]:
            return [
                Chunk(title="Doc1", content="Content1"),
                Chunk(title="Doc2", content="Content2"),
            ]

    def dummy_build_deps() -> AgentDeps:
        return AgentDeps(
            llm_client=None,  # Provide a dummy LLM if agent.run needs it internally
            embedding_client=DummyEmbeddingClient(),
            db_client=DummyDBClient(),
            reasoner_output=None,
        )

    monkeypatch.setattr("pydanticai_api_template.agents.rag.orchestrator.build_deps", dummy_build_deps)

    # Patch the PydanticAI agent's run method directly to avoid actual LLM calls
    async def dummy_agent_run(*args: Any, **kwargs: Any) -> AITextResponse:
        # Simulate getting context from dummy DB
        db_client = DummyDBClient()
        chunks = await db_client.search_embeddings([], 0, {})
        context = "\n".join([c.content for c in chunks])
        # Return a dummy response incorporating the dummy context
        return AITextResponse(data=f"Dummy LLM answer based on: {context}")

    monkeypatch.setattr(agent, "run", dummy_agent_run)

    # Make request (no API key header needed due to dependency override)
    response = client.post(
        "/agentic-rag",
        json={"question": "What is the RAG pattern?"},
        # headers={"X-API-Key": "test"}, # No longer needed
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # Check if the dummy context is in the dummy answer
    assert "Content1" in data["answer"]
    assert "Content2" in data["answer"]
