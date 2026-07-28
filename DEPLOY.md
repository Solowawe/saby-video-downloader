# Инструкция по деплою на Render.com

## Шаг 1: Создать репозиторий на GitHub

1. Откройте https://github.com/new
2. **Repository name:** `saby-video-downloader`
3. **Public** (обязательно для бесплатного тарифа Render)
4. **Не** нажимайте "Add a README" (у нас уже есть)
5. Нажмите **Create repository**

## Шаг 2: Загрузить код в репозиторий

После создания репозитория, выполните в терминале:

```bash
# Перейти в папку web_service
cd d:\prjs\smart\cursor\video_downloader\web_service

# Инициализировать git
git init
git add .
git commit -m "Initial commit: Saby Video Downloader web service"

# Подключить ваш репозиторий (ЗАМЕНИТЕ username на ваш GitHub логин!)
git remote add origin https://github.com/username/saby-video-downloader.git

# Отправить код
git branch -M main
git push -u origin main
```

## Шаг 3: Создать аккаунт на Render.com

1. Откройте https://render.com
2. Нажмите **Get started** или **Sign up**
3. Выберите **Continue with GitHub**
4. Разрешите доступ к репозиторию `saby-video-downloader`

## Шаг 4: Создать Web Service

1. На панели Render нажмите **New +** → **Web Service**
2. Выберите репозиторий `saby-video-downloader`
3. Настройки:

| Параметр | Значение |
|----------|----------|
| **Name** | `saby-video-downloader` |
| **Region** | `Frankfurt (EU)` (ближе всего к России) |
| **Branch** | `main` |
| **Root Directory** | (оставьте пустым, т.к. репозиторий содержит только web_service) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | **Free** |

4. Нажмите **Create Web Service**

## Шаг 5: Готово!

Через 2-3 минуты сервис будет доступен по адресу:
```
https://saby-video-downloader.onrender.com
```

**Важно:** На бесплатном тарифе Render сервис "засыпает" после 15 минут бездействия.
Первый запрос после сна может занимать 10-30 секунд (пробуждение).

## Проверка

Откройте в браузере:
```
https://saby-video-downloader.onrender.com/health
```
Должен вернуться `{"status": "ok"}`.

## Обновление кода

После изменений в коде:
```bash
cd d:\prjs\smart\cursor\video_downloader\web_service
git add .
git commit -m "Описание изменений"
git push
```

Render автоматически перезапустит сервис.