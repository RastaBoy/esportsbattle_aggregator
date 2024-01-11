import os

# Настройки Postgres
POSTGRES_USERNAME=os.environ['POSTGRES_USERNAME']
POSTGRES_PASSWORD=os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST=os.environ['POSTGRES_HOST']
POSTGRES_PORT=os.environ['POSTGRES_PORT']
POSTGRES_DB_NAME=os.environ['POSTGRES_DB_NAME']

# Настройки приложения
APP_PORT=os.environ['APP_PORT']
UPDATE_TIMEOUT=os.environ['UPDATE_TIMEOUT']