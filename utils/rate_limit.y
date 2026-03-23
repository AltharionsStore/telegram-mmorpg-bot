from functools import wraps
from collections import defaultdict
import time
from telegram import Update
from telegram.ext import ContextTypes

rate_limits = defaultdict(list)

def rate_limit(limit_per_second=1, time_window=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            now = time.time()
            # bersihkan request lama
            rate_limits[user_id] = [t for t in rate_limits[user_id] if now - t < time_window]
            if len(rate_limits[user_id]) >= limit_per_second:
                await update.message.reply_text("⏳ Terlalu banyak permintaan, coba lagi nanti.")
                return
            rate_limits[user_id].append(now)
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator
