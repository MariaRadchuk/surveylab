variable "environment" {
  description = "Назва середовища"
  type        = string
}

# Пароль БД генерує Terraform: у коді та в репозиторії його немає
resource "random_password" "db" {
  length  = 24
  special = false
}

resource "aws_secretsmanager_secret" "db" {
  name                    = "surveylab/${var.environment}/db"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({
    username = "surveylab"
    password = random_password.db.result
  })
}

output "secret_arn" {
  value = aws_secretsmanager_secret.db.arn
}
