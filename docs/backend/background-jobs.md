# Фоновые задачи

Фоновые задачи выполняются через Celery worker-ы. Redis используется как broker
и может использоваться для статусов задач, временных кодов и легкого кеша.

В локальном Docker Compose настроены сервисы:

- `redis` - Redis broker/backend.
- `celery-worker` - обработчик фоновых задач.
- `celery-beat` - запуск задач по расписанию.

## Задачи

- Парсинг внешних сайтов или API.
- Импорт и нормализация турнирных данных.
- Пересчет рейтингов.
- Отправка email при регистрации и восстановлении пароля.
- Периодическая синхронизация данных.

## Требования

- Задачи должны быть идемпотентными там, где это возможно.
- Повторный импорт одного турнира не должен создавать дубликаты.
- Статус долгих задач должен быть доступен администратору.
- Ошибки парсинга и расчета должны логироваться с достаточным контекстом.

## Локальный запуск

Запустить полный dev-стек:

```powershell
docker compose up --build
```

Запустить только Redis и Celery worker:

```powershell
docker compose up redis celery-worker
```

Запустить Celery Beat:

```powershell
docker compose up celery-beat
```

Проверить примерную debug-задачу из backend-контейнера:

```powershell
docker compose run --rm backend python -c "from app.tasks.debug import ping; print(ping.delay().get(timeout=10))"
```
