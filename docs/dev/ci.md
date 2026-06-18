# CI

CI настроен через GitHub Actions в `.github/workflows/ci.yml`.

## Когда запускается

- При push в `main`.
- При push в `develop`.
- При pull request в `main` или `develop`.

## Проверки

Backend:

- установка Python-зависимостей;
- `ruff format --check`;
- `ruff check`;
- `pytest`.

Frontend:

- установка Node.js-зависимостей;
- `npm run format:check`;
- `npm run lint`;
- `npm run typecheck`;
- `npm run test`.

Документация:

- установка зависимостей документации;
- `mkdocs build`.

Docker Compose:

- `docker compose config`.

## Важные замечания

Во frontend пока нет `package-lock.json`, поэтому CI использует `npm install`.
После появления lock-файла команду в CI стоит заменить на `npm ci`.

CI должен оставаться отражением локальных команд. Если меняется команда в
README, Makefile или `package.json`, нужно проверить, что workflow остается
актуальным.
