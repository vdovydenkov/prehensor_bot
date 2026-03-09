# bot/presentation/handlers/statistic.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.presentation.messaging.telegram_messenger import send_text
from bot.presentation.formaters.list_formater import format_list
from bot.presentation.handlers.common.handler_decorators import (
    CommandContext,
    handle_user_errors,
    prepare_handler_context,
)

import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
@prepare_handler_context
async def statistic_command(
    update:  Update,
    context: ContextTypes.DEFAULT_TYPE,
    ctx:     CommandContext,
) -> None:
    service = ctx.user_service

    users = await service.list_users(ctx.domain_user)

    msg_for_user = format_list(users)

    await send_text(
        context.bot,
        ctx.chat.id,
        msg_for_user,
    )
