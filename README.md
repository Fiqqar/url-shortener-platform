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