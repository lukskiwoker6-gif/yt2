import os
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

from config import BOT_TOKEN
from downloader import download_video


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Пришли ссылку на видео.\n"
        "Выберешь качество — получишь файл."
    )


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        return

    context.user_data["url"] = url

    keyboard = [
        [
            InlineKeyboardButton("360p", callback_data="360"),
            InlineKeyboardButton("720p", callback_data="720"),
        ],
        [
            InlineKeyboardButton("1080p", callback_data="1080"),
            InlineKeyboardButton("MP3", callback_data="mp3"),
        ],
    ]

    await update.message.reply_text(
        "Выбери качество:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def choose_quality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    url = context.user_data.get("url")
    quality = q.data

    if not url:
        await q.edit_message_text("Ссылка устарела. Пришли заново.")
        return

    await q.edit_message_text("Скачиваю...")

    try:
        path, title = download_video(url, quality)
        await q.message.reply_document(
            document=open(path, "rb"),
            caption=f"{title} ({quality})"
        )
        os.remove(path)
    except Exception as e:
        await q.edit_message_text(f"Ошибка: {e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(choose_quality))

    print("BOT STARTED — FINAL VERSION")
    app.run_polling()


if __name__ == "__main__":
    main()
