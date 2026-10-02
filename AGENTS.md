# AGENTS.md — url-shortener-platform

## 1. Project Identity

- Repository: `url-shortener-platform`
- Root folder: `url-shortener-platform/`
- Backend image: `url-shortener-backend`
- Frontend image: `url-shortener-frontend`
- Terraform infra name: `url-shortener-infrastructure`
- Use these names consistently. No alternatives without technical reason.

## 2. Environment

- Developer uses Windows PowerShell. All commands below work in PowerShell.
- `make` is NOT native to PowerShell. Get it via Git Bash, WSL, or `choco install make`.
- Every `make <target>` below lists its plain equivalent. Prefer plain commands in PowerShell.
- PowerShell venv activate: `.venv\Scripts\Activate.ps1` (not `source .venv/bin/activate`).
- Use `;` or separate lines, not `&&`. Use `Join-Path` / backslashes for paths.

## 3. Stack

- Backend: Python 3.12+, FastAPI, Uvicorn, Redis, Pydantic, pytest, Ruff, pip-audit, prometheus-fastapi-instrumentator
- Frontend: Vue 3, Vite, TypeScript, Vitest, Vue Test Utils, npm audit
- Infra: Docker, Docker Compose, Terraform (Docker Provider)
- CI/CD: GitHub Actions (tests, lint, scans, container + infra checks)
- Observability: Prometheus, Grafana, Alertmanager
- Load: Locust
- Security: Ruff, pip-audit, npm audit, Trivy, Dependabot

## 4. Repository Structure

Monorepo. Responsibilities stay separated.

```text
url-shortener-platform/
  backend/
    app/
      api/
      core/
      models/
      schemas/
      services/
      repositories/
      observability/
      main.py
    tests/
    requirements.txt
    pyproject.toml
  frontend/
    src/
      components/
      views/
      services/
      composables/
      types/
      router/
    tests/
    package.json
    vite.config.ts
    tsconfig.json
  infra/
    terraform/
      main.tf
      variables.tf
      outputs.tf
      providers.tf
      versions.tf
    docker/
  monitoring/
    prometheus/
      prometheus.yml
      rules/
    grafana/
      dashboards/
      provisioning/
    alertmanager/
      alertmanager.yml
  loadtest/
    locustfile.py
  docker-compose.yml
  Makefile
  .env.example
  AGENTS.md
  README.md
```

## 5. Commands

Run from repo root in PowerShell unless noted.

### Run / dev

- make dev = docker compose up --build
- make backend = cd backend; uvicorn app.main:app --reload --port 8000
- make frontend = cd frontend; npm run dev
- Backend venv (PowerShell):
  cd backend; python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
- Frontend install: cd frontend; npm install

### Build

- make install = backend pip install -r requirements.txt plus frontend npm install
- make docker-up = docker compose up --build -d
- make docker-down = docker compose down
- make monitoring-up = docker compose -f docker-compose.yml up -d prometheus grafana alertmanager

### Test

- make test = run both below
- make test-backend = cd backend; pytest -q
- make test-frontend = cd frontend; npm test -- --run
- make load-test = cd loadtest; locust -f locustfile.py

### Lint / format

- make lint = backend ruff check . plus frontend npm run lint
- make format = backend ruff format . plus frontend npm run format

### Terraform

Run the Terraform targets from the repository root. The PowerShell script works without GNU Make; Make targets delegate to it.

- make tf-fmt = terraform -chdir=infra/terraform fmt -recursive
- make tf-init = terraform -chdir=infra/terraform init
- make tf-validate = terraform -chdir=infra/terraform validate
- make tf-plan = terraform -chdir=infra/terraform plan -out=tfplan
- make tf-apply = terraform -chdir=infra/terraform apply tfplan
- make tf-destroy = scripts/dev.ps1 tf-destroy; it prints the destroy plan and requires typing DESTROY before applying it
- PowerShell equivalents: scripts\dev.ps1 tf-fmt, tf-init, tf-validate, tf-plan, tf-apply, or tf-destroy

Use either Docker Compose or Terraform for the local stack, not both on the same port at the same time. Commit infra/terraform/.terraform.lock.hcl; never commit state, plan files, or terraform.tfvars.

### Docker

- make docker-build / scripts\dev.ps1 docker-build = docker build -t url-shortener-backend:dev backend
- make up / scripts\dev.ps1 up = docker compose up -d --build
- make down / scripts\dev.ps1 down = docker compose down (never -v)
- make logs / scripts\dev.ps1 logs = docker compose logs backend --tail 50
- make ps / scripts\dev.ps1 ps = docker compose ps
## 6. Hard Rules

- Do not delete working tests to make CI pass.
- Do not disable scanners without documented justification.
- Do not remove monitoring because it is inconvenient.
- Do not weaken validation to accept invalid input.
- Do not silently change API contracts.
- Do not swap Vue, FastAPI, or Redis without approval.
- Do not add Kubernetes / microservices without justification.
- Do not remove Terraform because Compose works locally.
- Never commit secrets or Terraform state.

## 7. Working Style

- Work in small steps. Simplest solution first.
- Keep README and Makefile in sync with real commands.
- No destructive actions without explicit ask.
- Run verification (tests / lint / plan) before saying done.

## 8. Docs Index

Read ONLY the doc that matches the current task. Never load all docs.

| When you work on... | Read |
|---|---|
| Project goals, principles | docs/getting-started/overview.md |
| Stack, repo layout, high-level arch | docs/getting-started/architecture.md |
| Endpoints, status codes, contracts | docs/backend/api-contract.md |
| Data model, config, errors | docs/backend/backend-design.md |
| Backend tasks | docs/backend/phase1-backend-implementation.md |
| Frontend tasks | docs/frontend/frontend.md |
| Tests, lint, local run | docs/frontend/phase1-testing-and-workflow.md |
| Docker, Compose | docs/delivery/docker.md |
| Terraform infra | docs/delivery/terraform.md |
| CI, pipelines, scans | docs/delivery/ci-cd.md |
| Releases, branches, commits | docs/delivery/release-and-git.md |
| Metrics, dashboards | docs/observability/observability.md |
| Alerts, failure injection | docs/observability/alerting.md |
| Load tests | docs/observability/load-testing.md |
| QA layers | docs/quality/qa-testing.md |
| Recovery, release checks | docs/quality/qa-validation.md |
| Hardening | docs/quality/security.md |
| Deps, CI/TF security, envs | docs/delivery/supply-chain-and-environments.md |
| Docs rules, scope | docs/governance/documentation-and-scope.md |
| Scope changes, migrations | docs/governance/change-policy.md |
| Code / log / metric style | docs/quality/conventions.md |
| Restrictions, dep rules | docs/governance/agent-rules.md |
| Order, milestones, DoD | docs/getting-started/roadmap-and-dod.md |

## 9. Current Status

- [x] Milestone 1: Backend can create, redirect, and analyze short URLs.
- [ ] Milestone 2: Frontend provides the complete basic user flow.
- [ ] Milestone 3: Backend and frontend run through Docker Compose.
- [ ] Milestone 4: Terraform can reproduce the intended infrastructure.
- [ ] Milestone 5: CI validates code, tests, security, containers, and infrastructure.
- [ ] Milestone 6: Prometheus and Grafana provide meaningful telemetry.
- [ ] Milestone 7: Alertmanager detects meaningful failures.
- [ ] Milestone 8: Locust validates baseline and stress behavior.
- [ ] Milestone 9: Failure injection and recovery are verified.
- [ ] Milestone 10: Security and release validation are complete.

Update this when a milestone is done.
