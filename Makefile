.DEFAULT_GOAL := help

PYTHON = python
MANAGE = $(PYTHON) manage.py

.PHONY: help install run test lint format migrate makemigrations test-data collectstatic clean

help:
	@echo "Available commands for willowstretch project:"
	@echo "  make install       - Install project dependencies from requirements.txt"
	@echo "  make run           - Run the Django development server"
	@echo "  make test          - Run tests with pytest and generate a coverage report"
	@echo "  make lint          - Run linting with ruff and type checking with mypy"
	@echo "  make makemigrations - Create new database migrations"
	@echo "  make migrate       - Apply database migrations"
	@echo "  make format        - Format code with ruff"
	@echo "  make test-data     - Generate test data"
	@echo "  make collectstatic - Collect static files"
	@echo "  make clean         - Remove temporary files"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Installing NLTK requirements"
	python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt_tab')" || echo "NLTK skipped"

run:
	@echo "Starting Django development server..."
	$(MANAGE) runserver

test:
	@echo "Running tests..."
	pytest

fix:
	@echo "Fixing lint errors..."
	ruff check . --fix
	@echo "Formatting code..."
	ruff format .

lint:
	@echo "🧹 Cleaning MyPy cache..."
	rm -rf .mypy_cache
	@echo "Running linter and type checker..."
	ruff check .
	mypy .

format:
	@echo "Formatting code with ruff..."
	ruff format .

makemigrations:
	@echo "Creating database migrations..."
	$(MANAGE) makemigrations

migrate:
	@echo "Applying database migrations..."
	$(MANAGE) migrate

test-data:
	@echo "Generating test data..."
	# Note: Command ini akan error kalau kamu belum bikin custom command 'seed_production'
	# $(MANAGE) seed_production
	# $(MANAGE) seed_test_data
	@echo "Skipping seed (command not created yet)"

collectstatic:
	@echo "Collecting static files..."
	$(MANAGE) collectstatic --no-input

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache