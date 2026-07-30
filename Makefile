.PHONY: run build

run:
	uv run python3 src/app.py

build:
	uv sync