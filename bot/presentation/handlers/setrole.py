# bot/presentation/handlers/setrole.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.presentation.messaging.telegram_messenger import send_text
from bot.presentation.handlers.common.handler_decorators import (
    CommandContext,
    handle_user_errors,
    prepare_handler_context,
)

import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
@prepare_handler_context
async def set_role_command(
    update:  Update,
    context: ContextTypes.DEFAULT_TYPE,
    ctx:     CommandContext,
) -> None:
    service = ctx.user_service

    # Приводит к верхнему регистру, убирает пробелы и отрезает "/SetRole".
    target_role = _parse_command(ctx.message.text)

    assigned_role = await service.set_role(
        ctx.domain_user,
        target_role
    )

    msg_for_user = (
        f'Роль "{assigned_role.value}" установлена.'
        if assigned_role
        else 'Роль не установлена.'
    )

    await send_text(
        context.bot,
        ctx.chat.id,
        msg_for_user,
    )

def _parse_command(msg: str) -> str:
    '''Приводит к верхнему регистру, убирает пробелы и отрезает "/SetRole".'''
    return (
        msg
        .strip()
        .upper()
        .removeprefix('/SETROLE ')
    )
