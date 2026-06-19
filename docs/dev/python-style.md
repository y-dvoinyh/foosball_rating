# Стиль Python-кода

Этот документ фиксирует базовые правила форматирования Python-кода в backend.
Правила должны быть простыми, автоматизируемыми и одинаковыми для локальной
разработки, pre-commit и CI.

## Инструмент

Для форматирования, переносов строк, сортировки импортов и базового линтинга
используем Ruff.

Конфигурация находится в `backend/pyproject.toml`.

Проверка:

```powershell
cd backend
ruff format --check .
ruff check .
```

Автоисправление:

```powershell
cd backend
ruff format .
ruff check . --fix
```

Через Docker Compose:

```powershell
docker compose run --rm backend-lint
docker compose run --rm backend-format
```

## Форматирование

- Максимальная длина строки: 100 символов.
- Отступ: 4 пробела.
- Кавычки: двойные.
- Line endings: LF.
- Версия Python для правил форматирования: Python 3.12.
- Финальную раскладку переносов выбирает `ruff format`.

Если выражение не помещается в 100 символов, используем переносы внутри
скобок, квадратных скобок или фигурных скобок. Не используем обратный слеш
для переноса строк.

Хорошо:

```python
result = await rating_service.calculate_player_rating(
    player_id=player_id,
    tournament_id=tournament_id,
    include_archived_matches=False,
)
```

Плохо:

```python
result = await rating_service.calculate_player_rating(player_id=player_id, tournament_id=tournament_id, include_archived_matches=False)
```

## Импорты

Импорты сортирует Ruff.

Группы импортов:

1. стандартная библиотека;
2. сторонние зависимости;
3. внутренние модули проекта `app`.

Внутри группы импорты сортируются автоматически.

Пример:

```python
from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
```

## Многострочные структуры

Для длинных списков, словарей, аргументов функций и вызовов функций используем
многострочный формат с висячей запятой.

```python
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:8080",
]
```

```python
return PlayerRatingRead(
    player_id=player.id,
    rating=rating.value,
    updated_at=rating.updated_at,
)
```

## Что не решаем вручную

Не спорим руками о пробелах, переносах, сортировке импортов и кавычках.
Если Ruff меняет форматирование, принимаем формат Ruff как стандарт проекта.

Если правило кажется неудобным, сначала меняем `backend/pyproject.toml`,
документацию и CI, а потом форматируем код заново.
