"""
Observability module for PydanticAI API Template.

This module configures logfire for logging and tracing. It provides
functions to set up observability for the application.
"""

import os
from typing import Any, Optional

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
    app: Any = None,
) -> None:
    """
    Set up LogFire for observability.

    Args:
        service_name: The name of the service
        environment: The environment (dev, staging, prod)
        app: Optional FastAPI app instance for instrumentation
    """
    if not is_logfire_enabled():
        return

    # Configure LogFire
    token = os.getenv("LOGFIRE_TOKEN")
    project_id = os.getenv("LOGFIRE_PROJECT_ID")

    # Determine environment from ENV var or default to development
    env = environment or os.getenv("ENVIRONMENT", "development")

    # Configure LogFire with token (preferred) or project_id as fallback
    if token:
        logfire.configure(
            token=token,
            service_name=service_name,
            environment=env,
        )
    else:
        # Legacy configuration with API key and project ID
        api_key = os.getenv("LOGFIRE_API_KEY")
        if api_key and project_id:
            logfire.configure(
                api_key=api_key,
                project_id=project_id,
                service_name=service_name,
                environment=env,
            )
        else:
            logfire.info(
                "LogFire configuration incomplete. Set LOGFIRE_TOKEN or both LOGFIRE_API_KEY and LOGFIRE_PROJECT_ID.",
            )
            return

    # Set up instrumentation for common libraries
    logfire.instrument_httpx()  # HTTP client monitoring

    # Instrument FastAPI - use basic version to avoid linter issues
    # The app parameter might be needed in some versions but not others
    try:
        # For type safety, we ignore the type checker
        logfire.instrument_fastapi()
    except Exception as e:
        logfire.warning(f"Failed to instrument FastAPI: {e}")

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
