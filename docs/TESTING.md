# Testing Guide

This document describes how to test the PydanticAI API Template, including the MCP server.

## Running Tests

### Automated Tests

To run the automated tests:

```bash
# Run all tests
pydanticai-api-template test

# Run specific tests with pytest directly
python -m pytest tests/test_mcp_server.py -v
```

### Test Coverage

To generate test coverage reports:

```bash
python -m pytest --cov=pydanticai_api_template tests/
```

## Testing the MCP Server

### Automated Tests

The MCP server has unit tests in `tests/test_mcp_server.py` that test:

1. Server creation
2. Chat tool functionality
3. Error handling

### Manual Testing

#### Prerequisites

1. Install dependencies:
   ```bash
   pip install -e ".[test]"
   ```

2. Set up environment variables:
   ```bash
   # Create a .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

#### Running the MCP Server

Start the MCP server:

```bash
pydanticai-api-template run-mcp
```

The server will start on http://localhost:3001 by default.

#### Using the Example Client

Run the example MCP client to test connection to the server:

```bash
python examples/mcp_client_example.py
```

This will send test messages to the MCP server and display the responses.

#### Testing with curl

You can also test the SSE connection using curl:

```bash
curl -N http://localhost:3001/sse
```

This should establish a connection to the SSE endpoint.

## Testing Checklist

- [ ] Verify that the MCP server starts without errors
- [ ] Verify that the chat tool responds to messages
- [ ] Verify error handling when the OpenAI API key is missing
- [ ] Verify error handling when the LLM service returns an error
- [ ] Verify that multiple clients can connect to the server

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Make sure you've installed the package with dev dependencies: `pip install -e ".[dev,test]"`

2. **OpenAI API Key issues**:
   - Check that your OpenAI API key is correctly set in the .env file
   - Check that the .env file is in the correct location (project root)

3. **Port already in use**:
   - If port 3001 is already in use, change the port: `pydanticai-api-template run-mcp --port 3002`

### MCP Server Logs

To see detailed logs from the MCP server:

```bash
pydanticai-api-template run-mcp --log-level debug
```

This will show more detailed information about the server operation and any errors.

## Continuous Integration

If you're setting up CI/CD pipelines, add the following steps to test the MCP server:

```yaml
# Example GitHub Actions step
- name: Test MCP Server
  run: |
    python -m pytest tests/test_mcp_server.py -v
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```
