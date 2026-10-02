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


# Part 2: Backend Architecture & Data Model

## 12. API Contract

The backend API must use explicit request and response schemas.

FastAPI route handlers should not contain large amounts of business logic.

Prefer the following separation:

    API Router
        |
        v
    Service Layer
        |
        v
    Repository Layer
        |
        v
    Redis

### 12.1 Create URL

Endpoint:

    POST /api/v1/urls

Request:

    {
      "url": "https://example.com/some/long/path"
    }

Responsibilities:

- validate the URL
- generate a unique short code
- store the mapping
- initialize analytics data
- return the created resource

Expected success status:

    201 Created

Possible client errors:

    400 Bad Request
    422 Unprocessable Entity

The API should return structured JSON error responses.

### 12.2 Get URL Information

Endpoint:

    GET /api/v1/urls/{code}

Purpose:

Return metadata about a shortened URL without performing a browser redirect.

Possible response:

    {
      "code": "aB3xY7",
      "short_url": "http://localhost:8000/aB3xY7",
      "target_url": "https://example.com/some/long/path",
      "clicks": 42
    }

If the short code does not exist:

    404 Not Found

### 12.3 URL Analytics

Endpoint:

    GET /api/v1/urls/{code}/analytics

Purpose:

Return analytics associated with a shortened URL.

The initial implementation should remain simple.

Possible response:

    {
      "code": "aB3xY7",
      "clicks": 42
    }

Additional analytics fields may be added later.

### 12.4 Redirect

Endpoint:

    GET /{code}

Purpose:

Redirect the client to the target URL.

Success:

    3xx redirect

Missing code:

    404 Not Found

Invalid code:

    400 Bad Request

Internal infrastructure failures should return a generic server error rather than exposing implementation details.

### 12.5 Health

Endpoint:

    GET /health

Purpose:

Determine whether the application process is alive.

The liveness endpoint should not perform expensive operations.

Expected response:

    {
      "status": "ok"
    }

### 12.6 Readiness

Endpoint:

    GET /ready

Purpose:

Determine whether the application can serve traffic.

The readiness check may verify Redis connectivity.

Possible response:

    {
      "status": "ready"
    }

If required dependencies are unavailable:

    503 Service Unavailable

---

## 13. Short Code Generation

Short codes must be:

- URL-safe
- compact
- deterministic in uniqueness
- easy to validate
- generated without relying on random collision handling as the primary mechanism

A preferred initial approach is a Redis-backed numeric sequence combined with a Base62 encoder.

Conceptual flow:

    Redis INCR
        |
        v
    Numeric ID
        |
        v
    Base62 encoding
        |
        v
    Short code

Example:

    1       -> 1
    10      -> A
    61      -> z
    62      -> 10

The exact alphabet should be defined centrally.

For example:

    0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

Do not duplicate the alphabet across multiple modules.

The encoding function should be deterministic and independently unit tested.

### 13.1 Collision Handling

The preferred design avoids collisions by using a monotonic Redis counter.

Do not use:

    random string -> check -> retry

as the primary generation mechanism unless a later requirement specifically calls for it.

The counter operation should be atomic.

Redis `INCR` provides the required atomic increment behavior.

---

## 14. Redis Data Model

Redis is the initial persistence layer.

The data model should remain explicit and documented.

Suggested keys:

    url:{code}
    analytics:{code}:clicks
    meta:urls:sequence

Example:

    url:aB3xY7

Value:

    https://example.com/some/long/path

Counter:

    analytics:aB3xY7:clicks

Value:

    42

Global sequence:

    meta:urls:sequence

Value:

    12345

The exact representation may use Redis strings or hashes depending on implementation needs.

Do not introduce complex Redis structures without a clear benefit.

---

## 15. Redis Atomicity

Short-code generation must use an atomic operation.

Preferred sequence:

    INCR meta:urls:sequence
        |
        v
    Encode resulting integer
        |
        v
    SET url:{code}

The system must not rely on application-level locking for this operation.

Tests should verify that concurrent creation does not produce duplicate codes.

If concurrency tests are introduced, they should focus on observable correctness rather than attempting to prove Redis internals.

---

## 16. URL Storage

The minimum stored URL mapping must contain the destination URL.

Example:

    url:aB3xY7 -> https://example.com

If metadata is required, use a structured representation.

Potential fields:

- target URL
- created timestamp
- click count
- optional expiration timestamp

Do not store unnecessary duplicated information.

The canonical destination URL should have one clear source of truth.

---

## 17. Optional URL Expiration

TTL support may be implemented as an optional feature.

If implemented:

- expiration must be explicit
- TTL values must be validated
- expired URLs must behave as not found
- analytics behavior after expiration must be documented

Do not make TTL part of the critical path unless it is required by the final product specification.

A simple Redis TTL is preferred over building a custom expiration scheduler.

---

## 18. Backend Module Responsibilities

### `app/main.py`

Responsibilities:

- create the FastAPI application
- register routers
- configure middleware
- configure observability
- expose health/readiness/metrics endpoints

Avoid putting business logic here.

### `app/api/`

Responsibilities:

- HTTP routing
- request parsing
- response serialization
- dependency injection
- HTTP-specific error handling

Routers should remain thin.

### `app/schemas/`

Responsibilities:

- Pydantic request models
- Pydantic response models
- API validation schemas

Schemas should represent API contracts rather than Redis implementation details.

### `app/models/`

Responsibilities:

Represent internal application/domain models when useful.

Do not create models merely for the sake of having a model directory.

### `app/services/`

Responsibilities:

- URL creation
- short-code generation orchestration
- redirect lookup
- analytics operations
- business rules

Services should not depend directly on FastAPI request objects.

### `app/repositories/`

Responsibilities:

- Redis access
- key construction
- persistence operations
- atomic operations
- Redis-specific behavior

The service layer should not contain raw Redis commands when those commands can be encapsulated in a repository.

### `app/core/`

Responsibilities:

- configuration
- application constants
- shared exceptions
- security-related configuration
- common utilities

Keep this directory small.

### `app/observability/`

Responsibilities:

- application metrics
- custom Prometheus metrics
- instrumentation helpers
- logging configuration where appropriate

Do not mix business logic into observability modules.

---

## 19. Configuration

Configuration must come from environment variables or a configuration file loaded from environment variables.

Use Pydantic Settings or an equivalent typed configuration system.

Potential configuration values:

    APP_ENV=development
    APP_HOST=0.0.0.0
    APP_PORT=8000

    REDIS_HOST=redis
    REDIS_PORT=6379
    REDIS_DB=0

    BASE_URL=http://localhost:8000

    LOG_LEVEL=INFO

Configuration requirements:

- provide `.env.example`
- never commit real secrets
- provide safe local defaults where appropriate
- validate required production settings
- avoid hardcoding environment-specific values

The application must not depend on a developer-specific filesystem path.

---

## 20. Environment Separation

Support at least these conceptual environments:

- development
- test
- production

Development configuration may prioritize convenience.

Test configuration should be isolated from development data.

Production configuration must not use development credentials or unsafe debug settings.

Do not create separate application implementations for each environment.

Environment differences should primarily come from configuration.

---

## 21. Error Handling

The API should use predictable error responses.

Client errors should contain enough information for the frontend to understand what went wrong.

Internal exceptions should be logged server-side.

Do not expose:

- stack traces
- Redis connection details
- filesystem paths
- environment variables
- credentials
- internal implementation details

Example conceptual error:

    {
      "detail": "Short URL not found"
    }

For validation errors, use FastAPI/Pydantic's structured validation behavior unless a custom format is required.

---

## 22. Application Exceptions

Where useful, define domain-specific exceptions.

Examples:

    URLNotFoundError
    InvalidShortCodeError
    URLCreationError
    AnalyticsNotFoundError

These should be translated into HTTP responses at the API boundary.

Do not catch every exception and silently continue.

Unexpected exceptions should remain visible through logs and appropriate server error responses.

---

## 23. Logging

Application logs should be structured enough to diagnose problems.

At minimum, logs should include useful contextual information such as:

- timestamp
- log level
- event/message
- HTTP method
- request path
- status code
- request duration
- short code where relevant

Avoid logging sensitive information.

Do not log:

- secrets
- authorization credentials
- full environment configuration
- unnecessary personal information

Log levels should generally follow:

    DEBUG
    INFO
    WARNING
    ERROR
    CRITICAL

Development may use more verbose logging than production.

---

## 24. Request Correlation

If request correlation is implemented, use a request ID.

The request ID may be:

- accepted from a trusted incoming header, or
- generated by the application

The ID should appear in relevant logs.

Do not rely on request IDs as an authentication mechanism.

This feature is optional for the first implementation but recommended if it can be implemented without unnecessary complexity.

---

## 25. Redirect Safety

The URL shortener accepts user-controlled destination URLs.

The backend must validate the destination URL before storing it.

At minimum:

- require a valid URL structure
- require an allowed scheme
- reject malformed URLs
- avoid accepting arbitrary unsupported protocols

The initial implementation should normally allow:

    http
    https

Do not allow schemes such as:

    javascript:
    data:
    file:

unless there is an explicit and justified requirement.

Validation must happen server-side even if the frontend performs validation.

---

## 26. Backend Testing Boundary

Backend tests should verify behavior at multiple levels.

Unit tests should cover:

- Base62 encoding
- URL validation
- short-code validation
- service logic
- error conditions

Repository tests should cover:

- Redis reads
- Redis writes
- atomic sequence generation
- analytics counters

API tests should cover:

- successful URL creation
- invalid URLs
- missing short codes
- redirect behavior
- analytics retrieval
- health endpoint
- readiness endpoint
- validation errors

Integration tests should verify that the major components work together.

Tests should avoid depending on external internet services.

---

## 27. Backend Dependency Principles

Keep runtime dependencies minimal.

Before adding a package, determine whether:

1. the standard library is sufficient
2. an existing dependency already provides the required capability
3. the dependency is actively maintained
4. the dependency introduces unnecessary security or maintenance risk

Every dependency should have a clear reason to exist.

Pin or constrain dependencies appropriately for reproducible CI builds.

Run dependency auditing as part of the CI pipeline.


# Part 3: Application Development & Testing

## 28. Phase 1 - Application Development

Phase 1 establishes a complete local application before infrastructure automation is introduced.

The expected result is a working URL shortener that can be run locally and tested automatically.

Phase 1 goals:

- implement FastAPI backend
- implement Redis persistence
- implement short-code generation
- implement redirect behavior
- implement analytics
- implement Vue frontend
- implement API integration
- implement backend tests
- implement frontend tests
- establish local developer workflow

The application must be usable before moving to Docker, Terraform, CI/CD, and observability infrastructure.

---

## 29. Backend Implementation Order

Implement backend functionality in this order:

1. Project configuration
2. FastAPI application bootstrap
3. Configuration management
4. Redis connection management
5. Redis repository
6. Base62 encoder
7. URL validation
8. URL creation service
9. Redirect service
10. Analytics service
11. API schemas
12. API routers
13. Health endpoint
14. Readiness endpoint
15. Error handling
16. Logging
17. Prometheus instrumentation
18. Backend tests

Do not implement all functionality inside `main.py`.

Keep the application modular from the beginning.

---

## 30. Backend Application Bootstrap

The FastAPI application should:

- initialize the application
- load configuration
- initialize required dependencies
- register API routers
- register health endpoints
- configure middleware
- configure Prometheus instrumentation
- configure exception handlers where needed

Application startup and shutdown behavior should be explicit.

Redis connections should be managed through the application's lifecycle rather than creating a new connection for every request.

---

## 31. Redis Connection Management

Use a reusable Redis client or connection pool.

Do not create a new Redis connection for every HTTP request.

The Redis layer should support:

- connection initialization
- connectivity checking
- command execution
- clean shutdown where required

Connection failures should be handled predictably.

The readiness endpoint should be able to detect when Redis is unavailable.

---

## 32. Base62 Utility

The Base62 encoder should be implemented as a small isolated utility.

Requirements:

- deterministic output
- URL-safe characters
- support positive integer IDs
- reject invalid input where appropriate
- independently unit tested

Conceptual interface:

    encode_base62(value: int) -> str

The function should not know anything about Redis or HTTP.

Keep the algorithm independent from the application framework.

---

## 33. URL Validation

Destination URLs must be validated server-side.

The validation layer should verify:

- valid URL structure
- allowed scheme
- presence of a usable host
- reasonable input length
- rejection of unsupported schemes

At minimum, allow:

    http
    https

Reject unsafe or unsupported schemes.

Validation errors should produce a client-facing 4xx response.

The frontend may perform additional validation for user experience, but backend validation remains authoritative.

---

## 34. URL Creation Service

The URL creation service should coordinate:

1. validation
2. atomic sequence generation
3. Base62 encoding
4. Redis persistence
5. analytics initialization if required
6. response construction

Conceptual flow:

    create_url(target_url)
        |
        +--> validate URL
        |
        +--> INCR sequence
        |
        +--> encode ID
        |
        +--> store mapping
        |
        +--> initialize analytics
        |
        +--> return result

The service must not depend on Vue or frontend-specific concepts.

---

## 35. Redirect Service

The redirect service should:

1. validate the short code
2. retrieve the target URL
3. handle missing URLs
4. increment analytics
5. return the destination URL

Analytics updates should not corrupt redirect behavior.

If analytics tracking fails, the system should have a clearly defined policy.

The initial implementation may treat analytics failure as an application error if consistency is prioritized, or isolate it if redirect availability is prioritized.

The chosen behavior must be documented and tested.

---

## 36. Analytics Service

The analytics service should provide a minimal interface.

Potential operations:

    increment_clicks(code)
    get_click_count(code)

The service should hide Redis key construction from API routes.

The initial analytics model can use a simple counter.

Do not build a full event pipeline for the initial version.

---

## 37. API Router Design

Use separate routers for logically different responsibilities.

Suggested structure:

    app/api/
    ├── __init__.py
    ├── dependencies.py
    ├── health.py
    └── urls.py

Potential route grouping:

### URL routes

    POST /api/v1/urls
    GET /api/v1/urls/{code}
    GET /api/v1/urls/{code}/analytics

### Redirect

    GET /{code}

### Health

    GET /health
    GET /ready

### Metrics

    GET /metrics

Keep route handlers short.

A route handler should primarily:

- receive input
- invoke the appropriate service
- translate the result into an HTTP response

Business logic belongs in services.

---

## 38. Dependency Injection

Use FastAPI dependency injection for shared application resources where appropriate.

Potential dependencies:

- Redis repository
- configuration
- services
- request context

Avoid excessive dependency nesting.

The dependency graph should remain easy to understand.

---

## 39. Frontend Implementation

The Vue frontend should provide a simple user interface for the URL shortener.

Initial functionality:

- URL input
- client-side validation
- submit action
- generated short URL display
- copy-to-clipboard action
- basic error display
- analytics lookup
- loading states

The frontend should prioritize usability and clarity over visual complexity.

---

## 40. Frontend Structure

Suggested structure:

    frontend/src/
    ├── components/
    │   ├── UrlForm.vue
    │   ├── ShortUrlResult.vue
    │   └── AnalyticsCard.vue
    │
    ├── views/
    │   ├── HomeView.vue
    │   └── AnalyticsView.vue
    │
    ├── services/
    │   └── api.ts
    │
    ├── composables/
    │   └── useUrlShortener.ts
    │
    ├── types/
    │   └── api.ts
    │
    ├── router/
    │   └── index.ts
    │
    ├── App.vue
    └── main.ts

The exact component structure may evolve.

Avoid creating a component for every trivial HTML element.

---

## 41. Frontend API Layer

All backend API communication should be centralized.

Do not scatter raw `fetch()` calls throughout Vue components.

Preferred pattern:

    Component
        |
        v
    Composable
        |
        v
    API Service
        |
        v
    FastAPI

The API service should handle:

- request construction
- base URL configuration
- JSON serialization
- response parsing
- API error handling

---

## 42. Frontend Types

Use TypeScript interfaces or types for API responses.

Example:

    interface CreateUrlRequest {
      url: string
    }

    interface CreateUrlResponse {
      code: string
      short_url: string
      target_url: string
    }

Types should reflect the backend API contract.

Avoid using `any` for API data unless there is a documented reason.

---

## 43. Frontend State

Keep state close to the component or composable that owns it.

Typical state:

- input URL
- loading state
- generated result
- error message
- analytics data

Do not introduce a global state management library unless application complexity requires it.

For the initial application, Vue composables and component state should be sufficient.

---

## 44. Frontend Validation

Client-side validation should provide immediate feedback.

At minimum:

- reject empty input
- validate URL syntax
- prevent obviously unsupported protocols
- show useful validation messages

Client-side validation is for user experience.

It must never replace backend validation.

---

## 45. Frontend Error Handling

The frontend should distinguish between:

- validation errors
- API client errors
- not-found errors
- server errors
- network failures

Error messages should be understandable to users.

Do not display raw backend stack traces or internal exception messages.

---

## 46. Copy-to-Clipboard

The generated short URL should provide a convenient copy action.

The implementation should:

- use the browser Clipboard API where supported
- provide feedback after successful copying
- handle unsupported or failed clipboard operations gracefully

Do not make clipboard functionality a dependency for core URL creation.

---

## 47. Frontend Testing

Use Vitest and Vue Test Utils.

Tests should cover:

### Components

- URL form renders
- invalid input is rejected
- submit action works
- loading state is displayed
- result is displayed
- errors are displayed
- copy action behaves correctly

### API service

- successful request parsing
- API error handling
- network failure behavior

### Composables

- state transitions
- loading state
- successful creation
- error handling

Avoid relying on real backend services in unit tests.

Mock API requests where appropriate.

---

## 48. Backend Testing Strategy

Use pytest as the primary backend test framework.

Organize tests around behavior rather than implementation details.

Suggested structure:

    backend/tests/
    ├── unit/
    │   ├── test_base62.py
    │   ├── test_validation.py
    │   └── test_services.py
    │
    ├── integration/
    │   ├── test_repository.py
    │   └── test_redis.py
    │
    └── api/
        ├── test_urls.py
        ├── test_redirect.py
        └── test_health.py

The exact organization may evolve.

---

## 49. Unit Test Requirements

Unit tests should be deterministic and fast.

At minimum test:

### Base62

- zero or defined minimum behavior
- positive integers
- large values
- invalid values

### Validation

- valid HTTP URL
- valid HTTPS URL
- missing scheme
- unsupported scheme
- malformed URL
- excessive input length if a limit exists

### Services

- successful URL creation
- missing URL
- redirect lookup
- analytics increment
- analytics retrieval
- expected domain errors

---

## 50. API Integration Tests

API tests should exercise the FastAPI application through an HTTP test client.

Cover:

- POST URL success
- POST URL validation failure
- GET URL metadata
- redirect success
- redirect missing code
- analytics success
- analytics missing code
- health success
- readiness success
- readiness failure

The tests should verify:

- HTTP status codes
- response structure
- important response values
- expected side effects

Do not assert irrelevant implementation details.

---

## 51. Redis Integration Tests

Redis integration tests should run against an isolated Redis instance.

Possible approaches:

- local Redis service
- Docker Compose test dependency
- test container infrastructure if introduced later

Tests must not modify a developer's persistent production-like data.

At minimum verify:

- URL storage
- URL retrieval
- sequence increment
- analytics counter increment
- missing key behavior
- TTL behavior if implemented

---

## 52. Test Isolation

Tests must be isolated from one another.

Do not depend on:

- test execution order
- previously created short codes
- shared persistent state
- external websites
- developer-specific environment variables

Use fixtures for shared resources.

Clean or namespace Redis test data appropriately.

---

## 53. Test Naming

Test names should describe observable behavior.

Prefer:

    test_create_url_returns_generated_short_code

over:

    test_create_url_1

Prefer:

    test_redirect_returns_404_for_unknown_code

over:

    test_redirect_error

Tests should communicate intent without requiring the reader to inspect the implementation.

---

## 54. Test Coverage

Coverage is a signal, not the sole definition of quality.

Prioritize coverage of:

- business logic
- validation
- error paths
- persistence behavior
- API contracts
- critical redirect behavior

Do not write meaningless tests solely to increase a coverage percentage.

A reasonable coverage target may be established after the initial implementation and adjusted based on actual project complexity.

---

## 55. Code Quality

Python code should follow the configured Ruff rules.

Type hints should be used for public functions and important internal interfaces.

Keep functions focused.

Avoid premature abstractions.

Frontend TypeScript should use strict typing where practical.

Avoid suppressing type errors without a documented reason.

---

## 56. Local Development Workflow

The application should be easy to run locally.

The developer should be able to:

1. clone the repository
2. configure environment variables
3. install dependencies
4. start Redis
5. start backend
6. start frontend
7. run tests
8. run linting

The README must document the exact commands.

The local workflow should not depend on cloud infrastructure.

---

## 57. Makefile

The root Makefile should provide common developer commands.

Potential targets:

    make install
    make dev
    make backend
    make frontend
    make test
    make test-backend
    make test-frontend
    make lint
    make format
    make docker-up
    make docker-down
    make terraform-init
    make terraform-plan
    make terraform-apply
    make monitoring-up
    make load-test

Targets may evolve as implementation progresses.

Each target should perform one understandable task.

Avoid Makefile targets that silently perform destructive operations.

---

## 58. Development Commands

Example backend workflow:

    cd backend
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload --port 8000

Example frontend workflow:

    cd frontend
    npm install
    npm run dev

The exact commands may differ based on final project configuration.

The README and Makefile must remain synchronized with the actual implementation.

---

## 59. Definition of Done for Phase 1

Phase 1 is complete when:

- backend starts successfully
- frontend starts successfully
- Redis integration works
- users can create short URLs
- generated short URLs redirect correctly
- analytics counters work
- health endpoint works
- readiness endpoint works
- invalid URLs are rejected
- unknown short codes return appropriate errors
- backend tests pass
- frontend tests pass
- linting passes
- configuration is documented
- local setup is documented
- no secrets are committed

Only after these conditions are satisfied should the project proceed to the infrastructure and containerization phase.


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


# Part 5: CI/CD & Security Automation

## 89. Phase 3 - CI/CD Pipeline

The CI/CD pipeline should automatically verify application quality and infrastructure correctness.

The primary goals are:

- detect broken code early
- run automated tests
- enforce linting
- audit dependencies
- build container images
- scan container images
- validate Terraform
- provide reproducible checks
- prevent known security issues from silently reaching production

The pipeline should be fast enough for normal pull-request development.

Avoid running expensive operations when they are not relevant to the changed files.

---

## 90. GitHub Actions Structure

Workflows should live under:

    .github/workflows/

Suggested workflows:

    .github/
    └── workflows/
        ├── backend-ci.yml
        ├── frontend-ci.yml
        ├── infrastructure-ci.yml
        ├── security.yml
        └── release.yml

The exact number of workflows may be consolidated if doing so improves maintainability.

Do not create separate workflows merely to increase the apparent number of CI/CD components.

---

## 91. Pull Request Validation

Every pull request should trigger the appropriate automated checks.

Backend changes should trigger:

- dependency installation
- Ruff
- pytest
- pip-audit

Frontend changes should trigger:

- dependency installation
- TypeScript checks where configured
- Vitest
- npm audit

Infrastructure changes should trigger:

- Terraform formatting validation
- Terraform initialization
- Terraform validation
- Terraform plan where practical

Container-related changes should trigger:

- Docker build
- Trivy scan

The final workflow structure may use path filters to avoid unrelated jobs.

---

## 92. Backend CI

Backend CI should run in a supported Python environment.

Recommended sequence:

    checkout
        |
        v
    setup Python
        |
        v
    install dependencies
        |
        +--> Ruff
        |
        +--> pytest
        |
        +--> pip-audit

The workflow should fail if required checks fail.

Do not allow test failures to be ignored merely to keep CI green.

---

## 93. Backend Dependency Installation

Use a reproducible dependency installation process.

The project should maintain a clear distinction between:

- runtime dependencies
- development/test dependencies

Possible approaches:

- requirements files
- optional dependency groups
- a modern Python packaging configuration

The chosen method should be documented.

CI must install the same dependency definitions used by developers.

---

## 94. Ruff

Ruff should be used for Python linting and formatting enforcement.

CI should run checks in a non-mutating mode.

Conceptual commands:

    ruff check .
    ruff format --check .

The exact configuration should live in `pyproject.toml`.

Do not disable lint rules globally just to make the existing code pass.

If a rule is inappropriate for the project, configure the exception explicitly and document the reasoning when necessary.

---

## 95. Pytest

CI should run the complete backend test suite.

Conceptual:

    pytest

If coverage reporting is configured:

    pytest --cov=app --cov-report=term-missing

Tests should fail the job when an unexpected failure occurs.

Do not use `|| true` or equivalent behavior to hide test failures.

---

## 96. Backend Test Environment

Backend CI should provide required test dependencies.

If integration tests require Redis, CI should provide Redis through a service container.

Conceptual architecture:

    GitHub Actions Runner
        |
        +--> Python test environment
        |
        +--> Redis service
        |
        v
      pytest

The test environment must remain isolated from external production systems.

---

## 97. pip-audit

Run pip-audit against the project's Python dependency set.

The goal is to detect known vulnerabilities in installed or declared Python packages.

CI should make the security policy explicit.

If a vulnerability is temporarily accepted, document:

- affected package
- vulnerability
- reason for acceptance
- mitigation
- expected resolution

Do not permanently ignore vulnerabilities without justification.

---

## 98. Frontend CI

Frontend CI should run in a supported Node.js environment.

Recommended sequence:

    checkout
        |
        v
    setup Node.js
        |
        v
    npm ci
        |
        +--> type check
        |
        +--> Vitest
        |
        +--> build
        |
        +--> npm audit

Use `npm ci` in CI when a lockfile is available.

Do not use `npm install` as the default CI installation mechanism when reproducibility can be achieved through the lockfile.

---

## 99. Frontend Testing

Vitest should run the frontend test suite.

Conceptual:

    npm run test
    or
    npm run test:unit

The exact script should be defined in `package.json`.

Tests should cover critical user-facing behavior.

A frontend test failure should fail CI.

---

## 100. Frontend Build

CI should verify that the production frontend can build.

Conceptual:

    npm run build

This catches:

- TypeScript errors
- missing imports
- invalid Vite configuration
- broken production compilation
- unresolved dependencies

A successful unit-test run is not sufficient if the production build is broken.

---

## 101. npm audit

Run npm audit against the frontend dependency tree.

The severity policy should be explicit.

Do not blindly use an aggressive automatic fix command in CI because dependency upgrades can introduce breaking changes.

Prefer:

    npm audit

and review actionable vulnerabilities deliberately.

---

## 102. Infrastructure CI

Terraform validation should run whenever infrastructure changes are relevant.

Recommended sequence:

    terraform fmt -check
        |
        v
    terraform init
        |
        v
    terraform validate
        |
        v
    terraform plan

Terraform initialization should use a locked provider configuration when possible.

Do not commit generated `.terraform` directories.

---

## 103. Terraform Plan

For pull requests that modify infrastructure, produce a Terraform plan.

The plan should help reviewers understand infrastructure changes before merge.

The plan should not automatically apply changes to production.

Automatic apply should require an explicit deployment strategy and environment controls.

For the portfolio project, a manual or controlled apply process is acceptable.

---

## 104. Docker Build CI

Container builds should be tested in CI.

Build:

    url-shortener-backend

and:

    url-shortener-frontend

The image names should remain consistent with the project identity.

CI should fail if either production image cannot be built.

Do not require deployment merely to verify that a Docker image builds.

---

## 105. Docker Image Tags

Use immutable or traceable tags for CI artifacts.

Useful tag sources include:

- Git commit SHA
- Git tag
- release version

Example conceptual:

    url-shortener-backend:<commit-sha>
    url-shortener-frontend:<commit-sha>

Avoid using `latest` as the only release identifier.

If `latest` is published for convenience, it should not be the only way to identify the image.

---

## 106. Trivy

Trivy should scan built container images.

Scan both:

    url-shortener-backend

and:

    url-shortener-frontend

The security policy should define which severities fail CI.

A reasonable initial policy may fail on known HIGH or CRITICAL vulnerabilities when a fix is available.

False positives or accepted risks should be documented rather than silently ignored.

---

## 107. Container Security Scope

Trivy scanning should cover at least:

- OS packages
- application dependencies where supported
- known vulnerabilities

Do not assume that a successful Docker build means the image is secure.

Security scanning is an additional verification layer.

---

## 108. GitHub Actions Permissions

Workflows should explicitly define permissions.

Prefer the minimum required permissions.

For workflows that only need to read repository contents:

    permissions:
      contents: read

Additional permissions should be granted only when required.

Avoid:

    permissions: write-all

unless there is a specific documented requirement.

---

## 109. Secrets

Secrets must never be committed to Git.

Potential secrets may include:

- deployment credentials
- notification credentials
- API keys
- registry credentials
- cloud credentials

Use GitHub Actions Secrets or an appropriate secret-management mechanism.

Do not put secrets in:

- source code
- Dockerfiles
- Terraform variables committed to Git
- `.env`
- workflow YAML as plaintext

`.env.example` may contain placeholders but never real credentials.

---

## 110. GitHub Actions Pinning

Actions should use stable, intentional versions.

Where the project's security policy permits, pin third-party actions to immutable commit SHAs.

If tags are used for maintainability, keep them updated and review action changes.

Do not blindly copy arbitrary third-party workflow snippets into the repository.

---

## 111. Dependency Management

Use Dependabot for automated dependency update proposals.

Suggested configuration:

    .github/dependabot.yml

Monitor:

- pip dependencies
- npm dependencies
- GitHub Actions
- Docker-related dependencies where supported

Dependabot pull requests should still pass the project's normal CI checks.

Do not automatically merge every dependency update without validation.

---

## 112. Dependency Update Policy

Dependency updates should be reviewed based on:

- security impact
- compatibility
- changelog/release notes
- test results
- breaking changes

Security updates should receive appropriate priority.

Major version upgrades may require manual review.

Do not upgrade dependencies solely because a newer version exists if it creates unnecessary instability.

---

## 113. Security Workflow

A dedicated security workflow may run:

    Ruff
    pip-audit
    npm audit
    Trivy
    Terraform validation

The security workflow should complement, not duplicate excessively, the normal application CI.

If the same check already runs in another workflow, decide whether centralization or duplication provides greater reliability.

Avoid maintaining multiple contradictory security policies.

---

## 114. Workflow Concurrency

Use GitHub Actions concurrency where appropriate to avoid redundant runs.

For example, newer commits to the same pull request may cancel outdated in-progress CI runs.

Do not cancel workflows that perform irreversible deployment operations.

Concurrency behavior should be documented when it affects deployment.

---

## 115. CI Caching

Dependency caching may be enabled to reduce workflow time.

Potential caches:

- pip
- npm
- Docker build layers
- Terraform provider/plugin cache where appropriate

Caching must not compromise reproducibility.

If a cache becomes corrupted, CI should still be able to perform a clean installation.

---

## 116. CI Failure Behavior

CI should fail clearly when a required check fails.

Examples:

- lint failure
- unit test failure
- integration test failure
- frontend build failure
- Docker build failure
- Terraform validation failure
- security scan failure

Do not hide errors through:

    continue-on-error: true

unless the check is explicitly informational.

Informational security findings must be labeled as such.

---

## 117. Release Workflow

A release workflow may run when a version tag is pushed.

Conceptual flow:

    Git tag
       |
       v
    CI verification
       |
       v
    Build images
       |
       v
    Security scan
       |
       v
    Publish artifacts
       |
       v
    Create release metadata

Do not publish artifacts that have not passed the required verification stages.

The exact container registry may be selected later.

---

## 118. Release Versioning

Use a consistent versioning strategy.

Semantic Versioning may be used:

    MAJOR.MINOR.PATCH

Examples:

    0.1.0
    0.2.0
    1.0.0

Before version `1.0.0`, breaking changes may still occur, but they should be documented.

Git tags should correspond to release versions.

---

## 119. Branch Strategy

Keep Git branching simple.

Recommended:

    main
      |
      +--> feature/*
      +--> fix/*
      +--> chore/*
      +--> docs/*

The `main` branch should remain deployable or at least CI-green.

Avoid maintaining long-lived development branches without a concrete reason.

Pull requests should be preferred over direct pushes for meaningful changes.

---

## 120. Commit Strategy

Commits should be small enough to understand and review.

Prefer conventional commit-style messages where practical.

Examples:

    feat: add URL creation endpoint
    fix: handle missing short codes
    test: add redirect integration tests
    ci: add Trivy image scanning
    infra: add Redis Terraform resource
    docs: document local setup

Avoid giant commits that combine unrelated application, infrastructure, and documentation changes.

---

## 121. CI/CD Definition of Done

Phase 3 is complete when:

- backend CI runs automatically
- frontend CI runs automatically
- backend tests run in CI
- frontend tests run in CI
- production frontend build runs in CI
- Ruff runs in CI
- pip-audit runs in CI
- npm audit runs in CI
- Terraform formatting and validation run in CI
- Terraform plan can be generated
- Docker images build successfully
- Trivy scans application images
- GitHub Actions permissions are intentionally restricted
- Dependabot configuration exists
- secrets are excluded from source control
- failed required checks block successful CI
- release behavior is documented
- CI workflows are documented in the repository

The pipeline should provide meaningful confidence that code is ready for the next stage of deployment and observability work.


## 122. Phase 4 — Prometheus & Grafana Observability

Observability is part of the application design, not an afterthought.

The platform must expose enough telemetry to answer:

- Is the backend healthy?
- How much traffic is the backend receiving?
- How many requests are failing?
- How long do requests take?
- How many URLs are being created?
- How many redirects are occurring?
- Is Redis becoming unavailable or error-prone?
- Can an operator detect degradation before users report it?

The observability stack consists of:

- FastAPI application metrics
- Prometheus
- Grafana
- Alertmanager in the following phase
- Docker/container health information where appropriate

Monitoring failures must not become application failures.

## 123. Monitoring Directory Structure

The monitoring directory should follow this structure:

monitoring/
├── prometheus/
│   ├── prometheus.yml
│   └── rules/
│       ├── backend.yml
│       └── infrastructure.yml
├── grafana/
│   ├── dashboards/
│   │   └── url-shortener.json
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml
│       └── dashboards/
│           └── dashboard.yml
└── alertmanager/
    └── alertmanager.yml

Prometheus configuration belongs under:

monitoring/prometheus/

Grafana provisioning configuration belongs under:

monitoring/grafana/provisioning/

Dashboard JSON files belong under:

monitoring/grafana/dashboards/

Important Grafana configuration must be reproducible from repository files.

Do not manually configure the dashboard in the Grafana UI and treat that configuration as the source of truth.

## 124. FastAPI Metrics

The backend must expose Prometheus-compatible metrics.

Use:

prometheus-fastapi-instrumentator

for FastAPI HTTP instrumentation.

The application should initialize the instrumentator during FastAPI startup/bootstrap using the API supported by the installed library version.

The expected integration pattern is conceptually:

from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)

Do not blindly copy this snippet if the installed dependency version uses a different API.

The implementation must be verified against the actual installed package version.

The backend must expose:

/metrics

The endpoint must return Prometheus-compatible metrics.

The application must continue functioning if Prometheus is temporarily unavailable.

## 125. Instrumented HTTP Metrics

The FastAPI instrumentation should provide HTTP-level telemetry such as:

- request count
- request duration
- HTTP status information
- request method
- request handler/path information where supported
- in-progress requests where supported

Do not assume exact metric names from memory.

Metric names and labels must be verified against the actual output of:

curl http://localhost:<backend-port>/metrics

Documentation and Grafana queries must use the actual metric names produced by the installed version.

## 126. Custom Application Metrics

Default HTTP instrumentation is not enough.

The backend should expose application-level metrics for important business operations.

At minimum, provide metrics for:

- URL creation
- URL redirects
- analytics requests
- application errors
- Redis failures

Recommended conceptual metrics:

url_shortener_urls_created_total
url_shortener_redirects_total
url_shortener_analytics_requests_total
url_shortener_errors_total
url_shortener_redis_errors_total

Metric names may be adjusted to follow the naming conventions of the actual implementation.

Counters should use _total semantics where appropriate.

Custom metrics should be incremented at the service/business-logic layer rather than duplicated independently in every HTTP route.

For example:

- URL creation service increments the URL creation counter.
- Redirect service increments the redirect counter.
- Analytics service increments the analytics request counter.
- Infrastructure/database exception handling increments the relevant error counter.

This prevents the same business operation from being counted multiple times when several API routes call the same service.

## 127. Metric Labels

Labels must remain low-cardinality.

Acceptable examples:

method
status
route
operation
error_type

Avoid using unbounded values as labels.

Never use these as Prometheus labels:

- full URL
- short code
- user ID
- IP address
- User-Agent
- request ID
- arbitrary exception message

Do not create one time series per URL.

For example, this is unacceptable:

redirects_total{short_code="abc123"}

because the number of short codes can grow indefinitely.

Prefer:

redirects_total{operation="redirect"}

or another bounded label set.

High-cardinality metrics can cause memory growth and make Prometheus significantly more expensive to operate.

## 128. Histogram Usage

Latency should be represented using histogram metrics where practical.

The observability stack should support queries for:

- p50
- p95
- p99

request latency.

Do not calculate latency percentiles by averaging request durations.

Use Prometheus histogram functions such as:

histogram_quantile(...)

against the actual histogram bucket metric emitted by the installed instrumentation.

Grafana panels must use the real metric names from /metrics.

## 129. Prometheus Configuration

Create:

monitoring/prometheus/prometheus.yml

The configuration should define:

- global scrape interval
- evaluation interval
- backend scrape job
- rule files
- appropriate scrape timeout

The backend should be discoverable through the Docker Compose network.

Prefer service names over hardcoded container IP addresses.

Example conceptual target:

backend:<port>

Do not configure Prometheus against a dynamically assigned container IP.

The Prometheus scrape configuration must target:

/metrics

on the backend service.

## 130. Prometheus Scrape Configuration

The backend scrape job should have a clear name such as:

url-shortener-backend

Keep labels useful and bounded.

Recommended static labels may include:

service="url-shortener-backend"
environment="local"

Do not attach request-level or URL-level data to Prometheus target labels.

If multiple environments are introduced later, use environment-specific configuration rather than duplicating application logic.

## 131. Prometheus Rule Evaluation

Prometheus should load rule files from:

monitoring/prometheus/rules/

Keep alerting rules separate from the main Prometheus configuration.

Use descriptive filenames:

backend.yml
infrastructure.yml

Rules should be readable and independently reviewable.

Do not place dozens of unrelated rules into one large configuration file.

Each rule should contain:

- clear alert name
- expression
- duration where appropriate
- severity
- useful annotations
- concise description

The actual alert definitions will be expanded in the Alertmanager phase.

## 132. Grafana Provisioning

Grafana must be configured through provisioning files.

The Prometheus datasource should be automatically created from:

monitoring/grafana/provisioning/datasources/prometheus.yml

The dashboard provider should be configured from:

monitoring/grafana/provisioning/dashboards/dashboard.yml

Dashboards should load from:

monitoring/grafana/dashboards/

The goal is:

docker compose up

followed by Grafana startup should produce a usable dashboard without requiring manual configuration through the Grafana UI.

Do not rely on undocumented manual dashboard state.

## 133. Grafana Dashboard

Create one primary dashboard for the URL Shortener platform.

Suggested dashboard title:

URL Shortener Platform

The dashboard should prioritize operational information over visual decoration.

Recommended panels:

Traffic:
- requests per second
- request rate by route
- redirects per second
- URL creation rate

Reliability:
- HTTP 4xx rate
- HTTP 5xx rate
- application error rate
- Redis error rate

Latency:
- p50 latency
- p95 latency
- p99 latency

Application Operations:
- URLs created
- redirects
- analytics requests

Use counter rates for time-series views and cumulative counters where useful.

## 134. Grafana Dashboard Design Rules

The dashboard should be readable at a glance.

Recommended structure:

Row 1:
- Request Rate
- Error Rate
- P95 Latency

Row 2:
- Redirect Rate
- URL Creation Rate
- Analytics Request Rate

Row 3:
- P50 Latency
- P99 Latency
- Redis Errors

Row 4:
- Backend / Process Health

Exact layout may change based on available metrics.

Use meaningful panel titles.

Use units correctly:

- requests/sec
- seconds or milliseconds
- count
- percentage

Do not display raw Prometheus values without explaining what they represent.

## 135. PromQL Rules

PromQL queries should be written for operational meaning rather than simply exposing raw counters.

For counters, use functions such as:

rate(...)

or:

increase(...)

depending on the panel's purpose.

For latency histograms, use:

histogram_quantile(...)

with the appropriate bucket series.

Do not hardcode metric names before verifying the actual output of /metrics.

If the instrumentation library changes metric names, update Grafana queries accordingly.

## 136. Backend Metrics Verification

Before considering observability complete, manually verify:

GET /metrics

returns metrics successfully.

Then generate application traffic:

POST /api/v1/urls
GET /<short-code>
GET /api/v1/urls/<short-code>/analytics

After generating traffic, confirm that relevant counters change.

At minimum verify:

1. HTTP request metrics change.
2. URL creation metrics change.
3. Redirect metrics change.
4. Analytics metrics change.
5. Error metrics change when a controlled error is generated.
6. Grafana displays the resulting activity.
7. Prometheus successfully scrapes the backend.

## 137. Redis Observability

Redis health must be observable.

The application should expose Redis failures through application metrics when Redis operations fail.

At minimum distinguish, where reliably possible:

- Redis unavailable
- Redis operation error
- Redis timeout

Do not expose raw Redis exception strings as Prometheus labels.

Redis connectivity should also be represented in:

/health

and/or:

/ready

according to the semantics defined during backend implementation.

Readiness should fail when the application cannot perform dependencies required for normal operation.

Liveness should not necessarily fail merely because Redis is temporarily unavailable.

Do not conflate liveness with dependency readiness.

## 138. Health vs Readiness

Use:

/health

for basic application liveness.

Use:

/ready

for whether the service is ready to handle normal traffic.

Conceptually:

/health
    process is alive

/ready
    process is alive
    required dependencies are reachable

The exact dependency checks should match the application's actual startup/runtime requirements.

Do not perform unnecessarily expensive dependency checks on every liveness probe.

## 139. Monitoring Failure Isolation

Monitoring must not become a single point of failure.

If Prometheus is down:

backend continues serving requests

If Grafana is down:

backend continues serving requests

If Alertmanager is down:

backend continues serving requests
Prometheus continues collecting metrics

The application must not make synchronous calls to Grafana, Prometheus, or Alertmanager as part of normal request handling.

Metrics collection should remain lightweight and non-blocking from the perspective of normal API behavior.

## 140. Observability Local Development

Local development should support starting the observability stack through Docker Compose.

Expected architecture:

Browser
   |
Frontend
   |
Backend
   |
Redis

Prometheus ---> Backend /metrics
    |
    v
Grafana

Alertmanager will consume Prometheus alerts in the next phase.

Keep monitoring services on the same Docker network where required.

Do not expose every monitoring port publicly by default.

For local development, exposing Grafana and Prometheus to localhost is acceptable.

For production-like deployments, access should be restricted appropriately.

## 141. Observability Security

Do not expose sensitive application data through metrics.

Metrics must never contain:

- private URLs
- credentials
- API keys
- tokens
- cookies
- authorization headers
- request bodies
- raw IP addresses unless explicitly required and reviewed

Do not log or metricize secrets for debugging convenience.

Observability data is production data and must be treated accordingly.

## 142. Observability Documentation

The README should document:

- where /metrics is exposed
- how to access Prometheus locally
- how to access Grafana locally
- dashboard purpose
- how to verify scraping
- how to generate sample traffic
- where Prometheus rules are stored
- where Grafana dashboards are stored

Example local service URLs may be documented once actual Docker Compose ports are finalized.

Do not document ports that are not actually configured.

## 143. Phase 4 Definition of Done

Phase 4 is complete when:

- [ ] Backend exposes /metrics.
- [ ] prometheus-fastapi-instrumentator is used for FastAPI HTTP instrumentation.
- [ ] Prometheus successfully scrapes the backend.
- [ ] HTTP request metrics are visible.
- [ ] URL creation metrics are visible.
- [ ] Redirect metrics are visible.
- [ ] Analytics metrics are visible.
- [ ] Error metrics are visible.
- [ ] Redis failures are observable.
- [ ] Metrics use bounded labels.
- [ ] No raw URL/code/IP data is used as unbounded metric labels.
- [ ] Latency can be inspected at p50/p95/p99 where supported.
- [ ] Grafana datasource is provisioned automatically.
- [ ] Grafana dashboard is provisioned automatically.
- [ ] Dashboard shows traffic, reliability, latency, and application operations.
- [ ] Monitoring failures do not stop the backend.
- [ ] README documents the observability stack.
- [ ] Metrics have been manually verified with real application traffic.


## 144. Phase 5 — Alerting & Load Testing

The platform must not only collect metrics.

It must also:

- detect meaningful failures
- distinguish warning conditions from critical conditions
- route alerts through Alertmanager
- validate alert conditions
- generate controlled traffic
- measure application behavior under load
- verify recovery after failures

Alerting should be actionable.

Do not create alerts for every unusual metric change.

An alert should represent a condition that requires investigation or action.

## 145. Alerting Architecture

The monitoring architecture is:

Application
    |
    v
Prometheus
    |
    v
Alertmanager
    |
    v
Notification Target

Grafana is used for visualization and investigation.

Prometheus evaluates alert rules.

Alertmanager handles alert grouping, routing, and notification delivery.

The backend must never send alerts directly to notification providers during normal request handling.

## 146. Alertmanager Configuration

Create:

monitoring/alertmanager/alertmanager.yml

Alertmanager configuration should define:

- global configuration
- route configuration
- grouping
- repeat interval
- receiver definitions

Local development may use a simple receiver such as a webhook or another test destination.

Do not hardcode production credentials into the repository.

Secrets must be supplied through environment variables, Docker secrets, GitHub Actions secrets, or the deployment platform's secret manager.

## 147. Alert Severity

Use a small and consistent severity model.

Recommended levels:

warning
critical

Use warning for conditions that indicate degradation but do not necessarily represent an immediate outage.

Use critical for conditions that represent a major service failure or sustained inability to serve traffic.

Do not create unnecessary severity levels unless a concrete operational requirement exists.

## 148. Backend Alert Rules

Backend alert rules should cover meaningful failure modes.

Recommended alerts include:

- backend unavailable
- high HTTP 5xx rate
- sustained high request latency
- excessive application errors
- Redis dependency failure
- abnormal request saturation where measurable

Alert names should be descriptive.

Examples include:

BackendDown
BackendHighErrorRate
BackendHighLatency
RedisUnavailable

Exact names may be adjusted to the repository's naming convention.

## 149. Backend Availability Alert

The backend availability alert should detect when Prometheus can no longer successfully scrape the backend.

The alert should use the Prometheus scrape health signal for the backend service.

The alert should include a short delay before firing so that transient restarts do not immediately create noisy alerts.

The delay should be long enough to avoid normal container restart noise while remaining useful for genuine outages.

The alert annotation should identify:

- affected service
- environment
- reason

Do not include sensitive information.

## 150. High Error Rate Alert

The platform should detect sustained HTTP 5xx errors.

Do not alert on a single failed request.

Use an error rate calculated over a time window.

The exact PromQL expression must use the actual HTTP metrics emitted by the installed instrumentation.

The alert should only fire after the condition remains true for a meaningful duration.

Avoid hardcoding an arbitrary threshold without documenting why it exists.

For local development, thresholds may intentionally be lower so that failure injection is easy to demonstrate.

For production-like environments, thresholds should be tuned using observed baseline traffic.

## 151. High Latency Alert

Create an alert for sustained high request latency.

Use histogram metrics where available.

The alert should focus on a percentile such as p95 rather than average latency.

The threshold must be configurable and documented.

Do not choose a threshold solely because it produces a visually interesting Grafana graph.

## 152. Redis Failure Alert

The platform should detect Redis dependency failures.

Possible signals include:

- Redis error counter rate
- readiness failures
- application errors attributable to Redis
- dependency health metrics where available

The alert should avoid firing solely because one Redis request failed.

Use sustained failure or a meaningful error rate.

If Redis becomes unavailable, the alert should provide enough context to identify Redis as the affected dependency.

## 153. Alert Labels and Annotations

Alert labels should remain low-cardinality.

Recommended labels:

- alertname
- severity
- service
- environment

Annotations should provide human-readable context.

Recommended annotations:

- summary
- description

Do not put arbitrary request IDs, URLs, short codes, IP addresses, or exception strings into alert labels.

Do not create separate alerts for every URL or user.

## 154. Alert Grouping

Alertmanager should group related alerts.

For example, if the backend becomes unavailable, Prometheus may produce several related symptoms.

Alertmanager should prevent a single outage from becoming dozens of duplicate notifications.

Group by bounded dimensions such as:

- alertname
- service
- environment

The exact grouping strategy may be adjusted as the alert set grows.

## 155. Alert Routing

Routing should distinguish at least:

warning
critical

Critical alerts should receive more immediate notification treatment than warnings.

Local development may route both severities to the same test receiver.

Production deployments may route critical alerts to a more urgent destination.

Do not commit production notification URLs, tokens, passwords, or API keys.

## 156. Alert Testing

Every alert must be tested intentionally.

Do not consider an alert complete merely because Prometheus accepts the configuration.

Testing should verify:

1. condition becomes true
2. Prometheus evaluates the rule
3. alert enters pending or firing state
4. Alertmanager receives the alert
5. Alertmanager routes the alert correctly
6. notification target receives the expected alert
7. recovery causes the alert to resolve

Document how each alert can be tested locally.

## 157. Failure Injection

Failure injection must be controlled and reversible.

Examples include:

- stopping Redis
- restarting Redis
- stopping the backend
- restarting the backend
- generating controlled HTTP 5xx responses
- introducing artificial latency in a development-only code path
- generating sustained request traffic

Do not introduce failure injection into production code without an explicit feature flag and deployment policy.

Failure injection must never require modifying source code manually just to restore normal behavior.

## 158. Redis Failure Scenario

A Redis failure test should validate:

1. Redis is healthy.
2. Backend is healthy.
3. Normal URL creation works.
4. Redis is made unavailable.
5. Backend dependency behavior is observed.
6. readiness reflects the intended state.
7. Redis-related metrics increase.
8. Redis alert becomes active if thresholds are met.
9. Redis is restored.
10. Backend recovers.
11. Alert resolves.

The test must distinguish between:

liveness failure

and:

readiness or dependency failure.

Do not automatically restart the backend merely because Redis is unavailable unless that behavior is explicitly required.

## 159. Backend Failure Scenario

A backend failure test should validate:

1. Prometheus can initially scrape the backend.
2. Grafana displays normal traffic.
3. Backend is stopped.
4. Prometheus detects the scrape failure.
5. Backend availability alert fires.
6. Grafana reflects the outage.
7. Backend is restarted.
8. Prometheus detects recovery.
9. Alert resolves.

The expected recovery path must be documented.

## 160. Controlled HTTP Error Scenario

The application should have a safe development or testing mechanism for generating controlled errors.

Possible approaches include:

- dedicated test endpoint disabled outside test environments
- dependency injection that forces a known exception
- mocked service failure
- integration-test-only failure hook

Do not add an undocumented production endpoint for intentionally crashing the application.

Any failure injection mechanism must be explicitly scoped to development or testing.

## 161. Locust Load Testing

Use Locust for HTTP load testing.

Create:

loadtest/locustfile.py

The load test should model realistic platform behavior.

Do not generate traffic against external production systems by default.

The default target must be a local or explicitly configured environment.

## 162. Locust Configuration

The load test target should be configurable.

Prefer an environment variable such as:

LOCUST_HOST

or the standard Locust host configuration.

Do not hardcode the backend address throughout the test code.

The load test should support different environments without source-code modification.

## 163. Locust User Behavior

The load test should simulate multiple operations.

Recommended behavior distribution:

- create short URLs
- redirect to existing short URLs
- request analytics
- occasionally request invalid short codes

The exact distribution should be documented.

Do not create a new short URL for every single request if the purpose is to measure redirect performance.

Use a realistic mixture of reads and writes.

## 164. Locust Test Data

The load test should maintain a reusable pool of valid short codes where appropriate.

The test should:

1. create several URLs
2. capture their short codes
3. reuse those short codes for redirect and analytics requests

This produces a more realistic workload.

Do not hardcode real external URLs or private customer data.

Use safe test destinations such as example.com or another explicitly configured test destination.

## 165. Locust Scenarios

The load-testing documentation should define at least three scenarios.

### Baseline

Purpose:

Establish normal application behavior.

Measure:

- requests per second
- p50 latency
- p95 latency
- p99 latency
- HTTP error rate
- Redis errors
- CPU and memory where available

### Stress

Purpose:

Determine how the system behaves as concurrency increases.

Increase:

- concurrent users
- request rate
- test duration

Observe:

- latency degradation
- error rate
- Redis behavior
- container resource usage

### Recovery

Purpose:

Validate behavior after a dependency or service failure.

Sequence:

1. start baseline traffic
2. inject controlled failure
3. observe alerts and errors
4. restore dependency or service
5. continue traffic
6. verify recovery

## 166. Load Test Safety

Load tests must be explicitly scoped.

Never run stress tests against production infrastructure without authorization.

The default project configuration should target local development.

The README must clearly state that load tests are intended for local or staging environments and must not target production without explicit authorization.

Do not provide a default configuration that could accidentally target an unspecified external host.

## 167. Load Test Metrics

During load testing, monitor:

- request throughput
- request latency
- HTTP 4xx rate
- HTTP 5xx rate
- Redis errors
- backend availability
- CPU usage
- memory usage
- container restarts

Use Prometheus and Grafana to observe the application while Locust generates traffic.

The load test should not be evaluated only by Locust's final success percentage.

Correlate Locust results with application and infrastructure telemetry.

## 168. Performance Baseline

Record a baseline before stress testing.

At minimum capture:

- concurrency
- duration
- request rate
- p50 latency
- p95 latency
- p99 latency
- error rate

Also record relevant environment details:

- CPU
- RAM
- Docker resource limits
- Redis configuration
- backend configuration

Do not compare two benchmark results without considering whether the environments are materially different.

## 169. Load Test Documentation

Create:

loadtest/README.md

Document:

- prerequisites
- target configuration
- baseline scenario
- stress scenario
- recovery scenario
- expected metrics
- safety restrictions
- how to interpret results

The documented workflow must match the project's actual dependency installation and execution method.

## 170. Failure Recovery Principles

The system should recover without requiring manual database or data reconstruction after ordinary development failures.

After restarting Redis:

- existing persistent data should remain when persistence is configured
- backend should reconnect
- readiness should recover
- normal URL operations should resume

After restarting the backend:

- Redis data should remain intact
- frontend should reconnect when requests are made
- Prometheus should resume scraping
- Grafana should resume displaying current data

After restarting monitoring services:

- backend should remain operational
- Prometheus should resume scraping
- Grafana should reconnect to Prometheus
- alerting should resume

## 171. Phase 5 Definition of Done

Phase 5 is complete when:

- [ ] Alertmanager is included in the monitoring stack.
- [ ] Prometheus sends alerts to Alertmanager.
- [ ] Warning and critical severities are defined.
- [ ] Backend availability alert exists.
- [ ] High HTTP error-rate alert exists.
- [ ] High latency alert exists.
- [ ] Redis failure alert exists.
- [ ] Alert labels remain low-cardinality.
- [ ] Alert routing is reproducible from repository configuration.
- [ ] Production secrets are not committed.
- [ ] Alerts have been manually tested.
- [ ] Alert recovery has been tested.
- [ ] Locust is configured.
- [ ] Baseline load testing is documented.
- [ ] Stress testing is documented.
- [ ] Recovery testing is documented.
- [ ] Load tests default to local or staging environments.
- [ ] Redis failure injection has been tested.
- [ ] Backend failure recovery has been tested.
- [ ] Controlled HTTP error handling has been tested.
- [ ] Grafana and Prometheus are used during load testing.
- [ ] Load-test results include latency and error-rate measurements.
- [ ] Failure recovery does not require manual data reconstruction.


## 172. Phase 6 — QA Strategy & End-to-End Validation

The project must be validated as a complete system, not only as isolated components.

Testing must cover:

- backend unit behavior
- backend API behavior
- Redis integration
- frontend component behavior
- frontend API integration
- end-to-end user flows
- Docker Compose integration
- infrastructure configuration
- observability
- alerting
- load testing
- failure recovery
- security checks

The goal is not maximum test count.

The goal is confidence that the system behaves correctly under normal, invalid, degraded, and recovery conditions.

## 173. Testing Pyramid

Use a testing pyramid.

Prefer:

1. unit tests
2. integration tests
3. API tests
4. end-to-end tests
5. load and resilience tests

Most business logic should be covered by fast unit tests.

Integration tests should verify boundaries such as:

- FastAPI to Redis
- API to service layer
- service to repository
- frontend to backend

End-to-end tests should cover critical user journeys rather than every internal implementation detail.

Load and resilience tests should validate system behavior under controlled stress and failure.

## 174. Backend Unit Testing

Backend unit tests should cover:

- Base62 encoding
- Base62 decoding if implemented
- short-code generation
- URL validation
- URL normalization where applicable
- analytics calculations
- service-level business rules
- domain exceptions
- configuration validation

Pure utilities should be tested independently from Redis and HTTP.

Tests should be deterministic.

Avoid real network calls in unit tests.

## 175. Backend API Testing

API tests should verify:

- successful URL creation
- invalid URL rejection
- missing request fields
- malformed request bodies
- redirect behavior
- unknown short codes
- analytics retrieval
- unknown analytics code
- health endpoint
- readiness endpoint
- metrics endpoint
- expected HTTP status codes
- response schema

Test both successful and unsuccessful requests.

Assertions should verify meaningful response content rather than only checking that the request completed.

## 176. Redis Integration Testing

Redis integration tests should use a real Redis instance or isolated Redis test service.

Do not mock every Redis operation and consider Redis integration complete.

Integration tests should verify:

- URL storage
- URL retrieval
- short-code uniqueness
- atomic sequence behavior
- analytics counter updates
- missing keys
- persistence behavior where configured
- connection failure handling

Tests must clean up their data.

Do not allow one test's Redis state to affect another test.

## 177. Redis Atomicity Testing

The short-code generation mechanism must remain correct under concurrent requests.

Where Redis INCR is used, integration testing should verify that concurrent creation requests produce unique codes.

The test should simulate multiple requests occurring close together.

The expected invariant is:

no duplicate short codes are produced.

Do not rely solely on sequential unit tests for this behavior.

## 178. Backend Error Testing

Test expected failure categories.

Examples:

- Redis unavailable
- Redis timeout
- missing short code
- invalid URL
- unexpected repository failure
- malformed request
- internal service exception

The API should return appropriate HTTP responses without exposing internal implementation details.

Do not expose:

- stack traces
- Redis connection strings
- credentials
- filesystem paths
- internal exception messages containing secrets

in normal production responses.

## 179. Frontend Component Testing

Frontend tests should cover important components.

At minimum:

UrlForm.vue
ShortUrlResult.vue
AnalyticsCard.vue

Test:

- rendering
- user input
- validation
- loading state
- success state
- error state
- emitted events
- displayed short URL
- copy interaction where practical

Tests should focus on observable behavior.

Avoid tightly coupling tests to internal implementation details.

## 180. Frontend Service Testing

The frontend API service layer should be tested independently.

Verify behavior for:

- successful URL creation
- failed URL creation
- analytics retrieval
- backend error responses
- malformed responses
- network failures

Do not duplicate API request logic across components.

Tests should confirm that components receive predictable service-level results.

## 181. Frontend Type Safety

TypeScript must remain enabled in strict mode where practical.

The frontend should avoid unnecessary use of:

any

Unknown external API data should be validated or safely transformed before being treated as trusted application data.

API response types should be centralized under the frontend type definitions.

Changing the backend response contract should require an intentional frontend type update.

## 182. End-to-End User Flows

At least the following end-to-end flows must be validated.

### Flow A — Create URL

1. User opens the frontend.
2. User enters a valid destination URL.
3. User submits the form.
4. Frontend sends the API request.
5. Backend validates the URL.
6. Backend generates a short code.
7. Backend stores the URL in Redis.
8. Backend returns the short URL.
9. Frontend displays the result.
10. User can copy the short URL.

### Flow B — Redirect

1. User opens a generated short URL.
2. Backend resolves the short code.
3. Redirect counter is updated.
4. User receives the expected redirect response.
5. Destination URL is reached.

### Flow C — Analytics

1. User opens the analytics view.
2. Frontend requests analytics.
3. Backend retrieves analytics data.
4. Frontend displays the result.
5. Values correspond to previously generated traffic.

## 183. Invalid User Flow Testing

End-to-end validation must also cover invalid behavior.

Examples:

- empty URL
- malformed URL
- unsupported URL scheme
- unknown short code
- invalid analytics code
- backend unavailable
- Redis unavailable

The frontend should show a useful user-facing error.

The frontend must not expose internal exception details.

## 184. API Contract Verification

Backend and frontend must agree on:

- endpoint paths
- HTTP methods
- request fields
- response fields
- status codes
- error format
- optional fields
- analytics structure

When an API contract changes:

1. update backend schema
2. update backend tests
3. update frontend types
4. update frontend service layer
5. update affected components
6. update documentation
7. run the full relevant test suite

Do not silently change response fields without updating consumers.

## 185. Test Data Strategy

Test data should be deterministic where possible.

Use clearly identifiable test destinations.

Do not use:

- real customer URLs
- private tokens
- production credentials
- personal information
- production Redis data

Tests must be safe to run repeatedly.

Generated test data should be cleaned up where persistence could affect future tests.

## 186. Test Isolation

Each test should control its own state.

Avoid hidden dependencies such as:

- test execution order
- previously created Redis keys
- manually configured environment variables
- locally cached frontend state
- an already-running external service that is not declared as a dependency

If a test requires Redis, that requirement must be explicit.

If a test requires Docker, that requirement must be documented.

## 187. Docker Integration Testing

The Docker Compose stack should be tested as a complete local environment.

Verify:

- frontend starts
- backend starts
- Redis starts
- Prometheus starts
- Grafana starts
- Alertmanager starts
- services can communicate
- health checks behave correctly
- volumes are mounted correctly
- configuration files are loaded
- monitoring services can reach the backend

The stack should be reproducible from a clean environment.

Do not depend on manually created Docker networks or containers.

## 188. Startup Order

Docker Compose startup order must not be treated as proof that dependencies are ready.

A service may start before Redis is actually accepting connections.

Use health checks and appropriate dependency conditions where supported.

The backend should handle dependency startup gracefully.

A temporary Redis startup delay should not permanently break the backend.

## 189. Container Health Checks

Health checks should exist for services where practical.

At minimum consider health checks for:

- backend
- Redis
- frontend where an HTTP health endpoint is available
- Prometheus
- Grafana
- Alertmanager

Health checks should be:

- lightweight
- deterministic
- representative of service availability
- safe to execute repeatedly

Do not make health checks perform expensive application operations.

## 190. Infrastructure Validation

Terraform configuration must be validated independently from application tests.

Required validation includes:

- formatting
- initialization
- provider resolution
- configuration validation
- plan generation

Infrastructure changes should not be considered complete if Terraform configuration is syntactically valid but produces an unintended plan.

Review resource changes before applying them.

## 191. Terraform Drift Awareness

Terraform should remain the source of truth for resources it manages.

Avoid manually modifying Terraform-managed infrastructure through Docker or another interface without updating the Terraform configuration.

If manual changes are unavoidable during debugging:

1. identify the drift
2. restore the intended state
3. update Terraform configuration if the change is permanent

Do not normalize undocumented infrastructure drift.

## 192. Security QA

Security validation should cover:

- dependency vulnerabilities
- container vulnerabilities
- unsafe URL schemes
- secret exposure
- insecure configuration
- excessive permissions
- unnecessary open ports
- unsafe CORS configuration
- malformed input handling
- error information leakage

At minimum integrate:

- Ruff
- pip-audit
- npm audit
- Trivy
- Dependabot

Security tooling should run automatically in CI where practical.

## 193. URL Security Testing

The URL shortener must explicitly reject dangerous schemes.

Reject examples such as:

- javascript
- data
- file

Allow only explicitly supported schemes such as:

- http
- https

Validation must happen server-side.

Frontend validation is not a security boundary.

The backend must never trust frontend validation.

## 194. CORS Testing

CORS configuration must be tested against the intended frontend origin.

Do not use unrestricted wildcard origins in production-like configuration unless there is a documented reason.

The allowed origin list should come from configuration.

Environment-specific origins should not require source-code modification.

## 195. Secret Management QA

Verify that secrets are absent from:

- source code
- committed environment files
- Docker images
- Terraform configuration
- GitHub Actions logs
- application logs
- Prometheus metrics
- Grafana dashboards

Use environment-specific secret injection.

The repository may contain:

.env.example

but must not contain real credentials.

## 196. Observability QA

Observability must be tested as part of the application.

Verify:

- /metrics responds
- Prometheus scrapes successfully
- Grafana receives Prometheus data
- application counters increase
- latency metrics change under traffic
- Redis failures produce relevant telemetry
- alerts fire under controlled conditions
- alerts resolve after recovery

A dashboard that loads but contains no meaningful application data is not considered complete.

## 197. Recovery Validation

Every critical dependency should have a recovery test.

At minimum:

### Redis recovery

Redis unavailable
    ->
backend detects dependency failure
    ->
metrics reflect failure
    ->
alert fires if threshold is met
    ->
Redis restored
    ->
backend reconnects
    ->
readiness recovers
    ->
alert resolves

### Backend recovery

Backend unavailable
    ->
Prometheus detects scrape failure
    ->
availability alert fires
    ->
backend restored
    ->
Prometheus resumes scraping
    ->
alert resolves

### Monitoring recovery

Prometheus or Grafana unavailable
    ->
application continues operating
    ->
monitoring service restored
    ->
telemetry collection or visualization resumes

## 198. Regression Testing

Every bug fix should include a regression test when practical.

The test should reproduce the failure before the fix and verify the intended behavior afterward.

Do not rely on manual memory to prevent regressions.

Regression tests should live near the relevant test suite.

Examples:

- invalid URL bypassing validation
- duplicate short-code generation
- Redis reconnect failure
- analytics counter not incrementing
- frontend error state not rendering
- incorrect redirect response
- incorrect API response schema

## 199. Test Naming

Test names should describe behavior.

Prefer names such as:

test_create_url_returns_unique_short_code

test_invalid_url_is_rejected

test_redirect_increments_click_count

test_missing_short_code_returns_not_found

test_redis_failure_marks_service_not_ready

Avoid names such as:

test_url

test_case_1

test_bug

A reader should understand the intended behavior from the test name.

## 200. CI Test Gates

Pull requests must not merge when required validation fails.

At minimum, CI should verify:

- backend formatting/linting
- backend tests
- frontend tests
- frontend type checking
- frontend build
- dependency security checks
- Terraform validation
- Docker build validation
- container security scanning

Do not make security checks informational if the repository's intended policy requires them to block merges.

If a security scanner produces a false positive, document and review the exception rather than silently disabling the scanner.

## 201. Quality Gates

A change is considered production-ready only when:

- functionality works
- tests pass
- types pass
- linting passes
- security checks pass
- containers build
- infrastructure validates
- observability remains functional
- documentation is updated when behavior changes

A feature is not complete merely because the happy path works locally.

## 202. QA Test Matrix

Maintain a test matrix covering:

Area:
Backend

Checks:
- unit tests
- API tests
- integration tests
- error handling

Area:
Frontend

Checks:
- component tests
- service tests
- type checking
- build

Area:
Redis

Checks:
- integration
- atomicity
- failure handling
- recovery

Area:
Docker

Checks:
- image build
- Compose startup
- health checks
- networking

Area:
Terraform

Checks:
- formatting
- validation
- plan review

Area:
CI/CD

Checks:
- pull request validation
- security scans
- image build
- release workflow

Area:
Observability

Checks:
- metrics
- Prometheus scrape
- Grafana dashboard
- alerting

Area:
Load Testing

Checks:
- baseline
- stress
- recovery

Area:
Security

Checks:
- dependencies
- containers
- secrets
- input validation
- configuration

## 203. Release Candidate Validation

Before creating a release candidate, perform a clean validation cycle.

Required sequence:

1. start from a clean working tree
2. install dependencies from lock or declared dependency files
3. run backend checks
4. run frontend checks
5. validate Terraform
6. build Docker images
7. start the complete Compose stack
8. verify health and readiness
9. execute critical user flows
10. verify metrics
11. verify Grafana
12. verify alerting
13. run a baseline load test
14. perform at least one controlled recovery test
15. review security scan results
16. review documentation

The exact commands may be automated through the Makefile or CI workflows.

## 204. Clean Environment Requirement

The application must be capable of starting from a clean development environment using documented setup instructions.

Do not depend on:

- globally installed Python packages
- globally installed Node packages
- manually configured Redis
- manually created Docker networks
- undocumented environment variables
- local files excluded from version control

If a dependency is required, document it.

If a configuration value is required, provide it through an example configuration or documented environment variable.

## 205. Test Artifacts

Generated test artifacts should not pollute the repository.

Do not commit:

- coverage caches
- pytest caches
- frontend build output
- temporary Locust results
- local Grafana state
- Prometheus data
- Docker volumes
- Terraform state
- secret files
- local environment files

Ensure appropriate entries exist in .gitignore and .dockerignore.

## 206. Phase 6 Definition of Done

Phase 6 is complete when:

- [ ] Backend unit tests cover core business logic.
- [ ] Backend API tests cover success and failure cases.
- [ ] Redis integration tests use an isolated Redis environment.
- [ ] Concurrent short-code generation has been tested.
- [ ] Frontend components have meaningful tests.
- [ ] Frontend API services have failure-path tests.
- [ ] Critical end-to-end flows have been validated.
- [ ] Invalid user flows have been validated.
- [ ] Docker Compose has been tested from a clean environment.
- [ ] Service health checks have been verified.
- [ ] Terraform validation passes.
- [ ] Security tooling passes or documented exceptions exist.
- [ ] URL security validation has been tested.
- [ ] CORS behavior has been tested.
- [ ] Secrets are absent from repository artifacts.
- [ ] Metrics and dashboards have been verified.
- [ ] Alerts have been verified.
- [ ] Redis recovery has been tested.
- [ ] Backend recovery has been tested.
- [ ] Monitoring recovery has been tested.
- [ ] Regression tests exist for important bugs.
- [ ] CI quality gates are enforced.
- [ ] Release candidate validation is documented.
- [ ] Clean-environment setup works.
- [ ] Generated development artifacts are excluded from version control.


## 207. Phase 7 — Security Hardening & Production Readiness

The project is intended to demonstrate production-oriented engineering.

Security must therefore be treated as a continuous engineering concern.

The objective is not to make the project artificially complex.

The objective is to prevent common classes of mistakes involving:

- input validation
- secrets
- authentication boundaries
- container configuration
- infrastructure permissions
- dependency vulnerabilities
- exposed services
- unsafe defaults
- information leakage
- CI/CD permissions

Security controls should be proportional to the actual application.

Do not introduce enterprise security systems that provide no meaningful value for this project.

## 208. Security Principles

Follow these principles:

- secure by default
- least privilege
- explicit trust boundaries
- validate at the server boundary
- fail safely
- do not expose secrets
- minimize exposed ports
- minimize container privileges
- keep dependencies current
- make security checks reproducible

Never treat frontend validation as a security boundary.

The backend is responsible for validating untrusted input.

## 209. Trust Boundaries

Identify the major trust boundaries:

Browser
    ->
Frontend
    ->
Backend API
    ->
Redis

Additional operational boundaries:

GitHub Actions
    ->
Container Registry

Terraform
    ->
Infrastructure Provider

Prometheus
    ->
Backend metrics endpoint

Locust
    ->
Backend API

Data crossing a trust boundary must be treated as untrusted unless explicitly verified.

## 210. Input Validation

All externally supplied input must be validated.

Important inputs include:

- destination URLs
- short codes
- analytics parameters
- query parameters
- request bodies
- HTTP headers where application logic uses them

Validation should occur at the API boundary.

Business logic should receive validated domain values rather than raw HTTP data whenever practical.

Validation errors should return predictable API responses.

Do not rely on implicit type coercion for security-sensitive values.

## 211. URL Validation Security

The URL shortener must explicitly define which URL schemes are supported.

The default supported schemes are:

- http
- https

The following schemes must be rejected:

- javascript
- data
- file

Other schemes should be rejected unless explicitly required and reviewed.

Validation should account for malformed URLs and ambiguous parsing cases.

Do not implement URL validation using only a simple string prefix check.

Use a proper URL parser and explicit scheme validation.

## 212. Redirect Security

Redirects must only use URLs previously validated and stored by the backend.

Do not accept a destination URL directly from the redirect request.

The short code should resolve to a stored destination.

The redirect endpoint must not allow arbitrary open redirects through request parameters.

The system should return an appropriate not-found response when a short code does not exist.

Do not reveal Redis keys or internal storage details in redirect errors.

## 213. Short-Code Validation

Short codes must follow a strict expected format.

The validation rules should define:

- allowed characters
- minimum length if applicable
- maximum length
- case sensitivity
- invalid character behavior

The API should reject malformed short codes before unnecessary Redis operations where practical.

Do not allow arbitrary Redis key fragments to be constructed from unrestricted user input.

## 214. Redis Key Safety

Redis keys should be generated by application-controlled templates.

User-controlled values must be validated before being incorporated into keys.

Use predictable namespaces such as:

url:{code}
analytics:{code}:clicks
meta:urls:sequence

Do not allow arbitrary key names supplied by clients.

Do not expose Redis commands through the HTTP API.

## 215. Redis Security

Redis should not be exposed publicly by default.

In Docker Compose:

- Redis should be reachable by backend services
- Redis does not need a public host port for normal application operation
- only required services should be exposed to the host

If Redis authentication is introduced, credentials must come from secret configuration.

Do not commit Redis passwords.

## 216. Docker Container Security

Containers should run with the minimum privileges required.

Where practical:

- run application processes as non-root users
- avoid privileged containers
- avoid host networking
- avoid unnecessary Linux capabilities
- avoid mounting the Docker socket
- use read-only filesystems where compatible
- minimize writable directories
- avoid unnecessary device access

Do not add security options merely for appearance.

Every security restriction must remain compatible with application functionality.

## 217. Docker Image Hardening

Production images should contain only what the application needs.

Avoid including:

- compilers
- development caches
- source-control metadata
- test artifacts
- local credentials
- unnecessary debugging utilities

Use multi-stage builds where they materially reduce the final image.

The frontend runtime image should contain built static assets rather than the full Node development environment when possible.

The backend image should install only required runtime dependencies.

## 218. Docker Image Pinning

Base images should use explicit versions.

Avoid relying exclusively on floating tags such as:

latest

Use stable version tags or digest pinning where appropriate.

When updating a base image:

1. update the Dockerfile
2. rebuild
3. run tests
4. run Trivy
5. verify application behavior

Do not silently change base images during unrelated feature work.

## 219. Dockerfile Hygiene

Dockerfiles should:

- use appropriate working directories
- minimize layers where practical
- avoid copying unnecessary files
- use .dockerignore
- avoid embedding secrets
- avoid unnecessary package managers in runtime images
- use deterministic dependency installation where possible

Do not copy the entire repository into a runtime image if only a subset is required.

## 220. Docker Compose Security

Docker Compose should expose only required ports.

Typical externally accessible services may include:

- frontend
- backend API
- Grafana
- Prometheus during local development

Redis should normally remain internal to the Compose network.

Alertmanager does not need a public host port unless local testing requires it.

Do not expose administrative services unnecessarily.

## 221. Network Segmentation

Use Docker networks deliberately.

At minimum the architecture should support communication between:

- frontend and backend
- backend and Redis
- Prometheus and backend
- Grafana and Prometheus
- Alertmanager and Prometheus

Services should not automatically receive access to every network if that access is unnecessary.

If separate networks improve isolation without adding unreasonable complexity, use them.

Do not create excessive network segmentation for a small portfolio application.

## 222. CORS Configuration

CORS must be explicit.

Allowed origins should come from configuration.

Development may allow the local frontend origin.

Production-like configuration should allow only intended frontend origins.

Do not use unrestricted origins with credentials.

Do not allow arbitrary origins based on request input.

## 223. Security Headers

The backend or frontend serving layer should consider appropriate HTTP security headers.

Relevant headers may include:

- Content-Security-Policy
- X-Content-Type-Options
- Referrer-Policy
- Strict-Transport-Security in HTTPS deployments

Only enable headers where their deployment semantics are understood.

Do not enable HSTS in a local HTTP-only environment if it would interfere with development.

Document environment-specific security behavior.

## 224. API Rate Limiting

Rate limiting is a potential future improvement.

The initial implementation does not need a complex distributed rate-limiting system unless required by the deployment environment.

However, the architecture should avoid making rate limiting impossible to introduce later.

Potential future locations include:

- reverse proxy
- API gateway
- Redis-backed limiter
- application middleware

Do not implement an elaborate limiter merely to claim that the project has one.

## 225. Authentication Scope

The initial URL shortener may remain unauthenticated if the intended product scope is a public anonymous shortener.

If user accounts are introduced later, authentication must be designed explicitly.

Do not add fake authentication solely for portfolio appearance.

If authentication is added, review:

- password handling
- session/token security
- authorization
- account ownership
- analytics access control
- secret storage
- token expiration

Authentication and authorization must not be confused.

## 226. Authorization Boundaries

If the platform becomes user-aware, every resource must have an explicit ownership model.

For example:

- who can view analytics
- who can delete a URL
- who can modify a URL
- who can manage administrative resources

Do not rely on hidden frontend routes for authorization.

Authorization must be enforced by the backend.

## 227. Error Handling Security

Production API responses must not expose internal implementation details.

Do not return:

- Python tracebacks
- Redis connection details
- filesystem paths
- environment variables
- internal class names
- SQL statements if a database is introduced
- secret values

Log technical details internally when appropriate.

Return safe, stable error messages to clients.

## 228. Logging Security

Logs should support debugging without becoming a data-leak source.

Do not log:

- passwords
- tokens
- API keys
- authorization headers
- cookies
- private destination URLs unless explicitly required
- complete request bodies containing sensitive data

Logs should contain useful operational context such as:

- timestamp
- level
- service
- route
- status
- duration
- error category

Request IDs may be used for correlation if they do not contain sensitive information.

## 229. Dependency Governance

Dependencies must be intentionally managed.

Backend dependencies should be reviewed for:

- security vulnerabilities
- maintenance status
- compatibility
- transitive dependencies

Frontend dependencies should receive the same treatment.

Avoid adding a dependency for functionality that can be implemented simply with the standard library or existing project dependencies.

Every new dependency should have a clear reason.

## 230. Dependency Update Policy

Dependency updates should be performed through controlled changes.

For each meaningful update:

1. inspect changelog or release notes where relevant
2. update dependency declaration
3. regenerate or update lock information if applicable
4. run tests
5. run security scans
6. rebuild containers
7. review behavior changes

Do not blindly accept automated dependency updates without CI validation.

## 231. Dependabot Policy

Dependabot should be enabled for relevant ecosystems.

Recommended coverage includes:

- Python
- npm
- GitHub Actions
- Docker where supported

Group low-risk dependency updates where appropriate.

Security updates should remain visible and should not be hidden by aggressive grouping.

## 232. GitHub Actions Security

GitHub Actions workflows must use least privilege.

Default workflow permissions should be restricted.

Grant write permissions only to jobs that require them.

Avoid using broad repository write permissions for test jobs.

Secrets must only be exposed to jobs that require them.

Do not print secrets for debugging.

Avoid passing secrets into pull requests from untrusted forks unless the workflow architecture explicitly protects them.

## 233. GitHub Actions Dependency Pinning

Third-party GitHub Actions should be pinned to stable versions.

For higher-security environments, pinning to immutable commit SHAs may be preferred.

When updating an action:

- review the release
- update the pinned reference
- run the affected workflow
- verify permissions

Do not use arbitrary third-party actions without reviewing their purpose and trustworthiness.

## 234. Container Registry Security

Published images should use predictable names.

Backend:

url-shortener-backend

Frontend:

url-shortener-frontend

Image tags should identify the source revision or release version.

Avoid relying only on a mutable latest tag.

Container registry credentials must be stored as CI secrets.

Do not place registry passwords in Dockerfiles or repository configuration.

## 235. Terraform Security

Terraform configuration must follow least privilege.

Do not create infrastructure permissions broader than required.

Secrets should not be hardcoded into Terraform files.

Sensitive variables should be marked appropriately.

Terraform state may contain sensitive information.

Do not commit local Terraform state to the repository.

Protect remote state appropriately if remote state is introduced later.

## 236. Terraform Secret Handling

Never place secrets directly in:

- variables.tf
- main.tf
- outputs.tf
- provider configuration
- committed tfvars files

Use environment variables or a dedicated secret management mechanism.

Sensitive outputs should be marked as sensitive.

Do not expose secrets through normal Terraform output.

## 237. Terraform State

Terraform state must be treated as sensitive infrastructure data.

Ignore local state files through .gitignore.

Do not commit:

- terraform.tfstate
- terraform.tfstate.backup
- crash logs
- local provider caches

If remote state is introduced, use the platform's access controls and locking capabilities.

## 238. Environment Management

The application must distinguish at least:

- local development
- CI
- production-like deployment

Environment-specific configuration should include:

- API base URL
- Redis connection
- allowed CORS origins
- monitoring settings
- logging level
- feature flags
- secret references

Do not duplicate source code simply to support environments.

Prefer configuration over conditional application forks.

## 239. Environment Variables

Environment variables should have clear names.

Examples include:

- APP_ENV
- REDIS_URL
- CORS_ALLOWED_ORIGINS
- LOG_LEVEL
- API_BASE_URL
- LOCUST_HOST

Actual variable names should remain centralized and documented.

Use Pydantic Settings on the backend to validate required configuration.

Invalid configuration should fail clearly during startup rather than causing obscure runtime failures.

## 240. .env.example

The repository should contain:

.env.example

It should document required configuration without containing real secrets.

Use placeholder values.

The example file should remain synchronized with the application's configuration model.

When a new required environment variable is introduced:

1. add it to configuration
2. add it to .env.example
3. document it
4. update deployment configuration
5. update relevant CI workflows

## 241. Configuration Validation

Configuration should be validated at startup.

Examples:

- invalid Redis URL
- unsupported environment value
- malformed CORS origins
- invalid port
- invalid logging level

The application should fail fast when mandatory configuration is invalid.

Do not silently substitute unsafe defaults for security-sensitive configuration.

## 242. Production Configuration

Production-like configuration should:

- disable development debug behavior
- use appropriate logging levels
- restrict CORS
- protect secrets
- minimize exposed ports
- use hardened container settings
- enable HTTPS at the appropriate infrastructure layer
- configure monitoring
- configure alerting

The local development environment may intentionally use simpler settings.

Do not confuse local convenience with production defaults.

## 243. Security Documentation

The README should document:

- supported URL schemes
- secret management expectations
- environment configuration
- exposed local services
- security scanning
- load-test safety
- production deployment considerations

Security documentation should describe actual behavior.

Do not claim that a control exists if it has not been implemented.

## 244. Architecture Documentation

The project should include a clear architecture section in the README.

It should explain:

- frontend responsibilities
- backend responsibilities
- Redis responsibilities
- Prometheus responsibilities
- Grafana responsibilities
- Alertmanager responsibilities
- Locust responsibilities
- Terraform responsibilities
- Docker responsibilities
- CI/CD responsibilities

A reader should understand the system without inspecting every source file.

## 245. Portfolio Presentation

The repository should demonstrate engineering judgment rather than merely technology usage.

README content should highlight:

- problem being solved
- architecture
- key engineering decisions
- testing strategy
- CI/CD
- observability
- security
- load testing
- failure recovery

Do not turn the README into a list of buzzwords.

Explain why important technologies exist in the architecture.

## 246. Architecture Decision Documentation

Important architectural decisions should be documented.

Examples:

- why Redis is used
- why Base62 is used
- why Redis INCR is used for code generation
- why FastAPI instrumentation is used
- why Prometheus and Grafana are separated
- why Docker and Terraform have different responsibilities
- why Locust is used
- why frontend and backend are separate services

Short explanations are sufficient.

Do not create a formal ADR system for every trivial implementation detail.

## 247. Technology Boundaries

Maintain clear responsibilities.

Docker:

- package applications
- provide reproducible runtime environments
- orchestrate local services

Terraform:

- define infrastructure resources
- manage infrastructure configuration
- provide reproducible infrastructure changes

GitHub Actions:

- automate validation
- build artifacts
- perform security checks
- publish releases

Prometheus:

- collect and evaluate metrics

Grafana:

- visualize metrics

Alertmanager:

- route alerts

Locust:

- generate controlled load

Do not move responsibilities between tools simply because it is technically possible.

## 248. Avoiding Overengineering

The project should remain understandable.

Do not introduce:

- Kubernetes
- service mesh
- Kafka
- event sourcing
- microservice decomposition
- distributed tracing infrastructure
- complex authentication platforms

unless a concrete requirement emerges.

A small URL shortener does not need an enterprise architecture to demonstrate engineering ability.

Complexity should be justified by a real problem.

## 249. Future Extension Points

Potential future features may include:

- custom aliases
- URL expiration
- user accounts
- authenticated analytics
- rate limiting
- domain management
- QR code generation
- click metadata
- database-backed persistence
- distributed tracing
- OpenTelemetry
- cloud deployment

These should remain future extensions unless explicitly required.

Do not implement future features prematurely.

## 250. Documentation Accuracy

Documentation must match implementation.

When behavior changes, update:

- README
- AGENTS.md where relevant
- API documentation
- environment examples
- deployment documentation
- monitoring documentation
- test instructions

Do not leave obsolete commands, ports, filenames, or architecture diagrams.

## 251. Security Review Checklist

Before release, review:

- [ ] no committed secrets
- [ ] no unsafe URL schemes
- [ ] backend validates all untrusted input
- [ ] Redis is not unnecessarily exposed
- [ ] CORS is restricted appropriately
- [ ] containers do not run with unnecessary privileges
- [ ] Docker images use maintained base versions
- [ ] dependencies are scanned
- [ ] container images are scanned
- [ ] GitHub Actions permissions are restricted
- [ ] Terraform secrets are not committed
- [ ] Terraform state is ignored
- [ ] logs do not expose secrets
- [ ] metrics do not expose sensitive data
- [ ] error responses do not expose internals

## 252. Phase 7 Definition of Done

Phase 7 is complete when:

- [ ] Input validation is enforced server-side.
- [ ] Redirect destinations are validated and stored safely.
- [ ] Short-code validation is explicit.
- [ ] Redis keys are application-controlled.
- [ ] Redis is not publicly exposed by default.
- [ ] Docker containers use reasonable security defaults.
- [ ] Docker images are minimized.
- [ ] Base images use explicit versions.
- [ ] CORS is configuration-driven.
- [ ] Error responses do not leak internals.
- [ ] Logs do not contain secrets.
- [ ] Dependency scanning is active.
- [ ] Dependabot is configured.
- [ ] GitHub Actions use least-privilege permissions.
- [ ] Container publishing does not expose registry credentials.
- [ ] Terraform follows least privilege.
- [ ] Terraform state is excluded from version control.
- [ ] Environment configuration is documented.
- [ ] .env.example is synchronized.
- [ ] Production-like configuration is separated from local configuration.
- [ ] Architecture documentation exists.
- [ ] Security documentation exists.
- [ ] Important architectural decisions are documented.
- [ ] Tool responsibilities remain clearly separated.
- [ ] The project avoids unnecessary infrastructure complexity.
- [ ] README claims match the actual implementation.


## 253. Phase 8 — Agent Operating Rules

Agents working on this repository must preserve the project's architecture, conventions, and engineering goals.

Before making changes, an agent should:

1. inspect the relevant files
2. understand existing abstractions
3. identify dependencies between components
4. determine the smallest correct change
5. implement the change
6. run relevant validation
7. review the resulting diff
8. update documentation when behavior changes

Do not rewrite unrelated code simply because another implementation style appears preferable.

Prefer incremental, reviewable changes.

## 254. Existing Code Takes Precedence

Before introducing a new abstraction, inspect whether the repository already provides one.

Examples include:

- existing configuration classes
- existing Redis clients
- existing API dependencies
- existing error handlers
- existing metric collectors
- existing test fixtures
- existing frontend API services
- existing shared TypeScript types

Do not create duplicate abstractions for the same responsibility.

If an existing abstraction is inadequate, improve it rather than silently bypassing it.

## 255. Change Scope

Keep changes focused.

A feature change should not automatically trigger unrelated:

- formatting changes
- dependency upgrades
- architecture rewrites
- file renames
- framework migrations
- dashboard redesigns

Unrelated cleanup should be performed separately unless it is required for correctness.

This keeps pull requests understandable and reduces regression risk.

## 256. Backward Compatibility

When changing an existing API or internal contract, consider existing consumers.

Before changing:

- endpoint paths
- request fields
- response fields
- status codes
- Redis key formats
- environment variable names
- metric names
- dashboard queries

identify affected components.

Update all affected consumers in the same change where practical.

Avoid silently breaking existing behavior.

## 257. API Evolution

API changes should be intentional.

For breaking changes:

1. identify the affected endpoint
2. update schemas
3. update backend implementation
4. update backend tests
5. update frontend types
6. update frontend API services
7. update frontend components
8. update documentation
9. validate end-to-end behavior

Keep the v1 API namespace stable unless a breaking change is explicitly required.

## 258. Database and Redis Compatibility

Redis data structures are part of the application's persistence contract.

Changing key formats can invalidate existing data.

Before changing:

- key prefixes
- value formats
- counter semantics
- serialization formats

determine whether existing data must remain compatible.

If migration is required, document the migration strategy.

Do not silently change persistent data formats.

## 259. Migration Strategy

If a future database is introduced, migrations must be explicit.

Do not modify persistent schemas manually and assume the application will remain compatible.

Schema changes should include:

- migration
- rollback consideration
- test coverage
- documentation

For Redis structure changes, document whether:

- existing keys remain compatible
- old keys are migrated
- old keys expire naturally
- data must be regenerated

## 260. Python Coding Conventions

Backend Python code should follow modern Python practices.

Prefer:

- type hints
- small functions
- explicit return types
- descriptive names
- dependency injection
- clear exception boundaries
- immutable values where practical

Avoid:

- unnecessary global state
- deeply nested functions
- giant service classes
- hidden side effects
- broad exception catching

Catch specific exceptions when practical.

Do not use bare exception handling.

## 261. FastAPI Conventions

FastAPI routes should remain thin.

A route should generally:

1. receive validated input
2. resolve dependencies
3. call the appropriate service
4. translate the result into an API response

Business logic should not be duplicated across route handlers.

Avoid putting large blocks of Redis logic directly inside endpoint functions.

Routes should remain easy to read and test.

## 262. Service Layer Conventions

Services contain business logic.

A service should coordinate:

- validation beyond schema-level validation
- repositories
- domain rules
- application metrics
- domain errors

Services should not depend directly on HTTP-specific objects unless there is a clear reason.

This keeps business logic reusable and testable.

## 263. Repository Conventions

Repositories should encapsulate persistence operations.

The repository layer should handle:

- Redis key construction
- Redis reads
- Redis writes
- Redis counters
- persistence-specific error translation

Business rules should remain outside the repository whenever practical.

Do not spread raw Redis commands across unrelated services.

## 264. Pydantic Conventions

Pydantic models should represent explicit API contracts.

Use separate models where request and response semantics differ.

Do not expose internal persistence models directly as public API schemas unless they intentionally represent the same contract.

Validation rules should remain clear and readable.

Avoid excessive custom validators when standard Pydantic validation is sufficient.

## 265. TypeScript Coding Conventions

Frontend TypeScript should prefer explicit types.

Use:

- interfaces or type aliases for API contracts
- typed service functions
- typed component props
- typed emitted events
- typed composables

Avoid unnecessary any.

Do not duplicate the same API type in multiple files.

Keep shared API types centralized.

## 266. Vue Conventions

Vue components should have focused responsibilities.

Prefer:

- Composition API
- composables for reusable stateful logic
- small components
- typed props
- typed emits
- clear loading/error/success states

Avoid giant components containing:

- API requests
- complex state management
- validation
- presentation
- analytics logic

all in one file.

Extract reusable logic when it becomes meaningfully complex.

## 267. Frontend State Management

Do not introduce a global state management library unless application complexity requires it.

For the initial application, local component state and composables are sufficient.

If global state becomes necessary, introduce it for a specific problem.

Do not add Pinia or another state library simply because it is popular.

## 268. Naming Conventions

Use descriptive and consistent names.

Python:

- snake_case for variables and functions
- PascalCase for classes
- UPPER_CASE for constants

TypeScript:

- camelCase for variables and functions
- PascalCase for types and Vue components

Vue components should use PascalCase filenames.

Infrastructure resources should use consistent descriptive names.

Names should communicate responsibility.

Avoid abbreviations unless they are universally understood in the project context.

## 269. File Organization

Files should be organized according to responsibility.

Do not create generic catch-all files such as:

utils.py

helpers.ts

common.ts

unless their contents genuinely represent a coherent reusable responsibility.

Prefer focused modules such as:

url_validation.py
base62.py
redis_repository.py

or equivalent names appropriate to the implementation.

## 270. Comments

Comments should explain why something exists, not restate what the code obviously does.

Good comments explain:

- non-obvious Redis behavior
- security decisions
- compatibility constraints
- unusual workarounds
- metric design decisions

Avoid comments such as:

increment counter by one

when the code already makes that obvious.

Remove outdated comments when implementation changes.

## 271. Documentation Comments

Public or complex functions should have documentation when the behavior is not obvious from the type signature and implementation.

Documentation should explain:

- purpose
- important inputs
- important outputs
- side effects
- exceptional behavior

Do not generate verbose documentation for trivial private functions.

## 272. Error Taxonomy

Application errors should have meaningful categories.

Examples:

- validation error
- not found
- dependency unavailable
- dependency timeout
- internal error

Map domain errors to HTTP responses at the API boundary.

Do not let low-level exceptions determine the public API contract accidentally.

## 273. Logging Levels

Use logging levels intentionally.

Debug:

Detailed information useful during development.

Info:

Normal important application lifecycle events.

Warning:

Unexpected but recoverable conditions.

Error:

Operation failed and requires investigation.

Critical:

Severe failure requiring immediate attention.

Do not log every request at error level.

Do not use critical logging for normal dependency failures that the application can recover from.

## 274. Metrics Conventions

Metrics must have stable names and bounded labels.

Before adding a metric ask:

1. What operational question does it answer?
2. Is a metric already available for the same question?
3. What is its cardinality?
4. What dashboard or alert consumes it?
5. What should happen if the metric is unavailable?

Do not create metrics solely because a value exists in application memory.

## 275. Alert Conventions

Every alert should answer:

- what is wrong?
- which service is affected?
- how severe is it?
- what should the operator investigate?

Alerts should not simply restate a raw metric.

Avoid alerts that fire frequently without requiring action.

If an alert repeatedly produces noise, tune or remove it.

## 276. Grafana Dashboard Conventions

Dashboard panels should support investigation.

A useful panel should have:

- descriptive title
- appropriate unit
- sensible time range
- understandable legend
- query that corresponds to a real operational question

Do not add panels simply to increase dashboard size.

Prefer a small number of useful panels over dozens of decorative graphs.

## 277. Load Test Conventions

Load tests must be reproducible.

Record:

- target environment
- test duration
- concurrency
- request profile
- application version
- relevant infrastructure configuration

Do not compare benchmark numbers without recording the conditions under which they were produced.

Load testing is a measurement exercise, not a competition for the largest requests-per-second number.

## 278. Performance Investigation

When performance degrades, investigate systematically.

Check:

1. request rate
2. latency
3. error rate
4. Redis latency/errors
5. CPU
6. memory
7. container restarts
8. network behavior
9. application logs

Do not optimize based on intuition alone when metrics can identify the bottleneck.

Avoid premature optimization.

## 279. Dependency Failure Behavior

External dependencies should fail predictably.

When Redis is unavailable:

- backend should return appropriate errors
- readiness should reflect dependency state
- metrics should record the failure
- alerts should fire when thresholds are met
- recovery should be automatic where practical

Do not hide dependency failures indefinitely.

Do not crash the process for every transient dependency error unless there is a deliberate reason.

## 280. Graceful Shutdown

Services should shut down gracefully.

The backend should:

- stop accepting new work appropriately
- allow in-flight requests to finish where practical
- close Redis connections
- release resources

The frontend runtime should terminate cleanly according to its container/runtime model.

Monitoring services should also be allowed to shut down cleanly.

## 281. Configuration Defaults

Defaults should be safe.

Examples:

- development-friendly values may be used locally
- production security settings should not depend on accidental defaults
- required secrets should not receive fake production values automatically

If a setting is security-sensitive, require explicit configuration where appropriate.

## 282. Agent Restrictions

Agents must not:

- delete working tests merely to make CI pass
- disable security scanners without documented justification
- remove monitoring because it is inconvenient
- weaken validation to support an invalid input
- commit secrets
- commit generated infrastructure state
- silently change API contracts
- replace Vue with another frontend framework
- replace FastAPI without explicit architectural approval
- replace Redis without a documented requirement
- introduce Kubernetes or microservices without justification
- remove Terraform merely because Docker Compose works locally

Architecture changes must be deliberate.

## 283. When to Refactor

Refactor when:

- duplication materially increases maintenance cost
- a module has multiple unrelated responsibilities
- tests become difficult because of poor boundaries
- a security problem is caused by the current structure
- a performance problem has been measured
- a clear abstraction repeatedly appears

Do not refactor merely because the existing code is stylistically different from personal preference.

## 284. When to Add a Dependency

Before adding a dependency, verify:

- standard library cannot reasonably solve the problem
- an existing dependency cannot solve it
- maintenance status is acceptable
- license is compatible
- security history is acceptable
- bundle/image impact is reasonable
- the dependency materially reduces complexity

Document important dependency decisions.

## 285. Implementation Order

The recommended implementation order is:

Phase 1:
Application development and testing

Phase 2:
Dockerization and Terraform

Phase 3:
CI/CD

Phase 4:
Prometheus and Grafana

Phase 5:
Alertmanager and load testing

Phase 6:
QA and end-to-end validation

Phase 7:
Security hardening and production readiness

Phase 8:
Final documentation, cleanup, and release validation

Do not jump directly into observability or infrastructure before the core application works.

Do not polish dashboards while core API behavior is still unstable.

## 286. Milestone Strategy

Each phase should produce a working increment.

Recommended milestones:

Milestone 1:
Backend can create, redirect, and analyze short URLs.

Milestone 2:
Frontend provides the complete basic user flow.

Milestone 3:
Backend and frontend run through Docker Compose.

Milestone 4:
Terraform can reproduce the intended infrastructure.

Milestone 5:
CI validates code, tests, security, containers, and infrastructure.

Milestone 6:
Prometheus and Grafana provide meaningful telemetry.

Milestone 7:
Alertmanager detects meaningful failures.

Milestone 8:
Locust validates baseline and stress behavior.

Milestone 9:
Failure injection and recovery are verified.

Milestone 10:
Security and release validation are complete.

## 287. Definition of Done for Features

A feature is complete only when:

- implementation exists
- relevant tests exist
- failure behavior is handled
- security implications are reviewed
- observability implications are considered
- documentation is updated when necessary
- CI passes

A feature should not be marked complete solely because it works manually once.

## 288. Definition of Done for Bug Fixes

A bug fix is complete when:

- root cause is understood
- fix is implemented
- regression test exists where practical
- related behavior remains functional
- CI passes
- documentation is updated if user-visible behavior changed

Do not fix symptoms while leaving an obvious root cause unresolved.

## 289. Definition of Done for Infrastructure Changes

Infrastructure changes are complete when:

- Terraform configuration is updated
- validation passes
- plan is reviewed
- Docker/Compose integration remains functional
- required secrets are handled safely
- monitoring remains functional
- documentation reflects the change

## 290. Definition of Done for CI/CD Changes

CI/CD changes are complete when:

- workflow syntax is valid
- permissions are appropriate
- required secrets are documented
- caching behaves correctly
- failure conditions are meaningful
- artifacts are reproducible
- security scanning remains enabled
- workflows do not leak secrets

## 291. Definition of Done for Observability Changes

Observability changes are complete when:

- metric exists for a meaningful reason
- cardinality is controlled
- Prometheus can collect it
- Grafana can visualize it when useful
- alerts use it when appropriate
- documentation explains its purpose

Do not add an alert without knowing how it will be investigated.

## 292. Definition of Done for Security Changes

Security changes are complete when:

- threat or failure mode is identified
- mitigation is implemented
- relevant tests exist
- CI validates the control where possible
- documentation explains important behavior
- usability is not unnecessarily degraded

Security should improve the system without becoming meaningless ceremony.

## 293. Final System Definition of Done

The URL Shortener & Analytics Platform is considered complete when all of the following are true:

Application:

- [ ] Users can create short URLs.
- [ ] Short codes are generated safely and uniquely.
- [ ] URLs are stored in Redis.
- [ ] Short URLs redirect correctly.
- [ ] Redirect analytics are recorded.
- [ ] Analytics can be retrieved.
- [ ] Invalid URLs are rejected.
- [ ] Unknown short codes return appropriate errors.
- [ ] Health and readiness endpoints work.
- [ ] Metrics endpoint works.

Frontend:

- [ ] URL creation flow works.
- [ ] Short URL result is displayed.
- [ ] Copy functionality works.
- [ ] Analytics are displayed.
- [ ] Loading states work.
- [ ] Error states work.
- [ ] Type checking passes.
- [ ] Frontend tests pass.
- [ ] Production build succeeds.

Testing:

- [ ] Backend unit tests pass.
- [ ] Backend API tests pass.
- [ ] Redis integration tests pass.
- [ ] Frontend tests pass.
- [ ] End-to-end critical flows pass.
- [ ] Regression tests exist for important bugs.
- [ ] Clean-environment validation succeeds.

Containers:

- [ ] Backend image builds.
- [ ] Frontend image builds.
- [ ] Redis runs through Compose.
- [ ] Services communicate correctly.
- [ ] Health checks work.
- [ ] Persistent data behavior is understood.
- [ ] Containers use reasonable security defaults.

Infrastructure:

- [ ] Terraform configuration is valid.
- [ ] Terraform plan is reviewed.
- [ ] Infrastructure naming is consistent.
- [ ] Infrastructure state is handled safely.
- [ ] Docker and Terraform responsibilities remain separated.

CI/CD:

- [ ] Backend CI passes.
- [ ] Frontend CI passes.
- [ ] Terraform CI passes.
- [ ] Docker images build successfully.
- [ ] Security scanning runs.
- [ ] Dependency scanning runs.
- [ ] Release workflow is reproducible.
- [ ] GitHub Actions permissions follow least privilege.

Observability:

- [ ] Prometheus scrapes the backend.
- [ ] Application metrics are available.
- [ ] Metrics use bounded labels.
- [ ] Grafana dashboard is provisioned.
- [ ] Request rate is visible.
- [ ] Error rate is visible.
- [ ] Latency is visible.
- [ ] URL creation and redirect activity are visible.
- [ ] Redis failures are observable.

Alerting:

- [ ] Alertmanager is configured.
- [ ] Backend availability alert works.
- [ ] High error-rate alert works.
- [ ] High latency alert works.
- [ ] Redis failure alert works.
- [ ] Alerts are routed correctly.
- [ ] Alert recovery has been verified.

Load Testing:

- [ ] Locust configuration exists.
- [ ] Baseline scenario exists.
- [ ] Stress scenario exists.
- [ ] Recovery scenario exists.
- [ ] Results record meaningful performance data.
- [ ] Tests are restricted to authorized environments.

Security:

- [ ] Server-side input validation exists.
- [ ] Unsafe URL schemes are rejected.
- [ ] Redis is not unnecessarily exposed.
- [ ] Secrets are not committed.
- [ ] Error responses do not leak internals.
- [ ] Logs do not leak secrets.
- [ ] Metrics do not contain sensitive data.
- [ ] Dependency scanning passes.
- [ ] Container scanning passes.
- [ ] GitHub Actions permissions are restricted.
- [ ] Terraform state is protected.

Documentation:

- [ ] README explains the project.
- [ ] Architecture is documented.
- [ ] Local development is documented.
- [ ] Environment configuration is documented.
- [ ] API behavior is documented.
- [ ] Monitoring is documented.
- [ ] Alerting is documented.
- [ ] Load testing is documented.
- [ ] Security considerations are documented.
- [ ] Important architectural decisions are documented.
- [ ] Documentation matches actual implementation.

## 294. Final Engineering Principles

The project should optimize for:

correctness over cleverness

clarity over abstraction

security over convenience

observability over guesswork

reproducibility over manual configuration

tests over assumptions

measured performance over speculation

small justified changes over unnecessary rewrites

The project should be impressive because the engineering decisions are sound, not because the architecture is unnecessarily large.

A small system implemented carefully demonstrates stronger engineering judgment than a complicated system that cannot be explained, tested, or operated.

## 295. Final Agent Rule

When uncertain, preserve the simplest architecture that satisfies the actual requirement.

Before introducing complexity, ask:

- What problem does this solve?
- Is the problem real in this project?
- Can the existing architecture solve it?
- What new operational cost does it introduce?
- How will it be tested?
- How will it be monitored?
- How will it be recovered?
- How will it be documented?

If those questions cannot be answered clearly, do not introduce the complexity yet.

The final implementation should remain understandable to another engineer who did not build it.

