from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

QUESTION_TYPES = {"single_choice", "multiple_choice", "rating", "open_text"}
CHOICE_TYPES = {"single_choice", "multiple_choice"}


class Question(BaseModel):
    text: str = Field(min_length=1, max_length=500)
    type: str
    options: Optional[List[str]] = None

    @field_validator("type")
    @classmethod
    def check_type(cls, value: str) -> str:
        if value not in QUESTION_TYPES:
            raise ValueError("unsupported question type")
        return value

    def model_post_init(self, __context) -> None:
        if self.type in CHOICE_TYPES and not (self.options and len(self.options) >= 2):
            raise ValueError("choice question needs at least two options")


class SurveyCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    questions: List[Question] = Field(min_length=1)


class Survey(SurveyCreate):
    id: int
