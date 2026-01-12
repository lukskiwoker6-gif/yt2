import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8228248528:AAFc0uNIquzw2U9eTz42XyTD_jCudupyO-U")

# 👉 ВСТАВЬ СВОЙ TELEGRAM ID
ADMIN_IDS = [1436019784]

# YouTube cookies
COOKIES_FILE = "cookies.txt"

# папка для загрузок
DOWNLOAD_DIR = "downloads"

# максимальный размер для отправки как video (Telegram Bot API)
TG_VIDEO_LIMIT = 2 * 1024 * 1024 * 1024  # 2GB
