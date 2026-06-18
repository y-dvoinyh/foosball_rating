# Foosball Rating

Техническая документация проекта для рейтингов игроков в настольный футбол.

Проект строится как публичный сайт с рейтингами и закрытой административной
частью. Большая часть страниц доступна без авторизации. Авторизация нужна для
пользовательских возможностей и административных действий.

## Быстрые ссылки

- [Архитектурный обзор](architecture/overview.md)
- [Git workflow](dev/git-workflow.md)
- [Локальный запуск](dev/local-setup.md)
- [Фоновые задачи](backend/background-jobs.md)
- [Аутентификация и права](backend/auth-and-permissions.md)

## Основной стек

- Backend: FastAPI.
- База данных: PostgreSQL.
- ORM и миграции: SQLAlchemy 2 async + Alembic.
- Фоновые задачи: Celery + Redis.
- Frontend: Vue 3 + Quasar + TypeScript.
- Reverse proxy: nginx.
- Локальное окружение: Docker Compose.
