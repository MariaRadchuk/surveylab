from typing import List

from fastapi import FastAPI, HTTPException

from .schemas import Survey, SurveyCreate
from .storage import SurveyStorage

app = FastAPI(title="SurveyLab API", version="0.1.0")
storage = SurveyStorage()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


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
