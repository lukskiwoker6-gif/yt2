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
        "👋 Пришли ссылку на видео.\n"
        "Я предложу выбрать качество."
    )


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.startswith("http"):
        return

    context.user_data["url"] = text

    keyboard = [
        [
            InlineKeyboardButton("🎬 360p", callback_data="360"),
            InlineKeyboardButton("🎬 720p", callback_data="720"),
        ],
        [
            InlineKeyboardButton("🎬 1080p", callback_data="1080"),
            InlineKeyboardButton("🎵 MP3", callback_data="mp3"),
        ]
    ]

    await update.message.reply_text(
        "Выбери качество:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def quality_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    quality = query.data
    url = context.user_data.get("url")

    if not url:
        await query.edit_message_text("❌ Ссылка устарела, пришли заново.")
        return

    await query.edit_message_text("⏳ Скачиваю...")

    try:
        path, title = download_video(url, quality)

        await query.message.reply_document(
            document=open(path, "rb"),
            caption=f"🎬 {title}\nКачество: {quality}"
        )

        os.remove(path)

    except Exception as e:
        await query.edit_message_text(f"❌ Ошибка: {e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(quality_chosen))

    print("✅ Bot started (mode 2: quality selection)")
    app.run_polling()


if __name__ == "__main__":
    main()
