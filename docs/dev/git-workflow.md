# Git workflow

Используем облегченную схему:

- `main` - стабильная ветка, код из нее должен быть готов к деплою.
- `develop` - основная ветка разработки и интеграции.
- короткие task-ветки создаются от `develop`.
- `release/*` создается только при необходимости стабилизировать версию перед
  попаданием в `main`.

## Типы task-веток

- `feature/<short-name>` - новая функциональность.
- `fix/<short-name>` - исправление ошибки в текущей разработке.
- `hotfix/<short-name>` - срочное исправление от `main`.
- `chore/<short-name>` - инфраструктура, зависимости, конфиги.
- `docs/<short-name>` - документация.
- `refactor/<short-name>` - рефакторинг без изменения поведения.
- `experiment/<short-name>` - исследовательская ветка, которую можно удалить.

## Примеры

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

## Процесс

1. Обновить `develop`.
2. Создать task-ветку от `develop`.
3. Сделать изменения и коммиты.
4. Открыть pull request в `develop`.
5. После проверки влить изменения в `develop`.
6. Когда версия готова к выпуску, при необходимости создать `release/<version>`.
7. После стабилизации влить release в `main` и вернуть release-фиксы обратно в
   `develop`, если они были.

## Коммиты

Используем Conventional Commits:

```text
feat(auth): add email confirmation
feat(import): parse kickertool live link
fix(rating): handle duplicate history rows
chore(infra): add celery worker
docs: describe git workflow
refactor(rating): split calculation service
```
