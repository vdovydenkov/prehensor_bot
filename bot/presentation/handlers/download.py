# bot/presentation/handlers/download.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.fetcher import fetch_url
from bot.core.messenger import send_media, send_to_chat
from bot.presentation.handlers.common.handler_decorators import (
    CommandContext,
    handle_user_errors,
    prepare_handler_context,
)

import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
@prepare_handler_context
async def download_command(
    update:  Update,
    context: ContextTypes.DEFAULT_TYPE,
    ctx:     CommandContext,
) -> None:
    ctx.user_service._check_user(
        ctx.domain_user,
    )

    # Идентификатор для логгера
    local_id = f'download_command:{ctx.domain_user.name}'

    cfg = context.bot_data['cfg']
    url = context.user_data.get('url')
    if not url:
        logger.warning(f'[{local_id}] url пустой.')
        return await send_to_chat(
            ctx.chat.id,
            context.bot,
            cfg.msg.no_link
        )

    media_info = await fetch_url(url, update, context, download=True)
    if not media_info:
        logger.warning(f'[{local_id}] media_info не содержит данных.')
        return await send_to_chat(
            ctx.chat.id,
            context.bot,
            cfg.err.download_failed,
        )

    context.user_data['media_info'] = media_info

    await send_media(
        ctx.chat.id,
        context.bot,
        media_info,
    )
