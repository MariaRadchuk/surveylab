import logging
import time
from typing import List

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from .config import APP_ENV
from .observability import (
    CONTENT_TYPE_LATEST,
    REQUEST_COUNT,
    REQUEST_LATENCY,
    SURVEYS_CREATED,
    render_metrics,
    setup_tracing,
)
from .schemas import Survey, SurveyCreate
from .storage import create_storage

logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(message)s")
logger = logging.getLogger("surveylab")

app = FastAPI(title="SurveyLab API", version="0.2.0")
storage = create_storage()
setup_tracing(app)
logger.info("SurveyLab API started: env=%s, storage=%s", APP_ENV, storage.kind)


@app.middleware("http")
async def collect_metrics(request: Request, call_next):
    """Метрики запитів для Prometheus: лічильник за кодами й гістограма затримки."""
    started = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        route = request.scope.get("route")
        path = route.path if route else request.url.path
        if path != "/metrics":
            REQUEST_COUNT.labels(request.method, path, str(status)).inc()
            REQUEST_LATENCY.labels(request.method, path).observe(time.perf_counter() - started)
            logger.info("%s %s -> %s", request.method, path, status)


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(render_metrics(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
def health():
    if not storage.ping():
        return JSONResponse(
            status_code=503, content={"status": "unavailable", "storage": storage.kind}
        )
    return {"status": "ok", "storage": storage.kind}


@app.post("/api/surveys", response_model=Survey, status_code=201)
def create_survey(data: SurveyCreate) -> Survey:
    survey = storage.add(data)
    SURVEYS_CREATED.inc()
    return survey


@app.get("/api/surveys", response_model=List[Survey])
def list_surveys() -> List[Survey]:
    return storage.list()


@app.get("/api/surveys/{survey_id}", response_model=Survey)
def get_survey(survey_id: int) -> Survey:
    survey = storage.get(survey_id)
    if survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey
