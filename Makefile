.PHONY: venv install test lint clean

venv:
	uv venv

install: venv
	uv sync --group dev
	uv run pre-commit install

test:
	uv run pytest

lint:
	uv run pre-commit run --all-files

clean:
	rm -rf .venv .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
