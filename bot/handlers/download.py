from telegram import Update
from telegram.ext import ContextTypes
from bot.core.fetcher import fetch_url
from bot.core.messenger import send_media, send_to_chat

async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cfg = context.bot_data['cfg']
    url = context.user_data.get('url')
    if not url:
        return await send_to_chat(update, context, cfg.msg.no_link)
    media_info = await fetch_url(url, update, context, download=True)
    if not media_info:
        return await send_to_chat(update, context, cfg.err.download_failed)
    context.user_data['media_info'] = media_info
    await send_media(update, context)
