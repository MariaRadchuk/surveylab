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

5. Етапи 4–5 плану (ЛР7) — тестування, спостережуваність і GitOps:
   1. `backend/app/observability.py` — метрики Prometheus (`/metrics`: кількість запитів за кодом,
      гістограма затримки, лічильник створених опитувань) і трасування OpenTelemetry (вмикається
      змінною `OTEL_EXPORTER_OTLP_ENDPOINT`);
   2. `tests/` — Postman/Newman (API), k6 (навантаження з порогами), Cypress (E2E сторінки викладача);
      `.github/workflows/tests.yml` запускає їх на піднятому стеку Compose;
   3. `deploy/monitoring/` — Prometheus, Alertmanager (webhook-отримувач), Grafana (дашборд
      «SurveyLab: огляд»), Loki + Promtail, Jaeger, node-exporter;
   4. `deploy/argocd/surveylab-staging.yaml` і `deploy/helm/surveylab/values-gitops.yaml` —
      розгортання Helm-діаграми з Git за допомогою ArgoCD (автосинхронізація, prune, selfHeal).

Запуск стека спостережуваності поруч із застосунком:

    docker compose up -d --build
    docker compose -p surveylab-monitoring --env-file .env \
      -f deploy/monitoring/docker-compose.yml up -d
    # Grafana http://localhost:3000, Prometheus http://localhost:9090,
    # Alertmanager http://localhost:9093, Jaeger http://localhost:16686

Тести: `newman run tests/postman/surveylab.postman_collection.json`,
`k6 run tests/k6/load.js`, `cd tests/e2e && npm ci && npx cypress run`.
