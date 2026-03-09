# bot/presentation/handlers/statistic.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.presentation.formaters.list_formater import format_list
from bot.presentation.common.handler_decorators import handle_user_errors
import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
async def statistic_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    local_id = 'statistic_command'

    chat_id = update.effective_chat.id
    if chat_id is None:
        logger.warning(f'[{local_id}] chat_id is None.')
        return

    service = context.bot_data.get('service')
    if service is None:
        logger.error(f'[{local_id}] User service is None!')
        return

    user_msg = update.message.text
    if not user_msg:
        logger.error(f'[{local_id}] update.message.text is empty!')
        return

    user = await service.get_user_by_id(
        update.effective_user.id
    )

    users = await service.list_users(user)
    msg_for_user = format_list(users)

    await send_to_chat(
        chat_id,
        context.bot,
        msg_for_user,
    )
