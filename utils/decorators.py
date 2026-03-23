from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from database import AsyncSessionLocal
from models import User
from sqlalchemy import select

def require_not_banned(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user and user.is_banned:
                await update.message.reply_text("❌ Anda telah dibanned dari bot ini.")
                return
        return await func(update, context, *args, **kwargs)
    return wrapper
