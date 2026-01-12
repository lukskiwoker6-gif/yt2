import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, ADMIN_IDS
from downloader import download_video


def is_admin(update: Update) -> bool:
    return update.effective_user.id in ADMIN_IDS


# ---------- COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Пришли ссылку на видео.\n"
        "Я скачаю и пришлю файл."
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    await update.message.reply_text(
        "🛠 Админ-панель\n\n"
        f"👤 Your ID: {update.effective_user.id}\n"
        f"📊 Users: (позже)\n"
    )


# ---------- MAIN HANDLER ----------

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.startswith("http"):
        return

    msg = await update.message.reply_text("⏳ Скачиваю видео...")

    try:
        path, title, size, duration = download_video(text)

        await msg.edit_text("📤 Отправляю в Telegram...")

        # 👉 ВСЕГДА отправляем как document
        await update.message.reply_document(
            document=open(path, "rb"),
            caption=f"🎬 {title}\n📦 {(size / 1024 / 1024):.1f} MB",
        )

        os.remove(path)

    except Exception as e:
        await msg.edit_text(f"❌ Ошибка:\n{e}")


# ---------- ENTRY ----------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    print("✅ Downloader bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
