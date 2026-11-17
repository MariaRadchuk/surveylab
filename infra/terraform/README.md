# Інфраструктура SurveyLab (Terraform)

Модулі: `network` (VPC, підмережі), `app-host` (EC2 + група безпеки),
`backups` (S3 з версіонуванням і шифруванням), `secrets` (секрет БД у
AWS Secrets Manager; пароль генерує Terraform).

Середовище `staging` налаштоване на локальний емулятор AWS (LocalStack,
`http://localhost:4566`, тестові ключі). Для реального AWS прибрати
`access_key`, `secret_key`, `skip_*` та блок `endpoints`.

```bash
cd environments/staging
terraform init && terraform plan
```
