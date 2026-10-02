# Phase 6: QA Strategy & Testing Layers

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

