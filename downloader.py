import os
import uuid
import yt_dlp
from config import DOWNLOAD_DIR, COOKIES_FILE, ARIA2_PATH


def download_video(url: str):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "format": "bv*+ba/best",
        "outtmpl": filepath,
        "merge_output_format": "mp4",
        "cookies": COOKIES_FILE,
        "external_downloader": "aria2c",
        "external_downloader_args": [
            "-x", "16",
            "-k", "1M"
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return filepath, info.get("title", "video")
