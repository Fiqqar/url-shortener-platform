# url-shortener-platform

See `AGENTS.md` for rules, commands, and workflow.

Docs: `docs/` (see Docs Index in `AGENTS.md`).

## Run with Docker

```powershell
Copy-Item .env.example .env  # first time only; set REDIS_HOST=redis
docker compose up -d --build
Invoke-RestMethod http://localhost:8000/health
docker compose ps
```
