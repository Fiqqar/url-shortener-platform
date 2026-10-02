# Phase 1: Backend Implementation

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

