# Release Workflow, Branching & Commits

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

Repository commits and pushes are made with the `relay` CLI (`relay --solo`). Relay stages the changes, writes a Conventional Commit message, and pushes to the current branch. Relay 2.5.0 is the version currently in use.

Common flags:

    relay --solo --staged   # commit only what is already staged
    relay --solo --no-push  # commit without pushing
    relay --solo --dry-run  # show the plan without changing anything
    relay --solo -m "fix: handle missing short codes"   # fixed message instead of AI generation

Without `--staged`, relay stages all working-tree changes (`git add .`) before committing, so stage the intended files first when the tree contains unrelated edits.

Relay is a local developer tool; CI validates the pushed commits regardless of how they were created.

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


