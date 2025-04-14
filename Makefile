.PHONY: install run shell-completion validate lint test clean docker-build docker-up docker-down docker-shell sync-configs logs setup

# Local development commands (primarily for direct host machine use)
# Note: When using Dev Containers, dependencies are already installed
install:
	uv sync && uv pip install -e .

run:
	pat run --reload

shell-completion:
	pat install-completion

validate:
	pat validate

# Code quality commands - note: dependencies are already installed in the container
# If running locally outside the container, these will install dependencies first
lint:
	if [ -f "/.dockerenv" ]; then \
		uv pip install --system -e ".[dev]"; \
	else \
		uv pip install -e ".[dev]"; \
	fi
	ruff check .
	ruff format --check .

test:
	if [ -f "/.dockerenv" ]; then \
		uv pip install --system -e ".[dev,test]"; \
	else \
		uv pip install -e ".[dev,test]"; \
	fi
	pytest

clean:
	rm -rf .venv dist build *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Docker workflow commands
docker-build:
	docker compose build

docker-up:
	docker compose up pydanticai-api-template-dev

docker-down:
	docker compose down

# Enter container shell
docker-shell:
	docker compose exec pydanticai-api-template-dev zsh

# Configuration management
# Use this when you:
# 1. Add/change CLI commands in src/pydanticai_api_template/cli.py (updates VS Code tasks)
# 2. Update development tool versions in pyproject.toml (syncs pre-commit hooks)
sync-configs:
	if [ -f "/.dockerenv" ]; then \
		uv pip install --system pyyaml tomli; \
	fi
	python scripts/tasks/update_configs.py

# View logs for the development container
logs:
	docker compose logs -f pydanticai-api-template-dev

# Complete setup command (for new developers, primarily outside Dev Containers)
setup: install docker-build shell-completion validate
	@echo "Setup complete! 🚀"
	@echo "Run 'make dev' to start local development (outside container)"
	@echo "Run 'make docker-up' to start in Docker (or use Dev Containers)"
