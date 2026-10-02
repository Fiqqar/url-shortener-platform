# Phase 4: Prometheus & Grafana Observability

## 122. Phase 4 — Prometheus & Grafana Observability

Observability is part of the application design, not an afterthought.

The platform must expose enough telemetry to answer:

- Is the backend healthy?
- How much traffic is the backend receiving?
- How many requests are failing?
- How long do requests take?
- How many URLs are being created?
- How many redirects are occurring?
- Is Redis becoming unavailable or error-prone?
- Can an operator detect degradation before users report it?

The observability stack consists of:

- FastAPI application metrics
- Prometheus
- Grafana
- Alertmanager in the following phase
- Docker/container health information where appropriate

Monitoring failures must not become application failures.

## 123. Monitoring Directory Structure

The monitoring directory should follow this structure:

monitoring/
├── prometheus/
│   ├── prometheus.yml
│   └── rules/
│       ├── backend.yml
│       └── infrastructure.yml
├── grafana/
│   ├── dashboards/
│   │   └── url-shortener.json
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml
│       └── dashboards/
│           └── dashboard.yml
└── alertmanager/
    └── alertmanager.yml

Prometheus configuration belongs under:

monitoring/prometheus/

Grafana provisioning configuration belongs under:

monitoring/grafana/provisioning/

Dashboard JSON files belong under:

monitoring/grafana/dashboards/

Important Grafana configuration must be reproducible from repository files.

Do not manually configure the dashboard in the Grafana UI and treat that configuration as the source of truth.

## 124. FastAPI Metrics

The backend must expose Prometheus-compatible metrics.

Use:

prometheus-fastapi-instrumentator

for FastAPI HTTP instrumentation.

The application should initialize the instrumentator during FastAPI startup/bootstrap using the API supported by the installed library version.

The expected integration pattern is conceptually:

from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)

Do not blindly copy this snippet if the installed dependency version uses a different API.

The implementation must be verified against the actual installed package version.

The backend must expose:

/metrics

The endpoint must return Prometheus-compatible metrics.

The application must continue functioning if Prometheus is temporarily unavailable.

## 125. Instrumented HTTP Metrics

The FastAPI instrumentation should provide HTTP-level telemetry such as:

- request count
- request duration
- HTTP status information
- request method
- request handler/path information where supported
- in-progress requests where supported

Do not assume exact metric names from memory.

Metric names and labels must be verified against the actual output of:

curl http://localhost:<backend-port>/metrics

Documentation and Grafana queries must use the actual metric names produced by the installed version.

## 126. Custom Application Metrics

Default HTTP instrumentation is not enough.

The backend should expose application-level metrics for important business operations.

At minimum, provide metrics for:

- URL creation
- URL redirects
- analytics requests
- application errors
- Redis failures

Recommended conceptual metrics:

url_shortener_urls_created_total
url_shortener_redirects_total
url_shortener_analytics_requests_total
url_shortener_errors_total
url_shortener_redis_errors_total

Metric names may be adjusted to follow the naming conventions of the actual implementation.

Counters should use _total semantics where appropriate.

Custom metrics should be incremented at the service/business-logic layer rather than duplicated independently in every HTTP route.

For example:

- URL creation service increments the URL creation counter.
- Redirect service increments the redirect counter.
- Analytics service increments the analytics request counter.
- Infrastructure/database exception handling increments the relevant error counter.

This prevents the same business operation from being counted multiple times when several API routes call the same service.

## 127. Metric Labels

Labels must remain low-cardinality.

Acceptable examples:

method
status
route
operation
error_type

Avoid using unbounded values as labels.

Never use these as Prometheus labels:

- full URL
- short code
- user ID
- IP address
- User-Agent
- request ID
- arbitrary exception message

Do not create one time series per URL.

For example, this is unacceptable:

redirects_total{short_code="abc123"}

because the number of short codes can grow indefinitely.

Prefer:

redirects_total{operation="redirect"}

or another bounded label set.

High-cardinality metrics can cause memory growth and make Prometheus significantly more expensive to operate.

## 128. Histogram Usage

Latency should be represented using histogram metrics where practical.

The observability stack should support queries for:

- p50
- p95
- p99

request latency.

Do not calculate latency percentiles by averaging request durations.

Use Prometheus histogram functions such as:

histogram_quantile(...)

against the actual histogram bucket metric emitted by the installed instrumentation.

Grafana panels must use the real metric names from /metrics.

## 129. Prometheus Configuration

Create:

monitoring/prometheus/prometheus.yml

The configuration should define:

- global scrape interval
- evaluation interval
- backend scrape job
- rule files
- appropriate scrape timeout

The backend should be discoverable through the Docker Compose network.

Prefer service names over hardcoded container IP addresses.

Example conceptual target:

backend:<port>

Do not configure Prometheus against a dynamically assigned container IP.

The Prometheus scrape configuration must target:

/metrics

on the backend service.

## 130. Prometheus Scrape Configuration

The backend scrape job should have a clear name such as:

url-shortener-backend

Keep labels useful and bounded.

Recommended static labels may include:

service="url-shortener-backend"
environment="local"

Do not attach request-level or URL-level data to Prometheus target labels.

If multiple environments are introduced later, use environment-specific configuration rather than duplicating application logic.

## 131. Prometheus Rule Evaluation

Prometheus should load rule files from:

monitoring/prometheus/rules/

Keep alerting rules separate from the main Prometheus configuration.

Use descriptive filenames:

backend.yml
infrastructure.yml

Rules should be readable and independently reviewable.

Do not place dozens of unrelated rules into one large configuration file.

Each rule should contain:

- clear alert name
- expression
- duration where appropriate
- severity
- useful annotations
- concise description

The actual alert definitions will be expanded in the Alertmanager phase.

## 132. Grafana Provisioning

Grafana must be configured through provisioning files.

The Prometheus datasource should be automatically created from:

monitoring/grafana/provisioning/datasources/prometheus.yml

The dashboard provider should be configured from:

monitoring/grafana/provisioning/dashboards/dashboard.yml

Dashboards should load from:

monitoring/grafana/dashboards/

The goal is:

docker compose up

followed by Grafana startup should produce a usable dashboard without requiring manual configuration through the Grafana UI.

Do not rely on undocumented manual dashboard state.

## 133. Grafana Dashboard

Create one primary dashboard for the URL Shortener platform.

Suggested dashboard title:

URL Shortener Platform

The dashboard should prioritize operational information over visual decoration.

Recommended panels:

Traffic:
- requests per second
- request rate by route
- redirects per second
- URL creation rate

Reliability:
- HTTP 4xx rate
- HTTP 5xx rate
- application error rate
- Redis error rate

Latency:
- p50 latency
- p95 latency
- p99 latency

Application Operations:
- URLs created
- redirects
- analytics requests

Use counter rates for time-series views and cumulative counters where useful.

## 134. Grafana Dashboard Design Rules

The dashboard should be readable at a glance.

Recommended structure:

Row 1:
- Request Rate
- Error Rate
- P95 Latency

Row 2:
- Redirect Rate
- URL Creation Rate
- Analytics Request Rate

Row 3:
- P50 Latency
- P99 Latency
- Redis Errors

Row 4:
- Backend / Process Health

Exact layout may change based on available metrics.

Use meaningful panel titles.

Use units correctly:

- requests/sec
- seconds or milliseconds
- count
- percentage

Do not display raw Prometheus values without explaining what they represent.

## 135. PromQL Rules

PromQL queries should be written for operational meaning rather than simply exposing raw counters.

For counters, use functions such as:

rate(...)

or:

increase(...)

depending on the panel's purpose.

For latency histograms, use:

histogram_quantile(...)

with the appropriate bucket series.

Do not hardcode metric names before verifying the actual output of /metrics.

If the instrumentation library changes metric names, update Grafana queries accordingly.

## 136. Backend Metrics Verification

Before considering observability complete, manually verify:

GET /metrics

returns metrics successfully.

Then generate application traffic:

POST /api/v1/urls
GET /<short-code>
GET /api/v1/urls/<short-code>/analytics

After generating traffic, confirm that relevant counters change.

At minimum verify:

1. HTTP request metrics change.
2. URL creation metrics change.
3. Redirect metrics change.
4. Analytics metrics change.
5. Error metrics change when a controlled error is generated.
6. Grafana displays the resulting activity.
7. Prometheus successfully scrapes the backend.

## 137. Redis Observability

Redis health must be observable.

The application should expose Redis failures through application metrics when Redis operations fail.

At minimum distinguish, where reliably possible:

- Redis unavailable
- Redis operation error
- Redis timeout

Do not expose raw Redis exception strings as Prometheus labels.

Redis connectivity should also be represented in:

/health

and/or:

/ready

according to the semantics defined during backend implementation.

Readiness should fail when the application cannot perform dependencies required for normal operation.

Liveness should not necessarily fail merely because Redis is temporarily unavailable.

Do not conflate liveness with dependency readiness.

## 138. Health vs Readiness

Use:

/health

for basic application liveness.

Use:

/ready

for whether the service is ready to handle normal traffic.

Conceptually:

/health
    process is alive

/ready
    process is alive
    required dependencies are reachable

The exact dependency checks should match the application's actual startup/runtime requirements.

Do not perform unnecessarily expensive dependency checks on every liveness probe.

## 139. Monitoring Failure Isolation

Monitoring must not become a single point of failure.

If Prometheus is down:

backend continues serving requests

If Grafana is down:

backend continues serving requests

If Alertmanager is down:

backend continues serving requests
Prometheus continues collecting metrics

The application must not make synchronous calls to Grafana, Prometheus, or Alertmanager as part of normal request handling.

Metrics collection should remain lightweight and non-blocking from the perspective of normal API behavior.

## 140. Observability Local Development

Local development should support starting the observability stack through Docker Compose.

Expected architecture:

Browser
   |
Frontend
   |
Backend
   |
Redis

Prometheus ---> Backend /metrics
    |
    v
Grafana

Alertmanager will consume Prometheus alerts in the next phase.

Keep monitoring services on the same Docker network where required.

Do not expose every monitoring port publicly by default.

For local development, exposing Grafana and Prometheus to localhost is acceptable.

For production-like deployments, access should be restricted appropriately.

## 141. Observability Security

Do not expose sensitive application data through metrics.

Metrics must never contain:

- private URLs
- credentials
- API keys
- tokens
- cookies
- authorization headers
- request bodies
- raw IP addresses unless explicitly required and reviewed

Do not log or metricize secrets for debugging convenience.

Observability data is production data and must be treated accordingly.

## 142. Observability Documentation

The README should document:

- where /metrics is exposed
- how to access Prometheus locally
- how to access Grafana locally
- dashboard purpose
- how to verify scraping
- how to generate sample traffic
- where Prometheus rules are stored
- where Grafana dashboards are stored

Example local service URLs may be documented once actual Docker Compose ports are finalized.

Do not document ports that are not actually configured.

## 143. Phase 4 Definition of Done

Phase 4 is complete when:

- [ ] Backend exposes /metrics.
- [ ] prometheus-fastapi-instrumentator is used for FastAPI HTTP instrumentation.
- [ ] Prometheus successfully scrapes the backend.
- [ ] HTTP request metrics are visible.
- [ ] URL creation metrics are visible.
- [ ] Redirect metrics are visible.
- [ ] Analytics metrics are visible.
- [ ] Error metrics are visible.
- [ ] Redis failures are observable.
- [ ] Metrics use bounded labels.
- [ ] No raw URL/code/IP data is used as unbounded metric labels.
- [ ] Latency can be inspected at p50/p95/p99 where supported.
- [ ] Grafana datasource is provisioned automatically.
- [ ] Grafana dashboard is provisioned automatically.
- [ ] Dashboard shows traffic, reliability, latency, and application operations.
- [ ] Monitoring failures do not stop the backend.
- [ ] README documents the observability stack.
- [ ] Metrics have been manually verified with real application traffic.


