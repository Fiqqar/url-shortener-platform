# Agent Restrictions & Dependency Rules

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

