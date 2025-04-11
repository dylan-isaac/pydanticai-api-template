FROM python:3.12-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y curl

# Set the working directory
WORKDIR /app

# Copy only what's needed for pip installation
COPY pyproject.toml README.md /app/
COPY app /app/app/

# Install the package
RUN pip install -e .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using our CLI
CMD ["python", "-m", "app.cli", "run", "--host", "0.0.0.0", "--port", "8000"] 