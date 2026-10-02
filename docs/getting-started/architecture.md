# Technology Stack, Repository Structure & Architecture

## 4. Technology Stack

### Backend

- Python 3.12+
- FastAPI
- Uvicorn
- Redis
- Pydantic
- Pydantic Settings
- pytest
- pytest-asyncio where required
- Ruff
- pip-audit
- prometheus-fastapi-instrumentator

### Frontend

- Vue 3
- Vite
- TypeScript
- Vitest
- Vue Test Utils
- npm audit

### Infrastructure

- Docker
- Docker Compose
- Terraform
- Terraform Docker Provider

### CI/CD

- GitHub Actions
- automated backend tests
- automated frontend tests
- linting
- dependency security scanning
- container security scanning
- infrastructure validation

### Observability

- Prometheus
- Grafana
- Alertmanager

### Load Testing

- Locust

### Security

- Ruff
- pip-audit
- npm audit
- Trivy
- Dependabot
- secure GitHub Actions configuration

---

## 5. Repository Structure

The repository uses a monorepo layout.

Target structure:

    url-shortener-platform/
    ├── backend/
    │   ├── app/
    │   │   ├── api/
    │   │   ├── core/
    │   │   ├── models/
    │   │   ├── schemas/
    │   │   ├── services/
    │   │   ├── repositories/
    │   │   ├── observability/
    │   │   └── main.py
    │   ├── tests/
    │   ├── requirements.txt
    │   └── pyproject.toml
    │
    ├── frontend/
    │   ├── src/
    │   │   ├── components/
    │   │   ├── views/
    │   │   ├── services/
    │   │   ├── composables/
    │   │   ├── types/
    │   │   └── router/
    │   ├── tests/
    │   ├── package.json
    │   ├── vite.config.ts
    │   └── tsconfig.json
    │
    ├── infra/
    │   ├── terraform/
    │   │   ├── main.tf
    │   │   ├── variables.tf
    │   │   ├── outputs.tf
    │   │   ├── providers.tf
    │   │   └── versions.tf
    │   └── docker/
    │       └── ...
    │
    ├── monitoring/
    │   ├── prometheus/
    │   │   ├── prometheus.yml
    │   │   └── rules/
    │   ├── grafana/
    │   │   ├── dashboards/
    │   │   └── provisioning/
    │   └── alertmanager/
    │       └── alertmanager.yml
    │
    ├── loadtest/
    │   ├── locustfile.py
    │   └── README.md
    │
    ├── docker-compose.yml
    ├── Makefile
    ├── .env.example
    ├── .gitignore
    ├── .dockerignore
    ├── AGENTS.md
    └── README.md

The exact structure may evolve during implementation, but responsibilities must remain clearly separated.

---

## 6. High-Level Architecture

The system consists of the following major components:

    Browser
       |
       v
    Vue 3 Frontend
       |
       | HTTP/JSON
       v
    FastAPI Backend
       |
       +----------------+
       |                |
       v                v
    Redis           Prometheus
       |                |
       |                v
       |             Grafana
       |
       v
    Short URL / Analytics Data

Alerting path:

    Prometheus
       |
       v
    Alertmanager
       |
       v
    Notification Target

Load-testing path:

    Locust
       |
       v
    FastAPI Backend
       |
       v
    Redis

The backend is the central application service.

The frontend communicates with the backend through documented HTTP APIs.

Redis is the primary persistence mechanism for the initial version.

Prometheus collects operational metrics from the backend.

Grafana visualizes Prometheus metrics.

Alertmanager handles alert routing.

Locust generates controlled traffic for performance testing.

---

## 7. Main Application Flow

### 7.1 Create Short URL

Expected flow:

1. User enters a destination URL in the frontend.
2. Frontend performs basic input validation.
3. Frontend sends a POST request to the backend.
4. Backend validates the request using Pydantic.
5. Backend generates a unique short code.
6. Backend stores the URL mapping in Redis.
7. Backend returns the short URL and metadata.
8. Frontend displays the generated short URL.

Conceptual request:

    POST /api/v1/urls

    {
      "url": "https://example.com/some/long/path"
    }

Conceptual response:

    {
      "code": "aB3xY7",
      "short_url": "http://localhost:8000/aB3xY7",
      "target_url": "https://example.com/some/long/path"
    }

The exact response fields may evolve, but the API contract must remain consistent and documented.

---

## 8. Redirect Flow

When a user visits a short URL:

    GET /{code}

The backend should:

1. Validate the code format.
2. Look up the corresponding target URL in Redis.
3. Record the redirect event or increment the relevant analytics counter.
4. Return an HTTP redirect to the target URL.

If the code does not exist:

    HTTP 404

The response must not expose internal Redis errors or implementation details.

Redirect handling should remain lightweight because it is expected to be one of the highest-frequency application paths.

---

## 9. Analytics Concept

The initial analytics implementation should focus on useful and simple metrics rather than a complex event-processing system.

At minimum, the system should be able to track:

- total redirects
- redirects per short code
- URL creation count
- HTTP request counts
- HTTP error counts
- request latency

Analytics data may initially be stored in Redis.

Do not introduce a relational database unless a concrete requirement emerges.

Future analytics capabilities may include:

- timestamps
- referrer information
- user-agent categories
- geographic approximation
- unique visitor estimation

These are future extensions and must not complicate the initial implementation.

---

## 10. API Versioning

Public application endpoints should use an explicit API prefix where appropriate.

Preferred pattern:

    /api/v1/...

Examples:

    POST /api/v1/urls
    GET  /api/v1/urls/{code}
    GET  /api/v1/urls/{code}/analytics

The redirect endpoint may remain outside the API namespace:

    GET /{code}

Health endpoints:

    GET /health
    GET /ready

Metrics endpoint:

    GET /metrics

The exact endpoint set may evolve, but API responsibilities must remain clearly separated from redirect behavior.

---

## 11. Initial Implementation Priorities

Implementation should proceed in the following order:

1. Backend application
2. Backend tests
3. Frontend application
4. Frontend tests
5. Local Docker environment
6. Terraform infrastructure
7. CI/CD
8. Prometheus
9. Grafana
10. Alertmanager
11. Locust load testing
12. Failure injection and recovery testing
13. Documentation and portfolio polish

Do not start infrastructure work before the application has a stable local development path.

Do not add observability dashboards before the underlying application metrics are reliable.

Do not perform load testing before functional tests pass.


