import os

# Настройки Postgres
POSTGRES_USERNAME=os.environ.get('POSTGRES_USERNAME', 'esports')
POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD', 'esports')
POSTGRES_HOST=os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT=os.environ.get('POSTGRES_PORT', 5432)
POSTGRES_DB_NAME=os.environ.get('POSTGRES_DB_NAME', 'esports')

# Настройки приложения
IS_DEV=bool(os.environ.get('IS_DEV', False))
APP_PORT=int(os.environ.get('APP_PORT', 11011))
UPDATE_TIMEOUT=int(os.environ.get('UPDATE_TIMEOUT', 60))