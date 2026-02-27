.PHONY: help install run clean lint lint-strict

# Default target: show help
help:
	@echo "Available targets:"
	@echo "  make install      - Install project dependencies using uv"
	@echo "  make run          - Run the maze application"
	@echo "  make clean        - Remove temporary files and caches"
	@echo "  make lint         - Run linting with flake8 and mypy"
	@echo "  make lint-strict  - Run strict linting with flake8 and mypy"

# Install dependencies from pyproject.toml using uv
install:
	uv sync --dev

# Run the main application
run:
	uv run python a_maze_ing.py

# Remove temporary files and caches
clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	@echo "Clean complete!"

# Run linting with flake8 and mypy
lint:
	@echo "Running flake8..."
	uv run flake8 .
	@echo "Running mypy..."
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Run strict linting with flake8 and mypy
lint-strict:
	@echo "Running flake8..."
	uv run flake8 .
	@echo "Running mypy in strict mode..."
	uv run mypy . --strict
