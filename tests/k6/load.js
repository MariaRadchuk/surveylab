// Навантажувальний тест SurveyLab (k6): читання списку, створення опитувань, перевірка стану.
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE = __ENV.BASE_URL || 'http://localhost:8081';

export const options = {
  stages: [
    { duration: '10s', target: 10 },
    { duration: '20s', target: 20 },
    { duration: '5s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],     // менше 1 % помилок
    http_req_duration: ['p(95)<500'],   // 95 % запитів швидше за 500 мс
  },
};

const SURVEY = JSON.stringify({
  title: 'Навантажувальний тест',
  questions: [{ text: 'Оцініть курс', type: 'rating' }],
});

export default function () {
  const health = http.get(`${BASE}/health`);
  check(health, { 'health 200': (r) => r.status === 200 });

  const list = http.get(`${BASE}/api/surveys`);
  check(list, { 'list 200': (r) => r.status === 200 });

  const created = http.post(`${BASE}/api/surveys`, SURVEY, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(created, { 'create 201': (r) => r.status === 201 });

  sleep(1);
}
