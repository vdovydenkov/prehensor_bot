from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.validators import is_http_url
from bot.core.fetcher import fetch_url
from bot.core.messenger import send_to_chat, show_media_info

async def message_processor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    cfg = context.bot_data['cfg']

    if not is_http_url(text):
        return await send_to_chat(update, context, cfg.msg.command_or_link)

    await send_to_chat(update, context, cfg.msg.check_link)
    info = await fetch_url(text, update, context, download=False)
    if info:
        context.user_data['media_info'] = info
        context.user_data['url'] = text
        await show_media_info(update, context, details=False)
