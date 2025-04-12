"""
Observability module for PydanticAI API Template.

This module configures logfire for logging and tracing. It provides
functions to set up observability for the application.
"""

import os
from typing import Optional

import logfire

# Try to import configure_pydantic_ai_instrumentation,
# but don't fail if it's not available
try:
    from logfire.pydantic_ai import configure_pydantic_ai_instrumentation

    HAS_PYDANTIC_AI_INTEGRATION = True
except ImportError:
    # Create a no-op function as fallback
    def configure_pydantic_ai_instrumentation() -> None:
        """No-op function when logfire.pydantic_ai is not available."""
        pass

    HAS_PYDANTIC_AI_INTEGRATION = False


def is_logfire_enabled() -> bool:
    """Check if LogFire is enabled via environment variable."""
    return os.getenv("LOGFIRE_ENABLED", "false").lower() in ("true", "1", "yes")


def setup_logfire(
    service_name: str = "pydanticai-api-template",
    environment: Optional[str] = None,
) -> None:
    """
    Set up LogFire for observability.

    Args:
        service_name: The name of the service
        environment: The environment (dev, staging, prod)
    """
    if not is_logfire_enabled():
        return

    # Configure LogFire
    api_key = os.getenv("LOGFIRE_API_KEY")
    project_id = os.getenv("LOGFIRE_PROJECT_ID")

    # Determine environment from ENV var or default to development
    env = environment or os.getenv("ENVIRONMENT", "development")

    # Configure LogFire with the API key and project ID
    logfire.configure(
        api_key=api_key,
        project_id=project_id,
        service_name=service_name,
        environment=env,
    )

    # Set up instrumentation for common libraries
    logfire.instrument_httpx()  # HTTP client monitoring
    logfire.instrument_fastapi()  # FastAPI monitoring
    logfire.instrument_asyncio()  # AsyncIO monitoring

    # Configure PydanticAI instrumentation if available
    if HAS_PYDANTIC_AI_INTEGRATION:
        configure_pydantic_ai_instrumentation()

    logfire.info(
        "LogFire observability configured successfully",
        service_name=service_name,
        environment=env,
    )


def shutdown_logfire() -> None:
    """Shutdown LogFire and flush any pending logs."""
    if is_logfire_enabled():
        logfire.info("Shutting down LogFire")
        logfire.shutdown()
