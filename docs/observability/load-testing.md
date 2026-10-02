# Phase 5: Locust Load Testing

## 161. Locust Load Testing

Use Locust for HTTP load testing.

Create:

loadtest/locustfile.py

The load test should model realistic platform behavior.

Do not generate traffic against external production systems by default.

The default target must be a local or explicitly configured environment.

## 162. Locust Configuration

The load test target should be configurable.

Prefer an environment variable such as:

LOCUST_HOST

or the standard Locust host configuration.

Do not hardcode the backend address throughout the test code.

The load test should support different environments without source-code modification.

## 163. Locust User Behavior

The load test should simulate multiple operations.

Recommended behavior distribution:

- create short URLs
- redirect to existing short URLs
- request analytics
- occasionally request invalid short codes

The exact distribution should be documented.

Do not create a new short URL for every single request if the purpose is to measure redirect performance.

Use a realistic mixture of reads and writes.

## 164. Locust Test Data

The load test should maintain a reusable pool of valid short codes where appropriate.

The test should:

1. create several URLs
2. capture their short codes
3. reuse those short codes for redirect and analytics requests

This produces a more realistic workload.

Do not hardcode real external URLs or private customer data.

Use safe test destinations such as example.com or another explicitly configured test destination.

## 165. Locust Scenarios

The load-testing documentation should define at least three scenarios.

### Baseline

Purpose:

Establish normal application behavior.

Measure:

- requests per second
- p50 latency
- p95 latency
- p99 latency
- HTTP error rate
- Redis errors
- CPU and memory where available

### Stress

Purpose:

Determine how the system behaves as concurrency increases.

Increase:

- concurrent users
- request rate
- test duration

Observe:

- latency degradation
- error rate
- Redis behavior
- container resource usage

### Recovery

Purpose:

Validate behavior after a dependency or service failure.

Sequence:

1. start baseline traffic
2. inject controlled failure
3. observe alerts and errors
4. restore dependency or service
5. continue traffic
6. verify recovery

## 166. Load Test Safety

Load tests must be explicitly scoped.

Never run stress tests against production infrastructure without authorization.

The default project configuration should target local development.

The README must clearly state that load tests are intended for local or staging environments and must not target production without explicit authorization.

Do not provide a default configuration that could accidentally target an unspecified external host.

## 167. Load Test Metrics

During load testing, monitor:

- request throughput
- request latency
- HTTP 4xx rate
- HTTP 5xx rate
- Redis errors
- backend availability
- CPU usage
- memory usage
- container restarts

Use Prometheus and Grafana to observe the application while Locust generates traffic.

The load test should not be evaluated only by Locust's final success percentage.

Correlate Locust results with application and infrastructure telemetry.

## 168. Performance Baseline

Record a baseline before stress testing.

At minimum capture:

- concurrency
- duration
- request rate
- p50 latency
- p95 latency
- p99 latency
- error rate

Also record relevant environment details:

- CPU
- RAM
- Docker resource limits
- Redis configuration
- backend configuration

Do not compare two benchmark results without considering whether the environments are materially different.

## 169. Load Test Documentation

Create:

loadtest/README.md

Document:

- prerequisites
- target configuration
- baseline scenario
- stress scenario
- recovery scenario
- expected metrics
- safety restrictions
- how to interpret results

The documented workflow must match the project's actual dependency installation and execution method.

## 170. Failure Recovery Principles

The system should recover without requiring manual database or data reconstruction after ordinary development failures.

After restarting Redis:

- existing persistent data should remain when persistence is configured
- backend should reconnect
- readiness should recover
- normal URL operations should resume

After restarting the backend:

- Redis data should remain intact
- frontend should reconnect when requests are made
- Prometheus should resume scraping
- Grafana should resume displaying current data

After restarting monitoring services:

- backend should remain operational
- Prometheus should resume scraping
- Grafana should reconnect to Prometheus
- alerting should resume

## 171. Phase 5 Definition of Done

Phase 5 is complete when:

- [ ] Alertmanager is included in the monitoring stack.
- [ ] Prometheus sends alerts to Alertmanager.
- [ ] Warning and critical severities are defined.
- [ ] Backend availability alert exists.
- [ ] High HTTP error-rate alert exists.
- [ ] High latency alert exists.
- [ ] Redis failure alert exists.
- [ ] Alert labels remain low-cardinality.
- [ ] Alert routing is reproducible from repository configuration.
- [ ] Production secrets are not committed.
- [ ] Alerts have been manually tested.
- [ ] Alert recovery has been tested.
- [ ] Locust is configured.
- [ ] Baseline load testing is documented.
- [ ] Stress testing is documented.
- [ ] Recovery testing is documented.
- [ ] Load tests default to local or staging environments.
- [ ] Redis failure injection has been tested.
- [ ] Backend failure recovery has been tested.
- [ ] Controlled HTTP error handling has been tested.
- [ ] Grafana and Prometheus are used during load testing.
- [ ] Load-test results include latency and error-rate measurements.
- [ ] Failure recovery does not require manual data reconstruction.


