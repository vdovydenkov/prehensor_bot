# bot/presentation/handlers/info.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_media_info
from bot.presentation.handlers.common.handler_decorators import (
    CommandContext,
    handle_user_errors,
    prepare_handler_context,
)

import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
@prepare_handler_context
async def info_command(
    update:  Update,
    context: ContextTypes.DEFAULT_TYPE,
    ctx:     CommandContext,
) -> None:
    ctx.user_service._check_user(
        ctx.domain_user,
    )

    media_info = context.user_data.get('media_info')
    await send_media_info(
        ctx.chat.id,
        context.bot,
        media_info,
        details=True
    )
