import logging
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .config import APP_ENV
from .schemas import Survey, SurveyCreate
from .storage import create_storage

logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(message)s")
logger = logging.getLogger("surveylab")

app = FastAPI(title="SurveyLab API", version="0.2.0")
storage = create_storage()
logger.info("SurveyLab API started: env=%s, storage=%s", APP_ENV, storage.kind)


@app.get("/health")
def health():
    if not storage.ping():
        return JSONResponse(
            status_code=503, content={"status": "unavailable", "storage": storage.kind}
        )
    return {"status": "ok", "storage": storage.kind}


@app.post("/api/surveys", response_model=Survey, status_code=201)
def create_survey(data: SurveyCreate) -> Survey:
    return storage.add(data)


@app.get("/api/surveys", response_model=List[Survey])
def list_surveys() -> List[Survey]:
    return storage.list()


@app.get("/api/surveys/{survey_id}", response_model=Survey)
def get_survey(survey_id: int) -> Survey:
    survey = storage.get(survey_id)
    if survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey
