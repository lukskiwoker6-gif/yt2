import os
import uuid
import yt_dlp
from config import DOWNLOAD_DIR, COOKIES_FILE


FORMATS = {
    "360": (
        "bv*[ext=mp4][height<=360]/"
        "bv*[height<=360]/"
        "best[height<=360]/best"
    ),
    "720": (
        "bv*[ext=mp4][height<=720]/"
        "bv*[height<=720]/"
        "best[height<=720]/best"
    ),
    "1080": (
        "bv*[ext=mp4][height<=1080]/"
        "bv*[height<=1080]/"
        "best[height<=1080]/best"
    ),
    "mp3": "bestaudio/best",
}


def download_video(url: str, quality: str):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "format": FORMATS.get(quality, FORMATS["720"]),
        "outtmpl": f"{filepath}.%(ext)s",
        "merge_output_format": "mp4",
        "cookiefile": COOKIES_FILE,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "retries": 3,
        "fragment_retries": 3,
        "concurrent_fragment_downloads": 8,
    }

    if quality == "mp3":
        ydl_opts.update({
            "extract_audio": True,
            "audio_format": "mp3",
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = info.get("ext", "mp4")

    return f"{filepath}.{ext}", info.get("title", "video")
