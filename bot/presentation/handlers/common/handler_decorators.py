# bot/presentation/handlers/common/handler_decorators.py

from dataclasses import dataclass
from functools import wraps
from telegram import Update, Chat, Message
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.application.exceptions import (
    UserServiceError,
    AccessDeniedError,
    UserBlockedError,
    UserNotFoundError,
    RoleNotFoundError,
)

from bot.application.user_service import UserService
from bot.domain.models.user import DomainUser

import logging
logger = logging.getLogger("prehensor")

@dataclass
class CommandContext:
    user_service: UserService
    chat:         Chat
    domain_user:  DomainUser
    message:      Message

# --- Decorators

def handle_user_errors(func):

    @wraps(func)
    async def wrapper(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        *args,
        **kwargs
    ):

        msg_for_user    = 'Возникла ошибка при обработке команды. Администратор уведомлен.'
        msg_for_error   = ''
        msg_for_warning = 'Something wrong in command handlers.'

        user = update.effective_user

        user_id    = user.id if user else "unknown"
        user_name  = getattr(user, "name", "unknown")
        user_label = f'[{user_name}:{user_id}]'

        try:
            return await func(update, context, *args, **kwargs)

        except UserServiceError as e:
            error_message = str(e)
            msg_for_user  = 'Возникла ошибка при выполнении команды. Администратор уведомлен.'
            msg_for_error = (
                f'{user_label} UserService internal error.\n'
                f'{error_message}'
            )

        except AccessDeniedError:
            msg_for_user    = 'Недостаточно прав для выполнения команды.'
            msg_for_warning = f'{user_label} Access denied.'

        except UserBlockedError:
            msg_for_user    = 'Ваш пользователь заблокирован.'
            msg_for_warning = f'{user_label} Tried to command by blocked user.'

        except UserNotFoundError:
            msg_for_user    = 'Пользователь не найден.'
            msg_for_warning = f'{user_label} User not found.'

        except RoleNotFoundError:
            msg_for_user = 'Такой роли не существует.'

        if msg_for_warning:
            # Добавляем в лог id чата, пользователя и сообщение из update
            msg_for_warning += (
                f"\nUpdate info:"
                f"\nchat_id={update.effective_chat.id if update.effective_chat else 'None'}"
                f"\nuser_id={update.effective_user.id if update.effective_user else 'None'}"
                f"\ntext={getattr(update.effective_message, 'text', None)}"
            )

            logger.warning(msg_for_warning)
        elif msg_for_error:
            logger.error(msg_for_error)

        await send_to_chat(
            update.effective_chat.id,
            context.bot,
            msg_for_user,
        )
    
    return wrapper


def prepare_handler_context(func):

    @wraps(func)
    async def wrapper(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        *args,
        **kwargs
    ):

        chat = update.effective_chat
        user = update.effective_user
        msg  = update.effective_message

        missing = []
        if not chat:
            missing.append('chat')
        if not msg:
            missing.append('message')
        if not user:
            missing.append('user')

        if missing:
            logger.warning(
                'Update missing %s chat_id=%s user_id=%s msg=%s',
                '/'.join(missing),
                chat.id  if chat else None,
                user.id  if user else None,
                msg.text if msg  else None,
            )
            return

        service: UserService = context.bot_data.get("service")
        if not service:
            logger.error(
                'User service is not initialized. Chat_id=%s User_id=%s',
                chat.id,
                user.id,
            )
            return

        domain_user = await service.get_user_by_id(user.id)

        ctx = CommandContext(
            service,
            chat,
            domain_user,
            message=msg,
        )
        return await func(
            update,
            context,
            ctx,
            *args,
            **kwargs
        )

    return wrapper

