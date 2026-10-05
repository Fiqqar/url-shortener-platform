# Phase 3: CI/CD Pipeline & Security Automation

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

The workflows currently implemented in this repository are `backend-ci.yml`, `frontend-ci.yml`, `terraform-ci.yml`, `docker-ci.yml`, and `monitoring-ci.yml`, which validates the Prometheus and Grafana configuration under `monitoring/`.

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

Every action in `.github/workflows/` is pinned to a full-length immutable commit SHA, with the exact release as a trailing comment:

    - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1

For annotated tags, pin the peeled commit SHA (the commit the tag points to), not the tag object SHA. Tags can move or be repointed; commit SHAs cannot.

The trailing version comment keeps updates reviewable and lets Dependabot's `github-actions` ecosystem bump the SHA and the comment together.

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

