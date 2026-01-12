from config import ADMIN_IDS
from database import is_paid, get_channel


async def has_access(update, context) -> bool:
    user_id = update.effective_user.id

    if user_id in ADMIN_IDS:
        return True

    if is_paid(user_id):
        return True

    channel = get_channel()
    if not channel:
        return True  # если канал не задан

    try:
        member = await context.bot.get_chat_member(channel, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False
