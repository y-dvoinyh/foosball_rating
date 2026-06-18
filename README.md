# foosball_rating

Веб-приложение для рейтингов игроков в настольный футбол.

## Архитектурное решение

Проект строится как публичный сайт с рейтингами и закрытой административной
частью. Большая часть страниц доступна без авторизации. Авторизация нужна для
пользовательских возможностей и административных действий.

Основной стек:

- Backend: FastAPI.
- База данных: PostgreSQL.
- ORM и миграции: SQLAlchemy 2 async + Alembic.
- Фоновые задачи: Celery + Redis.
- Задачи по расписанию: Celery Beat или APScheduler.
- Frontend: Vue 3 + Quasar + TypeScript.
- Состояние и маршрутизация фронтенда: Pinia + Vue Router.
- HTTP-клиент: Axios.
- Reverse proxy: nginx.
- Локальное окружение: Docker Compose.

## Зоны ответственности backend

Backend на FastAPI отвечает за доменную модель, API, аутентификацию, права
доступа, парсинг/импорт данных и расчет рейтингов.

Основные backend-модули:

- Игроки, турниры, соревнования, команды, матчи, сеты.
- Рейтинги и история рейтингов.
- Импорт данных из внешних источников по настольному футболу и турнирам.
- Хранение исходных импортированных данных для воспроизводимого пересчета и отладки.
- Аутентификация по email/password.
- Подтверждение email кодом или токеном при регистрации.
- Ролевая модель прав с ограничением по областям доступа.
- Admin API для управления импортом, пользователями, правами и пересчетами рейтинга.

## Фоновые задачи

Фоновые задачи нужны для операций, которые не должны блокировать API-запросы:

- Парсинг внешних сайтов или API.
- Импорт и нормализация турнирных данных.
- Пересчет рейтингов.
- Отправка писем регистрации и восстановления пароля.
- Периодическая синхронизация с внешними источниками.

Задачи выполняются Celery worker-ами. Redis используется как broker для Celery,
а также может хранить временные коды подтверждения, статусы задач и легкий кеш.

## Аутентификация и авторизация

Аутентификация реализуется внутри FastAPI-приложения. Keycloak не входит в
начальную архитектуру.

Планируемая модель auth:

- Пользователи хранятся в PostgreSQL.
- Пароли хранятся в виде безопасных хешей.
- Авторизация использует access token и refresh token.
- Регистрация требует подтверждения email.
- Административные действия защищены ролями и scoped permissions.

Права должны поддерживать как глобальные роли, так и роли в рамках конкретной
области, например:

- Глобальный администратор.
- Администратор лиги.
- Менеджер турнира.
- Модератор контента.
- Обычный авторизованный пользователь.

## Административная панель

Основную административную панель нужно реализовать во frontend-приложении на
Quasar и подключить к admin endpoints в FastAPI. Так админка сможет учитывать
проектные роли, области доступа, импорт данных и процессы пересчета рейтинга.

Легкую FastAPI admin-библиотеку можно рассмотреть позже для внутреннего CRUD,
но она не должна заменять проектную административную панель.

## Уроки прошлых версий

Полезные идеи из `yarfoosball`:

- Доменная модель игроков, турниров, соревнований, команд, матчей, сетов,
  рейтингов и истории рейтингов.
- Процесс импорта данных из Kickertool.
- Хранение исходного импортированного JSON вместе с нормализованными сущностями.
- Публичные страницы рейтингов, профилей игроков и деталей соревнований.

Полезные идеи из `foosball_backend`:

- Celery + Redis для фоновых задач.
- Процесс подтверждения email.
- API для статуса и истории задач.

Решения для этой версии:

- Оставляем FastAPI как backend framework.
- Оставляем Quasar для frontend.
- Оставляем PostgreSQL как основную базу данных.
- Не используем Keycloak на старте.
- Держим инфраструктуру достаточно простой для локальной разработки и деплоя.

## Структура

- `frontend` - клиентское приложение на Vue 3 + Quasar.
- `backend` - backend на FastAPI с async SQLAlchemy.
- `nginx` - конфигурация локального reverse proxy.
- `docs` - техническая документация MkDocs Material.
- `mkdocs.yml` - конфигурация сайта документации.
- `requirements-docs.txt` - зависимости для сборки документации.
- `docker-compose.yml` - локальный стек для разработки.

## Документация

Техническая документация хранится в `docs/` и собирается через MkDocs Material.

Локальный запуск документации:

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

Сборка статического сайта документации:

```powershell
mkdocs build
```

После запуска документация доступна по адресу:

```text
http://127.0.0.1:8000
```

## Инструменты разработки

Установить dev-инструменты для pre-commit и документации:

```powershell
pip install -r requirements-dev.txt
pre-commit install
```

Основные команды:

```powershell
make up
make test
make lint
make format
make docs
```

Backend:

```powershell
cd backend
ruff check .
ruff format .
```

Frontend:

```powershell
cd frontend
npm run lint
npm run format:check
npm run typecheck
```

## Git workflow

Используем облегченную схему:

- `main` - стабильная ветка, код из нее должен быть готов к деплою.
- `develop` - основная ветка разработки и интеграции.
- короткие task-ветки создаются от `develop`.
- `release/*` создается только при необходимости стабилизировать версию перед
  попаданием в `main`.

Типы task-веток:

- `feature/<short-name>` - новая функциональность.
- `fix/<short-name>` - исправление ошибки в текущей разработке.
- `hotfix/<short-name>` - срочное исправление от `main`.
- `chore/<short-name>` - инфраструктура, зависимости, конфиги.
- `docs/<short-name>` - документация.
- `refactor/<short-name>` - рефакторинг без изменения поведения.
- `experiment/<short-name>` - исследовательская ветка, которую можно удалить.

Примеры:

```text
feature/auth-email-confirmation
feature/kickertool-import
feature/rating-calculation
feature/admin-panel
fix/rating-history-duplicates
chore/docker-compose-redis
docs/git-workflow
release/0.1.0
hotfix/broken-login
```

Обычный процесс разработки:

1. Обновить `develop`.
2. Создать task-ветку от `develop`.
3. Сделать изменения и коммиты.
4. Открыть pull request в `develop`.
5. После проверки влить изменения в `develop`.
6. Когда версия готова к выпуску, при необходимости создать `release/<version>`.
7. После стабилизации влить release в `main` и вернуть release-фиксы обратно в
   `develop`, если они были.

Для сообщений коммитов используем Conventional Commits:

```text
feat(auth): add email confirmation
feat(import): parse kickertool live link
fix(rating): handle duplicate history rows
chore(infra): add celery worker
docs: describe git workflow
refactor(rating): split calculation service
```

## Локальный запуск

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

Подключение к PostgreSQL из pgAdmin:

- Host: `db`
- Port: `5432`
- Database: значение `POSTGRES_DB`
- Username: значение `POSTGRES_USER`
- Password: значение `POSTGRES_PASSWORD`

## Миграции БД

Alembic настроен в директории `backend/`.

При обычном запуске через Docker Compose миграции автоматически применяются
отдельным сервисом:

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
