# Phase 6: Security QA, Recovery & Release Validation

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


