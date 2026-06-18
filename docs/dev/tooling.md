# Инструменты разработки

## Backend

Для Python-кода используем Ruff:

- `ruff check .` - линтинг.
- `ruff check . --fix` - автоисправления.
- `ruff format .` - форматирование.

Конфигурация находится в `backend/pyproject.toml`.

## Frontend

Для frontend-кода используем:

- ESLint для линтинга JavaScript, TypeScript и Vue.
- Prettier для форматирования.
- `vue-tsc` для проверки типов.
- Vitest для unit/component тестов.

Основные команды:

```powershell
cd frontend
npm run lint
npm run lint:fix
npm run format
npm run format:check
npm run typecheck
npm run test
```

## Pre-commit

Pre-commit запускает базовые проверки перед коммитом:

- trailing whitespace;
- end-of-file fixer;
- проверка YAML/JSON/TOML;
- Ruff check/format для backend;
- ESLint и Prettier check для frontend.

Установка:

```powershell
pip install -r requirements-dev.txt
pre-commit install
```

Ручной запуск всех hooks:

```powershell
pre-commit run --all-files
```

## Makefile

Для часто используемых команд есть `Makefile`.

```powershell
make up
make down
make worker
make beat
make test
make lint
make format
make docs
```

Если `make` недоступен в Windows-окружении, команды можно запускать напрямую
через `docker compose`, `ruff`, `npm` и `mkdocs`.
