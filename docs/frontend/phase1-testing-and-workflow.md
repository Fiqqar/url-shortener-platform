# Phase 1: Testing, Code Quality & Local Workflow

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


