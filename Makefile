.PHONY: build, test, lint, typecheck, format, push-update

AWS_PROFILE_NAME=data-admin
VERSION=0.1.4

setup-env:
	@python3 -m venv env 
	@source env/bin/activate && poetry install

format:
	@echo "\n🎨 Formatting..." && \
	python -m black plogging

typecheck: format
	@echo "\n🏷️ Type-checking..." && \
	python -m mypy plogging

lint: typecheck
	@echo "\n👔 Linting..." && \
	python -m flake8 plogging

test: lint
	@echo "\n🧪 Testing..." && \
	python -m pytest

build: test
	@echo "\n🧱 Building version ${VERSION}..." && \
	rm -rf dist && \
	poetry version ${VERSION} && \
	python -m build

