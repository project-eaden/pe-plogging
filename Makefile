.PHONY: build, test, lint, typecheck, format, push-update

AWS_PROFILE_NAME=data-admin
VERSION=0.1.2

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
	python -m build 

push-update: 
	@echo "\n🪪 Fetching AWS Deployment Credentials..." && \
	aws codeartifact login --tool twine --repository plogging --domain projecteaden --domain-owner 186292285156 --region eu-west-1 --profile $(AWS_PROFILE_NAME) && \
	echo "\n✅ Deploying version ${VERSION} to remote refactory..."
	twine upload --repository codeartifact dist/plogging-$(VERSION)-py3-none-any.whl --verbose
