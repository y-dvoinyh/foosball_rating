.PHONY: up down logs compose-config migrate worker beat test test-backend test-frontend lint lint-backend lint-frontend format format-backend format-frontend docs docs-build

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

compose-config:
	docker compose config

migrate:
	docker compose up migrate

worker:
	docker compose up celery-worker

beat:
	docker compose up celery-beat

test: test-backend test-frontend

test-backend:
	docker compose run --rm backend-tests

test-frontend:
	docker compose run --rm frontend-tests

lint: lint-backend lint-frontend

lint-backend:
	cd backend && ruff check .

lint-frontend:
	cd frontend && npm run lint

format: format-backend format-frontend

format-backend:
	cd backend && ruff format . && ruff check . --fix

format-frontend:
	cd frontend && npm run format

docs:
	mkdocs serve

docs-build:
	mkdocs build
