.PHONY: build, test, lint, typecheck, format, push-update

AWS_PROFILE_NAME=data-admin
VERSION=0.1.4

setup-env:
	@python3 -m venv env 
	@source env/bin/activate && poetry install

format:
	@echo "\n🎨 Formatting..." && \
	poetry run black . --config pyproject.toml

typecheck: format
	@echo "\n🏷️ Type-checking..." && \
	poetry run mypy plogging --config-file pyproject.toml

lint: typecheck
	@echo "\n👔 Linting..." && \
	poetry run flake8 plogging --toml-config pyproject.toml

test: lint
	@echo "\n🧪 Testing..." && \
	python -m pytest

build: test
	@echo "\n🧱 Building version ${VERSION}..." && \
	rm -rf dist && \
	poetry version ${VERSION} && \
	python -m build

