# SurveyLab

Платформа для створення й проведення онлайн-опитувань. Навчальний проєкт
з дисципліни «Основи DevOps» (лабораторні роботи №2 і №3).
Цільова аудиторія — викладачі закладів вищої освіти.

1. `index.js`, `index.test.js`, `Dockerfile`, `package.json` і
   `.github/workflows/` (крім `ci-stage1.yml`) — завдання 1.
2. `backend/` і `.github/workflows/ci-stage1.yml` — індивідуальне
   завдання: базовий бекенд SurveyLab (FastAPI) з конвеєром CI, що на
   кожне надсилання змін запускає flake8 та PyTest.
3. Етап 2 плану (ЛР3) — контейнеризація:
   1. `backend/Dockerfile` — багатоетапна збірка (builder + runtime),
      непривілейований користувач, HEALTHCHECK;
   2. `frontend/` — сторінка викладача на Nginx, проксіювання `/api/` до бекенду;
   3. `docker-compose.yml` — локальне середовище PostgreSQL + backend + frontend,
      змінні середовища з `.env` (шаблон `.env.example`);
   4. `.github/workflows/docker-stage2.yml` — збирання образів, сканування
      Trivy, публікація в GitHub Container Registry і перевірка стека через
      `docker compose`.

Локальний запуск середовища:

    cp .env.example .env
    docker compose up -d --build
    # http://localhost:8081
