# SurveyLab

Платформа для створення й проведення онлайн-опитувань. Навчальний проєкт
з дисципліни «Основи DevOps» (лабораторні роботи №2, №3 і №4).
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

4. Етап 3 плану (ЛР4) — оркестрація в Kubernetes:
   1. `deploy/helm/surveylab/` — Helm-діаграма: Deployment і Service бекенду та
      фронтенду, StatefulSet PostgreSQL, ConfigMap, Secret, Ingress, HPA
      бекенду, PodDisruptionBudget, проби справності, `helm test`;
   2. `deploy/helm/surveylab/values-staging.yaml` — параметри середовища staging;
   3. job `deploy-staging` у `.github/workflows/docker-stage2.yml` — після
      збирання образів розгортає реліз у кластері kind, перевіряє API,
      виконує оновлення без простою та відкіт.

Розгортання в локальному кластері (minikube з addon ingress і metrics-server):

    helm upgrade --install surveylab deploy/helm/surveylab \
      --namespace staging --create-namespace \
      -f deploy/helm/surveylab/values-staging.yaml \
      --set image.tag=<SHA коміту> --set db.password=<пароль> --wait
    helm test surveylab -n staging

Локальний запуск середовища (Docker Compose):

    cp .env.example .env
    docker compose up -d --build
    # http://localhost:8081
