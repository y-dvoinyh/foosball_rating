# Статус стека

Документ фиксирует, какие части заявленного стека уже настроены в каркасе, а
какие остаются предметной разработкой будущих фич.

## Настроено

- FastAPI backend.
- PostgreSQL.
- SQLAlchemy 2 async.
- Alembic.
- Redis.
- Celery worker.
- Celery Beat для задач по расписанию.
- Vue 3.
- Quasar.
- TypeScript.
- Pinia.
- Vue Router.
- Axios.
- nginx.
- Docker Compose.
- pgAdmin.
- MkDocs Material.
- pytest для backend.
- Vitest для frontend.
- Ruff для backend lint/format.
- ESLint и Prettier для frontend.
- pre-commit.
- GitHub Actions CI.

## Частично настроено

- Фоновые задачи: настроена инфраструктура Celery/Redis и примерная debug-задача.
  Доменные задачи импорта, email и пересчета рейтингов будут добавляться в
  отдельных feature-ветках.
- Scheduled jobs: настроен Celery Beat и примерное расписание. Реальные
  периодические задачи появятся вместе с импортом и синхронизацией.

## Еще не реализовано

- Доменная модель игроков, турниров, матчей и рейтингов.
- Auth: регистрация, login, refresh tokens, email confirmation.
- Ролевая модель и scoped permissions.
- Admin API.
- Административная панель на Quasar.
- Импорт данных из Kickertool и других источников.
- Алгоритм расчета рейтингов.
- Email sender.
- Task status/history API.
- E2E-тесты на Playwright.
