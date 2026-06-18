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
