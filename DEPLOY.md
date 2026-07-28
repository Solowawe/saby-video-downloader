# Инструкция по деплою на Railway.app

## Шаг 1: Создать аккаунт на Railway.app

1. Откройте https://railway.app
2. Нажмите **Start a New Project** или **Login**
3. Выберите **Continue with GitHub**
4. Авторизуйте Railway.app для доступа к вашему GitHub аккаунту
5. Подтвердите email (если потребуется)

## Шаг 2: Развернуть сервис

### Способ A — Через GitHub (рекомендуемый)

1. На панели Railway.app нажмите **New Project**
2. Выберите **Deploy from GitHub repo**
3. Выберите репозиторий `Solowawe/saby-video-downloader`
4. Railway автоматически определит Python и запустит сборку

### Способ B — Через Railway CLI

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

## Шаг 3: Настройки проекта

Railway.app автоматически определит настройки из `requirements.txt`, но нужно проверить:

1. Откройте проект в Railway Dashboard
2. Перейдите в **Variables**
3. Убедитесь, что переменная `PORT` установлена автоматически (Railway добавляет её сам)
4. Перейдите в **Settings** → **Deploy**

Проверьте команды (должны определиться автоматически, но если нет — укажите вручную):

| Параметр | Значение |
|----------|----------|
| **Root Directory** | (оставьте пустым) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

> **Важно:** `runtime.txt` удалён из репозитория, т.к. mise (менеджер версий Python на Railway) не имеет предварительно собранных бинарников для `python-3.11.0`. Railway сам выберет подходящую версию Python (3.12+). Все зависимости совместимы.

## Шаг 4: Дождаться деплоя

1. Railway автоматически запустит сборку и развёртывание
2. Статус изменится с **Deploying** на **Running** (обычно 1-3 минуты)
3. Нажмите на **Generate Domain** или используйте автоматически сгенерированный URL вида:
   ```
   https://saby-video-downloader.up.railway.app
   ```

## Шаг 5: Проверка

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