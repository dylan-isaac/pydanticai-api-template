# API Reference

This document provides reference documentation for the PydanticAI API Template's endpoints.

## Base URL

All API endpoints are relative to the base URL:

- **Development**: `http://localhost:8000`
- **Production**: Your deployed URL

## Authentication

Currently, no authentication is required for API endpoints in development. In production, you should implement appropriate authentication mechanisms.

## Endpoints

### GET /

**Description**: Simple root endpoint that returns a welcome message.

**Response**:

```json
{
  "message": "Welcome to the PydanticAI API Template!"
}
```

### POST /chat

**Description**: Sends a message to the PydanticAI agent and receives a structured reply.

**Request**:

```json
{
  "message": "Your message to the AI agent"
}
```

**Response**:

```json
{
  "reply": "The AI agent's response"
}
```

**Notes**:

- Requires `OPENAI_API_KEY` environment variable to be set
- Uses the `gpt-4o` model by default

### POST /story

**Description**: Generates a story idea with a title and premise based on the user's input.

**Request**:

```json
{
  "message": "Give me a sci-fi story about time travel"
}
```

**Response**:

```json
{
  "title": "Echoes of Tomorrow",
  "premise": "A physicist discovers that time isn't linear but layered, with each moment existing simultaneously. When she builds a device to view these layers, she witnesses a future catastrophe and must find a way to reach across time to prevent it."
}
```

**Notes**:

- Requires `OPENAI_API_KEY` environment variable to be set
- Uses the `gpt-4o` model by default
- Input can specify genre, themes, or characters to guide the story idea generation

## Error Responses

The API uses standard HTTP status codes to indicate the success or failure of a request.

### Common Error Codes

- **400 Bad Request**: Invalid request format
- **500 Internal Server Error**: Server-side error
- **502 Bad Gateway**: Error communicating with LLM provider
- **503 Service Unavailable**: AI service is not available (e.g., missing API key)

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Interactive Documentation

When the server is running, you can access interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide a user-friendly interface to explore the API, view request/response schemas, and test endpoints directly.

## Rate Limiting

No rate limiting is implemented in the template by default. In a production environment, you should add appropriate rate limiting based on your use case.

## Extending the API

To add new endpoints, see the [Developer Guide](./DEVELOPER.md) for instructions.

## MCP Server

The project includes an MCP (Model Context Protocol) server that allows AI agents to interact with our API.

### MCP Endpoint

- **URL**: `http://localhost:3001/sse`
- **Transport**: HTTP Server-Sent Events (SSE)

### Available Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `chat` | Chat with the AI assistant | `message`: The message to send to the assistant |
| `story` | Generate a story idea | `message`: The input to guide story generation (e.g., genre, theme) |

### Example Usage

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP

# Connect to the MCP server
server = MCPServerHTTP(url='http://localhost:3001/sse')
agent = Agent('openai:gpt-4o', mcp_servers=[server])

async def main():
    async with agent.run_mcp_servers():
        # Chat example
        chat_result = await agent.run('Your message here')
        print(chat_result.data)

        # Story generation example
        story_result = await agent.run_tool('story', message='Create a sci-fi story about time travel')
        print(f"Title: {story_result['title']}")
        print(f"Premise: {story_result['premise']}")
```

### Adding Custom Tools

To add custom tools to the MCP server, edit the `/app/src/pydanticai_api_template/mcp_server.py` file and add new tool functions using the `@server.tool()` decorator:

```python
@server.tool()
async def your_tool_name(param1: str, param2: int) -> str:
    """Your tool description

    More detailed description here.
    """
    # Tool implementation
    return "Result"
```

### Running the MCP Server

To start the MCP server:

```bash
pat run-mcp
```

By default, the server runs on `0.0.0.0:3001`. You can customize the host and port:

```bash
pat run-mcp --host 127.0.0.1 --port 4000
```
