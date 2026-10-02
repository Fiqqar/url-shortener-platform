# Change Scope, Compatibility & Migrations

## 253. Phase 8 — Agent Operating Rules

Agents working on this repository must preserve the project's architecture, conventions, and engineering goals.

Before making changes, an agent should:

1. inspect the relevant files
2. understand existing abstractions
3. identify dependencies between components
4. determine the smallest correct change
5. implement the change
6. run relevant validation
7. review the resulting diff
8. update documentation when behavior changes

Do not rewrite unrelated code simply because another implementation style appears preferable.

Prefer incremental, reviewable changes.

## 254. Existing Code Takes Precedence

Before introducing a new abstraction, inspect whether the repository already provides one.

Examples include:

- existing configuration classes
- existing Redis clients
- existing API dependencies
- existing error handlers
- existing metric collectors
- existing test fixtures
- existing frontend API services
- existing shared TypeScript types

Do not create duplicate abstractions for the same responsibility.

If an existing abstraction is inadequate, improve it rather than silently bypassing it.

## 255. Change Scope

Keep changes focused.

A feature change should not automatically trigger unrelated:

- formatting changes
- dependency upgrades
- architecture rewrites
- file renames
- framework migrations
- dashboard redesigns

Unrelated cleanup should be performed separately unless it is required for correctness.

This keeps pull requests understandable and reduces regression risk.

## 256. Backward Compatibility

When changing an existing API or internal contract, consider existing consumers.

Before changing:

- endpoint paths
- request fields
- response fields
- status codes
- Redis key formats
- environment variable names
- metric names
- dashboard queries

identify affected components.

Update all affected consumers in the same change where practical.

Avoid silently breaking existing behavior.

## 257. API Evolution

API changes should be intentional.

For breaking changes:

1. identify the affected endpoint
2. update schemas
3. update backend implementation
4. update backend tests
5. update frontend types
6. update frontend API services
7. update frontend components
8. update documentation
9. validate end-to-end behavior

Keep the v1 API namespace stable unless a breaking change is explicitly required.

## 258. Database and Redis Compatibility

Redis data structures are part of the application's persistence contract.

Changing key formats can invalidate existing data.

Before changing:

- key prefixes
- value formats
- counter semantics
- serialization formats

determine whether existing data must remain compatible.

If migration is required, document the migration strategy.

Do not silently change persistent data formats.

## 259. Migration Strategy

If a future database is introduced, migrations must be explicit.

Do not modify persistent schemas manually and assume the application will remain compatible.

Schema changes should include:

- migration
- rollback consideration
- test coverage
- documentation

For Redis structure changes, document whether:

- existing keys remain compatible
- old keys are migrated
- old keys expire naturally
- data must be regenerated

