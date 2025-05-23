# bot/handlers/download.py

import logging
logger = logging.getLogger('prehensor')

from telegram import Update
from telegram.ext import ContextTypes
from bot.core.fetcher import fetch_url
from bot.core.messenger import send_media, send_to_chat

async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.first_name or 'Anonym'
    user_msg = update.message.text

    logger.info(f'[{username}] /download, text={user_msg}')

    cfg = context.bot_data['cfg']
    url = context.user_data.get('url')
    if not url:
        logger.warning(f'[{username}] url пустой.')
        return await send_to_chat(update, context, cfg.msg.no_link)
    logger.debug(f'[{username}] Передаём данные в core/fetcher/fetch_url, URL={url}')
    media_info = await fetch_url(url, update, context, download=True)
    if not media_info:
        logger.warning(f'[{username}] media_info пустой.')
        return await send_to_chat(update, context, cfg.err.download_failed)
    context.user_data['media_info'] = media_info
    logger.debug(f'[{username}] Запускаем core/messenger/send_media.')
    await send_media(update, context)
