FROM python:3.12-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Copy only necessary files for dependency installation
COPY pyproject.toml README.md /app/
COPY src /app/src/

# Install uv and then install project dependencies using uv
# This utilizes uv's speed and lock file for reproducibility
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv pip install --system --no-cache --locked "."

# Copy the rest of the application code
# This is done after installing dependencies to leverage Docker layer caching
# No need to copy src again as it was copied above for install
# COPY src /app/src/

# Ensure the app directory is owned by the appuser
# This includes the installed package in site-packages if installed globally
# Adjust ownership based on where uv installs the package if needed
RUN chown -R appuser:appuser /app /usr/local/lib/python3.12/site-packages

# Switch to the non-root user
USER appuser
WORKDIR /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using the CLI entry point defined in pyproject.toml
# Ensures it runs as the non-root user
CMD ["pydanticai-api-template", "run", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info"] # Use CLI script name 