# SurveyLab backend

REST API сервісу опитувань (FastAPI). Локальний запуск:

    pip install -r requirements-dev.txt
    uvicorn app.main:app --reload
    pytest -q

Запуск у контейнері разом з PostgreSQL — з кореня репозиторію:

    docker compose up -d --build

Змінні середовища: `DATABASE_URL` (без неї використовується сховище в
пам'яті) і `APP_ENV`.
