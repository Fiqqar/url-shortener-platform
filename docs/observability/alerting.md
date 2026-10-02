# Phase 5: Alerting & Failure Injection

## 144. Phase 5 — Alerting & Load Testing

The platform must not only collect metrics.

It must also:

- detect meaningful failures
- distinguish warning conditions from critical conditions
- route alerts through Alertmanager
- validate alert conditions
- generate controlled traffic
- measure application behavior under load
- verify recovery after failures

Alerting should be actionable.

Do not create alerts for every unusual metric change.

An alert should represent a condition that requires investigation or action.

## 145. Alerting Architecture

The monitoring architecture is:

Application
    |
    v
Prometheus
    |
    v
Alertmanager
    |
    v
Notification Target

Grafana is used for visualization and investigation.

Prometheus evaluates alert rules.

Alertmanager handles alert grouping, routing, and notification delivery.

The backend must never send alerts directly to notification providers during normal request handling.

## 146. Alertmanager Configuration

Create:

monitoring/alertmanager/alertmanager.yml

Alertmanager configuration should define:

- global configuration
- route configuration
- grouping
- repeat interval
- receiver definitions

Local development may use a simple receiver such as a webhook or another test destination.

Do not hardcode production credentials into the repository.

Secrets must be supplied through environment variables, Docker secrets, GitHub Actions secrets, or the deployment platform's secret manager.

## 147. Alert Severity

Use a small and consistent severity model.

Recommended levels:

warning
critical

Use warning for conditions that indicate degradation but do not necessarily represent an immediate outage.

Use critical for conditions that represent a major service failure or sustained inability to serve traffic.

Do not create unnecessary severity levels unless a concrete operational requirement exists.

## 148. Backend Alert Rules

Backend alert rules should cover meaningful failure modes.

Recommended alerts include:

- backend unavailable
- high HTTP 5xx rate
- sustained high request latency
- excessive application errors
- Redis dependency failure
- abnormal request saturation where measurable

Alert names should be descriptive.

Examples include:

BackendDown
BackendHighErrorRate
BackendHighLatency
RedisUnavailable

Exact names may be adjusted to the repository's naming convention.

## 149. Backend Availability Alert

The backend availability alert should detect when Prometheus can no longer successfully scrape the backend.

The alert should use the Prometheus scrape health signal for the backend service.

The alert should include a short delay before firing so that transient restarts do not immediately create noisy alerts.

The delay should be long enough to avoid normal container restart noise while remaining useful for genuine outages.

The alert annotation should identify:

- affected service
- environment
- reason

Do not include sensitive information.

## 150. High Error Rate Alert

The platform should detect sustained HTTP 5xx errors.

Do not alert on a single failed request.

Use an error rate calculated over a time window.

The exact PromQL expression must use the actual HTTP metrics emitted by the installed instrumentation.

The alert should only fire after the condition remains true for a meaningful duration.

Avoid hardcoding an arbitrary threshold without documenting why it exists.

For local development, thresholds may intentionally be lower so that failure injection is easy to demonstrate.

For production-like environments, thresholds should be tuned using observed baseline traffic.

## 151. High Latency Alert

Create an alert for sustained high request latency.

Use histogram metrics where available.

The alert should focus on a percentile such as p95 rather than average latency.

The threshold must be configurable and documented.

Do not choose a threshold solely because it produces a visually interesting Grafana graph.

## 152. Redis Failure Alert

The platform should detect Redis dependency failures.

Possible signals include:

- Redis error counter rate
- readiness failures
- application errors attributable to Redis
- dependency health metrics where available

The alert should avoid firing solely because one Redis request failed.

Use sustained failure or a meaningful error rate.

If Redis becomes unavailable, the alert should provide enough context to identify Redis as the affected dependency.

## 153. Alert Labels and Annotations

Alert labels should remain low-cardinality.

Recommended labels:

- alertname
- severity
- service
- environment

Annotations should provide human-readable context.

Recommended annotations:

- summary
- description

Do not put arbitrary request IDs, URLs, short codes, IP addresses, or exception strings into alert labels.

Do not create separate alerts for every URL or user.

## 154. Alert Grouping

Alertmanager should group related alerts.

For example, if the backend becomes unavailable, Prometheus may produce several related symptoms.

Alertmanager should prevent a single outage from becoming dozens of duplicate notifications.

Group by bounded dimensions such as:

- alertname
- service
- environment

The exact grouping strategy may be adjusted as the alert set grows.

## 155. Alert Routing

Routing should distinguish at least:

warning
critical

Critical alerts should receive more immediate notification treatment than warnings.

Local development may route both severities to the same test receiver.

Production deployments may route critical alerts to a more urgent destination.

Do not commit production notification URLs, tokens, passwords, or API keys.

## 156. Alert Testing

Every alert must be tested intentionally.

Do not consider an alert complete merely because Prometheus accepts the configuration.

Testing should verify:

1. condition becomes true
2. Prometheus evaluates the rule
3. alert enters pending or firing state
4. Alertmanager receives the alert
5. Alertmanager routes the alert correctly
6. notification target receives the expected alert
7. recovery causes the alert to resolve

Document how each alert can be tested locally.

## 157. Failure Injection

Failure injection must be controlled and reversible.

Examples include:

- stopping Redis
- restarting Redis
- stopping the backend
- restarting the backend
- generating controlled HTTP 5xx responses
- introducing artificial latency in a development-only code path
- generating sustained request traffic

Do not introduce failure injection into production code without an explicit feature flag and deployment policy.

Failure injection must never require modifying source code manually just to restore normal behavior.

## 158. Redis Failure Scenario

A Redis failure test should validate:

1. Redis is healthy.
2. Backend is healthy.
3. Normal URL creation works.
4. Redis is made unavailable.
5. Backend dependency behavior is observed.
6. readiness reflects the intended state.
7. Redis-related metrics increase.
8. Redis alert becomes active if thresholds are met.
9. Redis is restored.
10. Backend recovers.
11. Alert resolves.

The test must distinguish between:

liveness failure

and:

readiness or dependency failure.

Do not automatically restart the backend merely because Redis is unavailable unless that behavior is explicitly required.

## 159. Backend Failure Scenario

A backend failure test should validate:

1. Prometheus can initially scrape the backend.
2. Grafana displays normal traffic.
3. Backend is stopped.
4. Prometheus detects the scrape failure.
5. Backend availability alert fires.
6. Grafana reflects the outage.
7. Backend is restarted.
8. Prometheus detects recovery.
9. Alert resolves.

The expected recovery path must be documented.

## 160. Controlled HTTP Error Scenario

The application should have a safe development or testing mechanism for generating controlled errors.

Possible approaches include:

- dedicated test endpoint disabled outside test environments
- dependency injection that forces a known exception
- mocked service failure
- integration-test-only failure hook

Do not add an undocumented production endpoint for intentionally crashing the application.

Any failure injection mechanism must be explicitly scoped to development or testing.

