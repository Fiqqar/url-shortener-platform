# Phase 2: Dockerization

# Part 4: Containerization & Infrastructure as Code

## 60. Phase 2 - Dockerization

After the application works locally and its tests pass, containerize the application.

Phase 2 goals:

- create backend Docker image
- create frontend Docker image
- create local Docker Compose environment
- containerize Redis
- containerize Prometheus
- containerize Grafana
- containerize Alertmanager
- establish reproducible local infrastructure
- prepare infrastructure for Terraform management

Containerization must not change application behavior.

---

## 61. Docker Responsibilities

Docker is responsible for:

- packaging applications
- defining runtime environments
- installing dependencies
- exposing application ports
- defining container startup commands
- creating reproducible application images
- running services locally

Dockerfiles should contain only what is required to build and run the respective application.

Do not place infrastructure provisioning logic inside Dockerfiles.

---

## 62. Terraform Responsibilities

Terraform is responsible for:

- declaring infrastructure resources
- managing Docker resources where the Docker provider is used
- managing networks
- managing containers
- managing persistent volumes
- expressing infrastructure dependencies
- providing reproducible infrastructure configuration

Terraform should not replace application Dockerfiles.

The separation should remain:

    Dockerfile
        |
        +--> How the application is packaged

    Terraform
        |
        +--> What infrastructure is created

---

## 63. Backend Dockerfile

Create a dedicated backend Dockerfile.

Expected properties:

- use an appropriate Python base image
- install only required runtime dependencies
- avoid unnecessary build tools in the final image
- run as a non-root user where practical
- expose the application port
- use an explicit startup command

The backend container should start FastAPI through Uvicorn.

Conceptual command:

    uvicorn app.main:app --host 0.0.0.0 --port 8000

The final command must match the actual application structure.

---

## 64. Backend Image Optimization

Use Docker layer caching effectively.

Place relatively stable dependency installation steps before frequently changing source code.

Do not copy unnecessary files into the image.

Use `.dockerignore`.

Exclude items such as:

- `.git`
- `.venv`
- `__pycache__`
- pytest caches
- local environment files
- editor configuration
- test artifacts

Never copy real `.env` files containing secrets into an image.

---

## 65. Frontend Dockerfile

Create a dedicated frontend Dockerfile.

A multi-stage build is preferred.

Conceptual stages:

    Node build stage
        |
        v
    Production static assets
        |
        v
    Lightweight runtime image

The final image should contain only what is required to serve the built frontend.

Do not ship the complete Node development environment in the production runtime image unless there is a concrete reason.

---

## 66. Frontend Runtime Configuration

Frontend configuration must account for the fact that Vite environment variables are generally resolved during the build process.

Do not assume backend URLs can always be changed after the frontend image has been built.

Choose one clear strategy and document it.

Possible strategies include:

- build-time API base URL
- reverse proxy
- runtime configuration file

For the initial project, prefer the simplest reliable strategy.

---

## 67. Redis Container

Redis should run as a separate service.

Development Docker Compose should provide Redis automatically.

The backend should connect using the Docker service name rather than `localhost` when running inside Compose.

Example conceptual configuration:

    REDIS_HOST=redis
    REDIS_PORT=6379

The host-side development configuration may use:

    REDIS_HOST=localhost

Do not hardcode Docker-specific connection values into application code.

---

## 68. Docker Compose

Docker Compose should provide a complete local stack.

Initial services:

    backend
    frontend
    redis

Observability services may be added later:

    prometheus
    grafana
    alertmanager

Load testing should normally run separately rather than being required for every normal application startup.

---

## 69. Docker Compose Networking

All application services that need to communicate should share an internal Docker network.

Conceptual network:

    url-shortener-network

Service-to-service communication should use Compose service names.

Example:

    backend -> redis:6379

Do not use container IP addresses.

Container IPs are ephemeral and should never be hardcoded.

---

## 70. Docker Compose Ports

Only expose ports that are required by the developer.

Example conceptual mapping:

    frontend: 3000
    backend: 8000
    redis: 6379
    prometheus: 9090
    grafana: 3001
    alertmanager: 9093

Actual frontend ports may differ depending on the chosen production/static server.

Do not expose internal-only services unnecessarily.

---

## 71. Health Checks

Important services should have health checks.

Backend health check:

    GET /health

Backend readiness check:

    GET /ready

Redis health check may use a Redis ping operation.

Health checks should be lightweight.

Compose dependencies should use health status where appropriate rather than assuming that container startup means service readiness.

---

## 72. Persistent Storage

Redis data should use a named Docker volume if persistence is required.

Conceptual:

    redis-data

Monitoring services may also use volumes if persistence is desired.

Do not bind-mount arbitrary developer filesystem paths unless necessary.

Named volumes provide a more portable local setup.

---

## 73. Docker Security

Container images should follow basic hardening practices.

Where practical:

- run application processes as non-root
- minimize installed packages
- use trusted base images
- keep dependencies updated
- scan images with Trivy
- avoid embedding secrets
- use read-only filesystem options where practical
- drop unnecessary Linux capabilities where practical

Do not add security flags that break the application without testing them.

---

## 74. Docker Image Naming

Use the project naming convention:

    url-shortener-backend

and:

    url-shortener-frontend

If tags are used, prefer explicit versioning or commit-based tags in CI.

Avoid relying exclusively on:

    latest

for deployment or release identification.

---

