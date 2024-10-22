# Comment System API

Простой REST API для управления комментариями: создание, список, удаление, флаг модерации. Хранилище — JSON-файл на диске, без внешних зависимостей.

## Быстрый старт

- Требования: `Python 3.11+`
- Установка зависимостей: `python -m pip install -r requirements.txt`
- Запуск: `./run.ps1 -Port 8001` (по умолчанию порт `8001`)

## Эндпоинты

- `GET /health` — статус сервиса
- `GET /comments?postId=&author=` — список комментариев с фильтрами
- `POST /comments` — создать комментарий
  - Тело: `{ "postId": "p1", "author": "alice", "text": "Hello!" }`
- `DELETE /comments/{id}` — удалить комментарий
- `POST /comments/{id}/flag` — пометить как «флагged» для модерации

## Примеры

Создать комментарий:

```
curl -s -X POST http://localhost:8001/comments \
  -H "Content-Type: application/json" \
  -d '{"postId":"p1","author":"alice","text":"Hello!"}'
```

Список по посту:

```
curl -s "http://localhost:8001/comments?postId=p1"
```

Удалить:

```
curl -i -X DELETE "http://localhost:8001/comments/<id>"
```

Флаг модерации:

```
curl -s -X POST "http://localhost:8001/comments/<id>/flag"
```

## Как это работает

- Данные сохраняются в `data/comments.json`
- Максимальный размер JSON тела: 10kb
- Валидация: обязательные поля `postId`, `author`, `text (>=3 символа)`

## Лицензия

MIT
