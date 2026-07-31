.PHONY: run build

run:
	uv run python -m src.app

build:
	uv sync