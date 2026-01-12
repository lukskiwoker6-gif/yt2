from telegram import Update
from telegram.ext import ContextTypes
from config import CHANNEL_USERNAME
from database import is_paid


async def has_access(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id

    if is_paid(user_id):
        return True

    try:
        member = await context.bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except:
        return False
