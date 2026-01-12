from config import CHANNEL_USERNAME, ADMIN_IDS
from database import is_paid


async def has_access(update, context) -> bool:
    user_id = update.effective_user.id

    # ✅ АДМИН — ВСЕГДА ДОСТУП
    if user_id in ADMIN_IDS:
        return True

    # 💰 ПЛАТНЫЙ — ДОСТУП
    if is_paid(user_id):
        return True

    # 🔒 ПРОВЕРКА ПОДПИСКИ
    try:
        member = await context.bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except:
        return False
