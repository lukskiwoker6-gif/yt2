import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes,
    filters, PreCheckoutQueryHandler
)

from config import BOT_TOKEN, ADMIN_IDS, CHANNEL_USERNAME
from downloader import download_video
from access import has_access
from payments import stars_invoice
from database import set_paid, add_stat, total_downloads
from database import set_channel, get_channel


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Пришли ссылку на видео.\n\n"
        "🔒 Бесплатно — подпишись на канал\n"
        f"{CHANNEL_USERNAME}\n\n"
        "💰 Или купи безлимит навсегда — 299⭐"
    )


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        **stars_invoice()
    )


async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_paid(update.effective_user.id)
    await update.message.reply_text("✅ Безлимит активирован навсегда!")


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    await update.message.reply_text(
        f"📊 Total downloads: {total_downloads()}"
    )

async def setchannel(update, context):
    if update.effective_user.id not in ADMIN_IDS:
        return

    if not context.args:
        await update.message.reply_text("Используй: /setchannel @channel")
        return

    channel = context.args[0]
    set_channel(channel)
    await update.message.reply_text(f"✅ Канал установлен: {channel}")

async def getchannel(update, context):
    if update.effective_user.id not in ADMIN_IDS:
        return

    ch = get_channel()
    await update.message.reply_text(f"Текущий канал: {ch}")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await has_access(update, context):
        await update.message.reply_text(
            "❌ Нет доступа.\n"
            f"Подпишись на {CHANNEL_USERNAME}\n"
            "или купи безлимит /buy"
        )
        return

    msg = await update.message.reply_text("⏳ Скачиваю...")

    try:
        path, title = download_video(update.message.text)
        await msg.edit_text("📤 Отправляю...")

        await update.message.reply_document(
            document=open(path, "rb"),
            caption=f"🎬 {title}"
        )

        add_stat(update.effective_user.id)
        os.remove(path)

    except Exception as e:
        await msg.edit_text(f"❌ Ошибка: {e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CommandHandler("setchannel", setchannel))
    app.add_handler(CommandHandler("getchannel", getchannel))

    print("✅ Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
