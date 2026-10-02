.PHONY: install lint test cov run redis-up redis-down

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
