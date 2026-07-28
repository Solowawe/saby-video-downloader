# Инструкция по деплою на Railway.app

## Шаг 1: Создать аккаунт на Railway.app

1. Откройте https://railway.app
2. Нажмите **Start a New Project** или **Login**
3. Выберите **Continue with GitHub**
4. Авторизуйте Railway.app для доступа к вашему GitHub аккаунту
5. Подтвердите email (если потребуется)

## Шаг 2: Развернуть сервис

### Через GitHub (рекомендуемый)

1. На панели Railway.app нажмите **New Project**
2. Выберите **Deploy from GitHub repo**
3. Выберите репозиторий `Solowawe/saby-video-downloader`
4. Railway автоматически обнаружит `Dockerfile` и запустит сборку

### Через Railway CLI

```bash
# Установить Railway CLI
npm i -g @railway/cli

# Войти в аккаунт
railway login

# Перейти в папку проекта
cd d:\prjs\smart\cursor\video_downloader\web_service

# Инициализировать проект
railway init

# Развернуть
railway up
```

## Шаг 3: Дождаться деплоя

1. Railway автоматически запустит сборку через Docker (1-3 минуты)
2. Статус изменится с **Deploying** на **Running**
3. Нажмите на **Generate Domain** или используйте автоматически сгенерированный URL вида:
   ```
   https://saby-video-downloader.up.railway.app
   ```

## Шаг 4: Проверка

Откройте в браузере:

```
https://ВАШ-ДОМЕН.railway.app/health
```

Должен вернуться `{"status": "ok"}`.

Затем откройте главную страницу и проверьте извлечение ссылки:
```
https://ВАШ-ДОМЕН.railway.app/
```

## Важно

- **Бесплатный тариф Railway** включает 500 часов в месяц и 100 GB трафика
- Сервис **не "засыпает"** как на Render.com (но может быть ограничение по трафику)
- Если нужно больше — можно обновить тариф ($5/мес за дополнительные ресурсы)
- Railway использует **эфемерную файловую систему** — история запросов хранится в памяти и сбрасывается при перезапуске
- **Dockerfile** использует `python:3.12-slim` — лёгкий образ, ~120 MB

## Обновление кода

После изменений в коде — просто запушите в GitHub:

```bash
cd d:\prjs\smart\cursor\video_downloader\web_service
git add .
git commit -m "Описание изменений"
git push
```

Railway автоматически перезапустит сервис (при подключении через GitHub).

## Полезные ссылки

- [Railway Dashboard](https://railway.app/dashboard)
- [Railway Documentation](https://docs.railway.app)
- [GitHub репозиторий](https://github.com/Solowawe/saby-video-downloader)