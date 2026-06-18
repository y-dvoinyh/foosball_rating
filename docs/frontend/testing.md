# Тестирование frontend

Frontend-тесты находятся рядом с тестируемыми файлами и запускаются через Vitest.

## Инструменты

- Vitest для unit/component тестов.
- Vue Test Utils для тестирования Vue-компонентов.
- jsdom как DOM-окружение.
- `@pinia/testing` для тестирования stores.

## Запуск

Локально:

```powershell
cd frontend
npm run test
```

В watch-режиме:

```powershell
cd frontend
npm run test:watch
```

Через Docker Compose:

```powershell
docker compose run --rm frontend-tests
```

## Что тестируем

- Компоненты с условной логикой.
- Composables.
- Pinia stores.
- Route guards.
- Формы, валидацию и обработку ошибок.
- Административные workflows на уровне компонентов.

## E2E

E2E-тесты на Playwright добавим позже, когда появятся реальные сценарии:

- просмотр рейтингов;
- профиль игрока;
- регистрация и авторизация;
- административный запуск импорта;
- просмотр статуса фоновой задачи.
