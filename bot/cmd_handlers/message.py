# bot/handlers/message.py

import logging
logger = logging.getLogger('prehensor')

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.validators import is_http_url
from bot.core.fetcher import fetch_url
from bot.core.messenger import send_to_chat, show_media_info

async def message_processor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.first_name or 'Anonym'
    text = update.message.text or ""

    logger.info(f'[{username}] В чат прислали: {text}')

    cfg = context.bot_data['cfg']

    logger.debug(f'[{username}] Проверяем http-валидатором.')
    if not is_http_url(text):
        return await send_to_chat(update, context, cfg.msg.command_or_link)

    await send_to_chat(update, context, cfg.msg.check_link)
    logger.debug(f'[{username}] Отправляем в fetcher/fetch_url.')
    info = await fetch_url(text, update, context, download=False)
    if info:
        logger.info(f'[{username}] Получили info от fetch_url, сохраняем в контекст и отправляем core/messenger/show_media_info')
        context.user_data['media_info'] = info
        context.user_data['url'] = text
        await show_media_info(update, context, details=False)
