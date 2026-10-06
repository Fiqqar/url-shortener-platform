# Load testing (Locust)

Intended for **local or staging environments you own** only.
Do **not** target production or any external host without explicit
written authorization. The default target is local development.

## Prerequisites

- Stack running locally: `docker compose up -d --build` (backend on
  `http://localhost:8000`, Redis healthy)
- Monitoring up (to correlate results):
  `docker compose up -d prometheus grafana`
- Python 3.12+ with Locust installed:

~~~powershell
pip install -r loadtest/requirements.txt
locust --version
~~~

## Target configuration

No source-code change needed. Host resolution order:

1. `locust --host <url>` (highest priority)
2. `LOCUST_HOST` env var
3. default `http://localhost:8000`

~~~powershell
# default (local)
locust -f loadtest/locustfile.py

# explicit host via CLI
locust -f loadtest/locustfile.py --host http://localhost:8000

# explicit host via env
$env:LOCUST_HOST = "http://localhost:8000"
locust -f loadtest/locustfile.py
~~~

Test destinations are safe placeholders (`https://example.com/...`);
no real external URLs or customer data are used. Redirect requests
use `allow_redirects=False`, so `example.com` never receives load.

## Behavior model (`locustfile.py`)

Per-user task weights (read-heavy, realistic mix):

| Task | Weight | Share* | Endpoint |
|---|---|---|---|
| redirect existing | 10 | ~59% | `GET /{code}` (no redirect follow) |
| analytics | 3 | ~18% | `GET /api/v1/urls/{code}/analytics` |
| URL info | 2 | ~12% | `GET /api/v1/urls/{code}` |
| create | 1 | ~6% | `POST /api/v1/urls` |
| invalid code | 1 | ~6% | unknown code (404) / malformed (400) |

\* Approximate; Locust picks tasks probabilistically.

Each virtual user seeds **5 codes** in `on_start` and reuses them for
redirect/analytics/info reads. Newly created codes join the pool
(bounded at 50) instead of one-URL-per-request, so redirect
throughput measures read performance, not write throughput.

## Scenarios

### 1. Baseline — establish normal behavior

~~~powershell
locust -f loadtest/locustfile.py --host http://localhost:8000 `
  --headless -u 10 -r 2 -t 2m --csv=baseline --html=baseline.html
~~~

Record at minimum: concurrency (10), duration (2m), request rate (RPS),
p50 / p95 / p99 latency, HTTP error rate — plus environment details:
CPU, RAM, Docker resource limits, Redis config (`redis:7-alpine`,
appendonly on), backend config (uvicorn workers, `REDIS_HOST=redis`).
This baseline is the reference for stress/recovery comparisons; do not
compare runs across materially different machines or configs.

### 2. Stress — find degradation point

Step concurrency up in stages, e.g. 25 → 50 → 100 users, 5m each:

~~~powershell
locust -f loadtest/locustfile.py --host http://localhost:8000 `
  --headless -u 50 -r 5 -t 5m --csv=stress-50 --html=stress-50.html
~~~

Observe: latency degradation (p95/p99), 4xx vs 5xx rate, Redis errors,
`docker stats` CPU/memory, container restarts (`docker compose ps`).
Stop stepping up when p95 exceeds **0.5s** for 2m (matches the
`HighLatency` alert) or 5xx exceeds **5%** (matches `HighErrorRate`).

### 3. Recovery — verify behavior after failure

1. Start baseline traffic (`-u 10 -r 2`, no `-t` so it runs open-ended).
2. Inject a controlled failure (pick one):
   `docker stop url-shortener-platform-backend-1` or
   `docker stop url-shortener-platform-redis-1`.
3. Observe errors in Locust + `BackendDown` / `RedisDown` firing in
   Prometheus (`http://localhost:9090/alerts`) and Alertmanager
   (`http://localhost:9093`).
4. Restore: `docker start <container>`, wait for healthy
   (`docker compose ps`, `GET /ready` returns `ready`).
5. Keep traffic running, verify error rate drops to baseline and no
   manual data reconstruction is needed (Redis persistence on,
   backend reconnects, Prometheus resumes scraping).

## Expected metrics (watch in Grafana + Locust together)

- Locust: RPS, p50/p95/p99, failures/s, per-endpoint breakdown
  (redirect should dominate throughput).
- Grafana dashboard "URL Shortener Platform": request + error rate,
  p50/p95/p99 latency, redirect / creation / analytics rates, Redis
  and application errors, scrape-target health, process memory.
- Prometheus alerts during runs: `BackendDown`, `HighErrorRate`
  (>5% 5xx for 2m), `HighLatency` (p95 >0.5s for 2m), `RedisDown`.

## How to interpret results

- A run is **not** judged by Locust success % alone. Correlate every
  run with Grafana/Prometheus: same RPS with rising p95 or Redis
  errors = regression even at 100% Locust success.
- Baseline vs stress: compare only same hardware/config. Note any
  Docker limit, Redis, or backend setting change alongside numbers.
- Known-good local shape: redirect p95 well under 0.5s at 10 users;
  invalid-code tasks return 404/400 (expected, counted separately
  from 5xx). Rising 5xx or `RedisDown`/`BackendDown` = stop and
  investigate backend logs (`docker compose logs backend --tail 50`)
  before pushing concurrency higher.

## Safety restrictions

- Default target is `http://localhost:8000`. No default config points
  at production or any unspecified external host.
- Never run the stress scenario against shared/staging hosts without
  owner approval, and never against production.
- Keep `--headless -u/-r/-t` bounded; do not raise file-descriptor or
  container-memory limits just to force higher numbers on a laptop.
