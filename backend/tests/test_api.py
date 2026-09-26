from fastapi.testclient import TestClient

from app.main import app, storage

client = TestClient(app)

VALID = {
    "title": "Оцінка курсу",
    "questions": [
        {"text": "Ваша оцінка?", "type": "rating"},
        {"text": "Що сподобалось?", "type": "single_choice", "options": ["Лекції", "Практика"]},
    ],
}


def setup_function():
    storage._items.clear()
    storage._next_id = 1


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_survey():
    created = client.post("/api/surveys", json=VALID)
    assert created.status_code == 201
    survey_id = created.json()["id"]
    fetched = client.get(f"/api/surveys/{survey_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == VALID["title"]


def test_list_surveys():
    client.post("/api/surveys", json=VALID)
    client.post("/api/surveys", json=VALID)
    assert len(client.get("/api/surveys").json()) == 2


def test_unknown_survey_returns_404():
    assert client.get("/api/surveys/999").status_code == 404


def test_survey_without_questions_rejected():
    response = client.post("/api/surveys", json={"title": "Порожнє", "questions": []})
    assert response.status_code == 422


def test_unsupported_question_type_rejected():
    bad = {"title": "X", "questions": [{"text": "Q", "type": "video"}]}
    assert client.post("/api/surveys", json=bad).status_code == 422


def test_choice_question_needs_options():
    bad = {"title": "X", "questions": [{"text": "Q", "type": "single_choice", "options": ["A"]}]}
    assert client.post("/api/surveys", json=bad).status_code == 422
