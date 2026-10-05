from prometheus_client import Counter

URLS_CREATED = Counter(
    "url_shortener_urls_created_total",
    "Total short URLs created.",
)

REDIRECTS = Counter(
    "url_shortener_redirects_total",
    "Total redirects served.",
)

ANALYTICS_REQUESTS = Counter(
    "url_shortener_analytics_requests_total",
    "Total analytics requests served.",
)

ERRORS = Counter(
    "url_shortener_errors_total",
    "Total application errors.",
    ["error_type"],
)

REDIS_ERRORS = Counter(
    "url_shortener_redis_errors_total",
    "Total Redis failures.",
    ["operation"],
)
