import os
import uuid
import yt_dlp
from config import COOKIES_FILE, DOWNLOAD_DIR


def download_video(url: str):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "format": "bv*+ba/best",
        "outtmpl": filepath,
        "merge_output_format": "mp4",
        "cookies": COOKIES_FILE,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    size = os.path.getsize(filepath)

    title = info.get("title", "video")
    duration = info.get("duration", 0)

    return filepath, title, size, duration
