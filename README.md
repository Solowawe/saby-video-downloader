---
title: Saby Video Downloader
emoji: 🎬
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000
---

# Saby Video Downloader — Web Service

Веб-сервис для получения прямых CDN ссылок на видео с saby.ru.

## Как это работает

1. Пользователь вставляет ссылку на страницу плеера Saby:
   ```
   https://play.saby.ru/multimedia-converter/embed/{UUID1}_{UUID2}
   ```
2. Сервер формирует прямую CDN ссылку:
   ```
   https://cdn-disk.sbis.ru/disk/api/v1/{UUID1}_{UUID2}
   ```
3. Пользователь получает готовую ссылку и может скачать видео напрямую с CDN Saby.

## Локальный запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
uvicorn main:app --reload --port 8000
```

Откройте http://localhost:8000

## API

### `POST /api/extract`

Извлечение CDN ссылки из URL вебинара.

**Request:**
```json
{
  "url": "https://play.saby.ru/multimedia-converter/embed/UUID1_UUID2"
}
```

**Response (200):**
```json
{
  "success": true,
  "cdn_url": "https://cdn-disk.sbis.ru/disk/api/v1/UUID1_UUID2",
  "filename": "UUID1_UUID2.mp4",
  "content_type": "video/mp4",
  "content_length": 123456789,
  "content_length_str": "117.7 MB",
  "accessible": true
}
```

### `GET /api/history`

Последние 20 запросов.

### `GET /health`

Health check.

## Структура проекта

```
web_service/
├── main.py              # FastAPI приложение
├── requirements.txt     # Зависимости
├── Dockerfile           # Docker-образ
├── templates/
│   └── index.html       # Главная страница
├── static/
│   └── style.css        # Стили
└── README.md            # Этот файл