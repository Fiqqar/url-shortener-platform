.PHONY: install lint test cov run redis-up redis-down docker-build up down logs ps tf-fmt tf-init tf-validate tf-plan tf-apply tf-destroy

install:
	py -3.13 -m venv backend/.venv
	backend/.venv/Scripts/python -m pip install -r backend/requirements.txt -r backend/requirements-dev.txt

lint:
	backend/.venv/Scripts/python -m ruff check backend

test:
	backend/.venv/Scripts/python -m pytest backend/tests -q

cov:
	backend/.venv/Scripts/python -m pytest backend/tests -q --cov=app --cov-report=term-missing

run:
	cd backend && .venv/Scripts/python -m uvicorn app.main:app --port 8000

redis-up:
	docker start url-redis 2>/dev/null || docker run -d --name url-redis -p 6379:6379 redis:7-alpine

redis-down:
	docker stop url-redis

docker-build:
	docker build -t url-shortener-backend:dev backend

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs backend --tail 50

ps:
	docker compose ps

tf-fmt:
	powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 tf-fmt

tf-init:
	powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 tf-init

tf-validate:
	powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 tf-validate

tf-plan:
	powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 tf-plan

tf-apply:
	powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 tf-apply

tf-destroy:
	powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 tf-destroy