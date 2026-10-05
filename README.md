# url-shortener-platform

See AGENTS.md for rules, commands, and workflow.

Docs: docs/ (see Docs Index in AGENTS.md).

## Run with Docker

~~~powershell
Copy-Item .env.example .env  # first time only; set REDIS_HOST=redis
docker compose up -d --build
Invoke-RestMethod http://localhost:8000/health
docker compose ps
~~~

## Observability (local)

Prometheus and Grafana run through Compose and bind to localhost only.

~~~powershell
docker compose up -d prometheus grafana   # or: make monitoring-up
~~~

- Prometheus: http://localhost:9090 (scrape target health at http://localhost:9090/targets)
- Grafana: http://localhost:3001; local default login `admin` / `admin` (change it for anything non-local)
- Dashboard "URL Shortener Platform" is provisioned from the repository, so the committed file is the source of truth

The dashboard covers request and error rate, p50/p95/p99 latency, redirect, URL creation, and analytics rates, Redis and application errors, scrape target health, and process memory. The Redis and application error panels stay empty until an error actually occurs.

Configuration lives in `monitoring/`:

- `monitoring/prometheus/prometheus.yml` scrapes `backend:8000/metrics` every 15s
- `monitoring/prometheus/rules/` holds Prometheus rule files (alert rules arrive in the Alertmanager phase)
- `monitoring/grafana/provisioning/` provisions the datasource and the dashboard provider
- `monitoring/grafana/dashboards/url-shortener.json` is the provisioned dashboard

Generate sample traffic and watch the panels move:

~~~powershell
$r = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/urls -ContentType "application/json" -Body '{"url":"https://example.com"}'
1..10 | ForEach-Object { curl.exe -s -o NUL "http://localhost:8000/$($r.code)" }
Invoke-RestMethod "http://localhost:8000/api/v1/urls/$($r.code)/analytics"
~~~

## Provision with Terraform

Use either Docker Compose or Terraform for this stack, not both on the same port at the same time. Terraform provisions the backend, Redis, a dedicated Docker network, and a persistent Redis volume. Docker Desktop must be running, and the local url-shortener-backend:dev image must exist.

~~~powershell
terraform -chdir=infra/terraform init
.\scripts\dev.ps1 tf-fmt
.\scripts\dev.ps1 tf-validate
.\scripts\dev.ps1 tf-plan
.\scripts\dev.ps1 tf-apply
~~~

To create the local backend image if needed, run docker build -t url-shortener-backend:dev backend from the repository root. The destroy command prints a destroy plan and requires typing DESTROY before it applies that plan:

~~~powershell
.\scripts\dev.ps1 tf-destroy
~~~

See infra/terraform/README.md for variables, outputs, and local infrastructure details.