.PHONY: help build up down logs clean install import-data

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all Docker containers
	docker-compose build

up: ## Start all services
	docker-compose up -d
	@echo "Services started!"
	@echo "Backend API: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "API Docs: http://localhost:8000/docs"

down: ## Stop all services
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

logs-postgres: ## Show postgres logs
	docker-compose logs -f postgres

clean: ## Stop and remove all containers, volumes, and networks
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf backend/app/__pycache__

install: ## Install dependencies (run after first clone)
	@echo "Creating .env file..."
	cp .env.example .env
	@echo "Building containers..."
	make build
	@echo "Starting services..."
	make up
	@echo "Waiting for services to be ready..."
	sleep 10
	@echo "Importing sample data..."
	make import-data
	@echo ""
	@echo "Installation complete!"
	@echo "Edit .env file and add your API keys:"
	@echo "  - ANTHROPIC_API_KEY"
	@echo "  - OPENAI_API_KEY"

import-data: ## Import sample data into database
	docker-compose exec backend python scripts/import_data.py

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

shell-db: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U ruesselsheim_bot -d ruesselsheim_chatbot

restart: ## Restart all services
	docker-compose restart

restart-backend: ## Restart backend service
	docker-compose restart backend

restart-frontend: ## Restart frontend service
	docker-compose restart frontend
