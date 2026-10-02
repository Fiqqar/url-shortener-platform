# Terraform: local Docker stack

## Requirements and scope

- Terraform version constraint: ~> 1.16.4.
- Docker provider: kreuzwerker/docker ~> 4.6.0; keep .terraform.lock.hcl under version control.
- A running Docker Desktop Engine on Windows, using the npipe endpoint configured in providers.tf.
- The local url-shortener-backend:dev image. Terraform references this image and does not build it.
- The stack contains only the backend and Redis. Redis data persists in the Terraform-managed url-shortener-tf-redis-data volume.

Use Docker Compose or Terraform for this stack, not both on the same host port at the same time. The backend publishes the configurable host port (default 8000); Redis has no published port.

## Variables

| Variable | Default | Description |
| --- | --- | --- |
| docker_host | npipe:////.//pipe//docker_engine | Docker Engine endpoint |
| backend_image | url-shortener-backend:dev | Existing local backend image |
| redis_image | redis:7-alpine | Tagged Redis image used by the stack |
| backend_port | 8000 | Host port mapped to backend port 8000 |

The example values are in terraform.tfvars.example. Copy it to terraform.tfvars only when you want to override defaults. It contains no credentials. Local state is ignored by Git and may contain infrastructure data.

## Outputs

| Output | Description |
| --- | --- |
| backend_url | Local backend URL |
| backend_container_name | Terraform backend container name |
| redis_container_name | Terraform Redis container name |
| redis_volume_name | Persistent Redis volume name |
| network_name | Dedicated Docker network name |

## PowerShell workflow

Run from the repository root:

~~~powershell
terraform -chdir=infra/terraform init
.\scripts\dev.ps1 tf-fmt
.\scripts\dev.ps1 tf-validate
.\scripts\dev.ps1 tf-plan
.\scripts\dev.ps1 tf-apply
~~~

The backend image can be built with docker build -t url-shortener-backend:dev backend. Applying requires reviewing the plan first. The tf-destroy command prints a destroy plan and asks for the exact confirmation DESTROY before applying it. Destroy removes the Terraform-managed containers, network, and Redis volume, including its persisted data.

Terraform state is local for this portfolio environment. Never commit state, plan files, or local terraform.tfvars files. The checked-in provider lock file pins the selected provider build.