.PHONY: install dev shell run validate lint test clean docker-build docker-up docker-down sync-configs logs

# Local development
install:
	uv sync && uv pip install -e .

dev:
	pydanticai-api-template run --reload

shell-completion:
	pydanticai-api-template install-completion

validate:
	pydanticai-api-template validate

lint:
	uv pip install -e ".[dev]"
	ruff check .
	black --check .

test:
	uv pip install -e ".[dev,test]"
	pytest

clean:
	rm -rf .venv dist build *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Docker commands
docker-build:
	docker compose build

docker-up:
	docker compose up pydanticai-api-template-dev

docker-down:
	docker compose down

# Enter container shell
docker-shell:
	docker compose exec pydanticai-api-template-dev bash

# Config management
sync-configs:
	python -m pip install tomli pyyaml
	python scripts/update_configs.py

# View logs for the development container
logs:
	docker compose logs -f pydanticai-api-template-dev

# One command to rule them all - for new developers
setup: install docker-build shell-completion validate
	@echo "Setup complete! 🚀"
	@echo "Run 'make dev' to start local development"
	@echo "Run 'make docker-up' to start in Docker" 