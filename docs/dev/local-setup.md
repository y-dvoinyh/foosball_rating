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
- pgAdmin: http://localhost:5050
- DB migrations: выполняются one-shot сервисом `migrate` перед запуском backend.

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
