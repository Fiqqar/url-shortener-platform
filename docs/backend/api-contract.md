# Backend Architecture: API Contract

# Part 2: Backend Architecture & Data Model

## 12. API Contract

The backend API must use explicit request and response schemas.

FastAPI route handlers should not contain large amounts of business logic.

Prefer the following separation:

    API Router
        |
        v
    Service Layer
        |
        v
    Repository Layer
        |
        v
    Redis

### 12.1 Create URL

Endpoint:

    POST /api/v1/urls

Request:

    {
      "url": "https://example.com/some/long/path"
    }

Responsibilities:

- validate the URL
- generate a unique short code
- store the mapping
- initialize analytics data
- return the created resource

Expected success status:

    201 Created

Possible client errors:

    400 Bad Request
    422 Unprocessable Entity

The API should return structured JSON error responses.

### 12.2 Get URL Information

Endpoint:

    GET /api/v1/urls/{code}

Purpose:

Return metadata about a shortened URL without performing a browser redirect.

Possible response:

    {
      "code": "aB3xY7",
      "short_url": "http://localhost:8000/aB3xY7",
      "target_url": "https://example.com/some/long/path",
      "clicks": 42
    }

If the short code does not exist:

    404 Not Found

### 12.3 URL Analytics

Endpoint:

    GET /api/v1/urls/{code}/analytics

Purpose:

Return analytics associated with a shortened URL.

The initial implementation should remain simple.

Possible response:

    {
      "code": "aB3xY7",
      "clicks": 42
    }

Additional analytics fields may be added later.

### 12.4 Redirect

Endpoint:

    GET /{code}

Purpose:

Redirect the client to the target URL.

Success:

    3xx redirect

Missing code:

    404 Not Found

Invalid code:

    400 Bad Request

Internal infrastructure failures should return a generic server error rather than exposing implementation details.

### 12.5 Health

Endpoint:

    GET /health

Purpose:

Determine whether the application process is alive.

The liveness endpoint should not perform expensive operations.

Expected response:

    {
      "status": "ok"
    }

### 12.6 Readiness

Endpoint:

    GET /ready

Purpose:

Determine whether the application can serve traffic.

The readiness check may verify Redis connectivity.

Possible response:

    {
      "status": "ready"
    }

If required dependencies are unavailable:

    503 Service Unavailable

---

