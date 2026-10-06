# Terraform: local Docker stack

## Requirements and scope

- Terraform `~> 1.16.4` and Docker provider `~> 4.6.0`; keep `.terraform.lock.hcl` under version control.
- Docker Desktop Engine on Windows, using the npipe endpoint in `providers.tf`.
- Existing local `url-shortener-backend:dev` and `url-shortener-frontend:dev` images. Terraform references these images; it does not build them.
- Terraform manages the backend, frontend, Redis, one Docker network, and a persistent Redis volume. Backend and frontend ports bind to `127.0.0.1`; Redis is not published. Redis has a configurable `maxmemory` default of `256mb` and uses `noeviction`, so new writes fail rather than deleting existing short URLs when the limit is reached.

Use Docker Compose or Terraform for the local stack, not both on the same host ports. Defaults are backend `8000` and frontend `3000`. Terraform derives the backend `BASE_URL` from `backend_port`. The frontend bundle contains its API base URL at build time, so if `backend_port` changes, rebuild the frontend image with a matching `VITE_API_BASE_URL` build argument.

## Variables

| Variable | Default | Description |
| --- | --- | --- |
| `docker_host` | `npipe:////.//pipe//docker_engine` | Docker Engine endpoint |
| `backend_image` | `url-shortener-backend:dev` | Existing local backend image |
| `frontend_image` | `url-shortener-frontend:dev` | Existing local frontend image |
| `redis_image` | `redis:7-alpine` | Tagged or digest-pinned Redis image |
| `redis_maxmemory` | `256mb` | Redis data memory cap; full Redis rejects writes |
| `backend_port` | `8000` | Host port mapped to backend port 8000 |
| `frontend_port` | `3000` | Host port mapped to frontend port 80 |

Copy `terraform.tfvars.example` to `terraform.tfvars` only when overriding defaults. It contains no credentials. Local state is ignored by Git and may contain infrastructure data.

## Outputs

`backend_url`, `frontend_url`, backend/frontend/Redis container names, Redis volume name, and network name.

## PowerShell workflow

Run from the repository root:

~~~powershell
terraform -chdir=infra/terraform init
.\scripts\dev.ps1 tf-fmt
.\scripts\dev.ps1 tf-validate
.\scripts\dev.ps1 tf-plan
.\scripts\dev.ps1 tf-apply
~~~

Build the expected images first when needed:

~~~powershell
docker build -t url-shortener-backend:dev backend
docker build -t url-shortener-frontend:dev --build-arg VITE_API_BASE_URL=http://localhost:8000 frontend
~~~

Review the plan before applying. `tf-destroy` prints a destroy plan and asks for the exact confirmation `DESTROY` before applying it. Destroy removes the Terraform-managed containers, network, and Redis volume, including persisted data.

Never commit state, plan files, or local `terraform.tfvars` files.

The named Redis volume survives container recreation, but it is not a backup. The project has no scheduled/off-host backup or automated restore procedure. See [Docker and Redis persistence notes](../../docs/delivery/docker.md#current-redis-persistence-and-backup-status) before treating the local volume as valuable data protection.
