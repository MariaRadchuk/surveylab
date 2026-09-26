from typing import Dict, List

from .schemas import Survey, SurveyCreate


class SurveyStorage:
    """In-memory сховище опитувань (на Етапі 1; замінюється PostgreSQL)."""

    def __init__(self) -> None:
        self._items: Dict[int, Survey] = {}
        self._next_id = 1

    def add(self, data: SurveyCreate) -> Survey:
        survey = Survey(id=self._next_id, **data.model_dump())
        self._items[survey.id] = survey
        self._next_id += 1
        return survey

    def get(self, survey_id: int):
        return self._items.get(survey_id)

    def list(self) -> List[Survey]:
        return list(self._items.values())
