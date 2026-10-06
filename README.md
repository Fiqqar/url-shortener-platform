# url-shortener-platform

See AGENTS.md for rules, commands, and workflow.

Docs: docs/ (see Docs Index in AGENTS.md).

## Run with Docker

~~~powershell
Copy-Item .env.example .env  # optional local overrides; Compose sets REDIS_HOST=redis
docker compose up -d --build
Invoke-RestMethod http://localhost:8000/health
docker compose ps
~~~

## Observability (local)

Prometheus and Grafana run through Compose and bind to localhost only.

~~~powershell
docker compose up -d prometheus alertmanager grafana   # or: make monitoring-up
~~~

- Prometheus: <http://localhost:9090> (scrape target health at <http://localhost:9090/targets>, alerts at <http://localhost:9090/alerts>)
- Alertmanager: <http://localhost:9093> (alerts at <http://localhost:9093/api/v2/alerts>)
- Grafana: <http://localhost:3001>; local default login `admin` / `admin` (change it for anything non-local)
- Dashboard "URL Shortener Platform" is provisioned from the repository, so the committed file is the source of truth

The dashboard covers request and error rate, p50/p95/p99 latency, redirect, URL creation, and analytics rates, Redis and application errors, scrape target health, and process memory. The Redis and application error panels stay empty until an error actually occurs.

Alerts (`monitoring/prometheus/rules/alerts.yml`): `BackendDown` (critical), `HighErrorRate` (warning, >5% 5xx for 2m), `HighLatency` (warning, p95 >0.5s for 2m), `RedisDown` (critical). Labels stay low-cardinality (`severity`, `service`, `environment`); thresholds are local-learning values, tune from baseline before non-local use.

Configuration lives in `monitoring/`:

- `monitoring/prometheus/prometheus.yml` scrapes `backend:8000/metrics` every 15s and sends alerts to `alertmanager:9093`
- `monitoring/prometheus/rules/alerts.yml` holds the 4 alert rules
- `monitoring/alertmanager/alertmanager.yml` routes warning + critical to the local test receiver (no real notifications; view in Alertmanager UI)
- `monitoring/grafana/provisioning/` provisions the datasource and the dashboard provider
- `monitoring/grafana/dashboards/url-shortener.json` is the provisioned dashboard

Configuration changes are validated in CI (`.github/workflows/monitoring-ci.yml` via `promtool check config`, `promtool check rules`, `amtool check-config`); run `python scripts/validate_monitoring.py` locally to reproduce the structural checks.

Test alert firing locally:

~~~powershell
docker compose up -d --build redis backend prometheus alertmanager
docker stop url-shortener-platform-backend-1  # wait ~75s: BackendDown firing in Prometheus + Alertmanager
Invoke-RestMethod http://localhost:9090/api/v1/alerts
Invoke-RestMethod http://localhost:9093/api/v2/alerts
docker start url-shortener-platform-backend-1  # wait ~60s: alerts resolve, target up
~~~

Generate sample traffic and watch the panels move:

~~~powershell
$r = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/urls -ContentType "application/json" -Body '{"url":"https://example.com"}'
1..10 | ForEach-Object { curl.exe -s -o NUL "http://localhost:8000/$($r.code)" }
Invoke-RestMethod "http://localhost:8000/api/v1/urls/$($r.code)/analytics"
~~~

## Provision with Terraform

Use either Docker Compose or Terraform for this stack, not both on the same host ports at the same time. Terraform provisions the backend, frontend, Redis, a dedicated Docker network, and a persistent Redis volume; backend and frontend ports bind to localhost. Docker Desktop must be running, and the local `url-shortener-backend:dev` and `url-shortener-frontend:dev` images must exist. The frontend image bakes in `VITE_API_BASE_URL` at build time; rebuild it if you change Terraform's backend host port.

~~~powershell
terraform -chdir=infra/terraform init
.\scripts\dev.ps1 tf-fmt
.\scripts\dev.ps1 tf-validate
.\scripts\dev.ps1 tf-plan
.\scripts\dev.ps1 tf-apply
~~~

To create the local images if needed, run these commands from the repository root:

~~~powershell
docker build -t url-shortener-backend:dev backend
docker build -t url-shortener-frontend:dev --build-arg VITE_API_BASE_URL=http://localhost:8000 frontend
~~~

The destroy command prints a destroy plan and requires typing DESTROY before it applies that plan:

~~~powershell
.\scripts\dev.ps1 tf-destroy
~~~

See infra/terraform/README.md for variables, outputs, and local infrastructure details.
