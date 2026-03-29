"""Prometheus metrics middleware and business counters."""

import time

from fastapi import FastAPI
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from starlette.requests import Request
from starlette.responses import Response

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

ACTIVE_REQUESTS = Gauge(
    "active_requests",
    "Number of active HTTP requests",
)

VIDEO_VIEWS_TOTAL = Counter(
    "video_views_total",
    "Total successful video views (business)",
)


def setup_metrics(app: FastAPI) -> None:
    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        path = request.url.path
        if path == "/metrics":
            return await call_next(request)

        ACTIVE_REQUESTS.inc()
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration = time.perf_counter() - start
            REQUEST_COUNT.labels(request.method, path, "500").inc()
            REQUEST_DURATION.labels(path).observe(duration)
            ACTIVE_REQUESTS.dec()
            raise

        duration = time.perf_counter() - start
        status = str(response.status_code)
        REQUEST_COUNT.labels(request.method, path, status).inc()
        REQUEST_DURATION.labels(path).observe(duration)
        ACTIVE_REQUESTS.dec()
        return response

    @app.get("/metrics")
    async def metrics_endpoint():
        data = generate_latest()
        return Response(data, media_type=CONTENT_TYPE_LATEST)
