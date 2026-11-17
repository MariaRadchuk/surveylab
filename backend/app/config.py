import os

# Конфігурація винесена у змінні середовища (етап 2 плану): у контейнері її
# задає docker-compose.yml, локально без змінних використовується пам'ять.
APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "")
