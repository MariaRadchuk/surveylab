from typing import Dict, List, Optional

from .config import DATABASE_URL
from .schemas import Survey, SurveyCreate


class SurveyStorage:
    """In-memory сховище опитувань (для тестів і локального запуску без БД)."""

    kind = "memory"

    def __init__(self) -> None:
        self._items: Dict[int, Survey] = {}
        self._next_id = 1

    def add(self, data: SurveyCreate) -> Survey:
        survey = Survey(id=self._next_id, **data.model_dump())
        self._items[survey.id] = survey
        self._next_id += 1
        return survey

    def get(self, survey_id: int) -> Optional[Survey]:
        return self._items.get(survey_id)

    def list(self) -> List[Survey]:
        return list(self._items.values())

    def ping(self) -> bool:
        return True


class PostgresSurveyStorage:
    """Сховище опитувань у PostgreSQL (контейнер db у docker-compose.yml)."""

    kind = "postgres"

    def __init__(self, dsn: str) -> None:
        import psycopg

        self._psycopg = psycopg
        self._dsn = dsn
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS surveys ("
                " id SERIAL PRIMARY KEY,"
                " title VARCHAR(200) NOT NULL,"
                " questions JSONB NOT NULL,"
                " created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())"
            )

    def _connect(self):
        return self._psycopg.connect(self._dsn)

    def add(self, data: SurveyCreate) -> Survey:
        from psycopg.types.json import Jsonb

        questions = [q.model_dump() for q in data.questions]
        with self._connect() as conn:
            row = conn.execute(
                "INSERT INTO surveys (title, questions) VALUES (%s, %s) RETURNING id",
                (data.title, Jsonb(questions)),
            ).fetchone()
        return Survey(id=row[0], **data.model_dump())

    def get(self, survey_id: int) -> Optional[Survey]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, title, questions FROM surveys WHERE id = %s", (survey_id,)
            ).fetchone()
        return Survey(id=row[0], title=row[1], questions=row[2]) if row else None

    def list(self) -> List[Survey]:
        with self._connect() as conn:
            rows = conn.execute("SELECT id, title, questions FROM surveys ORDER BY id").fetchall()
        return [Survey(id=r[0], title=r[1], questions=r[2]) for r in rows]

    def ping(self) -> bool:
        try:
            with self._connect() as conn:
                conn.execute("SELECT 1")
            return True
        except self._psycopg.Error:
            return False


def create_storage(database_url: str = DATABASE_URL):
    if database_url:
        return PostgresSurveyStorage(database_url)
    return SurveyStorage()
