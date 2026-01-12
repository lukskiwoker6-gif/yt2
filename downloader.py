import os
import uuid
import yt_dlp
from config import DOWNLOAD_DIR, COOKIES_FILE


def download_video(url: str):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        # 🔥 Главное: fallback-цепочка, НИКАКИХ "="
        "format": (
            "bv*[ext=mp4][height<=1080]/"
            "bv*[ext=mp4][height<=720]/"
            "bv*[ext=mp4][height<=480]/"
            "best[ext=mp4]/best"
        ),

        "outtmpl": filepath,
        "merge_output_format": "mp4",

        # ✅ cookies реально используются
        "cookiefile": COOKIES_FILE,

        # стабильность
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,

        # retry
        "retries": 3,
        "fragment_retries": 3,

        # ускорение
        "concurrent_fragment_downloads": 8,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return filepath, info.get("title", "video")
