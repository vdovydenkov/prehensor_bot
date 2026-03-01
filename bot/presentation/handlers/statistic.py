# bot/presentation/handlers/statistic.py
import logging
logger = logging.getLogger('prehensor')

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.infra.config.configurator import Cfg
from bot.infra.config.defaults import DEFAULT_RAW_CONFIG
from bot.presentation.formaters.list_formater import format_list

async def statistic_command(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
    local_id = f'statistic_command'

    chat_id = update.effective_chat.id
    if chat_id is None:
        logger.warning(f'[{local_id}] chat_id is None.')
        return

    service = context.bot_data.get('service')
    if service is None:
        logger.error(f'[{local_id}] User service is None!')
        return

    tg_user = update.effective_user
    username = tg_user.first_name or 'Anonym'
    user_msg = update.message.text

    # Идентификатор для логгера - добавляем имя пользователя
    local_id = f'statistic_command:{username}'

    logger.info(f'[{local_id}] user_msg={user_msg}')

    try:
        users = await service.list_users(tg_user.id)
        text = format_list(users)
    except Exception as e:
        logger.error("Formatter error", exc_info=e)
        text = "Возникла ошибка при формировании списка пользователей."

    await send_to_chat(
        chat_id,
        context.bot,
        text,
    )
