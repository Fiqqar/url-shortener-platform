"""Locust load test for url-shortener-platform.

Default target is local development only. Override with LOCUST_HOST
env var or ``locust --host <url>``. Never point stress runs at
production or any host you are not authorized to test.

Behavior distribution (per user, via task weights):
    - redirect to existing code: weight 10 (~59% of tasks, read-heavy)
    - request analytics:           weight 3  (~18%)
    - get URL info:                weight 2  (~12%)
    - create short URL:            weight 1  (~6%, only writer)
    - invalid / unknown code:      weight 1  (~6%, error-path coverage)

Redirects reuse a per-user pool of codes seeded in ``on_start``
(5 codes) instead of creating a new URL per request, so redirect
throughput reflects read performance. Newly created codes are added
to the pool (bounded at 50) to keep the working set realistic.
"""

import os
import random

from locust import HttpUser, between, task  # type: ignore[import-not-found]

DEFAULT_HOST = os.environ.get("LOCUST_HOST", "http://localhost:8000")

# Safe, non-customer test destinations only (no real user data).
TEST_TARGETS = [
    "https://example.com/",
    "https://example.com/some/long/path",
    "https://example.com/articles/load-test",
]

SEED_POOL_SIZE = 5
MAX_POOL_SIZE = 50

# Alphanumeric + unlikely to collide with seeded codes -> expect 404.
UNKNOWN_CODE = "noSuchCode000"
# Fails CODE_RE (^[0-9A-Za-z]{1,32}$) -> expect 400.
MALFORMED_CODE = "!!!not-a-code!!!"


class ShortenerUser(HttpUser):
    """Simulates one API consumer creating, resolving, and inspecting URLs."""

    host = DEFAULT_HOST
    wait_time = between(0.1, 0.5)

    def on_start(self) -> None:
        self.codes: list[str] = []
        for _ in range(SEED_POOL_SIZE):
            code = self._create_code(seed=True)
            if code:
                self.codes.append(code)

    def _create_code(self, seed: bool = False) -> str | None:
        label = "POST /api/v1/urls (seed)" if seed else "POST /api/v1/urls"
        with self.client.post(
            "/api/v1/urls",
            json={"url": random.choice(TEST_TARGETS)},
            name=label,
            catch_response=True,
        ) as resp:
            if resp.status_code == 201:
                try:
                    code = resp.json().get("code")
                except ValueError:
                    code = None
                if code:
                    resp.success()
                    return code
                resp.failure("201 without code in body")
            else:
                resp.failure(f"unexpected status {resp.status_code}")
        return None

    def _pick_code(self) -> str | None:
        return random.choice(self.codes) if self.codes else None

    @task(10)
    def redirect_existing(self) -> None:
        code = self._pick_code()
        if code is None:
            code = self._create_code()
            if code is None:
                return
            self.codes.append(code)
        # Do NOT follow the redirect: the target is an external test
        # destination (example.com) and must not receive load.
        with self.client.get(
            f"/{code}",
            name="GET /{code} (redirect)",
            allow_redirects=False,
            catch_response=True,
        ) as resp:
            if resp.status_code in (301, 302, 303, 307, 308):
                resp.success()
            else:
                resp.failure(f"unexpected status {resp.status_code}")

    @task(3)
    def read_analytics(self) -> None:
        code = self._pick_code()
        if code is None:
            return
        self.client.get(
            f"/api/v1/urls/{code}/analytics",
            name="GET /api/v1/urls/{code}/analytics",
        )

    @task(2)
    def read_url_info(self) -> None:
        code = self._pick_code()
        if code is None:
            return
        self.client.get(
            f"/api/v1/urls/{code}",
            name="GET /api/v1/urls/{code}",
        )

    @task(1)
    def create_url(self) -> None:
        code = self._create_code()
        if code:
            self.codes.append(code)
            if len(self.codes) > MAX_POOL_SIZE:
                self.codes.pop(0)

    @task(1)
    def invalid_code(self) -> None:
        # Expected error responses (404/400) are marked successful so the
        # failure rate only reflects unexpected behavior (e.g. 5xx).
        if random.random() < 0.5:
            with self.client.get(
                f"/{UNKNOWN_CODE}",
                name="GET /{code} (unknown -> 404)",
                allow_redirects=False,
                catch_response=True,
            ) as resp:
                if resp.status_code == 404:
                    resp.success()
                else:
                    resp.failure(f"expected 404, got {resp.status_code}")
        else:
            with self.client.get(
                f"/{MALFORMED_CODE}",
                name="GET /{code} (malformed -> 400)",
                allow_redirects=False,
                catch_response=True,
            ) as resp:
                if resp.status_code == 400:
                    resp.success()
                else:
                    resp.failure(f"expected 400, got {resp.status_code}")
