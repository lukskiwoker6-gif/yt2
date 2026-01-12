import os
import uuid
import yt_dlp
from config import DOWNLOAD_DIR, COOKIES_FILE


def download_video(url: str):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        # Лучшее видео + аудио, без экспериментов
        "format": "bestvideo+bestaudio/best",

        "outtmpl": filepath,
        "merge_output_format": "mp4",

        # ВАЖНО: cookies реально используются
        "cookiefile": COOKIES_FILE,

        # Анти-детект
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,

        # Поведение как браузер
        "extractor_args": {
            "youtube": {
                "player_client": ["web", "android"],
                "skip": ["dash", "hls"],
            }
        },

        # Тайминги
        "retries": 3,
        "fragment_retries": 3,
        "concurrent_fragment_downloads": 4,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return filepath, info.get("title", "video")
