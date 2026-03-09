# bot/presentation/handlers/statistic.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
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

    await send_to_chat(
        ctx.chat.id,
        context.bot,
        msg_for_user,
    )
