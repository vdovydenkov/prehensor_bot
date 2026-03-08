# bot/presentation/handlers/statistic.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.presentation.formaters.list_formater import format_list
from bot.application.exceptions import (
    UserServiceError,
    UserNotFoundError,
    UserBlockedError,
    AccessDeniedError,
)
import logging
logger = logging.getLogger('prehensor')

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

    user = await service.get_or_create_user(
        update.effective_user
    )
    user_msg = update.message.text

    # Идентификатор для логгера - добавляем имя пользователя
    local_id = f'statistic_command:{user.name}'

    logger.info(f'[{local_id}] user_msg={user_msg}')

    msg_to_user = None
    try:
        users = await service.list_users(user.tg_id)
        msg_to_user = format_list(users)
    except UserNotFoundError as e:
        msg = str(e)
        logger.warning(msg)
        msg_to_user = 'Возникла ошибка при получении статистики.'
    except UserBlockedError as e:
        msg = str(e)
        logger.warning(msg)
        msg_to_user = 'Ваш доступ заблокирован. Вы не можете выполнять никаких действий.'
    except AccessDeniedError as e:
        msg = str(e)
        logger.warning(msg)
        msg_to_user = 'У вас нет прав на просмотр статистики.'
    except UserServiceError as e:
        msg = str(e)
        logger.warning(msg)
        msg_to_user = 'Возникла ошибка при формировании статистики.'
    except Exception as e:
        logger.error("Formatter error", exc_info=e)
        msg_to_user = "Возникла ошибка при формировании списка пользователей."

    await send_to_chat(
        chat_id,
        context.bot,
        msg_to_user,
    )
