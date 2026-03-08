# bot/presentation/handlers/setrole.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.application.exceptions import (
    RoleNotFoundError,
)
import logging
logger = logging.getLogger('prehensor')

async def set_role_command(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
    local_id = 'set_role_command'

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
        return

    user = await service.get_or_create_user(
        update.effective_user
    )

    # Идентификатор для логгера - добавляем имя пользователя
    local_id = f'set_role_command:{user.name}'

    logger.info(f'[{local_id}] user_msg={user_msg}')

    msg_for_user = None
    # Отрезаем от сообщения команду: берем только то, что через пробел
    target_role = (
        user_msg
        .strip()
        .upper()
        .removeprefix('/SETROLE ')
    )

    try:
        assigned_role = await service.set_role(
            user,
            target_role
        )
        msg_for_user = f'Роль "{assigned_role.value or 'None'}" установлена.'
    except RoleNotFoundError as e:
        msg = str(e)
        logger.error(f'[{local_id}] {msg}')
        msg_for_user = 'Такой роли не существует.'
    except Exception:
        logger.exception('Set role failed.')
        msg_for_user = 'Не удалось установить роль.'

    await send_to_chat(
        chat_id,
        context.bot,
        msg_for_user,
    )
