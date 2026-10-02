# Coding, Naming, Logging, Metrics & Alert Conventions

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

