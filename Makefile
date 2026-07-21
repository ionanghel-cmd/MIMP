.PHONY: help install setup run run-dev docker-build docker-up docker-down lint clean test

help:
	@echo "MotoERP - Available commands"
	@echo "============================"
	@echo ""
	@echo "Setup:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make setup       - Full setup (.env + install)"
	@echo ""
	@echo "Running:"
	@echo "  make run         - Run Streamlit app (production)"
	@echo "  make run-dev     - Run with debug logging"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker container"
	@echo "  make docker-down  - Stop Docker container"
	@echo ""
	@echo "Development:"
	@echo "  make clean       - Remove __pycache__ and .pyc files"
	@echo "  make lint        - Run code linter"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

setup:
	@echo "⚙️  Setting up MotoERP..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "📝 Created .env - please edit with Supabase credentials"; \
	fi
	pip install -r requirements.txt
	@echo "✅ Setup complete!"

run:
	@echo "🚀 Starting MotoERP..."
	streamlit run app/app.py

run-dev:
	@echo "🚀 Starting MotoERP (Debug mode)..."
	streamlit run app/app.py --logger.level=debug

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t moto-erp:latest .
	@echo "✅ Image built"

docker-up:
	@echo "🐳 Starting Docker container..."
	docker-compose up

docker-down:
	@echo "🐳 Stopping Docker container..."
	docker-compose down

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned"

lint:
	@echo "🔍 Linting code..."
	python -m py_compile app/*.py
	@echo "✅ Code looks good"

test:
	@echo "🧪 Running tests..."
	@echo "Tests not yet implemented"
	@echo "See ROADMAP.md for testing phase"
