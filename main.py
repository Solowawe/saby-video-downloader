"""
Saby Video Downloader — Web Service.

FastAPI + Jinja2 веб-сервис для получения прямых CDN ссылок на видео с saby.ru.
Принимает URL страницы плеера (play.saby.ru/multimedia-converter/embed/...)
и возвращает прямую ссылку на mp4 с cdn-disk.sbis.ru.

Деплой: Render.com (Web Service)
Запуск локально: uvicorn main:app --reload
"""
import json
import logging
import os
import re
from datetime import datetime
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# FastAPI приложение
app = FastAPI(
    title="Saby Video Downloader",
    description="Веб-сервис для получения прямых CDN ссылок на видео с saby.ru",
    version="1.0.0",
)

# Подключаем статику и шаблоны
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Хранилище истории запросов (в памяти, без БД)
history: list[dict] = []
MAX_HISTORY = 20


# ===== Pydantic модели =====

class ExtractRequest(BaseModel):
    """Запрос на извлечение CDN ссылки."""
    url: str


class ExtractResponse(BaseModel):
    """Ответ с CDN ссылкой."""
    success: bool
    cdn_url: Optional[str] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    content_length_str: Optional[str] = None
    accessible: Optional[bool] = None
    error: Optional[str] = None


# ===== Логика извлечения CDN URL =====

def _build_cdn_url_from_page_url(page_url: str) -> Optional[str]:
    """
    Формирует CDN URL из URL страницы плеера Saby.

    Формат page_url:
        https://play.saby.ru/multimedia-converter/embed/{UUID1}_{UUID2}

    Формат CDN URL:
        https://cdn-disk.sbis.ru/disk/api/v1/{UUID1}_{UUID2}
    """
    if not page_url:
        return None

    # Проверяем, что это ссылка на плеер Saby
    if "play.saby.ru/multimedia-converter/embed/" not in page_url:
        return None

    # Извлекаем UUID из URL
    # Паттерн: UUID1_UUID2 (или просто UUID)
    match = re.search(
        r'/embed/([a-f0-9\-]+(?:_[a-f0-9\-]+)?)',
        page_url,
        re.IGNORECASE
    )
    if not match:
        return None

    uuid_part = match.group(1)
    cdn_url = f"https://cdn-disk.sbis.ru/disk/api/v1/{uuid_part}"
    return cdn_url


def _format_size(size_bytes: Optional[int]) -> str:
    """Форматирует размер в человекочитаемый вид."""
    if size_bytes is None:
        return "неизвестно"
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


async def _check_url_accessible(url: str) -> dict:
    """
    Проверяет доступность CDN URL через HEAD-запрос.
    Возвращает словарь с информацией о файле.
    """
    result = {
        "accessible": False,
        "content_type": None,
        "content_length": None,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.head(url)

            if response.status_code == 200:
                result["accessible"] = True
                result["content_type"] = response.headers.get("content-type")
                content_length = response.headers.get("content-length")
                if content_length:
                    result["content_length"] = int(content_length)
            elif response.status_code == 403:
                # CDN может возвращать 403 на HEAD, но GET работает
                # Пробуем GET с range=0-0
                try:
                    range_resp = await client.get(url, headers={"Range": "bytes=0-0"})
                    if range_resp.status_code in (200, 206):
                        result["accessible"] = True
                        content_length = range_resp.headers.get("content-range", "")
                        # Парсим Content-Range: bytes 0-0/123456789
                        range_match = re.search(r'/(\d+)$', content_length)
                        if range_match:
                            result["content_length"] = int(range_match.group(1))
                        result["content_type"] = range_resp.headers.get("content-type")
                except Exception:
                    pass
            logger.info(
                f"CDN check: {url} -> status={response.status_code}, "
                f"accessible={result['accessible']}"
            )
    except Exception as e:
        logger.warning(f"CDN check failed for {url}: {e}")

    return result


# ===== API Endpoints =====

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница сервиса."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "history": history}
    )


@app.post("/api/extract", response_model=ExtractResponse)
async def extract_cdn(req: ExtractRequest):
    """
    Извлекает CDN ссылку из URL страницы плеера Saby.

    Принимает URL вида:
        https://play.saby.ru/multimedia-converter/embed/{UUID1}_{UUID2}

    Возвращает прямую ссылку на mp4:
        https://cdn-disk.sbis.ru/disk/api/v1/{UUID1}_{UUID2}
    """
    url = req.url.strip()

    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    # Формируем CDN URL
    cdn_url = _build_cdn_url_from_page_url(url)

    if not cdn_url:
        error_msg = (
            "Неверный формат URL. Ожидается ссылка на плеер Saby:\n"
            "https://play.saby.ru/multimedia-converter/embed/..."
        )
        # Добавляем в историю даже ошибки
        history_entry = {
            "input_url": url,
            "success": False,
            "error": error_msg,
            "timestamp": datetime.now().isoformat(),
        }
        history.insert(0, history_entry)
        if len(history) > MAX_HISTORY:
            history.pop()

        return ExtractResponse(success=False, error=error_msg)

    # Проверяем доступность CDN ссылки
    check_result = await _check_url_accessible(cdn_url)

    # Формируем имя файла
    uuid_match = re.search(r'/api/v1/(.+)$', cdn_url)
    filename = f"{uuid_match.group(1).replace('_', '_')}.mp4" if uuid_match else "video.mp4"

    # Форматируем размер
    content_length = check_result.get("content_length")
    content_length_str = _format_size(content_length)

    # Добавляем в историю
    history_entry = {
        "input_url": url,
        "success": True,
        "cdn_url": cdn_url,
        "filename": filename,
        "content_length_str": content_length_str,
        "accessible": check_result.get("accessible", False),
        "timestamp": datetime.now().isoformat(),
    }
    history.insert(0, history_entry)
    if len(history) > MAX_HISTORY:
        history.pop()

    return ExtractResponse(
        success=True,
        cdn_url=cdn_url,
        filename=filename,
        content_type=check_result.get("content_type"),
        content_length=content_length,
        content_length_str=content_length_str,
        accessible=check_result.get("accessible", False),
    )


@app.get("/api/history")
async def get_history():
    """Возвращает историю запросов."""
    return {"history": history}


@app.get("/health")
async def health():
    """Health check для Render.com."""
    return {"status": "ok"}


# ===== Точка входа =====

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)