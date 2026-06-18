# Тестирование backend

Backend-тесты находятся в `backend/tests/` и запускаются через pytest.

## Запуск

Локально:

```powershell
cd backend
pytest
```

Через Docker Compose:

```powershell
docker compose run --rm backend-tests
```

## Принципы

- Быстрые unit/API-тесты не должны требовать реальной БД.
- Интеграционные тесты с БД добавляются отдельно и должны явно готовить данные.
- Для FastAPI endpoints используем `TestClient` или `httpx.AsyncClient`.
- Внешние сервисы, парсинг и email в unit-тестах заменяются fake/stub-реализациями.
