"""Спостережуваність SurveyLab: метрики Prometheus і (за бажанням) трасування OpenTelemetry."""
import logging
import os

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest  # noqa: F401

logger = logging.getLogger("surveylab")

REQUEST_COUNT = Counter(
    "surveylab_http_requests_total",
    "Кількість HTTP-запитів до SurveyLab API",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "surveylab_http_request_duration_seconds",
    "Тривалість обробки HTTP-запитів, с",
    ["method", "path"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5),
)
SURVEYS_CREATED = Counter(
    "surveylab_surveys_created_total", "Кількість створених опитувань"
)


def render_metrics() -> bytes:
    return generate_latest()


def setup_tracing(app) -> None:
    """Вмикає трасування, якщо задано OTEL_EXPORTER_OTLP_ENDPOINT (наприклад, адресу Jaeger)."""
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not endpoint:
        return
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    provider = TracerProvider(resource=Resource.create({"service.name": "surveylab-backend"}))
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint.rstrip("/") + "/v1/traces"))
    )
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app, excluded_urls="metrics,health")
    logger.info("Tracing enabled: %s", endpoint)
