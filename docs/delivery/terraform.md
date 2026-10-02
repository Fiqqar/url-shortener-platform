# Phase 2: Terraform

## 75. Terraform Structure

Terraform should live under:

    infra/terraform/

Suggested structure:

    infra/terraform/
    ├── versions.tf
    ├── providers.tf
    ├── variables.tf
    ├── main.tf
    ├── outputs.tf
    └── README.md

If the configuration grows substantially, split resources into additional files by responsibility.

Do not create many tiny Terraform files without a meaningful organizational benefit.

---

## 76. Terraform Provider

The initial infrastructure uses the Docker Terraform provider.

The provider should be configured explicitly.

The Terraform configuration should declare:

- required Terraform version
- required provider
- provider version constraints
- provider configuration

Do not depend on an implicitly selected provider version.

Provider versions should be constrained for reproducibility.

---

## 77. Terraform Resources

Terraform may manage:

- Docker network
- backend container
- frontend container
- Redis container
- Redis volume
- Prometheus container
- Grafana container
- Alertmanager container
- monitoring volumes where required

The exact resource list should reflect the final Compose architecture.

Avoid creating resources that are not actually required.

---

## 78. Terraform Variables

Infrastructure configuration should use variables for environment-specific values.

Potential variables:

    project_name
    environment
    backend_image
    frontend_image
    backend_port
    frontend_port
    redis_port
    prometheus_port
    grafana_port
    alertmanager_port

Use sensible defaults for local development where appropriate.

Do not store secrets as hardcoded Terraform values.

---

## 79. Terraform Naming

Terraform resources should use clear logical names.

Example:

    docker_network.app
    docker_container.backend
    docker_container.frontend
    docker_container.redis

Resource names should describe their infrastructure role.

The infrastructure naming convention should remain consistent with:

    url-shortener-infrastructure

---

## 80. Terraform Network

Create a dedicated Docker network.

Conceptual:

    url-shortener-network

Containers that require application communication should attach to this network.

The backend should reach Redis using the Terraform-managed container/service name.

Monitoring containers should be attached to the appropriate network so Prometheus can scrape the backend.

---

## 81. Terraform Dependencies

Terraform dependencies should be represented through resource references wherever possible.

Avoid unnecessary explicit `depends_on`.

Prefer:

    resource reference
        |
        v
    implicit dependency

Use explicit dependencies only when Terraform cannot infer the correct relationship.

---

## 82. Terraform Volumes

Persistent data should be represented using Docker volumes managed by Terraform when Terraform owns the infrastructure.

Potential volumes:

    url-shortener-redis-data
    url-shortener-prometheus-data
    url-shortener-grafana-data

Persistence requirements should be documented.

Do not persist ephemeral build artifacts.

---

## 83. Compose vs Terraform

Docker Compose and Terraform may describe overlapping local infrastructure, but their purposes must remain clear.

Compose is primarily for:

- fast local development
- convenient multi-container startup
- developer testing

Terraform is primarily for:

- declarative infrastructure
- reproducibility
- explicit infrastructure resources
- demonstrating infrastructure-as-code practices

Do not require developers to run both Compose and Terraform simultaneously for the same stack unless there is a concrete reason.

The README must explain which workflow is intended for which purpose.

---

## 84. Terraform Commands

The project should support:

    terraform fmt
    terraform init
    terraform validate
    terraform plan
    terraform apply

Destroying infrastructure should require an explicit command.

Do not hide destructive Terraform operations behind normal Makefile targets.

Example:

    make terraform-destroy

should require deliberate user action and be clearly documented as destructive.

---

## 85. Terraform State

Terraform state must not be committed to Git.

Ignore:

    terraform.tfstate
    terraform.tfstate.*
    .terraform/

If a remote backend is introduced later, its security and locking requirements must be documented.

For the initial local portfolio environment, local state may be acceptable.

---

## 86. Infrastructure Validation

Before applying Terraform:

    terraform fmt -check
    terraform validate
    terraform plan

CI should run formatting and validation.

A pull request should not silently modify infrastructure without showing the resulting Terraform plan when infrastructure changes are present.

---

## 87. Infrastructure Documentation

`infra/terraform/README.md` should document:

- required Terraform version
- required provider
- variables
- outputs
- initialization
- validation
- plan
- apply
- destroy
- local infrastructure assumptions

The root README should link to this documentation.

---

## 88. Definition of Done for Phase 2

Phase 2 is complete when:

- backend builds successfully as `url-shortener-backend`
- frontend builds successfully as `url-shortener-frontend`
- containers start successfully
- Redis is reachable by the backend
- health checks work
- Docker Compose can start the local stack
- Docker images contain no accidental secrets
- Docker images pass the configured security scan or documented exceptions exist
- Terraform initializes successfully
- Terraform formatting passes
- Terraform validation passes
- Terraform plan succeeds
- Terraform resources use consistent naming
- persistent data uses explicit volumes where required
- infrastructure documentation is complete

Only after this phase is stable should CI/CD automation become the primary focus.


