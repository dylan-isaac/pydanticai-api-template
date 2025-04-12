# Architecture

This document describes the system design and architecture of the PydanticAI API Template.

## System Overview

The PydanticAI API Template is built on the following key components:

```
┌───────────────────────────────────────────────────────┐
│                     FastAPI App                        │
│                                                       │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │   Routes    │   │  Pydantic   │   │    API      │  │
│  │ (endpoints) │◄──┤   Models    │◄──┤   Logic     │  │
│  └─────────────┘   └─────────────┘   └─────────────┘  │
│           ▲                ▲                ▲         │
└───────────┼────────────────┼────────────────┼─────────┘
            │                │                │
            ▼                ▼                ▼
┌───────────────────────────────────────────────────────┐
│                    PydanticAI                         │
│                                                       │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │   Agent     │───┤  Structured │───┤     LLM     │  │
│  │ Definitions │   │  Responses  │   │ Integration │  │
│  └─────────────┘   └─────────────┘   └─────────────┘  │
│                                                       │
└───────────────────────────────────────────────────────┘
```

## Component Details

### FastAPI Application

The FastAPI application provides the web API interface and handles HTTP requests and responses.

- **Routes (endpoints.py)**: Defines the API endpoints and their behavior.
- **Pydantic Models (models.py)**: Defines the data models for requests and responses.
- **API Logic**: Business logic for processing requests and generating responses.

### PydanticAI Integration

PydanticAI provides a bridge between the API and LLMs, allowing structured interactions.

- **Agent Definitions**: Configures the PydanticAI agent for handling AI requests.
- **Structured Responses**: Uses Pydantic models to ensure type-safe, validated responses from LLMs.
- **LLM Integration**: Handles communication with underlying LLM services (like OpenAI).

### CLI Application

A command-line interface for managing the application, built with Typer.

- **Server Command**: Starts the FastAPI server.
- **Utility Commands**: Helper functions for validation, cleanup, etc.
- **Development Tools**: Commands to assist the development workflow.

## Data Flow

1. Client sends a request to the API endpoint
2. FastAPI validates the request using Pydantic models
3. The endpoint handler processes the request and calls the PydanticAI agent
4. PydanticAI communicates with the LLM service using the request parameters
5. The LLM generates a response, which is parsed and validated by PydanticAI
6. The structured response is returned to the client

## Configuration Management

The application uses a hierarchical configuration approach:

1. Environment variables (highest priority)
2. .env file variables
3. Default values in code (lowest priority)

Key configuration options include:
- OPENAI_API_KEY: For LLM integration
- HOST/PORT: For server binding
- LOG_LEVEL: For log verbosity control

## Extensibility

The architecture is designed for extensibility:

1. **New LLM Providers**: Can be added by extending the PydanticAI configuration
2. **Additional Endpoints**: Can be easily added to endpoints.py
3. **New Models**: Can be defined in models.py to support new functionality
4. **CLI Commands**: Can be added to cli.py to support new operations

## MCP Server Architecture

The project includes an MCP (Model Context Protocol) server that exposes AI functionalities over a standardized protocol.

### Components

```
                  ┌──────────────────┐
                  │   MCP Client     │
                  │  (Any Protocol-  │
                  │ Compatible Agent)│
                  └────────┬─────────┘
                           │
                           │ HTTP SSE
                           │ Connection
                           ▼
┌───────────────────────────────────────────────┐
│                 MCP Server                     │
│                                               │
│  ┌───────────────┐      ┌───────────────────┐ │
│  │  FastMCP      │◄────►│ AI Agent Tools    │ │
│  │  Server       │      │                   │ │
│  └───────┬───────┘      └─────────┬─────────┘ │
│          │                        │           │
│          │                        │           │
│          ▼                        ▼           │
│  ┌───────────────┐      ┌───────────────────┐ │
│  │  FastAPI      │      │ PydanticAI Agent  │ │
│  │  Integration  │      │                   │ │
│  └───────────────┘      └───────────────────┘ │
└───────────────────────────────────────────────┘
```

### Key Components

1. **MCP Server** (`mcp_server.py`):
   - Implements the Model Context Protocol server using FastMCP
   - Provides AI tools that can be called by any MCP-compatible client
   - Integrates with the FastAPI application for unified deployment

2. **AI Agent Tools**:
   - `chat`: Exposes the chat functionality to MCP clients
   - Extensible: New tools can be added using the `@server.tool()` decorator

3. **Transport Protocol**:
   - Uses HTTP Server-Sent Events (SSE) for network communication
   - Allows multiple clients to connect to the server remotely

### Advantages

- **Standardized Protocol**: Allows any MCP-compatible agent to access your API's functionalities
- **Decoupled Architecture**: MCP clients don't need to know API implementation details
- **Unified Development**: Same AI agents used in both REST API and MCP server
- **Extensibility**: Easy to add new tools without changing client code
