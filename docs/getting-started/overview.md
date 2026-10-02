# Project Overview & Engineering Principles

# AGENTS.md

# URL Shortener & Analytics Platform

## 1. Project Identity

Project name:

    url-shortener-platform

Naming conventions:

- Repository: `url-shortener-platform`
- Root folder: `url-shortener-platform/`
- Backend Docker image: `url-shortener-backend`
- Frontend Docker image: `url-shortener-frontend`
- Terraform infrastructure name: `url-shortener-infrastructure`

Use these names consistently across:

- repository configuration
- directory structure
- Docker configuration
- Docker image names
- Terraform resources
- CI/CD workflows
- documentation
- local development commands

Do not introduce alternative project names unless there is a concrete technical reason.

---

## 2. Project Overview

This repository contains a production-oriented URL Shortener & Analytics Platform.

The project is intentionally designed as a portfolio-grade engineering system rather than a minimal CRUD application.

The implementation should demonstrate practical experience with:

- backend development
- frontend development
- API design
- automated testing
- containerization
- infrastructure as code
- CI/CD
- observability
- security scanning
- load testing
- failure testing
- recovery procedures
- technical documentation

The primary engineering goal is to build a system that is:

- simple enough to understand and maintain
- structured enough to demonstrate professional engineering practices
- observable enough to diagnose failures
- testable enough to support confident changes
- containerized and reproducible
- automated through CI/CD
- deployable through Terraform
- suitable for technical portfolio presentation

Do not introduce unnecessary complexity merely to make the architecture appear sophisticated.

Prefer clear engineering decisions over excessive abstraction.

---

## 3. Core Engineering Principles

### 3.1 Correctness First

The application must behave correctly before optimization or additional features are introduced.

Do not sacrifice correctness for:

- premature optimization
- unnecessary abstractions
- shorter code
- clever implementations
- excessive framework features

Functional behavior and reliable tests take priority.

### 3.2 Explicit Over Clever

Prefer code that another developer can understand quickly.

Use:

- descriptive names
- explicit control flow
- small functions
- clear module boundaries
- typed interfaces where appropriate
- predictable error handling

Avoid:

- unnecessary metaprogramming
- deeply nested abstractions
- magic behavior
- duplicated business logic
- hidden global state

### 3.3 Production-Oriented, Not Enterprise-Theater

The project should demonstrate real engineering practices without pretending to be a massive distributed system.

Do not add:

- Kubernetes without a concrete requirement
- microservices without a concrete reason
- message queues without a concrete use case
- service meshes
- unnecessary databases
- excessive authentication infrastructure

The target architecture is a modular monorepo using FastAPI, Vue, Redis, Docker, Terraform, GitHub Actions, Prometheus, Grafana, Alertmanager, and Locust.

### 3.4 Security by Default

Security should be considered throughout the implementation.

At minimum:

- validate user input
- validate URLs
- validate short-code format
- avoid unsafe string interpolation
- avoid leaking internal exceptions
- keep secrets out of source control
- use environment variables for configuration
- scan dependencies
- scan container images
- validate CI/CD permissions
- use least-privilege GitHub Actions permissions where practical

Security controls should remain understandable and maintainable.

### 3.5 Observable by Default

Important application behavior should be measurable.

The system should expose:

- application health
- readiness status
- HTTP request metrics
- latency information
- request counts
- error information
- redirect activity
- short URL creation activity
- operational signals where practical

Metrics should be useful for both debugging and portfolio demonstration.

---

