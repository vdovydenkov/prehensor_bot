# bot/handlers/download.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.fetcher import fetch_url
from bot.core.messenger import send_media, send_to_chat

import logging
logger = logging.getLogger('prehensor')

async def download_command(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
    chat_id = update.effective_chat.id
    if chat_id is None:
        logger.warning('download_command: chat_id is None.')
        return

    username = update.effective_user.first_name or 'Anonym'
    user_msg = update.message.text

    # Идентификатор для логгера
    local_id = f'download_command:{username}'

    logger.info(f'[{local_id}] user_msg={user_msg}')

    cfg = context.bot_data['cfg']
    url = context.user_data.get('url')
    if not url:
        logger.warning(f'[{local_id}] url пустой.')
        return await send_to_chat(chat_id, context.bot, cfg.msg.no_link)
    media_info = await fetch_url(url, update, context, download=True)
    if not media_info:
        logger.warning(f'[{local_id}] media_info не содержит данных.')
        return await send_to_chat(
                              chat_id,
                              context.bot,
                              cfg.err.download_failed
                          )
    context.user_data['media_info'] = media_info
    await send_media(
        chat_id,
        context.bot,
        media_info,
    )
