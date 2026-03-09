# bot/presentation/handlers/info.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_media_info
from bot.presentation.common.handler_decorators import handle_user_errors

import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
async def info_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    if chat_id is None:
        logger.warning('info_command: chat_id is None.')
        return

    username = update.effective_user.first_name or 'Anonym'
    user_msg = update.message.text

    # Идентификатор для логгера
    local_id = f'info_command:{username}'
    logger.info(f'[{local_id}] user_msg={user_msg}')

    media_info = context.user_data.get('media_info')
    await send_media_info(
        chat_id,
        context.bot,
        media_info,
        details=True
    )
