# Backend Design, Data Model, Config & Error Handling

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

The values currently supported by `backend/app/core/config.py` are:

    REDIS_HOST=redis
    REDIS_PORT=6379
    REDIS_DB=0
    BASE_URL=http://localhost:8000
    LOG_LEVEL=INFO
    CORS_ORIGINS=http://localhost:5173,http://localhost:3000
    MAX_BODY_BYTES=32768

Uvicorn bind host and port are set by the Docker command or the local run command; they are not read from application settings.

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


