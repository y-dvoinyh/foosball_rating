# Архитектура аутентификации

## Решение

Аутентификацию и авторизацию реализуем внутри текущего FastAPI-приложения как
модульный монолит. Auth-код должен иметь явную внутреннюю границу, чтобы позже
его можно было вынести в отдельный FastAPI-сервис без смены публичного
контракта.

На первом этапе используем JWT access token и refresh token.

## Почему не отдельный сервис сразу

Отдельный auth-service полезен для изучения микросервисной архитектуры, но для
текущего этапа проекта добавляет лишнюю инфраструктуру:

- межсервисные HTTP-запросы;
- отдельные настройки секретов и миграций;
- сетевые ошибки, retry и healthchecks;
- дополнительную сложность в самой критичной части системы.

Поэтому auth сначала живет внутри backend, но проектируется как отдельный
bounded context.

## Граница модуля

Остальные части backend не должны напрямую парсить JWT, работать с
refresh-токенами или читать внутренние auth-таблицы. Они используют зависимости
и сервисные интерфейсы auth-модуля.

Предполагаемая структура:

```text
backend/app/auth/
  router.py
  schemas.py
  service.py
  dependencies.py
  security.py
  tokens.py
  models.py
  repository.py
```

Модули матчей, рейтинга и администрирования должны получать текущего
пользователя через dependency, например `get_current_user`.

## API-контракт

Минимальный публичный контракт auth-модуля:

- `POST /auth/register` - регистрация пользователя;
- `POST /auth/login` - вход по email и password;
- `POST /auth/refresh` - выпуск новой пары токенов;
- `POST /auth/logout` - отзыв текущего refresh token;
- `GET /auth/me` - данные текущего пользователя.

Этот контракт должен оставаться стабильным, даже если auth позже будет вынесен
в отдельный сервис.

## Токены

### Access token

Access token является JWT с коротким временем жизни, например 15 минут.
На старте подписываем его симметричным алгоритмом `HS256`; секрет задается
через `AUTH_SECRET_KEY`.

Рекомендуемые claims:

- `sub` - идентификатор пользователя;
- `type` - тип токена, значение `access`;
- `iat` - время выпуска;
- `exp` - время истечения;
- `jti` - уникальный идентификатор токена;
- `role` или список ролей, если это понадобится для быстрых проверок.

Access token передается в заголовке:

```http
Authorization: Bearer <access_token>
```

Backend валидирует access token локально, без запроса в БД на каждый запрос.

### Refresh token

Refresh token имеет более долгий срок жизни, например 7-30 дней, и используется
только для получения новой пары токенов.

Refresh token:

- хранится в базе только в виде хеша;
- имеет собственный `jti`;
- может быть отозван;
- ротируется при каждом refresh-запросе.

При ротации старый refresh token инвалидируется, а клиент получает новый
access token и новый refresh token.

## Хранение на клиенте

Целевое решение:

- access token хранится в памяти frontend-приложения;
- refresh token хранится в `HttpOnly`, `Secure`, `SameSite` cookie.

На раннем этапе разработки допустимо временно возвращать оба токена в JSON, но
архитектуру backend проектируем так, чтобы перейти к cookie для refresh token
без переделки бизнес-логики.

## Данные

Минимальные таблицы для первого этапа:

```text
users
  id
  email
  password_hash
  is_active
  is_superuser
  created_at
  updated_at

refresh_tokens
  id
  user_id
  token_hash
  jti
  expires_at
  revoked_at
  created_at
  replaced_by_token_id
  user_agent
  ip_address
```

`user_agent` и `ip_address` нужны для аудита и управления сессиями, но могут
быть добавлены после MVP.

## Auth flow

Login:

```text
email/password correct
  -> issue access token
  -> issue refresh token
  -> save hashed refresh token
  -> return tokens to client
```

Refresh:

```text
refresh token received
  -> hash and find active token in DB
  -> check expiration and revocation
  -> revoke old refresh token
  -> issue new access token
  -> issue new refresh token
  -> save hashed new refresh token
  -> return new token pair
```

Logout:

```text
refresh token received
  -> hash and find token in DB
  -> mark token as revoked
```

## MVP

Первая реализация auth должна включать:

- регистрацию по email и password;
- безопасное хеширование паролей;
- login с выпуском access и refresh token;
- refresh token rotation;
- logout с отзывом refresh token;
- endpoint `/auth/me`;
- dependency для получения текущего пользователя;
- защиту одного или нескольких существующих backend endpoint.

После MVP можно добавить подтверждение email, сброс пароля, управление
сессиями, роли и OAuth.

## Возможный вынос в сервис

Если auth станет отдельным сервисом, основной backend должен продолжить
валидировать access JWT локально. В auth-service уйдут:

- регистрация;
- login;
- refresh;
- logout;
- хранение пользователей, паролей и refresh-токенов;
- управление сессиями.

Основной backend будет зависеть от стабильного JWT-контракта и публичных
auth-endpoint, а не от внутренних таблиц auth.
