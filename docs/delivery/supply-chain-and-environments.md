# Dependency Governance, CI Security, Terraform Security & Environments

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

Every action in `.github/workflows/` is pinned to a full-length immutable commit SHA with its release version as a trailing comment (`owner/action@<40-char-commit-sha> # vX.Y.Z`). For annotated tags, the pinned SHA is the peeled commit SHA, not the tag object SHA.

When updating an action:

- review the release
- update the pinned SHA and the version comment
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

