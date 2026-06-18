# Локальный запуск

## Docker Compose

```powershell
docker compose up --build
```

Сервисы:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs
- Nginx entrypoint: http://localhost:8080
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- pgAdmin: http://localhost:5050
- Celery worker: сервис `celery-worker`
- Celery Beat: сервис `celery-beat`
- DB migrations: выполняются one-shot сервисом `migrate` перед запуском backend.

## Hot reload

Hot reload включен в dev-окружении:

- backend запускается через `uvicorn --reload`;
- frontend запускается через `quasar dev`;
- `./backend` и `./frontend` подключены в контейнеры через bind mounts;
- для Docker Desktop и Windows включен polling file watcher.

Backend polling:

```yaml
WATCHFILES_FORCE_POLLING: "true"
```

Frontend polling:

```yaml
CHOKIDAR_USEPOLLING: "true"
WATCHPACK_POLLING: "true"
```

## Инструменты разработки

Установить dev-инструменты:

```powershell
pip install -r requirements-dev.txt
pre-commit install
```

Основные команды через Makefile:

```powershell
make up
make test
make lint
make format
make docs
```

Проверки можно запускать и напрямую:

```powershell
cd backend
ruff check .
ruff format .
```

```powershell
cd frontend
npm run lint
npm run format:check
npm run typecheck
```

## pgAdmin

Доступ в pgAdmin:

- URL: http://localhost:5050
- Email: значение `PGADMIN_DEFAULT_EMAIL`
- Password: значение `PGADMIN_DEFAULT_PASSWORD`

Подключение к PostgreSQL из pgAdmin:

- Host: `db`
- Port: `5432`
- Database: значение `POSTGRES_DB`
- Username: значение `POSTGRES_USER`
- Password: значение `POSTGRES_PASSWORD`

## Документация

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

После запуска документация будет доступна по адресу:

```text
http://127.0.0.1:8000
```

## Миграции БД

Alembic настроен внутри директории `backend/`.

При запуске полного dev-стека миграции применяются автоматически: `backend`
ждет успешного завершения сервиса `migrate`.

Запустить миграции вручную через Docker Compose:

```powershell
docker compose up migrate
```

Создать миграцию:

```powershell
cd backend
alembic revision --autogenerate -m "migration name"
```

Применить миграции:

```powershell
cd backend
alembic upgrade head
```

## Тесты backend

Тесты backend запускаются через pytest.

Запуск локально:

```powershell
cd backend
pytest
```

Запуск через Docker Compose:

```powershell
docker compose run --rm backend-tests
```

## Тесты frontend

Unit/component тесты frontend запускаются через Vitest.

Запуск локально:

```powershell
cd frontend
npm run test
```

Запуск через Docker Compose:

```powershell
docker compose run --rm frontend-tests
```
